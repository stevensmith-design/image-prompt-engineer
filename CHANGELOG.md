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
- Prompts are answered in the chat with labelled blocks, never written to a file unless asked, with an opt-in clipboard copy in Claude Code (`scripts/copy_prompt.py`). It never copies unasked, so it never overwrites the clipboard.
- The prompt to paste is one block: a plain-language summary on top, JSON details underneath. `generate.py` sends the same combined prompt by default.
- The brief always ends with the aspect ratio, since the Gemini app and ChatGPT have no setting for it. The prompt works wherever it is pasted; the settings line names options for tools that have them.
- Nine worked examples and twelve evals.
- The summary is a short brief (scene, mood, relationships, must-not-fail rules) and the JSON holds the details. New `characters` and `spatial_relationships` fields, and multilingual text split into `parts`.
