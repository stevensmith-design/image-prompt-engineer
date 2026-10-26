# Worked Examples

Eight examples across the five frameworks and both model families. Each shows the JSON spec and
the assembled prompt. Read the one closest to the user's request when you need a model answer.

These are the full internal specs. What the user pastes is the combined prompt from Step 6 of
SKILL.md: the `natural_language_prompt` on top, then the JSON without `output` and
`natural_language_prompt`.

---

## 1. Text-to-Image — Fashion Editorial (Nano Banana)

```json
{
  "operation": "generate",
  "framework": "text-to-image",
  "subject": "A striking fashion model wearing a tailored brown dress, sleek boots and a structured handbag",
  "action": "Posing with a confident, statuesque stance, slightly turned",
  "location_context": "Seamless deep cherry red studio backdrop",
  "composition": "Medium-full shot, center-framed",
  "style": {
    "genre": "fashion magazine editorial",
    "medium": "medium-format analog film",
    "film_stock": "pronounced grain",
    "color_grading": "high saturation"
  },
  "lighting": "Cinematic hard key light with soft fill",
  "output": {
    "model": "gemini-nano-banana-2.1",
    "aspect_ratio": "4:5",
    "resolution": "2K"
  },
  "natural_language_prompt": "A striking fashion model wearing a tailored brown dress, sleek boots and holding a structured handbag, posing with a confident, statuesque stance, slightly turned. A seamless, deep cherry red studio backdrop. Medium-full shot, center-framed. Fashion magazine editorial, shot on medium-format analog film with pronounced grain, high saturation, cinematic hard key light with soft fill."
}
```

Paste into Google AI Studio with Nano Banana 2.1, aspect ratio 4:5, resolution 2K.

---

## 2. Creative Director — Atmospheric Landscape (Nano Banana Pro)

```json
{
  "operation": "generate",
  "framework": ["text-to-image", "creative-director"],
  "subject": "An abandoned Japanese train station platform",
  "action": "Empty, overgrown with moss and wildflowers forcing through cracks in the concrete",
  "location_context": "Dense cedar forest visible through the open sides of the platform",
  "composition": "Wide establishing shot, low angle looking down the length of the platform",
  "style": {
    "genre": "fine art photography",
    "medium": "35mm film",
    "film_stock": "Kodak Portra 400, warm and slightly faded",
    "color_grading": "muted greens and warm yellows"
  },
  "camera": {
    "hardware": "Nikon F3",
    "lens": "24mm wide-angle",
    "angle": "low angle",
    "aperture": "f/5.6",
    "focus": "deep focus"
  },
  "lighting": "Overcast diffused daylight filtering through the forest canopy",
  "output": {
    "model": "gemini-3-pro-image",
    "aspect_ratio": "21:9",
    "resolution": "4K"
  },
  "natural_language_prompt": "An abandoned Japanese train station platform, empty and overgrown with moss and wildflowers forcing through cracks in the concrete. Dense cedar forest is visible through the open sides of the platform. Wide establishing shot from a low angle looking down the length of the platform. Shot on a Nikon F3 with a 24mm wide-angle lens at f/5.6, deep focus. Overcast diffused daylight filtering through the forest canopy. Kodak Portra 400, warm and slightly faded, muted greens and warm yellows. Fine art photography."
}
```

---

## 3. Multimodal — Product in a New Environment (GPT Image)

