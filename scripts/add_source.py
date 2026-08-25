#!/usr/bin/env python3
"""
add_source.py — register a new Zotero item so Claude can make cards from it.

This is the front door for "I want cards from this book / lecture / paper." It does the
mechanical parts (find the item, inspect its highlights, dump its table of contents,
write the registry entry); Claude does the judgment parts (propose a deck path that fits
Parker's existing tree, read the TOC text into a segment map) and asks Parker to confirm
the deck ONCE. After that the source is permanent and never asks again.

Typical flow:

  1. Find it:            python3 add_source.py --search "Alif Baa"
  2. Look at the decks:  python3 add_source.py --decks all::Other
  3. (segmented book)    python3 add_source.py --toc-pages 7-11 --key HF2UEQIN
                         ...Claude reads that text and writes the map with --write-map
  4. Register it:        python3 add_source.py --add --id arabic --key HF2UEQIN \\
                             --label "Arabic — Alif Baa, 3e" --kind textbook \\
                             --deck-root "all::Other::languages::arabic" \\
                             --segment-noun Unit --profile language
  5. Confirm:            python3 sources.py show arabic

Nothing here writes to Zotero or Anki. It only reads Zotero (on a copy of the DB),
reads Anki's deck list, and edits reference/sources.json + reference/maps/.
"""
import argparse, json, os, re, shutil, subprocess, sys, urllib.request
from collections import Counter

import sources as S

ANKI = "http://localhost:8765"
# Same set the extractor treats as "card me": highlight, underline, area, note. Counting
# only type=1 here would report "0 highlights waiting" for a lecture deck Parker had
# fully underlined.
CARD_TYPES = (1, 5, 3, 6)
TYPE_NAME = {1: "highlight", 2: "sticky note", 3: "figure selection", 4: "ink",
             5: "underline", 6: "note"}


def anki(action, **params):
    req = urllib.request.Request(
        ANKI, data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    try:
        res = json.loads(urllib.request.urlopen(req, timeout=20).read())
    except Exception as e:
        sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI}. Is Anki open? ({e})")
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res["result"]


def cmd_search(words):
    """Find candidate attachments in Zotero, with their highlight colors, so Claude can
    pick the right item and see whether it is actually highlighted yet."""
    con, tmp = S._open_db()
    try:
        cur = con.cursor()
        like = f"%{words}%"
        cur.execute("""SELECT i.key, ia.itemID, ia.path, ia.contentType
                       FROM itemAttachments ia JOIN items i ON i.itemID = ia.itemID
                       WHERE ia.path LIKE ? ORDER BY ia.path""", (like,))
        rows = cur.fetchall()
        if not rows:
            print(f"No Zotero attachment matches {words!r}.")
            print("Try fewer words, or a distinctive part of the filename.")
            return
        print(f"{len(rows)} match(es) for {words!r}:\n")
        for key, item_id, path, ctype in rows:
            cur.execute(f"""SELECT color, type, COUNT(*) FROM itemAnnotations
                            WHERE parentItemID=? AND type IN ({','.join('?' * len(CARD_TYPES))})
                            GROUP BY color, type ORDER BY 3 DESC""", (item_id, *CARD_TYPES))
            colors = cur.fetchall()
            cur.execute("SELECT COUNT(*) FROM itemAnnotations WHERE parentItemID=? AND comment != ''",
                        (item_id,))
            ncomments = cur.fetchone()[0]
            name = (path or "").replace("storage:", "")
            print(f"  key={key}   {name}")
            print(f"      type={ctype}")
            if colors:
                print("      marked:")
                for c, t, n in colors:
                    flag = "   <- yellow = card me" if c in ("#ffd400", "#facd5a") else ""
                    print(f"        {c}  {TYPE_NAME.get(t, t):<17} x{n}{flag}")
            else:
                print(f"      marked: NOTHING yet — nothing to card until Parker marks it up")
            if ncomments:
                print(f"      margin comments: {ncomments}")
            print()
    finally:
        con.close(); shutil.rmtree(tmp, ignore_errors=True)


def cmd_decks(prefix):
    """Print Parker's live deck tree so a proposed deck path fits his conventions
    instead of inventing a new one."""
    names = sorted(anki("deckNames"))
    if prefix:
        names = [n for n in names if n.startswith(prefix)]
    print(f"{len(names)} deck(s)" + (f" under {prefix}" if prefix else "") + ":")
    for n in names:
        print("  ", n)


