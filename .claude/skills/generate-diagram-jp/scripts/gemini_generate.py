"""Minimal Gemini Imagen wrapper for diagram generation.

Usage:
    python gemini_generate.py --description-file desc.txt --output out.png
    python gemini_generate.py --description "..." --output out.png
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv


def resolve_api_key() -> str:
    """Resolve Gemini API key with fallback order."""
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print(
            "Error: Gemini API key not found.\n"
            "Set GEMINI_API_KEY or GOOGLE_API_KEY in .env file.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


STYLE_PREAMBLES = {
    "academic": (
        "You are an expert scientific diagram illustrator. "
        "Generate a high-quality academic methodology diagram with clean vector style. "
        "The structure (backgrounds, boxes, lines, text) must be strictly monochrome — "
        "white backgrounds, white box fills, thin dark grey borders. "
        "The ONLY color comes from icons and pictograms, which use soft pastel fills. "
        "Do not include figure titles in the image."
    ),
    "balanced": (
        "You are a graphic recording artist creating a visually rich, hand-drawn style "
        "information diagram with structured spatial composition. "
        "Generate a diagram with a warm, approachable hand-drawn aesthetic — "
        "lines are sketchy and organic, arrows are bold hand-drawn strokes, "
        "boxes have soft colorful fills (soft sky blue, soft peach, soft mint, "
        "soft lavender, soft warm yellow). Use 4-5 soft tone colors for visual rhythm. "
        "Use simple rounded-rectangle filled banners for phase headings — "
        "do NOT use ribbon shapes or ribbon banners. "
        "Include speech bubbles for annotations, marker-highlight style underlines "
        "for key terms, and hand-drawn circled numbers for steps. "
        "Icons are large pastel-filled pictograms with sketch feel. "
        "Do NOT include any characters, mascots, or human figures. "
        "Use only abstract pictogram icons (gears, folders, shields, stars, etc.). "
        "Maintain clean grid alignment and consistent box sizing despite the hand-drawn feel. "
        "Do not include figure titles in the image."
    ),
    "graphic-note": (
        "You are a graphic recording artist creating a visually rich, hand-drawn style "
        "information diagram. "
        "Generate a diagram with a warm, approachable hand-drawn aesthetic — "
        "lines are sketchy and organic, arrows are bold hand-drawn strokes, "
        "boxes have soft colorful fills (soft sky blue, soft peach, soft mint, "
        "soft lavender, soft warm yellow). Use 4-5 soft tone colors. "
        "Include hand-drawn ribbon banners for phase headings, "
        "speech bubbles for annotations, marker-highlight style underlines "
        "for key terms, and cute deformed character mascots where appropriate. "
        "Numbered steps may use hand-drawn circled numbers. "
        "Do not include figure titles in the image."
    ),
}


def build_prompt(description: str, style: str = "balanced") -> str:
    """Wrap description with style-specific visualizer instructions."""
    preamble = STYLE_PREAMBLES.get(style, STYLE_PREAMBLES["balanced"])
    return (
        f"{preamble}\n\n"
        "CRITICAL: All text labels, annotations, and captions in the diagram "
        "MUST be written in Japanese (日本語). Use clear, readable Japanese text "
        "for every label. Do not use English for any text in the image. "
        "If the description contains English terms, translate them to natural "
        "Japanese. Do not generate garbled or misspelled text.\n\n"
        f"{description}"
    )


def generate_image(prompt: str, api_key: str) -> "Image.Image":
    """Call Gemini Imagen API and return PIL Image."""
    from google import genai
    from google.genai import types
    from PIL import Image

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    )

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=config,
    )

    # Extract image from response (same logic as PaperBanana)
    parts = None
    if getattr(response, "candidates", None):
        parts = response.candidates[0].content.parts
    else:
        parts = getattr(response, "parts", None)

    if not parts:
        raise ValueError("Gemini image response had no content parts.")

    for part in parts:
        if hasattr(part, "as_image"):
            try:
                return part.as_image()
            except Exception:
                pass
        inline = getattr(part, "inline_data", None)
        if inline and getattr(inline, "data", None):
            data = inline.data
            image_bytes = base64.b64decode(data) if isinstance(data, str) else data
            return Image.open(BytesIO(image_bytes))

    raise ValueError("Gemini image response did not contain image data.")


def main():
    parser = argparse.ArgumentParser(description="Generate diagram via Gemini Imagen")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--description-file", type=str, help="Path to description text file")
    group.add_argument("--description", type=str, help="Description text (fallback)")
    parser.add_argument("--style", type=str, default="balanced",
                        choices=["academic", "balanced", "graphic-note"],
                        help="Style mode (default: balanced)")
    parser.add_argument("--output", type=str, required=True, help="Output PNG path")
    args = parser.parse_args()

    # Read description
    if args.description_file:
        desc_path = Path(args.description_file)
        if not desc_path.exists():
            print(f"Error: Description file not found: {desc_path}", file=sys.stderr)
            sys.exit(1)
        description = desc_path.read_text(encoding="utf-8")
    else:
        description = args.description

    if not description.strip():
        print("Error: Description is empty.", file=sys.stderr)
        sys.exit(1)

    # Resolve API key
    api_key = resolve_api_key()

    # Build prompt with style-specific visualizer instructions
    prompt = build_prompt(description, style=args.style)

    # Generate
    try:
        image = generate_image(prompt, api_key)
    except Exception as e:
        print(f"Error: Image generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(output_path), format="PNG")

    # Verify file size
    if output_path.stat().st_size == 0:
        print("Error: Generated image file is empty (0 bytes).", file=sys.stderr)
        sys.exit(1)

    # Success: print path to stdout
    print(str(output_path.resolve()))


if __name__ == "__main__":
    main()