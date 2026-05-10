# Ping

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/ping/` |
| **Files** | audio.MP3 |
| **Common names** | ping, notification, message ding, alert |
| **UCS Category** | UI |
| **UCS Subcategory** | Notification / alert chime |
| **Duration variants** | Single |
| **Sonic character** | Clean mid-high tonal chime, slight bell quality, medium tail; friendly, not alarming. |
| **Emotional register** | Attention call, "look here," friendly notification. |

## When to Use

### ✅ Core triggers
- Notification, text, or DM popping on screen.
- A small fact, stat, or callout appearing as an overlay.
- Stylized "ding!" on a thought or realization.
- Marking a point in a numbered or bulleted on-screen list.

### ❌ Contraindications
- Serious or heavy dramatic moments — feels too light.
- Without a corresponding visual element to ping — feels random.
- Multiple pings in quick succession unless the visuals match exactly.

## Placement Rules

- **Sync/hit lands:** on_action
- **Lead-in:** start exactly on the frame the element appears.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~8 dB below dialogue.
- **Fade in:** none.
- **Fade out:** let the natural tail ring.
- **EQ:** no special treatment.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Only on actual on-screen notifications. |
| Commentary / exposé | ✅ | Great for fact callouts and list bullets. |
| Before & after | ⚠️ | Only if an info bubble accompanies the reveal. |
| Talking head / low drama | ✅ | Clean punctuation on a callout. |
| Dance / trending audio | ⚠️ | Easily buried; use only if the mix has space. |

## Audiocard

```json
{
  "sfx_id": "ping",
  "directory": "sound/effects/ping/",
  "files": ["audio.MP3"],
  "names": ["ping", "notification", "message ding", "alert"],
  "ucs_category": "UI",
  "ucs_subcategory": "Notification / alert chime",
  "emotional_register": "attention call",
  "sync_point": "on_action",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 8,
  "example_visual_context": ["notification appears", "fact callout overlay", "numbered list bullet", "realization beat"],
  "do_not_use_when": ["heavy dramatic moments", "no on-screen element to ping", "rapid succession without matching visuals"],
  "needs_review": false
}
```
