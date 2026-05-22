# Add full captions + emphasis + cinematic title cards + sound effects to the trimmed video

This builds **three independent layers** on top of an already-trimmed video. Keep them mentally separate — each is defined in one place and is iterated on independently.

- **Layer 1 — Caption track:** the ENTIRE video subtitled, every word, in 2–4 word chunks, medium size, SF Pro **Light Italic** — and ONLY Light Italic. Every word looks identical; no word in the caption track is ever bold. No SFX. On for the whole video EXCEPT while a title card is showing — see "Caption / title-card mutual exclusion" below.
- **Layer 2 — Emphasis:** Claude decides which individual words are important. An important word gets exactly one SFX hit when it is spoken — that is the ONLY effect of emphasis. The word is NOT bolded, NOT recolored, NOT resized in the caption track; it stays plain SF Pro Light Italic like every other caption word. Emphasis is audible only. This is the ONLY layer that produces SFX. (If an important word is also chosen as a title-card phrase, the card carries the visual weight — see Layer 3.)
- **Layer 3 — Title cards:** the big punchy cinematic cards (the original feature). Bigger than captions, in SF Pro Heavy Italic. While a title card is on screen, the caption track is hidden so the two never stack. A word destined to become a title card never appears in the caption track first — see "Caption / title-card mutual exclusion." SFX rules below.

**Caption / title-card mutual exclusion (critical):** the caption track and title cards must NEVER be on screen at the same time, and a word that will become a title card must NEVER appear in the caption track before the card shows it.

1. **No simultaneous display.** Whenever a title card's visibility window is open, the caption track is fully hidden for that window — plus a **1-frame pad on each side** (~0.042s at 24fps; scale to `1/fps` for other frame rates). The caption track hides 1 frame BEFORE the card appears and resumes 1 frame AFTER the card's clip window closes. The pad is anti-flicker insurance on both edges so a caption never peeks for a single frame as a card enters or leaves.

2. **No title word leaking into captions first.** A title card pops exactly when its first word is spoken, but the 2–4 word caption chunk containing that word may START EARLIER than the word (the chunk can open a word or two before). That would flash the title word as a normal caption a beat before the card hits — not allowed. So the hide window for a card extends BACKWARD to also cover the start of whatever caption chunk contains the card's first word. Concretely: if the card's first word sits inside caption chunk C, the entire chunk C is suppressed (it is not shown at all), so the title word's first on-screen appearance is the card itself. See Layer 1 step 5 for the exact rule.

Both rules apply ONLY to title cards. Emphasized words (Layer 2) do not hide or alter the caption at all — they are audible-only.

Output: `{{edit_dir}}/final_with_titles.mp4` — the trimmed video composited with the caption track, emphasis styling, title cards, image overlays, and synced SFX. Source video, EDL, and transcript are read-only.

## Inputs (you must have all before starting)
- **Trimmed video:** `{{path/to/source_edit.mp4}}` — already cut. Audio/visual base; do NOT re-cut it.
- **EDL:** `{{edit_dir}}/edl.json` — source→output time mapping for every kept range.
- **Transcript:** `{{edit_dir}}/transcripts/{{source_basename}}.json` — word-level Scribe JSON of the ORIGINAL (pre-trim) source. This drives the full caption track.
- **Fonts (absolute paths, REQUIRED):**
  - SF Pro Light Italic: `{{path/to/SF-Pro-LightItalic.otf}}`
  - SF Pro Heavy Italic: `{{path/to/SF-Pro-HeavyItalic.otf}}`
  These are the ONLY two fonts used anywhere in the output — captions, emphasis, and title cards. Do NOT load Montserrat or any Google Font. If a path is unreadable by the render process, copy the file into `{{edit_dir}}/animations/slot_titles/fonts/` first and reference it locally via `@font-face`.

