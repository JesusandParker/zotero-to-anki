---
name: zotero-to-anki
description: Turn anything Parker marks in YELLOW in Zotero into excellent Anki cloze cards — any textbook, lecture PDF, or paper. Use (1) to GENERATE cards when he points at a source ("make cards from chapter 6 of my EMT book", "I finished highlighting the Arabic unit", "make cards from this genetics lecture", "I highlighted something in that PowerPoint I want to memorize"), AND (2) to REGISTER a new source he hasn't used before ("add my organic chem textbook", "point this at my Arabic book"), AND (3) to FIX/REVIEW/IMPROVE existing cards or the card-maker itself when he reports a problem while studying ("I noticed an issue with a card", "this flashcard is wrong / the hint gives it away", "fix the card maker", "the cards keep doing X"), AND (4) to BATCH-PROCESS the complaints he types into the hidden "Card Feedback" field during review ("go look at my card feedback", "process my complaints", "go through the cards I ranted about", "harvest my Anki feedback"). On any single-card issue follow the "If Parker reports an issue" procedure below; for a batch, follow "Processing card feedback (batch)".
---

# Zotero → Anki

Parker marks what he wants to memorize in **yellow** while he reads. This turns those marks
into Anki cloze cards: grounded in the real page text, quality-checked by an adversarial
editor and a deterministic gate, and staged into a review deck he approves.

It works on **any source registered in `reference/sources.json`** — the EMT textbook it was
built on, an Arabic textbook, a genetics lecture PDF, a paper. Which PDF, which colors,
which page→segment map, which Anki deck, and which subject profile all come from the
registry. Nothing in the pipeline is specific to one book.

**The yellow mark is Parker's "this matters" signal — he has already decided what's
important. Your job is to turn it into the best possible card(s), not to re-decide
importance.**

## Three rules that override everything

1. **Always ground in the page paragraph.** Never write a card from the bare marked
   sentence. Use the `context` paragraph the extractor provides. Every claim on a card must
   be supported by that context. (This is what keeps cards correct instead of hallucinated.)
2. **Zero guessing.** If the context is too thin, ambiguous, or the mark didn't locate
   (`grounding: NOT_FOUND`), do NOT invent. Flag it for Parker. Especially for any number,
   dose, or threshold.
3. **Nothing is final.** Everything lands in the source's **staging deck**. Parker reviews,
   edits, and PROMOTES keepers into the sibling deck himself. You stage; he commits.

## Priority order when rules collide
**(1)** correct cloze formatting + reliable write to Anki, **(2)** completeness/coverage of
testable facts, **(3)** standalone atomicity, **(4)** a teachable Back Extra, **(5)**
readability/aesthetics, **(6)** speed — dead last. Parker will gladly wait for better cards;
never trade 1–5 for speed.

---

## Sources: what you can point at

```
python3 scripts/sources.py list          # every registered source
python3 scripts/sources.py show <id>     # one source, fully resolved
python3 scripts/sources.py segments <id> # its chapter/unit map
```

A source entry holds: the Zotero attachment key, the "card me" colors, an optional
page→segment map, the Anki deck templates, the tags, and the **subject profile**. Field
reference: `reference/sources.md`.

### What counts as "card me"
**Color decides, not markup style.** Parker highlights in textbooks but *underlines* on
lecture slides, and both mean the same thing to him. The extractor reads yellow (`#ffd400`
and the alternate-palette `#facd5a`) across:

| Zotero markup | Extractor `kind` | What to do with it |
|---|---|---|
| highlight, underline | `text` | Normal grounded card. The main path. |
| area selection | `image` | The figure IS the card — crop it and author from the image. |
| standalone note | `note` | Parker's OWN words, no source span. Ground it before carding, or flag it. |
| sticky note, ink | *(skipped)* | No cardable content. |

Any other color is deliberately ignored — blue is his ordinary reading emphasis, and on
lecture slides red often means *"not on the exam."*

### Registering a new source (the first-run flow)
When Parker points at something not in the registry:

