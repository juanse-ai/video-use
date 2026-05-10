# Pop whoosh

## Identity

| Field | Value |
|---|---|
| **Directory** | `sound/effects/pop-whoosh/` |
| **Files** | audio.MP3 |
| **Common names** | pop whoosh, swoosh-pop, transition pop, accent whoosh |
| **UCS Category** | Whoosh |
| **UCS Subcategory** | Whoosh with terminal pop / accent |
| **Duration variants** | Single |
| **Sonic character** | Short air sweep into a defined pop at the end; whoosh body builds, then snaps. |
| **Emotional register** | Energetic punctuation with a clear landing — motion that arrives. |

## When to Use

### ✅ Core triggers
- Title or kicker word flying in and snapping into place.
- Sticker, emoji, or graphic swooping onto frame.
- Quick whip-pan that lands on a specific subject.
- Pre-roll into a fast cut that itself is the punctuation.

### ❌ Contraindications
- Slow, contemplative cuts — too energetic.
- No defined landing visual — the terminal pop feels orphaned.
- Layered with another whoosh on the same beat.

## Placement Rules

- **Sync/hit lands:** on_cut
- **Lead-in:** start whoosh ~300–500 ms before the landing frame so the pop lands on the cut.
- **Short variant:** n/a
- **Medium variant:** n/a
- **Long variant:** n/a

## Mix Notes

- **Level:** ~7 dB below dialogue at the pop peak.
- **Fade in:** none — natural whoosh attack.
- **Fade out:** let the pop's tiny tail decay; do not hard-cut.
- **EQ:** high-pass below 80 Hz; preserve the pop transient.

## Genre / Content Fit

| Content type | Fit | Notes |
|---|---|---|
| Telenovela / drama narrative | ⚠️ | Use sparingly between beats. |
| Commentary / exposé | ✅ | Great for snapping in callouts and labels. |
| Before & after | ✅ | Strong on the "after" reveal arrival. |
| Talking head / low drama | ✅ | Adds polish on title pop-ins. |
| Dance / trending audio | ✅ | Fits the trending sticker-snap aesthetic. |

## Audiocard

```json
{
  "sfx_id": "pop_whoosh",
  "directory": "sound/effects/pop-whoosh/",
  "files": ["audio.MP3"],
  "names": ["pop whoosh", "swoosh-pop", "transition pop", "accent whoosh"],
  "ucs_category": "Whoosh",
  "ucs_subcategory": "Whoosh with terminal pop / accent",
  "emotional_register": "energetic arrival",
  "sync_point": "on_cut",
  "duration_variants_ms": [{"short": 0, "med": 0, "long": 0}],
  "loop": false,
  "mix_level_db_below_dialogue": 7,
  "example_visual_context": ["title snap-in", "sticker swoop", "whip-pan lands on subject", "fast cut punctuation"],
  "do_not_use_when": ["slow contemplative cuts", "no landing visual", "layered with another whoosh"],
  "needs_review": false
}
```
