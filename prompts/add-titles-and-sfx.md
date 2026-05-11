# Add cinematic title cards + sound effects to the trimmed video

Inputs (you must have all three before starting):
- **Trimmed video:** `{{path/to/source_edit.mp4}}` — already cut. This is the audio/visual base; do NOT re-cut it.
- **EDL:** `{{edit_dir}}/edl.json` — gives the source→output time mapping for every kept range.
- **Transcript:** `{{edit_dir}}/transcripts/{{source_basename}}.json` — word-level Scribe JSON of the ORIGINAL (pre-trim) source.

Optional:
- **Image inserts:** absolute paths + the spoken phrase that triggers them (e.g. "este video de acá" → `/path/to/thumbnail.jpg`).
- **Brand accent color:** hex (e.g. `#3d5eff`). Applied to 1–2 payoff cards only; the rest stay white.
- **Pacing mode:** `documentary` (sparse — 1 card every ~5–7s) or `dynamic` / `mrbeast` (1 card every ~2s). Default: `documentary`. Ask if unclear.
- **Opener camera move:** `none` (default), `zoom-out` (start zoomed in on subject, pull back to full frame), or `zoom-in` (start wide, push in). When `zoom-out`/`zoom-in` is requested, see the **Opener camera move** section below.

Output: `{{edit_dir}}/final_with_titles.mp4` — the trimmed video composited with title overlays, image overlays, and synced SFX. Source video, EDL, and transcript are read-only.

## Deliver
1. Build a HyperFrames slot at `{{edit_dir}}/animations/slot_titles/` (scaffold with `npx --yes hyperframes init . --example blank --non-interactive --skip-skills` if missing).
2. Pick the verbatim title-card phrases. **One card = one moment the speaker emphasizes.** Use ONLY words that appear in the transcript at that moment. No narrative summaries ("PASO 1", "EL MÉTODO"). Allowed: spelling/name corrections (e.g. transcript says "Grusenko", correct to "RUSENKO" if user supplies the real spelling). Max 4 words per card; split into two lines via `<br>` if it would overflow.
3. **Word-align every card.** For each card, find its first word in the transcript, get the source-time start, then convert to output-time using the EDL ranges:
   ```
   src_to_out(src_t):
     for r in edl.ranges:
       if r.start <= src_t <= r.end:
         return out_t_so_far + (src_t - r.start)
     # else clamp to nearest range edge
   ```
   That output time is BOTH `data-start` for the title AND `absolute_start_s` for its SFX. Drift between visual and audio = the whole point of this prompt; do not eyeball it.
4. **Card duration** = `(phrase_end_out - phrase_start_out) + 0.30s tail`, capped at `next_card_start - 0.05s`. Tight cards land hard; long tails feel sluggish.
5. Pick a SFX per card from the library at `/Users/juanse/Developer/video-use/sound/effects/`. Defaults that work:
   - First card / opening title → `pop-whoosh` (-7 dB)
   - Hard cut between scenes → `an-ideal-swoosh` (-8 dB)
   - Single emphasis word → `pop` (-9 dB)
   - Kicker / step card swoop → `pop-whoosh` (-7 dB)
   - Number / fact callout → `ping` (-8 dB)
   - Clever observation → `keen` (-8 to -9 dB)
   - Punchline land → `punch` (-6 dB)
   - Name / credit overlay → `ping` (-8 dB)
   - Build into payoff cut → `metalic-reverse-riser` peaks AT the cut (start = cut_time − 1.85s)
   - Final closing ding → `microwave-oven-clin` (-7 dB)
   - Image overlay pop-in → `pop` (-6 dB)

   **When the remaining video time after a card start is shorter than the SFX**, `-shortest` will truncate the SFX. That is fine for attack-forward SFX (`pop`, `ping`, `microwave-oven-clin`, `punch`) — the hit lands and the tail just gets cut. Do NOT pick a tail-heavy SFX (`riser`, `metalic-riser`, long whooshes) inside the final ~2s of the video; the build never resolves.

6. Render the HyperFrames composition to ProRes alpha MOV: `npx --yes hyperframes render . --format mov -f 24 -q standard -o render.mov`. **Must be `--format mov`** — WebM has no alpha, the overlay will be opaque.
7. Composite via ffmpeg: overlay the alpha MOV onto the trimmed video; mix dialogue + every SFX with `amix=inputs=N:normalize=0:duration=longest` so dialogue level is preserved AND the audio extends to the longest stream. Output to `final_with_titles.mp4`.
8. Sample one frame per card at `card_start + 0.2s` (after the scale-punch has settled) and visually verify alignment + frame fit.

## Pacing (cards per second)

