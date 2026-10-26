# Changelog

## 1.0.0 — 2026-10-26

First public release. Grew out of `nano-banana-prompter`.

- Supports two model families: Nano Banana (Gemini Image) and GPT Image (OpenAI / ChatGPT).
- Model-specific prompting rules, settings and limits moved into `references/`, each with a
  "last checked" date.
- JSON spec separates content fields from `output` settings, adds `preserve` for edits and numbered
  `references`.
- Optional `scripts/generate.py` (standard library only) to generate and edit images from a spec,
  with a dry-run mode and a JSON record saved next to every image.
- Generate-and-review loop for Claude Code.
- Copy and paste is the default; API generation is opt-in and never pushed.
- Eight worked examples and ten evals.
