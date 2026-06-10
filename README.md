# Naive UI Skill

A Claude skill for the [Naive UI](https://www.naiveui.com/) Vue 3 component library. Generated from the official `tusen-ai/naive-ui` source.

## Layout

```
naive-ui-skill/
├── LICENSE
├── README.md                         ← this file
├── naive-ui/                         ← the actual skill (copy this into your skills root)
│   ├── SKILL.md                      ← single dispatcher entry (READ THIS FIRST)
│   ├── scripts/                      ← Python, exec'able by Claude
│   │   ├── sync_official.py          ← shallow-clone tusen-ai/naive-ui
│   │   ├── extract_official.py       ← parse demos into a manifest
│   │   ├── generate_references.py    ← regenerate references/components/ from manifest + templates
│   │   ├── augment_tocs.py           ← inject ## Contents into >100-line references
│   │   ├── validate.py               ← structural and quality checks
│   │   └── package_skill.py          ← zip the skill for distribution
│   ├── references/                   ← on-demand knowledge base
│   │   ├── routing.md                ← component catalogue & selection matrix
│   │   ├── foundation/               ← 10 cross-cutting foundation skills
│   │   ├── rules/                    ← 37 practical rule references
│   │   └── components/               ← 95 components × {api, examples, patterns}
│   └── assets/
│       ├── templates/                ← 5 generator templates
│       └── data/                     ← official manifest snapshot
└── dist/                             ← built zips (gitignored)
    └── naive-ui.zip
```

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

The skill is regenerable from the official source. To refresh, run from inside the `naive-ui/` directory:

```bash
cd naive-ui
python scripts/sync_official.py --ref main            # shallow-clone to .cache/naive-ui
python scripts/extract_official.py                    # parse demos into manifest
python scripts/generate_references.py                 # regenerate references/components/
python scripts/augment_tocs.py                        # inject ## Contents
python scripts/validate.py                            # must report 0 error
python scripts/package_skill.py . ../dist             # rebuild dist/naive-ui.zip
```

Then `git add -A && git commit -m "chore: refresh from official Naive UI <shortCommit>"`.

## Source & License

Generated from [tusen-ai/naive-ui](https://github.com/tusen-ai/naive-ui) (MIT). The official repository owns the canonical API names, defaults, and version fields; this skill only adds routing, patterns, and decision support.
