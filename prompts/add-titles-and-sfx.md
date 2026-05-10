# Add cinematic title cards + sound effects to a trimmed video

Inputs (you must have all three before starting):
- **Trimmed video:** `{{path/to/source_edit.mp4}}` — already cut. This is the audio/visual base; do NOT re-cut it.
- **EDL:** `{{edit_dir}}/edl.json` — gives the source→output time mapping for every kept range.
- **Transcript:** `{{edit_dir}}/transcripts/{{source_basename}}.json` — word-level Scribe JSON of the ORIGINAL (pre-trim) source.

Optional:
- **Image inserts:** absolute paths + the spoken phrase that triggers them (e.g. "este video de acá" → `/path/to/thumbnail.jpg`).

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
   - First card / opening title → `pop-whoosh`
   - Hard cut between scenes → `an-ideal-swoosh`
   - Single emphasis word → `pop` (-9 dB)
   - Kicker / step card swoop → `pop-whoosh` (-7 dB)
   - Number / fact callout → `ping` (-8 dB)
   - Clever observation → `keen` (-9 dB)
   - Punchline land → `punch` (-6 dB)
   - Name / credit overlay → `ping` (-8 dB)
   - Build into payoff cut → `metalic-reverse-riser` peaks AT the cut (start = cut_time − 1.85s)
   - Final closing ding → `microwave-oven-clin`
   - Image overlay pop-in → `pop` (-6 dB)
6. Render the HyperFrames composition to ProRes alpha MOV: `npx --yes hyperframes render . --format mov -f 24 -q standard -o render.mov`. **Must be `--format mov`** — WebM has no alpha, the overlay will be opaque.
7. Composite via ffmpeg: overlay the alpha MOV onto the trimmed video; mix dialogue + every SFX with `amix=normalize=0` so dialogue level is preserved. Output to `final_with_titles.mp4`.
8. Sample 6-10 frames from the output at the title-card moments and visually verify alignment + frame fit.

## Style (proven defaults — change only if the user asks)
- Font: Montserrat 900 (Black), UPPERCASE, white `#ffffff`, soft drop shadow, NO hard outline.
- Position: lower-third, `top: 78%` (avoids face occlusion in portrait talking-head footage).
- Size: pick from `s-180`/`s-220`/`s-240`/`s-260`/`s-280`/`s-300`/`s-340`/`s-380` to fit the frame width. Single-line cards rarely fit at >300px on a 1920-wide frame; switch to two-line via `<br>`.
- Animation: scale-punch 100% → 102% over 3 frames (0.125s, `power2.out`). Hard cut in/out via the `.clip` visibility window. No fancy fades.
- Image overlays: rounded corners (radius 36px), 8px white border ring, layered drop shadow, scale-punch from 0.92 with `back.out(2)` over 180ms. Position with `top` so the image sits above (not over) the speaker's face.

## Critical: portrait/4K rendering
- HyperFrames composition root must declare `data-width` and `data-height` matching the source frame exactly. For a 1920×3414 portrait clip, set `data-width="1920" data-height="3414"` and `<body>` `width: 1920px; height: 3414px`. Otherwise the overlay scales wrong on composite.
- ffmpeg overlay filter: `[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v]`. Must be applied LAST in the filter chain (after any other video effects).
- 30ms audio fades are NOT needed here — the trimmed input already has them at every cut.

## SFX timing rules
- One card = one SFX firing at the same instant. No double-hits.
- Same UCS family (e.g. two pops, two swooshes) within 0.5s = remove one.
- Risers: at most one per 30s. Peak terminates AT a cut, never inside a beat.
- Image overlay = pop SFX at the moment of appearance, regardless of any concurrent title SFX.

## Self-eval before declaring done
After compositing, sample frames at every card start time + every image overlay start. For each frame check:
- Title text is fully on-screen (no horizontal overflow).
- Title is not occluding the speaker's face / eyes.
- Image overlays line up with whatever gesture the speaker makes ("points up" → image lands top-half).
- For 5+ scenes worth of cards, also `ffprobe` the output to confirm duration matches the trimmed input (no truncation from `-shortest`).

If a card overflows the frame, drop one size class. If two cards overlap visually, shorten the earlier one's duration. Re-render only the HyperFrames MOV (~3-4 min for 36s portrait); the composite step is ~30s.

## How I'll iterate
Natural-language feedback: "DAVID RUSENKO is too small", "the pop on ESCOGER is too quiet", "add an image at 18s when he says 'lista'". Update the title definitions and/or the SFX assignments and re-render. Title definitions live in one place; SFX assignments live in one place. Don't re-trim, don't re-transcribe.
