# Overlay a full-frame cutaway video onto a video (interactive)

This is a standalone tool. Its ONLY job is to drop one or more **full-frame cutaway videos** onto an already-finished video at moments you choose, then composite the result. While a cutaway plays, it **covers the entire frame** — but the **original video's audio keeps playing underneath**, and the cutaway's own audio is **muted**. It does NOT add captions, title cards, images, or text. It does NOT re-cut or re-transcribe the base video.

Output: `{{edit_dir}}/with_cutaways.mp4` — the input video with every cutaway composited full-frame at its chosen moment, original audio continuous throughout. The input video, EDL, transcript, and insert videos are read-only.

## How a cutaway behaves
- **Visual:** for its window, the cutaway video replaces the WHOLE frame (scaled crop-to-fill — see Step 4). The base video is not visible during that window.
- **Audio:** the **original/base video's audio plays continuously** across the whole output, including under every cutaway. The cutaway's own audio track is **completely muted** — it is never heard.
- **No SFX.** This tool adds no sound effects of any kind. The only audio in the output is the base video's original audio.
- **Seam fades:** a short ~30ms video fade at the cut-in and cut-out of each cutaway so the visual transition isn't a hard pop. Audio is untouched (it's the continuous base audio) so it needs no fade.

## Inputs (you must have all before starting)
- **Base video:** `{{path/to/video.mp4}}` — the finished video to place cutaways on. Its cut and its audio are the spine of the output; do NOT modify them.
- **EDL:** `{{edit_dir}}/edl.json` — source→output time mapping for every kept range. Needed to convert word triggers into the base video's timeline.
- **Transcript:** `{{edit_dir}}/transcripts/{{source_basename}}.json` — word-level Scribe JSON of the ORIGINAL (pre-trim) source. Needed for word triggers (start and end).

## Step 1 — Collect the cutaways interactively

Do NOT assume any inserts up front. Ask the user, one cutaway at a time, in a loop. For EACH cutaway, ask the following (group them so the user can answer in one pass, but ask the end-mode follow-ups based on their choice):

1. **Relative path of the insert video.** "What is the relative path of the video you want to insert?" — accept a path relative to `{{edit_dir}}` or an absolute path. Verify the file exists and is a readable video before continuing; if not, ask again.

2. **Start trigger — a trigger word.** "Which spoken word should the cutaway START on?" Then: "Which occurrence of that word — 1st, 2nd, 3rd…?" (default: 1st). Find that occurrence in the transcript, take its source-time start, and convert to output time via the EDL (see **Word alignment**). That output time is the cutaway's `cut_in` — the moment it takes over the frame.

3. **End mode.** "How should this cutaway END? Choose one:"
   - **(a) End trigger word** — ask "Which spoken word should the cutaway END on?" and "Which occurrence?" (default: 1st). Convert that word's source-time start to output time via the EDL — that output time is the `cut_out`. The cutaway covers the frame from `cut_in` to `cut_out`, then the base video resumes.
   - **(b) Specific duration** — ask "How many seconds should the cutaway play?" `cut_out = cut_in + duration`.
   - **(c) Play the whole insert** — the cutaway plays from its chosen start point (Step 1, q5) to the end of the insert file. `cut_out = cut_in + (insert_file_duration − insert_start_point)`.

4. **Confirm the window.** Whatever the end mode, compute `cut_in` and `cut_out` and show the user: "Cutaway will cover the frame from `{cut_in}`s to `{cut_out}`s of the final video — correct?"

5. **Start point inside the insert.** "Should the insert play from its beginning (0:00), or start later?" If "from 0:00", the insert plays from its first frame. If "start later", ask "At what second of the insert file should it start?" — call this `insert_start_point` (default 0).

6. After capturing the cutaway, ask: **"Any more cutaways? (yes / no)"** If yes, loop back to question 1. If no, proceed to Step 2.

Collect all cutaways before rendering. Order them by `cut_in` once gathered.

### Word alignment (start and end triggers)
```
src_to_out(src_t):
  for r in edl.ranges:
    if r.start <= src_t <= r.end:
      return out_t_so_far + (src_t - r.start)
  # else clamp to nearest range edge
```
A trigger word's source-time start → `src_to_out` → its time in the base video's timeline.

## Step 2 — Validate and clamp each window

