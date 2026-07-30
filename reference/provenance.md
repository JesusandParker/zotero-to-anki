# Provenance — how every card stays traceable

Parker's continuous-improvement principle: keep every piece of data from each run, so you
can pick any card out of Anki and work backwards.

Three questions, and where each is answered:

| Question | Answered by |
|---|---|
| **Why was this card made?** | `from_idx` → the marked highlight(s), their page, and Parker's margin note |
| **What did the agent do?** | `provenance.jsonl` → producing stage, editor changes, judge verdict, how numbers were verified |
| **Why that decision?** | `decisions.jsonl` and `dropped.jsonl` → every merge, collapse, cut, and kill, with its reason |

This is not bookkeeping for its own sake. **Provenance is what makes the grounding check
possible.** Before it existed, `check_cards.py` saw only card text, so the system's own
Rule 1 — *always ground in the page paragraph* — could never be verified mechanically. A
card that knows which highlight it came from can finally be tested against it (R13).

---

## Card fields

Beyond `Text` / `Back Extra` / `source` / `segment`:

| Field | Meaning |
|---|---|
| `from_idx` | **Required for new runs.** Indices into that segment's `*_highlights.json` — the marks this card was built from. A card citing several is a Rule-0 group. |
| `block` | The grouping unit the card was drafted in (e.g. `H_nervous_system`). Makes fan-out behaviour auditable. |
| `numeric` | Derived: the card states a value, dose, threshold, or time window. |
| `verified_against` | The page its digits were checked against, e.g. `"p531"`. |
| `verified_by` | Who checked — `judge`, `agent`, `parker`. |
| `needs_human_check` | **Derived, never asserted:** `(numeric or weak grounding) and not verified_against`. |
| `visual_source` | Proof a fact was read from an image: `{"pages": ["549"], "figures": [...], "note": "..."}` |
| `image` | A crop attached to the card itself (renders in Anki). |

### Why `visual_source` matters
Some material genuinely only exists as an image — a table with no text layer, an anatomy
plate, a hazmat placard, an Arabic script chart. A card built from one is legitimately
ungroundable in text, and R13 exempts it **only if it carries the evidence**.

This is not a formality. Chapter 6 produced 23 cards from three image-only tables. The
facts were correct — an agent had gone and read the pages — but nothing recorded that, so
from the artifacts alone a correct card was indistinguishable from a fabricated one. The
post-mortem could only tell them apart by finding a stray remark buried in an ad-hoc edits
file. Attaching the crop turns that archaeology into a lookup.

---

## The run store

```
runs/<source>/<segment>/<run_id>/
    manifest.json      metadata, the skill's git SHA at run time, counts, hazards found
    highlights.json    immutable snapshot of the extractor's output (the INPUT)
    cards.json         what shipped (the OUTPUT)
    provenance.jsonl   one record per card, incl. its Anki noteId once written
    decisions.jsonl    every merge / collapse / cut, with its reason
    dropped.jsonl      cards made and then killed, and why
    figures/           crops that are EVIDENCE of visual grounding
```

**`skill_sha` is load-bearing.** It records which version of the rules produced these
cards. Without it you cannot tell whether a bad card came from a bad rule or from a rule
that has since been fixed.

**`dropped.jsonl` is the most valuable file and used to not exist.** Every card that was
made and then killed, with the reasoning. That is where you audit — or disagree with — the
consolidation stage's judgement.

**What is deliberately NOT stored:** full-page renders. They regenerate from the PDF in a
second. Only crops attached to a card are kept, because those are evidence.

### The link back to Anki
`anki_write.py --run <dir>` writes each returned noteId into `provenance.jsonl`. The link
lives **in the repo, not as a tag on the card** — Parker had the `claude_generated` tag
stripped from every note as noise and keeps `ch<N>` only, so traceability must not cost him
deck clutter.

```bash
python3 scripts/run_store.py trace 1782941723577
```

...prints the run, the skill SHA, the block, the stage, the verification record, and every
source mark with its page and Parker's margin note.

---

## The hazard rule

A run's manifest carries `new_hazards_found`. Every entry must either name the regression
case that now catches it, or state that it cannot be mechanized and why:

```json
{"summary": "table captions ground as EXACT while the body is elsewhere",
 "regression_id": "R13"}

{"summary": "open-set answers need semantics to detect",
 "mechanizable": false,
 "why": "requires judging whether the answer space is open; the LLM judge owns it"}
```

`scripts/check_hazards.py` enforces this and `smoke_test.sh` runs it, so a run cannot
discover a problem and quietly leave the hole open.

This exists because that has now happened twice. The 2026-07-19 audit called 899 cards
"confirmed sound" while missing the whole bloated-c2 class. The Chapter 6 run *found* the
table-grounding hazard, wrote a paragraph about it in `SKILL.md`, shipped the affected
cards, and declared itself verified. Both were telling the truth about the checks that
existed. The doctrine is **name it, mechanize it, test it** — and step one keeps being
mistaken for the whole job.

---

## Reading the record

```bash
python3 scripts/run_store.py list              # every run
python3 scripts/run_store.py list emt          # one source
python3 scripts/run_store.py show emt 6        # manifest + samples of each log
python3 scripts/run_store.py trace <noteId>    # one Anki card -> its whole story
python3 scripts/sync_report.py --source emt    # what Parker changed after staging
```
