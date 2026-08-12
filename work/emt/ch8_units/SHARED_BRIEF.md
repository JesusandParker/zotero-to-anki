# Chapter 8 — Lifting and Moving Patients: shared drafting brief

You are drafting Anki cloze cards for ONE OR MORE units of EMT Chapter 8. Read the
standards FIRST, in this order, from
`/Users/parkerregner/.claude/skills/zotero-to-anki/reference/`:

1. `card-rules.md`  — the full standard. Rule 0 (group connected marks) before anything.
   Rules 16–22 are the Cold-Solve Gate and they run **per ROW**, not per card.
   Rules 23–25 are retrieval load. Rule 26 (procedures = decisions, never step
   recitation) is THE rule of this chapter.
2. `parker-preferences.md` — Parker's tastes; these WIN on conflict.
3. `card-recipes.md` — pick the archetype, then follow its template exactly.
   **§12 (Procedures & Skills) is the playbook for every Skill Drill unit.**
4. `profiles/emt.md` — the subject emphasis.
5. `note-format.md` — the exact JSON card object + Back Extra vocabulary.

## What kind of chapter this is

Lifting and Moving Patients is listed as a **recall-heavy** chapter in `profiles/emt.md`
§2 — but it is really a **procedures chapter**: body mechanics rules, carries, drags,
and five marked Skill Drills. Two consequences:

- **Never card a step recitation.** Per card-rules #26 / recipes §12, a drill or
  protocol is carded as: the indication ("when do you reach for THIS move instead of
  the alternative?"), the discriminating comparison, the contraindication or the step
  people get wrong, the decidable residue (positions, named end-states, values,
  confirmation cues), and at most a decision-point vignette. NEVER "list the N steps."
  `check_cards.py step_recitation` warns on position-cued rows; in this chapter treat
  every such warning as a real finding.
- Scenario auto-pairing is **light** (recall-heavy chapter), but genuinely
  decision-shaped facts (rapid extrication indications, positioning by condition,
  urgent-move triggers) deserve decision framing because that IS what the source
  teaches.

## Non-negotiables specific to this run

- **Cards come ONLY from the marks in your unit file(s)** (card-rules #29, R40 HARD
  gate). Context paragraphs ground and support; they do not license new cards on
  unmarked facts. If context-only material seems card-worthy, note it in your
  `_notes.md` for the hand-off — do NOT draft it.
- **Ground every claim in the `context` field of the marks you were given** or in the
  VERIFIED BLOCK below. If a fact is in neither, you may not assert it. Flag it.
- **`from_idx` is REQUIRED on every card** — the `_idx` values of the mark(s) the card
  was built from. The gate verifies grounding against exactly those marks.
- **Every number, distance, weight, count or time window → `"numeric": true`**, and
  record `verified_against: "p<page>"` + `verified_by: "agent"` ONLY if you checked the
  digits verbatim against the mark's own context/highlight text. Otherwise leave them
  null. `needs_human_check` is DERIVED by `verify_report.py` — never assert it by hand
  (you may set it `false` in the JSON; the report recomputes).
- **Two-way definitions by default** for term↔meaning facts:
  `{{c1::TERM::hint}} is {{c2::crisp 3-6 word meaning}}`. Never both halves under one
  number (R10 husk).
- **List rows get `<br><br>` between them**, never a single `<br>` (R14).
- Allowed HTML: `<b>`, `<i>`, `<br>`, `<img>`. Nothing else.
- Back Extra is required, opens with a labeled line from:
  `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:`
  `Mnemonic:` `Roster:`. Separate components with `<br><br>`. It must teach something
  the Text does not state — never re-define a term the card already defines.
- **`block`** on every card = your unit name (e.g. `K_rapid_extrication`).
- **`image` / `image_side`: leave both out entirely.** Figures are attached by a later
  pipeline stage (judged composites). If a claim is only supported by the VERIFIED
  BLOCK below, set `visual_source` exactly as instructed there.
- Card JSON shape (see `note-format.md`): `Text`, `Back Extra`, `source: "emt"`,
  `segment: 8`, `from_idx: [...]`, `block`, `numeric`, `verified_against`,
  `verified_by`, `needs_human_check: false`, `visual_source` (only when licensed
  below), and NO `image` key.

## VERIFIED BLOCK — facts read off rendered pages (the PDF text layer does NOT carry these)

Any card whose answer leans on one of these MUST set the `visual_source` value given
here verbatim (the file paths resolve under `work/emt/`, which is what the R13/R33 gate
verifies). Claims NOT listed here and not in your marks' context are off-limits.

### 1. Solo removal of an unresponsive patient from a vehicle — completion of mark 17's sentence (p801)
Mark 17's context cuts off at "Then rotate the patient so that his or her". Page 801
(read from `work/emt/page_801.png`) continues, verbatim:

> "…back is positioned toward the open vehicle door. Next, place your arms through the
> armpits and support the patient's head against your body (FIGURE 8-15A). While
> supporting the patient's weight, drag the patient from the seat. If the legs and feet
> clear the vehicle easily, you can rapidly drag the patient to a safe location by
> continuing this method (FIGURE 8-15B). If the legs and feet do not clear the vehicle
> easily, you can slowly lower the patient until he or she is lying on his or her back
> next to the vehicle, clear the legs from the vehicle, and, as previously described,
> use a long-axis body drag to move the patient a safe distance from the vehicle."

And, same page:

> "You should use one-person techniques to move a patient only if an immediately
> life-threatening danger exists and you are alone or, because of the pressing nature
> of the danger, your partner is moving a second patient simultaneously."

License: `"visual_source": {"pages": ["801"], "figures": ["page_801.png"], "note":
"continuation of the one-person vehicle removal + the one-person-technique indication,
read from the p801 render"}`

### 2. Rapid extrication vs vest-type device timing (p803)
Page 803 (read from `work/emt/page_803.png`), verbatim:

> "Normally, you would use an extrication-type vest or short backboard device to
> immobilize a seated patient with a suspected spinal injury before removing the
> patient from the vehicle. … However, proper placement of either of these devices on
> the patient usually requires between 6 and 8 minutes, and in some cases even longer.
> By using the rapid extrication technique instead, the patient can be moved from
> sitting in the vehicle to supine, on a backboard if required, in 1 minute or less."

(The "1 minute or less" half is ALSO in mark 18's context, so it grounds normally;
only the 6-to-8-minutes half needs this license.)

Also p803, the Urgent Moves lead-in (context for framing only — it is UNMARKED, so it
may support a stem or Back Extra but must not become its own card):

> "An urgent move may be necessary to move a patient with an altered level of
> consciousness, inadequate ventilation, or shock (hypoperfusion). An extreme weather
> condition may also make an urgent move necessary. … When a patient who is sitting in
> a vehicle must be urgently moved, use the rapid extrication technique."

License: `"visual_source": {"pages": ["803"], "figures": ["page_803.png"], "note":
"6-to-8-minute vest/short-backboard placement time, read from the p803 render"}`

### 3. TABLE 8-3 completeness (p803–804)
The table has exactly SIX situations, all present in mark 18's context (four on p803,
two at the top of p804). The rendered plate `work/emt/figures/TABLE_8_3.png` shows all
six. Count against the context, not against any single page.

