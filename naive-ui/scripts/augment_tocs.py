#!/usr/bin/env python3
"""augment_tocs.py — inject a `## Contents` block into every .md file under
references/ that has more than 100 lines and no Contents yet.

Usage:
    python scripts/augment_tocs.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TARGETS = [SKILL_ROOT / "references"]


def is_frontmatter_end(lines: list[str]) -> int:
    """Return the index of the closing `---` line, or -1."""
    if not lines or lines[0].rstrip() != "---":
        return -1
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return i
    return -1


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf8", errors="replace")
    if re.search(r"^##\s+Contents\s*$", text, re.M):
        return False
    lines = text.splitlines()
    if len(lines) <= 100:
        return False
    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            headings.append((i, m.group(1).strip()))
        if len(headings) >= 40:
            break
    if not headings:
        return False
    toc = ["## Contents", ""]
    for _, title in headings:
        anchor = re.sub(r"[^a-z0-9\u4e00-\u9fa5-]+", "-", title.lower()).strip("-")
        toc.append(f"- [{title}](#{anchor})")
    toc.append("")

    # insert after frontmatter (if any) and after the first H1
    insert_at = 0
    fe = is_frontmatter_end(lines)
    if fe >= 0:
        insert_at = fe + 1
    for i in range(insert_at, min(insert_at + 12, len(lines))):
        if re.match(r"^#\s+", lines[i]):
            insert_at = i + 1
            break
    new = lines[:insert_at] + toc + lines[insert_at:]
    path.write_text("\n".join(new) + "\n", encoding="utf8")
    return True


def main() -> None:
    updated = skipped = 0
    for root in TARGETS:
        if not root.exists():
            continue
        for f in root.rglob("*.md"):
            if inject(f):
                updated += 1
            else:
                skipped += 1
    print(f"Augmented {updated} files (skipped {skipped}).")


if __name__ == "__main__":
    main()
