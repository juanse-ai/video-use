#!/usr/bin/env python3
"""Upload a finished video to YouTube via the Data API v3 (OAuth 2.0).

IMPORTANT: uploading needs OAuth 2.0 — an API key alone CANNOT upload.
First run opens a browser for one-time consent and saves a refresh token to
`youtube_token.json`; every run after that is non-interactive.

One-time setup (do once):
  1. Google Cloud Console → create/enable "YouTube Data API v3".
  2. Create an OAuth client ID of type "Desktop app" → download the JSON.
  3. Save it next to the repo .env as `youtube_client_secret.json`.
  4. First `--video ...` run pops a browser; approve → token saved.

Usage:
  python helpers/youtube_upload.py \
    --video path/to/final.mp4 \
    --title "My title" \
    --description-file path/to/description.txt \
    --tags "tag1,tag2" \
    --category 27 --privacy private --language es
"""
from __future__ import annotations
import argparse, os, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLIENT_SECRET = REPO / "youtube_client_secret.json"
TOKEN = REPO / "youtube_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly"]


def get_credentials():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN.write_text(creds.to_json())
        return creds
    if not CLIENT_SECRET.exists():
        sys.exit(
            f"ERROR: OAuth client not found at {CLIENT_SECRET}\n"
            "Uploading requires OAuth 2.0 (an API key is not enough). Create a\n"
            "'Desktop app' OAuth client in Google Cloud Console, download the JSON,\n"
            f"and save it as {CLIENT_SECRET.name}. See this file's header for steps."
        )
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0)   # one-time browser consent
    TOKEN.write_text(creds.to_json())
    print(f"  saved auth token → {TOKEN.name} (future runs are non-interactive)")
    return creds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--title", required=True)
    ap.add_argument("--description-file", type=Path, help="UTF-8 text file (include 0:00 chapter lines)")
    ap.add_argument("--description", default="", help="inline description (used if no --description-file)")
    ap.add_argument("--tags", default="", help="comma-separated")
    ap.add_argument("--category", default="27", help="YouTube categoryId (27=Education, 28=Sci/Tech, 22=People)")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    ap.add_argument("--language", default="es", help="ISO-639-1 for title/description + audio")
    ap.add_argument("--publish-at", default=None, help="ISO-8601 UTC; sets privacy=private + scheduled publish")
    ap.add_argument("--playlist", default=None, help="optional playlistId to add the video to")
    args = ap.parse_args()

    if not args.video.exists():
        sys.exit(f"ERROR: video not found: {args.video}")
    if len(args.title) > 100:
        sys.exit(f"ERROR: title is {len(args.title)} chars (YouTube max 100).")
    description = (args.description_file.read_text(encoding="utf-8")
                  if args.description_file else args.description)
    if len(description) > 5000:
        sys.exit(f"ERROR: description is {len(description)} chars (YouTube max 5000).")
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    creds = get_credentials()
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)

    status = {"privacyStatus": args.privacy, "selfDeclaredMadeForKids": False}
    if args.publish_at:
        status["privacyStatus"] = "private"
        status["publishAt"] = args.publish_at

    body = {
        "snippet": {
            "title": args.title,
            "description": description,
            "tags": tags,
            "categoryId": str(args.category),
            "defaultLanguage": args.language,
            "defaultAudioLanguage": args.language,
        },
        "status": status,
    }

    size_mb = args.video.stat().st_size / 1e6
    print(f"uploading {args.video.name} ({size_mb:.1f} MB) as [{args.privacy}] …")
    media = MediaFileUpload(str(args.video), chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    resp = None
    last = -1
    while resp is None:
        try:
            prog, resp = req.next_chunk()
            if prog:
                pct = int(prog.progress() * 100)
                if pct >= last + 5:
                    print(f"  {pct}%"); last = pct
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504):
                print(f"  transient {e.resp.status}, retrying…"); time.sleep(3); continue
            raise

    vid = resp["id"]
    url = f"https://youtu.be/{vid}"
    print(f"DONE ✅  {url}   (studio: https://studio.youtube.com/video/{vid}/edit)")

    if args.playlist:
        yt.playlistItems().insert(part="snippet", body={"snippet": {
            "playlistId": args.playlist,
            "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
        print(f"  added to playlist {args.playlist}")

    print(vid)  # last line = bare video id, easy to capture


if __name__ == "__main__":
    main()
