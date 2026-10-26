# Image Prompt Engineer

A Claude skill that turns a rough image idea into a structured JSON prompt, then into the best
prompt for **Nano Banana** (Google Gemini Image) or **GPT Image** (OpenAI / ChatGPT).

It runs a short creative interview, fills in a JSON spec covering subject, composition, lighting,
camera, text and references, and assembles a paste-ready prompt that follows each model's own
prompting rules. In Claude Code it can also generate the image, review it against the spec and
refine it.

## Why JSON

A one-line prompt leaves most decisions to the model. A JSON spec makes every decision explicit:
what the subject is, how it's framed, where the light comes from, what text appears and in which
font. That has three effects:

- **Less ambiguity.** Gaps in the brief become empty fields you can see, not guesses the model makes.
- **Predictable iteration.** To change the lighting, change the `lighting` field. Everything else
  stays put.
- **Reuse.** Keep the `style` and `camera` blocks and swap the subject to make a consistent series.

Both models accept JSON-like structures directly, so you can paste the JSON itself, or paste the
assembled natural-language prompt the skill builds from it. Try both on your own images: the
generation script's `--send json` flag makes that comparison easy.

## What it covers

| | Nano Banana | GPT Image |
|---|---|---|
| Models | 2.1 (default), Pro, 2, 2 Lite | 2.5 Sunburst (default), 2.5 Flare, 2 |
| Text-to-image | Yes | Yes |
| Reference images | Up to 14, by role | Numbered inputs |
| Live web search | Yes (search grounding) | No, facts are written into the prompt |
| Text rendering and localization | Yes | Yes |
| Creative director (camera, lens, film stock) | Yes | Yes |
| Edits that preserve the rest of the image | Yes | Yes, plus masks |
| Transparent backgrounds | No | Yes |

Model IDs, sizes and limits live in [`references/`](image-prompt-engineer/references), each with
the date it was last checked against the official docs.

## Example

> **You:** Hero image for a blog post about slow mornings. Warm, quiet, a bit cinematic. For Nano Banana.

The skill asks one or two questions if it needs to (or skips them if you say "just go"), then returns:

```json
{
  "operation": "generate",
  "framework": ["text-to-image", "creative-director"],
  "subject": "A ceramic mug of black coffee on a worn oak windowsill",
  "action": "A thin ribbon of steam rising",
  "location_context": "A small apartment kitchen, soft city rooftops blurred outside the window",
  "composition": "Close-up, mug in the lower-left third, wide empty window light above for a headline",
  "camera": { "lens": "50mm", "aperture": "f/2", "focus": "shallow depth of field on the mug rim" },
  "lighting": "Low early-morning sun from camera-right, long soft shadows",
  "style": { "genre": "cinematic lifestyle photography", "color_grading": "warm amber highlights, muted shadows" },
  "output": { "model": "gemini-nano-banana-2.1", "aspect_ratio": "16:9", "resolution": "2K" },
  "natural_language_prompt": "A ceramic mug of black coffee on a worn oak windowsill, a thin ribbon of steam rising. ..."
}
```

It then shows the prompt to paste on its own, tells you where to paste it and which settings to
pick, and offers refinements.

More worked examples: [`references/examples.md`](image-prompt-engineer/references/examples.md).

## Install

**Claude Code**

```bash
git clone https://github.com/<your-username>/image-prompt-engineer.git
cp -r image-prompt-engineer/image-prompt-engineer ~/.claude/skills/
```

**Claude.ai and Claude Desktop**

Download `image-prompt-engineer.skill` from the
[latest release](../../releases/latest), then upload it under **Settings → Capabilities → Skills**.
(To build it yourself, run `./build.sh`.)

Then ask for an image prompt in plain words, for example "write me a GPT Image prompt for...". The
skill triggers on its own.

## Generating images from Claude Code (optional)

The skill includes [`scripts/generate.py`](image-prompt-engineer/scripts/generate.py), a small
script that sends a JSON spec straight to the Gemini or OpenAI API. It needs only Python 3, no
packages.

```bash
export GEMINI_API_KEY=...   # or OPENAI_API_KEY=...

python3 generate.py --spec prompts/hero.json --out images/
python3 generate.py --spec prompts/hero.json --send json      # send the JSON instead of prose
python3 generate.py --spec prompts/edit.json --ref images/hero.jpg
python3 generate.py --spec prompts/hero.json --dry-run        # print the request, send nothing
```

Settings are read from the spec's `output` block. Each image is saved with a `.json` record of the
exact prompt and settings that made it.

With a key set, Claude can run the full loop: write the spec, generate, look at the result, compare
it field by field against the spec, and fix only what's wrong. Each image costs money on your API
account, so the skill asks before generating several images or using the most expensive settings.

## Evals

[`evals/evals.json`](evals/evals.json) holds test prompts with checks for the behaviours that
matter: skipping the interview when told to, picking the right model, valid sizes, quoting text,
numbering references, handling unsupported requests. Run them with Anthropic's
[skill-creator](https://github.com/anthropics/skills) eval tooling.

## Keeping it current

Image models change every few months. When a new model ships, update its file in `references/`
(model IDs, limits, defaults and the "last checked" date) and the defaults in
`scripts/generate.py`. Pull requests are welcome.

## Credits

The five frameworks and base formulas build on Google Cloud's
[Ultimate prompting guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
and OpenAI's [image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting).

Not affiliated with Google, OpenAI or Anthropic. Nano Banana, Gemini, GPT Image and ChatGPT are
trademarks of their owners.

## License

[MIT](LICENSE) © 2026 Steven Smith
