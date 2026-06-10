---
name: "{componentKebab}-examples"
description: "Official demo index for {componentTitle} (enUS + zhCN). Invoke when the user wants to look up an official demo for a specific use case."
metadata:
  author: klarkxy
  version: "{version}"
  source: "tusen-ai/naive-ui"
  sourceRef: "{officialRef}"
  generatedAt: "{generatedAt}"
---

# {componentTitle} Examples Index

> Source: the `demo` block in `src/{componentPath}/demos/{enUS,zhCN}/index.demo-entry.md`. File list and titles are refreshed by `scripts/extract_official.py`; the full demo body lives in the upstream `tusen-ai/naive-ui` repository.

## Contents

{examplesToc}

{examplesBody}

## Maintenance

- Keep this file as a thin index only. Long snippets stay in the upstream repository.
- Re-run `python scripts/extract_official.py` whenever the official demo list changes.
