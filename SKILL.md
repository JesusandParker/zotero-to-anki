---
name: zotero-to-anki
description: Turn anything Parker marks in YELLOW in Zotero into excellent Anki cloze cards — and any word he marks in PURPLE into a plain-language definition card (the lexicon lane) — from any textbook, lecture PDF, or paper. Use (1) to GENERATE cards when he points at a source ("make cards from chapter 6 of my EMT book", "I finished highlighting the Arabic unit", "make cards from this genetics lecture", "define the words I marked", "I purpled some words in chapter 8"), AND (2) to REGISTER a new source he hasn't used before ("add my organic chem textbook", "point this at my Arabic book"), AND (3) to FIX/REVIEW/IMPROVE existing cards or the card-maker itself when he reports a problem while studying ("I noticed an issue with a card", "this flashcard is wrong / the hint gives it away", "fix the card maker", "the cards keep doing X"), AND (4) to BATCH-PROCESS the complaints he types into the hidden "Card Feedback" field during review ("go look at my card feedback", "process my complaints", "go through the cards I ranted about", "harvest my Anki feedback"). On any single-card issue follow the "If Parker reports an issue" procedure below; for a batch, follow "Processing card feedback (batch)".
---

# Zotero → Anki

Parker marks what he wants to memorize in **yellow** while he reads, and any word he
doesn't know in **purple** (usually a purple underline — it stacks cleanly under a yellow
highlight). This turns yellow marks into Anki cloze cards — grounded in the real page
text, quality-checked by an adversarial editor and a deterministic gate, and staged into
a review deck he approves — and purple marks into **plain-language definition cards** in
the same segment's deck (the lexicon lane: card-rules #28, recipes §4b).

It works on **any source registered in `reference/sources.json`** — the EMT textbook it was
built on, an Arabic textbook, a genetics lecture PDF, a paper. Which PDF, which colors,
which page→segment map, which Anki deck, and which subject profile all come from the
registry. Nothing in the pipeline is specific to one book.

**The yellow mark is Parker's "this matters" signal — he has already decided what's
important. Your job is to turn it into the best possible card(s), not to re-decide
importance.** The purple mark is the same contract for vocabulary: he has already decided
he didn't know the word — never re-decide that either (its only licensed skips are
integrity ones, always surfaced: card-rules #28).

## Four rules that override everything

