# Wrong answer

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/wrong-answer/` |
| **Files** | audio.MP3 |
| **Common names** | wrong answer, buzzer, game-show fail, incorrect |
| **UCS Category** | UI |
| **UCS Subcategory** | Negative game-show buzzer / fail tone |
| **Duration variants** | Single |
| **Sonic character** | Low-mid buzzer tone, slightly dissonant, blunt attack and quick decay; unambiguously "no." |
| **Emotional register** | Negation, mistake, "wrong" — comedic or judgmental. |

## When to Use

### ✅ Core triggers
- A statement is shown to be wrong, false, or refuted.
- Comedic "no" beat on a failed attempt or misguided guess.
- Punctuating a contradiction between what was claimed and what is true.
- Marking an item as incorrect in an on-screen list or quiz.

### ❌ Contraindications
- Serious factual rebuttals where the buzzer would feel mocking.
- Sympathetic moments — implies the subject is being mocked.
- Repeated within the same clip — wears thin fast.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** attack lands exactly on the "wrong" frame or refutation moment.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~6 dB below dialogue.
- **Fade in:** none — abrupt start.
- **Fade out:** let the short tail decay naturally.
- **EQ:** no special treatment; tame harshness around 2–3 kHz if it pierces.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Comedic only — breaks tone otherwise. |
| Commentary / exposé | ✅ | Standard on refuted claims and contradictions. |
| Before & after | ⚠️ | Only when "before" is being mocked. |
| Talking head / low drama | ✅ | Comedic punctuation on a misstep. |
| Dance / trending audio | ⚠️ | Works on musical hits only. |

## Audiocard

```json
{
  "sfx_id": "wrong_answer",
  "directory": "sound/effects/wrong-answer/",
  "files": ["audio.MP3"],
  "names": ["wrong answer", "buzzer", "game-show fail", "incorrect"],
  "ucs_category": "UI",
  "ucs_subcategory": "Negative game-show buzzer / fail tone",
  "emotional_register": "negation / mistake",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 6,
  "example_visual_context": ["claim shown to be false", "failed attempt or guess", "contradiction reveal", "incorrect quiz item"],
  "do_not_use_when": ["serious factual rebuttals", "sympathetic moments", "repeated within same clip"],
  "needs_review": false
}
```
