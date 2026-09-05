"""inventory_draft.json (hand-verified) -> inventory_final.json in the renderer's schema."""
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(f"{OUT}/inventory_draft.json", encoding="utf-8"))
items = d["items"]
def rows(pred, verify_col=False):
    out=[]
    for it in items:
        if pred(it):
            r=dict(it); 
            if it.get("verify") and it["verify"] not in ("pending",) and verify_col: r["when"] = f'{it["when"]} — audio: {it["verify"]}'
            out.append(r)
    return out
missing = lambda it: it["anki"].startswith("MISSING")
req   = rows(lambda it: it["status"]=="REQUIRED" and missing(it))
taught= rows(lambda it: it["status"] in ("TAUGHT","USED") and missing(it))
gated = rows(lambda it: it["anki"].startswith("SUSPENDED"))
opt   = rows(lambda it: it["status"] in ("OPTIONAL","INCIDENTAL","USED?") and missing(it))
stale = rows(lambda it: it["status"]=="STALE")
for r in gated: r["status"]="GATED"
for r in opt:
    if r["status"]=="USED?": r["status"]="INCIDENTAL"
ITEM_COLS=[["Arabic","ar","ar"],["Translit.","tr","tr"],["Meaning","gloss","txt"],["Where she said it","when","txt"],["Status","status","chip"]]
GATE_COLS=[["Arabic","ar","ar"],["Name","tr","tr"],["What she taught","gloss","txt"],["When","when","txt"],["Anki note","anki","txt"]]
final = {
 "title": "Khouri Vocab Gap Audit",
 "lede": d["lede"],
 "counts": {"required_missing": len(req), "taught_missing": len(taught), "gated": len(gated), "present": d["present_count"]},
 "sections": [
  {"id":"required","heading":"Missing, and she said they are required","intro":d["intro_required"],"cols":ITEM_COLS,"rows":req},
  {"id":"taught","heading":"Missing, taught with a meaning on the board or in the speaking round","intro":d["intro_taught"],"cols":ITEM_COLS,"rows":taught},
  {"id":"gated","heading":"In Anki but still suspended by the letter gate","intro":d["intro_gated"],"cols":GATE_COLS,"rows":gated,"paras":d.get("gated_paras",[])},
  {"id":"optional","heading":"Optional or incidental","intro":d["intro_optional"],"cols":ITEM_COLS,"rows":opt},
  {"id":"present","heading":"Already in Anki and fine","paras":d["present_paras"],"cols":ITEM_COLS,"rows":stale},
  {"id":"skills","heading":"Not vocabulary, but she expects it","intro":d["intro_skills"],"bullets":d["skills"]},
  {"id":"drills","heading":"Appendix: every dictation word she put on the board","intro":d["intro_drills"],"drills":[{"label":k,"words":v} for k,v in d["drill_words_dictated_in_class"].items()]}
 ],
 "method": d["method"]
}
json.dump(final, open(f"{OUT}/inventory_final.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("required",len(req),"taught",len(taught),"gated",len(gated),"opt",len(opt),"stale",len(stale))
