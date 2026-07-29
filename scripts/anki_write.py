#!/usr/bin/env python3
"""
anki_write.py — final stage: write finished cards into the source's staging deck.

Reads a JSON list of cards and adds each one as a cloze note via AnkiConnect, safely:
  * refuses to run unless check_cards.py stamped THESE exact bytes (the unskippable gate)
  * checks Anki is actually running (fails loud if not)
  * resolves the target deck, note type, and tags from the SOURCE REGISTRY
  * ensures the staging deck AND Parker's promotion deck exist before writing
  * validates every Text field contains cloze markup ({{c1::...}})
  * pre-flights each note with canAddNotesWithErrorDetail
  * writes ONE note at a time (never a batch) so one bad card can't roll back the rest
  * does NOT auto-sync to AnkiWeb (Parker syncs deliberately)

Every source keeps the two-deck promotion gate: the pipeline writes ONLY to the staging
deck ("claude review"), and Parker promotes keepers into the sibling himself. The deck
NAMES come from the registry, so a lecture doesn't inherit book-shaped naming.

Card JSON shape (list of objects):
  {"Text": "...{{c1::answer::hint}}...", "Back Extra": "Cue: ...",
   "source": "emt", "segment": 1,
   "image": "/abs/path/to/page.png"  (optional; added to media and <img>-embedded)}
`chapter` is still accepted as a synonym for `segment` (the original EMT canon files).

Usage:
    python3 anki_write.py work/emt/chapter_6_cards.json
    python3 anki_write.py work/emt/chapter_6_cards.json --dry-run
    python3 anki_write.py cards.json --source arabic
    python3 anki_write.py cards.json --deck "all::Other::languages::arabic::claude review"
"""
import argparse, base64, hashlib, json, os, re, sys, urllib.request

import sources as S

ANKI = "http://localhost:8765"
CLOZE_RE = re.compile(r"\{\{c\d+::")

# Parker wants a full paragraph break BETWEEN Back Extra components (e.g. a Distinguish
# line and a Pitfall line) — real white space, not a tight single line break (2026-07-02).
# Back Extra never breaks inside one flowing component (card-rules #5), so every run of
# <br> is a component boundary: collapse each to exactly <br><br>. Idempotent — cards
# already authored with <br><br> are untouched. This is the mechanical guarantee behind
# the rule, so the spacing holds even if a card is drafted with single <br>s.
_BR_RUN = re.compile(r"(?:\s*<br\s*/?>\s*)+", re.I)


def paragraphize(back_extra):
    if not back_extra:
        return back_extra
    be = _BR_RUN.sub("<br><br>", back_extra)
    return re.sub(r"^(?:<br>)+|(?:<br>)+$", "", be)  # trim any stray leading/trailing break


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


def seg_of(card):
    """Segment number for a card, accepting the legacy 'chapter' key."""
    v = card.get("segment", card.get("chapter"))
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards_json")
    ap.add_argument("--source", default=None,
                    help="source id (default: read from the cards' 'source' field)")
    ap.add_argument("--deck", default=None,
                    help="override the target deck entirely (default: from the registry, "
                         "per card, using its segment)")
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
    if not cards:
        sys.exit(f"ERROR: {args.cards_json} contains no cards.")

    # ---- which source? explicit flag, else the cards' own field, else fail loudly.
    source_id = args.source or next((c.get("source") for c in cards if c.get("source")), None)
    if not source_id and not args.deck:
        sys.exit("ERROR: cannot tell which source these cards belong to.\n"
                 "Add a \"source\": \"<id>\" field to the cards, or pass --source <id> "
                 "(see: python3 scripts/sources.py list), or pass --deck to route manually.")
    src = S.get_source(source_id) if source_id else None
    model = S.model(src) if src else "AnKing Cloze"

    call("version")  # liveness check (exits if Anki closed)
    if model not in call("modelNames"):
        sys.exit(f"ERROR: note type '{model}' not found in collection. Parker's cards live on "
                 f"this model since 2026-06-29; if it was renamed, update the source's "
                 f"\"model\" in reference/sources.json (or the registry default) to match "
                 f"whatever cloze type his current cards use.")

    # ---- create each segment's full substructure so BOTH our target ("claude review")
    # and Parker's promotion target exist before we write.
    if args.deck:
        call("createDeck", deck=args.deck)
        new_decks = [args.deck]
    else:
        segs = sorted({seg_of(c) for c in cards}, key=lambda v: (v is None, v))
        new_decks = []
        for seg in segs:
            staging, promote = S.deck_names(src, seg)
            call("createDeck", deck=staging)
            call("createDeck", deck=promote)
            new_decks += [staging, promote]
    # Fresh subdecks default to Anki's "Default" preset (bury-siblings OFF); two-way
    # definition cards need bury-siblings ON so the name-it/define-it halves space across
    # days. Copy the source root's preset onto the subdecks we just made. Non-fatal.
    if src:
        try:
            root_cfg = call("getDeckConfig", deck=src["deck_root"])["id"]
            call("setDeckConfigId", decks=new_decks, configId=root_cfg)
        except Exception:
            pass

    added, skipped = 0, []
    targets = set()
    for i, c in enumerate(cards):
        text = c.get("Text", "")
        if not CLOZE_RE.search(text):
            skipped.append((i, "no cloze markup in Text")); continue

        seg = seg_of(c)
        if args.deck:
            deck, tags = args.deck, (S.tags_for(src, seg) if src else [])
        else:
            deck, _promote = S.deck_names(src, seg)
            tags = S.tags_for(src, seg)
        if not deck:
            skipped.append((i, "no deck could be derived (missing segment and no --deck)")); continue
        targets.add(deck)  # record the INTENDED target, even if the card is skipped below

        # optional page image -> store in Anki media and embed
        if c.get("image") and os.path.exists(c["image"]):
            fn = f"{(src or {}).get('id','z2a')}_{os.path.basename(c['image'])}"
            call("storeMediaFile", filename=fn,
                 data=base64.b64encode(open(c["image"], "rb").read()).decode())
            text = text + f'<br><img src="{fn}">'

        note = {
            "deckName": deck, "modelName": model,
            "fields": {"Text": text, "Back Extra": paragraphize(c.get("Back Extra", ""))},
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

    print(f"{'[dry-run] would add' if args.dry_run else 'added'}: {added}/{len(cards)}")
    for t in sorted(targets):
        print(f"  -> {t}")
    if not targets:
        print("  (no target deck resolved — every card lacked a segment and no --deck was given)")
    if src and not args.deck:
        segs = sorted({seg_of(c) for c in cards}, key=lambda v: (v is None, v))
        for seg in segs:
            _s, promote = S.deck_names(src, seg)
            print(f"  (promote keepers into: {promote})")
    if skipped:
        print(f"skipped {len(skipped)}:")
        for i, why in skipped:
            print(f"  card #{i}: {why}")


if __name__ == "__main__":
    main()
