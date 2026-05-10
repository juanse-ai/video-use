# Metalic reverse riser

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/metalic-reverse-riser/` |
| **Files** | audio.MP3 |
| **Common names** | reverse riser, suck-back, pre-hit pull, metallic uppercut tail |
| **UCS Category** | Riser |
| **UCS Subcategory** | Reverse / pre-hit riser, metallic |
| **Duration variants** | Single |
| **Sonic character** | Reverse-shaped envelope (swells in, ends abruptly), metallic high-mid resonance, no decay tail — it disappears at the hit. |
| **Emotional register** | Anticipation, "pull-in" tension before a reveal. |

## When to Use

### ✅ Core triggers
- Building into a cut, reveal, or punchline frame.
- Pre-rolling a title card or chyron pop.
- Pulling the viewer into a zoom-in or push-in shot.
- Setting up a punch, impact, or "drop" SFX on the following frame.

### ❌ Contraindications
- Without a hit or visual change on the landing frame — feels unresolved.
- Layered with a forward riser — phase-clashes and double-builds.
- Slow narrative cuts where no anticipation is needed.

## Placement Rules

- **Sync/hit lands:** pre_action
- **Lead-in:** start the riser ~1.0–1.5 s before the cut so the envelope peaks exactly on the cut frame.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~7 dB below dialogue; can swell up to ~4 dB below at the peak.
- **Fade in:** the riser's natural reverse envelope handles this.
- **Fade out:** hard end on the cut frame.
- **EQ:** keep the metallic mid-band intact (1–4 kHz); tame any harshness above 8 kHz if it stings.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ✅ | Sets up reveals and confrontations cleanly. |
| Commentary / exposé | ✅ | Strong build into a damning fact or twist. |
| Before & after | ✅ | Classic pre-roll into the "after" reveal. |
| Talking head / low drama | ⚠️ | Use only when a real beat lands afterward. |
| Dance / trending audio | ⚠️ | Only if it can sit on the off-beat into a drop. |

## Audiocard

```json
{
  "sfx_id": "metalic_reverse_riser",
  "directory": "sound/effects/metalic-reverse-riser/",
  "files": ["audio.MP3"],
  "names": ["reverse riser", "suck-back", "pre-hit pull", "metallic uppercut tail"],
  "ucs_category": "Riser",
  "ucs_subcategory": "Reverse / pre-hit riser, metallic",
  "emotional_register": "anticipation",
  "sync_point": "pre_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 7,
  "example_visual_context": ["pre-roll into reveal", "build into title card", "pre-cut to punchline", "set-up for impact SFX"],
  "do_not_use_when": ["no hit on landing frame", "layered with forward riser", "slow narrative cuts"],
  "needs_review": false
}
```
