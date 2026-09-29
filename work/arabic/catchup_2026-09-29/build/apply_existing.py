#!/usr/bin/env python3
"""Changes to EXISTING Arabic notes for the catch-up (never overwrites anything Parker wrote).

1. Her voice on words that lack it -> the EMPTY `Lecture Notes` field ("Dr. Khouri says it (9/24): [sound]").
   Only if that field is empty; `Text`/`Back Extra`/`Audio` are never touched on unknown/edited notes.
2. Letters: her letter-name clip + one example word per form.
   - pipeline-OWNED Unit 2 form notes (authorship store says `owned`): appended to Back Extra.
   - everything else: the empty Lecture Notes field.
3. Tags (never content): ARAB101::tier::<chart|class|letters|concept|practice>, ARAB101::required.
4. Unsuspend: the 121 cards the 2026-09-22 quiz lockdown left suspended + the Unit 4 letters (daal,
   dhaal, raa, zaay). Letters of Units 5+ stay gated.
Every pre-image is written to build/existing_rollback.json BEFORE anything changes.
usage: apply_existing.py plan.json [--apply]
"""
import json, os, sys, subprocess, urllib.request

BASE = os.path.expanduser("~/arabic-catchup")
SKILL = os.path.expanduser("~/.claude/skills/zotero-to-anki")

def ac(action, **params):
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765", json.dumps({"action": action, "version": 6, "params": params}).encode()), timeout=120))
    if r.get("error"): raise RuntimeError(f"{action}: {r['error']}")
    return r["result"]

def owned(nid, field):
    out = subprocess.run(["python3", f"{SKILL}/scripts/authorship.py", "check", "--source", "arabic", "--note", str(nid)],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2 and " ".join(parts[:-1]) == field:
            return parts[-1] == "owned"
    return False

def main(plan_path, apply=False):
    plan = json.load(open(plan_path))
    nids = sorted({u["nid"] for u in plan.get("field_updates", [])} | {t["nid"] for t in plan.get("tags", [])})
    info = {n["noteId"]: n for n in ac("notesInfo", notes=nids)} if nids else {}
    rollback = {"fields": {}, "tags": {}, "unsuspended": plan.get("unsuspend", [])}
    todo = []
    for u in plan.get("field_updates", []):
        n = info[u["nid"]]; cur = n["fields"][u["field"]]["value"]
        if u["mode"] == "fill_empty":
            if cur.strip():
                print("  skip (not empty):", u["nid"], u["field"]); continue
            new = u["value"]
        elif u["mode"] in ("append_owned", "append_missing"):
            # append only the lines not already there; the field must be pipeline-owned, or one THIS run
            # filled from empty (its pre-image in an earlier rollback file is "")
            prior = {}
            for rp in sorted(__import__("glob").glob(f"{BASE}/build/existing_rollback*.json")):
                prior.update(json.load(open(rp)).get("fields", {}).get(str(u["nid"]), {}))
            ours = owned(u["nid"], u["field"]) or (u["field"] in prior and prior[u["field"]].strip() == "")
            if cur.strip() and not ours:
                print("  skip (not ours to extend):", u["nid"], u["field"]); continue
            have_lines = set(cur.split("<br><br>"))
            add = [l for l in u["value"].split("<br><br>") if l and l not in have_lines]
            if not add: continue
            new = (cur + "<br><br>" if cur.strip() else "") + "<br><br>".join(add)
        else:
            raise ValueError(u["mode"])
        rollback["fields"].setdefault(str(u["nid"]), {})[u["field"]] = cur
        todo.append((u["nid"], u["field"], new))
    for t in plan.get("tags", []):
        rollback["tags"][str(t["nid"])] = info[t["nid"]]["tags"]
    print(f"field updates: {len(todo)} | tag sets: {len(plan.get('tags', []))} | unsuspend cards: {len(plan.get('unsuspend', []))}")
    if not apply:
        print("dry run — nothing written"); return
    rp = f"{BASE}/build/existing_rollback.json"
    if os.path.exists(rp):   # never overwrite an earlier pre-image: each pass gets its own file
        n = 2
        while os.path.exists(f"{BASE}/build/existing_rollback_{n}.json"): n += 1
        rp = f"{BASE}/build/existing_rollback_{n}.json"
    json.dump(rollback, open(rp, "w"), ensure_ascii=False, indent=0)
    # media first
    have = set(ac("getMediaFilesNames", pattern="arabic*"))
    import base64
    for name, src in plan.get("media", {}).items():
        if name in have: continue
        ac("storeMediaFile", filename=name, data=base64.b64encode(open(src, "rb").read()).decode())
    by_note = {}
    for nid, field, val in todo: by_note.setdefault(nid, {})[field] = val
    for nid, fields in by_note.items():
        ac("updateNoteFields", note={"id": nid, "fields": fields})
    for t in plan.get("tags", []):
        if t.get("add"): ac("addTags", notes=[t["nid"]], tags=" ".join(t["add"]))
    if plan.get("unsuspend"): ac("unsuspend", cards=plan["unsuspend"])
    print("applied; rollback at", rp)

if __name__ == "__main__":
    main(sys.argv[1], apply="--apply" in sys.argv)
