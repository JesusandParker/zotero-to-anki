# C_power_grip — adversarial edit

Editor: independent pass, all checks 1–30 run per card, 18–24 per row. Fact pass re-run
from `C_power_grip.json` before editing. Drops: none. One card ADDED.

## Verdict table

| Card | Verdict | What changed |
|---|---|---|
| C1 (palm-up polarity) | PASS | Nothing. |
| C2 (10-inch numeric) | PASS | Nothing. Digits independently re-verified verbatim against mark 3's highlight ("at least 10 inches (25 cm) apart", p761); `verified_against`/`verified_by`/`numeric` correct as drafted. |
| C3 (name production) | ADDED | New card: indication → name, `{{c1::power grip::name of grip}}`, purpose clause deliberately absent from the stem. `from_idx: [3, 2]`. |

## Judgement calls

1. **C1's coin-flip — mandated shape confirmed fair.** A binary direction blank MUST
   carry the forced-choice hint (Layer A #4), so "50/50 for a non-knower" is by design,
   not a defect. What I verified: the knower's edge is real (the "greatest lifting
   strength" framing is exactly the book's fact the knower recalls as palm-up) and the
   non-knower has no DECODE from the visible text — nothing on the card implies a
   direction; folk physiology a reader brings is knowledge, not decoding. Passes
   knower-can / non-knower-can't.
2. **C2 and rule 27 — adjudicated satisfied, no hint added.** The trigger scope is a
   BARE quantity in an ATTRIBUTIVE slot; this answer carries its own operator + unit
   ("at least 10 inches (25 cm)"), and the slot "your hands should be ___ apart" admits
   only a separation-distance — "apart" after the blank does the announcing the way a
   trailing unit does. An adjective does not read naturally there (the carpals failure
   shape does not reproduce). Adding `::distance` would be over-hinting a slot the frame
   already constrains.
3. **The no-name-cloze call — PARTIALLY OVERRULED, burden met.** The drafter's core
   analysis is right and is preserved: the term↔purpose binding is untestable in either
   direction on one note, because the name's semantics ARE the purpose ("power" ↔
   "maximum force") — describe→name lets a non-knower coin the name; name→meaning
   decodes in reverse; and on a single note each direction leaves the other's leak
   visible. Any purpose-direction card is a padding card both populations can answer.
   BUT the two-way default demands a name-production direction if a non-decodable one
   exists, and one does: the INDICATION direction with the purpose suppressed —
   "Whenever you are lifting a patient, grasp the stretcher or backboard using the
   ___::name of grip." No power/force word is visible, so a non-knower cannot coin
   "power grip"; a knower is forced (the chapter names exactly one grip). Added as C3,
   a separate note (same-note placement re-leaks via the visible purpose on C1 — the
   drafter's own finding, re-verified). The drafter's suggested end-state route is also
   lawful but longer and less exam-shaped; the indication route matches how the fact is
   actually cued ("which grip when lifting?"). The purpose fact (P1) now lives visible
   on C1's front AND as C3's `Why:` — taught on both cards, blanked on neither, which is
   the only lawful treatment of a self-descriptive binding. The fact-pass line "P1
   MUST-TEST → tested as the visible binding" was a fudge (visible ≠ tested); C3 closes
   it in the one real direction.
4. **C3 sibling-reveal accepted.** C1's front shows "power grip" bold; C3 asks to
   produce it. This is the normal two-way-pair situation (the pair always co-reveals) —
   rule 13 targets scenario/classify cards defeated by pattern-matching, not
   definitional bindings, where recognizing the binding IS the fact. Since C3 is a
   separate note, bury-siblings will not space it from C1 — recorded as a known,
   house-tolerated cost (identical to every Distinguish/Roster cross-reveal).
5. **C3's Distinguish (power lift vs power grip) — grounded via cross-cite.** The
   power-lift definition ("lifting by extending the properly placed flexed legs") is in
   mark 2's context (unit B), hence `from_idx: [3, 2]`. It is the nearest confusable in
   the chapter ("power ___" family) and no unit cards the power lift (unmarked), so
   nothing is pre-revealed. Support line only; rule 29 untouched.
6. **End-state and insertion narration stay Back-Extra — drafter upheld.** The §12d
   component-cloze version ("underside on the {{curved palm}}, fingers over the
   {{top}}") is derivable from visible palm-up geometry, i.e. padding (rule 20's
   spirit); rule 26 licenses the narration as back-side reference. The thumb-phase
   separation (extended during insertion vs curled in the final grip) is preserved
   exactly as the drafter laid it out — do not merge the two lines.

## Hand-off flags

1. C3 is an editor-added card realizing the two-way default on marked content
   (mark 3's own indication sentence). If Parker finds name-production for "power grip"
   too easy in practice, C3 is the card to cut — C1/C2 stand without it.
2. C2's `needs_human_check: false` + verified fields is the brief's correct shape; the
   report will still surface it in the verified-numbers skim section.
