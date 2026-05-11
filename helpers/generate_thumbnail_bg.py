"""Generate an editorial thumbnail base image via Gemini "nano-banana".

Reusable across videos. Takes a subject reference photo + topic/prop/backdrop
parameters and produces a stylized 9:16 portrait base image — clean photographic
output, no text. Text overlay is added afterwards in HyperFrames.

Usage:
    uv run python helpers/generate_thumbnail_bg.py \
        --reference /path/to/subject.png \
        --out      /path/to/edit/animations/slot_thumbnail/bg_generated.png \
        --topic    "advice for first-time entrepreneurs" \
        --prop     "a small notebook"

Environment:
    GEMINI_API_KEY      required (read from .env in the project root if not in env)
    GEMINI_IMAGE_MODEL  optional override (default: gemini-2.5-flash-image-preview)

Design notes:
    - Prompt template encodes the editorial aesthetic from
      prompts/thumbnail-benchmarks/ (Kinfolk / The Gentlewoman tone).
    - Every parameter is overridable via flags so this helper works for any
      creator, any topic, any palette.
    - Never prints the API key. Never writes it to disk.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-2.5-flash-image"

PROMPT_TEMPLATE = """High-impact editorial thumbnail, portrait orientation 9:16 aspect ratio ({aspect_px}). The image must make a scrolling viewer STOP and click — magnetic and present, but with quiet confidence. Not a corporate headshot, not a fashion-flashy moment either.

Subject: the person in the reference photo. Preserve their face, features, hair color and texture, complexion, and identity exactly. Expression should feel real and present — depending on what the gesture suggests, this can be a soft knowing smile, a subtle smirk, an open mid-explanation look, a contemplative gaze, or a genuine laugh. Eyes always engaged with the camera (or pointedly off-camera mid-thought when the chosen pose calls for it). NEVER a polite stock-photo grin.

Framing: tight close-up to medium-close-up. Head and shoulders dominate ~60–75% of the frame. The face is the hero — eyes near the upper third. NOT a full-body shot. NOT a distant studio portrait.

Outfit: {outfit}. SF/YC founder aesthetic — quiet confidence, dressed intentionally but without signaling effort. Minimal layering (one layer, max two). Neutral / tonal palette (cream, oatmeal, sand, taupe, olive, charcoal, navy, black). Relaxed silhouette, natural fabrics (cotton, linen, merino, raw denim). No logos, no graphic prints, no shiny fabrics, no patterns. Outfit tone should contrast subtly with the backdrop — warm bg pairs with charcoal/navy/olive; cool bg pairs with cream/oatmeal/sand.

Pose / gesture: pick ONE that fits the topic energy. {gesture}. Whichever you choose, the body should feel candid mid-motion — leaning slightly, weight off one foot, mid-thought, mid-explanation — never frozen-and-posed. The viewer should feel addressed, not observed. **Avoid repeating the same gesture across videos for the same creator** — if a previous thumbnail used "hand reaching for camera," pick a different one this time.

Background: {backdrop}. Slight directional lighting from one side, gentle vignette toward the edges, NOT flat studio fluorescent. Subtle texture (matte plaster, soft seamless paper, warm-painted concrete, raw concrete, lived-in interior wall) — no patterns, no text, no logos. NO {banned_colors}, NO neon, NO oversaturation.

Composition: subject centered or slightly off-center, leaving the lower 30–40% of the frame open for a large typographic text overlay to be added later. A hand or prop can extend into that lower zone — overlap is good, it makes the text feel integrated with the photo.

Energy: editorial portrait meets caught-in-thought candid. Style references: {style_refs}. Topic of the underlying video: {topic}. Subtle film grain, sharp focus on the eyes, cinematic warmth. Feels like a magazine portrait of a thoughtful founder, NOT a LinkedIn profile photo and NOT a fashion editorial.

Do not add any text, captions, watermarks, logos, or graphic elements. Output a clean photographic image only."""

# Default gesture pool — varied so the same creator across multiple videos doesn't
# look like a duplicate. The model picks one that fits the topic. Override per-call
# with --gesture to force a specific pose.
DEFAULT_GESTURE_MENU = (
    "Pick whichever ONE of these gestures best fits the topic energy: "
    "(a) one hand to chin or jaw, head slightly tilted, mid-thought; "
    "(b) leaning forward with elbows resting on a surface, hands loosely clasped, smirk; "
    "(c) running one hand through hair mid-laugh, eyes squinting with real warmth; "
    "(d) open hand turned upward mid-explanation, as if delivering the punchline; "
    "(e) arms loosely crossed, slight knowing smirk, head tilted; "
    "(f) one finger pressed to lips like sharing a quiet observation; "
    "(g) looking just past the camera as if recalling something, slight smile; "
    "(h) hand at temple, eyes focused, caught mid-realisation; "
    "(i) palm extended toward the camera as if politely interrupting, eye contact; "
    "(j) holding a plain ceramic mug or a notebook loosely, attention on camera not the prop. "
    "Do NOT default to a wide-open palm pushing toward the camera unless it genuinely fits the topic."
)


def load_env() -> str:
    """Load .env from the project root and return GEMINI_API_KEY."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit(f"GEMINI_API_KEY not set in environment or {env_path}")
    return api_key


