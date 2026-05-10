# Censor beep

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/censor-beep/` |
| **Files** | audio.MP3 |
| **Common names** | censor, bleep, profanity beep, TV beep |
| **UCS Category** | UI |
| **UCS Subcategory** | Censor / broadcast tone |
| **Duration variants** | Single |
| **Sonic character** | Steady mid-frequency sine-like tone (~1 kHz), constant amplitude, no decay until cut. |
| **Emotional register** | Comedic flag, broadcast warning, mock formality. |

## When to Use

### ✅ Core triggers
- Covering a profanity, slur, or sensitive word in dialogue.
- Comedic blanking out of a name, brand, or reveal.
- Faux-broadcast moment that needs a "TV-edit" feel.
- Hiding a number, password, or private detail on screen for humor.

### ❌ Contraindications
- Serious documentary or news contexts where the bleep would feel mocking.
- Replacing words that don't need censoring — loses impact fast.
- Over a song or music bed where the tone clashes harmonically.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** start exactly on the syllable being censored; end exactly when the word ends.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** match or slightly exceed the censored word's loudness so it fully masks; typically ~4–6 dB below dialogue average.
- **Fade in:** none — hard start.
- **Fade out:** hard cut at end of word.
- **EQ:** no treatment; the tone is intentionally clinical.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Only for comedic beats; breaks immersion otherwise. |
| Commentary / exposé | ✅ | Standard for masking names, profanity, or sensitive info. |
| Before & after | ❌ | Rarely applicable. |
| Talking head / low drama | ✅ | Common comedic device for sharp cuts. |
| Dance / trending audio | ⚠️ | Works only if the beat allows a clean tone overlay. |

## Audiocard

```json
{
  "sfx_id": "censor_beep",
  "directory": "sound/effects/censor-beep/",
  "files": ["audio.MP3"],
  "names": ["censor", "bleep", "profanity beep", "TV beep"],
  "ucs_category": "UI",
  "ucs_subcategory": "Censor / broadcast tone",
  "emotional_register": "comedic flag",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 5,
  "example_visual_context": ["profanity in dialogue", "blanking out a name on screen", "faux TV-edit moment", "hiding a number for humor"],
  "do_not_use_when": ["serious documentary", "no actual word to mask", "harmonic clash with music"],
  "needs_review": false
}
```
