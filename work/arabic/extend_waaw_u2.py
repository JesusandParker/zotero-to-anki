#!/usr/bin/env python3
"""Unit 2 — extend the live waaw letter note with the connector fact from mark [13].

Playbook §2: letters in Units 2-10 EXTEND the existing note, never re-mint. The alif note
already carries this exact line (added 2026-09-04), so the two non-connectors stay parallel.
Only Text is written — it is `owned` in the authorship store; Back Extra is `edited`
(Parker's own work) and Audio is `unknown`, and neither is touched.

    python3 work/arabic/extend_waaw_u2.py            # dry run: guard verdict + diff
    python3 work/arabic/extend_waaw_u2.py --apply    # write, record authorship, re-read
"""
import json, os, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import authorship as A

EXT = os.path.join(HERE, "unit_2_waaw_ext.json")
RUN = open(os.path.join(HERE, "u2", "RUN_DIR")).read().strip()

def anki(action, **params):
    r = urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765",
        json.dumps({"action": action, "version": 6, "params": params}).encode()), timeout=30)
    out = json.load(r)
    if out.get("error"):
        raise SystemExit(f"AnkiConnect {action}: {out['error']}")
    return out["result"]

def main():
    apply = "--apply" in sys.argv
    card = json.load(open(EXT, encoding="utf-8"))[0]
    nid, new_text = card["extends_note_id"], card["Text"]
    if not os.path.exists(EXT + ".verified"):
        raise SystemExit("REFUSING: the extension file carries no .verified stamp — run check_cards.py first")
    live = anki("notesInfo", notes=[nid])[0]
    live_fields = {k: v["value"] for k, v in live["fields"].items()}
    old_text = live_fields["Text"]
    if not new_text.startswith(old_text):
        raise SystemExit("REFUSING: the new Text does not begin with the live Text verbatim — "
                         "an extension must only APPEND to the note")
    assert live_fields["Back Extra"] == card["Back Extra"], "Back Extra drifted since drafting — re-read the note"
    assert live_fields["Audio"] == card["Audio"], "Audio drifted since drafting — re-read the note"
    store = A.load("arabic")
    ok, report = A.guard("arabic", nid, live_fields, {"Text": new_text}, store=store)
    print("guard:", "ALLOW" if ok else "BLOCK"); print(report)
    print("\n--- appended ---")
    print(new_text[len(old_text):].replace("<br><br>", "\n"))
    if not ok:
        raise SystemExit("guard blocked the write — do not force it")
    if not apply:
        print("\n(dry run — pass --apply to write)"); return
    anki("updateNoteFields", note={"id": nid, "fields": {"Text": new_text}})
    A.record("arabic", nid, {"Text": new_text}, run=RUN, store=store)
    A.save("arabic", store)
    back = anki("notesInfo", notes=[nid])[0]["fields"]
    assert back["Text"]["value"] == new_text, "round-trip mismatch on Text"
    print("\nwrote + verified round-trip on note", nid)

main()
