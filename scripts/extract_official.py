#!/usr/bin/env python3
"""extract_official.py — parse src/<comp>/demos/{enUS,zhCN}/index.demo-entry.md
in the cached tusen-ai/naive-ui checkout and produce
assets/data/official-manifest.generated.json.

Zero external dependencies. Reuses the same parsing logic as the original
Node extractor (parseTable / splitRow / extractDemos), translated to Python.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_META = PROJECT_ROOT / "assets" / "data" / "official-source.json"
DEFAULT_OUT = PROJECT_ROOT / "assets" / "data" / "official-manifest.generated.json"


# ---------- Markdown table parsing ----------

def split_row(line: str) -> list[str]:
    """Split a single markdown table row, honouring `\\|` as a literal pipe."""
    s = line.strip().strip("|")
    out, cur = [], ""
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if ch == "|":
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
        i += 1
    if cur or not out:
        out.append(cur.strip())
    return out


def parse_table(block: str) -> list[dict]:
    """Parse a markdown table block into rows; each row has a `header` and column values."""
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return []
    header = split_row(lines[0])
    if not re.fullmatch(r"[\s|:-]+", lines[1]):
        return []
    col_count = len(header)
    rows = []
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) < col_count:
            continue
        if len(cells) > col_count:
            # upstream file with a missing newline inside a row
            extra = []
            while len(cells) > col_count:
                rows.append({"header": header, **{h: c for h, c in zip(header, cells[:col_count])}})
                cells = cells[col_count:]
            if len(cells) == col_count:
                rows.append({"header": header, **{h: c for h, c in zip(header, cells)}})
            continue
        rows.append({"header": header, **{h: c for h, c in zip(header, cells)}})
    return rows


# ---------- Heading & demo extraction ----------

H_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.M)
DEMO_RE = re.compile(r"```demo\s*\n([\s\S]*?)\n```")


def find_first_paragraph(md: str) -> str | None:
    """Return the first non-empty paragraph after the first H1, with HTML comments stripped."""
    lines = md.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^#\s+", line):
            for j in range(i + 1, len(lines)):
                raw = lines[j].strip()
                if raw == "":
                    continue
                if re.match(r"^#{1,6}\s+", raw):
                    return None
                cleaned = re.sub(r"<!--[\s\S]*?-->", "", raw)
                cleaned = re.sub(r"[*_`]", "", cleaned)
                cleaned = re.sub(r"\byou should\b", "this should", cleaned, flags=re.I)
                cleaned = re.sub(r"\byou must\b", "one must", cleaned, flags=re.I)
                cleaned = re.sub(r"\byou need to\b", "one needs to", cleaned, flags=re.I)
                cleaned = re.sub(r"\bplease (ensure|use|note|remember)\b", r"remember to \1", cleaned, flags=re.I)
                cleaned = re.sub(r"\s+", " ", cleaned).strip()
                return cleaned or None
            return None
    return None


def extract_demos(md: str) -> list[str]:
    m = DEMO_RE.search(md)
    if not m:
        return []
    return [s.strip() for s in m.group(1).splitlines() if s.strip()]


# ---------- Per-component extraction ----------

def derive_component_name(tsx_dir: Path) -> str | None:
    for f in tsx_dir.iterdir():
        if f.suffix in (".tsx", ".ts"):
            txt = f.read_text(encoding="utf8", errors="ignore")
            m = re.search(r"""name:\s*['"]([A-Z][A-Za-z0-9]+)['"]""", txt)
            if m:
                return m.group(1)
    return None


