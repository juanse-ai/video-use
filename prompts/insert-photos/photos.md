# Place image overlays on a video (interactive)

This is a standalone tool. Its ONLY job is to drop one or more still images onto an already-finished video at moments you choose, then composite the result. It does NOT add captions, title cards, or any text. It does NOT re-cut or re-transcribe anything.

Output: `{{edit_dir}}/with_images.mp4` — the input video with every image overlaid at its chosen moment and a `pop` SFX on each appearance. The input video, EDL, and transcript are read-only.

## Inputs (you must have all before starting)
- **Video:** `{{path/to/video.mp4}}` — the finished video to place images on. This is the audio/visual base; do NOT modify its cut.
- **EDL:** `{{edit_dir}}/edl.json` — source→output time mapping for every kept range. Needed to convert word-trigger times into the video's timeline.
- **Transcript:** `{{edit_dir}}/transcripts/{{source_basename}}.json` — word-level Scribe JSON of the ORIGINAL (pre-trim) source. Needed only for word triggers.
- **SFX library:** the `pop` sound at `sound/effects` (used on every image).

## Step 1 — Collect the images interactively

Do NOT assume any images up front. Ask the user, one image at a time, in a loop. For EACH image, ask these questions (use a single grouped prompt per image so the user answers in one go):

1. **Relative path of the image.** "What is the relative path of the image file?" — accept a path relative to `{{edit_dir}}` (or an absolute path). Verify the file exists and is a readable image (`.jpg`, `.jpeg`, `.png`, `.webp`) before continuing; if not, ask again.
2. **Trigger type.** "Trigger this image by a SECOND or by a WORD?" — two options:
   - **Second** — ask "At what second of the FINAL video should it appear?" This is a timestamp in the output video's timeline (the finished edit the user watches), NOT the original source. Use it directly as the image's appearance time.
   - **Word** — ask "Which spoken word triggers it?" then ask "Which occurrence of that word — 1st, 2nd, 3rd…?" (default: 1st). Find that occurrence in the transcript, take its source-time start, and convert to output time via the EDL (see **Word alignment** below). That output time is the image's appearance time.
3. After capturing the image, ask: **"Any more images? (yes / no)"** If yes, loop back to question 1 for the next image. If no, proceed to Step 2.

Collect all images before doing any rendering. Keep them in order of appearance time once all are gathered.

### Word alignment (word triggers only)
```
src_to_out(src_t):
  for r in edl.ranges:
    if r.start <= src_t <= r.end:
      return out_t_so_far + (src_t - r.start)
  # else clamp to nearest range edge
```
The triggering word's source-time start → `src_to_out` → the image's appearance time in the output video.

## Step 2 — Decide each image's duration

Each image stays on screen for a duration **Claude chooses, between 0.8s and 2.0s — never longer than 2.0s.** Pick within that range using:
- **How long the trigger is "live."** For a word trigger, the longer the word/short phrase is spoken, the longer the image can sit (up to the 2.0s cap). For a second trigger, lean toward ~1.5s as a neutral default.
- **How much there is to look at.** A busy image (a screenshot, a chart, a photo with detail) needs closer to 2.0s so the viewer can take it in. A simple image (a logo, an icon, a single object) can sit shorter, ~0.8–1.2s.
- **Hard cap from the video end.** If `appearance_time + duration` would run past the end of the video, shorten the duration so the image ends at the video end. Never let an image extend past the final frame.
- If two images would overlap in time, shorten the earlier one so it ends at least 0.1s before the next one starts.

## Step 3 — Place each image (sample the frame, avoid the speaker)

For each image, **sample one frame of the input video at the image's appearance time** and inspect it:
1. Locate the speaker — head and body — in that frame.
2. Mentally divide the frame's **safe content area** (see Platform safe areas below) into quadrants. Pick the quadrant that is emptiest and farthest from the speaker's head/body — usually the quadrant diagonally opposite the speaker.
3. Place the image centered in that quadrant.
4. **If the speaker fills the frame** and no quadrant is clearly clear of them, placing the image partly over the speaker is acceptable — prefer over their torso/shoulder, never over their face/eyes if it can be avoided. Speaker-overlap is the last resort, not the default.
5. The image must fall entirely inside the safe content area — never inside the bottom UI zone or the right-rail column (see below). If the chosen quadrant would push any edge of the image into a UI zone, shrink the image (Step 4) until it fits, or move it to a different safe quadrant.

## Step 4 — Image sizing (aspect-preserving, no framing)

