# Unit A — Vital signs at various ages + the age bands (marks 0, 1)

8 notes, 8 Anki cards (every note is a single `c1` group). File:
`work/emt/ch7_units/A_vitals_agebands_cards.json`

---

## Fact pass

### Mark 0 — TABLE 7-1 caption, p683 (`needs_visual: true`, `content: CAPTION_ONLY`)

The caption itself carries no fact. The unit's substance is (a) the 9x4 grid, read off the
rendered plate, and (b) three claims sitting in the mark's own `context` prose.

| Fact | Call | Where it went |
|---|---|---|
| Pulse by age (9 bands) | MUST-TEST | card #0 |
| Respirations by age (9 bands) | MUST-TEST | card #1 |
| Systolic BP by age (9 bands) | MUST-TEST | card #2 |
| Temperature by age (9 bands) | SUPPORTING | card #3 (lowest-yield in the unit — see "cuts") |
| The adult set, identical in all three adult bands | MUST-TEST | card #4 |
| Pulse/RR fall with age, BP rises with age | MUST-TEST | card #6 |
| 140 + 60 = normal in an infant, life-threatening in a 30-year-old | MUST-TEST | card #7 |
| Footnote "ranges may vary in different sources" | SKIP | hedge, not a testable fact |

### Mark 1 — neonate / infant definitions, p685

| Fact | Call | Where it went |
|---|---|---|
| Neonate = birth to 1 month | MUST-TEST | card #5 (row 1) |
| Infant = 1 month to 1 year | MUST-TEST | card #5 (row 2) |
| The first 12 months split into two named stages | SUPPORTING | card #5 Back Extra (`Distinguish:`) |
| "See Chapter 34 for the neonatal period" | SKIP | cross-reference, not content |

**No mark went uncarded.** Both marks are covered; nothing was silently dropped.

---

## Card shape — why it is 8 notes and not 36

The grid was split **by column, not by row**. Each vital sign is one grouped-reveal card
covering all nine bands, because the discrimination NREMT actually tests is "what is a
normal pulse for a toddler," not "recite the toddler row." Row-splitting would have
produced 36 micro-cards; a single 36-blank card is unanswerable. Four column cards plus one
cross-column adult card is the shape that matches how the knowledge is used.

