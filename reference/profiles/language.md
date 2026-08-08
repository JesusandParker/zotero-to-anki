# Language profile

For Arabic, Spanish, and Mandarin study materials — textbooks, workbooks, graded readers.

Language is the profile that departs most from the rest of the pipeline, because the goal
is **production under time pressure**, not recognition of a fact. Read this before
drafting; the universal rules in `card-rules.md` still bind, but several defaults flip.

---

## 1. What it's for
Reaching working fluency (~B2) — understanding and *producing* the language, not passing a
quiz about it. The test is a conversation, not a multiple-choice item.

## 2. Archetype mix
- ~45% vocabulary (word ↔ meaning, two-way — see below for the direction rule)
- ~20% morphology and patterns (verb forms, plurals, agreement, Arabic root patterns)
- ~15% grammar rules stated as a usable trigger ("when do you use X")
- ~10% fixed phrases / collocations / idioms, kept whole
- ~10% script, orthography, pronunciation

## 3. Direction is the whole game
`parker-preferences.md` makes definitions two-way by default, and for language that
default is **more** important, not less — but the two directions are not equal:

- **Recognition** (see the word → give the meaning) is the easy direction and comes free
  from reading.
- **Production** (see the meaning → produce the word) is the one that actually builds
  fluency and the one he'll fail without.

So: two-way by default, and when only one direction is affordable, **keep production**.
Do NOT two-way a fixed phrase, an example sentence, or a grammar rule.

## 4. Script, diacritics, and RTL
- **Arabic is right-to-left.** Never mix an RTL span and a Latin span inside one cloze — the
  rendering is unpredictable in Anki. Keep the Arabic on its own line; put the English on
  another line.
- **Vowel marks (harakat) are meaningful.** If the textbook prints them, keep them: the
  unvowelled form is a different, harder card and shouldn't be created by accident. If a
  card is specifically *about* vowelling, say so in the stem.
- **Never cloze a bare letter** unless the card is teaching that letter's form. A one-glyph
  blank is unanswerable in a shuffled deck.
- Check any Arabic card renders correctly in Anki the first time — the same one-time visual
  confirmation the MathJax cards got (`note-format.md`).

## 5. Traps
- **A dictionary gloss is not a definition.** "kataba = to write" is fine; "kataba = to
  write, to compose, to draft, to record, to inscribe" is five cards' worth of fuzz under
  one blank and fails the crisp-cloze rule (card-rules #5, R12). Pick the core sense; put
  the others in `Back Extra` under `Meaning:`.
- **Don't card a paradigm as one giant list.** A full verb conjugation table is a
  grouped-list card only if Parker genuinely memorizes it as one unit; otherwise it's the
  *pattern* that's worth a card, with the table in `Back Extra`.
- **Cognates and false friends need a `Distinguish:` line** — that's exactly what the field
  is for.
- **Don't invent example sentences.** Ground every example in the textbook page like any
  other claim (card-rules #10). If the book didn't give one, don't fabricate one.

## 6. The purple lane in a language source
A purple word here is vocabulary Parker met and couldn't read — which is this profile's
CORE material, so §3's direction rule OVERRIDES §4b's one-way default: **two-way by
default, and when only one direction is affordable, keep PRODUCTION** (meaning → word).
The gloss is still authored-plain (card-rules #28) and still crisp — the §5 trap above
("a dictionary gloss is not a definition") applies with full force. Keep the script rules
(§4) for the term side; the `Ex:` line carries the sentence he met it in, per §4b.
