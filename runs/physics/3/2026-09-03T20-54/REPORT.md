# Physics ch3 — Kinematics in Two Dimensions; Vectors (night unit 20260903-2046-1)

Giancoli 7e, night-shift unit scoped to **1 purple mark** on physical p. 72 (printed p. 51):
`resultant displacement`. **1 mark → 1 lexicon note** for
`…::PHYS 201 - General Physics I::Chapter 3 …::Book Highlights`, tag `physics-ch3`
(+ night tags `night::2026-09-03`, `night-unit::20260903-2046-1`).

## Scope
Stage 1 was pre-run by the night extractor; the unit file is the whole request (Rule 0 /
R40). No yellow marks in scope, no margin comments (`user_comment: null`), no
unsupported purples, no hygiene flags. Lexicon dedup: `result_displac` is a **new term**
— no ledger entry, no live-Anki collision, no colliding near-key. Cross-lane fold-in n/a.

## The card
`The <b>resultant displacement</b> is {{c1::the vector sum of the individual displacements}}.`
One-way (§4b default; matches all four accepted ch2 lexicon cards). Back Extra: `Ex:`
(verbatim p72 encounter sentence), `Distinguish:` (resultant magnitude vs distance
traveled, 11.2 km vs 15 km, **with the book's equality qualifier** — equal only when the
legs point the same way), `Cue:` (tail-to-tip). FIGURE 3-3 on the back.

## Anchor judgement (the run's main call)
`lexicon.py --find` matched p72 at distance 0, but its quote — *"resultant displacement
is represented by the arrow labeled DR in Fig"* — is a **representation sentence, not a
definition** (the Tier-1 pattern accepts passive verbs like "is represented by"). The
page's true definitional sentence (*"The resultant displacement vector, DR, is the sum of
the vectors D1 and D2"*) has an appositive between term and "is", which the pattern
cannot cross. Per the ch2 precedent (3 of 4 anchors kept external on non-definition
quotes), the anchor was kept **external + needs_human_check: true**, with the reason in
`verified_by` and `decisions.jsonl`. The deterministic gate's one WARNING (external vs
existing evidence entry) was adjudicated by BOTH the independent adversarial editor and
the independent LLM judge: **external is the honest tier** (claiming in_source on that
quote would be the R61 pressure failure). The authored answer agrees verbatim with the
page's own definitional sentence.

**Cleared warnings record (note-format "Recording that a WARNING was cleared"):**
`lexicon_check external-with-evidence cleared: the evidence quote contains no
definitional content to agree with; in_source would be self-asserted (editor + judge,
2026-09-03).`

## Editor & judge
- Independent adversarial editor: 1 real catch — the draft's `Distinguish:` stated the
  smaller-than-sum property as universal; p72 qualifies it (equality for collinear legs).
  Rewritten with the qualifier; line-initial pronoun replaced.
- Independent LLM judge: **PASS** (29/30 clean; the one non-clean item was an optional
  cosmetic quote-trim, declined in favor of verbatim quotation — the first editor had
  affirmatively endorsed the verbatim `Ex:`).

## Figures
- Fresh ch3 index: 37→38 figures (13-figure baseline was pre-ch3; the count anomaly in
  `figure_run --report` is this first full-chapter build, expected).
- **FIGURE 3-3 had no locatable art** (vector art), and the auto-associated
  `FIGURE_3_3.jpg` in the cache is **label-drifted chapter-opener car art** (the ch2
  hazard class, confirmed at the eyeball — do not use that file; debris left in cache,
  regenerates identically on rebuild).
- The real plate was produced by the proven vector-art route: full-page 450-dpi render →
  crop to the COMPLETE figure (caption included) → eyeballed clean (no bleed, no clipped
  labels) → `study_copy(lossless=True)` house matting → `figures/study/FIGURE_3_3_v2.png`
  (v2 name because the drifted debris occupies the base name).
- The matcher scored 0 proposals (it scores cloze answers only; the authored-definition
  answer shares no caption vocabulary, and the art was unindexed) → **forced proposal**
  per the FIGURE 7-2 precedent, judged with eyes on the actual study copy: keep, back
  side. `depicts` written back to `figure_index.json` permanently.

## Verification chain
`lexicon.py --find/--dedup` → fact pass → draft → independent adversarial edit →
consolidation (no-op, logged) → `verify_report` (Section A: 1 — the Vocabulary block) →
`check_block_spec` (17 requirements ✓) → `check_cards --highlights` (HARD-clean; 1
adjudicated warning; stamped) → independent LLM judge (PASS) → figure
index/match/forced-proposal/judge-look → `attach_figures --to-cards` → re-verified +
re-stamped → `figure_run --report --write-run`.

**Gate discovery caveat (the run's open hazard):** `check_cards`/`verify_report` resolve
highlights by the `<noun>_<segment>` convention, so the night-unit label required
explicit `--highlights` — without it the gate SKIPPED grounding/synthetic/lexicon checks
and still stamped (first invocation tonight did exactly that before being caught and
re-run properly). Recorded as an OPEN hazard in `manifest.json` — deliberately left
unclosed (mechanizable, but night runs don't edit shared gate code); `check_hazards.py`
stays red until a daytime session mechanizes it. Details + proposed regression shape in
the manifest entry.

## Outcome — write BLOCKED (Anki closed on the Mac)
AnkiConnect verified at 20:46 (orchestrator) and 20:52 (this session; dedup ran against
it). By the pre-write re-check it was gone: tunnel healthy, Mac awake, **no Anki process,
no crash report, profile prefs written 21:17 = clean quit** (Parker closed the app).
Polled 21:25–22:19; never relaunched Anki remotely (auto-sync-on-open risk; sync is
forbidden; not the night shift's call). **Nothing written — 0 notes.** The unit re-queues
automatically (marks unprocessed). The staged file is HARD-clean, stamped, judged, and
figure-attached; to land it by hand: open Anki, then
`python3 scripts/anki_write.py work/physics/night_20260903-2046-1_cards.json --run
runs/physics/3/2026-09-03T20-54`, add tags `night::2026-09-03 night-unit::20260903-2046-1`,
then `render_check.py` (look at it) and `media_audit.py --deck "…Chapter 3…::Book
Highlights" --prefix physics_`. If instead the unit simply re-runs tomorrow night, the
lexicon ledger/dedup makes either order safe (a prior manual write → the re-run skips as
duplicate and reports).
