# Chapter 10 (Patient Assessment) — shared drafting brief for ALL units

You are one drafting unit in a fan-out over EMT Chapter 10 (AAOS Emergency Care 12e,
"Patient Assessment", physical pages 914–1101). Work ONLY the marks assigned to your unit.

## Read these FIRST (all paths relative to /Users/parkerregner/.claude/skills/zotero-to-anki/)
1. `reference/card-rules.md` — the whole standard. Rule 0 first, then 23–27 (retrieval load).
2. `reference/card-recipes.md` — pick every card's archetype here.
3. `reference/parker-preferences.md` — wins over card-rules on conflict.
4. `reference/profiles/emt.md` — Chapter 10 is a CLINICAL chapter: push application.
5. `reference/note-format.md` — the exact card object shape.

## Your inputs
- Marks: `work/emt/chapter_10_highlights.json` — a JSON list; your unit's brief names your
  indices. Read ONLY your items (plus neighbors if checking Rule-0 adjacency at a unit
  boundary — but never card a neighbor unit's mark).
- Page renders already on disk: `work/emt/page_<N>.png` for N in {946, 948, 950, 951, 957,
  958, 975, 977, 980, 1027, 1028, 1032, 1033, 1034, 1049, 1050}. Render any other page you
  need: `python3 scripts/render_page.py --source emt <page> --dpi 170` (writes
  `work/emt/page_<N>.png`). READ the render before trusting any `needs_visual` or
  `PARTIAL`-grounding mark, and before committing any list count (`list_lead_in: true`).

## The contract (non-negotiable)
- **Cards come ONLY from your assigned marks** (card-rules #29). Unmarked page content may
  serve as visible framing/Back-Extra ONLY when the cited marks' own `context` supports it.
  If unmarked content seems exam-critical, write one line in your notes file — never a card.
- **Never drop a yellow span** (#1). Thin span → Rule-0 zoom-out → if still uncardable,
  card it as best you honestly can AND set a `"flag_for_parker"` note in your notes file.
- **Ground every claim** in the cited marks' `context` (#10). Zero guessing (#7 Layer A).
- **Every number/dose/threshold**: verify verbatim against the page render, then record
  `"verified_against": "p<page>"`, `"verified_by": "agent"`, `"numeric": true`. If you could
  NOT verify, leave `verified_against` null — the report derives `needs_human_check`.
  NEVER assert `needs_human_check` yourself; it is derived.
- **Cold-solve every card, per row** (#16–22). **Load-check every group** (#23–25): ≤4
  uncued answers per grouped reveal; 5–7 only with a spelled mnemonic the card teaches;
  value columns (numbers keyed by age/label) = ONE NOTE PER KEY (#25), never a panel, and
  note in the card `"needs_table_back": "<TABLE label>"` so the figure stage attaches the
  plate (do NOT set `image` yourself).
- Chunked sets: separate NOTES (#24), each with `Roster:` in Back Extra (own members
  **bold**). Unordered chunked sets get NO anchor note (#23.1).
- Two-way definitions for term↔meaning facts (`{{c1::TERM::hint}} is {{c2::crisp meaning}}`);
  one-way when only one direction is real. Never two-way lists/numbers/scenarios.
- The EMT auto-pair rule: for a sign/finding/threshold/"which one" fact, ALSO draft one
  short vignette forcing the decision (one stem, one cloze). Fresh exemplars only — never
  reuse a sibling card's example (#13).
- HTML: `<b> <i> <br> <img>` only. Lists of answers: `<br><br>` between rows (#19).
  Back Extra labeled lines (`Distinguish:` `Pitfall:` `Why:` `Mechanism:` `Ex:` `Cue:`
  `Pathway:` `Mnemonic:` `Roster:` `Meaning:`), separated `<br><br>`. No `Roster:` outside
  chunked sets. Back Extra must ADD something (never re-define a defined term).
- Margin comments (`user_comment`) are Parker's voice — obey them and record how in notes.
- **Do not card GCS or anything unmarked**, even if famous.

## Card object (one per NOTE, in a JSON list)
```json
{
  "Text": "…cloze text…",
  "Back Extra": "…labeled lines…",
  "source": "emt",
  "segment": 10,
  "from_idx": [<mark indices>],
  "block": "<X_short_name>",
  "numeric": false,
  "verified_against": null,
  "verified_by": null,
  "visual_source": null
}
```
- `visual_source`: `{"pages": ["975"], "note": "read from render"}` whenever a fact came
  off a page render rather than the text layer (mandatory for `needs_visual` marks whose
  answers are not in their `context` — that is R13).
- `needs_table_back`: optional string, see rule 25 above.
- Do NOT include `needs_human_check`, `image`, `kind`, or `lexicon` on yellow cards.

## Output (write BOTH)
- `work/emt/ch10_units/<UNIT>_cards.json` — the JSON list of card objects.
- `work/emt/ch10_units/<UNIT>_notes.md` — per block: a fact-pass table (proposition /
  where / MUST-TEST-SUPPORTING-SKIP / disposition), archetype choice, judgment calls,
  any flags for Parker, how each margin comment was honored, and what you verified
  against which render.

Aim for the smallest set of excellent cards that tests every MUST-TEST fact in your marks.
Expect roughly 0.6–1.2 cards per yellow mark after Rule-0 grouping — quality over count.
