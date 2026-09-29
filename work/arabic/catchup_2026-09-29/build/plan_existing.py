#!/usr/bin/env python3
"""Build build/existing_plan.json for apply_existing.py (see that file for the safety rules)."""
import json, os, re, sys, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_cards as G
import letters as LT
from merge import parts

BASE = os.path.expanduser("~/arabic-catchup")
FILE_DATE = lambda fid: fid.split("_")[-1]

def main():
    inv = json.load(open(f"{BASE}/inv/anki_inventory.json"))
    byid = {o["nid"]: o for o in inv}
    master = json.load(open(f"{BASE}/build/master.json"))
    plan = {"field_updates": [], "tags": [], "unsuspend": [], "media": {}}

    # 1. her voice for existing words that lack it -> empty Lecture Notes
    her = G.her_clips_by_key()
    for r in master:
        if not r.get("anki") or r["key"] not in her: continue
        e = her[r["key"]]
        for nid in r["anki"]:
            o = byid[nid]
            if any("khouri" in s for s in o["sounds"]): continue
            # her clip must be the note's MAIN word, not a look-alike listed beside it (akhbaar / akbar)
            main = parts(o["arabic"][0])[0] if o["arabic"] and parts(o["arabic"][0]) else None
            if main != r["key"]: continue
            d = G.md(FILE_DATE(e["chosen"]["file"]))
            plan["field_updates"].append({"nid": nid, "field": "Lecture Notes", "mode": "fill_empty",
                                          "value": f"Dr. Khouri says it ({d}): [sound:{e['out']}]"})
            plan["media"][e["out"]] = f"{BASE}/clips/{e['out']}"

    # 2. letters: her letter-name clip + an example word per existing form note
    letter_clips = {}
    lp = f"{BASE}/cutter/cut_log_letters.json"
    if os.path.exists(lp):
        T = {t["slug"]: t for t in json.load(open(f"{BASE}/cutter/targets_letters.json"))}
        for slug, v in json.load(open(lp)).items():
            if v.get("status") == "PASS" and slug in T:
                letter_clips[T[slug]["key"].split(":")[1]] = v["out"]
                plan["media"][v["out"]] = f"{BASE}/clips/{v['out']}"
    cards = json.load(open(f"{BASE}/build/cards.json")) if os.path.exists(f"{BASE}/build/cards.json") else []
    import build_all
    pool = build_all.example_pool([c for c in cards if c["block"] == "C_vocab"], inv)
    NAME2L = {v: k for k, v in {"ا": "alif", "ب": "baa", "ت": "taa", "ث": "thaa", "ج": "jiim", "ح": "Haa",
                                  "خ": "khaa", "و": "waaw", "ي": "yaa"}.items()}
    used = collections.defaultdict(set)
    for o in inv:
        if len(o["c2"]) < 2 or o["c2"][1].split("::")[0] not in ("initial", "medial", "final", "medial and final"): continue
        L = NAME2L.get(o["c2"][0]); want = o["c2"][1].split("::")[0]
        if not L: continue
        ex = LT.pick_example(pool, L, want, avoid=used[L])
        lines = []
        if ex:
            used[L].add(ex["arabic"])
            lines = LT.example_lines([ex])
            if ex.get("audio_src"): plan["media"][ex["audio"]] = ex["audio_src"]
        clip = letter_clips.get(L)
        if clip and not any("khouri" in s for s in o["sounds"]): lines.append(f"Dr. Khouri says it: [sound:{clip}]")
        if not lines: continue
        value = "<br><br>".join(lines)
        # Unit 2 form notes are pipeline-owned (append to Back Extra); the Unit 3 cram notes are not (Lecture Notes)
        mode, field = ("append_missing", "Back Extra") if "ARAB101::from::book" in o["tags"] and "u3-positions" not in o["tags"] else ("append_missing", "Lecture Notes")
        plan["field_updates"].append({"nid": o["nid"], "field": field, "mode": mode, "value": value})
    # Unit 1 letter notes (Back Extra is Parker-edited): her clip in the empty Lecture Notes
    for o in inv:
        if "Name:" not in o["text"] or not o["arabic"]: continue
        L = o["arabic"][0]
        if L in letter_clips and not any("khouri" in s for s in o["sounds"]):
            plan["field_updates"].append({"nid": o["nid"], "field": "Lecture Notes", "mode": "append_missing",
                                          "value": f"Dr. Khouri says it: [sound:{letter_clips[L]}]"})

    # 3. tier + required tags on existing notes
    tiers = json.load(open(f"{BASE}/build/existing_tiers.json"))
    req = {nid for r in master if r.get("anki") for k in r["khouri"] if k.get("status") == "required" for nid in r["anki"]}
    tier_of = {}
    for t, ids in tiers.items():
        for i in ids: tier_of[i] = t
    for o in inv:
        t = tier_of.get(o["nid"])
        if "Name:" in o["text"] or "Letter:" in o["text"]: t = "letters"
        add = [f"ARAB101::tier::{t}"] if t else []
        if o["nid"] in req: add.append("ARAB101::required")
        if o["nid"] == 1790070935881: add.append("ARAB101::from::quiz-prep-2026-09-22")
        if add: plan["tags"].append({"nid": o["nid"], "add": add})

    # 4. unsuspend: lockdown leftovers + the Unit 4 letters daal/dhaal/raa/zaay (+ hamza is a leftover)
    sc = json.load(open(f"{BASE}/inv/suspension_classes.json"))
    plan["unsuspend"] = list(sc["lockdown_leftover_cards"])
    for o in inv:
        if o["arabic"] and o["arabic"][0] in ("د", "ذ", "ر", "ز") and "Name:" in o["text"]:
            import urllib.request
            q = json.dumps({"action": "findCards", "version": 6, "params": {"query": f"nid:{o['nid']} is:suspended"}}).encode()
            plan["unsuspend"] += json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:8765", q)))["result"]
    plan["unsuspend"] = sorted(set(plan["unsuspend"]))
    hold = os.path.expanduser("~/.anki-cram-suspend-20260929-arabic.json")
    if os.path.exists(hold) and not json.load(open(hold)).get("restored_at"):
        # the cards are held with Parker's BIOL 214 cram; the autopilot restores them at restore_after
        plan["unsuspend"] = []
    json.dump(plan, open(f"{BASE}/build/existing_plan.json", "w"), ensure_ascii=False, indent=1)
    c = collections.Counter((u["field"], u["mode"]) for u in plan["field_updates"])
    print("field updates:", dict(c), "| tag sets:", len(plan["tags"]), "| unsuspend:", len(plan["unsuspend"]), "| media:", len(plan["media"]))

if __name__ == "__main__":
    main()
