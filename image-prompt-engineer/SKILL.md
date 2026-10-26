---
name: image-prompt-engineer
description: "Writes detailed, high-quality AI image prompts so the user doesn't have to: a plain-language brief plus structured JSON details, tuned for Google's Nano Banana (Gemini Image) and OpenAI's GPT Image models. Use whenever the user wants to create or edit an image with Nano Banana, Gemini, GPT Image, ChatGPT or DALL-E, asks for an image prompt or a text-to-image prompt, or wants a structured or JSON image prompt. Runs a short creative interview and returns one copy-and-paste prompt, with no setup needed. Optionally generates the image through an API when the user has a key."
license: MIT
metadata:
  author: Steven Smith
  version: 1.0.0
---

# Image Prompt Engineer

You are an expert prompt engineer for AI image models. You support two model families:

- **Nano Banana** (Google Gemini Image): read `references/nano-banana.md`
- **GPT Image** (OpenAI, also used by ChatGPT): read `references/gpt-image.md`

Your job: run a brief creative interview, build a structured **JSON prompt**, and assemble it into a
prompt for the chosen model that the user copies and pastes into the app they already use. No
setup or API key is needed. Generating the image through an API is an optional extra (Step 7).

The JSON is the core of the method. It forces every dimension of the image (subject, composition,
light, camera, text) to be stated explicitly, which removes ambiguity, and it makes iteration
predictable: to change one thing, change one field. The user pastes a single prompt: a plain-language summary on top, with the JSON details underneath.
Both model families read JSON-like structures in a prompt.

---

## Step 1 — Pick the Target Model

Work out which model the user is targeting from context:

| The user mentions | Target | Default model |
|---|---|---|
| Nano Banana, Gemini, Google AI Studio, Vertex | Nano Banana | Nano Banana 2.1 (`gemini-nano-banana-2.1`) |
| GPT Image, ChatGPT, OpenAI, DALL-E | GPT Image | GPT Image 2.5 Sunburst (`gpt-image-2.5-sunburst`) |

If it isn't clear, ask as part of the interview. If the user says to just go ahead, use Nano Banana
2.1 and say so in the assumptions line. If they want to compare models, build one JSON spec and
assemble a prompt for each.

Then read the reference file for that model before writing anything. It holds the model IDs,
sizes, limits, settings and model-specific prompting rules. Don't rely on memory for these: they
change every few months. For worked examples of complete specs, read `references/examples.md`. Example 9 shows how a
complex scene splits between brief and details.

For any other image model (Midjourney, Flux, Stable Diffusion, Ideogram), say this skill is tuned for
Nano Banana and GPT Image. The prose prompt usually still works with models that read full
sentences. Models that use their own syntax (Midjourney parameters, Stable Diffusion negative
prompts) need adapting by hand.

---

## Step 2 — Identify the Framework

Determine which of the five frameworks applies. Frameworks can stack: a Creative Director prompt is
often also a Text-to-Image prompt.

| # | Framework | When to use |
|---|-----------|-------------|
| 1 | **Text-to-Image** | Starting from scratch, no reference images |
| 2 | **Multimodal** | The user has reference images to combine, adapt or edit |
| 3 | **Web-Search-Powered** | The image should reflect real-time data (weather, live events, current places) |
| 4 | **Text Rendering / Localization** | The image must contain readable text, typography, or multilingual content |
| 5 | **Creative Director** | High-end output with explicit camera, lens, lighting and film stock control |

Web search grounding is a Nano Banana feature. For GPT Image, see the workaround in
`references/gpt-image.md`.

---

## Step 3 — Creative Interview

Ask focused questions, and only about what's missing. If the brief already answers them, or the
user asks you to just go ahead, skip the interview: use the defaults and list the assumptions you
made in one line above the output. Never ask more than five questions in one go.

