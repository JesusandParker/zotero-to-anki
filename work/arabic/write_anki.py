#!/usr/bin/env python3
"""Stage the gap-audit batch: media first (verified round-trip), then notes, then the Audio field."""
import json, os, base64, sys, urllib.request, hashlib
HERE=os.path.dirname(os.path.abspath(__file__))
DECK="all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I::Unit 2::Khouri Spoken 2026-09-05"
TAGS=["arabic-u2","khouri-spoken-2026-09-05"]
def ac(action, **params):
    req=json.dumps({"action":action,"version":6,"params":params}).encode()
    r=json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8765",req,{"Content-Type":"application/json"}),timeout=60).read())
    if r.get("error"): raise RuntimeError(f"{action}: {r['error']}")
    return r["result"]
cards=json.load(open(os.path.join(HERE,"gapaudit_cards.json"),encoding="utf-8"))
DRY = "--dry-run" in sys.argv
# ---- 1. media, with a verified round-trip (note-format.md rule 3)
media={}
for f in sorted(os.listdir(os.path.join(HERE,"clips"))):
    p=os.path.join(HERE,"clips",f); raw=open(p,"rb").read()
    if DRY: media[f]=f; continue
    got=ac("storeMediaFile", filename=f, data=base64.b64encode(raw).decode())
    back=base64.b64decode(ac("retrieveMediaFile", filename=got))
    assert hashlib.sha256(back).hexdigest()==hashlib.sha256(raw).hexdigest(), f"round-trip mismatch {f}"
    media[f]=got
    if got!=f: print(f"  NOTE: stored as {got} (requested {f})")
print(f"media: {len(media)} files stored + round-trip verified")
# ---- 2. deck + preset
if not DRY:
    ac("createDeck", deck=DECK)
    cfg=ac("getDeckConfig", deck="all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I::Unit 2::Khouri Thursday 2026-09-03")
    ac("setDeckConfigId", decks=[DECK], configId=cfg["id"])
    print(f"deck: {DECK}\npreset: {cfg['name']} (new/day {cfg['new']['perDay']}, buryNew {cfg['new'].get('bury')})")
# ---- 3. notes, one at a time, pre-flighted
ids=[]
for c in cards:
    note={"deckName":DECK,"modelName":"AnKing Cloze",
          "fields":{"Text":c["Text"],"Back Extra":c["Back Extra"],"Audio":c.get("Audio","")},
          "tags":TAGS,"options":{"allowDuplicate":False}}
    assert "{{c1::" in c["Text"], c["slug"]
    if DRY:
        ok=ac("canAddNotesWithErrorDetail", notes=[note])[0]
        print(f"  {'OK ' if ok['canAdd'] else 'NO '} {c['slug']:<18} {ok.get('error','')}")
        continue
    nid=ac("addNote", note=note); ids.append({"slug":c["slug"],"noteId":nid})
    print(f"  + {c['slug']:<18} {nid}")
if not DRY:
    json.dump(ids, open(os.path.join(HERE,"gapaudit_note_ids.json"),"w"), indent=1)
    print(f"\n{len(ids)} notes written")
