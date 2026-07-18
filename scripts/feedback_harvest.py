#!/usr/bin/env python3
"""
feedback_harvest.py — collect (and clear) Parker's hidden "Card Feedback" complaints.

During review Parker types complaints into the hidden `Card Feedback` field on his own
note types (`AnKing Cloze`, `AnKing Basic`) via Anki's Edit control. The field is not in
any card template, so it never renders while studying, but it stays attached to the exact
card. This script is the batch front-door to the existing "If Parker reports an issue with
a card" loop in SKILL.md:

  * harvest — find every note with a non-empty Card Feedback, dump card + rant to
              work/feedback_inbox_<date>.json and print a readable summary. (READ-ONLY.)
  * apply   — write approved fixes back (Text/Back Extra) and/or clear the feedback field,
              driven by a small JSON batch file. (MUTATES notes.)
  * clear   — convenience: blank Card Feedback on the given note ids. (MUTATES notes.)
  * show    — print one note's full fields (debugging). (READ-ONLY.)

Invariant this preserves: a non-empty Card Feedback means "unprocessed complaint." Only
clear a note AFTER its lesson is logged to reference/feedback-log.md, never before — that
way nothing is ever lost.

Scope guard: this only ever touches Parker's own note types (below). It never reads or
writes the AnkiHub-synced AnKing download decks (different models; leave them alone).

Usage:
    python3 feedback_harvest.py                          # harvest -> inbox JSON + summary
    python3 feedback_harvest.py --harvest                # same, explicit
    python3 feedback_harvest.py --show   <noteId>        # dump one note's fields
    python3 feedback_harvest.py --clear  <noteId> ...    # blank Card Feedback on these
    python3 feedback_harvest.py --apply  fixes.json      # apply a write-back batch (see below)

--apply batch file is a JSON list; each item may carry a fix, a clear, or both:
    [
      {"noteId": 123, "fields": {"Text": "...fixed...", "Back Extra": "..."}, "clear_feedback": true},
      {"noteId": 456, "clear_feedback": true}
    ]

Anki must be running (AnkiConnect lives inside the app; this fails loud if it's closed).
"""
import argparse, json, os, re, sys, urllib.request
from datetime import date

ANKI = "http://localhost:8765"
FEEDBACK_FIELD = "Card Feedback"
# Parker's OWN note types only. These (and only these) got the Card Feedback field on
# 2026-07-18. The AnkiHub-synced AnKing download decks use different models and are never
# touched here.
MODELS = ["AnKing Cloze", "AnKing Basic"]
# The "front" field differs by model: cloze cards use Text, basic cards use Front.
FRONT_FIELDS = ["Text", "Front"]

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(SKILL_ROOT, "work")


def call(action, **params):
    req = urllib.request.Request(
        ANKI, data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        res = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI}. Is Anki open? ({e})")
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res["result"]


_TAGS = re.compile(r"<[^>]+>")
def _plain(html, limit=None):
    """HTML -> rough plain text, for console previews only (JSON keeps the raw value)."""
    t = _TAGS.sub(" ", html or "")
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:limit] + "…") if (limit and len(t) > limit) else t


def _front(fields):
    for f in FRONT_FIELDS:
        if f in fields:
            return f, fields[f]["value"]
    k = next(iter(fields))  # fall back to first field
    return k, fields[k]["value"]


def harvest():
    """Every note (Parker's models) with a non-empty Card Feedback, newest note first."""
    model_q = " OR ".join(f'note:"{m}"' for m in MODELS)
    # `<field>:_*` = at least one char = non-empty; scope to Parker's own models.
    query = f'"{FEEDBACK_FIELD}:_*" ({model_q})'
    ids = call("findNotes", query=query)
    if not ids:
        return []
    notes = call("notesInfo", notes=ids)
    # note -> deck via its first card (one batched cardsInfo call)
    first_cards = [n["cards"][0] for n in notes if n.get("cards")]
    deck_by_card = {c["cardId"]: c["deckName"] for c in call("cardsInfo", cards=first_cards)} \
        if first_cards else {}
    items = []
    for n in notes:
        fields = n["fields"]
        fb = fields.get(FEEDBACK_FIELD, {}).get("value", "").strip()
        if not fb:  # belt-and-suspenders against any search-syntax quirk
            continue
        fkey, fval = _front(fields)
        first_card = n["cards"][0] if n.get("cards") else None
        items.append({
            "noteId": n["noteId"],
            "model": n["modelName"],
            "deck": deck_by_card.get(first_card, "?"),
            "front_field": fkey,
            "front": fval,
            "back_extra": fields.get("Back Extra", {}).get("value", ""),
            "feedback": fb,
        })
    items.sort(key=lambda x: x["noteId"], reverse=True)
    return items


def apply_batch(path):
    data = json.load(open(path))
    n_fix = n_clear = 0
    for item in data:
        nid = int(item["noteId"])
        fields = dict(item.get("fields") or {})
        if item.get("clear_feedback"):
            fields[FEEDBACK_FIELD] = ""
        if not fields:
            continue
        call("updateNoteFields", note={"id": nid, "fields": fields})
        if item.get("fields"):
            n_fix += 1
        if item.get("clear_feedback"):
            n_clear += 1
    print(f"applied: {n_fix} card fix(es), {n_clear} feedback field(s) cleared")


def clear(note_ids):
    for nid in note_ids:
        call("updateNoteFields", note={"id": int(nid), "fields": {FEEDBACK_FIELD: ""}})
    print(f"cleared Card Feedback on {len(note_ids)} note(s)")


def show(note_id):
    n = call("notesInfo", notes=[int(note_id)])[0]
    print(f"note {n['noteId']}  ({n['modelName']})")
    for k, v in n["fields"].items():
        print(f"  [{k}] {v['value']!r}")


def main():
    ap = argparse.ArgumentParser(description="Harvest/clear Parker's hidden Card Feedback complaints.")
    ap.add_argument("--harvest", action="store_true", help="collect non-empty feedback (default)")
    ap.add_argument("--apply", metavar="FIXES.json", help="apply a write-back batch (fixes and/or clears)")
    ap.add_argument("--clear", nargs="+", metavar="noteId", help="blank Card Feedback on these notes")
    ap.add_argument("--show", metavar="noteId", help="print one note's fields")
    args = ap.parse_args()

    call("version")  # liveness check (exits if Anki closed)

    if args.apply:
        apply_batch(args.apply); return
    if args.clear:
        clear(args.clear); return
    if args.show:
        show(args.show); return

    # default: harvest
    items = harvest()
    if not items:
        print("No card feedback waiting. (Nothing has a non-empty Card Feedback field.)")
        return
    os.makedirs(WORK, exist_ok=True)
    out = os.path.join(WORK, f"feedback_inbox_{date.today().isoformat()}.json")
    json.dump(items, open(out, "w"), ensure_ascii=False, indent=2)
    print(f"{len(items)} card(s) with feedback -> {out}\n")
    for it in items:
        print(f"── note {it['noteId']}  ·  {it['deck']}")
        print(f"   card: {_plain(it['front'], 140)}")
        print(f"   RANT: {it['feedback']}\n")
    print("Next: process each per SKILL.md → 'Processing card feedback (batch)', "
          "log to reference/feedback-log.md, then clear (or --apply).")


if __name__ == "__main__":
    main()