### 4. FIGURE 8-14 drag-method names (p800, in mark 16's context)
"A. Emergency clothes drag. B. Blanket drag. C. Arm drag. D. Arm-to-arm drag." These
four names are the book's own labels for the four floor/ground moves in marks 15–16 —
they ground normally via mark 16's context.

## Known step counts (for cross-checking drill claims against context)

Skill Drill photo-panel counts from the fig index: 8-9 → 3, 8-10 → 3 (but its context
shows FOUR "Step N" captions — trust the CONTEXT text for facts; the composite
discrepancy is handled at the figure stage, not by you), 8-11 → 4, 8-12 → 4. The
numbered TEXT lists in context are the full procedures (8-9 has 5 numbered items,
8-10 has 6). You are not carding step counts anyway (rule 26) — this is only so a
Back-Extra claim never contradicts the source.

## Deliverables, per unit

Write into `work/emt/ch8_units/`:
1. `<UNIT>_notes.md` — your fact pass: every atomic proposition in the marks + context,
   tagged MUST-TEST / SUPPORTING / SKIP, the archetype chosen per card, and any flags
   for hand-off (unmarked-but-tempting content, ambiguities, grounding gaps).
2. `<UNIT>_cards.json` — a JSON LIST of card objects in the exact note-format shape.

Do not touch any file outside `work/emt/ch8_units/`. Do not run `check_cards.py`
(the orchestrator runs the gate after the editor pass).
