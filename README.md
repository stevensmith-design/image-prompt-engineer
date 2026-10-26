# Image Prompt Engineer

A Claude skill that turns a rough image idea into a structured JSON prompt, then into the best
prompt for **Nano Banana** (Google Gemini Image) or **GPT Image** (OpenAI / ChatGPT).

It runs a short creative interview, fills in a JSON spec covering subject, composition, lighting,
camera, text and references, and assembles a prompt that follows each model's own prompting rules.
You copy it and paste it into the Gemini app, Google AI Studio or ChatGPT. No API key or setup
needed.

If you do have an API key, there's an optional script that lets Claude Code generate the image,
review it against the spec and refine it. You don't need it to use the skill.

## Why JSON

A one-line prompt leaves most decisions to the model. A JSON spec makes every decision explicit:
what the subject is, how it's framed, where the light comes from, what text appears and in which
font. That has three effects:

- **Less ambiguity.** Gaps in the brief become empty fields you can see, not guesses the model makes.
- **Predictable iteration.** To change the lighting, change the `lighting` field. Everything else
  stays put.
- **Reuse.** Keep the `style` and `camera` blocks and swap the subject to make a consistent series.

The prompt you paste combines both: a plain-language summary on top, so the model understands
the image as a whole, and the JSON details underneath, so nothing is left to chance. Both models
read JSON in a prompt. For simple images, prose alone often gives near-identical results, and you
can ask for prose only. The JSON earns its place on complex images: several subjects, exact text,
precise layout.

The two halves divide the work. The summary is the brief: the scene, the mood, how the main
elements relate to each other ("sitting side by side"), and the rules that must not fail ("every
menu line in Japanese and English"). The JSON holds the detail: each person's appearance, exact
text, materials, camera and light. In testing, prose alone got relationships and overall rules
right but lost detail, while JSON alone kept detail but misread positions. Together they cover
each other.

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

The skill asks one or two questions if it needs to (or skips them if you say "just go"), then
returns one prompt to paste:

```
A ceramic mug of black coffee on a worn oak windowsill, a thin ribbon of steam rising, in a small apartment kitchen with soft city rooftops blurred outside the window. ...

{
  "operation": "generate",
  "framework": ["text-to-image", "creative-director"],
  "subject": "A ceramic mug of black coffee on a worn oak windowsill",
  "action": "A thin ribbon of steam rising",
  "location_context": "A small apartment kitchen, soft city rooftops blurred outside the window",
  "composition": "Close-up, mug in the lower-left third, wide empty window light above for a headline",
  "camera": { "lens": "50mm", "aperture": "f/2", "focus": "shallow depth of field on the mug rim" },
  "lighting": "Low early-morning sun from camera-right, long soft shadows",
  "style": { "genre": "cinematic lifestyle photography", "color_grading": "warm amber highlights, muted shadows" }
}
```

Under it: "Paste into Google AI Studio. Model: Nano Banana 2.1, aspect ratio 16:9, resolution 2K."
Then a short list of refinements.

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

## How to use it

No API key, no setup. You need the skill installed and an account with the image app you
already use.

1. **Ask for an image in plain words.** Name the model or app if you know it: "Write me a Nano
   Banana prompt for a hero image of a quiet Kyoto tea house at dawn", or "I need a ChatGPT image
   prompt for a logo sticker". The skill triggers on its own.
2. **Answer a few questions,** or say "just go ahead" to skip them. The skill fills the gaps with
   sensible defaults and tells you what it assumed.
3. **Copy the prompt.** The reply has one block labelled **Prompt to paste**: a plain-language
   summary on top and the JSON details underneath. Copy the whole block, both parts together. The
   line under it says where to paste it and which settings to pick.

   In Claude.ai and Claude Desktop, use the copy button on the **Prompt to paste** block. In Claude
   Code (terminal or IDE), say **copy** and the skill puts the prompt on your clipboard. It never
   copies without asking, so it won't overwrite something you've already copied.
4. **Paste it into your image app:**
   - **Nano Banana**: the [Gemini app](https://gemini.google.com) (the aspect ratio is written into
     the prompt, since the app has no setting for it) or [Google AI Studio](https://aistudio.google.com)
     if you want to pick the model and resolution yourself.
   - **GPT Image**: ChatGPT (the aspect ratio is written into the prompt, since ChatGPT has no
     setting for it) or the OpenAI Playground.
5. **Refine.** Tell the skill what to change ("warmer light", "move the mug left", "make the text
   Japanese") and it updates the JSON and gives you a new prompt. To edit an image you've already
   generated, attach it and say what to change and what must stay the same.

Prefer one or the other? Ask for "prose only" or "JSON only".

The skill answers in the chat. It doesn't write prompts to files unless you ask it to save them.

## Generating images from Claude Code (optional)

Skip this section if you just want prompts to paste. The skill never asks you to set up an API.

The skill includes [`scripts/generate.py`](image-prompt-engineer/scripts/generate.py), a small
script that sends a JSON spec straight to the Gemini or OpenAI API. It needs only Python 3, no
packages.

```bash
export GEMINI_API_KEY=...   # or OPENAI_API_KEY=...

python3 generate.py --spec prompts/hero.json --out images/
python3 generate.py --spec prompts/hero.json --send prose     # summary only (or --send json)
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
numbering references, handling unsupported requests, and never pushing API setup on someone who just wants a prompt. Run them with Anthropic's
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
