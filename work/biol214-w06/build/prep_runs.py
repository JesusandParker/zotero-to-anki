#!/usr/bin/env python3
"""
prep_runs.py — one run-store record per subdeck file, so every cloze note anki_write
creates can be traced back (run_store.py trace <noteId>) to the slide/page it was read
from, the authorization it rests on, and the reviews it passed.

Prints `<cards file> <run dir>` pairs for the staging loop.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
SKILL = os.path.dirname(os.path.dirname(W))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import run_store as R  # noqa: E402

FILES = ["overview", "pectoral_girdle", "arm_forearm", "wrist_hand", "pelvic_girdle",
         "thigh_leg", "ankle_foot"]

for slug in FILES:
    path = os.path.join(W, f"cards_{slug}.json")
    cards = json.load(open(path))
    run = R.start_run("biol214-w06", slug,
                      note="Whole-deck build of the W06 Appendicular Skeleton lab at Parker's "
                           "request (authorized lane; no Zotero marks). Drafted from the "
                           "slides + speaker notes, the 9/30 lab recording, the Ch 8 study "
                           "guide, lab manual Ch 8 + blue pages, and the Popcorn pins; "
                           "independent card-craft review and anatomy fact-check applied "
                           "before staging.")
    R.snapshot(run, "cards.json", cards)
    for i, c in enumerate(cards):
        R.record(run, "provenance", {
            "card_index": i,
            "text_head": c["Text"][:90],
            "deck": c.get("deck"),
            "verified_against": c.get("verified_against"),
            "authorization": "parker 2026-09-30 (W06 maximal set, every source incl. the lab recording)",
            "stage": "drafted -> check_cards gate -> independent craft review -> "
                     "independent anatomy fact-check -> fixes applied",
            "image": os.path.basename(c.get("image") or "") or None,
            "image_side": c.get("image_side"),
        })
    print(path, run)
