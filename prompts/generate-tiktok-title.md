# Generate a viral TikTok title/caption for the finished video

Inputs (you must have all before starting):
- **Final video:** `{{edit_dir}}/final_with_titles.mp4` (or `{{path/to/source_edit.mp4}}` if titles weren't added). Just to confirm runtime + check the hook frame; you don't need to re-watch the whole thing.
- **Transcript:** `{{edit_dir}}/transcripts/{{source_basename}}.json` — word-level Scribe JSON. This is the source of truth for what's said.
- **EDL:** `{{edit_dir}}/edl.json` — to know which lines actually made it into the cut (so you don't tease a beat that got cut).

Optional:
- **Language hint:** the caption is written in the video's spoken language. Detect from `transcripts/*.json` `language_code`. Override with `--language en` if the user wants a translated caption.
- **Brand hashtags:** persistent tags the creator always uses (e.g. `#failfast`). If not supplied, omit.
- **Topic hashtags:** content-specific tags. If not supplied, generate 1–2 from the video's main theme.
- **Tone:** `personal` (default — "I/me/te" framing), `bold` (provocation, big claim), `question` (curiosity gap), or `observation` (third-person insight). Pick from material if unspecified.

Output: `{{edit_dir}}/title.txt` — single file, the final caption ready to paste into TikTok. **Every video gets a `title.txt`.** No exceptions, no fallback, no asking the user to write it themselves.

## Deliver
1. Read the packed transcript (`{{edit_dir}}/takes_packed.md` if it exists) or scan the raw JSON for what the speaker actually said. Identify:
   - **The hook beat** — the question, claim, or stake set in the first 2–3s of the cut.
   - **The payoff beat** — the punchline, advice, or reveal the video pivots around.
   - **The CTA beat** — what the speaker asks the viewer to do (if anything).
2. Write 3 caption candidates in 3 different angles. Each must be:
   - Written in the video's spoken language (default: detect from transcript).
   - ≤ 150 characters before hashtags.
   - First-line hook strong enough that the reader doesn't need to watch to feel something — but vague enough that they still want to watch.
   - Lower-case casual register by default. Capitalize ONLY for emphasis on 1 word max (e.g. `el consejo que me cambió la VIDA`).
   - Direct second-person address (`tú` / `you`) when the payoff is universal advice. Drop the second-person when the video is a personal story without a moral.

   Angles to vary across the 3 candidates:
   - **Personal voucher** — "I tried it, it worked, here's why it works for you too." Example: `estoy seguro que te la puede cambiar también a ti`.
   - **Curiosity gap** — tease the payoff without giving it away. Example: `el consejo que casi nadie aplica (y por eso fracasan)`.
   - **Bold claim / contrarian** — pick a fight with the default belief. Example: `si esperas a que tu producto sea perfecto, ya perdiste`.

3. Pick the strongest of the 3 by these tiebreakers, in order:
   - Does the first 4 words make the viewer pause-and-read? If two candidates tie, this wins.
   - Does it implicitly promise the value without spoiling it?
   - Does it feel like a HUMAN wrote it? Cut any phrase that smells like a copywriter ("descubre", "esto te va a sorprender", "no creerás", "el secreto que…"). Banned list at the bottom.
   - When in doubt, prefer the shorter one.

4. Append hashtags on a new line (or two spaces, TikTok renders both fine):
   - **Reach tags first** (1–2): `#fyp` `#parati` (Spanish) / `#fyp` `#foryou` (English). Don't stack both Spanish reach tags — pick one.
   - **Brand tag** (if supplied): exactly as the creator uses it.
   - **Topic tags** (1–2): derived from the video. Use single-word lowercase tags. Avoid generic mush like `#motivacion`, `#tips`, `#viral`. Prefer specific: `#emprendimiento`, `#producto`, `#consejo`, `#startup`, `#mvp`.
   - Total hashtags: 3–5. More than 5 looks spammy. Less than 3 leaves reach on the table.

5. Write the final caption to `{{edit_dir}}/title.txt`. One file. UTF-8. No BOM. No trailing newline beyond a single `\n`.

6. Show the user the 3 candidates and the chosen one in chat, with a one-line reason for the pick.

## Style rules
- **One emoji max, and only if it earns its place.** A 🚀 on a startup claim is fine; an emoji per phrase is spam. Default: zero emojis.
- **No quotation marks around the caption.** TikTok strips them and it reads stilted anyway.
- **No "watch till the end" / "stitch this" meta-CTAs** unless the user explicitly wants a CTA layer. The hook itself is the CTA.
- **Hashtag casing:** lowercase. `#fyp`, not `#FYP`. Camel-case only if the brand tag is camel-cased (e.g. `#FailFast` if that's the canonical form — ask if unsure).
- **Spelling:** match the speaker's register. If they say `tambien` without the accent in casual speech, the caption can drop it too. If they write formally, keep accents.
- **Honesty:** the caption must be true to what the video delivers. If the payoff is "launch before you're ready", don't promise "the secret to making millions". Mismatch tanks watch time and the algorithm punishes it.

## Banned phrases (do not use; they trigger "ad copy" pattern recognition)
- "descubre" / "discover"
- "no vas a creer" / "you won't believe"
- "el secreto que…" / "the secret to…"
- "esto te va a cambiar la vida" (verbatim — the speaker can say it in the video, but the caption should not parrot the cliché)
- "lee hasta el final" / "read till the end"
- "stitch este video" / "stitch this"
- "comenta sí si…" — except when the creator explicitly wants engagement bait

## Self-eval before writing title.txt
- Read the caption out loud. If it sounds like a Linkedin post, rewrite.
- First 4 words ≤ 25 characters total — TikTok truncates aggressively on mobile.
- Hashtags don't overlap in meaning (don't ship `#consejo` + `#tip` + `#advice`).
- The caption is in the video's language, not English-by-default.
- `title.txt` exists at the expected path and contains the caption.

## How I'll iterate
Natural-language feedback: *"more bold"*, *"drop the voucher angle, go contrarian"*, *"add #emprendimiento"*, *"shorter"*, *"english version please"*. Regenerate `title.txt` and reshow the 3-candidate list with the new constraint. Don't touch the video.

## Example (this session's video — `el-mejor-consejo`)
- Spoken language: `spa`
- Hook beat: "¿Cuál fue ese consejo que te cambió la vida?"
- Payoff beat: "si no te avergüenza la primera versión de tu producto, es porque lanzaste demasiado tarde"
- CTA beat: "vamos a ver qué dicen ustedes" (meta — first TikTok)

Three candidates that came out of running this prompt:

1. *(personal voucher)* `estoy seguro que te la puede cambiar también a ti #fyp #failfast #consejo`
2. *(curiosity gap)* `el consejo que me cambió la vida (y casi nadie aplica) #fyp #failfast #consejo`
3. *(bold claim)* `si esperas a lanzar tu producto perfecto, ya perdiste #fyp #failfast #emprendimiento`

Picked: **#3** — first 4 words `si esperas a lanzar` are short, set a stake immediately, and the payoff is the most universal. The voucher version (#1) is the user's own first instinct and works as a strong fallback; the curiosity-gap version (#2) reads slightly copywriter-y with `(y casi nadie aplica)`.

`title.txt` ships with #3.
