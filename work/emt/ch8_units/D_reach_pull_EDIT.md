# D_reach_pull — adversarial edit

Editor: independent pass, all checks 1–30 run per card, 18–24 per row. Fact pass re-run
from `D_reach_pull.json` before editing. Drops: none.

## Verdict table

| Card | Verdict | What changed |
|---|---|---|
| D1 (one-at-a-time polarity) | PASS | Nothing. Ex-line digits independently re-verified verbatim against mark 4's context ("stop and move back another 15 to 20 inches (38 to 50 cm)", p763). |
| D2 (kneel on the bed) | REWRITE (Back Extra only) | Cue line's overgeneralization removed: "the safe-pull posture is kneeling" contradicted caption C in mark 5's own context, which assigns knee-BENDING (not kneeling) to different-height pulls. Now "kneeling recurs in safe pulling — …". Text untouched. |

## Judgement calls

1. **D1 polarity — mandated hinted-binary shape confirmed fair.** Forced-choice hint
   present as required; knower recalls the rule, non-knower has no visible decode (the
   whys that would decode it — jostling / sudden spine force — are correctly on the
   back; any visible why-scaffold lets a reasoner derive the answer, exactly as the
   drafter's leak analysis found).
2. **D1 numeric-flag policy — correct as drafted.** The Text has no digits; the Ex line
   carries 15-to-20 in / 38-to-50 cm. The brief's rule is unscoped ("every number…"), a
   wrong Back-Extra digit is still a taught wrong digit, and the drafter verified and
   recorded `verified_against: "p763"` / `verified_by: "agent"`. I re-checked the digits
   verbatim; match. "Move yourself back" is the correct reading of the source's
   ambiguous "move back" (the reposition step is the EMT's, per the alternating-cycle
   sentence).
3. **The whys stay Back-Extra-only — drafter upheld after testing the alternative.** A
   whys-production sibling ("moving one at a time prevents ___ and ___") fails in the
   reverse direction: with the rule visible, a non-knower derives both answers by plain
   reasoning (both-at-once → jerky combined motion → jostling + sudden spinal load), so
   the card tests reasoning both populations have. Retention glue, not retrieval
   targets. No sibling added.
4. **D2 open-action blank — cold-solved honestly, hint carries real weight.** Without
   the hint, "If you must drag a patient across a bed, ___" is rule-16 bait (use a
   sheet? get help? lower the bed?). With `::your position`, the answer space collapses
   to postures/locations, and the book's counterintuitive answer (get ON the bed and
   kneel) is the one a knower produces; "kneel beside the bed" is precisely the wrong
   answer the card exists to beat, and the hint does not steer to it. Non-knower decode
   is blocked because the purpose ("avoid reaching beyond the recommended distance") is
   on the back — visible, it would hand a reasoner the answer (closer = on the bed).
   Verified the drafter's P7 placement is load-bearing; do not move the Why forward.
5. **Rule-11 prerequisite ("recommended distance") — closed within the card.** The term
   appears only in the Back Extra and is glossed in the same line by caption B's elbow
   rule ("elbows … only just beyond the front of your torso"), grounded verbatim in
   mark 5's context. No dangling term on the front.
6. **D2 Cue fix rationale (the one real fidelity catch):** caption C in mark 5's context
   reads "Bend your knees to pull a patient who is at a different height than you are"
   — so kneeling is NOT "the" safe-pull posture universally, and the draft Cue taught a
   small overgeneralization. The rewrite keeps the two genuine kneel cases (caption A
   ground pull; the highlighted bed rule) without the universal claim. Caption C's
   content itself stays uncarded (unmarked) and now also un-asserted.

## Hand-off flags

1. **Near-duplicate across units (needs an orchestrator call): D2 vs E_bed_transfers
   card 3.** E3 tests `{{c1::kneel on the hospital bed::your position}}` inside the
   stretcher-to-hospital-bed body drag (mark 7); D2 tests `{{c1::kneel on the
   bed::your position}}` as the general reach rule (mark 5). Same core answer, same
   hint, different marks and framing. Rule 12 tolerates a second card only for a
   genuinely new qualifier — E3's two-EMT transfer procedure arguably qualifies, but in
   the shuffled megadeck the two will feel like the same card. Options: keep both
   (each covers its own yellow mark) or fold the transfer framing into one card at the
   orchestrator level. I did not touch E (outside my units).
2. Unmarked-but-tempting inventory carried forward from the drafter, all still
   undrafted (R40): the 15-to-20-inch repositioning cycle values (Back-Extra support
   only), the ~15 in arms-extended figure (unused), the >1-minute strenuous-effort
   rule (unused anywhere), the elbows-beyond-torso reach limit (prereq-closure support
   only), the bend-knees/balance-force guidance (now unused after the Cue fix).