## Optional
- **Image inserts:** absolute paths + the spoken phrase that triggers them (e.g. "este video de acá" → `/path/to/thumbnail.jpg`).
- **Brand accent color:** hex (e.g. `#3d5eff`). Applied to 1–2 payoff title cards only; the rest stay white. Does NOT apply to the caption track.
- **Pacing mode:** `documentary` (sparse title cards — 1 every ~5–7s) or `dynamic` / `mrbeast` (1 every ~2s). Default: `documentary`. This affects TITLE CARDS only — the caption track is always full-coverage regardless of mode. Ask if unclear.
- **Opener camera move:** `none` (default), `zoom-out`, or `zoom-in`. See the **Opener camera move** section.

---

## LAYER 1 — Caption track (every word, hidden only under title cards)

The whole video is subtitled. Every word the speaker says appears as a caption. No gaps except natural pauses where nobody is speaking — and except while a title card is on screen, where the caption track is deliberately hidden.

1. **Chunk the transcript into caption groups of 2–4 words.** Walk the word-level transcript in order and group consecutive words into chunks of 2, 3, or 4 words. Prefer chunks that break on natural phrase boundaries (after a comma, before a conjunction, at a clause edge) rather than splitting mid-phrase. Never leave a 1-word orphan chunk — merge it into the neighbour. A chunk is at most 4 words; if a natural phrase is longer, split it into two chunks of balanced length.
2. **Time every chunk.** The chunk's `data-start` is the source-time start of its FIRST word, converted to output-time via the EDL. The chunk's end is the source-time end of its LAST word, converted to output-time. Use the same `src_to_out` conversion as everything else (see **Word alignment** below). A chunk stays on screen for its full word span; the NEXT chunk replaces it the instant its first word begins. No fade — hard swap.
3. **No SFX on the caption track.** Captions are continuous; a SFX per chunk would be a machine-gun. SFX come only from Layer 2.
4. If two consecutive chunks have a gap > ~0.6s between them (speaker pause), let the screen go empty during the pause rather than stretching the earlier chunk.
5. **Hide under title cards (mandatory).** After all caption chunks are timed, walk the title-card list. For every title card, build its hide window in two stages:

   **5a. Base padded window.** Start with `[card_start − PAD, card_end + PAD]` where `PAD = 1 frame` (~0.042s at 24fps; `1/fps` for other rates).

   **5b. Backward extension to swallow the title word's caption chunk.** Find the caption chunk `C` that contains the card's FIRST word (the word the card pops on). Because a 2–4 word chunk can begin before that word, `C.start` may be earlier than `card_start`. Extend the hide window's left edge back to `min(card_start − PAD, C.start)`. The full window is therefore `[min(card_start − PAD, C.start), card_end + PAD]`. This guarantees chunk `C` is fully covered, so the title word never appears as a normal caption before the card.

   Then suppress every caption chunk against the final hide window `[H_start, H_end]`:
   - A caption chunk fully inside the hide window → not rendered at all. (Chunk `C` always falls here by construction.)
   - A caption chunk that starts before the window and runs into it → its on-screen end is cut to `H_start`.
   - A caption chunk that starts inside the hide window and ends after it → its on-screen start is pushed to `H_end`.
   - A caption chunk spanning the entire window → split into a pre-card part (ending at `H_start`) and a post-card part (starting at `H_end`); drop either part if it becomes shorter than ~0.15s (too short to read).

   The `PAD` is anti-flicker insurance on both edges; the backward extension additionally ensures no title word is ever shown in the caption track before its card. The words under a hidden chunk are NOT re-shown later — they are covered by the title card, which is presenting the same moment. Caption and title-card visibility must be provably disjoint, and no caption chunk containing a title word may ever render.

### Caption style
- **Font:** SF Pro Light Italic (`{{path/to/SF-Pro-LightItalic.otf}}`), loaded via `@font-face`.
- **Case:** sentence case as spoken — do NOT uppercase the caption track. (Uppercase is reserved for title cards.)
- **Color:** white `#ffffff`.
- **Shadow:** a tight, low-blur, fairly opaque drop shadow — NOT a soft glow. Default value:
  `text-shadow: 0 1px 2px rgba(0,0,0,0.55);`
  This reads as "barely-there" to the viewer but keeps thin white text legible on bright frames. If the user says the shadow is too strong, lower the alpha (`0.55` → `0.4` → `0.3`); if captions are hard to read on a bright shot, raise the alpha toward `0.7` or add a second layer `0 0 4px rgba(0,0,0,0.45)`. Do NOT switch to a hard outline.
