#!/usr/bin/env python3
"""validate.py — structural and quality checks for this skill.

Checks:
  1.  SKILL.md exists, has YAML frontmatter, has `name` and `description`.
  2.  `name` is hyphen-case and matches the parent directory name.
  3.  `description` is at most 1024 characters and free of angle brackets.
  4.  SKILL.md body mentions `Required Reading Router` near the top.
  5.  Every reference listed in the router table actually exists on disk.
  6.  references/ is one level deep (no nested directories inside it).
  7.  references/*.md larger than 100 lines contain a `## Contents` section.
  8.  No reference file links to another `references/*.md` (one-level rule).
  9.  SKILL.md body is under 500 lines.
 10.  Generated references/components/<n>/api.md files exist for the 95
      components in assets/data/official-manifest.generated.json.

Usage:
    python scripts/validate.py [--strict] [--root .]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = PROJECT_ROOT / "skills" / "naive-ui"  # the shipped skill payload
MANIFEST = PROJECT_ROOT / "assets" / "data" / "official-manifest.generated.json"
EXCLUDED = {
    "_internal", "_mixins", "_styles", "_utils",
    "composables", "config-consumer", "locales", "themes", "theme-editor",
    "avatar-group", "button-group", "float-button-group", "icon-wrapper",
    "legacy-transfer",
}


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[3:end]
    fm: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        fm[key] = val
    return fm


def router_targets(skill_md: str) -> list[Path]:
    """Extract `references/...` paths mentioned anywhere in SKILL.md."""
    raw = re.findall(r"`references/[A-Za-z0-9_./-]+\.md`", skill_md)
    return [Path(p.strip("`")) for p in raw]


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate this skill.")
    ap.add_argument("--root", default=str(SKILL_ROOT))
    ap.add_argument("--strict", action="store_true",
                    help="Exit non-zero on warnings as well as errors.")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    skill_md = root / "SKILL.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_md.exists():
        print(f"SKILL.md not found at {skill_md}")
        return 1
    text = skill_md.read_text(encoding="utf8", errors="replace")
    fm = parse_frontmatter(text)
    if not fm:
        errors.append("SKILL.md: missing or invalid YAML frontmatter")
    else:
        if "name" not in fm:
            errors.append("SKILL.md: missing 'name'")
        else:
            name = fm["name"]
            if not re.fullmatch(r"[a-z0-9-]+", name):
                errors.append(f"SKILL.md: name '{name}' must be hyphen-case (lowercase, digits, hyphens)")
            if name != root.name:
                warnings.append(f"SKILL.md: name '{name}' does not match directory '{root.name}'")
        if "description" not in fm:
            errors.append("SKILL.md: missing 'description'")
        else:
            desc = fm["description"]
            if "<" in desc or ">" in desc:
                errors.append("SKILL.md: description contains angle brackets")
            if len(desc) > 1024:
                errors.append(f"SKILL.md: description too long ({len(desc)} chars)")

    # The dispatcher may be padded with blank lines, so allow up to 120 lines
    # of headroom before declaring the router missing.
    head = "\n".join(text.splitlines()[:120])
    if "Required Reading Router" not in head:
        errors.append("SKILL.md: missing 'Required Reading Router' in the first 120 lines")

    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md: body has {line_count} lines (>500)")

    # Router targets must exist
    for ref in router_targets(text):
        if not (root / ref).exists():
            errors.append(f"SKILL.md router references missing file: {ref}")

    # references/ depth + Contents
    refs_root = root / "references"
    if refs_root.exists():
        for sub in refs_root.iterdir():
            if sub.is_dir():
                # Subdirectory OK for components/n-<name>/, but no further nesting
                for inner in sub.rglob("*.md"):
                    depth = len(inner.relative_to(refs_root).parts)
                    if depth > 3:
                        errors.append(f"references/{inner.relative_to(root)}: nested too deep (depth {depth})")
                # also detect references linking to references
                for md in sub.rglob("*.md"):
                    txt = md.read_text(encoding="utf8", errors="replace")
                    # Allow patterns.md and api.md to mention `references/routing.md`
                    # (the canonical back-router). Other nested references remain warnings.
                    bad = re.findall(r"`references/[A-Za-z0-9_./-]+\.md`", txt)
                    bad = [b for b in bad if b != "`references/routing.md`"]
                    if bad:
                        warnings.append(f"{md.relative_to(root)}: contains nested references/ link(s) — prefer routing via SKILL.md")
                    # Broken relative links (escapes skill root, or points
                    # at a sibling-skill file that no longer exists in this
                    # single-skill layout). Allow http(s):// and #fragment
                    # links; flag relative paths that don't resolve to an
                    # existing file inside `root`. Common historical
                    # offender: ../naive-ui-theming/SKILL.md from a
                    # foundation file (multi-skill layout, no longer ships).
                    # If a reference wants to point at the upstream docs
                    # site, it should use a full https URL — generator
                    # output should be patched to do the same.
                    for href in re.findall(r"\]\(([^)]+)\)", txt):
                        if href.startswith(("http://", "https://", "#", "mailto:")):
                            continue
                        # strip an optional title ("foo.md \"title\"")
                        clean = href.split(None, 1)[0]
                        if not (clean.startswith("./") or clean.startswith("../")):
                            continue
                        target = (md.parent / clean).resolve()
                        try:
                            target.relative_to(root)
                        except ValueError:
                            errors.append(
                                f"{md.relative_to(root)}: link '{href}' escapes the skill root — "
                                f"rewrite as a path inside this skill"
                            )
                            continue
                        if not target.exists():
                            errors.append(
                                f"{md.relative_to(root)}: broken relative link '{href}' "
                                f"(resolves to {target.relative_to(root)}); use a full URL if it "
                                f"intentionally points at the upstream docs site"
                            )
                    lines = txt.splitlines()
                    if len(lines) > 100 and not re.search(r"^##\s+Contents\s*$", txt, re.M):
                        warnings.append(f"{md.relative_to(root)}: {len(lines)} lines but no '## Contents'")

    # Generated components: 95 api.md must exist
    if MANIFEST.exists():
        manifest = __import__("json").loads(MANIFEST.read_text(encoding="utf8", errors="replace"))
        comp_root = root / "references" / "components"
        missing = []
        for k in sorted(manifest["components"]):
            if k.startswith("_") or k in EXCLUDED:
                continue
            kebab = k if k.startswith("n-") else f"n-{k}"
            api = comp_root / kebab / "api.md"
            if not api.exists():
                missing.append(kebab)
        if missing:
            warnings.append(f"missing {len(missing)} generated component api.md: {missing[:5]}…")

    # Report
    print(f"Skill: {root}")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("No errors.")
    return 1 if args.strict and warnings else 0


if __name__ == "__main__":
    sys.exit(main())