def extract_component(name: str, src_root: Path) -> dict | None:
    comp_dir = src_root / "src" / name
    if not comp_dir.is_dir():
        return None
    en_doc = comp_dir / "demos" / "enUS" / "index.demo-entry.md"
    zh_doc = comp_dir / "demos" / "zhCN" / "index.demo-entry.md"
    source_files = sorted(p.name for p in comp_dir.iterdir() if p.suffix in (".tsx", ".ts"))

    api: dict[str, list[dict]] = {"props": [], "events": [], "slots": [], "methods": [], "subComponents": []}
    description = None
    demos_en, demos_zh = [], []

    if en_doc.exists():
        md = en_doc.read_text(encoding="utf8")
        description = find_first_paragraph(md)
        demos_en = extract_demos(md)
        for heading in H_RE.findall(md):
            # locate table immediately after this heading
            block = _table_after_heading(md, heading)
            rows: list[dict] = []
            note: str | None = None
            if block:
                rows = parse_table(block)
            if not rows:
                # No table — but upstream may use a `See [...]` link instead
                # (e.g. n-tooltip inherits popover's API). Capture verbatim.
                note = _see_hint_after_heading(md, heading)
                if note is None:
                    continue
            entry = {"title": heading, "lang": "enUS", "source": str(en_doc.relative_to(src_root.parent)),
                      "rows": rows}
            if note is not None:
                entry["note"] = note
            bucket = _bucket_for(heading)
            if bucket:
                api[bucket].append(entry)

    if zh_doc.exists():
        md = zh_doc.read_text(encoding="utf8")
        demos_zh = extract_demos(md)

    component_name = derive_component_name(comp_dir) or (
        "N" + "".join(s.capitalize() for s in name.split("-"))
    )

    return {
        "key": name,
        "componentName": component_name,
        "description": description,
        "sourceFiles": source_files,
        "api": api,
        "demos": {"enUS": demos_en, "zhCN": demos_zh},
        "docs": {
            "enUS": str(en_doc.relative_to(src_root.parent)) if en_doc.exists() else None,
            "zhCN": str(zh_doc.relative_to(src_root.parent)) if zh_doc.exists() else None,
        },
    }


def _bucket_for(title: str) -> str | None:
    t = title.lower()
    if "prop" in t:
        return "props"
    if "slot" in t:
        return "slots"
    if "method" in t or "expose" in t:
        return "methods"
    if "event" in t or "emit" in t:
        return "events"
    if "sub" in t or "child" in t:
        return "subComponents"
    return None


def _table_after_heading(md: str, heading: str) -> str | None:
    pat = re.compile(r"^#{2,3}\s+" + re.escape(heading) + r"\s*$", re.M)
    m = pat.search(md)
    if not m:
        return None
    start = m.end()
    # find end of next contiguous table block
    lines = md[start:].splitlines()
    block: list[str] = []
    in_table = False
    for ln in lines:
        if ln.strip().startswith("|"):
            block.append(ln)
            in_table = True
        else:
            if in_table:
                break
    if len(block) < 2:
        return None
    return "\n".join(block)


_SEE_HINT_RE = re.compile(r"See\s+\[([^\]]+)\]\(([^)]+)\)")


def _see_hint_after_heading(md: str, heading: str) -> str | None:
    """Return the `See [Foo](href)` link text+href if the section immediately
    following `heading` contains one and no table. This mirrors upstream's
    inheritance-style docs (e.g. `n-tooltip` props say "See Popover Props")."""
    pat = re.compile(r"^#{2,3}\s+" + re.escape(heading) + r"\s*$", re.M)
    m = pat.search(md)
    if not m:
        return None
    start = m.end()
    # Cap the search to the next 600 chars (one section's worth).
    snippet = md[start : start + 600]
    # Stop at the next heading
    cut = re.search(r"^#{2,3}\s+", snippet, re.M)
    if cut:
        snippet = snippet[: cut.start()]
    h = _SEE_HINT_RE.search(snippet)
    if not h:
        return None
    return h.group(0)  # the full "See [Foo](href)" string


# ---------- Driver ----------

def main() -> None:
    ap = argparse.ArgumentParser(description="Extract official manifest from cached Naive UI source.")
    ap.add_argument("--source", default=None, help="Override source dir (defaults to official-source.json).")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--components", default=None, help="Comma-separated subset of components to extract.")
    args = ap.parse_args()

    meta_path = DEFAULT_SOURCE_META
    if not meta_path.exists():
        print(f"missing {meta_path}; run sync_official.py first", file=sys.stderr)
        sys.exit(1)
    meta = json.loads(meta_path.read_text())
    source = Path(args.source) if args.source else Path(meta["source"])
    if not source.is_dir():
        print(f"source not a directory: {source}", file=sys.stderr)
        sys.exit(1)

    src_dir = source / "src"
    if not src_dir.is_dir():
        print(f"missing src/ in {source}", file=sys.stderr)
        sys.exit(1)
    all_keys = sorted(p.name for p in src_dir.iterdir() if p.is_dir())
    targets = args.components.split(",") if args.components else all_keys

    components: dict[str, dict] = {}
    for k in targets:
        if not k:
            continue
        info = extract_component(k, source)
        if info:
            components[k] = info

    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": str(source),
            "ref": meta["ref"],
            "commit": meta["commit"],
            "shortCommit": meta["shortCommit"],
            "syncedAt": meta["syncedAt"],
        },
        "componentCount": len(components),
        "components": components,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Wrote {len(components)} components to {out}")


if __name__ == "__main__":
    main()
