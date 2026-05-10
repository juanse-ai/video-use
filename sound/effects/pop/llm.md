# Pop

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/pop/` |
| **Files** | audio.MP3 |
| **Common names** | pop, bubble pop, button pop, snap |
| **UCS Category** | Foley |
| **UCS Subcategory** | Mouth / bubble pop |
| **Duration variants** | Single |
| **Sonic character** | Very short, mid-frequency pop with quick attack and no tail; bubbly and tight. |
| **Emotional register** | Playful, light, punctuation. |

## When to Use

### ✅ Core triggers
- A small element popping onto screen — emoji, sticker, icon, label.
- Quick scene-tag or word appearing in sync with a beat.
- Light comedic punctuation on a small action or gesture.
- Marking individual list items as they appear.

### ❌ Contraindications
- Heavy or dramatic content — too light to register.
- Large reveals — feels undersized.
- Without a clear small visual to sync to.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** start exactly on the pop frame; effectively zero pre-roll.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~9 dB below dialogue.
- **Fade in:** none.
- **Fade out:** hard end with the natural pop.
- **EQ:** no special treatment.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Only for light comedic asides. |
| Commentary / exposé | ✅ | Great for list bullets and small overlay reveals. |
| Before & after | ⚠️ | Too small for the main reveal; useful on small details. |
| Talking head / low drama | ✅ | Clean punctuation, doesn't overwhelm. |
| Dance / trending audio | ✅ | Fits the trending sticker-pop aesthetic. |

## Audiocard

```json
{
  "sfx_id": "pop",
  "directory": "sound/effects/pop/",
  "files": ["audio.MP3"],
  "names": ["pop", "bubble pop", "button pop", "snap"],
  "ucs_category": "Foley",
  "ucs_subcategory": "Mouth / bubble pop",
  "emotional_register": "playful punctuation",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 9,
  "example_visual_context": ["sticker/emoji appears", "small label pop-in", "list bullet appears", "small comedic gesture"],
  "do_not_use_when": ["heavy dramatic content", "large reveals", "no small visual to sync"],
  "needs_review": false
}
```
