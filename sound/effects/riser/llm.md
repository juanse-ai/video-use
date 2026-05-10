# Riser

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/riser/` |
| **Files** | audio.MP3 |
| **Common names** | riser, build, sweep-up, tension build |
| **UCS Category** | Riser |
| **UCS Subcategory** | Forward riser, generic |
| **Duration variants** | Single |
| **Sonic character** | Broad-band rising noise/tone with increasing brightness and amplitude; ends on a peak. |
| **Emotional register** | Building tension, anticipation. |

## When to Use

### ✅ Core triggers
- Building into a reveal, twist, or punchline cut.
- Pre-roll into an impact or drop.
- Push-in zoom culminating in a beat.
- Setting up a question that will be answered or smashed.

### ❌ Contraindications
- Nothing landing after the riser — leaves the viewer hanging.
- Two risers within ~30 seconds — exhausts attention quickly.
- Light, low-stakes content — feels overblown.

## Placement Rules

- **Sync/hit lands:** pre_action
- **Lead-in:** start the riser ~1.5–2.0 s before the target cut so it peaks on the hit frame.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~8 dB below dialogue at start; swells up to ~3–4 dB below at peak.
- **Fade in:** the riser's natural envelope handles the build.
- **Fade out:** hard end on the peak/cut frame; do not bleed past.
- **EQ:** preserve top-end brightness (2–6 kHz); high-pass below 80 Hz if it clashes with music sub.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ✅ | Standard build into confrontations or reveals. |
| Commentary / exposé | ✅ | Strong setup for damning quotes or stats. |
| Before & after | ✅ | Classic build into "after" reveal. |
| Talking head / low drama | ⚠️ | Only when a real beat follows. |
| Dance / trending audio | ⚠️ | Risky unless aligned to the music build. |

## Audiocard

```json
{
  "sfx_id": "riser",
  "directory": "sound/effects/riser/",
  "files": ["audio.MP3"],
  "names": ["riser", "build", "sweep-up", "tension build"],
  "ucs_category": "Riser",
  "ucs_subcategory": "Forward riser, generic",
  "emotional_register": "tension build",
  "sync_point": "pre_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 7,
  "example_visual_context": ["build into reveal", "push-in to a beat", "set-up for impact SFX", "tension before a twist"],
  "do_not_use_when": ["nothing lands after riser", "two risers within 30 s", "low-stakes comedic beats"],
  "needs_review": false
}
```
