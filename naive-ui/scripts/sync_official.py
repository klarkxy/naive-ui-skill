#!/usr/bin/env python3
"""sync_official.py — shallow-clone tusen-ai/naive-ui into .cache/ and record
the commit SHA in assets/data/official-source.json.

Idempotent: re-running with the same ref resets to origin/<ref>.

Usage:
    python scripts/sync_official.py --ref main
    python scripts/sync_official.py --ref v2.40.0
    python scripts/sync_official.py --source /path/to/local/naive-ui  # use a local checkout
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "https://github.com/tusen-ai/naive-ui.git"
SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CACHE = SKILL_ROOT / ".cache" / "naive-ui"
META_PATH = SKILL_ROOT / "assets" / "data" / "official-source.json"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, shell=False)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def ensure_git() -> None:
    code, out, _ = run(["git", "--version"])
    if code != 0:
        print("git not available on PATH", file=sys.stderr)
        sys.exit(2)
    print(out)


def ensure_cache(cache: Path, ref: str, dry_run: bool) -> None:
    if not cache.exists():
        if dry_run:
            print(f"[dry-run] would create {cache}")
            return
        cache.mkdir(parents=True)
    if not (cache / ".git").exists():
        if dry_run:
            print(f"[dry-run] would shallow-clone {REPO}@{ref} -> {cache}")
            return
        print(f"Cloning {REPO}@{ref} into {cache} …")
        code, _, err = run(["git", "clone", "--depth", "1", "--branch", ref, REPO, str(cache)])
        if code != 0:
            print(err, file=sys.stderr)
            raise SystemExit(1)
        return
    # existing clone: fetch and reset
    if dry_run:
        print(f"[dry-run] would fetch and reset {cache} to origin/{ref}")
        return
    run(["git", "-C", str(cache), "fetch", "--depth", "1", "origin", ref])
    code, _, err = run(["git", "-C", str(cache), "reset", "--hard", f"origin/{ref}"])
    if code != 0:
        print(err, file=sys.stderr)
        raise SystemExit(1)


def write_meta(source: Path, ref: str, cache: Path) -> None:
    META_PATH.parent.mkdir(parents=True, exist_ok=True)
    _, sha, _ = run(["git", "-C", str(source), "rev-parse", "HEAD"])
    _, short, _ = run(["git", "-C", str(source), "rev-parse", "--short", "HEAD"])
    _, status, _ = run(["git", "-C", str(source), "status", "--porcelain"])
    meta = {
        "source": str(source),
        "cacheDir": str(cache),
        "ref": ref,
        "commit": sha,
        "shortCommit": short,
        "dirty": bool(status),
        "syncedAt": datetime.now(timezone.utc).isoformat(),
    }
    META_PATH.write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync the official Naive UI source.")
    ap.add_argument("--ref", default="main")
    ap.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    ap.add_argument("--source", default=None, help="Use a local checkout instead of cloning.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ensure_git()
    cache = Path(args.cache_dir).resolve()
    if not args.source:
        ensure_cache(cache, args.ref, args.dry_run)
        source = cache
    else:
        source = Path(args.source).resolve()
        if not source.exists():
            print(f"source not found: {source}", file=sys.stderr)
            raise SystemExit(1)
    if not args.dry_run:
        write_meta(source, args.ref, cache)


if __name__ == "__main__":
    main()
