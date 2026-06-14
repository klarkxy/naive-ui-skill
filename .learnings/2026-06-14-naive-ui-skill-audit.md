---
name: naive-ui-skill-audit-2026-06-14
description: Audit + cleanup of the naive-ui-skill repo on 2026-06-14. Captures the original findings (6 broken cross-skill links, vite-ssge filename typo, README dist/ inconsistency, validate.py gap) and the resolution. Useful as the trail of evidence for the linked link-integrity learning.
metadata:
  type: project
  applies-to: naive-ui-skill
---

# naive-ui-skill audit & cleanup — 2026-06-14

Branch: `main` @ `90de6d1` (before this session).

## Findings (initial)

| # | Severity | Issue |
| --- | --- | --- |
| 1 | 🟠 | 6–8 broken cross-skill links in `references/foundation/*.md` (`../naive-ui-theming/SKILL.md` etc.) — leftover from a multi-skill → single-skill layout collapse |
| 2 | 🟠 | `references/rules/core-vite-ssge.md` filename typo + 2× `vite-sse` (non-existent product name) in body |
| 3 | 🟡 | README Option C references `dist/naive-ui.zip` which is .gitignore'd and not shipped |
| 4 | 🟡 | `scripts/validate.py` didn't catch cross-skill `../<other>/SKILL.md` links |
| 5 | 🟢 | `n-legacy-transfer/api.md` exists on disk but isn't in the official manifest's user-facing set (in EXCLUDED) — kept for historical reference, no marker |
| 6 | 🟢 | `assets/data/*.json` are GBK-encoded, not in the published skill (only `skills/naive-ui/` ships) |

## Fixes applied

1. Rewrote cross-skill links in: [quickstart.md](../skills/naive-ui/references/foundation/quickstart.md), [theming.md](../skills/naive-ui/references/foundation/theming.md), [dark-mode.md](../skills/naive-ui/references/foundation/dark-mode.md), [ssr.md](../skills/naive-ui/references/foundation/ssr.md), [design-color.md](../skills/naive-ui/references/foundation/design-color.md), [design-border.md](../skills/naive-ui/references/foundation/design-border.md), [design-overview.md](../skills/naive-ui/references/foundation/design-overview.md), [design-typography.md](../skills/naive-ui/references/foundation/design-typography.md). All → same-folder local paths.
2. `git mv core-vite-ssge.md → core-vite-ssg.md`; body `vite-sse` → `vite-ssg`; updated cross-ref in [core-ssr.md](../skills/naive-ui/references/rules/core-ssr.md).
3. README Option C: rewrite as "build the zip yourself first".
4. `scripts/validate.py`: added the resolve-then-check-existence rule. Bonus catch — it flagged a real `../../naive-ui/references/component-select.md` link in [component-select.md](../skills/naive-ui/references/rules/component-select.md) that the original audit missed.
5. `n-legacy-transfer/api.md`: deprecated banner pointing at `n-transfer`.
6. `n-config-provider/api.md`: 2× `../docs/customize-theme` → `https://www.naiveui.com/en-US/os-theme/docs/customize-theme` (official site, matches existing "Source Files" URL pattern). Removed the now-unused `info:` warning tier in `validate.py`.

## Verification

- `python scripts/validate.py --strict` → `No errors. exit=0` (final state)
- `python scripts/package_skill.py skills/naive-ui ./dist` → 338 files / ~482KB zip
- `git status` final: 12 modified + 1 rename (core-vite-ssge → core-vite-ssg)

## User policy notes for future audits

- **User has explicitly accepted that `assets/` is build-time only, not
  shipped.** Don't re-flag GBK encoding of `assets/data/*.json` as a
  distribution issue.
- **User prefers official-site redirects over local-stub `../docs/...`**
  for upstream docs references. Future regenerate of api.md should
  convert `../docs/<slug>` → `https://www.naiveui.com/en-US/os-theme/docs/<slug>`.

Related: [[skill-link-integrity-validator]] for the reusable validator
pattern that was extracted from this session.
