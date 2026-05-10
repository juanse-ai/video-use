# Sound Effects Library

This folder contains all sound effects available for video editing.

## Structure

Each sound effect lives in its own subfolder:

```
/sfx
  /metallic_reverse_riser
    audio.mp3
    llm.md
  /impact_boom
    audio.mp3
    llm.md
  /[effect_name]
    audio.mp3
    llm.md
```

## How to Use

1. Before placing any sound effect, read the `llm.md` inside that effect's folder.
2. The `llm.md` tells you exactly when to use it, when not to, where to place it on the timeline, and how to mix it.
3. Use `audio.mp3` as the asset path when inserting the effect into the edit.

## How to Select the Right SFX

Match the scene moment to an effect by scanning the `example_visual_context` field in each `llm.md`. If no effect fits the moment, use no sound — silence is always better than a mismatched SFX.

Never use more than one riser-type effect within 30 seconds. Never layer two SFX of the same category on the same frame unless the `llm.md` explicitly describes a pairing.