def cmd_toc(key, pages):
    """Dump the text of the book's PRINTED contents pages.

    Deliberately not an embedded-outline reader: most textbook PDFs Parker has are
    scanned or exported without a usable outline, but every one of them prints a table
    of contents. Claude reads this text and turns it into the segment map."""
    m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", pages)
    if not m:
        sys.exit("ERROR: --toc-pages expects a range like 7-11")
    lo, hi = int(m.group(1)), int(m.group(2))
    con, tmp = S._open_db()
    try:
        cur = con.cursor()
        cur.execute("""SELECT ia.path FROM itemAttachments ia JOIN items i ON i.itemID=ia.itemID
                       WHERE i.key=?""", (key,))
        row = cur.fetchone()
    finally:
        con.close(); shutil.rmtree(tmp, ignore_errors=True)
    if not row:
        sys.exit(f"ERROR: no Zotero attachment with key {key}")
    pdf = os.path.join(S.ZOTERO_STORAGE, key, (row[0] or "").replace("storage:", ""))
    if not os.path.exists(pdf):
        sys.exit(f"ERROR: PDF not on disk: {pdf}")
    out = subprocess.run(["pdftotext", "-layout", "-f", str(lo), "-l", str(hi), pdf, "-"],
                         capture_output=True, text=True, timeout=120)
    print(out.stdout)
    print(f"\n--- end of pages {lo}-{hi} ---", file=sys.stderr)
    print("Read the contents above, then write the segment map with:", file=sys.stderr)
    print("  python3 add_source.py --write-map <source-id> --noun Chapter  (JSON list on stdin)",
          file=sys.stderr)
    print("NOTE: map pages must be PHYSICAL PDF pages. If the printed page numbers differ "
          "from the PDF's, add the front-matter offset before writing.", file=sys.stderr)


def cmd_write_map(source_id, noun, offset):
    """Write reference/maps/<id>.json from a JSON list on stdin:
       [{"n":1,"name":"...","start":67,"end":129}, ...]"""
    try:
        segs = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: stdin is not valid JSON ({e}). Expected a list of "
                 f'{{"n":1,"name":"...","start":1,"end":20}} objects.')
    if not isinstance(segs, list) or not segs:
        sys.exit("ERROR: expected a non-empty JSON list of segments.")
    for s in segs:
        for f in ("n", "start", "end"):
            if f not in s:
                sys.exit(f"ERROR: segment missing '{f}': {s}")
        s["start"] += offset
        s["end"] += offset
    segs.sort(key=lambda s: s["n"])
    # sanity: overlapping or inverted ranges are a map-building mistake, not a book quirk
    for a, b in zip(segs, segs[1:]):
        if a["end"] >= b["start"]:
            print(f"  WARNING: {noun} {a['n']} ends p{a['end']} but {noun} {b['n']} "
                  f"starts p{b['start']} — overlapping ranges", file=sys.stderr)
    for s in segs:
        if s["end"] < s["start"]:
            sys.exit(f"ERROR: {noun} {s['n']} ends before it starts (p{s['start']}-{s['end']})")

    path = os.path.join(S.SKILL, "reference", "maps", f"{source_id}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"source": source_id, "noun": noun,
                   "note": "Page numbers are PHYSICAL PDF pages.",
                   "segments": segs}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {path}: {len(segs)} {noun.lower()}s, "
          f"{noun} {segs[0]['n']}-{segs[-1]['n']}, pages {segs[0]['start']}-{segs[-1]['end']}")
    print(f"Now point the source at it:  \"segments\": \"reference/maps/{source_id}.json\"")


