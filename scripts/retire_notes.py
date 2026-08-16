#!/usr/bin/env python3
"""
retire_notes.py — the operation this pipeline never had: taking a card OUT.

Every writer in this repo adds. `anki_write.py` adds notes, `attach_figures.py` adds
images, `feedback_harvest.py --apply` edits fields. Nothing could ever say "this note is
finished, its job now belongs to these other notes." So when a rule was written that
condemned cards already live, the remediation could only do half the job:

  * 2026-08-02, rule 23 (retrieval load): the 10-element radio report was chunked into
    phase notes. The 10-element card stayed live. Parker kept drawing it — 5 reviews,
    5 "Again."
  * 2026-08-03, rule 25 (keyed numeric panels): "Chapter 7: eight panels became 46
    per-key notes... **originals left in place to compare**." That was a reasonable call
    on the day. It was recorded in a commit message, which no program reads, and the
    provenance field meant for it (`replaces`) held the PROSE "a keyed panel of numbers
    hidden under one cloze (card-rules #25)" rather than the note ids — so no later pass
    could find the originals even in principle.
  * 2026-08-15: Parker hits the systolic-BP panel in review and asks why it isn't
    individual cards. It was. The individual cards had existed for twelve days, three
    rows down in the same deck.

So retirement is a real operation with a real record. Three properties make it safe
enough to run on a live collection:

  1. **It never deletes.** Retiring suspends every card of the note and tags it. His
     review history, his mnemonics, his pasted images all survive untouched — which is
     also why no `authorship.guard()` call is needed here: retirement writes no field.
     Deleting is a separate decision that stays Parker's, and the ledger keeps the full
     text so it is recoverable from the repo either way.
  2. **It demands a successor.** A note is only retired once the notes that replace it
     are verified live and unsuspended. Retiring with nothing to take over requires
     `--no-successors` AND a `--reason`, so "this fact is now untested" is a recorded
     decision instead of an accident.
  3. **It is reversible.** `undo` unsuspends and untags from the ledger's own record.

`check_cards.py --live` skips suspended notes, so a retirement genuinely closes the gate
instead of leaving a permanent red mark that trains everyone to ignore it.

    python3 scripts/retire_notes.py audit --source emt
    python3 scripts/retire_notes.py retire --source emt --note 1785508840234 \
            --rule "card-rules #25" --successors 1785758337196,1785758337271
    python3 scripts/retire_notes.py undo --source emt --batch 2026-08-15T20-51-03
    python3 scripts/retire_notes.py self-test
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
LEDGER = os.path.join(SKILL, "reference", "retirement-ledger.json")
ANKI = "http://localhost:8765"
RETIRE_TAG = "superseded"


def _http_call(action, **params):
    req = urllib.request.Request(
        ANKI, data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    try:
        res = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI}. Is Anki open? ({e})")
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res["result"]


# Indirected so self-test can run the whole flow against a fake collection.
CALL = _http_call


# ---------------------------------------------------------------- the ledger

def load_ledger():
    if not os.path.exists(LEDGER):
        return {"retired": []}
    return json.load(open(LEDGER))


def save_ledger(led):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "w") as fh:
        json.dump(led, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def retired_ids(led=None):
    led = led if led is not None else load_ledger()
    return {e["note_id"] for e in led["retired"] if not e.get("undone")}


def readable(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html or "")).strip()


# ---------------------------------------------------------------- retiring

def verify_successors(ids):
    """(ok, problems). A successor must exist and be in rotation — a suspended or
    missing replacement means the fact would silently stop being tested."""
    problems = []
    if not ids:
        return False, ["no successors given"]
    info = CALL("notesInfo", notes=list(ids))
    found = {n["noteId"] for n in info if n}
    for i in ids:
        if i not in found:
            problems.append(f"successor {i} does not exist")
    live_cards = [c for n in info if n for c in n.get("cards", [])]
    if live_cards:
        susp = CALL("areSuspended", cards=live_cards)
        if susp and all(bool(s) for s in susp):
            problems.append("every successor card is suspended — nothing would test this")
    return (not problems), problems


def retire(source, note_id, rule, successors, reason, batch, dry_run=False):
    """Suspend + tag one note, recording enough to undo it and to rebuild it by hand."""
    led = load_ledger()
    if note_id in retired_ids(led):
        return {"note_id": note_id, "status": "already retired"}

    info = CALL("notesInfo", notes=[note_id])
    if not info or not info[0]:
        return {"note_id": note_id, "status": "ERROR: note does not exist"}
    n = info[0]

    if successors:
        ok, problems = verify_successors(successors)
        if not ok:
            return {"note_id": note_id, "status": "REFUSED: " + "; ".join(problems)}
    elif not reason:
        return {"note_id": note_id,
                "status": "REFUSED: no successors and no --reason. Retiring a note with "
                          "nothing to replace it means the fact stops being tested; say so "
                          "explicitly with --no-successors --reason '...'"}

    entry = {
        "note_id": note_id,
        "source": source,
        "rule": rule,
        "successors": list(successors),
        "reason": reason,
        "batch": batch,
        "retired_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "cards": list(n.get("cards", [])),
        "tags_before": list(n.get("tags", [])),
        # Kept verbatim so the card is recoverable from the repo alone, even if the note
        # is later deleted by hand in Anki.
        "text": n["fields"].get("Text", {}).get("value", ""),
        "back_extra": n["fields"].get("Back Extra", {}).get("value", ""),
    }
    if dry_run:
        return {"note_id": note_id, "status": "would retire", "entry": entry}

    if entry["cards"]:
        CALL("suspend", cards=entry["cards"])
    CALL("addTags", notes=[note_id], tags=RETIRE_TAG)
    led["retired"].append(entry)
    save_ledger(led)
    return {"note_id": note_id, "status": "retired", "cards": len(entry["cards"])}


def undo(batch=None, note_id=None):
    led = load_ledger()
    restored = []
    for e in led["retired"]:
        if e.get("undone"):
            continue
        if batch and e.get("batch") != batch:
            continue
        if note_id and e["note_id"] != note_id:
            continue
        if e.get("cards"):
            CALL("unsuspend", cards=e["cards"])
        if RETIRE_TAG not in e.get("tags_before", []):
            CALL("removeTags", notes=[e["note_id"]], tags=RETIRE_TAG)
        e["undone"] = datetime.datetime.now().isoformat(timespec="seconds")
        restored.append(e["note_id"])
    save_ledger(led)
    return restored


# ---------------------------------------------------------------- audit

def audit(source):
    """Live notes this repo's own gate calls HARD ERRORS. Suspended notes are already
    out of rotation and out of scope, so a retirement removes a note from this list."""
    sys.path.insert(0, HERE)
    import check_cards as cc
    cards = cc.load_live("all", source)
    rows = []
    for c in cards:
        hard, _warn = cc.per_card(str(c["noteId"]), c, strict_html=False)
        if hard:
            rows.append((c["noteId"], readable(c.get("Text", ""))[:70], hard))
    return rows


# ---------------------------------------------------------------- self-test

def self_test():
    """Retirement runs against a live collection, so its refusals are the part that has
    to be right. Each case is a way this could quietly do the wrong thing."""
    global CALL, LEDGER
    import tempfile
    fails = []

    def case(name, cond):
        if not cond:
            fails.append(name)
        print(("  ok   " if cond else "  FAIL ") + name)

    fake = {
        1: {"noteId": 1, "cards": [11, 12], "tags": ["ch7"],
            "fields": {"Text": {"value": "panel {{c1::a}} {{c1::b}}"},
                       "Back Extra": {"value": "table"}}},
        2: {"noteId": 2, "cards": [21], "tags": [], "fields": {"Text": {"value": "row a"},
                                                               "Back Extra": {"value": ""}}},
        3: {"noteId": 3, "cards": [31], "tags": [], "fields": {"Text": {"value": "row b"},
                                                               "Back Extra": {"value": ""}}},
    }
    state = {"suspended": set(), "tags": {}, "log": []}

    def fake_call(action, **p):
        state["log"].append(action)
        if action == "notesInfo":
            return [fake.get(i) for i in p["notes"]]
        if action == "areSuspended":
            return [c in state["suspended"] for c in p["cards"]]
        if action == "suspend":
            state["suspended"].update(p["cards"])
            return True
        if action == "unsuspend":
            state["suspended"].difference_update(p["cards"])
            return True
        if action in ("addTags", "removeTags"):
            state["tags"].setdefault(p["notes"][0], set())
            if action == "addTags":
                state["tags"][p["notes"][0]].add(p["tags"])
            else:
                state["tags"][p["notes"][0]].discard(p["tags"])
            return True
        raise AssertionError("unexpected action " + action)

    CALL = fake_call
    tmp = tempfile.mkdtemp()
    LEDGER = os.path.join(tmp, "retirement-ledger.json")

    r = retire("emt", 1, "card-rules #25", [2, 3], None, "b1")
    case("retires a note whose successors are live", r["status"] == "retired")
    case("suspends every card of the note", state["suspended"] == {11, 12})
    case("tags it so it is findable in Browse", RETIRE_TAG in state["tags"].get(1, set()))
    case("never deletes", "deleteNotes" not in state["log"])

    r = retire("emt", 1, "card-rules #25", [2, 3], None, "b1")
    case("retiring twice is a no-op", r["status"] == "already retired")

    r = retire("emt", 2, "card-rules #25", [999], None, "b2")
    case("REFUSES when a successor does not exist", r["status"].startswith("REFUSED"))

    state["suspended"].add(31)
    r = retire("emt", 2, "card-rules #25", [3], None, "b2")
    case("REFUSES when every successor is suspended", r["status"].startswith("REFUSED"))
    state["suspended"].discard(31)

    r = retire("emt", 2, "card-rules #25", [], None, "b2")
    case("REFUSES a bare retirement with no reason", r["status"].startswith("REFUSED"))

    r = retire("emt", 2, "card-rules #25", [], "duplicate of note 3", "b2")
    case("allows it once the reason is stated", r["status"] == "retired")

    # The ledger must keep the text, or a later hand-deletion loses the card for good.
    led = load_ledger()
    case("ledger stores the card verbatim",
         any("{{c1::a}}" in e["text"] for e in led["retired"]))

    n = undo(batch="b1")
    case("undo restores the batch", n == [1])
    # Only THIS batch's cards — note 2 was retired under b2 and must stay suspended.
    case("undo unsuspends its cards and only its cards",
         not ({11, 12} & state["suspended"]) and 21 in state["suspended"])
    case("undo removes the tag", RETIRE_TAG not in state["tags"].get(1, set()))
    case("undo leaves other batches retired", 2 in retired_ids())

    # A tag Parker put there himself must survive an undo.
    state["tags"][2] = {RETIRE_TAG}
    load_ledger()["retired"]
    led = load_ledger()
    for e in led["retired"]:
        if e["note_id"] == 2:
            e["tags_before"] = [RETIRE_TAG]
    save_ledger(led)
    undo(note_id=2)
    case("undo keeps a tag that was already his",
         RETIRE_TAG in state["tags"].get(2, set()))

    print(f"\n{len(fails)} failure(s)" if fails else "\nall retirement cases pass")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="live notes that this repo's own gate hard-blocks")
    a.add_argument("--source", required=True)

    r = sub.add_parser("retire", help="suspend + tag a superseded note")
    r.add_argument("--source", required=True)
    r.add_argument("--note", action="append", required=True, type=int)
    r.add_argument("--rule", required=True, help='e.g. "card-rules #25"')
    r.add_argument("--successors", default="", help="comma-separated note ids that replace it")
    r.add_argument("--no-successors", action="store_true")
    r.add_argument("--reason", default=None)
    r.add_argument("--dry-run", action="store_true")

    u = sub.add_parser("undo", help="unsuspend + untag from the ledger")
    u.add_argument("--batch", default=None)
    u.add_argument("--note", type=int, default=None)

    sub.add_parser("self-test")
    args = ap.parse_args()

    if args.cmd == "self-test":
        return self_test()

    if args.cmd == "audit":
        rows = audit(args.source)
        if not rows:
            print(f"{args.source}: no live note hard-blocks the gate")
            return 0
        print(f"{args.source}: {len(rows)} live note(s) HARD-BLOCK the gate\n")
        for nid, text, hard in rows:
            rule = re.search(r"card-rules #\d+", hard[0])
            print(f"  {nid}  [{rule.group(0) if rule else '?'}]  {text}")
        print("\nEach needs either retirement (once its replacements are live) or a rule change.")
        return 1

    if args.cmd == "undo":
        n = undo(batch=args.batch, note_id=args.note)
        print(f"restored {len(n)} note(s): {n}")
        return 0

    succ = [int(x) for x in args.successors.split(",") if x.strip()]
    if succ and args.no_successors:
        ap.error("--successors and --no-successors are contradictory")
    batch = datetime.datetime.now().isoformat(timespec="seconds").replace(":", "-")
    rc = 0
    for nid in args.note:
        res = retire(args.source, nid, args.rule, succ, args.reason, batch,
                     dry_run=args.dry_run)
        print(f"  {res['note_id']}: {res['status']}")
        if "REFUSED" in res["status"] or "ERROR" in res["status"]:
            rc = 1
    if not args.dry_run and rc == 0:
        print(f"\nbatch {batch} — undo with:  python3 scripts/retire_notes.py undo --batch {batch}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
