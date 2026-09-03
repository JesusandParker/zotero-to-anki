#!/usr/bin/env python3
"""Write the Khouri Thursday (2026-09-03) vocab set into Anki.

Mirrors khouri_write.py (the Tuesday set): these notes come from a lecture recording, not
from Zotero marks, so they bypass anki_write.py's grounding gate on purpose. Form is gated
by check_block_spec.py BEFORE this runs, and by media_audit.py + render_check.py AFTER.

Steps (dry run by default; --apply writes):
  1. store every referenced media file, round-trip verified byte-for-byte (note-format.md)
  2. deck  …::Unit 2::Khouri Thursday 2026-09-03  on its OWN preset "Khouri Thursday cram"
     (cloned from the Liberty preset; new/day 40, new-sibling burying OFF so both directions
     of a note are served the same day). Clicking that deck directly serves the whole set
     today; from the root the Liberty 12/day cap still applies — which is why step 4 exists.
  3. add the notes (tags arabic-u2 + khouri-thu-2026-09-03)
  4. position the new cards at due 2028475… — directly behind the Tuesday set
     (2028451-2028474) and ahead of Book Highlights (2028554+), in her slide order.
Writes khouri_thursday_note_ids.json (rollback = delete those notes; nothing pre-existing
is modified).
"""
import json, subprocess, sys, os, hashlib, base64, re

APPLY = "--apply" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(HERE, "media")
CARDS = os.path.join(HERE, "khouri_thursday_cards.json")

ROOT = "all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"
DECK = f"{ROOT}::Unit 2::Khouri Thursday 2026-09-03"
MODEL = "AnKing Cloze"
TAGS = ["arabic-u2", "khouri-thu-2026-09-03"]
PRESET = "Khouri Thursday cram"
FIRST_DUE = 2028475          # Tuesday set ends at 2028474; Book Highlights starts 2028554

def ac(action, params=None):
    d = {"action": action, "version": 6}
    if params is not None: d["params"] = params
    r = subprocess.run(["curl", "-s", "localhost:8765", "-X", "POST", "-d", json.dumps(d)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    if j.get("error"): raise RuntimeError(f"{action}: {j['error']}")
    return j["result"]

cards = json.load(open(CARDS, encoding="utf-8"))

# ---- 1. media --------------------------------------------------------------
def sounds(t): return re.findall(r"\[sound:([^\]]+)\]", t or "")
clips = sorted({fn for c in cards for fn in sounds(c.get("Audio", "")) + sounds(c.get("Back Extra", ""))})
print(f"MEDIA — {len(clips)} clips referenced")
existing = set(ac("getMediaFilesNames", {"pattern": "arabic_*"}))
for fn in clips:
    p = os.path.join(MEDIA, fn)
    if not os.path.exists(p): raise SystemExit(f"missing clip: {p}")
    assert fn == fn.lower(), f"uppercase filename: {fn}"
    local = open(p, "rb").read()
    if fn in existing:
        got = base64.b64decode(ac("retrieveMediaFile", {"filename": fn}))
        same = hashlib.sha256(got).hexdigest() == hashlib.sha256(local).hexdigest()
        print(f"  already in collection: {fn} ({'identical' if same else 'DIFFERENT BYTES — never overwrite in place (R45); rename instead'})")
        if not same: raise SystemExit("stop")
        continue
    if not APPLY:
        print(f"  would store {fn} ({len(local)//1024} KB)"); continue
    returned = ac("storeMediaFile", {"filename": fn, "data": base64.b64encode(local).decode()})
    got = base64.b64decode(ac("retrieveMediaFile", {"filename": returned}))
    assert hashlib.sha256(got).hexdigest() == hashlib.sha256(local).hexdigest(), f"round-trip hash mismatch: {fn}"
    assert returned == fn, f"anki renamed {fn} -> {returned}"
    print(f"  stored+verified {returned} ({len(local)//1024} KB)")

# ---- 2. deck + preset ------------------------------------------------------
if APPLY:
    ac("createDeck", {"deck": DECK})
    lib = ac("getDeckConfig", {"deck": ROOT})
    # AnkiConnect has no "list presets" action: probe the deck we just made and clone if needed
    cur = ac("getDeckConfig", {"deck": DECK})
    if cur["name"] != PRESET:
        conf_id = ac("cloneDeckConfigId", {"name": PRESET, "cloneFrom": lib["id"]})
        conf = ac("getDeckConfig", {"deck": ROOT})           # fresh copy of Liberty as a template
        conf = {**conf, "id": conf_id, "name": PRESET}
        conf["new"] = {**conf["new"], "perDay": 40, "bury": False}
        ac("saveDeckConfig", {"config": conf})
        ac("setDeckConfigId", {"decks": [DECK], "configId": conf_id})
    got = ac("getDeckConfig", {"deck": DECK})
    print(f"DECK  {DECK}\n      preset '{got['name']}' new/day={got['new']['perDay']} bury-new={got['new']['bury']} rev/day={got['rev']['perDay']}")
else:
    print(f"DECK  would create {DECK} on preset '{PRESET}' (Liberty clone: new/day 40, bury-new off)")

# ---- 3. notes --------------------------------------------------------------
print(f"\nNOTES — {len(cards)}")
made = []
for c in cards:
    note = {"deckName": DECK, "modelName": MODEL,
            "fields": {"Text": c["Text"], "Back Extra": c["Back Extra"], "Audio": c.get("Audio", "")},
            "tags": TAGS, "options": {"allowDuplicate": False}}
    if not c["Text"].startswith("‎"):
        raise SystemExit(f"{c['slug']}: missing leading LRM (language.md 7a / U1-lrm)")
    if not APPLY:
        probe = {**note, "deckName": ROOT}     # the target deck does not exist until --apply
        err = ac("canAddNotesWithErrorDetail", {"notes": [probe]})[0]
        print(f"  {c['slug']:20s} canAdd={err['canAdd']} {err.get('error','')}")
        continue
    nid = ac("addNote", {"note": note})
    made.append(nid)
    print(f"  added {nid}  {c['slug']}")

# ---- 4. queue position -----------------------------------------------------
if APPLY:
    json.dump(made, open(os.path.join(HERE, "khouri_thursday_note_ids.json"), "w"))
    pos = FIRST_DUE; placed = []
    for nid in made:                      # slide order = note order; c1 then c2 within a note
        cids = ac("findCards", {"query": f"nid:{nid}"})
        info = sorted(ac("cardsInfo", {"cards": cids}), key=lambda x: x["ord"])
        for ci in info:
            ac("setSpecificValueOfCard", {"card": ci["cardId"], "keys": ["due"], "newValues": [pos], "warning_check": True})
            placed.append((ci["cardId"], pos)); pos += 1
    chk = ac("cardsInfo", {"cards": [c for c, _ in placed]})
    bad = [(c["cardId"], c["due"]) for c, (_, p) in zip(chk, placed) if c["due"] != p]
    assert not bad, f"due readback mismatch: {bad}"
    print(f"\nQUEUE  {len(placed)} cards placed at due {FIRST_DUE}..{pos-1} (readback verified)")
    print(f"wrote {len(made)} note ids -> khouri_thursday_note_ids.json")
else:
    print(f"\nQUEUE  would place {2*len(cards)} cards at due {FIRST_DUE}..{FIRST_DUE+2*len(cards)-1}")
    print("\nDRY RUN — rerun with --apply to write.")
