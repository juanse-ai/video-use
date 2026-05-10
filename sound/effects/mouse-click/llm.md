# Mouse click

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/mouse-click/` |
| **Files** | audio.MP3 |
| **Common names** | mouse click, click, button click, UI click |
| **UCS Category** | Foley |
| **UCS Subcategory** | Computer mouse / UI click |
| **Duration variants** | Single |
| **Sonic character** | Single short plastic click, mid-frequency, almost no tail; mechanical and dry. |
| **Emotional register** | Neutral confirmation, "selection," a small action. |

## When to Use

### ✅ Core triggers
- Cursor clicks a button, link, or UI element on screen.
- Cut to a new on-screen tab, document, or window.
- Stylized selection beat ("clicking" through choices).
- Quick punctuation on a thought "selecting" itself.

### ❌ Contraindications
- No on-screen UI or cursor — feels orphaned.
- Heavy dramatic beats — too small to register.
- Layered with another UI cue on the same frame.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** start exactly on the click frame; effectively zero pre-roll.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~10 dB below dialogue; meant to be heard, not felt.
- **Fade in:** none.
- **Fade out:** hard end with the natural click; no tail.
- **EQ:** no special treatment; high-pass below 200 Hz keeps it clean against bass.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ❌ | Too small for narrative beats. |
| Commentary / exposé | ✅ | Standard for screen-recording inserts. |
| Before & after | ⚠️ | Only when an on-screen action triggers the change. |
| Talking head / low drama | ✅ | Great for cuts to UI inserts or selections. |
| Dance / trending audio | ⚠️ | Buried in dense mixes. |

## Audiocard

```json
{
  "sfx_id": "mouse_click",
  "directory": "sound/effects/mouse-click/",
  "files": ["audio.MP3"],
  "names": ["mouse click", "click", "button click", "UI click"],
  "ucs_category": "Foley",
  "ucs_subcategory": "Computer mouse / UI click",
  "emotional_register": "neutral confirmation",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 10,
  "example_visual_context": ["cursor click on UI", "selecting an on-screen option", "tab/window change", "screen recording inserts"],
  "do_not_use_when": ["no on-screen UI", "heavy dramatic beats", "layered with another UI cue"],
  "needs_review": false
}
```
