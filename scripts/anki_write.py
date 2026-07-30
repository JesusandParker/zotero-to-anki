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
import authorship

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


# When a Text field is a LIST of things to produce, Parker wants each item on its own line
# with a blank line between them, so that a glance tells him HOW MANY answers he owes
# (2026-07-30). Packed single-<br> rows read as one grey block and hide the count. This is
# the Text-field twin of paragraphize() above, and the same contract: a rule in the docs
# AND a mechanical guarantee here, so the spacing holds even if a card is drafted tight.
#
# It fires ONLY on genuine list layouts, and "is this a list?" has exactly ONE definition:
# check_cards.list_shaped(). It lives there (the rules module) and is imported here so the
# REPAIRER and the WARNING can never disagree. They previously held separate copies of the
# same predicate and therefore the same bug — an all()-veto that let one long row silence
# both — which is how 12 packed cards reached Parker's review (2026-07-30).
_CLOZE_ANY = re.compile(r"\{\{c\d+::(.*?)(?:::(.*?))?\}\}")

from check_cards import list_shaped  # noqa: E402  (same dir; no import-time side effects)


def listify(text):
    """Blank line between the rows of a list-shaped Text. Idempotent; leaves prose alone."""
    if not text or "<img" in text.lower() or not re.search(r"<br", text, re.I):
        return text
    if not list_shaped(text):
        return text
    return "<br><br>".join(s.strip() for s in _BR_RUN.split(text) if s.strip())


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
    ap.add_argument("--run", default=None,
                    help="run directory from run_store.start_run(); the returned Anki noteIds are "
                         "written back into its provenance.jsonl so any card in Anki can be traced "
                         "to its mark, page, block, agent and judge verdict")
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
    note_ids = []   # (card_index, ankiNoteId) -> written back into the run's provenance
    own = authorship.load(source_id or "unknown")   # fingerprints of what WE write
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

        # optional figure -> store in Anki media and embed
        #
        # It goes on the BACK by default. A textbook plate labels its own anatomy, so the
        # very figures worth attaching are the ones whose labels ARE the cloze answers —
        # put the labeled skull on the front of "the cranium is formed by the
        # {{c1::frontal}}, {{c1::temporal}}..." and the card answers itself. On the back it
        # reinforces instead: he produces the words, then sees where they live.
        # Set "image_side": "front" only for a card that ASKS about the picture (identify
        # this structure), where the image is the question and leaks nothing.
        back = paragraphize(c.get("Back Extra", ""))
        if c.get("image") and os.path.exists(c["image"]):
            # Keep the stored name free of anything that needs escaping inside an
            # attribute. A source id or figure basename containing a space would
            # otherwise emit <img src="a b.png"> and silently render as a broken image.
            raw = f"{(src or {}).get('id','z2a')}_{os.path.basename(c['image'])}"
            fn = re.sub(r"[^A-Za-z0-9._-]+", "_", raw)
            call("storeMediaFile", filename=fn,
                 data=base64.b64encode(open(c["image"], "rb").read()).decode())
            tag = f'<img src="{fn}">'
            if c.get("image_side") == "front":
                text = text + "<br>" + tag
            else:
                back = (back + "<br><br>" + tag) if back.strip() else tag

        note = {
            "deckName": deck, "modelName": model,
            "fields": {"Text": listify(text), "Back Extra": back},
            "tags": tags,
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        }
        chk = call("canAddNotesWithErrorDetail", notes=[note])[0]
        if not chk["canAdd"]:
            skipped.append((i, chk.get("error", "canAdd=false"))); continue
        if args.dry_run:
            added += 1; continue
        nid = call("addNote", note=note)
        if nid:
            note_ids.append((i, nid))
            # Record EXACTLY what we wrote, so a later pass can tell our text from
            # Parker's edits and never overwrite his (see scripts/authorship.py).
            authorship.record(source_id or "unknown", nid, note["fields"],
                              run=args.run, store=own)
        added += 1

    if not args.dry_run:
        authorship.save(source_id or "unknown", own)
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
    # Link every staged card back to its run record. The link lives in the REPO, not as a
    # tag on the note: Parker had the `claude_generated` tag stripped from every card as
    # noise and keeps `ch<N>` only, so traceability must not cost him deck clutter.
    if args.run and note_ids and not args.dry_run:
        try:
            import run_store as R
            n = R.attach_note_ids(args.run, note_ids)
            print(f"  linked {n} card(s) to their provenance in {os.path.basename(args.run)}")
            print(f"  trace any of them later with:  python3 scripts/run_store.py trace <noteId>")
        except Exception as e:
            print(f"  WARNING: could not write note ids into the run record ({e})")
    elif note_ids and not args.dry_run:
        print("  NOTE: no --run given, so these cards have no traceable provenance record.")

    if skipped:
        print(f"skipped {len(skipped)}:")
        for i, why in skipped:
            print(f"  card #{i}: {why}")


if __name__ == "__main__":
    main()
