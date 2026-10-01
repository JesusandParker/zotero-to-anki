#!/usr/bin/env python3
"""
io_write.py — write the Image Occlusion notes (io/io_notes.json) into Anki, the same way
anki_write.py writes cloze notes:

  * media stored under the SAME name anki_write gives a figure ("biol214-w06_<file>",
    lowercase), so a plate used by both an IO note and a cloze card is stored once;
    every store is read back and byte-compared before any note references it (R45);
    the RETURNED filename is what the note uses (R47)
  * each note pre-flighted with canAddNotesWithErrorDetail, written one at a time
  * every returned note id read back with notesInfo (R65)
  * every write fingerprinted in the authorship store, so a later pass can tell these
    fields from Parker's own edits

Usage:  python3 io_write.py [--dry-run] [--only id1,id2]
"""
import argparse, base64, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
SKILL = os.path.dirname(os.path.dirname(W))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import authorship  # noqa: E402

ANKI = "http://localhost:8765"
SOURCE = "biol214-w06"
ROOT = ("all::LIBERTY::LIBERTY FALL 2026::BIOL 214 - Human Anatomy & Physiology I Lab::"
        "Practical 2::Appendicular Skeleton")
MODEL = "Image Occlusion+"
TAGS = ["BIOL214", "W06", "practical2", "figure"]


def call(action, **params):
    req = urllib.request.Request(ANKI, data=json.dumps(
        {"action": action, "version": 6, "params": params}).encode())
    res = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if res.get("error"):
        raise RuntimeError(f"{action}: {res['error']}")
    return res["result"]


def store(path):
    raw = f"{SOURCE}_{os.path.basename(path)}"
    fn = re.sub(r"[^A-Za-z0-9._-]+", "_", raw).lower()
    payload = open(path, "rb").read()
    stored = call("storeMediaFile", filename=fn, data=base64.b64encode(payload).decode()) or fn
    echo = call("retrieveMediaFile", filename=stored)
    if not echo or base64.b64decode(echo) != payload:
        sys.exit(f"media round-trip FAILED for {stored}; refusing to reference it")
    return stored


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    notes = json.load(open(os.path.join(W, "io", "io_notes.json")))
    if a.only:
        keep = set(a.only.split(","))
        notes = [n for n in notes if n["id"] in keep]
    call("version")
    if MODEL not in call("modelNames"):
        sys.exit(f"note type {MODEL!r} missing")
    own = authorship.load(SOURCE)
    written, skipped = [], []
    media = {}
    for n in notes:
        deck = f"{ROOT}::{n['deck']}"
        img = os.path.join(W, "figures", n["image"])
        if a.dry_run:
            fn = f"{SOURCE}_{n['image']}".lower()
        else:
            fn = media.get(img) or store(img)
            media[img] = fn
        fields = {"Occlusion": n["occlusion"], "Image": f'<img src="{fn}">',
                  "Header": n["header"], "Back Extra": n["back"], "Comments": ""}
        note = {"deckName": deck, "modelName": MODEL, "fields": fields,
                "tags": TAGS + n.get("tags", []),
                "options": {"allowDuplicate": False, "duplicateScope": "deck"}}
        chk = call("canAddNotesWithErrorDetail", notes=[note])[0]
        if not chk["canAdd"]:
            skipped.append((n["id"], chk.get("error")))
            continue
        if a.dry_run:
            written.append((n["id"], None))
            continue
        nid = call("addNote", note=note)
        authorship.record(SOURCE, nid, fields, run=None, store=own)
        written.append((n["id"], nid))
        print(f"  + {n['id']:24s} {n['cards']:3d} cards -> note {nid}")
    if not a.dry_run:
        authorship.save(SOURCE, own)
        ids = [nid for _, nid in written]
        info = call("notesInfo", notes=ids) if ids else []
        got = {r.get("noteId") for r in info if isinstance(r, dict)}
        lost = [(i, nid) for i, nid in written if nid not in got]
        if lost:
            sys.exit(f"VERIFY FAILED: {lost} did not read back")
        cards = sum(len(r.get("cards", [])) for r in info)
        print(f"verified: {len(got)} IO notes / {cards} cards read back")
        json.dump([{"id": i, "noteId": nid} for i, nid in written],
                  open(os.path.join(W, "io", "io_written.json"), "w"), indent=1)
    print(f"{'[dry-run] would add' if a.dry_run else 'added'} {len(written)}/{len(notes)}")
    for i, why in skipped:
        print(f"  skipped {i}: {why}")


if __name__ == "__main__":
    main()
