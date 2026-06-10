#!/usr/bin/env bash
# install.sh — install the Naive UI skill into Claude Code / Codex.
#
# One-liner:
#   curl -fsSL https://raw.githubusercontent.com/klarkxy/naive-ui-skill/main/install.sh | bash
#
# Optional environment overrides:
#   NAIVE_UI_SKILL_DIR   target skill directory (default: ~/.claude/skills/naive-ui)
#   NAIVE_UI_REF         git ref to fetch (default: main)
#   NAIVE_UI_REPO        source repo (default: klarkxy/naive-ui-skill)
set -euo pipefail

REPO="${NAIVE_UI_REPO:-klarkxy/naive-ui-skill}"
REF="${NAIVE_UI_REF:-main}"
DEST="${NAIVE_UI_SKILL_DIR:-$HOME/.claude/skills/naive-ui}"

# Sanity: only POSIX tools (curl, tar, mkdir, cp, rm, mktemp)
command -v curl >/dev/null 2>&1 || { echo "error: curl not found" >&2; exit 1; }
command -v tar  >/dev/null 2>&1 || { echo "error: tar not found"  >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Downloading ${REPO}@${REF} …"
TARBALL_URL="https://codeload.github.com/${REPO}/tar.gz/refs/heads/${REF}"
curl -fsSL "$TARBALL_URL" -o "$TMP/repo.tar.gz"

echo "→ Extracting …"
tar -xz -C "$TMP" -f "$TMP/repo.tar.gz"

# The tarball extracts to <repo>-<ref>/; locate the naive-ui/ payload inside.
SRC="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d -name "${REPO##*/}-*" | head -n 1)"
if [[ -z "$SRC" ]]; then
  echo "error: could not find extracted repo directory under $TMP" >&2
  exit 1
fi
if [[ ! -d "$SRC/skills/naive-ui" ]]; then
  echo "error: $SRC/skills/naive-ui not found — repo layout changed?" >&2
  exit 1
fi

echo "→ Installing into $DEST …"
mkdir -p "$(dirname "$DEST")"
# Refuse to overwrite a non-empty directory without --force
if [[ -d "$DEST" && -n "$(ls -A "$DEST" 2>/dev/null)" ]]; then
  echo "error: $DEST is not empty. Remove it first or set NAIVE_UI_SKILL_DIR to a fresh path." >&2
  exit 1
fi
mkdir -p "$DEST"
cp -r "$SRC/skills/naive-ui/." "$DEST/"

echo "✓ Installed."
echo ""
echo "Try it: open Claude Code and ask about a Naive UI component, e.g."
echo "  \"How do I render a remote-paginated n-data-table?\""
echo ""
echo "Uninstall: rm -rf \"$DEST\""