- **Size — MEDIUM.** Captions are read continuously, so they sit smaller than title cards. Use **s-120 to s-140** (font-size in px on the 1920w portrait frame). Default **s-130**. Title cards remain larger (s-180+) so the hierarchy is obvious. If a 4-word chunk overflows the safe content width at s-130, drop to s-120 for that chunk before considering anything else; never two-line the caption track — captions stay single-line.
- **Position:** centered horizontally; vertically anchored so the caption sits **just below the speaker's chin**, in the center-middle band of the frame — NOT at the bottom. Anchor by the caption's vertical center at roughly **62% of frame height** as the starting point, then nudge per video so the line clears the chin without floating in the middle of the torso. This keeps captions away from both the speaker's face and the bottom UI strip. See **Platform safe areas** — captions must still clear the right-rail column and the bottom UI zone (62% center-anchor does this by construction, but verify in the self-eval).
- **Animation:** none, or an extremely subtle 1-frame opacity cut-in. Captions should not punch or scale — they are a uniform reading surface. No word in the caption track animates, scales, or changes weight, including emphasized words.

---

## LAYER 2 — Emphasis (Claude picks important words → SFX only)

Within the running caption track, some individual words carry the meaning — the key noun, the payoff word, the imperative verb, the surprising number, the antithesis word. **Claude decides which words are important.** Be selective: emphasis is meaningless if everything is emphasized. As a rough budget, aim for **one emphasized word every ~4–8 seconds** of speech — fewer is fine, more dilutes it.

Emphasis is **audible only**. For each word Claude marks as important:
1. **No visual change whatsoever.** The word stays SF Pro Light Italic, same color, same size, same shadow as every other caption word. It is NOT bolded, NOT switched to Heavy Italic, NOT recolored, NOT resized, NOT scale-punched. The caption track is visually uniform — a viewer reading the captions sees no difference on an emphasized word. (Heavy Italic is used ONLY on title cards, Layer 3.)
2. **SFX:** the emphasized word gets exactly ONE SFX, fired at the word's output-time start (word-aligned, see below). This is the ONLY source of SFX in the entire output. Pick from the library at `sound/effects` using the table in the SFX section. The SFX hit is the entire payoff of emphasis.

If two important words fall within 0.5s of each other, emphasize only the stronger one — keep the SFX from colliding.

Note: if an important word is also a strong enough moment to be a title-card phrase, promote it to a title card (Layer 3) — the card then carries the visual weight and its own SFX, and you do NOT additionally place a Layer 2 SFX on the same word.

---

## LAYER 3 — Title cards (the big cinematic cards)

Title cards are the original punchy feature: a few big words slammed on screen at the strongest moments. While a card is on screen the caption track is hidden (see "Caption / title-card mutual exclusion") — the two never stack. Cards are visually bigger than captions.

1. Build a HyperFrames slot at `{{edit_dir}}/animations/slot_titles/` (scaffold with `npx --yes hyperframes init . --example blank --non-interactive --skip-skills` if missing). The caption track, emphasis layer, and title cards all live in this one HyperFrames composition.
2. Pick the verbatim title-card phrases. **One card = one moment the speaker emphasizes.** Use ONLY words that appear in the transcript at that moment. No narrative summaries ("PASO 1", "EL MÉTODO"). Allowed: spelling/name corrections (transcript says "Grusenko" → "RUSENKO" if the user supplies the real spelling). Max 4 words per card; split into two lines via `<br>` if it would overflow.
3. **Card timing — the card pops exactly when its first word starts being said.** A card's `data-start` is the output-time start of the FIRST word of its phrase, found in the transcript and converted via the EDL `src_to_out` (see **Word alignment**). The card must appear on the frame the speaker begins that word — not after the word, not on the sentence, not eyeballed. This is the same word-alignment math used everywhere; the card hit and the spoken word are frame-locked. That same output time is also the `absolute_start_s` of the card's SFX.
4. **Pacing** controls title-card density only:
   - `documentary` — ~1 card every 5–7s. Land on the strongest moments only. ~3–5 cards on a 24s edit.
   - `dynamic` / `mrbeast` — ~1 card every ~2s. ~10–12 cards on a 24s edit. Scale-punch bumps to 106% (default 102%).
