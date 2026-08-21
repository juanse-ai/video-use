# Trim a single-take talking head

Source: videos/explainer1Natalia/Google Chrome.mp4

## Deliver
1. Transcribe with word-level timestamps (skip if a cached transcript exists for this source).
2. Find every phrase that appears more than once. For each, keep the take with the clearest delivery / most natural pace; cut the rest.
3. Lift partial fragments out of false-start takes if they're the only clean version of a beat (e.g. lifting "Y si lo logras..." from inside a longer take that has a 5s pause and a false start in it).
4. Assemble in script order. Output to videos/Cata/C0380.MP4
5. Print a report listing each repeated phrase, which take was kept, and why.

## Style
- Cuts: tight. `pad_in=30ms`, `pad_out=80ms` per segment.
- Internal silences: scan every kept segment word-by-word. Any internal gap ≥ 400ms gets split out (segment becomes two ranges with the silence removed). Below 400ms is mid-phrase territory — leave it.
- Dramatic pauses are silences too. Cut them. Dynamic over theatrical unless I say otherwise.
- Don't cut across a word; snap every cut to a word boundary from the transcript.
- No subtitles, no overlays, no grade unless I ask.

## Critical: Scribe word-boundary drift on segment ends
ElevenLabs Scribe extends word boundaries into trailing silence on **sustained final syllables**. This is invisible from the JSON — the boundary at e.g. `aprender. [137.58–138.72]` will be 0.4–1.9s past where audio actually dies. Inside a phrase this is harmless. **At a segment end** it produces dead air that sounds unprofessional.

For every segment whose last word is sustained ("aprender", "vidas", "completamente", "acá", any long-vowel ending), open a `timeline_view` of the SOURCE around the last word and set the cut where the waveform actually goes flat — not at Scribe's boundary. Add ~80–100ms of natural decay tail; do not include the flat-line silence after.

## Self-eval before declaring done
After rendering, run `timeline_view` on the OUTPUT at:
- Every cut boundary (±1.5s window) — check for visual flash, audio spike pop
- The first 2s and **especially the last 2s** — check for dead air at the end (the most common failure mode)
- Any segment that ends on a sustained syllable

If anything looks off, fix the EDL and re-render. Don't show me the result until self-eval passes.

## How I'll iterate
I'll give natural-language feedback like "tighten the last cut", "drop beat 3", "the 'X' phrase has empty space at the end". Update `edl.json` and re-render. The EDL is the source of truth — never re-transcribe.
