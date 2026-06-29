#!/usr/bin/env python3
"""
anki_write.py — final stage: write finished cards into the Anki review subdeck.

Reads a JSON list of cards and adds each one as a cloze note via AnkiConnect,
safely:
  * checks Anki is actually running (fails loud if not)
  * ensures the target deck and the note type exist
  * validates every Text field contains cloze markup ({{c1::...}})
  * pre-flights each note with canAddNotesWithErrorDetail
  * writes ONE note at a time (never a batch) so one bad card can't roll back the rest
  * tags every card 'claude_generated' + 'ch<N>' so a batch is filterable / reversible
  * does NOT auto-sync to AnkiWeb (Parker syncs deliberately)

Card JSON shape (list of objects):
  {"Text": "...{{c1::answer::hint}}...", "Back Extra": "Cue: ...", "chapter": 1,
   "image": "/abs/path/to/page.png"  (optional; added to media and <img>-embedded)}

Usage:
    python3 anki_write.py cards.json
    python3 anki_write.py cards.json --deck "EMT::_Review" --dry-run
"""
import argparse, base64, json, os, re, sys, urllib.request

ANKI = "http://localhost:8765"
MODEL = "01_Cloze - Parkers Note Type"
DEFAULT_DECK = "EMT::_Review"
CLOZE_RE = re.compile(r"\{\{c\d+::")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards_json")
    ap.add_argument("--deck", default=DEFAULT_DECK)
    ap.add_argument("--dry-run", action="store_true", help="validate only, write nothing")
    args = ap.parse_args()

    cards = json.load(open(args.cards_json))
    call("version")  # liveness check (exits if Anki closed)
    if MODEL not in call("modelNames"):
        sys.exit(f"ERROR: note type '{MODEL}' not found in collection. Recreate it (fields: Text, Back Extra).")
    call("createDeck", deck=args.deck)

    added, skipped = 0, []
    for i, c in enumerate(cards):
        text = c.get("Text", "")
        if not CLOZE_RE.search(text):
            skipped.append((i, "no cloze markup in Text")); continue

        # optional page image -> store in Anki media and embed
        if c.get("image") and os.path.exists(c["image"]):
            fn = f"emt_{os.path.basename(c['image'])}"
            call("storeMediaFile", filename=fn,
                 data=base64.b64encode(open(c["image"], "rb").read()).decode())
            text = text + f'<br><img src="{fn}">'

        tags = ["claude_generated"]
        if c.get("chapter"):
            tags.append(f"ch{c['chapter']}")
        note = {
            "deckName": args.deck, "modelName": MODEL,
            "fields": {"Text": text, "Back Extra": c.get("Back Extra", "")},
            "tags": tags,
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        }
        chk = call("canAddNotesWithErrorDetail", notes=[note])[0]
        if not chk["canAdd"]:
            skipped.append((i, chk.get("error", "canAdd=false"))); continue
        if args.dry_run:
            added += 1; continue
        call("addNote", note=note)
        added += 1

    print(f"{'[dry-run] would add' if args.dry_run else 'added'}: {added}/{len(cards)} -> {args.deck}")
    if skipped:
        print(f"skipped {len(skipped)}:")
        for i, why in skipped:
            print(f"  card #{i}: {why}")


if __name__ == "__main__":
    main()