def build_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    return PROMPT_TEMPLATE.format(
        aspect_px=args.aspect_px,
        topic=args.topic,
        gesture=args.gesture,
        backdrop=args.backdrop,
        outfit=args.outfit,
        style_refs=args.style_refs,
        banned_colors=args.banned_colors,
    )


def generate(api_key: str, model: str, prompt: str, reference: Path, out: Path) -> None:
    ref_image = Image.open(reference)
    print(f"reference: {reference.name} ({ref_image.size[0]}x{ref_image.size[1]})")
    print(f"model:     {model}")
    print(f"out:       {out}")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=[prompt, ref_image],
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    saved = False
    for part in response.parts:
        if part.text is not None:
            print(f"[model text] {part.text[:240]}")
        elif part.inline_data is not None:
            part.as_image().save(out)
            with Image.open(out) as saved_img:
                print(f"saved: {out} ({saved_img.size[0]}x{saved_img.size[1]})")
            saved = True
            break

    if not saved:
        sys.exit("model returned no inline image data (refusal, safety filter, or wrong model id)")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate a thumbnail base image via Gemini nano-banana from a subject reference photo."
    )
    p.add_argument("--reference", required=True, type=Path, help="Path to the subject reference photo (PNG/JPG).")
    p.add_argument("--out", required=True, type=Path, help="Output path for the generated PNG.")
    p.add_argument("--topic", default="", help="One-line description of the video's topic — shapes prop/backdrop suggestions.")
    p.add_argument(
        "--gesture",
        default=DEFAULT_GESTURE_MENU,
        help=(
            "What the subject is doing with their hands/body/eyes. Default is a menu of 10 gestures "
            "the model picks from based on topic — guarantees variety across videos for the same creator. "
            "Override with a single specific gesture (e.g. \"hand at chin, head tilted, mid-thought\") to "
            "force a particular pose."
        ),
    )
    p.add_argument(
        "--backdrop",
        default="solid tonal backdrop in a warm neutral — warm taupe, soft sand, oatmeal, dusty clay, or muted olive. Matte texture, subtle directional light, gentle vignette toward the edges. Lived-in feel, not flat studio paper.",
        help="Backdrop palette / material.",
    )
    p.add_argument(
        "--outfit",
        default=(
            "minimal modern essentials in a neutral / tonal palette — plain crew-neck tee, lightweight "
            "half-zip knit, oversized cotton button-up worn open over a tee, relaxed chore coat, or a "
            "well-fitted plain sweatshirt. Colors: cream, oatmeal, sand, olive, charcoal, navy, or black. "
            "Natural fabrics, relaxed silhouette, no logos, no graphic prints, no shiny fabrics, no patterns. "
            "Quiet confidence — dressed intentionally but without signaling effort. SF / YC founder aesthetic."
        ),
        help="Outfit description. Modern minimal beats fashion-flashy and corporate-formal both.",
    )
    p.add_argument(
        "--style-refs",
        default=(
            "editorial portraits in the spirit of Cereal magazine, Monocle, A24 press shoots, and SF/YC founder "
            "press portraits — quiet, considered, present. NOT fashion editorial flash, NOT LinkedIn corporate."
        ),
        help="Magazine / photographer references that set the tone.",
    )
    p.add_argument(
        "--banned-colors",
        default="blues, electric/saturated colors",
        help="Colors to explicitly avoid in the output.",
    )
    p.add_argument("--aspect-px", default="1080x1920", help="Target pixel dimensions (used inside the prompt only).")
    p.add_argument(
        "--prompt-file",
        type=Path,
        default=None,
        help="If provided, use this file's contents as the prompt verbatim (ignores other prompt flags).",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_MODEL),
        help=f"Gemini image model id (default from $GEMINI_IMAGE_MODEL or {DEFAULT_MODEL}).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    api_key = load_env()
    prompt = build_prompt(args)
    generate(api_key, args.model, prompt, args.reference.resolve(), args.out.resolve())


if __name__ == "__main__":
    main()
