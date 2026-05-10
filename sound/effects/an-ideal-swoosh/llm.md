# An ideal swoosh

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/an-ideal-swoosh/` |
| **Files** | audio.MP3 |
| **Common names** | swoosh, whoosh, transition swoosh, swipe |
| **UCS Category** | Whoosh |
| **UCS Subcategory** | Air whoosh / transition |
| **Duration variants** | Single |
| **Sonic character** | Mid-to-high air sweep with a quick attack and short tail; light high-frequency emphasis, no metallic ring. |
| **Emotional register** | Neutral motion; light, clean energy without aggression. |

## When to Use

### ✅ Core triggers
- Hard cut between two scenes or two beats in the same scene.
- Text or graphic flying onto screen.
- Camera whip-pan or fake whip-pan transition.
- Pre-roll into a reveal or punchline frame.
- Quick B-roll cut where the visual change needs reinforcement.

### ❌ Contraindications
- Slow, contemplative cuts where motion energy would feel out of place.
- Back-to-back use within a few seconds — quickly becomes monotonous.
- Heavy dramatic moments needing tension or weight, not motion.

## Placement Rules

- **Sync/hit lands:** on_cut
- **Lead-in:** start the swoosh ~150–250 ms before the cut frame so the loudest peak hits the cut.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~6–8 dB below dialogue.
- **Fade in:** none — natural attack.
- **Fade out:** let the natural tail ring out; no hard cut.
- **EQ:** no special treatment; high-pass below 80 Hz if it muds the bed.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Use sparingly — better for cuts between beats, not within dramatic moments. |
| Commentary / exposé | ✅ | Great for moving between points or quotes. |
| Before & after | ✅ | Classic use on the reveal cut. |
| Talking head / low drama | ✅ | Subtle enough to add polish without distraction. |
| Dance / trending audio | ✅ | Works on visual hits aligned to the music. |

## Audiocard

```json
{
  "sfx_id": "an_ideal_swoosh",
  "directory": "sound/effects/an-ideal-swoosh/",
  "files": ["audio.MP3"],
  "names": ["swoosh", "whoosh", "transition swoosh", "swipe"],
  "ucs_category": "Whoosh",
  "ucs_subcategory": "Air whoosh / transition",
  "emotional_register": "neutral motion",
  "sync_point": "on_cut",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 7,
  "example_visual_context": ["hard cut between scenes", "text flying in", "whip-pan transition", "B-roll cut"],
  "do_not_use_when": ["slow contemplative cuts", "back-to-back within a few seconds", "heavy dramatic moments"],
  "needs_review": false
}
```
