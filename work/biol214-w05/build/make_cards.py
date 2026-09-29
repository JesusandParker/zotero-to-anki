#!/usr/bin/env python3
"""
make_cards.py — cards_src.NOTES -> pipeline card JSON (the shape check_cards.py and
anki_write.py consume), one file per subdeck plus cards_all.json for whole-batch checks.

Every card is on the AUTHORIZED lane (card-rules #29): there are no Zotero marks behind
this deck, so each card carries Parker's request, quoted, and the page it was read from.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cards_src  # noqa: E402

W = os.path.dirname(HERE)
FIG = os.path.join(W, "figures")

AUTH = {
    "by": "parker",
    "date": "2026-09-29",
    "asked": "(no question asked — his own request in chat, 2026-09-29, the whole W05 "
             "Axial Skeleton lab PowerPoint with nothing highlighted)",
    "quote": "turn my human anatomy lab PowerPoint over the axial skeleton into a fully "
             "functioning, perfectly well-made ANKI deck ... take each individual fact off of "
             "that PowerPoint turn that into its own individual flashcard and then attach an "
             "explanation and a picture ... let's just take all of the bones and memorize all "
             "of the parts",
    "scope": "every fact on the W05 Axial Skeleton slides and their speaker notes; the parts "
             "of every axial bone (lab manual Ch 6-7 figures and blue-page review questions, "
             "the Popcorn Points answer key)",
}

SLUG = {
    cards_src.BONE: "bone_basics",
    cards_src.SKULL: "skull_hyoid",
    cards_src.FORAMINA: "skull_foramina",
    cards_src.SPINE: "vertebral_column",
    cards_src.SACRUM: "sacrum_coccyx",
    cards_src.CAGE: "thoracic_cage",
}

PRONOUN_START = re.compile(r"(?:^|<br><br>)(?:Why|Cue|Pitfall|Mnemonic|Meaning|Ex|Distinguish|"
                           r"Parts):\s+(it|its|they|their|this|these|that)\b", re.I)


def notes():
    """The reviewed set if it exists (apply_review.py), else the raw draft."""
    rv = os.path.join(W, "cards_reviewed.json")
    return json.load(open(rv)) if os.path.exists(rv) else cards_src.NOTES


def media_name(fname):
    """The name anki_write stores a figure under — reused for inline back images."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", f"biol214-w05_{fname}").lower()


def main():
    by_deck, allc, problems = {}, [], []
    NOTES = notes()
    # A picture that IS a question (front) must not appear on any other card — reviewing
    # that card would teach the photo, and the question becomes recognition, not ID.
    fronts = {n["img"] for n in NOTES if n.get("side") == "front"}
    for i, n in enumerate(NOTES):
        for key in ("img", "back_img"):
            f = n.get(key)
            if f in fronts and not (key == "img" and n.get("side") == "front"):
                problems.append(f"note {i}: uses front-question image {f} as a {key}")
    front_users = {}
    for i, n in enumerate(NOTES):
        if n.get("side") == "front":
            front_users.setdefault(n["img"], []).append(i)
    for f, users in front_users.items():
        if len(users) > 1 and not all("pin " in NOTES[u]["text"] for u in users):
            problems.append(f"front image {f} is the question on several cards: {users}")
    for i, n in enumerate(NOTES):
        img = os.path.join(FIG, n["img"])
        if not os.path.exists(img):
            problems.append(f"note {i}: missing image {n['img']}")
        m = PRONOUN_START.search(n["back"])
        if m:
            problems.append(f"note {i}: Back Extra line opens with the pronoun {m.group(1)!r}: "
                            f"{n['back'][:70]}")
        back = n["back"]
        if n.get("back_img"):
            back = back + f'<br><br><img src="{media_name(n["back_img"])}">'
        card = {
            "Text": n["text"],
            "Back Extra": back,
            "source": "biol214-w05",
            "segment": None,
            "block": SLUG[n["deck"]],
            "deck": n["deck"],
            "from_idx": [],
            "authorization": AUTH,
            "verified_against": n["ver"],
            "verified_by": "claude — read directly off the slide/speaker notes/lab manual page named",
            "numeric": bool(n.get("num")),
            "needs_human_check": bool(n.get("num")),
            "image": img,
            "image_side": n.get("side", "back"),
            "draft_idx": n.get("draft_idx"),
            "back_img": n.get("back_img"),
        }
        by_deck.setdefault(n["deck"], []).append(card)
        allc.append(card)
    for deck, cards in by_deck.items():
        json.dump(cards, open(os.path.join(W, f"cards_{SLUG[deck]}.json"), "w"), indent=1,
                  ensure_ascii=False)
    json.dump(allc, open(os.path.join(W, "cards_all.json"), "w"), indent=1, ensure_ascii=False)
    for deck, cards in by_deck.items():
        print(f"{len(cards):3d}  {deck}")
    print(f"{len(allc):3d}  total")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  " + p)
        sys.exit(1)


if __name__ == "__main__":
    main()
