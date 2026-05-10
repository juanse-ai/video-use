# Microwave oven clin

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/microwave-oven-clin/` |
| **Files** | audio.MP3 |
| **Common names** | microwave ding, oven done, kitchen ding, ready chime |
| **UCS Category** | UI |
| **UCS Subcategory** | Appliance / done chime |
| **Duration variants** | Single |
| **Sonic character** | Single bright sine-like chime, mid-high pitched, short ring with quick decay; clean and unambiguously "done." |
| **Emotional register** | Completion, "ready," lightly comedic finality. |

## When to Use

### ✅ Core triggers
- Comedic "done" beat on a reveal — finished, served, ready.
- Punctuating the completion of a task or transformation on screen.
- Cooking, food, or kitchen-context videos when a thing is ready.
- Mock-formal "ding!" on a smart conclusion or insight.

### ❌ Contraindications
- Serious, dramatic, or somber content — feels flippant.
- When there is no completion or "done" beat being shown.
- Layered with other UI chimes — fights for the same ear.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** start exactly on the "done" frame; the attack is the hit.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~7 dB below dialogue.
- **Fade in:** none.
- **Fade out:** let the natural ring decay; do not hard-cut.
- **EQ:** no special treatment; de-ess if it clashes with sibilants.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Only for comedic beats. |
| Commentary / exposé | ✅ | Great punctuation on a "case closed" moment. |
| Before & after | ✅ | Classic ring on the "after" reveal. |
| Talking head / low drama | ✅ | Light, friendly button on a punchline. |
| Dance / trending audio | ⚠️ | Works only if the chime sits on a musical beat. |

## Audiocard

```json
{
  "sfx_id": "microwave_oven_clin",
  "directory": "sound/effects/microwave-oven-clin/",
  "files": ["audio.MP3"],
  "names": ["microwave ding", "oven done", "kitchen ding", "ready chime"],
  "ucs_category": "UI",
  "ucs_subcategory": "Appliance / done chime",
  "emotional_register": "completion / comedic finality",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 7,
  "example_visual_context": ["comedic done beat", "task complete on screen", "food ready", "case closed punchline"],
  "do_not_use_when": ["serious dramatic moments", "no completion beat", "layered with other UI chimes"],
  "needs_review": false
}
```
