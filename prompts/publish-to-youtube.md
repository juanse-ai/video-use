# Publish a finished video to YouTube (title + chapters + description, then upload)

This is a standalone tool. Its ONLY job is to take a **finished** video and put it on YouTube with good metadata: it writes a **title** that matches the content, splits the video into **chapters/sections** by what is being said at each moment, writes a **description** that fits the content, then **uploads** the file. It does NOT re-cut, re-encode, or alter the video — the file is uploaded as-is.

Output: the video live on YouTube (URL printed), plus `{{edit_dir}}/youtube/` holding the exact `title.txt`, `description.txt` (with chapters), and `tags.txt` that were used.

## ⚠️ Read first — uploading needs OAuth, not just the API key
`YOUTUBE_API_KEY` (in the repo `.env`) is enough for *reading* YouTube, but **YouTube rejects API-key auth for uploads** — `videos.insert` requires **OAuth 2.0**. So there is a **one-time** setup; after it, every future upload is truly "paste this prompt → done", no browser.

**One-time OAuth setup (do once, ~3 min):**
1. Google Cloud Console → same project as the API key → enable **YouTube Data API v3**.
2. APIs & Services → Credentials → **Create OAuth client ID** → application type **Desktop app** → download the JSON.
3. Save that JSON as **`youtube_client_secret.json`** in the repo root (next to `.env`). It is gitignored.
4. The first upload opens a browser once to approve the channel; the token is saved to `youtube_token.json` and reused forever after (auto-refreshed).

If `youtube_client_secret.json` is missing when this prompt runs, STOP and tell the user to do the 3 steps above — do not try to upload with the API key (it will fail).

## Inputs
- **Finished video:** `{{video_path}}` — e.g. `{{edit_dir}}/final.mp4` or `{{edit_dir}}/with_intro.mp4`. Uploaded as-is.
- **Transcript:** `{{edit_dir}}/transcripts/<name>.json` (word-level Scribe) and/or `{{edit_dir}}/takes_packed.md` — the source of truth for title/chapters/description. Never invent content that isn't spoken.
- **EDL (if the video was trimmed):** `{{edit_dir}}/edl.json` — needed to map transcript (source) times to the delivered video's timeline for chapters.
- **Keys/creds:** `YOUTUBE_API_KEY` in `.env` (already set); `youtube_client_secret.json` + `youtube_token.json` in the repo root (OAuth, see above).
- **Uploader:** `helpers/youtube_upload.py`.

## Step 1 — Generate the metadata from the transcript
Read the transcript (and skim a few `timeline_view` frames if useful) and produce, **in the video's spoken language**:

- **Title** — one line, **≤ 100 chars**. Concrete and content-accurate; lead with the value/topic (what the viewer learns or sees). No ALL-CAPS, no clickbait, no emoji spam (one tasteful emoji max, optional).
- **Chapters (sections)** — segment the video by topic shifts in the narration. Rules:
  - Timestamps are in the **delivered video's timeline**, not the source. If the video was trimmed, map each chosen source time → output time with the EDL (`src_to_out`, below). If the uploaded file has the **prepended intro**, add the intro offset (the reveal start, ~3.46s) to every content timestamp and make **`0:00` the intro**.
  - **First chapter MUST be `0:00`.** Use `≥ 3` chapters; each chapter **≥ 10s** long; strictly ascending. (These are YouTube's requirements for auto-chapters — violate them and chapters silently don't render.)
  - Label each chapter in 2–5 words describing that moment. Format `M:SS Label` (or `H:MM:SS` past an hour), one per line.
- **Description** — 2–4 sentence summary of what the video shows/teaches (content-accurate, the video's language), then a blank line, then the chapter list, then a blank line and 3–6 relevant hashtags. **≤ 5000 chars.**
- **Tags** — 5–12 comma-separated keywords from the actual topics.

```
src_to_out(src_t):                # map a source-time to the trimmed output timeline
  out = 0
  for r in edl.ranges:
    if src_t < r.start:  return out
    if src_t <= r.end:   return out + (src_t - r.start)
    out += (r.end - r.start)
  return out
# then, if the uploaded file includes the intro:  chapter_time = src_to_out(src_t) + intro_offset
```

Write the results to `{{edit_dir}}/youtube/title.txt`, `description.txt`, `tags.txt`.

## Step 2 — Confirm before uploading (uploading is outward-facing)
Show the user the **title, full description (with chapters), tags, and the target privacy**. Default privacy is **`private`** (or `unlisted` for sharing a link). **Never upload as `public` without explicit confirmation.** Wait for approval or edits. Apply any edits to the files.

## Step 3 — Upload
```
python helpers/youtube_upload.py \
  --video "{{video_path}}" \
  --title "$(cat {{edit_dir}}/youtube/title.txt)" \
  --description-file "{{edit_dir}}/youtube/description.txt" \
  --tags "$(cat {{edit_dir}}/youtube/tags.txt)" \
  --category 27 --privacy private --language <es|en>
```
- `--category`: 27 Education, 28 Science & Tech, 22 People & Blogs (pick by content; product/how-to → 27 or 28).
- `--language`: the video's language (sets title/description + `defaultAudioLanguage`).
- Optional: `--publish-at "2026-08-25T14:00:00Z"` to schedule; `--playlist <id>` to add to a playlist.
- Run with the repo venv python. First run opens the browser once (OAuth); after that it's silent.

## Step 4 — Report
Print the **watch URL** and the **Studio edit URL** (the helper prints both). Tell the user the privacy state and that they can flip it to public in Studio (or re-run with `--privacy public` after confirming). Confirm the chapters rendered (first line `0:00`, ≥3, ascending).

## Self-check before declaring done
- Title ≤ 100 chars; description ≤ 5000; chapters start at `0:00`, ≥ 3, each ≥ 10s, ascending, and match the delivered timeline (spot-check one against the video with `timeline_view`).
- Metadata language matches the spoken language; nothing claimed that isn't in the transcript.
- The uploaded privacy is what the user approved (never public without an explicit yes).

## How I'll iterate
"punchier title", "merge chapters 3–4", "shorter description", "make it unlisted", "schedule for Monday 9am", "add to my Tutorials playlist" → edit the `youtube/*.txt` or re-run the uploader with the changed flag. The video file is never modified; metadata edits after upload can also be pushed via a `videos.update` call or done in Studio.
