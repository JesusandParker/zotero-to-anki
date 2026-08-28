#!/usr/bin/env python3
"""Create the six new Khouri-list notes, store their audio, tag the whole Tuesday set.

These cards do NOT come from Zotero marks, so they deliberately do not go through
anki_write.py (whose grounding gate is keyed to extractor marks — inventing marks to
satisfy it is exactly what card-rules #29 / R40 forbid). Form is instead checked with
`check_cards.py --live` after the write, plus media_audit.py and render_check.py.

Every media store is round-trip verified before any note references it (note-format.md,
"Updating media that is already on live notes", rule 3).
Run with --apply to write; default is a dry run.
"""
import json, subprocess, sys, os, hashlib, base64

APPLY = "--apply" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(HERE, "media")
CARDS = os.path.join(HERE, "khouri_tuesday_cards.json")

ROOT = "all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"
DECK = f"{ROOT}::Unit 1::Khouri Tuesday 2026-09-01"
MODEL = "AnKing Cloze"
TAGS = ["arabic-u1", "khouri-tue-2026-09-01"]

# every note in the Tuesday set, new + already-existing, gets the batch tag
EXISTING = [1786229800997, 1786229801072, 1786229801147, 1786229801222, 1786229801295,
            1786229801372, 1786229801447, 1786229801521, 1786229801596]

def ac(action, params=None):
    d = {"action": action, "version": 6}
    if params: d["params"] = params
    r = subprocess.run(["curl", "-s", "localhost:8765", "-X", "POST", "-d", json.dumps(d)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    if j.get("error"): raise RuntimeError(f"{action}: {j['error']}")
    return j["result"]

cards = json.load(open(CARDS, encoding="utf-8"))

# ---- 1. media: store + round-trip verify -----------------------------------
import re as _re
def _sounds(t): return _re.findall(r"\[sound:([^\]]+)\]", t or "")
clips = []
for c in cards:
    clips += _sounds(c.get("Audio","")) + _sounds(c.get("Back Extra",""))
# clips referenced by the eight enriched existing notes
clips += [f"arabic_khouri_{s}.mp3" for s in
          ("salaam_alaykum", "ahlan", "ahla_wa_sahla", "ana",
           "ismi", "min", "ana_min_madiinat", "fii")]
clips = sorted(set(clips))

print(f"MEDIA — {len(clips)} clips")
for fn in clips:
    p = os.path.join(MEDIA, fn)
    if not os.path.exists(p): raise SystemExit(f"missing clip: {p}")
    assert fn == fn.lower(), f"uppercase filename: {fn}"
    local = open(p, "rb").read()
    if not APPLY:
        print(f"  would store {fn} ({len(local)//1024} KB)"); continue
    returned = ac("storeMediaFile", {"filename": fn,
                                     "data": base64.b64encode(local).decode()})
    # reference the RETURNED name, never the requested one (note-format.md rule 2)
    got = base64.b64decode(ac("retrieveMediaFile", {"filename": returned}))
    assert hashlib.sha256(got).hexdigest() == hashlib.sha256(local).hexdigest(), \
        f"round-trip hash mismatch: {fn}"
    assert returned == fn, f"anki renamed {fn} -> {returned}; update the note refs"
    print(f"  stored+verified {returned} ({len(local)//1024} KB)")

# ---- 2. deck ---------------------------------------------------------------
if APPLY:
    ac("createDeck", {"deck": DECK})
    try:  # carry the root preset so bury-siblings keeps the two-way halves apart
        conf = ac("getDeckConfig", {"deck": ROOT})
        ac("setDeckConfigId", {"decks": [DECK], "configId": conf["id"]})
        print(f"DECK  {DECK}\n      preset '{conf['name']}' copied from root")
    except Exception as e:
        print(f"DECK  {DECK}\n      preset copy skipped: {e}")
else:
    print(f"DECK  would create {DECK}")

# ---- 3. notes --------------------------------------------------------------
print(f"\nNOTES — {len(cards)}")
made = []
for c in cards:
    note = {"deckName": DECK, "modelName": MODEL,
            "fields": {"Text": c["Text"], "Back Extra": c["Back Extra"],
                       "Audio": c.get("Audio", "")},
            "tags": TAGS, "options": {"allowDuplicate": False}}
    if not c["Text"].startswith("‎"):
        raise SystemExit(f"{c['slug']}: missing leading LRM (language.md 7a / U1-lrm)")
    if not APPLY:
        err = ac("canAddNotesWithErrorDetail", {"notes": [note]})[0]
        print(f"  {c['slug']:20s} canAdd={err['canAdd']} {err.get('error','')}")
        continue
    nid = ac("addNote", {"note": note})
    made.append(nid)
    print(f"  added {nid}  {c['slug']}")

# ---- 4. tag the existing nine so the whole Tuesday set is one query ---------
if APPLY:
    ac("addTags", {"notes": EXISTING, "tags": "khouri-tue-2026-09-01"})
    print(f"\ntagged {len(EXISTING)} existing notes khouri-tue-2026-09-01")
    json.dump(made, open(os.path.join(HERE, "khouri_new_note_ids.json"), "w"))
    print(f"wrote {len(made)} new note ids")
else:
    print(f"\nwould tag {len(EXISTING)} existing notes khouri-tue-2026-09-01")
    print("\nDRY RUN — rerun with --apply to write.")
