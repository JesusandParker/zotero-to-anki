#!/usr/bin/env python3
"""Apply build/required_plan.json (from required_pivot.py) to Anki, 2026-09-30.

1. pre-image of every ARAB 101 card (suspended flag, queue, due, type) + note tags + the preset
   -> build/required_rollback.json, written BEFORE anything changes
2. suspend every card of the not-required notes, tag them ARAB101::parked-2026-09-30
3. ARAB101::required = exactly the kept notes (vocab + writing + numbers)
4. presets: "ARAB cram" (500/day, 1m step, bury off) becomes the long-term "ARAB 101" preset; a clone
   "ARAB 101 - quiz push (revert after 10/13)" carries the push (NEW_PER_DAY, max interval 3 days)
   and all five ARAB decks move onto it. A cram record with restore_after 2026-10-14 04:00 lets
   ~/bin/anki-autopilot move them back automatically (the stale-preset lesson of the 9/30 checkup).
usage: apply_required.py [--apply]
"""
import copy, json, os, sys, datetime, urllib.request

BASE = os.path.expanduser("~/arabic-catchup")
ROOT = "all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"
DECKS = [ROOT] + [f"{ROOT}::Unit {u:02d}" for u in (1, 2, 3, 4)]
NEW_PER_DAY = 64            # 248 new required cards / 4 days (Wed 9/30 - Sat 10/3) + slack for buried siblings
PUSH_MAX_IVL = 3            # every card comes back within 3 days until Test 1
PUSH_NAME = "ARAB 101 - quiz push (revert after 10/13)"
RECORD = os.path.expanduser("~/.anki-cram-suspend-20260930-arab-quiz-push.json")
PARK_TAG = "ARAB101::parked-2026-09-30"

def ac(action, **params):
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765", json.dumps({"action": action, "version": 6, "params": params}).encode()), timeout=300))
    if r.get("error"): raise RuntimeError(f"{action}: {r['error']}")
    return r["result"]

def settle(cfg, per_day, max_ivl, name):
    cfg["name"] = name
    cfg["new"]["perDay"] = per_day
    cfg["new"]["delays"] = [1.0, 10.0]          # his settled 1m/10m steps (2026-08-02)
    cfg["new"]["bury"] = True; cfg["rev"]["bury"] = True; cfg["buryInterdayLearning"] = True
    cfg["rev"]["maxIvl"] = max_ivl
    cfg["rev"]["perDay"] = 9999
    cfg["newGatherPriority"] = 3                # random notes, like Global (all) and Liberty
    cfg["newSortOrder"] = 4                     # random card, like Global (all)
    return cfg

def main(apply=False):
    plan = json.load(open(f"{BASE}/build/required_plan.json"))
    keep = [int(n) for n in plan["keep"]]
    park = [int(n) for n in plan["suspend"]]
    park_cards = [c for r in plan["suspend"].values() for c in r["cards"]]
    keep_cards = [c for r in plan["keep"].values() for c in r["cards"]]
    all_nids = ac("findNotes", query=f'"deck:{ROOT}"')
    assert sorted(all_nids) == sorted(keep + park), "deck changed since the plan was built; re-run required_pivot.py"
    cids = ac("findCards", query=f'"deck:{ROOT}"')
    info = ac("cardsInfo", cards=cids)
    susp = dict(zip(cids, ac("areSuspended", cards=cids)))
    notes = ac("notesInfo", notes=all_nids)
    old_cfg = ac("getDeckConfig", deck=ROOT)
    new_keep = sum(1 for c in info if c["cardId"] in set(keep_cards) and c["type"] == 0)
    print(f"keep {len(keep)} notes / {len(keep_cards)} cards ({new_keep} new) | park {len(park)} notes / {len(park_cards)} cards")
    print(f"preset now: {old_cfg['name']} (id {old_cfg['id']}) new/day {old_cfg['new']['perDay']} -> push {NEW_PER_DAY}/day, max ivl {PUSH_MAX_IVL}d")
    if not apply:
        print("dry run - nothing written"); return

    rb = {"at": datetime.datetime.now().isoformat(timespec="seconds"),
          "cards": {c["cardId"]: {"note": c["note"], "suspended": susp[c["cardId"]], "queue": c["queue"],
                                  "due": c["due"], "type": c["type"], "deck": c["deckName"]} for c in info},
          "tags": {n["noteId"]: n["tags"] for n in notes},
          "preset": old_cfg, "deck_preset": {d: ac("getDeckConfig", deck=d)["id"] for d in DECKS}}
    rp = f"{BASE}/build/required_rollback.json"
    assert not os.path.exists(rp), "rollback file exists - refusing to overwrite a pre-image"
    json.dump(rb, open(rp, "w"), ensure_ascii=False)

    for i in range(0, len(park_cards), 1000): ac("suspend", cards=park_cards[i:i + 1000])
    ac("unsuspend", cards=keep_cards)
    ac("removeTags", notes=all_nids, tags="ARAB101::required")
    ac("addTags", notes=keep, tags="ARAB101::required")
    ac("addTags", notes=park, tags=PARK_TAG)

    # long-term preset (the one the decks return to on 10/14) + the push clone they study on now
    long_cfg = settle(copy.deepcopy(old_cfg), 20, 36500, "ARAB 101")
    ac("saveDeckConfig", config=long_cfg)
    push_id = ac("cloneDeckConfigId", name=PUSH_NAME, cloneFrom=old_cfg["id"])
    ac("setDeckConfigId", decks=DECKS, configId=push_id)
    push_cfg = settle(ac("getDeckConfig", deck=ROOT), NEW_PER_DAY, PUSH_MAX_IVL, PUSH_NAME)
    ac("saveDeckConfig", config=push_cfg)

    rec = {"created": datetime.datetime.now().isoformat(timespec="seconds"),
           "purpose": "Parker 2026-09-30: ARAB 101 required-only push for the Tue 10/6 quizzes and Test 1 (~10/13). "
                      "No cards to restore (the not-required notes stay parked under tag " + PARK_TAG + " until he says "
                      "otherwise); this record only moves the five ARAB decks from the push preset back to 'ARAB 101'.",
           "keep_active": ROOT, "restore_after": "2026-10-14T04:00:00",
           "preset_restore": {d: {"before": old_cfg["id"], "during": push_id, "before_name": "ARAB 101",
                                  "during_name": PUSH_NAME} for d in DECKS},
           "groups": {}}
    json.dump(rec, open(RECORD, "w"), indent=1)
    print("applied; rollback at", rp, "| push preset id", push_id, "| auto-revert record", RECORD)

if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
