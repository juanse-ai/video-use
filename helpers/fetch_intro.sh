#!/usr/bin/env bash
# Resolve the branded intro. Plan A: always fetch fresh from Cloudflare R2 (INTRO_URL in .env),
# trying as hard as possible (follow redirects, patient timeouts, 6 retries incl. network errors).
# Plan B: the version-controlled repo copy — used ONLY if Cloudflare is unreachable or returns junk.
#
# Safety: the download lands in a TEMP file and is validated with ffprobe BEFORE it atomically
# replaces the repo copy, so a failed/partial download can never corrupt Plan B.
#
# Prints the path of the USABLE intro on the LAST stdout line. Exit 0 if usable, 1 if neither works.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL="$REPO/images/intro/INTRO HORIZONTAL FINAL1.mp4"   # committed Plan B
URL="$(grep '^INTRO_URL=' "$REPO/.env" 2>/dev/null | cut -d= -f2- || true)"

log(){ echo "[fetch-intro] $*" >&2; }

valid(){ # $1=file → readable 1920x1080 h264 mp4 WITH an audio stream
  [ -s "$1" ] || return 1
  ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height \
      -of csv=p=0 "$1" 2>/dev/null | grep -q '^h264,1920,1080$' || return 1
  ffprobe -v error -select_streams a:0 -show_entries stream=codec_name \
      -of csv=p=0 "$1" 2>/dev/null | grep -q . || return 1
  return 0
}

if [ -n "$URL" ]; then
  tmp="$(mktemp "${TMPDIR:-/tmp}/intro.XXXXXX.mp4")"
  if curl -fL -s -o "$tmp" \
        --connect-timeout 10 --max-time 180 --retry 6 --retry-delay 2 --retry-all-errors "$URL" \
     && valid "$tmp"; then
    mv -f "$tmp" "$LOCAL"; log "Cloudflare OK — fresh intro fetched, repo cache refreshed."
  else
    log "Cloudflare FAILED or returned an invalid file — falling back to repo copy."
    rm -f "$tmp" 2>/dev/null || true
  fi
else
  log "INTRO_URL not set in .env — falling back to repo copy."
fi

# Plan B (and final validation of whatever we ended up with)
if valid "$LOCAL"; then
  echo "$LOCAL"; exit 0
fi
log "FATAL: no usable intro — Cloudflare unreachable AND repo copy missing/corrupt ($LOCAL)."
exit 1
