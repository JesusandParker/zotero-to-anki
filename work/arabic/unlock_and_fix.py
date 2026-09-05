#!/usr/bin/env python3
"""(1) unsuspend the six notes the letter gate held back — she has now taught all of them;
   (2) fix the two stale lines the audit found. Authorship: all six letter/mark notes and
   both vocab notes are pipeline-authored, and the edits are additive."""
import json, urllib.request, os
HERE=os.path.dirname(os.path.abspath(__file__))
def ac(action, **params):
    req=json.dumps({"action":action,"version":6,"params":params}).encode()
    r=json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8765",req,{"Content-Type":"application/json"}),timeout=60).read())
    if r.get("error"): raise RuntimeError(f"{action}: {r['error']}")
    return r["result"]
GATED={1786229799726:"yaa (3 Sep)",1786229800702:"hamza (27 Aug / 1 Sep / 3 Sep)",
       1786229799800:"fatHa (3 Sep)",1786229799874:"Damma (3 Sep)",
       1786229799949:"kasra (3 Sep)",1786229800250:"sukuun (3 Sep)"}
roll=[]
for nid,why in GATED.items():
    cids=ac("findCards", query=f"nid:{nid}")
    info=ac("cardsInfo", cards=cids)
    roll.append({"nid":nid,"why":why,"cards":[{"id":c["cardId"],"queue":c["queue"],"type":c["type"],"due":c["due"],"ivl":c["interval"]} for c in info]})
    ac("unsuspend", cards=cids)
    after=ac("cardsInfo", cards=cids)
    print(f"unsuspended {why:<34} nid={nid} cards={len(cids)} queue {[c['queue'] for c in info]} -> {[c['queue'] for c in after]}")
json.dump(roll, open(os.path.join(HERE,"unsuspend_rollback.json"),"w"), indent=1)

# --- stale line 1: maca as-salaama still claims she has not taught it (she confirmed it 3 Sep)
NID_SALAAMA=1787929190843
n=ac("notesInfo", notes=[NID_SALAAMA])[0]; be=n["fields"]["Back Extra"]["value"]
OLD="Pitfall: Dr. Khouri has NOT taught this one yet."
assert OLD in be, "stale line not found — read it before editing"
i=be.index(OLD); j=be.find("<br><br>", i); j = j if j!=-1 else len(be)
new_line=("Ex: she confirmed it on 3 Sep when you asked how to say goodbye — \"if he's leaving "
          "or I'm leaving, <i>maca as-salaama</i>.\" (On 27 Aug she had said \"we didn't talk about this one.\")")
be2=be[:i]+new_line+be[j:]
ac("updateNoteFields", note={"id":NID_SALAAMA,"fields":{"Back Extra":be2}})
print(f"\nfixed maca as-salaama ({NID_SALAAMA}): stale 'not taught yet' -> her 3 Sep confirmation")

# --- stale line 2: ism / ismii need her "S, not SH" correction
ADD="Pitfall: the s is a plain <i>siin</i> — she stopped a student on 3 Sep with \"S, not SH.\""
for nid,label in ((1788401440019,"ism"),(1786229801372,"ismii")):
    n=ac("notesInfo", notes=[nid])[0]; be=n["fields"]["Back Extra"]["value"]
    if "S, not SH" in be: print(f"  {label} already has it"); continue
    ac("updateNoteFields", note={"id":nid,"fields":{"Back Extra":be+"<br><br>"+ADD}})
    print(f"fixed {label} ({nid}): added her 'S, not SH' correction")
