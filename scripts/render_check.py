#!/usr/bin/env python3
"""Render-review gate — LOOK at real cards the way Parker sees them, before hand-off.

Created 2026-08-08 (Arabic Unit 1). The run's root process failure: every check inspected
STORED FIELDS (notesInfo, checksums, stamps) and none inspected the RENDERED CARD. What
shipped as a result was invisible to every gate: whole-card RTL flips (R44 — direction is
decided by the card's first strong character), duplicate play buttons, lopsided crops.

This pulls real rendered card HTML from Anki, wraps it in the note type's actual CSS inside
a `dir="auto"` harness (the flip-inducing environment), rewrites media to file:// paths into
collection.media, screenshots each with headless Chrome, and tiles them into ONE contact
sheet. A human (or the session) must then LOOK at it — this script gets the pixels in front
of eyes; it does not replace them.

    python3 scripts/render_check.py --deck 'all::…::Unit 1::Book Highlights' \
        --cards work/arabic/unit_1_cards.json --model 'AnKing Cloze' \
        [--per-block 1] [--out /tmp/render_check.png]

Samples one note per `block` from the cards file (both card ordinals), matched to live notes
by normalized Text.
"""
import json, re, os, sys, glob, argparse, subprocess, urllib.request, collections

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def anki(action, **params):
    r = urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765",
        json.dumps({"action": action, "version": 6, "params": params}).encode()))
    out = json.load(r)
    if out.get("error"):
        raise SystemExit(f"AnkiConnect {action}: {out['error']}")
    return out["result"]

def norm(t):
    return re.sub(r"\s+|<br\s*/?>", "", t)[:80]

def media_dir():
    base = os.path.expanduser("~/Library/Application Support/Anki2")
    for d in os.listdir(base):
        p = os.path.join(base, d, "collection.media")
        if os.path.isdir(p):
            return p
    raise SystemExit("collection.media not found")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    ap.add_argument("--cards", required=True)
    ap.add_argument("--model", default="AnKing Cloze")
    ap.add_argument("--per-block", type=int, default=1)
    ap.add_argument("--out", default="/tmp/render_check.png")
    a = ap.parse_args()
    if not os.path.exists(CHROME):
        raise SystemExit("headless Chrome not found — render review must be done manually")

    cards = json.load(open(a.cards))
    css = anki("modelStyling", modelName=a.model)["css"]
    media = media_dir()

    nids = sorted(anki("findNotes", query=f'deck:"{a.deck}"'))
    live = {norm(n["fields"]["Text"]["value"]): n["noteId"]
            for n in anki("notesInfo", notes=nids)}

    picked = collections.defaultdict(list)
    for c in cards:
        b = c.get("block", "?")
        if len(picked[b]) < a.per_block and norm(c["Text"]) in live:
            picked[b].append(live[norm(c["Text"])])

    shots = []
    for block, ids in sorted(picked.items()):
        for nid in ids:
            for ci in anki("cardsInfo", cards=anki("findCards", query=f"nid:{nid}")):
                html = re.sub(r'src="([^"]+)"',
                              lambda m: (f'src="file://{media}/{m.group(1)}"'
                                         if not m.group(1).startswith(("http", "file", "_"))
                                         else m.group(0)),
                              ci["answer"])
                page = (f'<!doctype html><html><head><meta charset="utf-8">'
                        f"<style>{css}</style></head>"
                        f'<body class="card nightMode night_mode" style="background:#2f2f31" '
                        f'dir="auto"><div id="qa">{html}</div></body></html>')
                fn = f"/tmp/rc_{block}_{nid}_{ci['ord']}"
                open(fn + ".html", "w").write(page)
                subprocess.run([CHROME, "--headless", "--disable-gpu",
                                f"--screenshot={fn}.png", "--window-size=640,900",
                                "--hide-scrollbars", f"file://{fn}.html"],
                               capture_output=True)
                shots.append(fn + ".png")
    if not shots:
        raise SystemExit("no cards matched — check --cards / --deck")

    rows = []
    for i in range(0, len(shots), 3):
        row = f"/tmp/rc_row{i}.png"
        subprocess.run(["magick", *shots[i:i+3], "+append", row], check=True)
        rows.append(row)
    subprocess.run(["magick", *rows, "-append", "-resize", "1500x", a.out], check=True)
    print(f"{len(shots)} rendered cards -> {a.out}")
    print("NOW LOOK AT IT. The checklist: direction (no flipped colons/periods), ONE play "
          "button per clip, crops complete with even margins, no boilerplate, both cloze "
          "directions present where required.")

if __name__ == "__main__":
    main()
