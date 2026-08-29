# JUDGE A — verdict report, chapter 10 cards 0–84

Independent LLM judge pass (final quality gate), 2026-08-29. Scope: array indices 0–84 of
`work/emt/chapter_10_cards.json`, every editor-checklist check run per card and per row,
plus the batch-wide cross-card give-away sweep (check #16) across all 254 cards.
Grounding read against `chapter_10_highlights.json` (marked spans + contexts), with page
renders pulled for p949, p950, p951 where a table/count needed the real page.

**Per the orchestrator's process change, no in-place edits were made.** All fixes are in
`work/emt/ch10_units/JUDGE_A_patch.json` (3 entries: indices 20, 23, 72), full replacement
cards keyed by current-file index. `from_idx` untouched everywhere. No re-stamp performed.

---

## 1. Checker-warning adjudications (all 7 in range)

| # | Warning | Verdict |
|---|---------|---------|
| 17 | first-letter hints ::A ::U (AVPU) | **UPHOLD** the standing clearance. AVPU is a spelled mnemonic, bold in the stem; the book itself keys the four levels by letter (marks 13–16, p945–948). Exactly the rule-18 license (SAMPLE shape). 4 items, letter-cued — load fine. |
| 20 | husk: c1 hides 2 multi-word spans | **UPHOLD the husk clearance** (each blank was independently anchored by its visible level name) — **but the card is REWRITTEN anyway** for a different defect the clearance never covered: see §2, index 20. |
| 21 | husk: c1 hides 2 multi-word spans | **UPHOLD.** "Unresponsive patients usually have no ___ reflex and so lack the ability to ___" — the visible subject + slot frames make both blanks one causal unit a knower produces cold (cough/gag → can't protect airway). Not a husk; scaffold points at both answers. |
| 27 | says "four" but clozes 3 | **UPHOLD.** "Four" counts the orientation questions (visible anchor); the clozed list is the three memory tiers. Tier wording verified verbatim against the p950 render this pass (top of page: long-term = person+place; intermediate = place+time year/month; short-term = time day-of-week + event). Detector misfire. |
| 32 | answer "is" visible in stem | **UPHOLD.** The blank carries the mandatory forced-choice `::is / is not` hint (card-rules #13) — the options are on the front by design; the stem's other "is" tokens are grammar, not leaks. |
| 59 | absolute + unhinted blank | **UPHOLD.** "cannot palpate a carotid pulse" is a clinical finding inside a vignette, not a prohibition rule; the unresponsive + pulseless state forces exactly one first action (source verbatim, mark 45). This is card-rules #16's own sanctioned fix, not its failure shape. |
| 81 | "too slow" not in cited context | **UPHOLD.** "Too slow" is the applied verdict of the verified >2 s threshold (mark 69: "Suspect poor peripheral circulation when capillary refill takes more than 2 seconds"); "suspect poor peripheral circulation" is verbatim. Faithful paraphrase, not an addition. |

(Warnings #86, #90, #93, #102, #114, #123, #148, #155, #177, #194, #196, #214 are outside
my range — left to judges B/C.)

## 2. Fixes applied (in JUDGE_A_patch.json)

**Index 20 — REWRITTEN: flipped to the classify direction.**
Old form: "…{{c1::moving or crying out::response}} grades the patient P (responsive to
pain), while {{c1::staying flaccid…::response}} grades the patient U (unresponsive)."
The visible parenthetical expansions *(responsive to pain)* / *(unresponsive)* nearly
restate the hidden answers — a non-knower can decode "moving or crying out" from
"responsive to pain" (card-rules #3 decode path; the #20 label-restates-answer shape;
Parker's R15 quote: "you're giving away the answer while trying to give me a hint").
New form: two behavior rows → hidden AVPU grade ("The patient moves or cries out →
graded {{c1::P (responsive to pain)::AVPU grade}}" / flaccid row → U), the classify shape
check #22 explicitly blesses, and the clinically real direction (observe behavior → assign
grade). Complements sibling 19 (V-vs-P) without duplicating it. Added a grounded Cue
("moaning or withdrawing already counts as responding" — verified verbatim on the p949
render). Same facts, same `from_idx` [15, 16, 18], same page verification.

**Index 23 — TRIMMED to 58 words (was 67; Layer A #6 hard max is 60).**
Tightened the lead-in ("the three best sites") and the fourth row ("upward pressure along
the orbital rim (underside of the eyebrow)"). Wording re-verified against the p949 render
("apply upward pressure along the ridge of the orbital rim along the underside of the
eyebrow (without applying any pressure to the eyeball)") — faithful, no content lost;
the eyeball caution stays in Back Extra. List kept whole (4 cohesive site/technique rows,
count visible — splitting would hurt cohesion).

**Index 72 — Back Extra: dropped the `Formal:` line.**
`Formal:` is licensed on lexicon cards only (note-format.md), and this is a regular card;
quoting the glossary definition also re-defined the term on a definition card (Layer A #5).
The "tough shell" idea survives in the `Parts:` line. Cue/Distinguish/Parts retained.
See §3 for the purple-mark context on this card.

## 3. Cross-batch findings (check #16 sweep over all 254 cards, plus rule-12 dedupe)

**No hard rule-13 sibling leaks into my range.** Every scenario/classify card in 0–84 uses
a fresh exemplar not spelled out on any sibling's stem or Ex line (chainsaw cut, gym
collapse, limp 7-month-old, intoxicated driver, motorcyclist femur, bee-sting stridor
family, etc.). Card 34's femur exemplar is TABLE 10-1's own printed example (p951 render)
and no sibling prints it — clean.

**Benign, structural interferences (reviewed, deliberately left):**
- AVPU family: cards 18/20 necessarily print level expansions that card 17 hides — the
  anchor-vs-discrimination layering every mnemonic family has; bury-siblings spaces them.
- Card 57 visibly names "brachial" + infant while 55/56 hide it — the technique card must
  name the pulse to ask the maneuver; a third infant→brachial cloze would over-test.
- Cards 61–63 visibly state "pulse but not breathing → ventilations," which card 58 hides —
  rate/interval cards must state their condition+intervention; card 58 tests the decision.
- Card 77's road-race exemplar overlaps card 78's Ex quote ("after strenuous exercise…
  diaphoretic") — the book's own canonical example; the tested discrimination (soaked-through
  vs slight film) is intact and any correct exemplar must be a drenched patient. Cleared.

**Cross-batch DEDUPE flag for the orchestrator (out of my patch scope — cards 230/232 are
in another judge's range):** the 2-second capillary-refill threshold is carded twice —
my 83 (from marks 68/69, p968, primary-assessment skin check) vs 230 (neurovascular exam
section), and the application pair likewise: my 81 (4-year-old, 3 s) vs 232 (6-year-old,
4 s). Both pairs are individually sound and separately marked, but they test the same
claim (rule 12: dedupe by meaning). Recommend the orchestrator either merge 230/232 into
the 83/81 family or keep 230/232 with a Distinguish line justifying the second context
(extremity-local vs systemic). My cards need no change either way.

**Purple-lane surfacing (rule 28 requires this reach Parker's hand-off report):** purple
mark 58 ("sclera", p966) is the chapter's ONLY lexicon mark not served by a `kind: lexicon`
card — it is folded into yellow card 72 (cites yellow 56/57 + purple 58), which
`lexicon_check` explicitly sanctions as a fold-in. The term IS defined two-way on that card
(with Parts + Distinguish), and glossary evidence exists (`lexicon_evidence.json` 'scler',
p4122). Cost to surface: "scler" never enters the lexicon ledger, so a future purple
re-mark of sclera will not be recognized as a repeat. Either bless the fold-in as-is
(my recommendation — the card is good) or have the stager add a ledger entry manually.

## 4. Per-card sweep notes (everything else PASSED)

All 85 cards were run through every checklist row (1–30, per row on list cards). Beyond
the three fixes above: grounding traced to marked spans for every card (marks 0–71, 91,
103, 104 all cited, none dropped, none overruled); TABLE 10-1's 3+3+1 partition on cards
29–31 page-verified including the p951 spill (only the distracting-injury definition
continues — no missed rows); all numeric cards (10, 17, 23, 25, 27, 29, 30, 40, 42, 43,
55, 61–63, 73, 81, 83) carry `verified_against`/`verified_by` so the safety flag derives
correctly; "such as" lists correctly NOT carded as closed sets (cards 4, 65 — items visible
or slot-hinted, never a memorize-this blank); rosters present and self-bolded on every
chunked-family note (29–31, 52–53, 61–62); no deixis, no source-artifact words (all
detector hits were anatomy/idiom false positives — "above the collar bone", "playground
slide", "clinical picture"), no unlabeled Back-Extra chunks, no disallowed tags; layouts
use `<br><br>` rows throughout. Card 0's five-part grouped list (5 uncued) judged licensed
under check 25's structure-handle clause: the phases are a strict operational sequence and
the chapter's own spine, numbered rows show the count — noted here as a judged clearance.
Application-fit sanity check: ~26% of the range makes Parker decide something, meeting the
clinical-chapter bar. Margin comment on mark 39 ("THATS SO SAD") is an emotional aside,
not an instruction — nothing to honor beyond noting it.

## 5. Cards I could NOT fix (needs human)

**None.** No card in 0–84 required a fix I couldn't make. The two judgment calls I want
human/orchestrator eyes on are in §3 (the 230/232 dedupe decision, and blessing the
sclera fold-in for the ledger).
