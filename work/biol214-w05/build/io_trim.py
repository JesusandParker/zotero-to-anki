#!/usr/bin/env python3
"""
io_trim.py — Parker, 2026-09-29: "find the image occlusion things I absolutely have to
memorize, add those, and then suspend the rest of the image occlusion" — the lab marks what
must be memorized with RED BOXES.

Red boxes exist on exactly three slides (checked three ways — overlay shapes in the .pptx,
red rectangles on the rendered slides, red rectangles baked into each embedded picture):
slide 12 cranial foramina (10), slide 14 typical vertebra (5), slide 18 sacrum/coccyx (10).
Each box already has its own IO card (foramina_red / typical_vertebra_red / sacrum_red), so
nothing had to be added.

KEEP   those 25, plus the same red-boxed foramina on the two skull-MODEL photos — slide 12's
       notes: "Look at these on a model—there could be a model on the practical" (12 cards).
SUSPEND every other IO card in the deck (the cloze cards are untouched). The exact ids go to
       io/io_trim_2026-09-29.json so the trim can be undone precisely.

Usage:  python3 io_trim.py [--dry-run]
"""
import datetime, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
AX = ("all::LIBERTY::LIBERTY FALL 2026::BIOL 214 - Human Anatomy & Physiology I Lab::"
      "Practical 2::Axial Skeleton")
REC = os.path.join(W, "io", "io_trim_2026-09-29.json")

RED_NOTES = {"foramina_red", "typical_vertebra_red", "sacrum_red"}     # every card kept
MODEL_KEEP = {                                                          # red-boxed foramina on models
    "cranial_floor_model": {"internal acoustic canal", "foramen magnum", "foramen rotundum",
                            "foramen lacerum", "foramen ovale", "foramen spinosum",
                            "jugular foramen", "hypoglossal canal"},
    "skull_inferior": {"foramen lacerum", "foramen ovale", "foramen spinosum", "foramen magnum"},
}


def ak(a, **p):
    r = json.loads(urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765", json.dumps({"action": a, "version": 6, "params": p}).encode(),
        {"Content-Type": "application/json"}), timeout=300).read())
    if r.get("error"):
        raise RuntimeError(f"{a}: {r['error']}")
    return r["result"]


def main():
    dry = "--dry-run" in sys.argv
    notes = {n["id"]: n for n in json.load(open(os.path.join(W, "io", "io_notes.json")))}
    nid = {w["id"]: w["noteId"] for w in json.load(open(os.path.join(W, "io", "io_written.json")))}
    keep, cut, why = [], [], {}
    for key, n in notes.items():
        label = {a["c"]: a["printed"][0] for a in n["answers"]}
        cards = ak("cardsInfo", cards=ak("findCards", query=f"nid:{nid[key]}"))
        assert len(cards) == n["cards"], (key, len(cards), n["cards"])
        for c in cards:
            k = c["ord"] + 1                                   # IO card ord 0 = {{c1::...}}
            name = label[k]
            if key in RED_NOTES or name in MODEL_KEEP.get(key, ()):
                keep.append(c["cardId"]); why[c["cardId"]] = f"{key} c{k} {name}"
            else:
                cut.append(c["cardId"])
    for key, want in MODEL_KEEP.items():                      # every named model label must exist
        have = {a["printed"][0] for a in notes[key]["answers"]}
        assert want <= have, (key, want - have)
    print(f"IO cards: keep {len(keep)}, suspend {len(cut)} (of {len(keep) + len(cut)})")
    for cid in keep:
        print("  keep", why[cid])
    if dry:
        print("[dry-run] nothing changed")
        return
    already = [c for c, s in zip(cut, ak("areSuspended", cards=cut)) if s]
    json.dump({"created": datetime.datetime.now().isoformat(timespec="seconds"),
               "why": "Parker 2026-09-29: keep only the red-boxed image occlusion (plus the same "
                      "red-boxed foramina on the skull-model photos); suspend the rest",
               "kept": {str(c): why[c] for c in keep},
               "suspended": sorted(set(cut) - set(already)),
               "already_suspended_before": already}, open(REC, "w"), indent=1)
    ak("suspend", cards=cut)
    # verify: exactly the kept IO cards are active, and the deck serves cloze + kept IO
    live = set(ak("findCards", query=f'"deck:{AX}" -is:suspended "note:Image Occlusion+"'))
    assert live == set(keep), (len(live), len(keep))
    cloze = ak("findCards", query=f'"deck:{AX}" -is:suspended -"note:Image Occlusion+"')
    names = sorted(d for d in ak("deckNames") if d == AX or d.startswith(AX + "::"))
    st = ak("getDeckStats", decks=["all"] + names)
    print(f"\nactive now: {len(cloze)} cloze + {len(live)} IO = {len(cloze) + len(live)}")
    for v in st.values():
        print(f"  serves {v['new_count']:>4} new  {v['name'].split('::')[-1]}")
    top = next(v for v in st.values() if v["name"] == "all")
    assert top["new_count"] == len(cloze) + len(live), top
    ak("sync")
    print(f"wrote {REC}; synced")


if __name__ == "__main__":
    main()
