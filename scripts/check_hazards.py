#!/usr/bin/env python3
"""
check_hazards.py — a run may not discover a problem and merely write prose about it.

This exists because the same failure has now happened twice, in a system explicitly built
to prevent it:

  * 2026-07-19: an audit declared 899 cards "confirmed sound" and missed the entire
    bloated-c2 class, because that class was neither a named check nor mechanically
    detectable.
  * 2026-07-29: the Chapter 6 run FOUND the table-grounding hazard, wrote a paragraph
    about it into SKILL.md, shipped 23 affected cards, and declared itself verified.

Both runs were telling the truth about the checks that existed. The system's own doctrine
is three steps — **name it, mechanize it, test it** — and step one keeps getting mistaken
for the whole job.

So: every hazard a run records in its manifest must either name the regression case that
now catches it, or say plainly that it cannot be mechanized and why. `smoke_test.sh` runs
this, so a run cannot quietly leave a known hole open.

    python3 scripts/check_hazards.py

Manifest shape (`runs/<source>/<segment>/<run_id>/manifest.json`):

    "new_hazards_found": [
      {"summary": "table captions ground as EXACT while the body is elsewhere",
       "regression_id": "R13"},
      {"summary": "open-set answers can't be detected without semantics",
       "mechanizable": false,
       "why": "requires judging whether the answer space is open; the LLM judge owns it"}
    ]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
RUNS = os.path.join(SKILL, "runs")
CASES = os.path.join(SKILL, "reference", "regression-cases.md")


def known_regression_ids():
    if not os.path.exists(CASES):
        return set()
    return set(re.findall(r"^##\s+(R\d+[a-z]?)\b", open(CASES).read(), re.M))


def main():
    ids = known_regression_ids()
    problems, checked, hazards = [], 0, 0

    if not os.path.isdir(RUNS):
        print("no runs recorded yet — nothing to check")
        return 0

    for root, _dirs, files in os.walk(RUNS):
        if "manifest.json" not in files:
            continue
        checked += 1
        mpath = os.path.join(root, "manifest.json")
        try:
            m = json.load(open(mpath))
        except Exception as e:
            problems.append(f"{mpath}: unreadable manifest ({e})")
            continue
        rel = os.path.relpath(root, SKILL)
        for h in m.get("new_hazards_found") or []:
            hazards += 1
            summary = (h.get("summary") or "<no summary>")[:80]
            rid = h.get("regression_id")
            if rid:
                if rid not in ids:
                    problems.append(
                        f"{rel}: hazard {summary!r} names regression '{rid}', which is not in "
                        f"reference/regression-cases.md — add the case, or fix the id")
                continue
            if h.get("mechanizable") is False:
                if not h.get("why"):
                    problems.append(
                        f"{rel}: hazard {summary!r} is marked not-mechanizable but gives no `why`")
                continue
            problems.append(
                f"{rel}: hazard {summary!r} was recorded but NOT closed — it needs either a "
                f"`regression_id` (name it, mechanize it, test it) or "
                f"`mechanizable: false` with a `why`")

    print(f"checked {checked} run manifest(s), {hazards} recorded hazard(s)")
    if problems:
        print("OPEN HAZARDS (a run found something and left the hole open):")
        for p in problems:
            print("  x", p)
        return 1
    print("  every recorded hazard is closed by a regression case or explicitly justified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
