#!/usr/bin/env python3
"""generate_references.py — read assets/data/official-manifest.generated.json
and the 6 generator templates, and write references/components/n-<name>/{api,
examples,patterns}.md for each component in the manifest.

Internal / sub-component directories are excluded (composables, locales,
themes, theme-editor, config-consumer, legacy-transfer, avatar-group,
button-group, float-button-group, icon-wrapper).

Usage:
    python scripts/generate_references.py                  # write to references/components/
    python scripts/generate_references.py --out other/dir
    python scripts/generate_references.py --component button
    python scripts/generate_references.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = PROJECT_ROOT / "naive-ui"
ASSETS_DIR = PROJECT_ROOT / "assets"
MANIFEST = ASSETS_DIR / "data" / "official-manifest.generated.json"
TEMPLATES = ASSETS_DIR / "templates"
DEFAULT_OUT = SKILL_DIR / "references" / "components"

EXCLUDED = {
    "_internal", "_mixins", "_styles", "_utils",
    "composables", "config-consumer", "locales", "themes", "theme-editor",
    "avatar-group", "button-group", "float-button-group", "icon-wrapper",
}


def esc_md(value) -> str:
    s = str(value or "")
    s = re.sub(r"<!--[\s\S]*?-->", "", s)
    s = s.replace("|", "\\|")
    s = re.sub(r"\s*\n\s*", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def titleize(kebab: str) -> str:
    return " ".join(s.capitalize() for s in kebab.split("-"))


def normalize_kebab(key: str) -> str:
    return key if key.startswith("n-") else f"n-{key}"


def rows_to_table(rows: list[dict]) -> str:
    """Render rows grouped by header signature. Empty list → empty placeholder."""
    if not rows:
        return "_（无数据）_"
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        h = tuple(r.get("header") or list(r.keys()))
        groups.setdefault(h, []).append(r)
    out: list[str] = []
    for h, rs in groups.items():
        cols = list(h)
        out.append("| " + " | ".join(esc_md(c) for c in cols) + " |")
        out.append("| " + " | ".join(["---"] * len(cols)) + " |")
        for r in rs:
            out.append("| " + " | ".join(esc_md(r.get(c, "")) for c in cols) + " |")
        out.append("")
    return "\n".join(out).rstrip()


def section_block(blocks: list[dict]) -> str:
    """Render an API section: table of rows, with any per-block `note` appended.

    If rows are empty but a note exists (e.g. upstream says
    `See [Popover Props](popover#Popover-Props)`), emit the note verbatim
    instead of the `_（无数据）_` placeholder — mirroring upstream.
    """
    rows = [row for b in blocks for row in b.get("rows", [])]
    notes = [b["note"] for b in blocks if b.get("note")]
    if not rows and not notes:
        return ""
    if not rows:
        # Notes only — emit each note on its own line as a paragraph.
        return "\n\n".join(notes)
    table = rows_to_table(rows)
    if notes:
        return table + "\n\n" + "\n\n".join(notes)
    return table


def describe_short(c: dict) -> str:
    title = titleize(c["key"].replace("^n-", ""))
    raw = c.get("description") or f"{title} component."
    raw = re.sub(r"^" + re.escape(title) + r"\s*components?\.?\s*", "", raw, flags=re.I)
    return f"{title} component. {raw}".strip()


def detect_aliases(c: dict) -> str:
    aliases: set[str] = set()
    for block in c["api"].get("subComponents", []):
        for row in block.get("rows", []):
            name = row.get("Name", "").lower()
            if name:
                aliases.add(f"<{name}>")
    if not aliases:
        return "- (no official sub-components discovered)"
    return "\n".join(
        f"- `<{a}>` — see `references/components/{normalize_kebab(c['key'])}/api.md`"
        for a in sorted(aliases)
    )


def build_examples_toc(c: dict) -> str:
    lines = []
    for f in c["demos"]["enUS"]:
        anchor = re.sub(r"[^a-z0-9]+", "-", f.lower()).strip("-")
        lines.append(f"- [{f}](#{anchor})")
    return "\n".join(lines) or "- (no official demo discovered)"


def build_examples_body(c: dict) -> str:
    if not c["demos"]["enUS"]:
        return "## Official demo list is empty\n\nSee `tusen-ai/naive-ui/src/" + c["key"] + "/demos/` for more examples."
    parts: list[str] = []
    for f in c["demos"]["enUS"]:
        zh = "yes" if f in c["demos"]["zhCN"] else "no"
        anchor = re.sub(r"[^a-z0-9]+", "-", f.lower()).strip("-")
        parts.append(
            f"### {f}\n\n"
            f"> Path: `src/{c['key']}/demos/enUS/{f}` (zhCN available: **{zh}**)\n\n"
            f"Stub: see the original file for the full demo title and code.\n"
        )
    return "\n".join(parts).rstrip()


def selection_matrix(c: dict) -> str:
    return (
        "| Option | When to use | When not to use |\n"
        "| --- | --- | --- |\n"
        f"| `{normalize_kebab(c['key'])}` | {esc_md(c.get('description') or '')} | Task does not involve this component |\n"
        "| Sibling alternatives | Consult `references/routing.md` for the selection matrix | — |\n"
    )


def performance_notes(c: dict) -> str:
    if c["key"] in {"data-table", "tree", "select", "cascader", "virtual-list", "tree-select"}:
        return (
            "- Enable `virtual-scroll` before reaching for `filter` / `remote`.\n"
            "- For large datasets, prefer server-side sort/filter/pagination over client-side."
        )
    return "- Default behaviour covers most cases. Revisit this section only on visible lag or memory growth."


def theme_and_ssr_notes(c: dict) -> str:
    return (
        "- **Theme**: drive every colour / radius / shadow through `theme-overrides`. Never hardcode CSS values.\n"
        "- **Dark mode**: when customising the primary colour, always set `primaryColorSuppl` or dark-mode hover/pressed will look wrong.\n"
        "- **SSR**: wrap the app in `n-config-provider`. If you call `useThemeVars()` inside a `n-modal` / `n-drawer` slot, call it at the root level first."
    )


def upgrade_notes(c: dict) -> str:
    return (
        f"- Last sync: `{c['docs']['enUS'] or '—'}`.\n"
        f"- Version field: see the `Version` column in `api.md`."
    )


def antipatterns() -> str:
    return (
        "- Reaching into the component's internal DOM with `document.querySelector`.\n"
        "- Calling `useThemeVars()` outside `n-config-provider`.\n"
        "- Copy-pasting old demo code without checking the `Version` column."
    )


def related_docs(c: dict) -> str:
    en = f"`{c['docs']['enUS']}`" if c["docs"]["enUS"] else "—"
    zh = f"`{c['docs']['zhCN']}`" if c["docs"]["zhCN"] else "—"
    return (
        f"- Official EN: {en}\n"
        f"- Official ZH: {zh}\n"
        f"- Routing: `references/routing.md`"
    )


def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf8", errors="replace")


def render(tpl: str, vars: dict) -> str:
    return re.sub(r"\{(\w+)\}", lambda m: str(vars.get(m.group(1), m.group(0))), tpl)


def emit_component(c: dict, meta: dict, out_root: Path) -> list[tuple[Path, str]]:
    kebab = normalize_kebab(c["key"])
    title = titleize(c["key"].replace("^n-", ""))
    short = describe_short(c)
    base = {
        "componentKebab": kebab,
        "componentTitle": title,
        "version": meta["source"]["shortCommit"],
        "officialRef": meta["source"]["commit"],
        "generatedAt": meta["generatedAt"],
        "componentPath": c["key"],
        "langHint": "zh-CN",
        "sourceFiles": ", ".join(c["sourceFiles"]),
    }

    main_vars = {
        **base,
        "shortZh": short,
        "useCase": f"implement or compose {title} for forms, actions, or dialogs",
        "negativeCase": "cross-cutting concerns such as theme, i18n, or SSR — see foundation/ instead",
        "useCasePositives": c.get("description") or f"{title} component.",
        "useCaseNegatives": "Cross-cutting concerns (theme, i18n, SSR) — see the foundation/ section.",
        "aliases": detect_aliases(c),
        "keyPitfalls": "- See the `Antipatterns` section in `references/components/" + kebab + "/patterns.md`.",
    }

    api_vars = {
        **base,
        "shortZh": f"{title} API reference. {short}",
        "propsTable": section_block(c["api"].get("props", [])),
        "eventsTable": section_block(c["api"].get("events", [])),
        "slotsTable": section_block(c["api"].get("slots", [])),
        "methodsTable": section_block(c["api"].get("methods", [])),
        "subComponentsTable": section_block(c["api"].get("subComponents", [])),
    }

    examples_vars = {
        **base,
        "shortZh": f"{title} official demo index. {short}",
        "examplesToc": build_examples_toc(c),
        "examplesBody": build_examples_body(c),
    }

    patterns_vars = {
        **base,
        "shortZh": f"{title} patterns, pitfalls, theme, SSR, and selection.",
        "selectionMatrix": selection_matrix(c),
        "performanceNotes": performance_notes(c),
        "themeAndSsrNotes": theme_and_ssr_notes(c),
        "upgradeNotes": upgrade_notes(c),
        "antipatternList": antipatterns(),
        "relatedDocs": related_docs(c),
    }

    comp_dir = out_root / kebab
    return [
        (comp_dir / "api.md", render(load_template("component-api-reference.md"), api_vars)),
        (comp_dir / "examples.md", render(load_template("component-examples-reference.md"), examples_vars)),
        (comp_dir / "patterns.md", render(load_template("component-patterns-reference.md"), patterns_vars)),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate references/components from manifest.")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--component", default=None, help="Generate a single component (e.g. 'button').")
    ap.add_argument("--manifest", default=str(MANIFEST))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not Path(args.manifest).exists():
        print(f"manifest not found: {args.manifest}; run extract_official.py first", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf8", errors="replace"))

    keys = (
        [args.component]
        if args.component
        else sorted(
            k for k in manifest["components"]
            if not k.startswith("_") and k not in EXCLUDED
        )
    )

    out_root = Path(args.out)
    plan: list[tuple[Path, str]] = []
    for k in keys:
        if k not in manifest["components"]:
            print(f"[skip] {k} not in manifest", file=sys.stderr)
            continue
        plan.extend(emit_component(manifest["components"][k], manifest, out_root))

    if args.dry_run:
        print(f"Plan: {len(plan)} files for {len(keys)} components under {out_root}")
        for p, _ in plan[:6]:
            print(f"  would write {p}")
        if len(plan) > 6:
            print(f"  …and {len(plan) - 6} more")
        return

    for p, content in plan:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf8")
    print(f"Wrote {len(plan)} files for {len(keys)} components under {out_root}")

    # Post-step: run the project-root cleanup so freshly regenerated files
    # don't carry placeholder noise. Failure here is non-fatal — the operator
    # can re-run `scripts/cleanup_generated.py` manually.
    try:
        import runpy
        cleanup_path = PROJECT_ROOT / "scripts" / "cleanup_generated.py"
        if cleanup_path.exists():
            print(f"Post-step: {cleanup_path.relative_to(PROJECT_ROOT)}")
            runpy.run_path(str(cleanup_path), run_name="__main__")
    except SystemExit as e:  # the cleanup script uses sys.exit() to abort
        if e.code:
            print(f"cleanup_generated.py exited with code {e.code}", file=sys.stderr)


if __name__ == "__main__":
    main()