5. **Card duration** = `(phrase_end_out − phrase_start_out) + 0.30s tail`, capped at `next_card_start − 0.05s`.

### Title-card style
- **Font:** SF Pro Heavy Italic (`{{path/to/SF-Pro-HeavyItalic.otf}}`), UPPERCASE, white `#ffffff`. Same tight low-blur shadow as captions (heavier weight tolerates a slightly stronger shadow if needed). NO hard outline.
- **Position:** anchor by the BOTTOM edge so the bottom line lands on the platform safe line at **72% of frame height** (`bottom: 28%`). This is distinct from the caption track's 62%-center anchor — title cards sit lower, captions sit at chin level, so the two never stack on the same line.
- **Brand accent color (optional):** when supplied, apply via an `.accent` class to ONLY the 1–2 payoff cards. Rest stay white. Never applies to captions.
- **Size class:** `s-180`/`s-200`/`s-220`/`s-240`/`s-260`/`s-280`/`s-300`/`s-340`/`s-380` (px). Title cards are always bigger than the caption track's s-120–140.
- **Single-line char budget on 1920w portrait** (working in a 1570px safe container):
  | Size | Max chars (incl. spaces) |
  |---|---|
  | s-380 | ~8 |
  | s-340 | ~9 |
  | s-300 | ~11 |
  | s-260 | ~12 |
  | s-240 | ~13 |
  | s-220 | ~14 |
  | s-200 | ~16 |
  | s-180 | ~18 |
  Wider than budget → split with `<br>` into two lines, each ≤8 chars. Two-line cards typically render s-260 (tight) or s-220 (longer). **When in doubt, two lines.**
- **Animation:** scale-punch 100% → 102% (documentary) / 106% (dynamic) over 3 frames (0.125s, `power2.out`). Hard cut in/out via the `.clip` visibility window. No fades.
- **Image overlays:** rounded corners (radius 36px), 8px white border ring, layered drop shadow, scale-punch from 0.92 with `back.out(2)` over 180ms. Position with `top` so the image sits above the speaker's face. Same platform safe-area rules as everything else.

---

## Word alignment (applies to caption chunks, emphasis words, title cards, and their SFX)

For any element, find its word in the transcript, get the source-time start, then convert to output-time using the EDL ranges:
```
src_to_out(src_t):
  for r in edl.ranges:
    if r.start <= src_t <= r.end:
      return out_t_so_far + (src_t - r.start)
  # else clamp to nearest range edge
```
That output time is the element's `data-start` AND, where it has a SFX, the SFX's `absolute_start_s`. Drift between visual and audio is the failure mode this whole prompt exists to prevent — do not eyeball it.

---

## SFX library and selection

SFX fire ONLY on emphasized words (Layer 2) and, separately, on title cards (Layer 3) and image overlays. The caption track itself is silent.

Pick a SFX per emphasized word / card from the library at `sound/effects`:
- First card / opening title → `pop-whoosh`
- Hard cut between scenes → `an-ideal-swoosh`
- Single emphasis word → `pop`
- Kicker / step card swoop → `pop-whoosh`
- Number / fact callout → `ping`
- Clever observation → `keen`
- Punchline land → `punch`
- Name / credit overlay → `ping`
- Final closing ding → `microwave-oven-clin`
- Image overlay pop-in → `pop`

**Risers are BANNED.** The three riser SFX — `riser`, `metalic-riser`, `metalic-reverse-riser` — must NEVER be used anywhere in the video, under any circumstance. Not on title cards, not on emphasized words, not on image overlays, not on the opener zoom, not at the start, not at the end. The output contains zero risers. The opener camera zoom (if used) has no sound of its own. Do not add any `-i` input for a riser file to the ffmpeg command.

