# Naive UI Skill

> 🌐 **You are reading the English version.** [🇨🇳 Switch to zh-CN →](./README.zh-CN.md)

A Claude skill for the [Naive UI](https://www.naiveui.com/) Vue 3 component library. Generated from the official `tusen-ai/naive-ui` source.

## Install

Pick whichever path fits your environment. All three land the skill at `~/.claude/skills/naive-ui/`.

### Option A — `npx skills` (recommended; works for Claude Code, Codex, Cursor, Windsurf)

```bash
npx skills add klarkxy/naive-ui-skill --skill naive-ui -g -y
```

This downloads the `naive-ui/` subdirectory from this repo and drops it into your global skills folder. No `git` needed. To update later: `npx skills update klarkxy/naive-ui-skill`.

### Option B — One-liner shell (no Node required)

```bash
curl -fsSL https://raw.githubusercontent.com/klarkxy/naive-ui-skill/main/install.sh | bash
```

Uses POSIX `curl` + `tar` only. Set `NAIVE_UI_SKILL_DIR` to override the target.

### Option C — Manual clone / zip

```bash
# from a clone
git clone https://github.com/klarkxy/naive-ui-skill.git
cp -r naive-ui-skill/skills/naive-ui ~/.claude/skills/

# or build and install the zip locally
git clone https://github.com/klarkxy/naive-ui-skill.git
cd naive-ui-skill
python scripts/package_skill.py
unzip dist/naive-ui.zip -d ~/.claude/skills/
```

> For Codex / Trae / other agents, replace `~/.claude/skills/` with `~/.codex/skills/` / `~/.trae/skills/` etc.

## Usage

Once installed, invoke the skill explicitly:

```
/skill naive-ui
```

Or rely on the description match: any user request mentioning "Naive UI", `n-data-table`, `n-form`, "Naive UI components / theming / dark mode", "nuxt integration with naive-ui", etc. should trigger this skill.

## Source & License

Generated from [tusen-ai/naive-ui](https://github.com/tusen-ai/naive-ui) (MIT). The official repository owns the canonical API names, defaults, and version fields; this skill only adds routing, patterns, and decision support.