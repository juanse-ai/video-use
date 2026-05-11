# Generate the editorial base image for a video thumbnail (Gemini nano-banana)

Reusable prompt — covers the AI-base step only. Once `bg_generated.png` exists, hand off to `prompts/generate-thumbnail.md` for typography + composite.

## The aesthetic target

The base image must **stop the scroll** without being a fashion-flash or a corporate headshot. Aim for **quiet confidence** — the SF / YC founder portrait register: dressed intentionally but without signaling effort, present and considered, photographed for a thoughtful magazine portrait.

Benchmarks live in `/Users/juanse/Developer/video-use/thumbnails/benchmark/`:
- `o8mrneEH...avif` — Claude "MANAGED AGENTS" thumbnail. Tight close-up, dynamic hand gesture, big genuine smile, warm tonal backdrop, contrast-rich outfit, italic-serif label + big bold-caps title.
- `oQQGvfQ2...jpeg` — editorial portrait in a single-color staged set, integrated prop, no text.
- `oMwAhiqh...jpeg` — sharp tonal backdrop with prop extended toward camera, mixed sans-bold + italic-serif typography.

**Defining traits to chase every time:**

- **Tight close-up to medium-close-up** — head and shoulders fill ~60–75% of the frame. Face is the hero, eyes near the upper third. Never full-body, never corporate distance.
- **Quiet-confidence pose** — caught mid-thought, mid-explanation, mid-laugh — never frozen-and-posed. The subject should feel present, not staged.
- **Real expression matched to the gesture** — soft knowing smile, subtle smirk, open mid-explanation look, contemplative gaze, OR a genuine laugh when the topic calls for it. Eyes engaged with the camera, OR pointedly off-camera mid-thought when the pose supports it. **Never** a polite closed-mouth stock-photo grin.
- **Modern minimal outfit (SF / YC founder aesthetic)** — quiet confidence, dressed intentionally without signaling effort. One layer (max two). Neutral / tonal palette: cream, oatmeal, sand, olive, charcoal, navy, black. Natural fabrics: cotton crew-neck tee, lightweight half-zip knit, oversized cotton button-up, relaxed chore coat, well-fitted plain sweatshirt, raw denim. **NO logos, NO graphic prints, NO shiny fabrics, NO patterns.** Outfit tone should contrast subtly with the backdrop.
- **Warm tonal backdrop** — taupe, sand, oatmeal, dusty clay, muted olive, warm taupe. Slight directional lighting + gentle vignette toward the edges. Lived-in feel, NOT flat studio paper, NOT fluorescent.
- **Composition with room for text** — subject centered or slightly off-center, leaving the lower 30–40% of the frame open. A hand or prop can extend into the text zone — overlap makes the text feel integrated.

**Variety rule (critical):**
**Do NOT make every thumbnail look the same.** The helper's default gesture is a MENU of ~10 different poses — the model picks one that fits the topic. When generating a thumbnail for a creator who already has previous thumbnails, look at what gesture was used last (`videos/<creator>/<prior-video>/edit/thumbnail.jpg` or the prior `bg_generated.png`) and explicitly pick a DIFFERENT one this time via `--gesture "..."`. Same creator + same gesture twice in a row = recognizable repetition = feed fatigue. Vary the gesture, vary the expression, optionally vary the backdrop tone within the warm-tonal range.

**Things NOT to do** (encoded in the helper defaults — these are hard-learned lessons):
- ❌ Hand on hip, formal pose. Reads as a corporate LinkedIn portrait.
- ❌ Full-body shot. The face is the parasocial pull — show it big.
- ❌ Fitted formal dress, suit, or blazer-over-button-down. Corporate signal.
- ❌ Leather jacket on every video. That's a fashion-flashy signal, not quiet confidence — use only when the brand truly calls for it.
- ❌ Polite closed-mouth smile. Doesn't register at scroll speed.
- ❌ Same hand-reaching-for-camera gesture twice for the same creator.
- ❌ A held phone, a microphone, a ring light, a laptop. Generic studio props kill the editorial feel. If a prop is used, it should be tactile and analog (plain ceramic mug, hardcover notebook, single sheet of paper).
- ❌ Logos, branded clothing, graphic tees, shiny fabrics, busy patterns.
- ❌ Crowded scenes (cafés, streets, offices). Solid tonal backdrop only.
- ❌ Watermarks, captions, brand chrome in the AI output. Text is the HyperFrames step's job.

## Inputs

