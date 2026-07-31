# Chapter 7 — Life Span Development: shared drafting brief

You are drafting Anki cloze cards for ONE unit of EMT Chapter 7. Read the standards
FIRST, in this order, from `/Users/parkerregner/.claude/skills/zotero-to-anki/reference/`:

1. `card-rules.md`  — the full standard. Rule 0 (group connected marks) before anything.
   Rules 16–22 are the Cold-Solve Gate and they run **per ROW**, not per card.
2. `parker-preferences.md` — Parker's tastes; these WIN on conflict.
3. `card-recipes.md` — pick the archetype, then follow its template exactly.
4. `profiles/emt.md` — the subject emphasis.
5. `note-format.md` — the exact JSON card object + Back Extra vocabulary.

## What kind of chapter this is

Life Span Development is a **recall-heavy** chapter (per `profiles/emt.md` §2), not a
clinical one. Age bands, normal ranges, developmental milestones, definitions. Do NOT
force scenario vignettes onto developmental definitions — the profile explicitly warns
against that. The auto-pair scenario rule is **light** here. The exception: normal
**vital-sign ranges** and any finding that changes field management (fontanelles,
infant airway, geriatric subdural) genuinely deserve one application card each.

## Non-negotiables specific to this run

- **Ground every claim in the `context` field of the marks you were given.** If a fact
  is not in your marks' context and not in the verified block below, you may not assert
  it. Flag it instead.
- **`from_idx` is REQUIRED on every card** — the list of `_idx` values of the mark(s)
  the card was built from. The gate uses it to verify grounding. Get it right.
- **Every number, range, age, percentage, dose or time window → `"numeric": true` and
  `"needs_human_check": true`.** This chapter is almost entirely numbers.
- **Two-way definitions by default** for term↔meaning facts:
  `{{c1::TERM::hint}} is {{c2::crisp 3-6 word meaning}}`. Never put both halves under
  the same cloze number (that is the R10 husk).
- **List rows get `<br><br>` between them**, never a single `<br>` (R14).
- Allowed HTML: `<b>`, `<i>`, `<br>`, `<img>`. Nothing else.
- Back Extra is required, opens with a labeled line from:
  `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:`
  Separate distinct components with `<br><br>`. It must teach something the Text does not
  already state — never re-define a term the card already defines.

## VERIFIED BLOCK — facts read off rendered pages (the PDF text layer does NOT have these)

### TABLE 7-1 Vital Signs at Various Ages (title p683, body is a rendered image on p684)
Read directly from the extracted plate `work/emt/figures/TABLE_7_1.png`. These digits are
the source of truth; do not adjust them, and do not import ranges from any other chapter
or from `card-recipes.md` (its examples are from a different table).

| Age | Pulse (beats/min) | Respirations (breaths/min) | Systolic BP (mm Hg) | Temperature (°F) |
|---|---|---|---|---|
| Neonate (0 to 1 month) | 100 to 180 | 30 to 60 | 50 to 70 | 98 to 100 (37°C to 38°C) |
| Infant (1 month to 1 year) | 100 to 160 | 25 to 50 | 70 to 95 | 96.8 to 99.6 (36°C to 37.5°C) |
| Toddler (1 to 3 years) | 90 to 150 | 20 to 30 | 80 to 100 | 96.8 to 99.6 (36°C to 37.5°C) |
| Preschool age (3 to 6 years) | 80 to 140 | 20 to 25 | 80 to 100 | 98.6 (37°C) |
| School age (6 to 12 years) | 70 to 120 | 15 to 20 | 80 to 110 | 98.6 (37°C) |
| Adolescent (12 to 18 years) | 60 to 100 | 12 to 20 | 90 to 110 | 98.6 (37°C) |
| Early adult (19 to 40 years) | 60 to 100 | 12 to 20 | 90 to 130 | 98.6 (37°C) |
| Middle adult (41 to 60 years) | 60 to 100 | 12 to 20 | 90 to 130 | 98.6 (37°C) |
| Older adult (61 years and older) | 60 to 100 | 12 to 20 | 90 to 130 | 98.6 (37°C) |

Footnote: "Vital sign ranges may vary in different sources."

Any card built on this table MUST carry `"visual_source": "figures/TABLE_7_1.png"` —
the mark is flagged `needs_visual`, so without visual evidence the gate HARD-blocks it (R13).

### The age bands the chapter uses (from TABLE 7-1 and the figure captions)
Neonate 0–1 month · Infant 1 month–1 year · Toddler 1–3 y · Preschooler 3–6 y ·
School-age 6–12 y · Adolescent 12–18 y · Early adult 19–40 y · Middle adult 41–60 y ·
Older adult 61 y and older.

### The tail of the p724 nervous-system passage (mark 52's context is cut off mid-sentence)
Verbatim from the source page:
> "Throughout life, the cranial vault is almost entirely occupied by the brain, the
> meningeal layers, and the cerebrospinal fluid between these layers. As such, there is
> virtually no empty space. However, in older adults, the age-related shrinkage of the
> brain creates a void between the brain and the outermost layer of the meninges. The
> resulting space gives the brain room to move inside the cranium (FIGURE 7-14). As such,
> any mechanism that causes a rapid or forceful shifting of the brain has the potential
> to result in the tearing of bridging veins. Subsequent bleeding into the open space may
> go unnoticed for some time."

## Parker's margin comments (his voice on the page — you MUST obey these)

- **On mark 7 (p688, infant tongue/airway):** *"One clever way to make this card would be
  to say something like guess all of the things different in an infant mouth than an adult
  or you could say something like list three main things that are different or something
  like that."*
  → He is asking for a **grouped-reveal list card** naming the ways an infant's upper
  airway differs from an adult's, rather than isolated fragment cards. Build it. The
  source supports these differences (p688): tongue larger in proportion to the oral
  cavity; airway proportionally shorter and narrower; proportionally oversized occiput;
  increased flexibility of the trachea. Neonates are also primarily nose breathers.
  Ground each item you include; do not pad the list to hit a number.

- **On mark 18 (p690, FIGURE 7-2 Fontanelles):** *"I want to see if you can add a
  high-quality screenshot like a high definition screenshot of this into the flashcards
  relating to the fontanelles."*
  → Do NOT try to attach it yourself. The figure pipeline runs after drafting and will
  attach `FIGURE 7-2` (2177×887 px, already extracted). Your job is just to make sure the
  fontanelle cards exist and use the word "fontanelle" prominently so the matcher finds
  them. Note in your unit's `notes` field that FIGURE 7-2 is wanted on these cards.

## Output

Write your unit's cards to `work/emt/ch7_units/<UNIT>_cards.json` as a JSON list of
objects in exactly this shape:

```json
{
  "Text": "...cloze markup...",
  "Back Extra": "Distinguish: ...<br><br>Pitfall: ...",
  "source": "emt",
  "segment": 7,
  "from_idx": [7, 8],
  "numeric": false,
  "verified_against": null,
  "verified_by": null,
  "needs_human_check": false,
  "visual_source": null,
  "image": null
}
```

Then write a short `work/emt/ch7_units/<UNIT>_notes.md` recording: your fact pass
(MUST-TEST / SUPPORTING / SKIP per mark), which marks you merged and why, any mark you
could NOT card and why, and anything the next stage must know.

**Every mark you were given must be covered by some card, or explicitly flagged.** Never
silently drop a yellow mark.