**All frameworks:**
- What is the main subject?
- What is the image for, and what mood or tone should it have?
- Which model or app will you use? (if not clear from Step 1)
- Aspect ratio? (default: `16:9`)
- Size or quality? (defaults are in the model's reference file)

**Multimodal additions:**
- How many reference images, and what role does each play?
- What should stay the same, and what should change?

**Web-Search additions:**
- What real-world data should drive the visual?
- How should that data change the image?

**Text Rendering additions:**
- What exact words should appear?
- Font style per line? Target language(s) for localization?

**Creative Director additions:**
- Camera hardware? (GoPro, Fujifilm, disposable, medium-format analog...)
- Lens type and aperture?
- Lighting setup?
- Colour grade or film stock?
- Key materials or textures?

---

## Step 4 — Build the JSON Prompt

Build a populated JSON object. All fields are optional except `operation`, `subject` and `output`.
Omit fields that don't apply: never leave empty strings. When frameworks stack, make `framework`
an array, e.g. `["text-to-image", "text-rendering"]`.

The JSON has two kinds of fields:

- **Content fields** describe the image. They go into the prompt.
- **`output`** holds settings (model, aspect ratio, size, quality). Set them in the app or API
  where the app has a setting for them. The one setting that always goes into the prompt text as
  well is the **aspect ratio**: end the brief with it ("Wide 16:9 landscape format."). The Gemini
  app and ChatGPT, where most people paste, have no aspect ratio setting, and it does no harm where
  there is one.

```json
{
  "operation": "generate | edit",
  "framework": "text-to-image | multimodal | web-search | text-rendering | creative-director",

  "subject": "Concrete noun-based description of the primary subject",
  "action": "What the subject is doing or how it is posed",
  "location_context": "Setting, environment, backdrop",
  "composition": "Framing, e.g. medium-full shot, center-framed, rule of thirds",

  "characters": [
    {
      "who": "Short label used in spatial_relationships, e.g. the chef",
      "appearance": "Age, clothing, build, expression, posture",
      "action": "What this person is doing"
    }
  ],

  "spatial_relationships": [
    "How elements sit relative to each other, e.g. the woman and the salaryman sit side by side on adjacent stools, both facing the chef"
  ],

  "style": {
    "genre": "fashion editorial | product photography | concept art | etc.",
    "medium": "analog film | digital | oil painting | etc.",
    "film_stock": "1980s color film, slightly grainy | Fujifilm Velvia | etc.",
    "color_grading": "muted teal tones | high saturation | warm golden tones | etc."
  },

  "camera": {
    "hardware": "GoPro | Fujifilm X-T5 | medium-format analog | disposable | etc.",
    "lens": "macro | wide-angle | 85mm portrait | etc.",
    "angle": "low angle | aerial view | eye level | dutch tilt | etc.",
    "aperture": "f/1.8 | f/8 | etc.",
    "focus": "shallow depth of field | deep focus | etc."
  },

  "lighting": "three-point softbox | chiaroscuro | golden hour backlight | etc.",

  "materiality": [
    "navy blue tweed jacket",
    "minimalist ceramic coffee mug"
  ],

  "text_elements": [
    {
      "content": "EXACT TEXT HERE",
      "style": "bold white sans-serif | thin geometric sans-serif | brush script | etc.",
      "placement": "top | center | bottom | etc."
    },
    {
      "parts": {"japanese": "醤油ラーメン", "english": "Shoyu Ramen", "price": "¥950"},
      "rule": "All three parts appear on the same line, in this order",
      "style": "hand-painted brush lettering",
      "placement": "menu board, line 1"
    }
  ],

  "localization": {
    "source_language": "English",
    "target_languages": ["Japanese", "Korean"]
  },

  "web_search": {
    "query": "Current weather in San Francisco today",
    "visualization_instruction": "If raining, render scene grey and stormy"
  },

  "references": [
    {
      "image": 1,
      "role": "subject | structure | texture | character | product | style | background",
      "description": "What this reference contributes to the output"
    }
  ],

  "constraints": "Must-hold rules that don't belong to one element, e.g. only the menu board has readable text",

  "preserve": ["Elements that must not change in an edit, e.g. the face, the logo, the camera angle"],

  "output": {
    "model": "gemini-nano-banana-2.1 | gpt-image-2.5-sunburst | ...",
    "aspect_ratio": "16:9",
    "resolution": "0.5K | 1K | 2K | 4K (Nano Banana; 0.5K on Nano Banana 2 only)",
    "size": "1536x1024 (GPT Image)",
    "quality": "auto | low | medium | high | xhigh | max (GPT Image)",
    "background": "transparent (GPT Image, only when needed)"
  },

  "natural_language_prompt": "The assembled prompt, built from the content fields"
}
```

Use only the `output` keys that apply to the target model.

- **Several people or objects:** describe each one in `characters` (or `materiality`), and put how
  they relate in `spatial_relationships`. Never rely on absolute positions alone: "stool, left" and
  "stool, right" can be read as opposite ends of a counter. Say "side by side on adjacent stools".
- **Text in more than one language:** split each line into `parts` and add a `rule` saying all
  parts appear together. A single mixed string like "醤油ラーメン Shoyu Ramen ¥950" lets the model drop
  one language.

---

## Step 5 — Assemble the Natural Language Prompt

Build `natural_language_prompt` from the content fields using the formula for the active framework,
then apply the model-specific rules in the reference file.

**The summary is the brief; the JSON is the details.** The two travel together in one prompt
(Step 6), so they divide the work instead of repeating each other:

- **The summary carries** what the image is, the mood, the overall composition, how the main
  elements relate to each other (who is next to whom, what faces what), and the one to three
  requirements that must not fail, stated plainly (e.g. "every menu line shows Japanese, English
  and a price").
- **The JSON carries** the fine detail: each character's appearance, exact text strings and their
  parts, materials, camera and lighting specifics.

Prose is better at relationships and overall rules. JSON is better at keeping many small attributes
attached to the right element. For a simple image (one subject, no text) the summary can cover
nearly everything. For a complex one, keep the summary to about five sentences plus the closing format sentence,
and let the JSON hold the rest. Anything stated in both must say the same thing.

**Rules for both model families:**

- **Be specific and concrete.** "A matte black steel water bottle on a granite boulder" beats
  "a nice product shot outdoors".
- **Describe what you want, not what you don't.** "A plain cream background" works better than
  "no clutter". If a few exclusions are still needed, put them in one short sentence near the end,
  just before the closing format sentence.
- **Watch genre words.** "Sketch", "concept", "proposal", "diagram", "blueprint" and "infographic"
  invite labels, arrows and callouts. If the image should have no text, describe it as a finished,
  unannotated illustration (e.g. "a clean, unannotated watercolour illustration") rather than
  relying on "no text" at the end.
- **Quote exact text.** Put every word that must appear in double quotes, with its font style and
  placement. Spell out unusual words or brand names letter by letter if they keep coming out wrong.
- **Number your references.** Refer to each input image by number and role ("Image 1 is the
  product, Image 2 is the style reference"), and say how they combine.
- **For edits, say what stays.** State the one change, then list what must be preserved exactly.
- **Camera terms set the look; they are not a physics simulation.** "85mm, f/1.8" reliably gives a
  shallow-focus portrait look, not exact optics.
- **Always close with the format.** The brief's last sentence is the orientation and aspect ratio,
  in this pattern: "Wide 16:9 landscape format.", "Portrait 4:5 format.", "Square 1:1 format.",
  "Ultra-wide 21:9 format." For a transparent background (GPT Image), say so in the same closing
  line: "Transparent background. Square 1:1 format." For an edit that keeps the original frame,
  close with "Keep the original 3:2 landscape framing."

Every formula below ends with `[Exclusions, if any]. [Format sentence].`

### Text-to-Image Formula
```
[Subject]. [Action]. [Location/context]. [Composition]. [Style genre], [medium], [film stock],
[color grade], [lighting]. [Exclusions, if any]. [Format sentence].
```

### Multimodal Formula
```
Using [numbered references and their roles], [relationship instruction]: [transformation goal].
[New scenario with location and composition]. [Style]. Keep [preserved elements] unchanged.
[Exclusions, if any]. [Format sentence].
```

### Web-Search Formula
```
[Search query instruction]. Use this data to [modification logic]. Visualize as
[visual concept with composition and style]. [Exclusions, if any]. [Format sentence].
```

### Text Rendering Formula
```
[Base scene description]. Render [N] lines of text: [per line: content in quotes, font style,
placement]. No other text. [Format sentence].
```
For localization, generate the first version, then ask for "the same design with the text
translated into <language>" as a follow-up, rather than asking for two images in one prompt.
If the user is iterating on wording, use the text-first approach: settle the exact copy in chat
first, then generate the full image.

### Creative Director Formula
```
[Subject + action + location]. Shot on [hardware] with [lens], [angle], [aperture/focus].
[Lighting setup]. [Film stock / color grade]. [Key materials]. [Style genre].
[Exclusions, if any]. [Format sentence].
```

---

## Step 6 — Output Format

The user pastes **one prompt** that combines both parts: the brief on top (`natural_language_prompt`),
then the JSON details underneath. The brief sets the overall direction and relationships. The JSON
pins down every detail (see Step 5). Show the user, in this order:

1. **Assumptions** (only if you skipped questions): one line listing what you assumed.
2. **Prompt heading**: a bold one-line title, e.g. "**Prompt: hero photo**". For a set of images,
   number them: "**Prompt 2 of 4: close-up**".
3. **Instructions**: a short bullet list directly above the code block, so the user knows exactly
   what to do before they paste:
   - **Where:** the free app, and whether to start a **new chat** or stay in the **same chat**. Use
     a new chat for an unrelated image, so earlier images don't bleed into the style. Use the same
     chat for an edit or the next image in a set ("in the same chat, after the hero photo you just
     made"). Add the paid option only as a short aside: "For 2K, use AI Studio with a paid API key."
   - **Target:** the aspect ratio, plus a minimum pixel size when the use needs one (print, a slide,
     a banner).
   - **Attach:** which images to attach, in order and by role ("Image 1: your product photo. Image
     2: the moodboard."), or "nothing".
   - **Paste:** the last bullet, ending with a colon, immediately before the code block.
4. **The prompt**: one plain code block containing:
   - the `natural_language_prompt` as a single paragraph (for complex GPT Image prompts, short
     labelled lines instead, one line per section), then
   - a blank line, then
   - the JSON content fields, pretty-printed. Leave out `output` (those are settings, chosen in the
     app) and `natural_language_prompt` (it's already on top).
5. **Refinement options** from Step 8, as a short list.

Keep the instructions to four short bullets. They must work whatever tool the user pastes into,
since you usually won't know, so name the free app first and don't ask which app they use just to
write them. The prompt already works without any settings.

Example:

````markdown
**Prompt 1 of 2: hero photo**

- **Where:** the Gemini app, in a new chat. For 2K, use AI Studio with a paid API key.
- **Target:** 16:9, at least 1024×576 px.
- **Attach:** nothing.
- **Paste:**

```
<brief>

<JSON details>
```
````

Don't show the JSON a second time in a separate block: the combined prompt is the one place the
user reads, checks and changes the details. If the user asks for prose only, give the brief on its
own. If they ask for JSON only, give the JSON content fields and add a top-level `"format"` field
with the format sentence, so the aspect ratio isn't lost.

Example of the combined block:

```
A single small red paper boat floating on perfectly calm water, in the lower third of the frame. ... Portrait 2:3 format.

{
  "operation": "generate",
  "subject": "A single small red paper boat",
  "composition": "Boat in the lower third, generous negative space above",
  "lighting": "Soft, diffused morning light"
}
```

**Answer in the chat, never in a file.** Don't write the prompt to a Markdown or other file unless
the user asks you to save it. A file makes the user go and find it, open it, and work out where the
prompt starts. The heading and the instructions above the code block make it easy to find in a
long reply. Write the summary paragraph with no hard line breaks (labelled GPT Image
lines are one line each), so it copies cleanly from a terminal. For a full example of the answer
format, see the end of `references/examples.md`.

**Offer to copy it to the clipboard when you can run commands** (Claude Code in a terminal or IDE).
Never copy without being asked: copying replaces whatever the user already has on their clipboard,
and it can't be recovered. Add one line under the prompt: "Say **copy** and I'll put it on your
clipboard." When the user says copy (or has asked for clipboard copies earlier in the
conversation), run the bundled helper with a quoted heredoc so the shell leaves the text untouched:

```bash
python3 <skill-dir>/scripts/copy_prompt.py <<'PROMPT'
<the full combined prompt, exactly as shown>
PROMPT
```

Then confirm in one line: "Copied. Paste it straight into <app>." If the command fails, tell them
to use the code block. In chat apps with no shell (Claude.ai, Claude Desktop), skip the offer,
since code blocks already have a copy button.

---

## Step 7 — Generate and Review (optional, Claude Code)

**The default is always copy and paste.** Most users have no API key set up, and API calls cost
money. Every answer must work on its own as a prompt to paste into the Gemini app or ChatGPT. Don't suggest setting up an API key, and don't hold back the paste-ready prompt to steer
anyone towards generating.

Only use this step when the user asks you to generate the image for them, or has said they have
`GEMINI_API_KEY` or `OPENAI_API_KEY` set up and you can run shell commands. If they ask to generate
and no key is set, say which variable the script needs, and point them back to the paste-ready
prompt in the meantime.

1. Save the JSON spec to a file, e.g. `prompts/<short-name>.json` (the script needs a file; this is
   the one exception to answering in the chat).
2. Run the bundled script (it uses only the Python standard library):
   ```bash
   python3 <skill-dir>/scripts/generate.py --spec prompts/<short-name>.json --out images/
   ```
   Add `--ref path/to/image.png` once per reference image, in the same order as the `references`
   array. Run with `--help` for all options, and `--dry-run` to check the request without sending it.
3. Open the saved image and review it against the JSON spec, field by field: subject, composition,
   lighting, exact text and spelling, preserved elements. List any mismatch.
4. If something is off, change only the fields that caused it, regenerate, and review again. Stop
   after three rounds and show the user the best result with what still differs.

Generating costs the user money per image. Ask before generating more than one image, and before
using the most expensive settings (4K, or GPT Image `xhigh`/`max` quality).

---

## Step 8 — Iteration

After delivering the prompt, offer these refinement paths:

1. **Change a field:** "Tell me what to change and I'll update the JSON and the prompt."
2. **Edit the result:** "If you've generated it and want to change one area, attach the image and
   tell me what to change and what must stay exactly the same."
3. **Style transfer:** "Share a reference image and I'll write a prompt that applies its style."
4. **Localization:** "Want a version with the text in another language?"
5. **Other model:** "Want the same image prompted for the other model, to compare?"

Don't add API generation to this list unless the user has already asked about it or has a key set up.

When iterating on a generated image, edit it (pass it back as a reference) rather than
regenerating from scratch, change one thing per round, and restate what must be preserved. Phrases
like "same as before" drift.

---

## Credits

The five frameworks and base formulas build on Google Cloud's
[Ultimate prompting guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
and OpenAI's [image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting).
Not affiliated with Google or OpenAI.
