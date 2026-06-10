# Component Catalogue

The official Naive UI catalogue is generated from `assets/data/official-manifest.generated.json`. This file is a hand-written index that helps a new reader pick the right component without scanning 95 entries.

> **STOP. Read `references/components/n-<name>/api.md` for exact prop/event/slot names.** This routing page is for selection only; never quote API details from here.

## Selection matrix (high-traffic patterns)

| If you need… | Pick | Why |
| --- | --- | --- |
| A primary action button | `n-button` with `type="primary"` | Standard affordance, full theme support |
| A form with validation | `n-form` + `n-form-item` + rules | Native async-validator integration |
| A multi-step form | `n-form` with `n-grid` + `n-form-item-gi` | Inline grid layout with label placement |
| A dataset table with sorting, filter, pagination | `n-data-table` | Virtual scroll, remote, fixed columns, tree data |
| A simple static table | `n-table` | Lightweight, no remote data |
| A dropdown single-select | `n-select` | filterable, multiple, async, virtual |
| A tree-structured select | `n-tree-select` | Built on top of `n-tree` |
| A cascading region picker | `n-cascader` | Multi-level path selection |
| A date / time / datetime picker | `n-date-picker` | Range, shortcuts, time, datetime modes |
| A modal dialog (forms inside) | `n-dialog` + `useDialog` | Programmatic API + Provider context |
| A plain dialog (no form) | `n-modal` | Lower-level, custom-trigger friendly |
| A side drawer | `n-drawer` | Slide-in panel |
| A toast message | `useMessage()` + `n-message-provider` | Global API, types: info/success/warning/error |
| A notification | `useNotification()` + `n-notification-provider` | Global API, top-right corner |
| A confirm popover | `n-popconfirm` | Lightweight, in-place |
| A loading bar | `useLoadingBar()` + `n-loading-bar-provider` | Page-level progress |
| A skeleton loader | `n-skeleton` | Block / text / circle placeholders |
| An image with preview | `n-image` | Group preview, lazy load |
| A virtualised list | `n-virtual-list` (standalone) or `n-data-table` built-in virtual scroll | For 1k+ rows |
| A tree with checkboxes | `n-tree` with `checkable` | Async load, drag, virtual scroll |
| A tag input | `n-dynamic-tags` | Add/remove inline |
| A file uploader | `n-upload` | Custom request, drag-drop, image style |
| A code editor / display | `n-code` | highlight.js integration |
| A rich typography set | `n-typography` (h1..h6, p, ul, …) | Title / text / blockquote |
| A form item with a custom slot | `n-form-item` + slot | Full layout control |
| An editable cell in a table | `n-data-table` with `render` returning `n-input` etc. | Per-cell custom component |
| A floating action button | `n-float-button` | Bottom-right, optional group |

## Common sub-components (alias, not separate skills)

The following sub-component tags are mentioned in their parent component's
official `api.md`. For everything else, treat the sub-component tag as a
plain Vue component and consult its parent's official documentation.

| Sub-component tag | Parent skill |
| --- | --- |
| `n-tab`, `n-tab-pane` | `references/components/n-tabs/api.md` |
| `n-step` | `references/components/n-steps/api.md` |
| `n-grid-item` | `references/components/n-grid/api.md` |
| `n-form-item-row` | (deprecated; use `n-form-item-gi`) |

> Tags NOT listed above (`n-form-item`, `n-collapse-item`, `n-radio-group`, …)
> are real Vue tags but do not appear in the official per-parent API tables.
> If a user asks about one of them, route to the parent api.md and let the
> reader infer from the parent's slot / props documentation; do not invent
> sub-component-only API.

## Excluded (internal helpers, not user-facing)

`composables/`, `locales/`, `themes/`, `theme-editor/`, `config-consumer/`, `_internal/`, `_mixins/`, `_styles/`, `_utils/`, plus the four alias directories `avatar-group/`, `button-group/`, `float-button-group/`, `icon-wrapper/` (no standalone official documentation).

## Maintenance

- This file is hand-curated. The exhaustive 95-row table lives in `assets/data/official-manifest.generated.json`.
- When adding a new pattern, write the rationale in a single row, not a long essay.