### Required
- **Subject reference photo.** Located in `/Users/juanse/Developer/video-use/thumbnails/base-photos/<creator-slug>/`. Convention: each speaker gets one subdirectory, kebab-case, containing one or more isolated portrait photos against a clean background. Examples:
  - `/Users/juanse/Developer/video-use/thumbnails/base-photos/natalia-serrano/Natalia-Serrano.png`
  - `/Users/juanse/Developer/video-use/thumbnails/base-photos/<other-creator>/<Name>.png`

  When a new video drops for a creator with no base-photos directory yet, ask the user for an isolated high-resolution portrait (≥ 800px on the shorter side, clean background, neutral expression) and save it there before running the helper. Likeness preservation in nano-banana depends on the reference being clean and well-lit.

- **Output path.** Convention: `{{edit_dir}}/animations/slot_thumbnail/bg_generated.png`.

### Optional (sensible defaults — override per video)
The helper's defaults are tuned for the SF / YC quiet-confidence aesthetic. Flags override per-call when the topic or brand calls for something different.

- **`--topic`** — one line on what the video is about. Shapes the gesture choice and the overall energy implicitly.
- **`--gesture`** — what the subject is doing with their hands/body/eyes. **Default is a menu of ~10 distinct gestures** (hand at chin, leaning forward elbows-down, running hand through hair mid-laugh, open hand mid-explanation, arms loosely crossed with smirk, finger to lips, looking off-camera recalling, hand at temple mid-realisation, palm-out polite interruption, holding a plain mug/notebook). The model picks one that fits the topic. Override with a single explicit gesture (e.g. `--gesture "hand at chin, head tilted, looking just past the camera mid-thought"`) to force a specific pose, especially when avoiding repetition vs the creator's prior thumbnails.
- **`--backdrop`** — tonal backdrop. Default: `"solid tonal backdrop in a warm neutral — warm taupe, soft sand, oatmeal, dusty clay, or muted olive. Matte texture, subtle directional light, gentle vignette toward the edges. Lived-in feel, not flat studio paper."` Override per brand or to break up a series visually.
- **`--outfit`** — outfit description. Default: `"minimal modern essentials in a neutral / tonal palette — plain crew-neck tee, lightweight half-zip knit, oversized cotton button-up worn open over a tee, relaxed chore coat, or a well-fitted plain sweatshirt. Colors: cream, oatmeal, sand, olive, charcoal, navy, or black. Natural fabrics, relaxed silhouette, no logos, no graphic prints, no shiny fabrics, no patterns. Quiet confidence — dressed intentionally but without signaling effort. SF / YC founder aesthetic."`
- **`--style-refs`** — magazine/aesthetic references. Default: `"editorial portraits in the spirit of Cereal magazine, Monocle, A24 press shoots, and SF/YC founder press portraits — quiet, considered, present. NOT fashion editorial flash, NOT LinkedIn corporate."`
- **`--banned-colors`** — colors to forbid. Default: `"blues, electric/saturated colors"`. Override per brand palette.
- **`--prompt-file`** — fully override the prompt from a file (escape hatch for when none of the flags fit).
- **`--model`** — Gemini image model id. Default: `gemini-2.5-flash-image` (the canonical nano-banana — note: NOT `-preview`, that returns 404). Override via `--model` or `GEMINI_IMAGE_MODEL` env var when a newer preview is available (`gemini-3.1-flash-image-preview`, `nano-banana-pro-preview` are alternatives on the current Gemini API).

The full prompt template lives inside the helper script (`helpers/generate_thumbnail_bg.py`). Flags become tokens, no separate template file to maintain.

## Deliver

1. Verify the subject reference exists at `thumbnails/base-photos/<creator-slug>/<Name>.png`. If missing, ask the user for a high-resolution isolated portrait and save it there. **Do not** use a frame extracted from the video as the reference — those have ambient lighting and the wrong framing, the AI base will inherit both.
2. Verify `GEMINI_API_KEY` is in `/Users/juanse/Developer/video-use/.env`. **Do not `cat` the .env**; the helper loads it via `python-dotenv`. If missing, ask the user to add it.
3. Run the helper from the project root:

   ```bash
   cd /Users/juanse/Developer/video-use
   uv run python helpers/generate_thumbnail_bg.py \
     --reference "thumbnails/base-photos/<creator-slug>/<Name>.png" \
     --out      "videos/<creator>/<video>/edit/animations/slot_thumbnail/bg_generated.png" \
     --topic    "<one-line topic>"
   ```

   In Claude Code, the agent may be blocked by the auto-mode classifier for credential-touching scripts. Either re-run the command yourself (whitelisted) or ask the user to run via `! <command>` in chat.

