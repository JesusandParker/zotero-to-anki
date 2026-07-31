# Unit C — editor verdicts (marks 10–19)

Adversarial pass over the drafter's 7 notes. Result: **1 PASS · 4 REWRITE · 2 DROP** →
**6 notes / 9 Anki cards** (was 7 notes / 10 cards). `check_cards.py` clean: 0 hard, 0
warnings, stamped. Every mark 10–19 is still covered; mark 18 remains the one deliberate
non-card (caption pointer, `needs_visual`).

## Verdicts, one line per drafted note

| # | drafted note | verdict | what changed |
|---|---|---|---|
| 0 | four-reflex match card (4 rows) | **REWRITE → split into new #0 + #1** | 2 of 4 rows were self-answering (R15). Rows dropped, coverage re-homed to a grouped-reveal roster card. See below. |
| 1 | rooting + sucking = the feeding pair | **DROP** | Absorbed into new #0's `Cue:` line. See below. |
| 2 | fontanelle two-way definition (c1/c2/c3) | **REWRITE** | c2 crisped 7→6 words ("unfused" cut); Back Extra rewritten so it stops restating c2. Cloze structure kept — it is correct and it is the figure carrier. |
| 3 | posterior/anterior closure ages | **REWRITE** | Lead-in "The two fontanelles…" asserted a count the source never makes (the chapter discusses two; the skull has six). Now "The fontanelles do not close at the same age:". Rows, `→`, `<br><br>` and the numeric flags untouched. |
| 4 | depressed vs bulging contrast | **PASS** | Genuine R10-licensed multi-dimensional contrast — NOT a husk. Text untouched. Back Extra only: the `Cue:` line was restating both c2 answers in plain words, so it is now a real hook (`Mnemonic:`). |
| 5 | dehydration vignette → expected fontanelle | **DROP** | R6 / editor #16. See below. |
| 6 | teething | **REWRITE** | Text kept (the low-grade qualifier IS clozed — no R1 failure). Back Extra's ungrounded clinical directive softened to a pure entailment; `needs_human_check` raised. |

## The four judgement calls the orchestrator asked for

**1. The match card's rows — two of the four answer themselves. Dropped them.**
Run R15 per row, and the reflex NAMES do the leaking, not the drafter's phrasing:

- *palmar grasp* — the cue must say "an object placed in the **palm**… the hand **closes
  around** it". "palm" → *palmar* and "closes around" → *grasp*. The row cannot be phrased
  around this: the name is a literal description of the trigger. Self-answering. **Dropped.**
- *sucking* — "stroking the **lips** prompts the baby to **latch on**" → sucking. Same
  problem, and the row flagged in the brief. **Dropped.**
- *Moro* and *rooting* are the only two opaque names in the set, so they are the only two
  rows that make him produce anything. **Kept**, with one fix: the Moro row's alias was
  inside its own blank (`{{c1::Moro (startle)}}`) while the cue said "caught off guard" —
  which *is* being startled. Alias moved to the Back Extra, cue re-anchored on the
  observable behaviour ("arms fly open wide, fingers spread, as if grabbing at something").
  Now neither name is derivable from its cue.

Neither the checker nor a whole-card read catches any of this — `row_label_tautology`
misses "palm"/"palmar" (stems differ at 5 chars) and "lips/latch"/"sucking" (no shared
stem). It is judge-only.

