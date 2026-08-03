# Chapter 8 run brief — Lifting and Moving Patients (p738–867)

Prepared 2026-08-03, before the run. Everything below was verified, not assumed.

## What is different about this chapter

**It is a procedures chapter, and procedures are a content type chapters 1–7 barely
contain.** Four of Parker's five visual marks are **Skill Drills** — numbered photo
sequences, one step per page. That whole path was untested until this prep and was broken
in three places (R29); it is fixed and tested now, but it is the part of the run to watch.

## State of the inputs (verified)

| | |
|---|---|
| Marks | **32**, all yellow, **32/32 grounded EXACT** |
| Margin comments | **none** — no `user_comment` to honor this chapter |
| Needs a visual read | **5**: TABLE 8-3 (p803) and Skill Drills 8-9, 8-10, 8-11, 8-12 |
| Figures indexed | **39** for ch8 — 27 FIGUREs, 1 TABLE, **11 SKILL DRILL composites** |
| No locatable art | TABLE 8-1 and TABLE 8-3 — **correct, not a defect**: both are live text in the PDF, not embedded rasters, and their bodies are in the extractor context |

TABLE 8-3's four bullets are confirmed present in mark 18's context, so cards from it
ground normally and need no plate.

## Skill Drills — what the pipeline now does

A drill is composited into **one plate showing the whole procedure**: the banner, every
step's photo and caption in order, and the full numbered step text. That is the artifact
that belongs on the back of a procedure card, and it is the same part-and-whole design
Parker asked for with tables ("disconnected for memorizing, connected by the table").

Step counts, for cross-checking during the run: 8-2 → 3, 8-3 → 3, 8-4 → 2, 8-5 → 2,
8-6 → 4, 8-7 → 8, 8-8 → 3, 8-9 → 3, 8-10 → 3, 8-11 → 4, 8-12 → 4.

**Watch for:** a composite whose step count looks wrong for the procedure. The walk stops
at the next caption or the first page with no step heading, so a drill interrupted by a
figure mid-procedure could end early. Check the count against the drill's own numbered
list, which is in the context text.

## Card-shape rules that will bite hardest here

- **Rule 23 (retrieval load).** A drill's steps are an ordered list; ≥8 uncued answers is a
  HARD block. Skill Drill 8-7 has **8 steps** — it must be chunked into named phases on
  separate notes, never c1..cN on one note (rule 24). The composite goes on each phase
  note's back so the whole procedure stays in view.
- **Rule 25 (value columns).** Watch for weight limits, patient/device capacities and
  lifting thresholds keyed by device — those are one note per key with the table on the back.
- **Recipes §7 (sequences)** is the archetype for drills: arrows and connectives stay
  visible outside the clozes, order is the knowledge.
- The **anchor-note trap** (rule 23's refinement): if you partition a drill into phases,
  the phase NAMES are yours, not the book's — keep them visible in each note's stem and do
  not cloze them. Test the order with a grounded "you have just done X, what comes next?"
  vignette instead.

## Commands, in order

```
python3 scripts/extract_highlights.py --source emt --segment 8          # already run: 32 marks
.venv/bin/python scripts/build_figure_index.py --source emt --segment 8 # already run: 39
python3 scripts/figure_run.py --source emt --segment 8 --preflight
#   ... draft per SKILL.md Stage 2, one unit at a time, independent editors ...
python3 scripts/verify_report.py work/emt/chapter_8_cards.json
python3 scripts/check_cards.py    work/emt/chapter_8_cards.json
.venv/bin/python scripts/match_figures.py --source emt --segment 8 --json work/emt/ch8_figure_proposals.json
python3 scripts/judge_figures.py --source emt --segment 8 --emit  work/emt/ch8_judge_worklist.json
#   ... LOOK at every plate, fill in `depicts`, keep/drop each card ...
python3 scripts/judge_figures.py --source emt --segment 8 --apply work/emt/ch8_judge_verdicts.json
python3 scripts/attach_figures.py --source emt --segment 8 --to-cards   # FRESH segment route
python3 scripts/check_cards.py work/emt/chapter_8_cards.json            # re-stamp after attaching
python3 scripts/anki_write.py  work/emt/chapter_8_cards.json --run runs/emt/8/<run_id>
```

Chapter 8 has never been staged, so it takes the **`--to-cards` fresh-segment route**.
Never run `anki_write.py` on an already-staged chapter — it adds notes rather than
updating them.

## Open question for Parker, worth settling before the run

Skill Drill 8-7 (rapid extrication) is **8 steps** and TABLE 8-3 gives the 4 situations
that call for it. Under rule 23 the 8-step procedure must be chunked. Ask whether he wants
the drills carded as *procedures to reproduce* (heavier, chunked into phases) or as
*recognition* cards (lighter: which drill, when to use it, the one or two steps that are
easy to get wrong) with the composite plate carrying the rest. That choice sets the
chapter's card count more than any other decision.