### SFX volume — reduced 35% from the prior baseline
The prior baseline levels are listed below as **OLD → NEW**. Reducing a SFX by 35% means it plays at 65% of its prior linear amplitude, which is **−3.7 dB** quieter. Apply this offset to every SFX (round to one decimal):
| SFX | OLD level | NEW level (−3.7 dB) |
|---|---|---|
| `pop-whoosh` | −7 dB | **−10.7 dB** |
| `an-ideal-swoosh` | −8 dB | **−11.7 dB** |
| `pop` | −9 dB (−6 for image overlay) | **−12.7 dB** (−9.7 image) |
| `ping` | −8 dB | **−11.7 dB** |
| `keen` | −8 to −9 dB | **−11.7 to −12.7 dB** |
| `punch` | −6 dB | **−9.7 dB** |
| `microwave-oven-clin` | −7 dB | **−10.7 dB** |
If the user later says a specific SFX is still too loud or now too quiet, adjust that one SFX only.

### SFX timing rules
- One emphasized word / one card = one SFX. No double-hits.
- Same UCS family (two pops, two swooshes) within 0.5s → remove one. Reusing the same SFX file ≥1s apart is fine — provide it as multiple `-i` inputs, each with its own `adelay`.
- Risers (`riser`, `metalic-riser`, `metalic-reverse-riser`) are BANNED — zero risers anywhere in the video, see the SFX library section.
- **Truncation:** when the remaining video time after a SFX start is shorter than the SFX, `-shortest` truncates it. Fine for attack-forward SFX (`pop`, `ping`, `microwave-oven-clin`, `punch`) — the hit lands, tail is cut. Do NOT pick a tail-heavy SFX (long whooshes) inside the final ~2s.
- Image overlay = pop SFX at appearance, regardless of any concurrent SFX.

---

## Render and composite

6. Render the HyperFrames composition (caption track + emphasis + title cards, all layers) to ProRes alpha MOV:
   `npx --yes hyperframes render . --format mov -f 24 -q standard -o render.mov`
   **Must be `--format mov`** — WebM has no alpha, the overlay would be opaque.
7. Composite via ffmpeg: overlay the alpha MOV onto the trimmed video; mix dialogue + every SFX with `amix=inputs=N:normalize=0:duration=longest` so dialogue level is preserved AND audio extends to the longest stream. Output to `final_with_titles.mp4`.
8. Self-eval (below) before declaring done.

### Critical: portrait/4K rendering
- HyperFrames composition root must declare `data-width` / `data-height` matching the source frame exactly. For a 1920×3414 portrait clip: `data-width="1920" data-height="3414"`, `<body>` `width: 1920px; height: 3414px`.
- Composition root must set `data-duration="{{trimmed_video_duration_s}}"` (exact, to 3 decimals). Default is 10s — anything shorter renders a black MOV past 10s. The caption track must cover the FULL duration.
- ffmpeg overlay filter: `[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v]`, applied LAST in the filter chain.
- 30ms audio fades are NOT needed — the trimmed input already has them at every cut.
- HF lint will warn `external_script_dependency` (GSAP CDN) and `timeline_track_too_dense` (the caption track WILL exceed 5 elements per track — this is expected and non-blocking for a full caption track). Ignore both.

---

## Platform safe areas (TikTok / Reels / Shorts)

NON-negotiable framing rules. Apply to the caption track, emphasis words, title cards, and image overlays.

**Bottom UI zone — bottom ~25–28% of the frame is owned by the platform** (caption, username, hashtags, music, CTA). Any text here gets obscured.

**Right-rail column — rightmost ~14% of the frame is owned by the platform** (like / comment / share / sound icons). Any text extending into this column gets obscured.

