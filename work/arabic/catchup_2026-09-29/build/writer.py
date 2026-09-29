#!/usr/bin/env python3
"""Write note specs to Anki safely.

- media: storeMediaFile only under NEW lowercase names (never replace bytes under an existing
  name, R45); refuses if a name exists with different bytes.
- notes: canAddNotesWithErrorDetail preflight, because addNotes is all-or-nothing per batch.
- every created note id is appended to build/created_notes.json (the rollback list).
usage: writer.py cards.json [--dry]
"""
import json, os, sys, base64, hashlib, urllib.request

BASE = os.path.expanduser("~/arabic-catchup")

def ac(action, **params):
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765", json.dumps({"action": action, "version": 6, "params": params}).encode()), timeout=120))
    if r.get("error"): raise RuntimeError(f"{action}: {r['error']}")
    return r["result"]

def store_media(name, path, existing):
    assert name == name.lower(), f"media name must be lowercase: {name}"
    data = open(path, "rb").read()
    if name in existing:
        cur = ac("retrieveMediaFile", filename=name)
        if cur and hashlib.sha1(base64.b64decode(cur)).hexdigest() == hashlib.sha1(data).hexdigest():
            return "same"
        raise RuntimeError(f"media name collision with DIFFERENT bytes: {name} — version the name")
    ac("storeMediaFile", filename=name, data=base64.b64encode(data).decode())
    existing.add(name)
    return "stored"

def main(path, dry=False):
    cards = json.load(open(path))
    existing = set(ac("getMediaFilesNames", pattern="arabic*"))
    media = {}
    for c in cards:
        for name, src in (c.get("media") or {}).items(): media[name] = src
    print(f"{len(cards)} notes, {len(media)} media files")
    for d in sorted({c["deck"] for c in cards}):
        if not dry: ac("createDeck", deck=d)
    notes = [{"deckName": c["deck"], "modelName": "AnKing Cloze",
              "fields": {"Text": c["Text"], "Back Extra": c.get("Back Extra", ""), "Audio": c.get("Audio", ""),
                         "Lecture Notes": c.get("Lecture Notes", "")},
              "tags": c["tags"], "options": {"allowDuplicate": False, "duplicateScope": "deck"}} for c in cards]
    pre = ac("canAddNotesWithErrorDetail", notes=notes)
    bad = [(i, p.get("error")) for i, p in enumerate(pre) if not p.get("canAdd")]
    if bad:
        for i, e in bad[:20]: print("  CANNOT ADD", i, e, cards[i]["Text"][:80])
        sys.exit(f"{len(bad)} notes fail preflight; nothing written")
    if dry:
        print("dry run: preflight clean"); return
    for name, src in media.items(): store_media(name, src, existing)
    ids = ac("addNotes", notes=notes)
    if any(i is None for i in ids): sys.exit(f"addNotes returned nulls: {ids}")
    log = json.load(open(f"{BASE}/build/created_notes.json")) if os.path.exists(f"{BASE}/build/created_notes.json") else []
    log += [{"nid": i, "text": c["Text"][:80], "deck": c["deck"]} for i, c in zip(ids, cards)]
    json.dump(log, open(f"{BASE}/build/created_notes.json", "w"), ensure_ascii=False, indent=0)
    print(f"added {len(ids)} notes")
    # the deck presets: new unit decks must land on the same preset as their siblings
    root_cfg = ac("getDeckConfig", deck="all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I")["id"]
    for d in sorted({c["deck"] for c in cards}):
        if ac("getDeckConfig", deck=d)["id"] != root_cfg:
            ac("setDeckConfigId", decks=[d], configId=root_cfg); print("  preset fixed on", d)

if __name__ == "__main__":
    main(sys.argv[1], dry="--dry" in sys.argv)
