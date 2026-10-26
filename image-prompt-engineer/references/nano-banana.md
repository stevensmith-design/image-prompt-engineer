# Nano Banana (Google Gemini Image)

Last checked against Google's Gemini API docs on 26 October 2026. Models change often: check
https://ai.google.dev/gemini-api/docs/image-generation before relying on the limits below.

## Models

| Model | ID | Use it when |
|---|---|---|
| **Nano Banana 2.1** (default) | `gemini-nano-banana-2.1` | Almost everything. Google's recommended model for new work. |
| Nano Banana Pro | `gemini-3-pro-image` | Text-heavy designs and professional assets, style reference images, or the user asks for Pro. |
| Nano Banana 2 | `gemini-3.1-flash-image` | The user needs 0.5K (512px) output. Previous generation. |
| Nano Banana 2 Lite | `gemini-3.1-flash-lite-image` | Cheap, fast 1K drafts with no search grounding. |

`gemini-2.5-flash-image` (the original Nano Banana) is legacy. Don't recommend it for new work.

## Limits

| | 2.1 | Pro | 2 | 2 Lite |
|---|---|---|---|---|
| Resolutions | 1K, 2K, 4K | 1K, 2K, 4K | 0.5K, 1K, 2K, 4K | 1K only |
| Reference images (max 14 total) | 10 objects + 4 characters | 6 objects + 5 characters + 3 style | 10 objects + 4 characters | 14 objects |
| Search grounding | Web + image search | Web search | Web + image search | No |
| Thinking levels | minimal, medium, high (default medium) | Always on | minimal, high (default minimal) | minimal, high |

**Aspect ratios:** `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`. Nano
Banana 2.1 and 2 also support the extreme ratios `1:4`, `4:1`, `1:8`, `8:1`.

**Resolution values** are case-sensitive in the API: `"2K"`, not `"2k"`. Default is 1K.

All outputs carry a SynthID watermark.

## Defaults

- Model: `gemini-nano-banana-2.1`
- Aspect ratio: `16:9`
- Resolution: `1K` for drafts. Suggest `2K` or `4K` for final assets.

## Where to paste

You usually won't know where the user pastes, so the prompt must work in all of these. The brief
always carries the aspect ratio, and settings are a bonus where the tool has them.

- **Gemini app** (gemini.google.com or the mobile app): paste the prompt and send. The app has no
  aspect ratio or resolution setting and may choose the model itself, so the brief must end with the
  aspect ratio ("Wide 16:9 landscape format."). Don't promise a specific model or resolution here.
  For text-heavy images, tell the user that results may vary with the model the app uses, and that
  AI Studio lets them pick Nano Banana Pro.
- **Google AI Studio** (aistudio.google.com): pick the model, aspect ratio and resolution in the
  settings panel, then paste the prompt. Best for control.
- **API / Vertex AI**: send the prompt as `input`, and set `aspect_ratio` and `image_size` in
  `response_format`. See `scripts/generate.py`.

## Prompting rules for Nano Banana

- **Write a narrative description, not a keyword list.** Google's own examples are full,
  descriptive sentences. The more specific the scene, the more control you get.
- **Text rendering is a strength.** State the exact text in quotes, a descriptive font style, and
  the colour scheme. Prefer Pro for dense or professional typography.
- **Leave room for overlaid text** by placing the subject off-centre and describing the empty
  background ("subject in the lower-right third, wide empty sky above").
- **References:** stay within the per-model limits above. For characters, say "keep the exact face,
  hair and clothing from Image 1". Use Pro when the user wants dedicated style references.
- **Sequential art and storyboards** work best with Pro and Nano Banana 2.
- **Editing:** attach the image and say what should change and what should stay the same. The model
  matches the original's style, lighting and perspective. For several rounds of edits, continue the
  same conversation (or pass `previous_interaction_id` in the API) instead of starting over.
- **Search grounding:** for real-time data (weather, scores, stock charts, recent events), tell the
  model to search, then say how the result should change the image. In the API, add
  `tools: [{"type": "google_search"}]`. Not available on 2 Lite.
- **Localization:** Nano Banana can translate text in place. Ask for "the same design with the text
  translated into Japanese", and check the output with a native speaker before using it.

## API notes

The Gemini API generates images through the Interactions endpoint:

```
POST https://generativelanguage.googleapis.com/v1beta/interactions
x-goog-api-key: $GEMINI_API_KEY

{
  "model": "gemini-nano-banana-2.1",
  "input": [
    {"type": "text", "text": "<prompt>"},
    {"type": "image", "mime_type": "image/png", "data": "<base64>"}
  ],
  "response_format": {"type": "image", "mime_type": "image/jpeg", "aspect_ratio": "16:9", "image_size": "2K"}
}
```

Up to two interim "thought" images may come back before the final one. The last image is the
final render.
