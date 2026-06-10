#!/usr/bin/env python3
"""refresh.py — one-shot pipeline for refreshing the Naive UI skill.

Steps
-----
1.  sync_official.py            shallow-clone tusen-ai/naive-ui into .cache/
2.  extract_official.py         parse demos into data/official-manifest.generated.json
3.  generate_references.py      regenerate references/components/ (auto-runs cleanup)
4.  augment_tocs.py             inject `## Contents` into >100-line references
5.  validate.py                 structural / quality checks (must report 0 error)
6.  package_skill.py            (only with --package) rebuild dist/naive-ui.zip

Usage
-----
    python scripts/refresh.py                # refresh + validate, no zip
    python scripts/refresh.py --package      # also rebuild dist/naive-ui.zip
    python scripts/refresh.py --ref v2.39.0  # pin to a specific official ref
    python scripts/refresh.py --skip-sync    # skip step 1 if .cache/ is already current
    python scripts/refresh.py --strict       # treat validate.py warnings as errors

Exit codes
----------
  0  success
  1  a step raised an uncaught exception
  N  the Nth step (1-indexed) returned non-zero
"""
from __future__ import annotations

import argparse
import runpy
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = PROJECT_ROOT / "naive-ui"
SCRIPTS = PROJECT_ROOT / "scripts"

# (script path, runpy argv, friendly name)
STEPS: list[tuple[Path, list[str], str]] = [
    (SCRIPTS / "sync_official.py", [], "sync_official.py"),
    (SCRIPTS / "extract_official.py", [], "extract_official.py"),
    (SCRIPTS / "generate_references.py", [], "generate_references.py"),
    (SCRIPTS / "augment_tocs.py", [], "augment_tocs.py"),
    (SCRIPTS / "validate.py", [], "validate.py"),
]


def run_step(idx: int, script: Path, argv: list[str], name: str) -> bool:
    print(f"\n=== Step {idx}/{len(STEPS)}: {name} ===")
    if not script.exists():
        print(f"  missing: {script.relative_to(PROJECT_ROOT)}", file=sys.stderr)
        return False
    saved_argv = sys.argv
    sys.argv = [str(script)] + argv
    try:
        runpy.run_path(str(script), run_name="__main__")
        return True
    except SystemExit as e:
        if e.code not in (None, 0):
            print(f"  {name} exited with code {e.code}", file=sys.stderr)
            return False
        return True
    finally:
        sys.argv = saved_argv


def main() -> int:
    ap = argparse.ArgumentParser(description="Refresh the Naive UI skill end-to-end.")
    ap.add_argument("--ref", default="main", help="Git ref for sync_official.py (default: main).")
    ap.add_argument(
        "--skip-sync",
        action="store_true",
        help="Reuse existing .cache/naive-ui (don't fetch from origin).",
    )
    ap.add_argument(
        "--package",
        action="store_true",
        help="After a clean validate, also rebuild dist/naive-ui.zip.",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Pass --strict to validate.py (warnings become errors).",
    )
    args = ap.parse_args()

    # Per-step argv
    argv_by_name: dict[str, list[str]] = {
        "sync_official.py": (
            [] if args.skip_sync else ["--ref", args.ref]
        ),
        "extract_official.py": [],
        "generate_references.py": [],
        "augment_tocs.py": [],
        "validate.py": ["--strict"] if args.strict else [],
    }

    for i, (script, _default_argv, name) in enumerate(STEPS, 1):
        ok = run_step(i, script, argv_by_name[name], name)
        if not ok:
            print(f"\nAborted at step {i} ({name}).", file=sys.stderr)
            return i

    if args.package:
        print(f"\n=== Packaging: package_skill.py ===")
        package_script = SCRIPTS / "package_skill.py"
        if not package_script.exists():
            print(f"  missing: {package_script}", file=sys.stderr)
            return 100
        saved_argv = sys.argv
        sys.argv = [str(package_script), str(SKILL_ROOT), str(PROJECT_ROOT / "dist")]
        try:
            runpy.run_path(str(package_script), run_name="__main__")
        except SystemExit as e:
            if e.code not in (None, 0):
                return 101
        finally:
            sys.argv = saved_argv

    print("\nRefresh complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