1. **Find it:** `python3 scripts/add_source.py --search "<title words>"` — shows the Zotero
   key, file type, and what's marked in it. Confirm you have the right item; his library
   holds near-duplicate copies of several books.
2. **Propose the deck.** Read his live tree — `python3 scripts/add_source.py --decks all` —
   and propose a path that *fits his existing conventions* rather than inventing a new
   shape. **Ask him once, and only once.** Once he confirms, it's saved forever.
3. **Segment it, if it's a book.** Dump the printed contents pages and read them:
   ```
   python3 scripts/add_source.py --toc-pages 7-11 --key <KEY>
   ```
   Then write the map (page numbers must be PHYSICAL PDF pages — use `--offset` when the
   printed numbers differ from the PDF's):
   ```
   echo '[{"n":1,"name":"...","start":12,"end":40}]' | \
     python3 scripts/add_source.py --write-map <id> --noun Chapter --offset 0
   ```
   A lecture or paper needs no map — it's addressed whole.
4. **Register it:**
   ```
   python3 scripts/add_source.py --add --id <id> --key <KEY> --label "..." \
     --kind textbook|lecture --deck-root "<confirmed deck>" \
     --profile emt|science|language|default
   ```
5. **Verify:** `python3 scripts/sources.py show <id>`, then extract.

**Fail loudly, don't guess:** if the attachment isn't a real PDF (Zotero's stored
contentType lies — one of his lecture files is a PPTX labeled `application/pdf`), the
extractor stops with the fix. Don't work around it.

---

## If Parker reports an issue with a card (his main ongoing loop — START HERE)

Once cards exist, this is the primary use. A fresh session with NO memory of past work can
do this end-to-end from this skill alone. When he says *"I noticed an issue with a card,"*
*"the hint gives it away,"* *"this card is wrong":*

1. **Read the standards first** — `reference/regression-cases.md` (every flaw caught before
   + how it's caught; his issue is usually a known class), then `reference/card-rules.md`
   and `reference/parker-preferences.md`.
2. **Find the card** — in Anki via AnkiConnect at `localhost:8765` (Anki must be running;
   search by a distinctive phrase) and in the source's `work/<source>/*_cards.json`.
   - **To sweep the whole class mechanically, audit the LIVE deck:**
     `python3 scripts/check_cards.py --live <N|all> --source <id>`. This runs the
     deterministic gate against the cards as they actually exist in Anki — the only way to
     catch defects that entered by hand-editing (Parker edits on Mac and iPhone), which
     never pass back through the file gate. Diagnostic only; it never writes or stamps.
3. **Diagnose honestly — one-off or systemic?** If it's a *kind* of mistake (not a typo),
   assume systemic: the rules would let it recur, so fix the rules, not just the card.
4. **Fix the card(s)** in Anki and in the JSON.
5. **If systemic:** encode the rule (`card-rules.md` / `editor-checklist.md` /
   `parker-preferences.md`, or the source's `profiles/<name>.md` if it's subject-specific),
   AND add a case to `reference/regression-cases.md` (a BAD card the checks must catch + a
   GOOD card they must NOT over-flag), AND extend `scripts/check_cards.py` if it can be
   mechanized.
6. **Re-verify:** run `python3 scripts/check_cards.py work/<source>/<file>.json` and
   `python3 scripts/test_regressions.py` — the regression library is executable and must
   stay green in both directions: catch the bad, spare the good.
7. **Log it** in `reference/feedback-log.md` (date, source, what he flagged, the fix, the
   rule/test added).
8. **Commit + push** per `CLAUDE.md`.

Be honest about one-off vs systemic, and never over-correct — the regression suite's "don't
over-flag" cases are the guard against swinging too far.

## Processing card feedback (batch) — "go look at my complaints"

Parker leaves complaints *while studying* by typing into a hidden **`Card Feedback`** field
via Anki's **Edit** button — it never shows during review but stays attached to the exact
card, on Mac and iPhone. This is the batch front-door to the loop above, and it spans every
source plus his Liberty course cards.

1. **Harvest** (Anki must be running):
   ```
   python3 scripts/feedback_harvest.py
   ```
   Lists every note with a non-empty `Card Feedback` and writes
   `work/feedback_inbox_<date>.json`. Read it. Non-empty = unprocessed.
2. **Process each item** with the procedure above. Route by the card's deck:
   - *Card-craft* issues (leaky hint, under-clozing, phrasing, formatting) → the shared
     `reference/` canon here, whatever the subject. This is the home of card craft.
   - *Subject-emphasis* issues ("stop making scenario cards for legal definitions") → the
     relevant `reference/profiles/<name>.md`.
   - A **Liberty course deck** card whose complaint is about *selection/scoring* ("this
     shouldn't exist", "you missed the real testable fact") → also route to `course-to-anki`
     per its feedback loop (adjust `scripts/score.py` weights or the pass prompts, and log why).
3. **Write back** — one small JSON batch does fixes and clears together:
   ```
   python3 scripts/feedback_harvest.py --apply fixes.json
   ```
   where `fixes.json` is a list of `{"noteId": …, "fields": {"Text": "…", "Back Extra": "…"},
   "clear_feedback": true}`. (Or `--clear <noteId> …` when the card just needed logging.)
4. **Log every item** in `reference/feedback-log.md` — the permanent history. The field is
   only the transient inbox.
5. **Clear a card's feedback ONLY after it's logged** — a non-empty `Card Feedback` must
   always mean "still unprocessed," so nothing is ever lost.
6. Re-run the checker and `test_regressions.py` if you touched any rule, then **commit +
   push**, and remind Parker to **sync** (his cards live on his phone too).

The `Card Feedback` field is **hidden + human-only**: the generator must never write into it.

---

## The pipeline

Work **one segment at a time** (a chapter, a unit, or a whole lecture), and within it, **one
marked item at a time**. Parker explicitly wants this blocked, focused approach.

### Stage 0 — Know the subject
Open the source's profile (`reference/profiles/<name>.md`, named in the registry). It says
what the material is *for*, which archetypes should dominate, and the subject's traps. The
universal card craft is unchanged; the profile is only the emphasis.

### Stage 1 — Extract (once per segment)
```
python3 scripts/extract_highlights.py --source <id> --segment <N>     # a mapped book
python3 scripts/extract_highlights.py --source <id>                   # a flat lecture/paper
python3 scripts/extract_highlights.py --source <id> --pages 515-680   # an explicit range
```
Writes `work/<source>/<label>_highlights.json` (marked items + grounded `context` + page +
`kind` + any margin `user_comment` + a `list_lead_in` flag). Read it.

- **`list_lead_in: true`** marks an item that introduces an enumerated list. The extractor
  widens its context and pulls the next page, but you MUST still read the whole list off the
  source page and test EVERY item — lists that span a page break are where items get dropped
  (card-rules #14).
- **`kind: "image"`** — crop it and author from the figure:
  `python3 scripts/render_page.py --source <id> --crop-from work/<source>/<label>_highlights.json`
- **A highlighted TABLE CAPTION means "card the table's CONTENT."** Two traps, both hit in
  Chapter 6 (2026-07-29):
  1. **The body is often a rendered image**, so `pdftotext` returns the caption plus a bare
     "Description" stub and *silently yields no rows*. Three of Chapter 6's tables (6-9, 6-10,
     6-12) were image-only. If a table's rows don't come back as text, **render the page and
     read it** (`python3 scripts/render_page.py --source <id> <page> --dpi 170`) before
     drafting — otherwise the content is quietly lost.
  2. **`grounding: EXACT` on such an item is misleading** — it matched the *caption*, not the
     body. A verifier that only greps page text will wrongly condemn correct table-derived
     cards as fabricated. Render before judging them.

  Also dedupe hard afterward: a table is usually a **recap** of prose the neighbouring
  highlights already cover, so table rows are the single most common source of same-fact
  duplicates (card-rules #12). Card what the table *adds*, not what it repeats.
- **`kind: "note"`** — Parker's own words with no source span. Ground it against the page
  before carding, or flag `needs_human_check`. Never card an ungrounded note silently.
- **`user_comment`** is Parker talking directly to you. Obey it:
  - *"Know all of these!!"* → test every item exhaustively;
  - a **question** → answer it (grounded only in the source) and surface it at hand-off;
  - *"look more into this"* → flag `needs_human_check` and tell him what to look into;
  - an **exclusion** — *"NOT ON THE EXAM"*, *"not in the slides"*, *"these are subjective so
    don't just mem"* → **do not card it**, or card only the part he indicated. This is the
    one licensed exception to "never drop a marked span," because he is explicitly
    overriding his own mark. Say so at hand-off.

  Never silently ignore a margin comment.

### Stage 2 — For each item: classify → draft → edit

0. **Group first (Rule 0 — before anything else).** Scan the items around this one (same
   page, consecutive, overlapping `context`). If several are parallel pieces of one idea —
   the bullet lead-ins under a single heading, a set of related terms, the steps of one
   process — treat them as ONE unit and make a single unified card. Never fragment a
   connected set, and never drop a marked span as "thin." See `card-rules.md` Rule 0.

1. **Classify the fact type, then open its recipe.** Definition · numeric value/dose/cutoff ·
   classification list · ordered sequence · comparison/direction-of-change · mechanism ·
   indication/contraindication · trigger · buzzword/vignette · figure · ambiguous fragment.
   Then open the matching section of **`reference/card-recipes.md`** — the archetype playbook
   (when-to-use, exact template, hint + Back-Extra conventions, do's/don'ts). Drill into
   `reference/cloze-mastery.md` only for more exemplars.

2. **Fact pass, THEN draft.** First list every atomic proposition in the marked span + its
   `context`, and tag each: **MUST-TEST** (he must *produce* it from memory — a definition, a
   goal/purpose/function, a number/range, a discriminating feature, an
   indication/contraindication, an ordered step, a sign), **SUPPORTING** (only cues the
   answer — leave it visible), or **SKIP** (incidental filler). THEN draft card(s) so that
   EVERY must-test fact is clozed somewhere. Leaving a must-test fact unclozed as scenery is
   the under-clozing bug.

3. **Edit each candidate** through `reference/editor-checklist.md` as an adversary —
   mandatory, and best run by fresh, *independent* eyes (a writer defends its own work; a
   reviewer hunts the miss). Its #1 job: re-run the fact pass — is every MUST-TEST fact
   actually clozed, or is one sitting as scenery? Set `needs_human_check: true` for any
   number/dose/threshold or weak grounding.

4. Keep survivors as card objects in the shape from `reference/note-format.md` — including
   `"source": "<id>"` and `"segment": <N>`, which is how the writer routes them.

**Generate DECOMPOSED, never hand-crafted in one pass.** Work one unit at a time, each
getting its own fact-pass → draft → *independent* adversarial edit. Do NOT draft a whole
segment inside one context window: that is how an AI takes shortcuts and skips the checks.
For a full segment, FAN OUT in THREE stages: (1) **group aggressively** so a connected
cluster is ONE unit; (2) per-unit draft + *independent* edit; (3) **global consolidation**.

### Stage 2.5 — Global consolidation (REQUIRED after any fan-out)
A per-unit fan-out has no global view, so it duplicates the same fact across neighboring
units and over-fragments one concept into many micro-cards (it once turned 36 marks into 76
cards). After all units are drafted and edited, run ONE pass with the WHOLE segment in view:
**dedupe** the same fact carded twice (keep the best), **collapse** a concept split into many
micro-cards down to the 1–2 high-yield ones, and **trim** genuine trivia — all WITHOUT
dropping any must-test fact. Emit a transparent merge/collapse/cut log so Parker can audit
the balance.

### Stage 2.75 — Verify (a mandatory gate, never skip)
Reliability is a harness, not a promise to be careful.
1. `python3 scripts/check_cards.py work/<source>/<file>.json` — the deterministic gate (legal
   HTML + cloze-present = HARD block; literal-answer-in-stem, parenthetical-after-cloze,
   husks, first-letter-hint leaks, bloated single blanks, numeric-without-flag, in-batch
   duplicates = warnings). Fix HARD errors; route every warning to the judge. On a HARD-clean
   pass it writes a `<file>.verified` stamp (a hash of the exact file).
2. The independent LLM judge runs the FULL `reference/editor-checklist.md` on every card
   (run, never eyeballed).
3. Both are calibrated against `reference/regression-cases.md`. Whenever a rule, the checker,
   or the judge changes, run `python3 scripts/test_regressions.py` so nothing regresses.

**This gate is physically unskippable:** `anki_write.py` refuses to stage any file without a
current `.verified` stamp, and editing the JSON after the check invalidates it. `--force`
exists as a deliberate escape hatch only.

### Stage 3 — Stage into Anki (once per segment)
```
python3 scripts/anki_write.py work/<source>/<file>_cards.json
```
(Add `--dry-run` first to validate without writing — dry-run skips the stamp gate.) Each card
goes to its source's staging deck, derived from its `source` + `segment`, on the registry's
note type, with the registry's tags, one at a time, with pre-flight validation. The writer
also creates the promotion deck so Parker's target exists, and copies the deck root's preset
so bury-siblings stays on for two-way definitions. **Anki must be open.**

### Stage 4 — Hand off
Tell Parker:
- how many cards landed where, and to promote keepers into the sibling deck;
- the `needs_human_check` ones (doses/numbers/weak grounding) to verify;
- **answers to any margin questions** he wrote, from the source, with what to double-check;
- anything he flagged "look more into this," and the specific thing to look into;
- anything you did NOT card because a margin comment excluded it.

Margin comments are Parker's voice on the page; a hand-off that ignores one has failed even
if the cards are perfect.

---

## Reference files (load on demand)
- `reference/sources.md` — the source registry: fields, deck templates, how to add one.
- `reference/profiles/*.md` — per-subject emphasis (`emt` · `science` · `language` · `default`).
- `reference/card-rules.md` — the full standard (Layer A form + Layer B judgment, including
  the Cold-Solve Gate). Read before drafting.
- `reference/parker-preferences.md` — Parker's living tastes. Read before drafting; when it
  conflicts with card-rules, this wins.
- `reference/card-recipes.md` — **the archetype playbook**: which card shape to use plus the
  exact template. The primary drafting reference; consult it every time.
- `reference/editor-checklist.md` — the 20-point adversarial Editor pass. Read before editing.
- `reference/note-format.md` — note type, cloze/MathJax/image syntax, Back Extra vocabulary,
  write targets.
- `reference/regression-cases.md` — R1–R12, the failure library. Read FIRST on any bug report.
- `reference/feedback-log.md` — the running history of what Parker caught and how it was fixed.
- `reference/cloze-mastery.md` — 2,391 annotated AnKing exemplars. **Large — open only the
  section for the card type you're writing.**

## Improving over time (the feedback loop)
When Parker reacts to a card, that's the signal that makes this system grow. Route it, then
commit + push:
- **One bad card** → fix that card. No rule change.
- **A recurring pattern** ("cards keep doing X") → a rule in `card-rules.md` /
  `editor-checklist.md`, plus a regression case, plus a checker extension if mechanizable.
- **A subject-specific pattern** ("stop doing X for Arabic") → that source's profile.
- **A taste** ("I like it phrased like Y") → `parker-preferences.md`.
- **An extraction or routing issue** → the script or the registry.

Always generalize: turn "this card is wrong" into the rule that prevents the whole class.
That's how the next segment inherits everything learned in the last one — and now, how a new
*subject* inherits everything already learned from EMT.