Identical adjacent values are merged into one row rather than repeated (SBP "Toddler and
preschool age — 80 to 100"; temperature "Preschool age through older adult — 98.6°F"), so
no row is padding.

**Units live in the lead-in** on cards #0-#2 (`in beats/min`, `in breaths/min`, `in mm Hg`)
rather than being repeated in six blanks — licensed by `card-recipes.md` §5 ("strip the
unit out only when the stem already prints it"). Cards #3 and #4 carry mixed units, so
there the unit sits inside each cloze.

**Marks merged:** mark 1 was folded into card #5 with mark 0's Age column (`from_idx:
[0, 1]`) — the neonate/infant boundary is one leg of the nine-band ladder, and carding it
separately would have been an R12 duplicate. Card #5 keeps all nine bands in one note per
Parker's "big lists stay whole" rule; it is the heaviest card in the unit (9 blanks) and
that is deliberate.

**No separate two-way neonate/infant definition card** was made, on purpose: card #5
already tests band-name → age range, and unit B (`B_neonate_physical`) owns the neonate as
a subject. If consolidation wants the reverse direction (age → band name), it should add
it once, globally, not per unit.

**Cross-card leak avoided:** cards #0-#3 label their rows with band NAMES only and never
print the age ranges, because the ranges are card #5's answers. Do not "helpfully" add
`(0 to 1 month)` back into those row labels during consolidation — it hands card #5 away.

---

## THE NEXT STAGE MUST KNOW

### 1. The briefing's adult-collapse framing is factually wrong — do not propagate it

The drafting instruction said the bands "adolescent through older adult collapse to one set
of values (60-100, 12-20, 90-130)." **That is wrong for blood pressure.** Read off the
plate:

- Adolescent (12-18 y): pulse 60-100, resp 12-20, **systolic 90 to 110**
- Early / middle / older adult: pulse 60-100, resp 12-20, **systolic 90 to 130**

Pulse and respirations reach adult values at adolescence; systolic BP does not until 19.
Card #4 is scoped to the three *adult* bands only, and carries the adolescent exception as
its `Distinguish:` line. **If any sibling unit or the consolidation pass repeats
"90 to 130 from adolescence on," it is a wrong card — kill it.**

### 2. `visual_source` shape: I wrote the dict, the brief asked for a bare string

The brief specified `"visual_source": "figures/TABLE_7_1.png"`. The canonical shape is a
**dict** (`reference/provenance.md` line 33), and the bare string is a live hazard:

- `scripts/attach_figures.py:307` — `vs = c.get("visual_source") or {}` then
  `vs.get("figures")`. A bare string is truthy, so this becomes `str.get(...)` →
  **`AttributeError`, crashing the figure-attach stage** for the whole segment.
- `scripts/match_figures.py:93` reads defensively (`isinstance(vs, dict)`), so a bare
  string is silently *ignored* there instead — the card loses its page hint.
- `check_cards.py:614` only tests truthiness, so both shapes clear R13 equally.

I wrote the dict (`pages: ["683","684"]`, `figures: ["figures/TABLE_7_1.png"]`,
`labels: ["TABLE 7-1"]`). **Sibling units that followed the brief literally will have bare
strings — normalize them to dicts before `attach_figures.py` runs.**

### 3. Figure placement: TABLE_7_1 must land on the BACK

The plate is a complete answer key for cards #0-#5. `image_side` defaults to `back`, which
is correct here — leave it. Front placement would destroy six cards at once
(`note-format.md`: "higher answer-coverage is a stronger reason to put the image on the
back").

### 4. Two checker warnings, both benign — clear them, do not "fix" them

- `#0 & #1: 86% similar Text — possible duplicate`. **Not a duplicate.** Pulse and
  respirations are different columns with deliberately identical row skeletons. Meaning-
  dedupe (R12) must not merge them.
- `#5: row label 'Older adult' shares ['older'] with its own answer '61 years and older'`
  (R20). The tested content is the number **61**; "and older" is the source's phrasing of
  an open upper bound, and "Older adult" cues nothing numeric. Kept the book's wording
  rather than distorting it to silence a detector documented as deliberately generous.

### 5. `verify_report.py` will rewrite the flags — expected

Every card carries `verified_against`, so `derived = (numeric or weak) and not verified` is
False and **all 8 will have `needs_human_check` flipped to `false`**. That is the intended
semantics (verified against the rendered plate = already human-checked); Section A of the
verify report is correctly empty. I drafted them `true` per the brief; the flip is
normalization, not a regression.

### 6. Detector gap found: `VALUE` does not match `beats/min` / `breaths/min`

Card #7's Text carries "140 beats/min", "60 breaths/min", "30-year-old" and
`check_cards.VALUE` matches **none** of them — the regex has `/min` as a unit but not
`beats/min`, and `30-year-old` has no second digit for the range branch. So #7 derives
`numeric: false` and drops out of the verification report entirely.

Not a problem for this card (its digits are verbatim in mark 0's own `context` field,
grounding `EXACT`, and I recorded that in `verified_against` / `verified_by`). But
`N beats/min` is the single most common numeric notation in this textbook, so any future
card using it without a range will silently escape the numeric gate. Worth a one-line fix
to `VALUE` in `scripts/check_cards.py`.

### 7. Deliberate overlap for consolidation to rule on

Card #4 (adult set) restates the last row of #0, #1 and #2. Kept on purpose: "what are
normal adult vitals" is the highest-frequency retrieval in EMS and is a cross-column read
that the three ladder cards never train (encoding specificity, card-rules #8). If
consolidation judges it an R12 duplicate, **cut #4, not the ladder rows** — and if #4 is
cut, move its `Distinguish:` line (the adolescent 90-110 exception) onto card #2.

### 8. Source tension on card #7 — the prose and the grid disagree

The p683 prose calls a pulse of 140 with respirations of **60** "usually normal for an
infant." The grid puts infant respirations at **25 to 50**; 60 breaths/min is above the
infant band and falls only inside the *neonate* band (30 to 60). The book contradicts
itself.

Card #7 is built to be safe either way: both ages are **visible** in the stem and the only
blanks are the binary normal/life-threatening judgement, so the card never asks Parker to
name the age group from those digits. An earlier draft that clozed the age group was
discarded for exactly this reason. Flagging it because Parker may notice the mismatch while
studying — the honest answer is that the textbook's prose is loose, and the grid governs.

### 9. Cheapest cut if the chapter runs long

Card #3 (temperature) is the lowest-yield note here — NREMT does not test age-banded
temperatures, and 98.6°F holds from preschool age on. It exists so the fourth column is not
silently dropped. Cut it first.
