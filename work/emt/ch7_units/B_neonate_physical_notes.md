# Unit B — neonate/infant physical (weight, airway, pulmonary) — drafting notes

Marks: 2, 3, 4, 5 (p687 weight passage) · 6, 7, 8 (p688 airway/chest passage) · 9 (p689 barotrauma).
Output: 8 notes → 13 Anki cards (notes 2, 3, 7 make two each; note 8 makes three).
`check_cards.py` deterministic pass: clean, stamped.

## Fact pass

| Mark | Fact | Call |
|---|---|---|
| 2 | Birth weight 6–8 lb (3–3.5 kg) | **MUST-TEST** → card 1 (row 1) |
| 3 | Head ≈ 25% of body weight; consequence: land headfirst when they fall | **MUST-TEST** → card 2 (both halves) |
| 4 | First week: weight falls 5–10% from fluid loss | **MUST-TEST** → card 1 (row 2) |
| 5 | Regain from week 2; ~1 oz (30 g)/day; ×2 by 4–6 mo; ×3 by 1 y | **MUST-TEST** → card 1 (rows 3–5); its context tail (can't extend arms to break a fall) → card 2 Back Extra |
| 6 | Neonates primarily nose breathers; <6 mo susceptible to nasal congestion → viral URI; choking baby → clear the nose | **MUST-TEST** → cards 3 (fact) + 4 (application) |
| 7 | Tongue larger vs oral cavity; airway shorter/narrower; oversized occiput; flexible trachea; obstruction more common; positioning is the EMT's job; hyperextend/hyperflex obstructs | **MUST-TEST** → cards 5 (Parker's grouped-reveal list) + 6 (positioning) |
| 8 | Rib cage less rigid, ribs horizontal → diaphragmatic (belly) breathing; also carries the full hyperextend/hyperflex sentence | **MUST-TEST** → card 7; the positioning sentence → card 6 |
| 9 | Infant lungs fragile; forceful BVM/overinflation → barotrauma; immature muscles, few alveoli, low O2 need, poor compensation | **MUST-TEST** → card 8 (two-way def + cause); the compensation physiology is SUPPORTING → Back Extra |

No mark was dropped and none needed flagging as un-cardable.

## Rule 0 merges

- **Marks 2, 4, 5 → one card.** Birth weight, first-week loss, regain rate, doubling and
  tripling are five points on ONE trajectory, so they are a single grouped-reveal timeline
  (five blanks, same `c1`), not four numeric fragments. Parker's "big cohesive lists stay
  whole" applies: the set is the weight story of the first year.
- **Mark 3 split out of that timeline deliberately.** Head-as-25%-of-body-weight is a
  different axis (proportion, not trajectory) and it carries its own field consequence, so
  it is its own two-cloze card: the number and the headfirst-landing implication anchor each
  other. That is the "number plus the action it triggers" flip from `profiles/emt.md`.
- **Mark 6 → two cards, on purpose.** The fact card and the application card could not be
  merged: any stem that says "neonates are nose breathers" hands over the answer to "what do
  you clear on a choking-infant call" (R3 leak). Separating them is what keeps the vignette
  honest. This is the ONE application card the brief licenses for infant airway.
- **Marks 7, 8 → two cards.** The four anatomic differences (Parker's list card) and the
  positioning rule are distinct: one is anatomy to produce, the other is a do/don't. Mark 8's
  context carries the complete hyperextend/hyperflex sentence that mark 7's context truncates,
  which is why card 6 cites `from_idx [7, 8]`.

## Parker's margin comment (mark 7) — what I built

Grouped-reveal list card, all four items under `c1`, each row **leading with its cloze** so the
ITEM is the answer (R17/R22 — no showing the items and punching out filler), rows separated by
`<br><br>` (R14/R19) so the four blanks and therefore the count are visible at a glance:

- a larger tongue relative to the size of the oral cavity
- a proportionally shorter and narrower airway
- a proportionally oversized occiput
- a more flexible trachea

**Deliberate choices the next stage should not "fix":**

1. **No count in the stem.** Parker's comment suggested "list three main things," but the
   source's own enumeration is open — p688 says "Due to factors <i>such as</i> the
   proportionally oversized occiput, the increased flexibility of the trachea, and the
   infant's limited or absent ability to reposition…" Parker's preference file forbids
   carding a "such as" list as a closed memorize-these set, so I did not assert "four."
   The four visible blank rows give him the count without the card claiming the book closed
   the list. If a later pass wants a stated count, it needs a source sentence that closes it.
2. **"Nose breathers" is NOT in the list.** It is grounded and adjacent, but it is a
   functional fact about *neonates* with a different action attached (clear the nose), and it
   already owns cards 3 and 4. Adding it would blur the anatomic set and duplicate a card.
3. **"Limited or absent ability to reposition" is NOT in the list either** — it is not an
   anatomic difference of the upper airway, it is why positioning falls to the EMT. It lives
   in card 6's Back Extra, which also keeps it from leaking into card 5's answers (R13).

## Numeric / human-check flags

Cards 1, 2, 3, 4 carry `numeric: true` + `needs_human_check: true`.
Card 4's only number is the invented vignette age ("2-month-old"); it is flagged per the
brief's blanket rule, but the digit to verify is really just that 2 months sits inside the
source's "younger than 6 months" band. Cards 5–8 carry no numbers.

## For the consolidation stage

- **No overlap with neighbours.** Unit A owns the neonate/infant age-band definitions and
  TABLE 7-1; unit C owns reflexes and fontanelles. Nothing here touches TABLE 7-1, so no card
  in this unit needs `visual_source`, and none is `needs_visual`.
- **Watch for a dedupe collision on head size.** Card 2 tests head = 25% of body weight.
  Unit C's mark 14 (cranial bones not yet fused) and the fontanelle cards live on the same
  anatomic theme; if another unit also cards "the infant head is proportionally huge," keep
  mine (it carries the headfirst-fall consequence) and drop the duplicate.
- **One fact left visible-but-untested on purpose:** "airway obstruction is more common in
  infants than in older children and adults" is the lead-in frame of card 5 rather than its
  own card — alone it would be a one-word coin-flip card. Flagging it in case consolidation
  would rather test it somewhere.
- **Two Back Extra lines are grounded glosses, not verbatim source**, in case the editor pass
  wants to strike them: card 6's "tipping the head too far back … chin drop toward the chest"
  (the plain-English meaning of hyperextension/hyperflexion) and card 7's "abdominal movement
  by itself is not a sign of distress" (corollary of the book's "typically seen in infants").
  Everything else on every card traces to the `context` of its `from_idx` marks.
- A `B_neonate_physical_cards.json.verified` stamp exists from the unit-level check; it will
  be invalidated by any edit and does not carry over to the merged chapter file.
