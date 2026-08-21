# Prepend the branded intro (white-flash reveal)

This is a standalone tool. Its ONLY job is to attach the **"Fail Fast" branded intro** to the front of a finished video so that the intro's ending **white flash dissolves away to reveal the first frame of the video** — the white screen is *replaced by* the start of the edit. Nothing else changes: it does not re-cut, re-transcribe, caption, grade, or add SFX to the base video. The intro is the standard opener for every video from now on.

Output: `{{edit_dir}}/with_intro.mp4` — the base video with the intro prepended and the white-to-video handoff composited. The base video, its EDL, and its transcript are read-only.

## The idea (read this first)
The intro ends on a **full-screen white flash that holds**. Instead of cutting from that white to the video, the white itself **fades away to uncover the video underneath it**. Because we fade the intro's *own* white pixels down to reveal the video, the white is identical on both sides of the join — there is no seam, no black frame, and no second flash. To the viewer: the intro flashes white, and out of that white the video appears. Smooth, energetic, on-brand.

The intro's audio **impact lands on the flash** and its reverb tail rings out over the first ~1.6s of the video, bridging the cut so the sound is seamless too.

## Inputs
- **Intro asset (Cloudflare R2, with local Plan B):** the horizontal (16:9) branded opener, hosted at the public URL in `INTRO_URL` (repo `.env`). It is **fetched fresh from Cloudflare each run** (Step 0); the committed copy at `images/intro/INTRO HORIZONTAL FINAL1.mp4` stays in the repo and serves as the **offline fallback** if R2 can't be reached. Read-only from here — to change the intro, replace the object in the R2 bucket; the next run picks it up automatically.
- **Base video:** `{{path/to/video.mp4}}` — the finished edit to open with the intro. Its cut, audio, and every frame are the spine of the output; do NOT alter them (only delay them by the intro's length).

## Intro asset — measured facts (cached copy from Cloudflare; re-verified in Step 1)
- 1920×1080, 24 fps, h264 / yuv420p, stereo AAC 48 kHz, **5.083 s** (~4.87 MB). Carries a junk data stream — **drop it** (map only video + audio).
- **Visual timeline:** `0.00–3.29s` starry-black space background with the rocket + "Fail Fast" wordmark building in → `3.29–3.46s` snaps to white → `3.46–5.08s` **holds pure white** (avg luma ≈ 234).
- **Audio:** riser peaks ~0.9s → sustained bed → **IMPACT on the flash (~3.4–3.6s)** → reverb tail decaying to silence by ~5.0s.

## Transition parameters (recommended defaults; all tunable)
- `REVEAL_START = 3.46s` into the intro — the first pure-white frame; this is where the white begins to dissolve into the video. **Re-verify per Step 1** in case the asset was re-exported.
- `REVEAL_DUR = 0.25s`, ease-out — how long the white takes to clear and uncover the video. Snappier (matches the flash energy) ≈ 0.18s; softer ≈ 0.40s.
- The base video's **frame 0 is placed at output time `REVEAL_START`**, so the reveal uncovers the video's true opening (nothing is skipped).
- Keep the intro's **audio to its natural tail (~5.08s)** — it plays ~1.6s over the video's opening. The base video's audio **fades up over ~0.5s** from `REVEAL_START`. If the video opens on speech, shorten/duck the intro tail so the first words aren't buried.

## Step 0 — Resolve the intro (Cloudflare first, repo copy as Plan B)
Run the helper — it **always tries Cloudflare first** and only falls back to the committed repo copy if R2 is unreachable or returns junk:
```
INTRO="$(bash helpers/fetch_intro.sh)"   # prints the intro path to use on its LAST line
```
- **Plan A (always attempted, max effort):** downloads `INTRO_URL` (from `.env`) with retries to a **temp** file, validates it (`ffprobe`: 1920×1080 h264 + audio), then **atomically** replaces the repo cache `images/intro/INTRO HORIZONTAL FINAL1.mp4`. A failed or partial download never touches the good copy.
- **Plan B:** if Cloudflare fails/returns junk, it uses the committed repo copy and logs `[fetch-intro] … falling back` to stderr. Surface that warning to the user so they know it ran offline.
- If the helper exits non-zero, **STOP** — no usable intro (would require R2 down AND the repo copy missing/corrupt, which shouldn't happen since it's version-controlled).
- Use `"$INTRO"` (the printed path) as the intro for every step below. The file carries a junk data stream — map only video + audio.

## Step 1 — Probe and verify
1. Probe the **base video**: width, height, fps, SAR, pixel format, and color range. This is the output canvas.
2. Re-confirm the intro's white onset: measure per-frame average luma and set `REVEAL_START` to the first frame at the sustained white plateau (avg luma ≥ 233). If the asset matches the facts above, `REVEAL_START = 3.46s`.

## Step 2 — Conform the intro to the base video's canvas
- Output resolution, fps, SAR, and pixel format = the **base video's**. Convert the intro 24 fps → base fps with smooth frame-rate conversion.
- Scale the intro **crop-to-fill (cover), centered** — no black bars; the white flash must fill the frame edge-to-edge.
- The asset is the **horizontal (16:9)** intro, ideal for landscape edits. For a vertical/other-aspect target, crop-to-fill still yields a clean full-frame white flash, but the wide "Fail Fast" wordmark may crop; if that's unacceptable, use the matching vertical intro asset instead (ask the user).
- Render both the intro and the base video in the **same color range** so the white does not step in luminance across the join.

## Step 3 — Composite the white-flash reveal
Layer the conformed intro **on top of** the base video:
- Base video sits underneath, its frame 0 at output time `REVEAL_START`.
- Intro layer opacity: **1.0** for `t < REVEAL_START` (fully covers the video) → ramps **1.0 → 0.0** across `[REVEAL_START, REVEAL_START + REVEAL_DUR]` with an ease-out → **0.0** after (layer gone).
- Discard the intro **video** beyond `REVEAL_START + REVEAL_DUR` (the leftover white hold is not needed).
- Keep the intro **audio** to its natural tail; the base video's audio fades up per the parameters above. Do not click or gap at the audio join.

Net effect: the viewer sees the full intro build and flash to white; the white then dissolves over `REVEAL_DUR` to reveal the video; total added length ≈ `REVEAL_START` (~3.46s). No dead white hold.

## Self-eval before declaring done
Run `timeline_view` on the **OUTPUT** and confirm:
- **0–0.5s:** intro starts clean — no black lead-in, audio and video in sync from frame 0.
- **Around `REVEAL_START` (±0.5s):** the white → video handoff is smooth. The frame just before the reveal is full white; it dissolves to clean video. There must be **NO hard cut, NO black flash, NO second white flash, and NO jump/pop**.
- **Video opening:** the base video's true first frame is present (not skipped) and fills the frame correctly (no bars, no off-center crop).
- **Audio:** the intro impact lands on the flash and the tail rings out; the base audio rises without a click; no gap or overlap pop at the join.
- **Format:** output resolution and fps equal the base video's; total duration ≈ base duration + `REVEAL_START`.

If anything looks or sounds off, adjust the parameters and re-render. Don't show the result until self-eval passes.

## How I'll iterate
Natural-language feedback, e.g. "make the reveal snappier" → lower `REVEAL_DUR`; "hold the white a beat longer" → nudge `REVEAL_START` later or add a brief white hold; "the intro is too loud over my first line" → shorten/duck the intro audio tail; "the logo is cropped on my vertical video" → switch to fit or the vertical intro asset. Re-render only the composite — don't re-probe unless the intro asset itself changed. **New intro?** Just upload it to the R2 bucket (same object, or update `INTRO_URL` in `.env`) — the next run fetches it and re-verifies the white onset; no change to this prompt needed.
