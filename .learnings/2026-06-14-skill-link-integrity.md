---
name: skill-link-integrity-validator
description: When auditing a Claude Skill's `references/` tree, the most common dead links come from a multi-skill → single-skill reorganization and from generator output that re-emits upstream `../docs/...` paths. A single "resolve-then-check-existence" rule in a validator catches both.
metadata:
  type: project
  applies-to: skill-authoring, repo-audit
---

# Skill link integrity: two recurring dead-link patterns

When auditing a Claude Skill (or any documentation tree) that pulls in
generator output, the **two** most common classes of broken markdown links
are:

1. **Cross-skill escapes from a multi-skill → single-skill migration.** A
   previous version of the skill split its content into several
   `skills/<name>-<topic>/` directories; later it collapsed into one. The
   foundation/ files still contain `[…](../naive-ui-theming/SKILL.md)`
   links that point at the old siblings. Detected in
   [naive-ui-skill audit 2026-06-14](../README.md) — 6–8 instances in
   the foundation tree.
2. **Generator-emitted upstream docs paths.** The extractor copies
   `demos/index.demo-entry.md` content verbatim, including relative
   links like `../docs/customize-theme` that mean
   `https://www.naiveui.com/.../docs/customize-theme` upstream but resolve
   to nothing in the local skill tree. Detected in
   [n-config-provider/api.md](../skills/naive-ui/references/components/n-config-provider/api.md).

**Why:** both classes silently rot the user experience — an agent following
the link gets a 404 inside the skill instead of useful docs. CI didn't
catch them because most validators only check that the markdown
*parses*, not that the link *resolves*.

**How to apply:** in any skill/repo validator, add a single check:

```python
for href in re.findall(r"\]\(([^)]+)\)", text):
    if href.startswith(("http://", "https://", "#", "mailto:")):
        continue
    clean = href.split(None, 1)[0]                 # strip " \"title\""
    if not (clean.startswith("./") or clean.startswith("../")):
        continue
    target = (md.parent / clean).resolve()
    try:
        target.relative_to(skill_root)             # must stay inside skill
    except ValueError:
        errors.append(...)
    if not target.exists():                        # must actually exist
        errors.append(...)
```

This catches **both** patterns in one rule — the cross-skill link escapes
the skill root (first check), the `../docs/...` link resolves to a
nonexistent path (second check). No special-cases needed.

**Don't add a `info:` / severity tier** for "we know this is upstream
docs" — it becomes maintenance debt and lets new instances of the same
pattern slip through. Instead, fix the generator (or the few
hand-written files) to use a full https URL when pointing at the
upstream site, and the rule returns to binary "exists / doesn't exist".

Related: [[naive-ui-skill-audit-2026-06-14]] for the full audit report.
