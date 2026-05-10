# Money chakin

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/money-chakin/` |
| **Files** | audio.MP3 |
| **Common names** | cha-ching, cash register, money sound, sale ding |
| **UCS Category** | Foley |
| **UCS Subcategory** | Cash register / money cue |
| **Duration variants** | Single |
| **Sonic character** | Bright "cha-ching" with metallic bell tail, two-stage attack (mechanical clack + bell ring), short body. |
| **Emotional register** | Money, win, profit — playful or smug. |

## When to Use

### ✅ Core triggers
- A dollar amount or price appearing on screen.
- Comedic emphasis on someone making/losing money.
- Punctuating a sales pitch, conversion, or revenue beat.
- Visual gag where money is gained, transferred, or hinted at.

### ❌ Contraindications
- Serious financial discussion — feels mocking.
- Without money or value context — feels random.
- Repeated frequently within a clip — quickly becomes corny.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** attack lands on the frame the money/number appears or is mentioned.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~6 dB below dialogue.
- **Fade in:** none.
- **Fade out:** let the bell tail decay naturally.
- **EQ:** preserve mid-high bell shimmer; high-pass below 100 Hz if it muds the bed.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Comedic only — breaks tone otherwise. |
| Commentary / exposé | ✅ | Strong on revealing profits, costs, or cash transfers. |
| Before & after | ✅ | Great on the "after" reveal when the win is monetary. |
| Talking head / low drama | ✅ | Light comedic flag on a money-related line. |
| Dance / trending audio | ⚠️ | Works only if it lands on a musical hit. |

## Audiocard

```json
{
  "sfx_id": "money_chakin",
  "directory": "sound/effects/money-chakin/",
  "files": ["audio.MP3"],
  "names": ["cha-ching", "cash register", "money sound", "sale ding"],
  "ucs_category": "Foley",
  "ucs_subcategory": "Cash register / money cue",
  "emotional_register": "money / win",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 6,
  "example_visual_context": ["dollar amount appears", "sales conversion beat", "money gained on screen", "profit reveal"],
  "do_not_use_when": ["serious financial discussion", "no money context", "repeated within same clip"],
  "needs_review": false
}
```