For each cutaway, in `cut_in` order:
- **Insert shorter than the window.** If the cutaway's window (`cut_out − cut_in`) is longer than the insert footage actually available (`insert_file_duration − insert_start_point`), the insert **ends early and the base video resumes** for the remainder. Do NOT freeze the last frame, do NOT loop. The effective `cut_out` becomes `cut_in + (insert_file_duration − insert_start_point)`. Tell the user this happened.
- **Window past the end of the base video.** If `cut_out` exceeds the base video duration, clamp `cut_out` to the base video end.
- **Overlapping cutaways.** If two cutaways overlap in time, shorten the earlier one so its `cut_out` is at least 0.1s before the next one's `cut_in`, and tell the user.

## Step 3 — Seam fades

At each cutaway's `cut_in` and `cut_out`, apply a **~30ms video fade** (cross or dip) so the visual handoff between base and cutaway isn't a hard cut-pop. Audio is the continuous base track and is NOT faded or interrupted at the seams. No SFX, no audio ducking — the base audio simply plays straight through.

## Step 4 — Scale each insert crop-to-fill

Each insert video must cover the **entire output frame**. If the insert's aspect ratio differs from the base video's:
- **Crop-to-fill.** Scale the insert so it fully covers the output frame, preserving the insert's aspect ratio, then crop the overflow. No letterbox bars, no distortion. A landscape insert into a portrait frame is scaled up until it fills the height/width and the sides are cropped; center the crop unless the user later asks otherwise.
- The insert must end up exactly `{base_frame_w}×{base_frame_h}`.

## Step 5 — Build the cutaway composition

This tool composites in ffmpeg directly — the cutaways are full-frame video segments, not an alpha overlay, so HyperFrames is not needed.

For each cutaway, prepare a trimmed, scaled, muted segment of the insert:
- Trim the insert from `insert_start_point` for the effective window length.
- Scale + crop-to-fill to the base frame size (Step 4).
- Drop the insert's audio entirely (`-an` on that input, or do not map its audio).

## Step 6 — Composite with ffmpeg

Build a single ffmpeg command that:
- Takes the base video as input 0 and each insert as a further input.
- For each cutaway, uses an `overlay` enabled only for its `[cut_in, cut_out]` window (`overlay=...:enable='between(t,cut_in,cut_out)'`), or equivalently splits the base timeline and concatenates base/insert segments — either approach is fine as long as the cutaway fully covers the frame for exactly its window.
- Applies the ~30ms seam fades at each window edge.
- **Audio: maps ONLY the base video's audio** to the output, untouched and continuous. No insert audio is mapped. No SFX. The output audio is exactly the base video's audio.
- Output to `{{edit_dir}}/with_cutaways.mp4`.

## Platform safe areas

Because cutaways are **full-frame**, there is no overlay-margin question for the cutaway itself — it covers everything by design. But note: any platform UI (caption bar, right-rail icons) will sit on top of the cutaway just as it sits on the base video. If a cutaway contains its own text or important detail near the frame edges, that detail may be obscured by TikTok/Reels/Shorts UI. This tool does not move or rescale the cutaway to dodge UI — if the user flags it, the fix is to pick a different insert or accept it. Just be aware and mention it if a cutaway clearly has edge text.

## Self-eval before declaring done

For each cutaway, sample frames of the output and check:
- At `cut_in + 0.2s`: the cutaway fully covers the frame — no slice of the base video showing at any edge (crop-to-fill worked).
- At `cut_in − 0.1s` and `cut_out + 0.1s`: the base video is showing — the cutaway is present ONLY within its window.
- The insert is not distorted or stretched — aspect ratio preserved, overflow cropped.
- If the insert was shorter than the window, the base video correctly resumed at the early `cut_out`.
- **Audio:** play across each seam — the base audio is continuous and uninterrupted through `cut_in` and `cut_out`, and NONE of the insert's audio is audible at any point.
- The ~30ms seam fades are present (no hard visual pop at the edges).
- `ffprobe` the output: duration ≈ base video duration (within ~120ms encoder padding) — a cutaway must not change the total length.

If a cutaway shows base video at an edge, the crop-to-fill scale was too small — recompute and re-render. If insert audio is audible, the insert's audio stream was mapped — drop it and re-render.

## How I'll iterate

Natural-language feedback per cutaway: *"start the cutaway one word later"* (re-pick the start word/occurrence) · *"end it on 'entonces' instead"* (switch to end-trigger mode with that word) · *"make the cutaway 2 seconds shorter"* (switch to duration mode or trim it) · *"the insert starts too early — begin it at 0:05"* (raise `insert_start_point`) · *"the crop is cutting off the left side — crop from the right"* (shift the crop center) · *"add another cutaway"* (re-run the Step 1 loop for just the new one).

Update the relevant cutaway's definition and re-render. Each cutaway lives in one place. Don't touch the base video's cut or audio.