- **No framing.** The image is placed as-is: no rounded corners, no border ring, no drop shadow, no background plate. Just the image.
- **Fit, don't stretch.** Fit the image inside a box within the chosen safe quadrant, **preserving the image's original aspect ratio** (letterbox-fit). Never stretch, squish, or crop the image to force a shape. If the image is wide and the quadrant is tall, the image simply ends up shorter; if tall, narrower.
- **Default box:** the image's longest side fits within roughly **40–45% of the frame's safe content width**, scaled down further if needed to keep it inside the quadrant and out of all UI zones. Big enough to read, small enough to leave the speaker and the rest of the frame clear.
- A subtle **pop-in animation** is fine (scale from ~0.92 to 1.0 with `back.out(2)` over ~180ms) — this is motion, not framing, so it's allowed. No fade.

## Step 5 — SFX

Every image gets exactly ONE `pop` SFX, fired at the image's appearance time (the same time as `data-start`). Pull `pop` from `sound/effects`. If several images reuse the same `pop` file, provide it as multiple `-i` inputs in the ffmpeg command, each with its own `adelay`. If two images appear within 0.5s of each other, keep only one `pop` to avoid a double-hit.

## Step 6 — Build the HyperFrames overlay

1. Build a HyperFrames slot at `{{edit_dir}}/animations/slot_images/` (scaffold with `npx --yes hyperframes init . --example blank --non-interactive --skip-skills` if missing).
2. The composition root must declare `data-width` and `data-height` matching the input video frame EXACTLY. For a 1920×3414 portrait clip: `data-width="1920" data-height="3414"`, and `<body>` `width: 1920px; height: 3414px`. A mismatch scales the overlay wrong on composite.
3. The composition root must set `data-duration="{{video_duration_s}}"` (exact, to 3 decimals). The default is 10s — anything shorter renders a black/empty MOV past 10s.
4. Each image is one element: positioned per Step 3, sized per Step 4, visible only for its Step 2 duration via a `.clip` visibility window, with the Step 4 pop-in animation.
5. Render to ProRes alpha MOV: `npx --yes hyperframes render . --format mov -f 24 -q standard -o render.mov`. **Must be `--format mov`** — WebM has no alpha and the overlay would be opaque.

## Step 7 — Composite with ffmpeg

Overlay the alpha MOV onto the input video and mix in every `pop`:
- Video: `[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v]` — applied last in the filter chain.
- Audio: mix the video's original audio with every `pop` SFX using `amix=inputs=N:normalize=0:duration=longest` so the original audio level is preserved and the track extends to the longest stream.
- Output to `{{edit_dir}}/with_images.mp4`.

## Platform safe areas (TikTok / Reels / Shorts)

NON-negotiable for vertical output. Every image overlay must sit fully inside the safe content area.

**Bottom UI zone — the bottom ~25–28% of the frame is owned by the platform** (caption, username, hashtags, music, CTA). No image may enter this strip.

**Right-rail column — the rightmost ~14% of the frame is owned by the platform** (like / comment / share / sound icons). No image may enter this column.

| Output dimension | Safe content area | Horizontal margin each side | Top margin | Bottom margin |
|---|---|---|---|---|
| 1080×1920 | 880px wide | 100px | ~115px | ~538px (28%) |
| 1920×3414 | 1570px wide | 175px | ~205px | ~956px (28%) |
| Other portrait | `0.815 × frame_w` wide | `0.0925 × frame_w` | `~0.06 × frame_h` | `0.28 × frame_h` |

Every image overlay must fit entirely within this safe content area — all four edges inside the margins, nothing in the bottom UI zone or the right-rail column.

## Self-eval before declaring done

For each image, sample one frame of the output at `appearance_time + 0.2s` (after the pop-in has settled) and check:
- The image is fully on-screen, inside the safe content area — no edge in the bottom UI zone or right-rail column.
- The image preserves its original aspect ratio — not stretched, squished, or cropped.
- The image is placed away from the speaker's face; it overlaps the speaker only if the frame left no clear quadrant, and even then never over the eyes.
- The image is on screen for its intended duration (0.8–2.0s, never more) and does not run past the end of the video.
- The `pop` SFX fires at the image's appearance, audible over the original audio.
- `ffprobe` the output: duration ≈ input video duration (within ~120ms encoder padding). Larger drift = `-shortest` truncation; check SFX placements.

If an image overflows a UI zone, shrink it or move it to another safe quadrant and re-render. If an image lands awkwardly on the speaker, try the opposite quadrant first; only accept speaker-overlap when no quadrant is clear.

## How I'll iterate

Natural-language feedback per image: *"the logo at 8s is too big"* (shrink the fit box) · *"move the screenshot off his face"* (re-sample, pick a clearer quadrant) · *"the image at 'lista' should last longer"* (extend duration toward the 2.0s cap) · *"trigger it one word later"* (re-pick the word/occurrence) · *"the pop is too loud on the second image"* (adjust that one SFX level) · *"add another image"* (re-run the Step 1 loop for just the new one).

Update the relevant image's definition and re-render. Each image lives in one place. Don't touch the input video.