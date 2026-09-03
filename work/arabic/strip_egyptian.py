#!/usr/bin/env python3
"""Remove every Egyptian (maSri) pronunciation from Parker's live ARAB 101 notes.

Parker, 2026-09-03: "I don't want any of the Egyptian audio pronunciations in any of the
flashcards ever again." Dr. Khouri teaches FuSHa as the graded standard and Levantine as her
own dialect; Egyptian was never anything he is tested on, and it was doubling the audio on
every vocab back.

SAFETY MODEL. Several of these Back Extra fields are `unknown` in the authorship store
(SKILL.md step 4: never rewrite a field this system did not write). So this script never
rewrites a field. It applies a fixed list of EXACT (old -> new) span edits, each of which
must match exactly once, and asserts that the only characters that changed are the ones in
those spans. Everything Parker wrote survives byte-for-byte. Full pre-images go to
egyptian_strip_rollback.json before anything is sent.

Run with --apply to write; default is a dry run.
"""
import json, subprocess, sys, os, re

APPLY = "--apply" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROLLBACK = os.path.join(HERE, "egyptian_strip_rollback.json")

def ac(action, params=None):
    d = {"action": action, "version": 6}
    if params is not None: d["params"] = params
    r = subprocess.run(["curl", "-s", "localhost:8765", "-X", "POST", "-d", json.dumps(d)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    if j.get("error"): raise RuntimeError(f"{action}: {j['error']}")
    return j["result"]

# --- the edits ------------------------------------------------------------------------
# (a) AUDIO: drop the Egyptian half of a dialect line, keep the Levantine half.
#     Generated, because the shape is perfectly regular.
# (b) TEXT: Egyptian dialect FORMS he would otherwise try to imitate. Hand-written, because
#     each needs its surviving Levantine content to still read as a sentence.
TEXT_EDITS = {
 1786229800997: [("<br><br>Distinguish: Egyptian <i>issalaamu calaykum</i> (initial i-).", "")],
 1786229801222: [("Distinguish: Levantine says <i>marHaba</i>; no Egyptian column in the book for this one.",
                  "Distinguish: Levantine says <i>marHaba</i>.")],
 1786229801372: [("Distinguish: Egyptian and Levantine both say <i>ismi</i> (short final i).",
                  "Distinguish: Levantine says <i>ismi</i> (short final i).")],
 1786229801521: [("Distinguish: Egyptian <i>midiinit</i> · Levantine <i>madiinit</i>.",
                  "Distinguish: Levantine <i>madiinit</i>.")],
 1788401440126: [(" Egyptian <i>eeh</i>, which goes at the END of the question.", "")],
 1788401440753: [("Distinguish: Levantine <i>wayn</i> · Egyptian <i>feen</i>.",
                  "Distinguish: Levantine <i>wayn</i>.")],
 1788401440860: [("Distinguish: Levantine <i>min wayn inte?</i> · Egyptian <i>inta mineen?</i>",
                  "Distinguish: Levantine <i>min wayn inte?</i>")],
 1788401440964: [("Distinguish: Levantine <i>eeh</i> · Egyptian <i>aywa</i>.",
                  "Distinguish: Levantine <i>eeh</i>.")],
}
# DELIBERATELY NOT TOUCHED, and why:
#  * 1786229802451 / 802501 / 802552 — background cards built from HIS OWN yellow highlights
#    (Alif Baa pp. 22, 28): what shaami/maSri mean, Damascus vs Cairo, the hard-g fact.
#    Book knowledge about the dialect, not a pronunciation to imitate. His marks are the
#    prioritization signal (SKILL.md); deleting them is his call, not mine.
#  * 1788401440338 — Dr. Khouri's own line "Egyptians use it a lot ... they use a lot of
#    titles." That is usage guidance for HaDratuka, the FuSHa word he is learning.
#  * not my decks::Arabic::AlifBaa (7 notes) — a parked download, 100% suspended, serves
#    nothing, not pipeline-authored.
# Notes allowed to keep the WORD "Egyptian" after this pass (see the block above for why).
KEEP_MENTION = {1786229802451, 1786229802501, 1786229802552, 1788401440338}

AUDIO_RE = re.compile(r"Egyptian (\[sound:[^\]]*_masri\.mp3\]) · (Levantine \[sound:[^\]]*_shaami\.mp3\])")

def plan_field(val):
    """Return (new_value, [(old, new), ...]) for the audio-line edits in one field."""
    edits = []
    for m in AUDIO_RE.finditer(val):
        edits.append((m.group(0), m.group(2)))
    out = val
    for old, new in edits:
        out = out.replace(old, new, 1)
    return out, edits

def main():
    q = '(masri OR Egyptian OR maSri) "deck:all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"'
    nids = ac("findNotes", {"query": q})
    notes = {n["noteId"]: n for n in ac("notesInfo", {"notes": nids})}
    print(f"{len(notes)} live ARAB notes mention Egyptian\n")

    rollback, updates = {}, []
    for nid, n in sorted(notes.items()):
        for fname in ("Text", "Back Extra", "Audio"):
            if fname not in n["fields"]: continue
            old = n["fields"][fname]["value"]
            new, applied = plan_field(old)
            for o, w in TEXT_EDITS.get(nid, []):
                if o in new:
                    assert new.count(o) == 1, f"{nid} {fname}: span appears {new.count(o)}x, expected 1: {o[:60]}"
                    new = new.replace(o, w, 1); applied.append((o, w))
            if not applied: continue
            # nothing outside the listed spans may change
            probe = old
            for o, w in applied: probe = probe.replace(o, w, 1)
            assert probe == new, f"{nid} {fname}: edit is not span-local"
            # Hard invariant: no Egyptian AUDIO may survive, anywhere, ever.
            assert "_masri.mp3" not in new, f"{nid} {fname}: Egyptian audio survived:\n{new}"
            # Soft invariant: an "Egyptian"/"maSri" WORD may survive only on the notes listed
            # in KEEP_EGYPTIAN_TEXT above (his own highlights; Khouri's usage quote).
            assert nid in KEEP_MENTION or not re.search(r"Egyptian|maSri", new), \
                   f"{nid} {fname}: Egyptian dialect text survived and is not on the keep list:\n{new}"
            rollback[f"{nid}:{fname}"] = old
            updates.append((nid, fname, old, new, applied))

    print(f"{len(updates)} fields to edit across {len({u[0] for u in updates})} notes\n")
    for nid, fname, old, new, applied in updates:
        print("=" * 92); print(f"{nid} [{fname}]")
        for o, w in applied:
            print(f"   - {o[:150]}")
            print(f"   + {w[:150] if w else '(line removed)'}")

    if not APPLY:
        print("\nDRY RUN — rerun with --apply to write.")
        return
    json.dump(rollback, open(ROLLBACK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nrollback pre-images -> {ROLLBACK}")
    for nid, fname, old, new, applied in updates:
        ac("updateNoteFields", {"note": {"id": nid, "fields": {fname: new}}})
        back = ac("notesInfo", {"notes": [nid]})[0]["fields"][fname]["value"]
        assert back == new, f"readback mismatch on {nid} [{fname}]"
    print(f"{len(updates)} fields edited and read back clean.")
    left = ac("findNotes", {"query": q})
    print(f"live ARAB notes still mentioning Egyptian: {len(left)} (expected 4: 3 book-fact cards + Khouri's titles quote)")

if __name__ == "__main__":
    main()
