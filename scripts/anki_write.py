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
import argparse, base64, hashlib, json, os, re, sys, urllib.request

ANKI = "http://localhost:8765"
# 2026-07-01: Parker's homemade cloze cards migrated to "AnKing Cloze" during the
# 2026-06-29 styling session (the old "01_Cloze - Parkers Note Type" was deleted).
# AnKing Cloze fields: Text, Back Extra, Lecture Notes, Missed Questions,
# Additional Resources — we fill only the first two; the rest are Parker's own
# study-time fields and stay empty.
MODEL = "AnKing Cloze"
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
    ap.add_argument("--force", action="store_true",
                    help="stage even if the verification stamp is missing/stale (escape hatch)")
    args = ap.parse_args()

    # Verification gate: refuse to stage a file that check_cards.py didn't pass clean.
    # The stamp is a hash of the exact bytes, so editing the JSON after the check
    # invalidates it. This turns Stage 2.75 from "please don't skip" into "can't skip".
    if not args.dry_run and not args.force:
        stamp = args.cards_json + ".verified"
        cur = hashlib.sha256(open(args.cards_json, "rb").read()).hexdigest()
        ok = False
        if os.path.exists(stamp):
            try:
                ok = json.load(open(stamp)).get("sha256") == cur
            except Exception:
                ok = False
        if not ok:
            sys.exit(
                f"ERROR: no valid verification stamp for {args.cards_json}.\n"
                f"Run the gate first:  python3 scripts/check_cards.py {args.cards_json}\n"
                f"(Then re-run this.)  If check_cards passed but you edited the JSON after, "
                f"re-run check_cards to re-stamp. Use --force only to deliberately bypass.")

    cards = json.load(open(args.cards_json))
    call("version")  # liveness check (exits if Anki closed)
    if MODEL not in call("modelNames"):
        sys.exit(f"ERROR: note type '{MODEL}' not found in collection. Parker's cards live on "
                 f"this model since 2026-06-29; if it was renamed, update MODEL here to match "
                 f"whatever cloze type his current cards use (check notesInfo on tag:claude_generated).")
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