Dropping two rows would have lost marks 11 and 13, so the coverage moved to a **grouped-reveal
roster card** (new #0: "In a healthy, full-term newborn, four reflexes are present at
birth:" + four clozed names). That is card-rules #22's preferred shape (a) — cloze the
items themselves — and it is a closed taxonomy the source names, so it is answerable cold
(R9 MUST-NOT-OVER-FLAG). Net effect: **6 real recalls, 0 freebies**, where the drafted pair
gave 4 real and 2 free. Also removed the invented count from the match lead-in ("Four
reflexes… Name each one") so it no longer promises four answers while owing two.

**2. Note 1 (rooting + sucking as the feeding pair) does NOT earn its place. Dropped.**
Three reasons, in order of weight: (a) the roster card now makes him produce *rooting* and
*sucking* by name, so the feeding card asks for the same two words a second time; (b) "two
other reflexes play an important role in feeding" is a **context sentence, not a
highlighted span** — it carries no never-drop protection, and every yellow mark it touches
(12, 13) is carded twice over; (c) its Back Extra was a live **R6 sibling leak** — "rooting
turns the newborn's head toward whatever touches the cheek" is exactly the cue→answer
mapping of the match card's rooting row, reworded. The grouping fact survives as the
roster card's `Cue:` line, where it is reference rather than a second test.

**3. Note 4 (depressed vs bulging) is a licensed contrast, not a husk. PASSED unsplit.**
Cover c1 → the *dehydration* / *increased intracranial pressure* anchors stay visible and
both blanks carry the forced-choice hint. Cover c2 → the *depressed* / *bulging* anchors
stay visible. Each blank is answerable with its sibling shown, which is precisely the
shape R10's "THE JUDGE clears multi-dimensional contrast" paragraph protects. `husk_groups`
also declines it on its own terms (c1: both spans forced-choice-hinted; c2: only one span
is multi-word). **Not split into singletons.**

**4. Note 0 at ~80 words — moot, and the argument was wrong anyway.**
The rewrite lands at 22 words (roster) + 40 (match), so the cap is no longer in play. For
the record the drafter's defence was half right: a genuine cohesive list does stay whole at
any length (card-rules #6), and a match card's rows are rows, not prose — so the 60-word
prose cap was not the reason to touch it. The reason was R15.

## Things consolidation and the figure stage MUST know

1. **The figure matcher scores CLOZE ANSWERS, not visible text — the brief's premise is
   inverted.** `match_figures.score()` computes coverage as *(answer words ∩ figure caption
   terms) / answer words*; the visible stem is never read. Simulated against the real index:

   | card | coverage vs FIGURE 7-2 | matched | outcome |
   |---|---|---|---|
   | #2 fontanelle definition | **0.375** (page_dist 0, archetype spatial) | change, fontanelles, shape | **TEACHES tier — the only card that will be proposed** |
   | #3 closure ages | 0.00 | — | dropped (zero-coverage block; also `numeric` → archetype False) |
   | #4 depressed/bulging | 0.00 | — | dropped |
   | #0, #1 reflexes | 0.00 | — | dropped |

   So keeping **`{{c1::Fontanelles}}` as a cloze ANSWER on note #2 is what earns Parker his
   figure** — un-clozing it to make the word "visible" would have destroyed the only match
   in the unit. The word is already visible in the Text of #3 and #4 and it buys nothing.
   `{{c3::change shape}}` is load-bearing twice over: a real untested fact, and 2 of the 3
   matched terms. (Cutting "unfused" from c2 also mattered — at 9 answer-words coverage
   falls to 0.333 and drops below `--min-coverage 0.34`.)

   **Parker asked for FIGURE 7-2 on the fontanelle cards, plural.** The matcher will only
   ever offer note #2. If more than one is wanted, #3 and #4 must be **force-attached** —
   they cannot be reached by tuning a threshold.

2. **`check_cards.VALUE` does not recognise month/year ages, so `verify_report.py` will
   SILENTLY CLEAR the numeric flags on card #3 — and on most of Chapter 7.** Verified by
   running the real derivation: card #3 (`numeric: true`, `needs_human_check: true`,
   hand-asserted per the brief) derives to `False/False`, because `verify_report` recomputes
   `numeric = bool(VALUE.search(text))`. Measured against `VALUE`:

   ```
   'the third month'      False     '9 and 18 months'   False
   '2 months'             False     '6 months'          False
   '1 month to 1 year'    False     '61 years and older' False
   '98.6'                 False     '9 to 18 months'    True    '100 to 180 beats/min' True
   ```

   Only digit-`to`-digit ranges and the unit list survive. This is a **chapter-wide** hole,
   not a unit-C one — Chapter 7 is age bands in months and years end to end (TABLE 7-1's
   `1 month to 1 year` bands, TABLE 7-2's `2 months` / `6 months` rows, `61 years and
   older`, the bare `98.6` temperatures). Every such card loses its safety flag at the
   verify stage. I did **not** patch `check_cards.py` — seven other unit editors are
   running against the same gate and a mid-run change would invalidate their stamps. Fix
   belongs to the orchestrator: add `months?|years?|weeks?|days?` to the `VALUE` unit
   alternation and `and` to the range connective, then re-run `verify_report.py` for the
   whole chapter. Worth a regression case.

3. **Card #5 (teething) carries one disclosed inference**, inherited from the drafter and
   softened: the source says only "sometimes accompanied by a low-grade fever"; the Back
   Extra adds "so a higher fever in an infant is not explained by teething." That is an
   entailment of the source's own scope rather than new clinical content, and it is what
   makes the qualifier worth carding — but it is not literal, so `needs_human_check: true`.
   Note `verify_report.py` will clear that flag too (EXACT grounding, no digits), so if the
   orchestrator wants Parker's eyes on it, it needs surfacing another way.

4. **Cards #0 and #1 will look like duplicates to a similarity pass — they are not.**
   Same four marks, and *Moro* / *rooting* are answers on both. #0 tests the roster (which
   reflexes exist); #1 tests the mapping (which behaviour is which). Merging them
   re-creates the self-answering rows this edit removed. `check_cards`' near-duplicate
   detector does not fire on them (texts share almost no wording).

5. **Note #2 keeps `needs_human_check: true` and it is correct** — mark 14 is
   `grounding: PARTIAL` (the 450-char window cuts at "These areas, called"). The
   continuation is verbatim in mark 14's own `highlight` field and at the head of 15/16/17's
   context, so the human glance is a formality. `verify_report` derives the same flag
   independently.

6. **Unit boundaries unchanged.** Nothing here overlaps B or D. If unit D cards teething off
   TABLE 7-2's "6 months: begins teething", that is the age of onset — a different fact —
   and both should survive; only a second "low-grade fever" card would be a dedupe target.
