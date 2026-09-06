#!/usr/bin/env python3
"""Store the gated clips under NEW names, repoint the notes, add the Back Extra lines,
then delete any file the swap orphaned. Media rule R45: never reuse a filename."""
import json, os, base64, hashlib, urllib.request
HERE=os.path.dirname(os.path.abspath(__file__))
def ac(a,**p):
    r=json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8765",
        json.dumps({"action":a,"version":6,"params":p}).encode(),
        {"Content-Type":"application/json"}),timeout=60).read())
    if r.get("error"): raise RuntimeError(f"{a}: {r['error']}")
    return r["result"]
gate=[r for r in json.load(open(f"{HERE}/fixes_gate.json",encoding="utf-8")) if r.get("dur")]
noteids={n["slug"]:n["noteId"] for n in json.load(open(f"{HERE}/gapaudit_note_ids.json",encoding="utf-8"))}
edits=json.load(open(f"{HERE}/text_edits.json",encoding="utf-8"))
orphans=[]
for r in gate:
    slug=r["slug"]; nid=noteids[slug]; f=r["file"]
    note=ac("notesInfo",notes=[nid])[0]; old=note["fields"]["Audio"]["value"].strip()
    data=open(f"{HERE}/clips2/{f}","rb").read()
    got=ac("storeMediaFile",filename=f,data=base64.b64encode(data).decode())
    back=base64.b64decode(ac("retrieveMediaFile",filename=got))
    assert hashlib.sha256(back).hexdigest()==hashlib.sha256(data).hexdigest(), f"round-trip {f}"
    ac("updateNoteFields",note={"id":nid,"fields":{"Audio":f"[sound:{got}]"}})
    print(f"  {slug:<16} Audio {old or '(empty)'} -> [sound:{got}]  ({r['dur']}s, ar={r['ar'][:18]!r})")
    if old.startswith("[sound:") and got not in old:
        orphans.append(old[7:-1])
for slug,e in edits.items():
    nid=noteids.get(slug)
    if not nid: continue
    be=ac("notesInfo",notes=[nid])[0]["fields"]["Back Extra"]["value"]
    key=e["append"].split("[sound:")[0][:38]
    if key and key in be: print(f"  {slug}: Back Extra already carries it"); continue
    ac("updateNoteFields",note={"id":nid,"fields":{"Back Extra":be+"<br><br>"+e["append"]}})
    print(f"  {slug}: Back Extra += {e['append'][:56]}…")
# an orphan is only deletable once nothing references it
refs=set()
for n in ac("notesInfo",notes=ac("findNotes",query='tag:khouri-spoken-2026-09-05')):
    refs.add(n["fields"]["Audio"]["value"]); refs.add(n["fields"]["Back Extra"]["value"])
blob=" ".join(refs)
for o in orphans:
    if o in blob: print(f"  keeping {o} — still referenced"); continue
    ac("deleteMediaFile",filename=o); print(f"  deleted orphan {o}")
print("\ndone")
