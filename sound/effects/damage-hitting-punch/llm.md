# Damage hitting punch

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/damage-hitting-punch/` |
| **Files** | 0510(16).MP3 |
| **Common names** | damage hit, heavy impact, body blow, hit punch |
| **UCS Category** | Impact |
| **UCS Subcategory** | Body / damage impact |
| **Duration variants** | Single |
| **Sonic character** | Low-mid thud with bass weight on attack, short percussive body, minimal tail; heavier and more painful than a clean punch. |
| **Emotional register** | Damage, pain, shock — emphatic and grounded. |

## When to Use

### ✅ Core triggers
- On-screen hit, slap, body impact in narrative content.
- Cutting to a damaging revelation or "ouch" moment in commentary.
- Punctuating a hostile question or accusation landing on a subject.
- Emphasizing a stat or fact that "hits hard" in exposé content.

### ❌ Contraindications
- Light comedic moments — too heavy, kills the joke.
- Soft transitions or scene-changes — feels violent and out of place.
- When the body-language on screen has no impact gesture.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** the loudest attack frame must coincide with the impact frame; no pre-roll.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~5 dB below dialogue; can sit closer when there is no concurrent speech.
- **Fade in:** none — sharp attack is the whole effect.
- **Fade out:** let the natural decay ring; do not hard-cut the tail.
- **EQ:** preserve low-mid weight (80–200 Hz); pull a small dip around 400 Hz if it muds the bed.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ✅ | Standard for physical impacts and emotional gut-punches. |
| Commentary / exposé | ✅ | Great on damaging facts or accusations. |
| Before & after | ⚠️ | Works only if the "before" frame is being negatively emphasized. |
| Talking head / low drama | ⚠️ | Use sparingly — too heavy unless the line warrants it. |
| Dance / trending audio | ❌ | Clashes with music energy. |

## Audiocard

```json
{
  "sfx_id": "damage_hitting_punch",
  "directory": "sound/effects/damage-hitting-punch/",
  "files": ["0510(16).MP3"],
  "names": ["damage hit", "heavy impact", "body blow", "hit punch"],
  "ucs_category": "Impact",
  "ucs_subcategory": "Body / damage impact",
  "emotional_register": "damage / pain",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 5,
  "example_visual_context": ["on-screen physical hit", "damaging revelation", "accusation landing", "stat that hits hard"],
  "do_not_use_when": ["light comedic moments", "soft transitions", "no impact gesture on screen"],
  "needs_review": false
}
```