```json
{
  "operation": "generate",
  "framework": "multimodal",
  "references": [
    {"image": 1, "role": "product", "description": "Matte black stainless steel water bottle"},
    {"image": 2, "role": "background", "description": "Misty alpine meadow at sunrise"}
  ],
  "subject": "The matte black water bottle from Image 1",
  "action": "Resting naturally on a granite boulder",
  "location_context": "The misty alpine meadow from Image 2",
  "composition": "Low angle close shot, mountain range softly blurred behind",
  "style": {
    "genre": "photorealistic outdoor lifestyle product photography",
    "color_grading": "cool morning tones"
  },
  "lighting": "Low sunrise backlight with a slight lens flare",
  "preserve": ["The bottle's exact shape, finish and logo from Image 1"],
  "output": {
    "model": "gpt-image-2.5-sunburst",
    "aspect_ratio": "3:2",
    "size": "1536x1024",
    "quality": "high"
  },
  "natural_language_prompt": "A photorealistic outdoor lifestyle product photo. Image 1 is the product: a matte black stainless steel water bottle. Image 2 is the background: a misty alpine meadow at sunrise. Place the bottle from Image 1 resting naturally on a granite boulder in the meadow from Image 2. Low angle close shot, with the mountain range softly blurred behind. Low sunrise backlight with a slight lens flare, cool morning tones. Keep the bottle's exact shape, finish and logo from Image 1 unchanged. No added text or watermarks."
}
```

Send through the edits endpoint with both images attached, in order. In ChatGPT, attach both
images and add "Landscape, 3:2." at the end.

---

## 4. Multimodal — Character Consistency for a Storyboard (Nano Banana)

```json
{
  "operation": "generate",
  "framework": "multimodal",
  "references": [
    {"image": 1, "role": "character", "description": "A red-haired woman in a trench coat"}
  ],
  "subject": "The red-haired woman in the trench coat from Image 1",
  "action": "Walking purposefully through a crowded night market",
  "location_context": "Tokyo alley night market, neon signs, steam rising from food stalls",
  "composition": "Medium shot from behind, slightly to the left, tracking her movement",
  "style": {
    "genre": "cinematic thriller film still",
    "color_grading": "deep shadows, neon cyan and magenta highlights"
  },
  "preserve": ["Her exact face, hair colour and trench coat from Image 1"],
  "output": {
    "model": "gemini-nano-banana-2.1",
    "aspect_ratio": "16:9",
    "resolution": "2K"
  },
  "natural_language_prompt": "Using Image 1 as the character reference, keep the exact face, red hair and trench coat of the woman. She is walking purposefully through a crowded Tokyo alley night market, neon signs overhead and steam rising from food stalls. Medium shot from behind and slightly to the left, tracking her movement. Cinematic thriller film still, deep shadows, neon cyan and magenta highlights."
}
```

For the next storyboard frame, keep the same reference and `style`, and change only `action`,
`location_context` and `composition`.

---

## 5. Web-Search-Powered — Live Weather (Nano Banana)

```json
{
  "operation": "generate",
  "framework": "web-search",
  "web_search": {
    "query": "Current weather and time of day in Shibuya, Tokyo",
    "visualization_instruction": "Sunny daytime: warm golden light and dense crowds. Rain: grey sky, wet reflective streets and umbrellas. Night: neon reflected on wet pavement."
  },
  "subject": "Shibuya Crossing",
  "composition": "Elevated wide shot from above the pedestrian crossing",
  "style": {
    "genre": "cinematic urban photography",
    "medium": "high-resolution digital"
  },
  "output": {
    "model": "gemini-nano-banana-2.1",
    "aspect_ratio": "16:9",
    "resolution": "2K"
  },
  "natural_language_prompt": "Search for the current weather and time of day in Shibuya, Tokyo. Use this data to set the lighting and atmosphere: if it is sunny and daytime, warm golden light and dense crowds; if it is raining, a grey sky, wet reflective streets and people with umbrellas; if it is night, neon lights reflected on wet pavement. Render Shibuya Crossing as an elevated wide shot from above the pedestrian crossing. Cinematic urban photography, high-resolution digital."
}
```

For GPT Image: look the weather up first, then replace the search instruction with the facts
("A rainy evening in Shibuya...").

---

## 6. Text Rendering + Localization — Beauty Promo (Nano Banana Pro)