def cmd_add(a):
    reg = S.load_registry()
    if a.id in reg["sources"] and not a.replace:
        sys.exit(f"ERROR: source '{a.id}' already exists. Pass --replace to overwrite it, "
                 f"or pick another id.")

    # verify the Zotero item resolves and is actually highlighted before committing
    con, tmp = S._open_db()
    try:
        cur = con.cursor()
        cur.execute("""SELECT ia.itemID, ia.path FROM itemAttachments ia
                       JOIN items i ON i.itemID=ia.itemID WHERE i.key=?""", (a.key,))
        row = cur.fetchone()
        if not row:
            sys.exit(f"ERROR: no Zotero attachment with key {a.key}. "
                     f"Find it with: add_source.py --search \"<words>\"")
        item_id, path = row
        colors = a.colors.split(",") if a.colors else reg["defaults"]["colors"]
        cur.execute(f"""SELECT type, COUNT(*) FROM itemAnnotations WHERE parentItemID=?
                        AND type IN ({','.join('?' * len(CARD_TYPES))})
                        AND color IN ({','.join('?' * len(colors))})
                        GROUP BY type ORDER BY 2 DESC""", (item_id, *CARD_TYPES, *colors))
        by_type = cur.fetchall()
        n_hl = sum(n for _t, n in by_type)
    finally:
        con.close(); shutil.rmtree(tmp, ignore_errors=True)

    entry = {
        "label": a.label,
        "attachment_key": a.key,
        "kind": a.kind,
        "segments": a.segments,
        "segment_noun": a.segment_noun,
        "deck_root": a.deck_root,
        "deck": a.deck or ("{root}::" + a.segment_noun + " {segment}::Book Highlights"
                           if a.segments else "{root}::Book Highlights"),
        "tags": [t for t in (a.tags.split(",") if a.tags else []) if t],
        "profile": a.profile,
    }
    if a.colors:
        entry["colors"] = a.colors.split(",")
    if a.notes:
        entry["notes"] = a.notes
    entry = {k: v for k, v in entry.items() if v not in (None, [], "")}

    reg["sources"][a.id] = entry
    S.save_registry(reg)

    print(f"registered source '{a.id}'")
    print(f"  {a.label}")
    print(f"  Zotero key {a.key}  ({os.path.basename((path or '').replace('storage:',''))})")
    print(f"  card-me colors: {', '.join(colors)}  ->  {n_hl} marked item(s) waiting")
    for t, n in by_type:
        print(f"      {TYPE_NAME.get(t, t)}: {n}")
    if n_hl == 0:
        print("  NOTE: nothing marked in these colors yet. Registering is still correct — "
              "Parker just hasn't marked it up, or this source uses different colors "
              "(check `add_source.py --search` output and set --colors).")
    src = S.get_source(a.id)
    print(f"  cards go to:  {S.deck_name(src, 1 if a.segments else None)}")
    print(f"  profile:      {os.path.basename(S.profile_path(src))}")
    print(f"\nNext: python3 extract_highlights.py --source {a.id}" +
          (" --segment 1" if a.segments else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--search", help="find Zotero attachments whose filename matches these words")
    ap.add_argument("--decks", nargs="?", const="", help="print Parker's live Anki deck tree (optionally filtered by prefix)")
    ap.add_argument("--toc-pages", help="dump the printed contents pages, e.g. 7-11 (needs --key)")
    ap.add_argument("--write-map", metavar="SOURCE_ID", help="write reference/maps/<id>.json from a JSON list on stdin")
    ap.add_argument("--noun", default="Chapter", help="segment noun for --write-map (Chapter/Unit/Lesson)")
    ap.add_argument("--offset", type=int, default=0,
                    help="add this to every start/end in --write-map (printed page -> physical PDF page)")

    ap.add_argument("--add", action="store_true", help="register the source")
    ap.add_argument("--id", help="short source id, e.g. arabic")
    ap.add_argument("--key", help="Zotero attachment key, e.g. HF2UEQIN")
    ap.add_argument("--label", help="human label shown in listings")
    ap.add_argument("--kind", default="textbook", help="textbook | lecture | article | reference")
    ap.add_argument("--deck-root", help="Anki deck root, e.g. all::Other::languages::arabic")
    ap.add_argument("--deck", help="deck template for this source's cards "
                    "(default derives from --deck-root, e.g. '{root}::Chapter {segment}::Book Highlights')")
    ap.add_argument("--segments", help="path to a segment map, e.g. reference/maps/arabic.json")
    ap.add_argument("--segment-noun", default="Chapter", help="Chapter | Unit | Lesson | Section")
    ap.add_argument("--tags", help="comma-separated tag templates, e.g. 'arabic,unit{segment}'")
    ap.add_argument("--profile", default="default", help="emt | language | science | default")
    ap.add_argument("--colors", help="comma-separated 'card me' colors (default: the registry's yellows)")
    ap.add_argument("--notes", help="a note stored with the source for future sessions")
    ap.add_argument("--replace", action="store_true", help="overwrite an existing source id")
    a = ap.parse_args()

    if a.search:
        return cmd_search(a.search)
    if a.decks is not None:
        return cmd_decks(a.decks)
    if a.toc_pages:
        if not a.key:
            sys.exit("ERROR: --toc-pages needs --key <ZoteroKey>")
        return cmd_toc(a.key, a.toc_pages)
    if a.write_map:
        return cmd_write_map(a.write_map, a.noun, a.offset)
    if a.add:
        missing = [f for f in ("id", "key", "label", "deck_root") if not getattr(a, f)]
        if missing:
            sys.exit("ERROR: --add requires " + ", ".join("--" + m.replace("_", "-") for m in missing))
        return cmd_add(a)
    ap.print_help()


if __name__ == "__main__":
    main()
