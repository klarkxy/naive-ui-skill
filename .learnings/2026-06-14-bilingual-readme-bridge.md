---
name: bilingual-readme-bridge
description: When shipping a bilingual README, the language-toggle line in the source-language file should be pure ASCII (BCP-47 code + flag emoji) — never the target language's own script. That makes "source file is X-clean" mechanically checkable with a one-line `grep`.
metadata:
  type: project
  applies-to: docs, l10n, README
---

# Bilingual README: bridge the two versions, keep the source pure

When shipping a `README.md` (English) + `README.<lang>.md` (e.g.
`README.zh-CN.md`) pair, the language-toggle line at the top of **each**
file is a piece of meta-content that needs to stay in sync. The common
pattern is:

```markdown
# Project Name

> 🌐 **You are reading the English version.** [Switch to zh-CN →](./README.zh-CN.md)
```

## Rule: the source-language file's bridge uses ASCII, not the target script

A naive bridge is tempting:

```markdown
# ❌ English README contains the target's own script
> 🌐 **You are reading the English version.** [简体中文 →](./README.zh-CN.md)
```

This forces the English README to carry Chinese characters just to label
the link — which is exactly what a "no Chinese in the English README"
policy says not to do. **The fix is to label the link with pure ASCII
identifiers** that any reader can decode:

```markdown
# ✅ English README stays ASCII-clean
> 🌐 **You are reading the English version.** [🇨🇳 Switch to zh-CN →](./README.zh-CN.md)
```

- The **flag emoji** is universal — `🇨🇳` is recognizable to non-Chinese
  readers as the China flag.
- The **BCP-47 code** (`zh-CN`, `ja`, `fr`, …) is the standard way
  computers refer to a language; readers familiar with i18n get it
  immediately.
- **No characters from the target language** appear in the source file.

## Why this matters

1. **It becomes a mechanical property.** "README.md is Chinese-free" is
   one `grep` away:

   ```bash
   LC_ALL=C grep -nP '[\xe4-\xe9]' README.md
   ```

   (UTF-8 3-byte sequences in the CJK range start with `0xE4`–`0xE9`.)
   Wire that into `validate.py` and a regression is a CI failure, not
   a code review miss.
2. **It survives translation churn.** If you later add a `README.ja.md`
   or `README.fr.md`, you don't need to teach the bridge line the
   new language's script.
3. **The non-source file has no constraint.** `README.zh-CN.md` can
   freely use `English →` as its link label — `English` is the English
   word, not English-language characters in the source file's
   script sense.

## Detect-and-fix recipe

```bash
# Find CJK characters (or any script) in a file
LC_ALL=C grep -nP '[\xe4-\xe9]' README.md      # CJK
LC_ALL=C grep -nP '[\xd0-\xd3][\x80-\xbf]{2}|[\xd7][\x80-\xbf]{2}' README.md  # Cyrillic
LC_ALL=C grep -nP '[\xe3\x81-\xe3\xbf]' README.md  # Hiragana / Katakana
```

If `validate.py` is part of the project, add the same scan as a hard
check. It costs nothing and prevents the "I forgot to scrub the
example" class of regression.

Related: [[skill-link-integrity-validator]] for a different
"no-leakage" rule (links must resolve to existing files inside the
skill root).
