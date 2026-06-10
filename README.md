# Naive UI Skill

A Claude skill for the [Naive UI](https://www.naiveui.com/) Vue 3 component library. Generated from the official `tusen-ai/naive-ui` source.

## Layout

```
naive-ui-skill/
├── README.md                         ← this file
├── LICENSE                           ← repo-level MIT
├── naive-ui/                         ← the SKILL PAYLOAD (copy this into your skills root)
│   ├── SKILL.md                      ← single dispatcher entry (READ THIS FIRST)
│   ├── LICENSE
│   └── references/                   ← on-demand knowledge base
│       ├── routing.md                ← component catalogue & selection matrix
│       ├── foundation/               ← 10 cross-cutting foundation skills
│       ├── rules/                    ← 37 practical rule references
│       └── components/               ← 96 components × {api, examples, patterns}
├── assets/                           ← generator inputs (NOT shipped)
│   ├── templates/                    ← 5 generator templates
│   └── data/                         ← official manifest + source metadata
├── scripts/                          ← developer-only, NOT shipped
│   ├── sync_official.py              ← shallow-clone tusen-ai/naive-ui
│   ├── extract_official.py           ← parse demos into a manifest
│   ├── generate_references.py        ← regenerate references/components/ + auto-clean
│   ├── augment_tocs.py               ← inject ## Contents into >100-line references
│   ├── validate.py                   ← structural and quality checks
│   ├── package_skill.py              ← zip the skill payload for distribution
│   ├── cleanup_generated.py          ← post-step: drop empty sections + fix double-bullets
│   └── refresh.py                    ← one-shot wrapper for the full refresh pipeline
└── dist/                             ← built zips (gitignored)
    └── naive-ui.zip
```

The shipped skill payload (`naive-ui/`) contains **only** what Claude reads at skill-runtime: `SKILL.md`, `LICENSE`, and `references/`. All scripts and generator inputs stay at the project root.

## Install

The publishable artefact is the `naive-ui/` subdirectory. Copy it into your skills root, e.g. `~/.claude/skills/naive-ui/` or `~/.codex/skills/naive-ui/`. Claude Code and Codex auto-discover skills in those directories.

```bash
# from a clone
git clone https://github.com/<owner>/naive-ui-skill.git
cp -r naive-ui-skill/naive-ui ~/.claude/skills/

# or use the prebuilt zip
unzip naive-ui-skill/dist/naive-ui.zip -d ~/.claude/skills/
```

## Usage

Once installed, invoke the skill explicitly:

```
/skill naive-ui
```

Or rely on the description match: any user request mentioning "Naive UI", "n-data-table", "n-form", "Naive UI 组件 / 主题 / 暗色", "nuxt 集成 naive-ui", etc. should trigger this skill.

## Maintenance

The skill is regenerable from the official source. The simplest path is the project-root wrapper:

```bash
cd naive-ui-skill
python scripts/refresh.py                 # sync + extract + generate + cleanup + validate
python scripts/refresh.py --package       # also rebuild dist/naive-ui.zip
python scripts/refresh.py --ref v2.40.0   # pin to a specific official tag
python scripts/refresh.py --skip-sync     # reuse an existing .cache/naive-ui
```

To run steps individually from the project root:

```bash
cd naive-ui-skill
python scripts/sync_official.py --ref main     # shallow-clone to .cache/naive-ui
python scripts/extract_official.py             # parse demos into manifest
python scripts/generate_references.py          # regenerate + auto-clean
python scripts/augment_tocs.py                 # inject ## Contents where missing
python scripts/validate.py                     # must report 0 error
python scripts/package_skill.py naive-ui dist  # rebuild dist/naive-ui.zip
```

Then `git add -A && git commit -m "chore: refresh from official Naive UI <shortCommit>"`.

### What `cleanup_generated.py` does

After every regeneration, `generate_references.py` invokes `scripts/cleanup_generated.py` as a post-step. The cleanup sweeps two classes of placeholder noise out of the freshly generated files:

1. **`api.md`** — drops `## X` sections whose body is empty or just `_（无数据）_`. The `## Contents` TOC is rebuilt to list only surviving sections.
2. **`patterns.md`** — collapses `- - X` (double-bullet artefact from the template) into `- X`.

It is idempotent: re-running it on already-clean files is a no-op.

## Source & License

Generated from [tusen-ai/naive-ui](https://github.com/tusen-ai/naive-ui) (MIT). The official repository owns the canonical API names, defaults, and version fields; this skill only adds routing, patterns, and decision support.