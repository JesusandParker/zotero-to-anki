#!/usr/bin/env python3
"""
tag_notes.py — after anki_write, give each cloze note its per-card tags.

anki_write tags every note with the source's registry tags (BIOL214 W06 practical2) only.
This deck also carries, per card (`extra_tags`, set by make_cards.py):
  src::slides / src::recording / src::study-guide / src::manual / src::blue-pages /
  src::popcorn   — which source(s) the fact was read from, so the deck can be cut down to
                   one source later (the W05 quiz trim needed exactly that)
  optional       — the lab said this is not required
The run's provenance.jsonl maps card_index -> anki_note_id (anki_write --run writes it), so
every tag lands on exactly the note that card became. Read back and verified.

Usage:  python3 tag_notes.py <cards_json> <run_dir> [--dry-run]
"""
import json, os, sys, urllib.request


def ak(a, **p):
    r = json.loads(urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765", json.dumps({"action": a, "version": 6, "params": p}).encode(),
        {"Content-Type": "application/json"}), timeout=120).read())
    if r.get("error"):
        raise RuntimeError(f"{a}: {r['error']}")
    return r["result"]


def main():
    cards_json, run = sys.argv[1], sys.argv[2]
    dry = "--dry-run" in sys.argv
    cards = json.load(open(cards_json))
    nid_of = {}
    for line in open(os.path.join(run, "provenance.jsonl")):
        r = json.loads(line)
        if r.get("anki_note_id") is not None:
            nid_of[r["card_index"]] = r["anki_note_id"]
    missing = [i for i in range(len(cards)) if i not in nid_of]
    if missing:
        sys.exit(f"{len(missing)} card(s) have no anki_note_id in {run}: {missing[:10]}")
    by_tags = {}
    for i, c in enumerate(cards):
        tags = tuple(sorted(c.get("extra_tags") or []))
        if tags:
            by_tags.setdefault(tags, []).append(nid_of[i])
    for tags, nids in by_tags.items():
        print(f"  {len(nids):3d} notes  +{' '.join(tags)}")
        if not dry:
            ak("addTags", notes=nids, tags=" ".join(tags))
    if dry:
        return
    info = ak("notesInfo", notes=list(nid_of.values()))
    have = {n["noteId"]: set(n["tags"]) for n in info}
    bad = [(i, nid_of[i]) for i, c in enumerate(cards)
           if not set(c.get("extra_tags") or []) <= have.get(nid_of[i], set())]
    if bad:
        sys.exit(f"VERIFY FAILED: tags missing on {bad[:10]}")
    print(f"verified: tags present on all {len(cards)} notes")


if __name__ == "__main__":
    main()