0. **Cards come ONLY from Parker's marks. Never select content for him — no matter how
   sparse the marking.** His vision for this pipeline, stated 2026-08-08: *"every day I
   might read 10 pages in the textbook and you're able to go in and create perfect
   amazing really good solid flashcards off of those 10 pages"* — the marks on those
   pages, nothing more. A lightly-marked chapter is a SMALL batch, not a delegation:
   "I've only highlighted a little bit, please do this for me" means *run the pipeline
   on the little bit*. If unmarked content ever seems worth carding, SAY SO at hand-off
   and stop — never draft it, not even clearly labeled (the 2026-08-08 "coverage lane"
   labeled every synthetic mark `selected_by: "claude"` and was still 80 retracted
   cards and two wasted hours). Spend the whole effort budget making HIS marks'
   cards excellent instead. Enforced: `check_cards.synthetic_marks_check` HARD-blocks
   any card citing a non-extractor mark (card-rules #29, R40).

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
**Color picks the LANE; markup style never matters.** Parker highlights in textbooks but
*underlines* on lecture slides, and both mean the same thing to him. Two colors have
meaning — **yellow** (`colors`, default `#ffd400`/`#facd5a`) = "this matters, card it";
**purple** (`lexicon_colors`, default `#a28ae5`/`#c885da`) = "I don't know this word,
define it plainly" (his habit: a purple underline, stacking cleanly under yellow):

| Mark | Extractor `kind` | What to do with it |
|---|---|---|
| yellow highlight/underline | `text` | Normal grounded card. The main path. |
| yellow area selection | `image` | The figure IS the card — crop it and author from the image. |
| yellow standalone note | `note` | Parker's OWN words, no source span. Ground it before carding, or flag it. |
| **purple highlight/underline** | `lexicon` | An unknown WORD → one authored plain-language definition card. Card-rules #28, recipes §4b — run `lexicon.py --find` + `--dedup` first. |
| purple area selection / note | `unsupported_purple` | No defined meaning yet — surface it at hand-off and ask; never guess, never drop. |
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
4. **Fix the card(s)** in Anki and in the JSON — but FIRST check who wrote what:
   ```
   python3 scripts/authorship.py check --source <id> --note <noteId>
   ```
   **Never overwrite a field this system did not author.** Parker adds mnemonics he
   invented, images he pasted, TTS audio and notes to himself, and none of it is visible
   to the pipeline. `owned` may be rewritten; **`edited` and `unknown` may not** — read the
   live value, carry his additions into the new version, or ask him. `authorship.guard()`
   enforces this in code; verified whitespace-only repairs still pass.
   *Also:* content that is **not in the source is not automatically a fabrication** — it may
   be Parker's. Check authorship before concluding a past run invented something.
   (2026-07-30: a session deleted a mnemonic he wrote himself and called it a caught
   fabrication. See `parker-preferences.md`.)
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
- **`needs_visual: true`** — the text layer does NOT contain what this mark points at. Two
  causes, both common: the mark is a **table/figure caption** (`content: CAPTION_ONLY`) whose
  body sits on the next page or in a rendered image, or it sits on an **image-heavy page**
  (`content: SPARSE_PAGE`). Render the page, read it, and **attach the crop** to the card via
  `image`/`visual_source`. This is not optional politeness: `check_cards.py` HARD-blocks a card
  whose claims are absent from its cited text and which carries no visual evidence (R13).
  ```
  python3 scripts/render_page.py --source <id> <page>
  ```
  *Read `grounding` and `content` as two different questions.* `grounding: EXACT` means only
  "I found your marked text" — it says nothing about whether the material is present. EMT
  TABLE 4-4 was `EXACT` with a context paragraph about not touching a patient's torso.
- **A marked `SKILL DRILL` caption is a PROCEDURE, and it gets two special treatments.**
  (1) The extractor follows it across every page carrying a `Step N` heading, so its whole
  step sequence is in `context` — but the step text is the *source*, not the card. **Card it
  as decisions, never as a recitation** (card-rules #26, recipes §12): the indication, the
  trade-off that justifies it, the contraindication, the step people get wrong, and a
  decision-point vignette. `check_cards.py step_recitation` warns if you slip back into
  numbering steps. (2) `build_figure_index.py` composites the drill's step panels into ONE
  plate showing the whole procedure — attach that to the back, so the full sequence is
  visible the moment he answers.
- **A marked TABLE with no raster** (many are typeset as live text) is rendered from the page
  by `build_figure_index.py` (`text-table-render`), so it is still attachable — Parker's
  design puts the source table on the back of every card split out of it (rule 25).
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
- **`kind: "lexicon"`** — a PURPLE word: "define this plainly" (card-rules #28, recipes
  §4b). The item carries `term`, `term_key`, and hygiene `flags` (`multiword` = probable
  drag slip; `midword` = an edge clips a word — check the page, fix the term, and surface
  the flag at hand-off). Before drafting ANY of them, run both:
  ```
  python3 scripts/lexicon.py --find <id> --terms-from work/<source>/<label>_highlights.json
  python3 scripts/lexicon.py --dedup work/<source>/<label>_highlights.json   # Anki open
  ```
  `--find` hunts the source itself for each word's own definition (glossary first — the
  book often defines it three chapters later) and writes the evidence file the gate
  verifies (R37); `--dedup` says which words are already carded (ledger + live Anki
  check). A duplicate key with the SAME sense = skip and report; a DIFFERENT sense
  (hypoxia/hypoxemia collide by design) = a new card with a visible domain cue.
- **`kind: "unsupported_purple"`** — a purple area-selection or standalone note. No
  defined meaning yet: list it at hand-off and ask Parker what he wants; never guess.
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

0b. **Then size the unit (Rule 23 — the other half of Rule 0).** Rule 0 pulls a scattered set
   TOGETHER; rule 23 decides how much of it fits on one card. Count the answers a single cloze
   group would hide with no per-item cue: **≤4** ships as one card, **5–7** only with a real
   retrieval handle (a spelled mnemonic the card teaches, or a structure that regenerates the
   members), **≥8** must be chunked into named sub-groups on SEPARATE NOTES plus an anchor
   note — never c1..cN on one note, which shows the rest of the list for free (rule 24). A
   grouped reveal is graded all-or-nothing, so a ten-item card fails even when every fact on
   it is known. `check_cards.py` HARD-blocks ≥8 uncued. See `card-rules.md` #23–24.
   **And if the answers are NUMBERS keyed by a label** — vitals by age, milestones by month —
   it is one note PER KEY with the source table attached on the back, however few rows there
   are: the column interpolates, so visible neighbours hand over the blank (rule 25, HARD at
   4 rows).

1. **Classify the fact type, then open its recipe.** Definition · **lexicon (purple word
   → recipes §4b)** · numeric value/dose/cutoff · classification list · ordered sequence ·
   comparison/direction-of-change · mechanism · indication/contraindication · trigger ·
   buzzword/vignette · figure · **procedure/skill drill** · ambiguous fragment.
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
   `"source"`, `"segment"`, and **`"from_idx"`: the indices of the mark(s) this card was built
   from**. Provenance is required (`reference/provenance.md`): it is what lets the gate verify
   Rule 1, and what lets a future session ask any card in Anki why it exists. Record
   `verified_against` / `verified_by` for every number you check, and `visual_source` for
   anything you read off a rendered page.

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

**Cross-lane fold-in (purple × yellow).** When Parker purples a word AND the same batch
carries a yellow card that already tests that term↔meaning (he yellowed the book's own
definition of it), do NOT ship both: **fold the lexicon card into the grounded definition
card** — keep the yellow card, make sure its meaning side reads plainly (the crisp-c2 rule
already forces this), add the lexicon card's `Ex:`/`Parts:` lines to its Back Extra, and
cite BOTH marks in `from_idx` (a fold-in must keep at least one yellow mark cited — the
gate enforces it, R36). Log the fold in `decisions.jsonl`. Same-batch duplicate `term_key`s
(the checker warns): merge same-sense repeats; sense-split true homonyms with a visible
domain cue on each.

### Stage 2.75 — Verify (a mandatory gate, never skip)
Reliability is a harness, not a promise to be careful.
0. `python3 scripts/verify_report.py work/<source>/<file>_cards.json` — derives
   `needs_human_check` from what was actually verified (rather than "contains a digit") and
   writes `<file>_VERIFY.md` split into **Section A: needs your eyes** and **Section B:
   verified, skim**. Run it BEFORE the gate; it rewrites the file, which invalidates any stamp.
0b. `python3 scripts/check_block_spec.py work/<source>/<file>_cards.json` — the **cumulative
   requirements** check. `check_cards.py` asks *is this card well-formed?*; this asks *does it
   still satisfy every requirement Parker has ever established for its block?* Requirements
   only ever get ADDED to it, so a later fix can never silently undo an earlier one (the
   failure that created it: country cards went one-way → two-way → one-way again across three
   rounds of his feedback). **Any new preference he states becomes a rule here, in the same
   session he states it.** When writing a rule, make its *applies-to* predicate structural —
   a predicate that keys on the feature being tested cannot catch that feature's removal.
1. `python3 scripts/check_cards.py work/<source>/<file>.json` — the deterministic gate (legal
   HTML + cloze-present = HARD block; literal-answer-in-stem, parenthetical-after-cloze,
   husks, first-letter-hint leaks, bloated single blanks, numeric-without-flag, in-batch
   duplicates = warnings). **R13 grounding** is checked here too: every cloze answer is tested
   against the context of the mark(s) the card cites. An answer absent from a `needs_visual`
   mark with no attached evidence is a HARD block — attach the crop. Fix HARD errors; route
   every warning to the judge. On a HARD-clean pass it writes a `<file>.verified` stamp.
2. The independent LLM judge runs the FULL `reference/editor-checklist.md` on every card
   (run, never eyeballed).
3. Both are calibrated against `reference/regression-cases.md`. Whenever a rule, the checker,
   or the judge changes, run `python3 scripts/test_regressions.py` so nothing regresses.

**This gate is physically unskippable:** `anki_write.py` refuses to stage any file without a
current `.verified` stamp, and editing the JSON after the check invalidates it. `--force`
exists as a deliberate escape hatch only.

### Stage 2.85 — Preflight, and the post-mortem afterwards
Run this before the figure stages and again when they're done. It exists because the
evidence for a figure run ends up spread across an index, a proposals file, a verdicts
file, an undo record and the live deck — fine while one session holds it in mind, useless
the next day.

```
python3 scripts/figure_run.py --source <id> --segment <N> --preflight
python3 scripts/figure_run.py --source <id> --segment <N> --report --write-run
```

`--preflight` asserts the things that have silently broken before: the venv, ImageMagick,
Anki, a modern-schema highlights file, enough cards placeable on a page for the matcher to
work, a study copy for every figure. `--report` prints every stage's count and a list of
**ANOMALIES** — each one a defect that actually happened (unjudged proposals, a card
carrying two figures, an image on the question side, a judge rejecting most of what it was
given, a figure count that moved against its baseline). It caught a real one immediately:
Chapter 5's proposals had been silently un-judged by a `--force` re-match.

### Stage 2.9 — Attach figures (once per segment)
A textbook's plates are half of what it teaches, and the pipeline used to render them,
read them, and throw the pixels away. Build the index once per segment, then propose:

```
.venv/bin/python scripts/build_figure_index.py --source <id> --segment <N>
.venv/bin/python scripts/match_figures.py --source <id> --segment <N> \
    --json work/<src>/ch<N>_figure_proposals.json
```

**Extract, never crop.** In a real publisher PDF each plate is already a discrete embedded
raster at its ORIGINAL resolution (EMT's skull is 2133×1035, ~336 dpi). Rendering the page
and cutting it out discards roughly 2× linear resolution. This also dissolves the
figure-spans-two-pages problem: a plate straddling a page break is ONE image object placed
twice, and extracting returns it whole — **splitting is a property of pagination, not of
the picture.**
**That guarantee covers embedded RASTERS only.** A table typeset as live text has no image
object, so it is re-rendered from the page (`text-table-render`) and genuinely can be cut
by a page break — EMT TABLE 8-3 lost two of its six rows that way. Check the row count of
any `text-table-render` plate against the mark's context before trusting it (R32). `render_page.py` is still the right tool for *reading* a page; it is the
wrong tool for *harvesting* art.

The index also captures the book's accessibility **long description** — prose naming
everything labelled in the plate — which is what turns "what is in this picture" into text
a card's answers can be tested against. It is accepted only when it corroborates its own
caption; a description that shares no vocabulary with its caption is the wrong one and is
dropped rather than believed.

**Be generous, but the axis is CONGRUENT vs INCONGRUENT — not necessary vs unnecessary.**
Parker is happy to carry a figure he does not strictly need (the developmental age-group
photos: *"there's no problem with having those pictures in the back extra"*). What he will
not carry is a picture that makes him ask *"why in the world is that picture there?"* —
*"it leads me to a root of confusion instead of a root of actually succeeding, because I'm
sitting here questioning what this picture has to do with the flashcard."* A teenager on a
card about teenagers costs nothing; a crying baby on a card about hand position costs
attention. So coverage and archetype grade how STRONG a match is, not whether it happens —
but **zero shared vocabulary is never enough, not even on the card's own page.** A page
holds many paragraphs and the figure illustrates ONE of them. `--strict` restores the
conservative all-three-signals rule.

**The matcher scores a card by its CLOZE ANSWERS ONLY — never its visible text.** This is
the single most counter-intuitive thing about the stage and it inverts the obvious advice.
A card can be squarely on topic, say the subject three times in plain prose, and still
score **0.00** and be zero-coverage-blocked; conversely a card earns a plate by *hiding*
the word. On EMT ch7 the fontanelle definition card matched FIGURE 7-2 at 0.375 because
`{{c1::Fontanelles}}` was its answer, while the two neighbouring fontanelle cards — whose
answers are months, and *depressed*/*bulging* — scored 0.00 despite naming fontanelles in
every line. So: **never write a card to feed the matcher.** Answer quality decides the
wording; if the right card then scores zero and the plate genuinely belongs on it, add the
proposal by hand and judge it like any other (`forced: true`), which is what Parker's
margin request for FIGURE 7-2 "on the flashcards relating to the fontanelles" required.

### Stage 2.95 — JUDGE the figures (mandatory; word overlap cannot do this)
Matching can tell you a figure and a card share vocabulary. It cannot tell you the figure
**depicts** what the card is about, and that is the only question that matters. Two real
misses, both caught by Parker while studying:

- FIGURE 4-2 (*"the effectiveness of body language: happy / angry / sad"*, three faces) on
  a card about holding your **palms out** toward a hostile patient — **zero** shared words;
  it matched on page adjacency alone.
- FIGURE 4-17 (a radio transmission diagram: control centre → tower → ambulance) on
  *"a cellular telephone is a low-power portable radio"* — shared `radio` and `repeater`,
  both genuinely distinctive words, so no frequency trick catches it. The plate shows a
  base station; the card is about a phone.

So the figure pipeline gets the same shape Stage 2.75 gives cards: a deterministic gate,
then an **independent pass that actually looks.**

```
python3 scripts/judge_figures.py --source <id> --segment <N> --emit  work/<src>/ch<N>_judge_worklist.json
#   LOOK at every figure. Fill in `depicts` (what it really shows) and mark each card keep/drop.
python3 scripts/judge_figures.py --source <id> --segment <N> --apply work/<src>/ch<N>_judge_verdicts.json --strip-live
```

The worklist is **one entry per distinct FIGURE, not per proposal** (a chapter has ~15–40
plates against ~25–100 proposals), so you describe each plate once and judge all its cards
from that — 2–3× less looking for the same answer. `--strip-live` **reconciles** the deck
to the surviving set, not just the judge's rejects: proposals also vanish when the matcher
tightens, and those are equally wrong to leave on a card. Parker's own pasted images are
never touched. The `depicts` text is written back into `figure_index.json` as
`seen_description` — permanently, because it is the description the publisher never
supplied for most plates, and it makes the *next* match smarter.

**Figures go on the BACK.** A plate labels its own anatomy, so the figures most worth
attaching are exactly the ones whose labels ARE the cloze answers; on the front they answer
the card. Set `"image_side": "front"` only when the picture IS the question (*identify this
structure*). Attach the **`study_file`** (1400px, ~150 KB), not the native archive — that
is what keeps a whole book to ~0.25 GB of media instead of 1.75 GB.

**Every study copy is MATTED (`--pad-pct`, default 4%).** Extraction cuts exactly to the
artwork bounds, so without this a label like *"Parietal bone"* ends flush against the image
edge and the card looks cramped — the breathing room Parker got for free when he
screenshotted a region of the page, and which he asks for by name. The copy is trimmed to
its true content box first (plates carry inconsistent built-in whitespace; normalising is
what makes the final margin uniform), then bordered by 4% of the **normalised** long edge —
since every study copy is scaled to the same long edge, that is the same absolute margin on
every figure, wide or tall. The border colour is **sampled from the plate's own corner**, so
a figure on a dark ground is not framed in a white halo.

**Rebuilding the study copies changes the FILES but not their names**, and the notes already
reference those names — so after any `--pad-pct` / `--max-px` change on an already-attached
segment, push the new images with `attach_figures.py --refresh-media`. A plain re-run would
correctly skip every card as already-attached and leave the stale images in place forever.

**The quality bar (Parker, 2026-08-08 — non-negotiable):** a card carries the book's
COMPLETE figure, caption included, or no figure at all. A fragment, a clipped label, a
wrong-art pairing, or page-text bleed never ships — reject at the judge-look, re-render
properly, look again. Line art (vector renders, text tables) is **lossless PNG at full
render resolution (≥400 dpi), never resized, never JPEG** — `study_copy(lossless=True)`
does this automatically for every `*render*` extraction. Photos keep native-resolution
extraction (that IS the book's own quality). For vector-art books, the proven route is a
full-page render at high dpi cropped to the whole figure and EYEBALLED — automated
region-guessing produced truncated fragments on Snustad ch9.

**Updating media that is already on live notes — three rules, each learned the hard way
(2026-08-08):**
1. **Never swap bytes under an existing filename.** Anki's UI caches media BY NAME; an
   open session keeps showing the old image even though the collection holds the new
   bytes. Store under a NEW versioned name (`…_v2.png`), rewrite the notes' `<img>` tags,
   then delete the orphaned old file.
2. **Reference the RETURNED filename, never the requested one.** `storeMediaFile`
   case-normalizes names (`FIGURE` → `figure`); on Parker's case-insensitive Mac the
   mismatch is invisible, on any case-sensitive sync target it is a broken image.
3. **Round-trip verify every store:** `retrieveMediaFile` the name back and compare
   hashes before touching any note. A store you didn't verify didn't happen.

### Attaching: two routes, and picking the wrong one duplicates the chapter

**A fresh segment (Chapter 7 onward) — figures go into the CARDS FILE, before staging:**

```
python3 scripts/attach_figures.py --source <id> --segment <N> --to-cards
python3 scripts/check_cards.py work/<src>/chapter_<N>_cards.json     # re-stamp
python3 scripts/anki_write.py   work/<src>/chapter_<N>_cards.json
```

This sets `image` + `image_side: "back"` on each kept card and lets Stage 3 embed them as it
creates the notes. It **refuses to run on unjudged proposals** — word overlap alone attaches
pictures that are merely nearby.

**A segment already staged (Chapters 1–6) — update the live notes:**

```
python3 scripts/attach_figures.py --source <id> --segment <N> --dry-run
python3 scripts/attach_figures.py --source <id> --segment <N>
python3 scripts/attach_figures.py --undo work/<src>/figure_attach_undo_seg<N>.json
```

**Never re-run `anki_write.py` on an already-staged segment to add figures** — it ADDS
notes, so it would produce 202 duplicates instead of 202 pictures. The live path matches
notes by Text, is idempotent, accumulates an undo record, and gives each card exactly one
pipeline figure (`--replace` / `--allow-multiple` to opt out).

**Both routes are bound by the authorship guard.** `attach_figures` and
`judge_figures --strip-live` write `Back Extra` on notes this system may not have authored,
and everything predating the authorship store is `unknown` — protected. They pass
`figure_only=True`, a **verified** predicate: the write is allowed only when stripping
pipeline-owned `<img src="<source>_…">` from both sides leaves byte-identical residue.
Parker's own pasted images never carry that prefix, so **removing one still fails the
guard.** Never relax this to make a write succeed.

### Stage 3 — Stage into Anki (once per segment)
```
python3 scripts/anki_write.py work/<source>/<file>_cards.json --run runs/<source>/<seg>/<run_id>
```
Pass `--run` so each staged card's Anki noteId is written back into the run's
`provenance.jsonl`; that link is what makes `run_store.py trace <noteId>` work later.
(Add `--dry-run` first to validate without writing — dry-run skips the stamp gate.) Each card
goes to its source's staging deck, derived from its `source` + `segment`, on the registry's
note type, with the registry's tags, one at a time, with pre-flight validation. The writer
also creates the promotion deck so Parker's target exists, and copies the deck root's preset
so bury-siblings stays on for two-way definitions. **Anki must be open.**

### Stage 4 — Hand off
Tell Parker:
- how many cards landed where, and to promote keepers into the sibling deck;
- the `needs_human_check` ones (doses/numbers/weak grounding) to verify — including the
  **Vocabulary block**: every externally-anchored definition, term + gloss on one line
  each (he met each word in context, so a wrong gloss takes seconds to spot);
- **purple repeats** — words already carded that he marked again (rule 28: a repeat is
  data — the first card isn't doing its job; offer the existing card for review);
- **purple hygiene flags** (drag slips / clipped words) and any `unsupported_purple`
  marks, with the question of what he wants them to mean;
- **answers to any margin questions** he wrote, from the source, with what to double-check;
- anything he flagged "look more into this," and the specific thing to look into;
- anything you did NOT card because a margin comment excluded it.

Margin comments are Parker's voice on the page; a hand-off that ignores one has failed even
if the cards are perfect.

### Stage 5 — Close the run (required)
Finish the run record: `run_store.finish(run, cards=…, counts=…, hazards=[…])`.

**If this run discovered a new failure mode, it must be closed, not just described.** Every
entry in `new_hazards_found` needs either a `regression_id` naming the case that now catches
it, or `mechanizable: false` with a `why`. `scripts/check_hazards.py` enforces this and
`smoke_test.sh` runs it. This exists because the pattern has recurred: a run finds a real
hazard, writes a paragraph about it, ships the affected cards, and reports itself verified.
Naming a hazard is step one of *name it, mechanize it, test it* — not the whole job.

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
- `reference/editor-checklist.md` — the 28-point adversarial Editor pass. Read before editing.
- `reference/note-format.md` — note type, cloze/MathJax/image syntax, Back Extra vocabulary,
  write targets.
- `reference/regression-cases.md` — R1–R37, the failure library. Read FIRST on any bug report.
- `reference/provenance.md` — the card provenance schema, the run store, and the hazard rule.
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
