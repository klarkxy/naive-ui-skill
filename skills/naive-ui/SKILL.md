---
name: naive-ui
description: This skill is a reference manual for the Naive UI Vue 3 component library. Use it when the user works with Naive UI. Not for: other UI libraries (Element Plus, Ant Design Vue, Vuetify, PrimeVue) or generic Vue 3 questions.
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

## Reference File Anatomy

Each reference file follows a predictable shape — no need to read one first to learn the layout:

- **`references/routing.md`** — selection matrix + sub-component alias table. Read first when the user asks "which Naive UI component for X?".
- **`references/components/n-<name>/api.md`** — canonical prop / event / slot / method / expose tables. Empty sections are dropped; the `## Contents` TOC reflects what remains.
- **`references/components/n-<name>/examples.md`** — list of official demo names with paths into the upstream source.
- **`references/components/n-<name>/patterns.md`** — selection matrix, performance & remote data, theme & SSR, antipatterns, related official docs.
- **`references/foundation/*.md`** — one self-contained guide per cross-cutting topic (install, theming, dark mode, i18n, SSR, design tokens).
- **`references/rules/core-*.md` / `component-*.md`** — bite-sized rules for specific patterns; each carries a `## Contents` at the top.

## Operating Loop

1. **Identify the task class**: form, table, dialog, theme, dark mode, i18n, SSR, or component selection.
2. **Open the right entry**:
   - Selection question → `references/routing.md` first.
   - Implementation question → `references/components/n-<name>/api.md` for prop/event/slot/method names, then `references/components/n-<name>/patterns.md` for recipes and `references/components/n-<name>/examples.md` for official demo coverage.
   - Cross-cutting question → `references/foundation/<name>.md` or `references/rules/<rule>.md`.
3. **Apply the references verbatim** — every prop/event/slot name, default value, and version field must come from `references/components/<name>/api.md`, not from this file.
4. **For framework-wide concerns** (auto-import, Provider order, JSX, controlled/uncontrolled), consult `references/rules/core-*.md`.
