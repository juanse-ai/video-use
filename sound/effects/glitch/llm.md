# Glitch

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/glitch/` |
| **Files** | audio.MP3 |
| **Common names** | glitch, digital glitch, error stutter, datamosh |
| **UCS Category** | Designed |
| **UCS Subcategory** | Digital glitch / artifact |
| **Duration variants** | Single |
| **Sonic character** | Stuttered digital fragments, bit-crushed noise bursts, fast amplitude jumps; high-frequency content with no melodic pitch. |
| **Emotional register** | Disruption, malfunction, tension, "something is wrong." |

## When to Use

### ✅ Core triggers
- Hard cut paired with a visual glitch, datamosh, or RGB-split effect.
- Punctuating a reveal of a lie, error, or contradiction.
- Transition between two opposing or jarring ideas.
- Introducing a meme insert, on-screen error, or "system corrupted" moment.

### ❌ Contraindications
- Calm, narrative, or emotional sequences — destroys mood.
- Without any corresponding visual disruption — feels random.
- Layered with another riser or whoosh on the same frame.

## Placement Rules

- **Sync/hit lands:** on_cut
- **Lead-in:** start glitch on the cut frame; do not pre-roll, the disruption *is* the cut.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~6 dB below dialogue; can sit louder during music-only frames.
- **Fade in:** none — abrupt start.
- **Fade out:** hard cut on exit frame, or let trail into next cue if intentional.
- **EQ:** high-pass at ~100 Hz to keep it from competing with bass; preserve the rough top end.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Use only for "lie exposed" or "fracture" moments. |
| Commentary / exposé | ✅ | Strong on contradictions, lies, or "system error" reveals. |
| Before & after | ⚠️ | Works if the transition itself is the dramatic break. |
| Talking head / low drama | ⚠️ | Too aggressive unless the content is overtly disruptive. |
| Dance / trending audio | ✅ | Fits trending edit aesthetics with glitch visuals. |

## Audiocard

```json
{
  "sfx_id": "glitch",
  "directory": "sound/effects/glitch/",
  "files": ["audio.MP3"],
  "names": ["glitch", "digital glitch", "error stutter", "datamosh"],
  "ucs_category": "Designed",
  "ucs_subcategory": "Digital glitch / artifact",
  "emotional_register": "disruption / malfunction",
  "sync_point": "on_cut",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 6,
  "example_visual_context": ["visual glitch effect", "RGB split cut", "lie or contradiction reveal", "system error overlay"],
  "do_not_use_when": ["calm narrative beats", "no visual disruption", "layered with another riser or whoosh"],
  "needs_review": false
}
```
