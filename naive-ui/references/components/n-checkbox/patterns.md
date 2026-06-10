---
name: "n-checkbox-patterns"
description: "Patterns, pitfalls, theme, SSR, and selection guidance for Checkbox. Invoke when the user is making a real-world decision about Checkbox, handling edge cases, or comparing it to neighbouring components."
metadata:
  author: klarkxy
  version: "7a12097"
  source: "tusen-ai/naive-ui"
  sourceRef: "7a12097edc91962712d78f8cd9e301928eb5e558"
  generatedAt: "2026-06-10T05:47:50.172850+00:00"
---

# Checkbox Patterns & Decisions

> This file ships a generator-filled skeleton. Hand-curate the **Selection matrix**, **Performance & remote patterns**, **Theme & SSR notes**, and **Antipatterns** sections; the rest stays deterministic.
> Section convention: `## Heading`, sub-bullets start with `- **trigger condition** — behaviour / note`.

## Contents

- [Selection matrix](#selection-matrix)
- [Performance & remote](#performance--remote)
- [Theme & SSR](#theme--ssr)
- [Upgrade notes](#upgrade-notes)
- [Antipatterns](#antipatterns)
- [Related official docs](#related-official-docs)

## Selection matrix

| Option | When to use | When not to use |
| --- | --- | --- |
| `n-checkbox` | Yo, yo, check it out. | Task does not involve this component |
| Sibling alternatives | Consult `references/routing.md` for the selection matrix | — |


## Performance & remote

- Default behaviour covers most cases. Revisit this section only on visible lag or memory growth.

## Theme & SSR

- **Theme**: drive every colour / radius / shadow through `theme-overrides`. Never hardcode CSS values.
- **Dark mode**: when customising the primary colour, always set `primaryColorSuppl` or dark-mode hover/pressed will look wrong.
- **SSR**: wrap the app in `n-config-provider`. If you call `useThemeVars()` inside a `n-modal` / `n-drawer` slot, call it at the root level first.

## Upgrade notes

- Last sync: `naive-ui\src\checkbox\demos\enUS\index.demo-entry.md`.
- Version field: see the `Version` column in `api.md`.

## Antipatterns

- Reaching into the component's internal DOM with `document.querySelector`.
- Calling `useThemeVars()` outside `n-config-provider`.
- Copy-pasting old demo code without checking the `Version` column.

## Related official docs

- Official EN: `naive-ui\src\checkbox\demos\enUS\index.demo-entry.md`
- Official ZH: `naive-ui\src\checkbox\demos\zhCN\index.demo-entry.md`
- Routing: `references/routing.md`
