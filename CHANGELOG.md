# Changelog

## 1.0.0 — 2026-10-26

First public release.

- Writes image prompts for Nano Banana (Gemini Image) and GPT Image (OpenAI / ChatGPT).
- One prompt to paste: a short plain-language brief on top (scene, mood, how elements relate, the
  rules that must not fail, the aspect ratio), with the JSON details underneath.
- Prompt first, questions after: you get a finished prompt in the first reply, with sensible
  defaults and a few optional tweaks.
- Works by copy and paste in the free Gemini app or ChatGPT. No API key or setup.
- Each prompt comes with four short instructions: where to paste it (new chat or the same one),
  the target size, what to attach, then the prompt.
- Five frameworks: text-to-image, multimodal, web-search, text rendering and creative director.
- Model IDs, sizes, limits and prompting rules for each model in `references/`, each with a
  "last checked" date.
- Nine worked examples, including a complex multi-character, bilingual scene, and a complete
  answer as the user sees it.
- In Claude Code: answers stay in the chat, and the prompt goes to your clipboard when you say
  "copy".
- Optional `scripts/generate.py` (Python standard library only) to generate and edit images through
  the Gemini or OpenAI API, with a dry-run mode and a record of the prompt saved next to each image.
- Example images in the README, made with Nano Banana from prompts this skill wrote.
- Thirteen evals.
