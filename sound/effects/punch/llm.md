# Punch

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/punch/` |
| **Files** | audio.MP3 |
| **Common names** | punch, hit, jab, impact |
| **UCS Category** | Impact |
| **UCS Subcategory** | Punch / body impact |
| **Duration variants** | Single |
| **Sonic character** | Mid-low body, fast attack, short body, minimal tail; less heavy than a damage hit, more clean and percussive. |
| **Emotional register** | Hit, decisive landing, "smack of truth." |

## When to Use

### ✅ Core triggers
- On-screen punch or hit gesture.
- Hard cut into a punchline frame.
- Emphasizing a sharp accusation or callout.
- Punctuating a kicker line or final word in a sequence.

### ❌ Contraindications
- Soft transitions or contemplative beats.
- Multiple punches stacked within a short window — desensitizes fast.
- When the moment needs weight or pain, prefer damage-hitting-punch instead.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** the attack lands exactly on the gesture/cut frame; no pre-roll.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~6 dB below dialogue.
- **Fade in:** none.
- **Fade out:** let the natural decay ring; no hard cut.
- **EQ:** preserve low-mid (100–250 Hz) for body; tame any 400 Hz mud.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ✅ | Standard for physical hits and emphatic beats. |
| Commentary / exposé | ✅ | Strong on accusations and kicker lines. |
| Before & after | ⚠️ | Works only for negatively-charged comparisons. |
| Talking head / low drama | ⚠️ | Only when the line genuinely lands hard. |
| Dance / trending audio | ⚠️ | Use on musical hits only. |

## Audiocard

```json
{
  "sfx_id": "punch",
  "directory": "sound/effects/punch/",
  "files": ["audio.MP3"],
  "names": ["punch", "hit", "jab", "impact"],
  "ucs_category": "Impact",
  "ucs_subcategory": "Punch / body impact",
  "emotional_register": "decisive landing",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 6,
  "example_visual_context": ["on-screen hit gesture", "cut into punchline", "sharp accusation", "kicker line emphasis"],
  "do_not_use_when": ["soft transitions", "stacked punches in short window", "need for heavier damage feel"],
  "needs_review": false
}
```