4. Inspect the output (`bg_generated.png`):
   - Subject likeness preserved (face recognizable as the reference person).
   - Tight close-up — head + shoulders dominate, not a full-body shot.
   - Hand reaching for the camera OR equivalent dynamic gesture. If the AI generated a static hand-on-hip pose, re-run with a sharper gesture instruction in `--prop` (e.g. `--prop "palm extended toward the camera, almost touching the lens"`).
   - Big genuine smile/laugh — eyes engaged. If the AI produced a closed-mouth polite smile, retry with `"caught mid-laugh, mouth open, real candid energy"` appended to `--outfit` or via `--prompt-file`.
   - Backdrop is one solid tonal color. If the AI produced a busy location, retry with `"absolutely plain backdrop, no furniture, no plants, no architecture, no windows"`.
   - Lower 30–40% has room for text. If the subject fills the entire frame, retry asking for `"subject centered with lower third open for text"`.
   - No text/logos in the output. Retry if any leaked in.

5. If the model returns no inline data (refusal, safety filter, wrong model id):
   - Confirm the model id is current: `gemini-2.5-flash-image`, `gemini-3.1-flash-image-preview`, or `nano-banana-pro-preview` are the working ids as of the last verified session.
   - Soften "preserve her face exactly" to "in the style of the woman in the reference" if safety triggers fire.
   - Check the reference isn't being filtered for celebrity-likeness reasons.

## Iteration vocabulary

- *"too corporate"* → check the helper defaults are loaded; drop any flag overrides that pushed the outfit toward formal (`--outfit "navy dress"`).
- *"too fashion-flashy"* / *"looks like a magazine cover not a founder"* → drop `--outfit "leather jacket"`-style overrides; let the default SF/YC minimal kick back in.
- *"different backdrop, sage green"* → `--backdrop "matte sage green plaster wall, slight texture, soft directional light"`.
- *"more dramatic lighting"* → append `"strong key light from camera-right, soft fall-off on the opposite side, cinematic warmth"` via `--outfit` or `--prompt-file`.
- *"different gesture"* / *"don't repeat the last one"* → override `--gesture` with a single explicit pose. Phrases that work: `"hand at chin, head tilted, looking just past the camera mid-thought"`, `"both hands raised palms-up in mock surrender, head tilted, smirk"`, `"finger to lips like sharing a quiet observation"`, `"leaning forward, elbows on a surface, hands clasped, knowing smile"`, `"holding a plain ceramic mug loosely, attention on the camera not the mug"`.
- *"smaller in the frame, more room for text"* → append to `--gesture` something like `"sitting back from the camera slightly, head and chest fill the upper two-thirds, lower 40% of the frame is open"`.
- *"keep the [specific item] from reference"* → `--outfit "the [item] from the reference, unchanged"` — note this often produces a corporate feel if the reference is a formal photo; only do it when the brand requires it.

## Anti-patterns (encoded in the helper's default prompt — surface here so iteration doesn't undo them)

- ❌ Generic studio props (microphone, phone, ring light). Editorial uses tactile/analog objects, or no prop at all.
- ❌ Loud saturated backdrops. Tonal is the look — one warm muted color, slight directional lighting.
- ❌ Fashion-flashy outfit choices on every video (leather jacket, oversized blazer with statement collar). Quiet confidence is the register.
- ❌ Watermarks or text in the AI output. Text is the HyperFrames step.
- ❌ Centered face-fills-entire-frame with no room for text. Composition needs negative space in the lower third.
- ❌ Crowded scenes (cafés, streets, offices, kitchens). Solid backdrop only.
- ❌ "Stand still and smile" energy. Always caught-in-motion or caught-mid-thought.
- ❌ Same gesture repeated across a creator's videos. Always check the previous thumbnail and pick a different pose.

## Next step
Once `bg_generated.png` exists, follow `prompts/generate-thumbnail.md` to:
1. Compose the editorial typography (Inter Bold + Playfair Display Italic) over the AI base in HyperFrames.
2. Render via `hyperframes render` → extract the first frame with ffmpeg → `{{edit_dir}}/thumbnail.jpg`.

## File layout reference

```
/Users/juanse/Developer/video-use/
├── helpers/
│   └── generate_thumbnail_bg.py        ← reusable CLI
├── prompts/
│   ├── generate-thumbnail-base.md      ← this file (AI base step)
│   └── generate-thumbnail.md           ← full thumbnail workflow (base + typography + extract)
├── thumbnails/
│   ├── base-photos/                    ← source-of-truth subject portraits
│   │   ├── natalia-serrano/
│   │   │   └── Natalia-Serrano.png
│   │   └── <creator-slug>/
│   │       └── <Name>.png
│   └── benchmark/                      ← reference thumbnails for the click-bait aesthetic
│       └── *.{jpeg,avif}
└── videos/<creator>/<video>/edit/
    └── animations/slot_thumbnail/
        ├── bg_generated.png            ← output of this step
        ├── bg.jpg                      ← fallback (video frame) for typography preview before AI base exists
        ├── index.html                  ← HyperFrames composition (typography overlay)
        └── render.mp4                  ← single-frame HF render, ffmpeg-extracts to thumbnail.jpg
```
