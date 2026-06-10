---
name: naive-ui
description: Naive UI (Vue 3) component-library skill. Invoke when the user needs to implement, debug, select, or upgrade a Naive UI component, layout, theme, dark mode, i18n, or SSR setup — phrases like "n-data-table 远程分页", "Naive UI 暗色模式", "nuxt 集成 naive-ui", "n-form 动态校验", "naive-ui 主题色覆盖", "n-select 虚拟滚动 50000 条" all count. Do not invoke for non-Naive-UI Vue tasks, generic Vue 3 questions, or other UI libraries (Element Plus, Ant Design Vue, Vuetify, PrimeVue).
license: MIT
metadata:
  source: tusen-ai/naive-ui
  sourceRef: 7a12097edc91962712d78f8cd9e301928eb5e558
  generatedBy: scripts/generate_references.py
  handReviewed: true
---

# Naive UI Skill

> **STOP. Read the listed reference before writing any Naive UI code.** This `SKILL.md` is a dispatcher only. Full prop/event/slot tables, official demo lists, and pattern recipes live in `references/`. Do not paraphrase the dispatcher — load the file.

## When to Invoke

Invoke this skill when the user needs to:

- Implement a Naive UI component, layout, theme, form, or feedback overlay
- Debug Naive UI behaviour (controlled vs uncontrolled, SSR, Teleport, dark mode, Provider order, auto-import)
- Pick a Naive UI component for a given UI pattern (e.g. "how do I render a multi-select with search and remote data")
- Upgrade or migrate an existing Naive UI project to a newer release
- Build a Nuxt / VitePress / Vite SSG site that uses Naive UI

Do not invoke this skill for:

- Generic Vue 3 / TypeScript questions unrelated to Naive UI
- Other UI libraries (Element Plus, Ant Design Vue, Vuetify, PrimeVue)
- Backend / Node.js work that does not touch Naive UI

## Required Reading Router

Match the user task to one or more rows. Read the listed files **in full before producing output**. They are load-bearing — the inline content in this file is a pointer, not a substitute.

| Task | MUST read |
| --- | --- |
| Look up a component's prop / event / slot / method / expose | `references/components/n-<name>/api.md` |
| See the official demo list and what each demo covers | `references/components/n-<name>/examples.md` |
| Handle large data / remote pagination / virtual scroll / dark mode / SSR pitfalls | `references/components/n-<name>/patterns.md` |
| Browse the full component catalogue and selection guidance | `references/routing.md` |
| Install / auto-import / Provider order / SFC usage | `references/foundation/quickstart.md` |
| Theme overrides, `useThemeVars`, customise theme | `references/foundation/theming.md` |
| Dark mode, `useOsTheme`, `primaryColorSuppl` pitfalls | `references/foundation/dark-mode.md` |
| Locale / date-locale / multi-language support | `references/foundation/i18n.md` |
| Nuxt / VitePress / Vite SSG / Webpack SSR | `references/foundation/ssr.md` |
| Design tokens (color / border / typography / layout) | `references/foundation/design-color.md`, `design-border.md`, `design-typography.md`, `design-layout.md`, `design-overview.md` |
| Practical rules (controlled/uncontrolled, auto-import, JSX, UMD, fonts, troubleshooting) | `references/rules/core-*.md` and `references/rules/component-*.md` |

> **STOP. Read `references/routing.md` before recommending a component.** Routing.md contains the official component catalogue and selection matrix; do not enumerate components from memory.

## Repository Layout

```text
naive-ui/
├── SKILL.md                                ← this file (dispatcher)
├── assets/                                 ← generator inputs
│   ├── templates/                          ← 5 generator templates (kept for reproducibility)
│   └── data/                               ← official manifest snapshot
├── references/                             ← on-demand knowledge base
│   ├── routing.md                          ← component catalogue & selection matrix
│   ├── foundation/                         ← 10 cross-cutting foundation skills
│   │   ├── quickstart.md
│   │   ├── theming.md
│   │   ├── dark-mode.md
│   │   ├── i18n.md
│   │   ├── ssr.md
│   │   ├── design-color.md
│   │   ├── design-border.md
│   │   ├── design-typography.md
│   │   ├── design-layout.md
│   │   └── design-overview.md
│   ├── rules/                              ← 37 practical rule references
│   │   ├── core-*.md                       ← core-setup, core-theme, core-ssr, …
│   │   └── component-*.md                  ← component-form, component-datatable, …
│   └── components/                         ← 95 components × {api, examples, patterns}
│       └── n-<name>/
│           ├── api.md
│           ├── examples.md
│           └── patterns.md
└── scripts/                                ← Python utilities, exec'able by Claude
    ├── sync_official.py                    ← shallow-clone tusen-ai/naive-ui into .cache/
    ├── extract_official.py                 ← parse demos into data/official-manifest.generated.json
    ├── generate_references.py              ← regenerate references/components/ from manifest + templates/
    ├── augment_tocs.py                     ← inject `## Contents` into >100-line references
    ├── validate.py                         ← check frontmatter, router, link, and ref depth
    └── package_skill.py                    ← zip the skill into ../dist/naive-ui.zip