| Output dimension | Title-card bottom anchor | Caption center anchor | Safe content width | Horizontal margin each side |
|---|---|---|---|---|
| 1080×1920 | y = 1382px (72%) | y ≈ 1190px (62%) | 880px | 100px |
| 1920×3414 | y = 2458px (72%) | y ≈ 2117px (62%) | 1570px | 175px |
| Other portrait | y = `0.72 × frame_h` | y ≈ `0.62 × frame_h` | `0.815 × frame_w` | `0.0925 × frame_w` |

**Implementation contract:**
1. **Captions** anchor by vertical CENTER at ~62% of frame height (just below the chin, center-middle band). Nudge per video so the line clears the chin and doesn't float over mid-torso. The 62% band is well clear of the bottom UI zone.
2. **Title cards** anchor by BOTTOM edge at 72%. Captions at 62% and cards at 72% never collide on the same line.
3. **Width:** the widest rendered line (caption chunk OR card) must fit inside the safe content width. Captions overflow → drop s-130 to s-120. Title cards overflow → drop one size class, then two-line.
4. **No text inside the right-rail column.** Centered captions/cards clear it by construction.

**Tradeoff to accept:** the 62% caption band sits over the speaker's upper torso. That is correct and intended — it keeps captions below the chin/face and above the bottom UI. If captions land on a distracting gesture, nudge that video's caption anchor down a few percent, but never below ~68% (that risks the bottom UI) and never up onto the face.

---

## Opener camera move (when requested)

Adds a 0.5–2.0s zoom at the start. Applied to the **base video only** in the ffmpeg composite step — all overlays (captions, cards, images) composite on top of the already-zoomed frame and stay fixed in screen space.

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
- `{OUTW}`/`{OUTH}` = output frame size.
- `{START_ZOOM}` = initial zoom. **1.3 is the sweet spot.** 1.5 too aggressive on portrait; 1.2 barely noticeable; 1.4 for a cinematic close-up.
- `{RATE}` = (`{START_ZOOM}` − 1.0) / `{DURATION}`. Linear ramp from `START_ZOOM` at t=0 to 1.0 at t=DURATION, then clamps.
- `{CROP_Y}` = vertical crop offset. Portrait talking-head → `0` (top-aligned). Landscape / centered footage → `(ih-{OUTH})/2`.

**Duration feel** (START_ZOOM=1.3): 2.0s/RATE 0.15 cinematic · 1.2s/0.25 balanced · 0.8s/0.375 snappy · 0.5s/0.6 punch-out.

**Sync to the first caption chunk** (not the first title card — the caption track starts earlier). Time the zoom so it resolves at or just before the first caption appears.

**For `zoom-in`:** invert — `min({END_ZOOM}, 1.0 + RATE*t)`, `RATE = ({END_ZOOM} − 1.0) / DURATION`. Lands at 1.15–1.25× on a payoff word; use the same word-alignment math.

Order matters: `[0:v] → scale → crop → [zoomed]; [zoomed][1:v] → overlay → [v]`. Never zoom AFTER the overlay or the captions/cards zoom too.

---

## Self-eval before declaring done

Sample frames and check:

**Caption track:**
- Sample several frames across the whole video. The caption track is present and correct for the FULL duration — no long stretches of missing captions while the speaker is talking, EXCEPT under title cards where captions are intentionally hidden.
- Captions are 2–4 word chunks, SF Pro Light Italic, centered, sitting just below the chin (~62% band), not on the face, not in the bottom UI zone.
- Each caption is single-line and fully on-screen — no horizontal overflow. Overflow → drop s-130 to s-120.
- Shadow is subtle but the white text is legible on bright frames. Too strong → lower alpha; illegible → raise alpha.
- **Caption / title-card exclusion:** for every title card, sample a frame inside the card's window. The caption track must NOT be visible there — only the card. If a caption shows under a card, the hide logic in Layer 1 step 5 was not applied. Also confirm captions hide ~1 frame before each card appears and resume ~1 frame after each card ends — a clean gap on both edges, no caption peeking at the entry or exit frame.

