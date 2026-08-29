# E_of_D3 — editor report (EMT ch9, blocks F / H / I)

Independent adversarial pass over `D3_cards.json` (7 cards). Every card run through every
check in `reference/editor-checklist.md`; checks 18–24 run on **every row**, not just per
card. Grounding re-verified word-for-word against the cited marks' `highlight` + `context`
in `work/emt/chapter_9_highlights.json` (idx 9–13, 15, 16). The pipeline's derivation
contract was confirmed at the source (`verify_report.py`: `needs_human_check = (numeric or
weak) AND NOT verified_against`), so verified-numeric-stays-false is the system's own rule,
not a drafter dodge.

**Verdicts: 5 PASS · 2 REWRITE · 0 DROP.** Every assigned mark keeps coverage (rule 1
honored — nothing vetoed).

## Per-card verdicts

| # | Card | Verdict | Failed checks | Exact change made |
|---|------|---------|---------------|-------------------|
| 1 | F-A — four elements of team communication (grouped reveal) | **PASS** | — | None. 4 uncued = at rule-23 cap; rows `<br><br>` (ck 21); count "four" stated and matches 4 clozed items against the full p884–885 list (ck 17 — "Supportive and Coordinated Leadership" opens the NEXT section of the 5-element *team* list, not this one); no letter hints and correctly so — the four names are not a book-taught acronym (ck 20); `Meaning:`/`Pitfall:` both grounded verbatim-or-better in idx 9's context. On the sibling-exposure worry, see ruling (b) below. |
| 2 | F-B — constructive intervention (two-way definition) | **PASS** | — | None. `{{c1::term}} … {{c2::meaning}}` under different numbers is the licensed two-way shape, NOT a husk and NOT a leak (R3/R10 precision — deliberately left un-"fixed"). c2 = 4 words, crisp (ck 6). c1 cold-solves off the visible trigger + action; hint `::communication element` is a clean form label (ck 9). "even the team leader" left visible is right — clozing it self-answers off the frame's own escalation (ck 22). |
| 3 | H-A — closed-loop communication (two-way definition + Ex) | **REWRITE** | 3 (grounding: quoted dialogue not verbatim) | **Ex line restored to word-for-word p888:** Becky's first reply had been clipped to `"Got it. I'll put him on 10 liters."` where the book reads `"…on 10 liters of oxygen."`, and the terminal period was missing inside Aziz's correction (`…with 2 liters"` → `…with 2 liters."`). Narration re-jointed (`catches the mishear:` / `reads back:`) so all four utterances sit inside quotes exactly as printed. Nothing else touched: c1/c2 shape licensed two-way; c2 = 6 words, inside the 3–6-word target and far from R12's 9-word bloat line; stem frame ("to reduce errors when sending or receiving") is situational, not definitional (ck 15). `numeric: true` + `verified_against` recorded → `needs_human_check` false by the verify_report contract. |
| 4 | I-A — PACE grouped reveal + pre-step c2 | **REWRITE** | Safety overlay / batch numeric convention (no craft check failed) | **Metadata only: `numeric` false → true.** The stem states a count ("four-step"), and this batch's own convention — the drafter's F-A note, "numeric: true because the stem states the count 'four'" — demands the same flag here. Count verified: 4 letters of PACE, 4 clozed rows, p888. `verified_against` present → derived `needs_human_check` stays false. Text/Back Extra untouched. Craft all passes: letter hints licensed (PACE spelled + bolded in stem — ck 20's one license); c2 pre-step is a *different fact* under its own number, expressly legal per rule 24's "not a violation" clause, and cold-solves off the "First ___, then use PACE" frame (the book's own protocol structure); c2 span = 7 words, under the 9-word warn line, and it is the load-bearing verb+object (rule 15). Stem's rewording away from "brought to the attention of" was verified — it removes an "attention" echo into c2's answer. Good catch by the drafter. |
| 5 | I-B — Alert vs Emergency audiences (contrast) | **PASS** | — | None. Both blanks carry the §6-endorsed same-option-pair hint (`::team leader / entire team`) — the mandatory forced-choice for a which-goes-where binary (ck 13); both under one c1 = a 2-item cued group (ck 25 fine). "goes **immediately**" is grounded flavor from the E line, not a leak. `Distinguish:` teaches the *trigger* contrast, which the Text doesn't state (ck 11). |
| 6 | I-C — Challenge = suggest an alternative plan | **PASS** | — | None. The visible "clearly challenge the current course of action" is rule-18's *exposed shared scaffold* (clozing it would self-answer off the step name "Challenge" — ck 22's not-a-violation side); the blank is the short, load-bearing, non-derivable residue (4 words, crisp). The Ex quote ("Lieutenant, I think this additional action should be taken. Do you agree?") checked **verbatim** against idx 16. `Distinguish:` line carries the E-trigger contrast — see ruling (b) on it restating I-B's answer on a back. |
| 7 | I-D — leader broadcasts the altered plan | **PASS** | — | None. Single blank, `::role` slot label; anchored by the PACE-challenge situation; grounded in "it is essential for the leader to communicate the change to everyone else on the team." A smart non-knower can *guess* "team leader" at coin-flip odds, but the genuine competing answer (the challenging crew member — the person who knows the change best) is exactly what the book is ruling out, so the discrimination is real; the `Distinguish:` line teaches that split. Knower-certain, non-knower-not — passes ck 15's median. Kept as its own note: folding into I-C as c2 would let "the plan is then altered" decode I-C's c1 (the drafter's split reasoning verified and endorsed). |

## Rulings on the drafter's open concerns

**(a) "Courtesy" and "a clear message" get no definition cards of their own.** Ratified.
Idx 12's only *mark* is the element name, and F-A tests that name as a produced member —
the mark keeps coverage, so rule 1 is satisfied; nothing was vetoed. A
`Courtesy → {{be polite}}` card fails check 22's litmus (the answer is the label's own
dictionary sense) — Parker's stated corollary: a row that answers itself is padding, not
coverage. The one non-obvious practice in the descriptions (names/ranks, never "someone")
is taught as F-A's `Pitfall:`, which is the right surface for it.

**(b) The cross-card-exposure worry — `Meaning:` glosses on cards 1 and 4 spell out
sibling answers (F-B's c2, H-A's mechanism, I-B's audiences, I-C's exact "suggest an
alternative plan"; I-C's `Distinguish:` likewise restates I-B's Emergency→entire-team).**
Ruled in the drafter's favor — this is the house part-and-whole doctrine working as
designed, not a defect, on four grounds:
1. The leak surface is **Text + hints** — Back Extra renders only after answering, and a
   *sibling's* back is a further step removed.
2. Check 16 / rule 13 target **scenario/classify exemplar reuse** (answering by
   recognizing a neighbor's Ex). No scenario card here borrows a sibling's exemplar; I-B
   is a direct contrast card, not a vignette, and no fresh-exemplar obligation applies.
3. Parker's own design mandates exactly this exposure: `Roster:`/`Mnemonic:` lines put
   every sibling's answers on every family card's back ("the part and the whole in each
   flash card"). Rule 25's no-restating-on-the-back caveat is expressly scoped to
   **numeric value columns**, which interpolate; words don't.
4. The one place back-exposure would have been free rehearsal *within the same note
   family* is F-B — and F-B's own c1 card already shows "respectfully question or
   correct" visible (the nature of a two-way card), so trimming card 1's gloss would cost
   fidelity and buy nothing.
   The drafter's pre-emptive trim (removing "suggest an alternative plan" from I-B's
   `Distinguish:`) was verified in the shipped text and kept.

**(c) H2 (purpose: "both parties know they share the same understanding") in Back Extra,
not clozed.** Ratified. Clozed, it is a fuzzy 8-word decode-not-recall span; visible in
the stem, it paraphrase-leaks c2. The back is the only placement that neither leaks nor
pads.

**(d) PACE trigger meanings never clozed (Probe/Emergency glosses; Challenge's
"not corrected" left visible).** Ratified per check 22's litmus — each candidate blank is
the label's own sense ("Probe → look or ask to confirm", "Emergency → imminent serious
danger", "escalate when not corrected"). The discriminating *audiences* are tested (I-B),
the non-derivable Challenge content is tested (I-C), the trigger contrasts live on the
backs. Coverage over padding, per Parker's corollary.

**(e) `numeric`/`needs_human_check` "false by derivation."** Confirmed against
`verify_report.py` (lines 73–94): a drafter's `numeric: true` is kept, and
`needs_human_check` derives false when `verified_against` is recorded. The drafter's
handling was correct on F-A and H-A; the I-A inconsistency (stated count, `numeric:
false`) was the one slip — fixed (card 4).

**(f) I-D split out of I-C.** Ratified — see card 7 row.

## Cross-unit observations (noted only — no dedupe performed, per assignment)

- D4's L-block step 4 ("Communicate the plan to the team and implement it", idx 22) vs
  I-D: verified distinct — the five-step decision loop's step vs the idx-16 rule that the
  **leader** broadcasts a **challenge-altered** plan. Different claim; the drafter's
  no-merge call stands.
- F-A ("four elements of team communication") sits one nesting level below the
  five-essential-team-elements list (idx 7–8, another unit's blocks, "Effective
  Collaboration and Communication" being member #3). No same-fact collision, but the
  downstream consolidator should confirm the five-element card (wherever it lives) does
  not also enumerate the four communication sub-elements.

## Escalation

**Checker gap (systemic, not this batch's defect):** the `VALUE` regex in
`check_cards.py` has no unit branch for **liters** — `2 liters`, `10 liters`, `15 liters
per minute` (spelled out, no slash) all fail to match, so an oxygen-flow value on a card
whose drafter does NOT manually assert `numeric: true` would silently skip the safety
overlay. This is the same shape as the R51 "inches" hole fixed on 2026-08-12. H-A was
covered only because the drafter asserted the flag by hand. Suggested fix (with its own
regression case, per the house loop): add `liters?|L\b|lpm` to the unit alternation and a
spelled-out `per min(ute)?` alternative to the slash-rate branch. Not applied here —
outside this edit's scope.