```

The `naive-ui-skill/` repo also has a project-root `scripts/` directory (not shipped with the skill — developer-only):

```
naive-ui-skill/
├── README.md
├── naive-ui/                               ← the skill (this directory)
└── scripts/                                ← developer-only, not in the packaged zip
    ├── cleanup_generated.py                ← post-step that runs from inside generate_references.py
    └── refresh.py                          ← one-shot wrapper: sync → extract → generate → cleanup → validate
```

## Operating Loop

1. **Identify the task class**: form, table, dialog, theme, dark mode, i18n, SSR, or component selection.
2. **Open the right entry**:
   - Selection question → `references/routing.md` first.
   - Implementation question → `references/components/n-<name>/api.md` for prop/event/slot/method names, then `references/components/n-<name>/patterns.md` for recipes and `references/components/n-<name>/examples.md` for official demo coverage.
   - Cross-cutting question → `references/foundation/<name>.md` or `references/rules/<rule>.md`.
3. **Apply the references verbatim** — every prop/event/slot name, default value, and version field must come from `references/components/<name>/api.md`, not from this file.
4. **For framework-wide concerns** (auto-import, Provider order, JSX, controlled/uncontrolled), consult `references/rules/core-*.md`.

## Conventions

- **Dispatcher, not encyclopedia.** This file stays lean (target <300 lines). Do not paste API tables here.
- **One-level reference depth.** `references/*.md` files do not link to other `references/*.md` (except the canonical back-router `references/routing.md`, which is explicitly whitelisted). Every reference is one click from this file.
- **Generated content is marked.** `references/components/<name>/api.md` files include `<!-- generated -->` markers and an `officialRef` (commit SHA) for traceability.
- **Hand-reviewed files** are flagged via `metadata.handReviewed: true` and listed in the `CHANGELOG.md`.
- **`license: MIT` is informational only.** The Claude Code skill loader only consumes `name` and `description`; the field is kept here for humans reading the frontmatter.

## Maintenance Commands

Run the project-root wrapper for a one-shot refresh:

```bash
# from the repo root (naive-ui-skill/)
python scripts/refresh.py                # sync + extract + generate + cleanup + validate
python scripts/refresh.py --package      # also rebuild dist/naive-ui.zip
python scripts/refresh.py --ref v2.40.0  # pin to a specific official tag
python scripts/refresh.py --skip-sync    # reuse an existing .cache/naive-ui
```

Or run each step individually from inside the `naive-ui/` directory:

```bash
cd naive-ui

# 1. Sync the official Naive UI source into .cache/naive-ui
python scripts/sync_official.py --ref main

# 2. Extract the official manifest from src/<comp>/demos/{enUS,zhCN}/index.demo-entry.md
python scripts/extract_official.py

# 3. Regenerate all references/components/ from manifest + assets/templates/.
#    generate_references.py auto-invokes ../scripts/cleanup_generated.py as a
#    post-step, so freshly regenerated files have no `_（无数据）_` placeholders
#    or `- - ` double-bullets.
python scripts/generate_references.py

# 4. (optional) Inject `## Contents` blocks into any reference file that grew past 100 lines
python scripts/augment_tocs.py

# 5. Validate the skill (frontmatter, router, link integrity, ref depth)
python scripts/validate.py

# 6. Package for distribution (zip this directory into ../dist/naive-ui.zip)
python scripts/package_skill.py . ../dist

# 7. (optional) Re-run the cleanup on its own — idempotent
python ../scripts/cleanup_generated.py --dry-run   # preview
python ../scripts/cleanup_generated.py              # apply
```

> **STOP. Run `python scripts/validate.py` after every regeneration.** Validation must report 0 error before publishing.
