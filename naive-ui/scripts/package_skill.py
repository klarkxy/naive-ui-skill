#!/usr/bin/env python3
"""package_skill.py — zip this skill directory into a portable .zip artefact.

Usage:
    python scripts/package_skill.py                     # → ../dist/naive-ui.zip
    python scripts/package_skill.py <skill_dir> <out_dir>

The output zip is laid out as `naive-ui/...` at the top level, matching the
installed shape: drop the unzipped folder straight into ~/.claude/skills/.
"""
from __future__ import annotations

import argparse
import os
import sys
import zipfile
from pathlib import Path

# Things to keep out of the published zip
EXCLUDE_DIRS = {".cache", "__pycache__", "dist", ".git", "node_modules"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
EXCLUDE_SUFFIXES = (".pyc", ".pyo")


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if path.name in EXCLUDE_FILES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Package a skill directory into a .zip.")
    ap.add_argument("skill_dir", nargs="?", default=".",
                    help="Path to the skill directory (default: current dir).")
    ap.add_argument("out_dir", nargs="?", default="../dist",
                    help="Output directory (default: ../dist).")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    if not (skill_dir / "SKILL.md").exists():
        print(f"error: {skill_dir}/SKILL.md not found", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    arc_root = skill_dir.name  # top-level folder inside the zip
    zip_path = out_dir / f"{arc_root}.zip"

    written = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in sorted(skill_dir.rglob("*")):
            if not src.is_file():
                continue
            rel = src.relative_to(skill_dir)
            if should_skip(rel):
                continue
            arc = arc_root / rel
            zf.write(src, arc.as_posix())
            written += 1
    print(f"wrote {zip_path} ({written} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
