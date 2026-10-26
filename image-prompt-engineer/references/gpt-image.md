# GPT Image (OpenAI)

Last checked against OpenAI's image docs on 26 October 2026. Models change often: check
https://developers.openai.com/api/docs/guides/image-prompting before relying on the limits below.

## Models

| Model | ID | Use it when |
|---|---|---|
| **GPT Image 2.5 Sunburst** (default) | `gpt-image-2.5-sunburst` | Final assets, precise edits, demanding quality. |
| GPT Image 2.5 Flare | `gpt-image-2.5-flare` | Fast everyday generation and drafts. Quality is roughly GPT Image 2. |
| GPT Image 2 | `gpt-image-2` | The user has a validated GPT Image 2 workflow. |

`gpt-image-1.5` is deprecated (shutdown 1 December 2026) and `gpt-image-1` is retired. DALL-E is
no longer offered: treat "DALL-E" as a request for GPT Image.

OpenAI's advice for choosing: start with Sunburst when quality matters, then test Flare with the
same prompts and switch if quality holds.

## Settings

**Size:** `auto`, or a custom `WIDTHxHEIGHT` where each edge is at most 3,840px and a multiple of
16, the long edge is at most 3x the short edge, and total pixels are between 655,360 and 8,294,400.
Above 3,686,400 pixels (e.g. 2560x1440) is experimental.

Map aspect ratios to sizes like this:

| Aspect ratio | Standard size | Large (experimental) |
|---|---|---|
| 1:1 | 1024x1024 | 2048x2048 |
| 3:2 / 2:3 | 1536x1024 / 1024x1536 | — |
| 4:3 / 3:4 | 1536x1152 / 1152x1536 | — |
| 4:5 / 5:4 | 1024x1280 / 1280x1024 | — |
| 16:9 / 9:16 | 2048x1152 / 1152x2048 | 3840x2160 / 2160x3840 |
| 21:9 | 2688x1152 | — |

Ratios beyond 3:1 (such as `1:4`, `4:1`, `8:1`) are not possible. Offer `3:1` / `1:3` instead, or
suggest Nano Banana.

**Quality:** `auto` (default), `low`, `medium`, `high`, `xhigh`, `max` on GPT Image 2.5
(`low`, `medium`, `high`, `auto` on GPT Image 2). Use `medium` or higher for small or dense text.
Only use `xhigh` or `max` when a lower setting has visibly failed: they are slower and cost more.

**Background:** `transparent` for logos, stickers and cut-outs. Needs PNG or WebP output.

**`n`:** number of images per request. Useful for logo or layout variations.

## Defaults

- Model: `gpt-image-2.5-sunburst`
- Aspect ratio: `16:9` → size `2048x1152`
- Quality: `auto`

## Where to paste

You usually won't know where the user pastes, so the prompt must work in all of these. The brief
always carries the aspect ratio, and settings are a bonus where the tool has them.

- **ChatGPT**: paste the prompt into a chat. ChatGPT has no size or model setting, so write the
  aspect ratio and orientation into the prompt as a closing sentence ("Landscape, 16:9."), and ask
  for a transparent background in words if needed.
- **OpenAI Playground / API**: set model, size, quality and background as parameters. Needs an
  OpenAI API account with billing, so mention it only for users who already have one. See
  `scripts/generate.py`.

## Prompting rules for GPT Image

- **Lead with the result.** Open with what the image is and what it's for ("A product hero image
  for a skincare landing page: ..."), then describe the visible details.
- **For complex images, use labelled sections.** GPT Image follows structure well. For dense briefs,
  assemble the prompt as short labelled sections instead of one paragraph:
  ```
  Scene: ...
  Subject: ...
  Details: ...
  Text: "..." in ...
  Constraints: ...
  ```
  JSON-like structures also work. OpenAI's guide says to use whichever form is easiest to read and
  update.
- **Ask for photorealism explicitly** when that's the goal ("a photorealistic photograph"), and
  describe light, materials, framing and texture.
- **Text:** quote every word, describe placement and typography, and end with "No other text."
  Spell unusual words letter by letter. Check spelling in the output.
- **References:** number every input image and give it a role: "Image 1: the product. Image 2: the
  style reference. Image 3: the background." Then say how they combine.
- **Edits:** say what to change, list what must stay fixed, and state exclusions (no added logos or
  watermarks). Change one thing at a time and inspect the result. For local edits, a mask (PNG
  with an alpha channel) limits the change to one area.
- **Iterate on the output.** Pass the previous image back as an input, request one change, and
  restate the details to preserve.
- **No web search in the Image API.** If the brief needs real-time data, look it up first (or ask the
  user), then write the facts into the prompt as plain description. In ChatGPT, the user can ask
  ChatGPT to search first in the same chat.

## API notes

- Generate: `POST https://api.openai.com/v1/images/generations` (JSON body: `model`, `prompt`,
  `size`, `quality`, `background`, `n`).
- Edit or use references: `POST https://api.openai.com/v1/images/edits` (multipart form, one
  `image[]` field per input image, optional `mask`).
- The response holds base64 images in `data[i].b64_json`.
