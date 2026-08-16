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

**Second shape of the same failure, found 2026-08-15 (card-rules #32, R52).** A run may
also not FIX something and merely write prose about the leftovers. The Chapter 7
rule-25 remediation replaced eight keyed numeric panels with 46 per-key notes and left
the eight originals live, recording that decision as "originals left in place to compare"
— in a commit message, which no program reads — while the provenance field meant for it
(`replaces`) held a prose sentence instead of the note ids. Twelve days later Parker drew
the systolic-BP panel in review and asked why it wasn't individual cards. It was; the
replacements were three rows down in the same deck.

So a run that supersedes existing notes must name them, in its manifest:

    "supersedes": [
      {"note_id": 1785508840234, "rule": "card-rules #25",
       "successors": [1785758337196, 1785758337271],
       "status": "retired"},                       # verified against the retirement ledger
      {"note_id": 1785508840410, "rule": "card-rules #25",
       "status": "pending", "why": "left live so Parker can compare"}
    ]

`retired` must be backed by `reference/retirement-ledger.json`. `pending` keeps this check
RED on purpose — a deferred cleanup is an open item, and the whole lesson of this file is
that an open item recorded only in prose is an item nobody closes. To settle it, either
retire the note (`retire_notes.py`) or change the status to `waived` with a `why`, the
same escape hatch `mechanizable: false` already provides for hazards.

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


def retired_note_ids():
    """Note ids the retirement ledger says are actually out of rotation."""
    path = os.path.join(SKILL, "reference", "retirement-ledger.json")
    if not os.path.exists(path):
        return set()
    try:
        led = json.load(open(path))
    except Exception:
        return set()
    return {e["note_id"] for e in led.get("retired", []) if not e.get("undone")}


def supersession_problems(rel, m, retired):
    """A run that replaced notes must name them and account for each one.

    The trigger is deliberately wide: a manifest that COUNTS replacements, or a
    provenance file that carries a `replaces` key, is claiming it superseded something.
    Chapter 7's run did both — `"replaced_panels": 8` and a `replaces` on all 46 rows —
    and still left no way to find a single original, because the value was prose."""
    out = []
    claims = [k for k in (m.get("counts") or {}) if re.search(r"replac|supersed", k, re.I)]
    sup = m.get("supersedes")

    if claims and not sup:
        out.append(
            f"{rel}: manifest counts {claims} but has no `supersedes` block — the run says it "
            f"replaced notes and never names WHICH, so nothing can ever retire or verify them")
    for e in sup or []:
        nid, status = e.get("note_id"), e.get("status")
        if not isinstance(nid, int):
            out.append(f"{rel}: supersedes entry has no integer `note_id` ({e!r}) — a prose "
                       f"description is not a target a later pass can act on")
            continue
        if status == "retired":
            if nid not in retired:
                out.append(f"{rel}: note {nid} is marked `retired` but is not in "
                           f"reference/retirement-ledger.json — retire it for real "
                           f"(scripts/retire_notes.py) or correct the status")
        elif status == "waived":
            if not e.get("why"):
                out.append(f"{rel}: note {nid} is `waived` with no `why`")
        elif status == "pending":
            out.append(f"{rel}: note {nid} is still PENDING retirement"
                       + (f" ({e['why']})" if e.get("why") else "")
                       + " — it is live and superseded. Retire it, or waive it with a `why`")
        else:
            out.append(f"{rel}: note {nid} has status {status!r} — expected "
                       f"retired / pending / waived")
    return out


def prose_replaces(rel, root, has_supersedes):
    """`replaces` must carry note ids. This is the exact field Chapter 7 filled with a
    sentence, which is why the originals were unreachable by any automated pass.

    The real requirement is that a supersession be addressable SOMEWHERE, so a manifest
    carrying a proper `supersedes` block satisfies it and this check stands down — which
    is how the four historical remediation runs close without rewriting their provenance
    row by row. New runs, which have no such block until they write one, still answer to
    it at the row level."""
    if has_supersedes:
        return []
    path = os.path.join(root, "provenance.jsonl")
    if not os.path.exists(path):
        return []
    bad = 0
    for line in open(path):
        try:
            r = json.loads(line)
        except Exception:
            continue
        v = r.get("replaces")
        if v is None:
            continue
        if not (isinstance(v, list) and all(isinstance(x, int) for x in v)):
            bad += 1
    if bad:
        return [f"{rel}: {bad} provenance row(s) carry a `replaces` that is not a list of "
                f"note ids — record WHICH notes were superseded, not a description of them"]
    return []


def main():
    ids = known_regression_ids()
    retired = retired_note_ids()
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
        problems += supersession_problems(rel, m, retired)
        problems += prose_replaces(rel, root, bool(m.get("supersedes")))
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
        print("OPEN HAZARDS (a run found or fixed something and left the hole open):")
        for p in problems:
            print("  x", p)
        return 1
    print("  every recorded hazard is closed by a regression case or explicitly justified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