- **`documentary`** — ~1 card every 5–7s. Use for explainers, interviews, calmer feel. Land cards only on the strongest moments. For a 24s edit, that's 3–5 cards.
- **`dynamic` / `mrbeast`** — ~1 card every 2s, sometimes ~1.5s. Use for high-energy social cuts. Mark every emphasized word (key noun, payoff word, imperative verb, antithesis word). For a 24s edit, that's 10–12 cards. Cards can sit shoulder-to-shoulder with sub-1s durations — short enough to read but quick enough to feel snappy.

In dynamic mode the scale-punch should be bumped to **106%** (default is 102%). The bigger landing matches the higher density.

## Style (proven defaults — change only if the user asks)
- Font: Montserrat 900 (Black) via Google Fonts (`@import` in HF composition), UPPERCASE, white `#ffffff`, soft drop shadow, NO hard outline.
- Position: lower-third, `top: 78%` (avoids face occlusion in portrait talking-head footage).
- **Brand accent color (optional):** when supplied, apply via an `.accent` class to **only the 1–2 payoff cards** — the imperative verb (e.g. `LÁNZALO`), the punchline (e.g. `DEMASIADO TARDE`), or a single hero word. The rest stay white. Color-saturating every card kills the accent.
- Size class: `s-180`/`s-200`/`s-220`/`s-240`/`s-260`/`s-280`/`s-300`/`s-340`/`s-380` (font-size in px).
- **Single-line char budget on 1920w portrait** (Montserrat 900 ≈ 0.55× font-size per uppercase char, working in a 1820px container):
  | Size | Max chars (incl. spaces) | Example that fits |
  |---|---|---|
  | s-380 | ~8 | `LÁNZALO` (7) |
  | s-340 | ~9 | `LÁNZALO` (7) |
  | s-300 | ~11 | `PERFECTO` (8), `TE GUSTA` (8), `CONSEJO` (7) |
  | s-260 | ~12 | `AVERGÜENZA` (10) |
  | s-240 | ~13 | `AVERGÜENZA` (10) |
  | s-220 | ~14 | `NO DEBES VER` (12) |
  | s-200 | ~16 | `PRIMER VIDEO` (12) |
  | s-180 | ~18 | (rarely needed) |

  Anything wider than the budget → split with `<br>` into two lines, each ≤8 chars (e.g. `¿CAMBIÓ<br>LA VIDA?`, `DEMASIADO<br>TARDE`, `PRIMER VIDEO<br>EN TIKTOK`). Two-line cards typically render at s-260 (tight phrases) or s-220 (longer phrases). **When in doubt, two lines** — the cost of an overflow ("DEMASIADO TA…" with `RDE` clipped) is a re-render; the cost of two lines is one extra `<br>`.

- Animation: scale-punch 100% → **102% (documentary) / 106% (dynamic)** over 3 frames (0.125s, `power2.out`). Hard cut in/out via the `.clip` visibility window. No fancy fades.
- Image overlays: rounded corners (radius 36px), 8px white border ring, layered drop shadow, scale-punch from 0.92 with `back.out(2)` over 180ms. Position with `top` so the image sits above (not over) the speaker's face.

## Opener camera move (when requested)

Adds a 0.5–2.0s zoom at the start of the video to punch the viewer into the scene. The zoom is applied to the **base video only** in the ffmpeg composite step — title overlays composite on top of the already-zoomed frame and stay fixed in screen space, so cards don't ride the zoom.

**Filter pattern** (insert before the overlay step in `-filter_complex`):
```
[0:v]scale=
  w='{OUTW}*(max(1.0,{START_ZOOM}-{RATE}*t))':
  h='{OUTH}*(max(1.0,{START_ZOOM}-{RATE}*t))':
  eval=frame:flags=lanczos,
crop={OUTW}:{OUTH}:x='(iw-{OUTW})/2':y={CROP_Y}
[zoomed];
[zoomed][1:v]overlay=0:0:format=auto:eof_action=pass[v];
```

Where:
- `{OUTW}` / `{OUTH}` = output frame size (e.g. `1920`/`3414` for portrait).
- `{START_ZOOM}` = initial zoom factor. **1.3 is the sweet spot.** 1.5 is too aggressive on portrait (crops out parts of the face when top-aligned); 1.2 is barely noticeable. Cinematic close-up: 1.4.
- `{RATE}` = (`{START_ZOOM}` − 1.0) / `{DURATION}`. The expression `max(1.0, START_ZOOM − RATE*t)` is the per-frame zoom factor; linear ramp from `START_ZOOM` at t=0 to 1.0 at t=DURATION, then clamps to 1.0 for the rest of the video. Linear is right for short zooms — easing adds nothing under 1s.
- `{CROP_Y}` = vertical crop offset. For **portrait talking-head** use `0` (top-aligned) — the speaker's face is in the upper third of the frame and a centered crop loses the eyes. For landscape or speaker-centered footage, use `(ih-{OUTH})/2`.

**Duration feel cheat-sheet** (with START_ZOOM=1.3):

