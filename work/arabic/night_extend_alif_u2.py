#!/usr/bin/env python3
"""Night unit 20260904-0840-1 — extend the live Unit 1 alif letter note with Unit 2's content.

Playbook §2 (arabic-unit-playbook.md): letters in Units 2-10 EXTEND the existing note, never
re-mint. Only the Text field is written (authorship: `owned`); Back Extra and Audio are
protected (`edited` / `unknown`) and are never touched. The guard is consulted BEFORE the
write and the fingerprint recorded AFTER it, exactly as fix_unit1_letters.py does.

    python3 work/arabic/night_extend_alif_u2.py            # dry run: guard verdict + diff
    python3 work/arabic/night_extend_alif_u2.py --apply    # write, record authorship, re-read
"""
import json, os, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import authorship as A

EXT = os.path.join(HERE, "night_20260904-0840-1_alif_ext.json")

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
    nid = card["extends_note_id"]
    new_text = card["Text"]
    stamp = EXT + ".verified"
    if not os.path.exists(stamp):
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
    print("guard:", "ALLOW" if ok else "BLOCK")
    print(report)
    print("\n--- appended lines ---")
    print(new_text[len(old_text):].replace("<br><br>", "\n"))
    if not ok:
        raise SystemExit("guard blocked the write — do not force it")
    if not apply:
        print("\n(dry run — pass --apply to write)")
        return
    anki("updateNoteFields", note={"id": nid, "fields": {"Text": new_text}})
    A.record("arabic", nid, {"Text": new_text}, run="runs/arabic/2/2026-09-04T09-03", store=store)
    A.save("arabic", store)
    back = anki("notesInfo", notes=[nid])[0]["fields"]
    assert back["Text"]["value"] == new_text, "round-trip mismatch on Text"
    assert back["Back Extra"]["value"] == live_fields["Back Extra"], "Back Extra changed — must not happen"
    assert back["Audio"]["value"] == live_fields["Audio"], "Audio changed — must not happen"
    cards = anki("cardsInfo", cards=anki("findCards", query=f"nid:{nid}"))
    print(f"\nwrote note {nid}; round-trip verified; authorship recorded for Text")
    print("cards on the note now:", [(c["ord"], c["deckName"]) for c in cards])

if __name__ == "__main__":
    main()