**Emphasis:**
- The caption track is visually uniform — sample frames on emphasized words and confirm they look IDENTICAL to surrounding caption words (Light Italic, same size, same color, no bold, no punch). If any caption word renders bolder than its neighbours, that is a bug.
- Emphasis is selective (~1 per 4–8s), not on every other word.
- Each emphasized word has exactly one SFX, word-aligned to when it's spoken.

**Title cards:**
- Sample one frame per card at `card_start + 0.2s`. Text fully on-screen, in SF Pro Heavy Italic, bigger than the caption track, not occluding the face. Bottom-anchored at 72%.
- **Card timing:** the card appears exactly when the speaker starts its first word — verify by sampling a frame at `card_start − 1 frame` (card absent, word not yet started) and `card_start` (card present, word starting). No drift.
- **No title word leaks into captions.** For each card, sample frames in the ~1s BEFORE `card_start`. The card's word(s) must NOT appear anywhere in the caption track during that pre-roll — the caption chunk containing the title word must be fully suppressed (Layer 1 step 5b). The word's first on-screen appearance is the card itself.
- Accent color (if used) on only the 1–2 payoff cards.

**SFX:**
- SFX fire ONLY on emphasized words, title cards, and image overlays — never on plain caption chunks.
- All SFX levels reflect the −3.7 dB (35%) reduction.
- No same-family SFX within 0.5s. No tail-heavy SFX in the last 2s.
- **Risers:** zero risers in the mix — `riser`, `metalic-riser`, `metalic-reverse-riser` appear nowhere, not even on the opener zoom. Confirm no riser file was passed as an ffmpeg `-i` input.

**Global:**
- Fonts: ONLY SF Pro Light Italic and SF Pro Heavy Italic appear anywhere. No Montserrat, no Google Font.
- **Platform safe-area check (REQUIRED).** Mentally overlay a TikTok/Reels frame: bottom 25–28% strip and right 14% column. NO caption, emphasis word, title card, or image overlay falls inside either zone.
- `ffprobe` the output: duration ≈ trimmed input duration (within ~120ms encoder padding). Larger drift = `-shortest` truncation; check SFX placements.

---

## How I'll iterate

Natural-language feedback, per layer:

**Captions:** *"captions are too big / too small"* (adjust s-130 within s-120–140) · *"captions are too high / covering the chin"* (nudge the 62% anchor) · *"captions too low / near the buttons"* (raise toward 60%) · *"shadow too strong"* (lower the rgba alpha) · *"captions hard to read on bright shots"* (raise alpha or add a second shadow layer) · *"use 3-word chunks not 4"* (tighten the chunk size range).

**Emphasis:** *"too many SFX hits"* / *"not enough emphasis"* (adjust the ~1-per-4–8s budget) · *"don't emphasize ESCOGER, emphasize LANZARLO instead"* (change which word gets the SFX) · *"that word should be a title, not just a sound"* (promote the emphasized word to a Layer 3 title card).

**SFX:** *"the pop on RUSENKO is too quiet / loud"* (adjust that one SFX level) · *"swap the ping for a pop on the number"* · *"reduce SFX more"* (apply a further dB cut).

**Title cards:** *"DAVID RUSENKO is too small"* · *"drop the PERFECTO card"* · *"swap the yellow accent for #3d5eff"* · *"go from dynamic to documentary"* · *"the card pops too late / too early"* (the card is not word-aligned — re-anchor `data-start` to the first word's output time) · *"a caption is still showing under the title"* (the Layer 1 step-5 hide logic missed that card window — re-clip the overlapping caption chunk).

**Framing / zoom:** *"buttons overlapping the text"* / *"add safe margin"* (drop safe content width) · *"zoom-out faster"* (halve DURATION, double RATE) · *"start tighter"* (bump START_ZOOM 1.3 → 1.4). The opener zoom is silent — there is no riser to tune.

Each layer's definitions live in one place. Update the relevant layer and re-render. Don't re-trim, don't re-transcribe. Re-render the HyperFrames MOV (~30s for 24s portrait, ~3–4 min for 36s+); composite is ~30s; zoom-only changes need no HF re-render.