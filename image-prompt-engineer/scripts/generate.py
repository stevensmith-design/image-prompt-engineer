#!/usr/bin/env python3
"""Generate or edit an image with Nano Banana (Gemini API) or GPT Image (OpenAI API).

Standard library only. Reads the API key from GEMINI_API_KEY or OPENAI_API_KEY.

Examples:
  python3 generate.py --spec prompts/hero.json --out images/
  python3 generate.py --spec prompts/hero.json --send json          # send the JSON itself as the prompt
  python3 generate.py --prompt "A red fox in snow" --model gpt-image-2.5-flare --aspect 3:2
  python3 generate.py --spec prompts/edit.json --ref images/hero.png --dry-run

Settings come from the spec's "output" block unless overridden by flags.
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
OPENAI_URL = "https://api.openai.com/v1/images"
DEFAULT_MODELS = {"gemini": "gemini-nano-banana-2.1", "openai": "gpt-image-2.5-sunburst"}
KEY_ENV = {"gemini": "GEMINI_API_KEY", "openai": "OPENAI_API_KEY"}

# Aspect ratio -> GPT Image size. Edges are multiples of 16 and the long edge is at most 3x the short.
OPENAI_SIZES = {
    "1:1": "1024x1024",
    "3:2": "1536x1024", "2:3": "1024x1536",
    "4:3": "1536x1152", "3:4": "1152x1536",
    "5:4": "1280x1024", "4:5": "1024x1280",
    "16:9": "2048x1152", "9:16": "1152x2048",
    "21:9": "2688x1152",
}

# Spec fields that are settings or derived output, not image content.
NON_CONTENT_FIELDS = {"output", "natural_language_prompt"}

TIMEOUT_SECONDS = 300


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def load_spec(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        spec = json.loads(text)
    except json.JSONDecodeError:
        return {"natural_language_prompt": text.strip()}
    if not isinstance(spec, dict):
        fail(f"{path} must contain a JSON object")
    return spec


def build_prompt(spec, send):
    if send == "json":
        content = {k: v for k, v in spec.items() if k not in NON_CONTENT_FIELDS}
        if not content:
            fail("--send json needs a spec with content fields")
        return json.dumps(content, indent=2, ensure_ascii=False)
    prompt = spec.get("natural_language_prompt")
    if not prompt:
        fail("the spec has no natural_language_prompt (use --send json to send the JSON instead)")
    return prompt


def pick_provider(model, provider):
    if provider:
        return provider
    if model:
        return "openai" if model.startswith(("gpt-", "dall-e")) else "gemini"
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return "gemini"


def read_image(path):
    data = Path(path).read_bytes()
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return data, mime


def short_b64(value):
    return value if len(value) <= 40 else f"{value[:20]}...<{len(value)} chars>"


def redact(obj):
    """Shorten base64 payloads so a dry run is readable."""
    if isinstance(obj, dict):
        return {k: short_b64(v) if k == "data" and isinstance(v, str) else redact(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


def post(url, headers, body):
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        fail(f"HTTP {err.code} from {url}\n{detail}")
    except urllib.error.URLError as err:
        fail(f"could not reach {url}: {err.reason}")


# --- Gemini -----------------------------------------------------------------

def gemini_request(args, prompt):
    if args.refs:
        parts = [{"type": "text", "text": prompt}]
        for path in args.refs:
            data, mime = read_image(path)
            parts.append({"type": "image", "mime_type": mime, "data": base64.b64encode(data).decode()})
        body = {"model": args.model, "input": parts}
    else:
        body = {"model": args.model, "input": prompt}

    response_format = {"type": "image", "mime_type": "image/jpeg"}
    if args.aspect:
        response_format["aspect_ratio"] = args.aspect
    if args.resolution:
        response_format["image_size"] = args.resolution.upper()
    body["response_format"] = response_format

    if args.thinking:
        body["generation_config"] = {"thinking_level": args.thinking}
    if args.search:
        body["tools"] = [{"type": "google_search"}]
    if args.previous_id:
        body["previous_interaction_id"] = args.previous_id
    return body


def find_images(obj, found):
    """Collect every inline image in the response, in order."""
    if isinstance(obj, dict):
        mime = obj.get("mime_type") or obj.get("mimeType") or ""
        if isinstance(obj.get("data"), str) and (obj.get("type") == "image" or mime.startswith("image/")):
            found.append((obj["data"], mime or "image/jpeg"))
        for value in obj.values():
            find_images(value, found)
    elif isinstance(obj, list):
        for value in obj:
            find_images(value, found)
    return found


def run_gemini(args, prompt, key):
    body = gemini_request(args, prompt)
    if args.dry_run:
        return {"endpoint": GEMINI_URL, "body": redact(body)}, []
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    response = post(GEMINI_URL, headers, json.dumps(body).encode())
    # output_image is the final render. Otherwise take the last image found, since interim
    # "thought" images come first.
    images = find_images(response.get("output_image"), []) or find_images(response, [])
    if not images:
        fail("no image in the response:\n" + json.dumps(redact(response), indent=2)[:2000])
    data, mime = images[-1]
    meta = {"interaction_id": response.get("id")}
    return meta, [(base64.b64decode(data), mime)]


# --- OpenAI -----------------------------------------------------------------

def openai_fields(args, prompt):
    fields = {"model": args.model, "prompt": prompt}
    size = args.size or OPENAI_SIZES.get(args.aspect or "", None)
    if args.aspect and not size:
        fail(f"no GPT Image size for aspect ratio {args.aspect}; pass --size WIDTHxHEIGHT")
    if size:
        fields["size"] = size
    if args.quality:
        fields["quality"] = args.quality
    if args.background:
        fields["background"] = args.background
    if args.n > 1:
        fields["n"] = str(args.n)
    return fields


def multipart(fields, files):
    boundary = uuid.uuid4().hex
    chunks = []
    for name, value in fields.items():
        chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    for name, path in files:
        data, mime = read_image(path)
        filename = Path(path).name
        chunks.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
            f"Content-Type: {mime}\r\n\r\n".encode() + data + b"\r\n"
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def run_openai(args, prompt, key):
    fields = openai_fields(args, prompt)
    if args.refs or args.mask:
        url = f"{OPENAI_URL}/edits"
        files = [("image[]", path) for path in args.refs]
        if args.mask:
            files.append(("mask", args.mask))
        if args.dry_run:
            return {"endpoint": url, "fields": fields, "files": files}, []
        body, content_type = multipart(fields, files)
    else:
        url = f"{OPENAI_URL}/generations"
        if "n" in fields:
            fields["n"] = int(fields["n"])
        if args.dry_run:
            return {"endpoint": url, "body": fields}, []
        body, content_type = json.dumps(fields).encode(), "application/json"

    headers = {"Authorization": f"Bearer {key}", "Content-Type": content_type}
    response = post(url, headers, body)
    images = [(base64.b64decode(item["b64_json"]), "image/png") for item in response.get("data", []) if item.get("b64_json")]
    if not images:
        fail("no image in the response:\n" + json.dumps(response, indent=2)[:2000])
    return {"usage": response.get("usage")}, images


# --- Main -------------------------------------------------------------------

def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] or "image"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--spec", help="JSON spec file (or a plain-text prompt file)")
    source.add_argument("--prompt", help="prompt text")
    parser.add_argument("--send", choices=["prose", "json"], default="prose",
                        help="send the natural_language_prompt (default) or the JSON content fields")
    parser.add_argument("--provider", choices=["gemini", "openai"], help="inferred from the model if omitted")
    parser.add_argument("--model", help="model ID, e.g. gemini-nano-banana-2.1 or gpt-image-2.5-sunburst")
    parser.add_argument("--aspect", help="aspect ratio, e.g. 16:9")
    parser.add_argument("--resolution", help="Gemini only: 1K, 2K or 4K")
    parser.add_argument("--size", help="OpenAI only: WIDTHxHEIGHT or auto (overrides --aspect)")
    parser.add_argument("--quality", help="OpenAI only: auto, low, medium, high, xhigh, max")
    parser.add_argument("--background", help="OpenAI only: auto, opaque or transparent")
    parser.add_argument("--n", type=int, default=1, help="OpenAI only: number of images")
    parser.add_argument("--thinking", help="Gemini only: minimal, medium or high")
    parser.add_argument("--search", action="store_true", help="Gemini only: enable Google Search grounding")
    parser.add_argument("--previous-id", help="Gemini only: interaction ID to continue editing from")
    parser.add_argument("--ref", dest="refs", action="append", default=[],
                        help="reference or input image; repeat in the order of the spec's references")
    parser.add_argument("--mask", help="OpenAI only: PNG mask with an alpha channel for a local edit")
    parser.add_argument("--out", default="images", help="output directory (default: images)")
    parser.add_argument("--dry-run", action="store_true", help="print the request without sending it")
    args = parser.parse_args()

    spec = load_spec(args.spec) if args.spec else {"natural_language_prompt": args.prompt}
    prompt = build_prompt(spec, args.send)
    output = spec.get("output", {}) if isinstance(spec.get("output"), dict) else {}

    args.model = args.model or output.get("model")
    args.provider = pick_provider(args.model, args.provider)
    args.model = args.model or DEFAULT_MODELS[args.provider]
    args.aspect = args.aspect or output.get("aspect_ratio")
    if args.provider == "gemini":
        args.resolution = args.resolution or output.get("resolution")
    else:
        args.size = args.size or output.get("size")
        args.quality = args.quality or output.get("quality")
        args.background = args.background or output.get("background")

    for path in args.refs + ([args.mask] if args.mask else []):
        if not Path(path).is_file():
            fail(f"image not found: {path}")

    key = os.environ.get(KEY_ENV[args.provider], "")
    if not key and not args.dry_run:
        fail(f"set {KEY_ENV[args.provider]} to generate with {args.model}")

    runner = run_gemini if args.provider == "gemini" else run_openai
    meta, images = runner(args, prompt, key)

    if args.dry_run:
        print(json.dumps(meta, indent=2, ensure_ascii=False))
        return

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{slugify(Path(args.spec).stem if args.spec else prompt)}-{time.strftime('%Y%m%d-%H%M%S')}"
    saved = []
    for index, (data, mime) in enumerate(images, start=1):
        ext = mimetypes.guess_extension(mime) or ".png"
        ext = ".jpg" if ext in (".jpe", ".jpeg") else ext
        suffix = f"-{index}" if len(images) > 1 else ""
        path = out_dir / f"{stem}{suffix}{ext}"
        path.write_bytes(data)
        saved.append(str(path))

    # Sidecar record so any image can be traced back to its exact prompt and settings.
    record = {
        "provider": args.provider,
        "model": args.model,
        "prompt": prompt,
        "settings": {k: getattr(args, k) for k in ("aspect", "resolution", "size", "quality", "background", "thinking")
                     if getattr(args, k, None)},
        "references": args.refs,
        "images": saved,
        **{k: v for k, v in meta.items() if v},
    }
    (out_dir / f"{stem}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    for path in saved:
        print(path)
    if meta.get("interaction_id"):
        print(f"interaction_id: {meta['interaction_id']} (pass with --previous-id to keep editing)")


if __name__ == "__main__":
    main()
