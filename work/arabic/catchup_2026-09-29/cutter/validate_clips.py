#!/usr/bin/env python3
"""After cutting: any PASS clip whose source span overlaps a span later marked NOT HER (student turn,
publisher audio, deliberate mistake) is invalidated — its log entry is removed so the next cutter run
redoes the word with the updated exclusions, and the mp3 is deleted."""
import json, glob, os
BASE = os.path.expanduser("~/arabic-catchup")
excl = {}
for f in glob.glob(f"{BASE}/lectures/*.json"):
    for w in json.load(open(f)).get("words", []):
        for sp in w.get("not_her_spans") or []:
            if isinstance(sp, dict) and sp.get("file") and sp.get("start") is not None:
                excl.setdefault(sp["file"], []).append((sp["start"] - 0.3, (sp.get("end") or sp["start"] + 1) + 0.3, sp.get("who", "")))
for fid, spans in json.load(open(f"{BASE}/cutter/exclusions.json")).items():
    if fid.startswith("_"): continue
    for sp in spans:
        excl.setdefault(fid, []).append((sp[0], sp[1], sp[2] if len(sp) > 2 else "excluded"))
bad = 0
for lp in glob.glob(f"{BASE}/cutter/cut_log*.json"):
    log = json.load(open(lp)); changed = False
    for slug, v in list(log.items()):
        c = v.get("chosen")
        if not c or not v.get("status", "").startswith("PASS"): continue
        hit = [w for (a, b, w) in excl.get(c["file"], []) if c["s"] < b and c["e"] > a]
        if hit:
            print(f"INVALID {os.path.basename(lp)} {slug}: {c['file']} {c['s']}-{c['e']} overlaps '{hit[0][:60]}'")
            if v.get("out") and os.path.exists(f"{BASE}/clips/{v['out']}"): os.remove(f"{BASE}/clips/{v['out']}")
            del log[slug]; changed = True; bad += 1
    if changed: json.dump(log, open(lp, "w"), ensure_ascii=False, indent=1)
print("invalidated", bad)
