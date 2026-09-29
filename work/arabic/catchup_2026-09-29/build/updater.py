#!/usr/bin/env python3
"""Bring the catch-up notes already in Anki up to date with build/cards.json (audio upgrades, fixed lines).
Only notes this build CREATED (build/created_notes.json) are touched; matched by exact Text.
Fields compared: Back Extra, Audio, Lecture Notes; tags: the ARAB101::no-audio marker follows the Audio field.
usage: updater.py [--apply]"""
import json, os, sys, base64, urllib.request
BASE = os.path.expanduser("~/arabic-catchup")
def ac(a, **p):
    r = json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:8765", json.dumps({"action": a, "version": 6, "params": p}).encode()), timeout=120))
    if r.get("error"): raise RuntimeError(f"{a}: {r['error']}")
    return r["result"]
apply = "--apply" in sys.argv
cards = {c["Text"]: c for c in json.load(open(f"{BASE}/build/cards.json"))}
created = [c["nid"] for c in json.load(open(f"{BASE}/build/created_notes.json"))]
info = ac("notesInfo", notes=created)
have = set(ac("getMediaFilesNames", pattern="arabic*"))
changes, media, unmatched = [], {}, 0
for n in info:
    t = n["fields"]["Text"]["value"]; c = cards.get(t)
    if not c: unmatched += 1; continue
    upd = {f: c.get(f, "") for f in ("Back Extra", "Audio", "Lecture Notes") if (c.get(f, "") or "") != n["fields"][f]["value"]}
    if upd:
        changes.append((n["noteId"], upd, c.get("Audio"), n["tags"]))
        for name, src in (c.get("media") or {}).items():
            if name not in have and src: media[name] = src
print(f"{len(changes)} notes to update, {len(media)} new media, {unmatched} unmatched")
if apply:
    for name, src in media.items():
        ac("storeMediaFile", filename=name, data=base64.b64encode(open(src, "rb").read()).decode())
    for nid, upd, audio, tags in changes:
        ac("updateNoteFields", note={"id": nid, "fields": upd})
        if audio and "ARAB101::no-audio" in tags: ac("removeTags", notes=[nid], tags="ARAB101::no-audio")
        if not audio and "ARAB101::no-audio" not in tags: ac("addTags", notes=[nid], tags="ARAB101::no-audio")
    print("applied")
