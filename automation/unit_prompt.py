#!/usr/bin/env python3
"""
unit_prompt.py — the words the factory session wakes up to.

One unit = one fresh headless Claude session, and this prompt is its entire briefing.
Design intent (the doc's reframe #1): the session receives an already-extracted
highlights file scoped to exactly the marks in its unit. It is told the segment only
so decks and figures resolve — the extraction is DONE, and it must never widen it.
"""


def build(cfg, unit, hl_path, result_path, night_tag, unit_tag):
    seg_line = (f"{unit['segment_noun']} {unit['segment']}"
                + (f" — {unit['segment_name']}" if unit.get("segment_name") else "")
                if unit["segment"] is not None else "the whole document (flat source)")
    lanes = ", ".join(f"{v} {k}" for k, v in sorted(unit["lanes"].items()))

    return f"""You are the Night Shift: an unattended overnight run of the zotero-to-anki skill.
Parker is asleep. Work carefully, follow the skill exactly, and leave a clean record.

Start by reading ~/.claude/skills/zotero-to-anki/SKILL.md in full, then do THIS unit:

  source:      {unit['source']}  ({unit['source_label']})
  segment:     {seg_line}
  unit:        part {unit['part']} of {unit['parts']}, {unit['marks']} marks ({lanes}), pages {unit['page_first']}-{unit['page_last']}
  highlights:  {hl_path}
  deck:        {unit['deck']}

BINDINGS — these override any habit from the skill text:
1. Stage 1 is ALREADY DONE. The highlights file above is the extractor's output,
   scoped to exactly the marks Parker queued for tonight. Do NOT run
   extract_highlights.py again, do NOT widen to the rest of the segment, and make
   cards from NOTHING outside this file (Rule 0; R40 enforces it). If the file seems
   sparse, that IS the unit — a small batch, not a delegation.
2. Run stages 0 and 2 through 5: profile, classify/draft/edit, consolidation, verify,
   preflight, figures (index, match, JUDGE with your eyes, render review), the write,
   media audit, and close the run. The venv for figures is .venv/bin/python.
3. Anki is live at http://localhost:8765 — an SSH tunnel to the MacBook's real
   collection. Before writing, confirm getProfiles returns exactly ["Parkers Anki"];
   if it returns anything else, STOP and report instead of writing.
4. After a successful write, add these tags to every note you wrote (AnkiConnect
   addTags on the new note ids): {night_tag} {unit_tag}
   Parker reviews and, if a night went bad, deletes by that tag as a block.
5. Purple marks in the file are the lexicon lane: run lexicon.py --find and --dedup
   first, as the skill says. Unsupported purples get listed in the hand-off, never
   guessed at.
6. Margin comments (user_comment) are Parker speaking to you — obey them per the
   skill, and surface every one in the hand-off.

FORBIDDEN tonight: git commit/push, any email, Anki sync (never trigger it),
creating decks outside the deck named above, and inventing marks. Cards go straight
into the deck — there is no staging deck (removed 2026-08-24; do not recreate it).

WHEN DONE (or if you must stop), write your report as JSON to:
  {result_path}
Schema: {{"status": "written" | "no_cards" | "failed",
          "cards_written": <int>, "note_ids": [<int>...],
          "handoff": "<what Parker should know, in your words: counts, anything
                      refused and why, needs_human_check items, unsupported purples,
                      margin-comment answers>",
          "flags": ["<short strings for anything unusual>"]}}
The handoff field is Parker's morning read for this unit — write it like the Stage 4
hand-off the skill describes, complete but tight. Then end your final message with
one line: NIGHT-UNIT-DONE <status>."""