```json
{
  "operation": "generate",
  "framework": ["text-to-image", "text-rendering"],
  "subject": "A sleek, minimalist nude-coloured face moisturiser jar",
  "location_context": "Warm beige studio background",
  "composition": "Glossy commercial beauty shot, product centered with text to its right",
  "style": {
    "genre": "high-end beauty product photography",
    "color_grading": "soft and radiant"
  },
  "lighting": "Soft radiant studio lighting",
  "text_elements": [
    {"content": "GLOW", "style": "flowing, elegant brush script", "placement": "top line"},
    {"content": "10% OFF", "style": "heavy, blocky condensed sans-serif", "placement": "middle line"},
    {"content": "Your First Order", "style": "thin, minimalist geometric sans-serif", "placement": "bottom line"}
  ],
  "localization": {"source_language": "English", "target_languages": ["Japanese"]},
  "output": {
    "model": "gemini-3-pro-image",
    "aspect_ratio": "4:5",
    "resolution": "2K"
  },
  "natural_language_prompt": "A high-end, glossy commercial beauty shot of a sleek, minimalist nude-coloured face moisturiser jar on a warm beige studio background, soft radiant lighting. To the right of the product, render three lines of text: top line \"GLOW\" in a flowing, elegant brush script; middle line \"10% OFF\" in a heavy, blocky condensed sans-serif; bottom line \"Your First Order\" in a thin, minimalist geometric sans-serif. No other text. Then render the same design with all text translated into Japanese."
}
```

---

## 7. Text Rendering — Transparent Logo Sticker (GPT Image)

```json
{
  "operation": "generate",
  "framework": ["text-to-image", "text-rendering"],
  "subject": "A circular sticker badge for a specialty coffee roaster",
  "composition": "Single centered badge, flat front view, generous padding around the edge",
  "style": {
    "genre": "flat vector-style illustration",
    "color_grading": "two colours: deep forest green and cream"
  },
  "materiality": ["A simple line drawing of a coffee bean with a small leaf in the center of the badge"],
  "text_elements": [
    {"content": "SLOW POUR", "style": "bold rounded sans-serif, curved along the top edge", "placement": "top arc"},
    {"content": "ROASTERS · EST. 2026", "style": "small spaced-out capitals, curved along the bottom edge", "placement": "bottom arc"}
  ],
  "output": {
    "model": "gpt-image-2.5-sunburst",
    "aspect_ratio": "1:1",
    "size": "1024x1024",
    "quality": "high",
    "background": "transparent"
  },
  "natural_language_prompt": "A circular sticker badge for a specialty coffee roaster, in a flat vector-style illustration.\nSubject: a simple line drawing of a coffee bean with a small leaf in the center of the badge.\nText: \"SLOW POUR\" in a bold rounded sans-serif curved along the top edge; \"ROASTERS · EST. 2026\" in small spaced-out capitals curved along the bottom edge. No other text.\nColours: deep forest green and cream only.\nComposition: a single centered badge, flat front view, generous padding around the edge, nothing outside the badge."
}
```

Uses GPT Image's labelled-section style. Set `background: transparent` with PNG output. In ChatGPT,
add "Transparent background." at the end.

---

## 8. Edit — Change One Thing, Preserve the Rest (GPT Image)

```json
{
  "operation": "edit",
  "framework": "multimodal",
  "references": [
    {"image": 1, "role": "subject", "description": "The user's generated photo of a living room with a grey sofa"}
  ],
  "subject": "The living room in Image 1",
  "action": "Replace the grey sofa with a deep green velvet sofa of the same size and position",
  "preserve": [
    "Camera angle and framing",
    "Lighting and shadows",
    "Every other object, including the rug, plants and artwork"
  ],
  "output": {
    "model": "gpt-image-2.5-sunburst",
    "aspect_ratio": "3:2",
    "size": "1536x1024"
  },
  "natural_language_prompt": "Edit Image 1. Replace the grey sofa with a deep green velvet sofa of the same size, in the same position. Keep everything else exactly the same: the camera angle and framing, the lighting and shadows, and every other object, including the rug, plants and artwork. Do not add any text, logos or watermarks."
}
```