| Duration | RATE | Vibe | When |
|---|---|---|---|
| 2.0s | 0.15 | Cinematic pull — slow, deliberate | Documentary, intro to a story |
| 1.2s | 0.25 | Balanced | Most content |
| 0.8s | 0.375 | Snappy | Dynamic / social |
| 0.5s | 0.6 | Punch-out | MrBeast / hook-heavy openers |

**Sync to the first card.** Time the zoom so it resolves AT or just before the first title card lands. If the first card is at out=0.61s, a 0.5s zoom works — the zoom settles at 0.5s and the card hits on a stable frame at 0.61s. A 1.2s zoom would still be moving when the card pops, which can feel busy.

**For `zoom-in` (push-in)**, invert: `min({END_ZOOM}, 1.0 + RATE*t)` with `RATE = ({END_ZOOM} - 1.0) / DURATION`. Push-ins typically land at 1.15–1.25× on a payoff word or hard cut — use the SAME word-alignment math as title cards to pick the moment.

**Don't apply the zoom AFTER the overlay** — that would zoom the title cards too. Order matters: `[0:v] → scale → crop → [zoomed]; [zoomed][1:v] → overlay → [v]`.

## Critical: portrait/4K rendering
- HyperFrames composition root must declare `data-width` and `data-height` matching the source frame exactly. For a 1920×3414 portrait clip, set `data-width="1920" data-height="3414"` and `<body>` `width: 1920px; height: 3414px`. Otherwise the overlay scales wrong on composite.
- HyperFrames composition root must also set `data-duration="{{trimmed_video_duration_s}}"` (exact, to 3 decimals). The default is 10s — anything shorter renders a black/empty MOV past 10s.
- ffmpeg overlay filter: `[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v]`. Must be applied LAST in the filter chain (after any other video effects).
- 30ms audio fades are NOT needed here — the trimmed input already has them at every cut.
- HF lint will warn `external_script_dependency` on the GSAP CDN and `timeline_track_too_dense` if you have >5 cards in one file. Both are non-blocking — `hyperframes render` handles the CDN automatically, and a single-file timeline is fine for ≤15 cards. Ignore unless the user wants the cards split into sub-compositions.

## SFX timing rules
- One card = one SFX firing at the same instant. No double-hits.
- Same UCS family (e.g. two pops, two swooshes) within 0.5s = remove one. Reusing the same SFX file ≥1s apart is fine — provide it as multiple `-i` inputs in the ffmpeg command, each with its own `adelay`.
- Risers: at most one per 30s. Peak terminates AT a cut, never inside a beat. Never use a riser in the last 2s of the video — the resolution would be truncated.
- Image overlay = pop SFX at the moment of appearance, regardless of any concurrent title SFX.

## Self-eval before declaring done
After compositing, sample one frame per card at `card_start + 0.2s` (the scale-punch has settled by then; pre-punch the text is at 100% which is fine but the dynamic feel comes from catching it at 106%). For each frame check:
- Title text is fully on-screen (no horizontal overflow). Overflow = drop one size class OR split to two lines via `<br>`.
- Title is not occluding the speaker's face / eyes. Lower-third `top: 78%` handles this for portrait talking-head; if the speaker gestures low into frame, lift to `top: 72%`.
- Accent color (if used) appears on only the 1–2 payoff cards, not everywhere.
- Image overlays line up with whatever gesture the speaker makes ("points up" → image lands top-half).
- `ffprobe` the output to confirm duration ≈ trimmed input duration (within ~120ms encoder padding from the HF MOV). Larger drift = truncation from `-shortest`; check the SFX placements.

If a card overflows the frame, drop one size class. If two cards overlap visually, shorten the earlier one's duration to `next_card_start - 0.05s`. Re-render only the HyperFrames MOV (~30s for 24s portrait, ~3–4 min for longer 36s+ pieces); the composite step is ~30s.

## How I'll iterate
Natural-language feedback: *"DAVID RUSENKO is too small"*, *"the pop on ESCOGER is too quiet"*, *"add an image at 18s when he says 'lista'"*, *"swap the yellow accent for #3d5eff"*, *"go from dynamic to documentary"*, *"too many cards in the middle — drop PERFECTO and TE GUSTA"*, *"zoom-out faster"*, *"start tighter, go to 1.5×"*. Update the title definitions, SFX assignments, or opener-zoom parameters and re-render. Each lives in one place. Don't re-trim, don't re-transcribe.

For zoom feedback specifically: *"faster"* = halve DURATION (and double RATE). *"slower"* = double DURATION (and halve RATE). *"tighter"* = bump `{START_ZOOM}` from 1.3 → 1.4. *"snappier"* = drop DURATION below 0.5s (RATE ≥ 0.6 with START_ZOOM=1.3). Re-render in ~1 min; no HF re-render needed because the zoom is purely an ffmpeg filter on the base video.
