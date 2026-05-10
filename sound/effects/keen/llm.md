# Keen

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/keen/` |
| **Files** | audio.MP3 |
| **Common names** | keen, sharp accent, blade shimmer, sting |
| **UCS Category** | Designed |
| **UCS Subcategory** | Sharp accent / shimmer sting |
| **Duration variants** | Single |
| **Sonic character** | Bright, narrow-band high-frequency accent with quick attack and short ring; metallic shimmer quality, no bass body. |
| **Emotional register** | Sharpness, precision, focus — the visual equivalent of a glint. |

## When to Use

### ✅ Core triggers
- Eye-glint or "aha" moment in a face close-up.
- Title or kicker word snapping into place.
- Punctuating a clever observation or smart insight.
- Decorative accent on a zoom-in to a small on-screen detail.

### ❌ Contraindications
- Heavy or dramatic impacts — too thin to support weight.
- Dense music beds with bright top end — gets buried.
- Repeated use within a short span — loses its accent quality.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** start on the visual glint frame; peak should hit within 50 ms of the gesture.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~8–10 dB below dialogue; meant to be a sparkle, not a hit.
- **Fade in:** none.
- **Fade out:** let the natural ring decay.
- **EQ:** preserve the air above 6 kHz; de-ess if it competes with sibilant speech.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ✅ | Classic for eye-glint or smirk closeups. |
| Commentary / exposé | ✅ | Good accent on a sharp observation. |
| Before & after | ✅ | Sparkle on the "after" reveal works well. |
| Talking head / low drama | ✅ | Adds polish without overwhelming. |
| Dance / trending audio | ⚠️ | Easily buried unless the mix has headroom in the highs. |

## Audiocard

```json
{
  "sfx_id": "keen",
  "directory": "sound/effects/keen/",
  "files": ["audio.MP3"],
  "names": ["keen", "sharp accent", "blade shimmer", "sting"],
  "ucs_category": "Designed",
  "ucs_subcategory": "Sharp accent / shimmer sting",
  "emotional_register": "sharp / precise",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 9,
  "example_visual_context": ["eye glint close-up", "title snap-in", "smart observation kicker", "zoom on small detail"],
  "do_not_use_when": ["heavy impacts", "dense bright music beds", "repeated within short span"],
  "needs_review": false
}
```
