#!/usr/bin/env python3
"""
detect_pending.py — "what has Parker marked that hasn't been carded yet?"

Stage 0 of the night shift. This is the script that decides what a nightly run WORKS ON,
and its whole design exists to make one specific failure impossible.

    On 2026-08-08 a run was pointed at a genetics chapter Parker had only partly
    highlighted. It read the chapter boundary as a job description, invented 99
    "coverage marks" for the parts he hadn't marked, and staged 79 cards he never
    asked for against 32 real ones. He retracted all 79.

    `check_cards.synthetic_marks_check` (R40) now hard-blocks a card citing a mark the
    extractor never produced. That is the backstop. THIS script is the fix: a run that
    is handed a list of marks and never told which chapter they came from has no
    "rest of the chapter" to fill in. The chapter is used only to name the deck, after
    the cards already exist.

So: the unit of work is A SET OF MARKS, never a chapter.

WHAT'S "PENDING"
    Every card-worthy mark in a registered source whose Zotero annotation key is not in
    `reference/processed-ledger.json`. That is deliberately NOT "marks added yesterday":

      - highlights made on the iPad that sync late are still caught whenever they land
      - a night that crashes loses nothing; tomorrow just finds a longer list
      - re-reading a chapter and adding six more marks queues six marks, not the chapter
      - a day with no reading produces an empty queue instead of an error

    The ledger advances ONLY after a confirmed Anki write (see mark_processed). If the
    write failed, the marks stay pending and come back tomorrow. Advancing it any
    earlier would silently delete a night's reading from the system's memory.

READ-ONLY against Zotero, same contract as extract_highlights.py: it copies the live DB
and reads the copy immutable, so it can run while Zotero is open and can never lock or
corrupt anything.

Usage:
    python3 scripts/detect_pending.py                  # the queue, human-readable
    python3 scripts/detect_pending.py --json           # same, for the scheduler
    python3 scripts/detect_pending.py --source emt     # one source only
    python3 scripts/detect_pending.py --cap 20         # smaller units (default 30)

    python3 scripts/detect_pending.py --baseline                    # "start from today"
    python3 scripts/detect_pending.py --baseline --before 2026-08-15

    python3 scripts/detect_pending.py --self-test
"""
import argparse, json, os, re, shutil, sys
from datetime import datetime, timezone

import sources as S

LEDGER = os.path.join(S.SKILL, "reference", "processed-ledger.json")

# Same lane rules as extract_highlights.py — color picks the lane, type picks the
# treatment within it. Kept in sync deliberately rather than imported, because importing
# extract_highlights drags in pdftotext and the whole grounding machinery for what is
# meant to be a cheap read.
TEXT_TYPES = (1, 5)     # highlight, underline
IMAGE_TYPES = (3,)      # area selection
NOTE_TYPES = (6,)       # standalone note
CARDABLE_TYPES = TEXT_TYPES + IMAGE_TYPES + NOTE_TYPES

DEFAULT_CAP = 30        # marks per unit; see build_units()


# --------------------------------------------------------------------------- ledger

def load_ledger():
    if not os.path.exists(LEDGER):
        return None
    with open(LEDGER) as f:
        return json.load(f)


def save_ledger(led):
    tmp = LEDGER + ".tmp"
    with open(tmp, "w") as f:
        json.dump(led, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, LEDGER)     # atomic: a killed run never leaves a half-written ledger


def new_ledger():
    return {
        "version": 1,
        "_comment": (
            "Zotero annotation keys whose cards have been CONFIRMED WRITTEN to Anki. "
            "detect_pending.py treats anything not in here as pending work. Only ever "
            "advanced after a successful write — see detect_pending.mark_processed. "
            "Advancing it before the write means a failed write silently erases that "
            "reading from the system forever."),
        "processed": {},
    }


def processed_keys(led=None):
    led = led if led is not None else load_ledger()
    return set((led or {}).get("processed", {}))


def mark_processed(keys, source_id, run_id, note="written"):
    """Record marks as done. Call this ONLY after Anki has confirmed the write.

    Importable by the writer stage; deliberately not exposed as a CLI flag, so nothing
    can advance the ledger by hand and desync it from what is actually in Anki.
    """
    led = load_ledger() or new_ledger()
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    for k in keys:
        led["processed"][k] = {"source": source_id, "run": run_id,
                               "at": stamp, "note": note}
    save_ledger(led)
    return len(keys)


# --------------------------------------------------------------------------- zotero

def registered_attachments():
    """{zotero attachment key: source_id} for every registered source.

    Sources are keyed by attachment_key rather than path because the key is stable and
    unambiguous across libraries — which is what lets Lydia's group-library books sit in
    the same registry as Parker's own without a second code path.
    """
    reg = S.load_registry()
    out, keyless = {}, []
    for sid in reg["sources"]:
        src = S.get_source(sid)
        key = src.get("attachment_key")
        if key:
            out[key] = sid
        else:
            keyless.append(sid)
    return out, keyless


def _phys_page(position, page_label):
    """Physical (1-based) PDF page, matching extract_highlights.py exactly.

    position.pageIndex is the 0-based PHYSICAL page; pageLabel is the PRINTED one. The
    whole pipeline speaks physical pages. The EMT book's zero offset made them identical
    and hid the distinction; genetics (printed = physical - 22) is what exposed it.
    """
    try:
        pidx = json.loads(position or "{}").get("pageIndex")
    except (ValueError, TypeError):
        pidx = None
    if pidx is not None:
        try:
            return int(pidx) + 1
        except (TypeError, ValueError):
            pass
    try:
        return int(re.sub(r"[^0-9]", "", str(page_label)))
    except (TypeError, ValueError):
        return None


def scan_marks():
    """Every cardable annotation in the library, tagged with its lane and source.

    Returns (marks, unregistered, keyless, external) where `unregistered` counts marks
    sitting on attachments no source claims. Those are REPORTED, never queued — most of
    the PDFs Parker marked in the last eight weeks are unregistered, and they include
    Fahrenheit 451, Mastery and Rich Dad Poor Dad. Leisure reading must not become
    flashcards.

    EXTERNAL MARKS ARE EXCLUDED BY DEFAULT, and this is load-bearing (measured
    2026-08-26). Zotero flags an annotation `isExternal=1` when it was baked into the
    PDF by whoever produced the file — a publisher, or a previous reader. In this
    library the split is total, with no overlap whatsoever:

        #ffd400  1213 marks   ALL isExternal=0   Parker's own
        #a28ae5    92 marks   ALL isExternal=0   Parker's own
        #facd5a  1059 marks   ALL isExternal=1   somebody else's
        #c885da     3 marks   ALL isExternal=1   somebody else's

    But #facd5a and #c885da are in the DEFAULT palette, on the old assumption that an
    externally-annotated PDF is one where Parker's marks land off-palette. The data says
    the reverse: off-palette colour has meant "not his mark" every single time. Register
    the Organic Chemistry textbook without this filter and the queue instantly fills
    with 1,054 highlights a stranger made — which is Rule 0 violated through the front
    door instead of by an agent inventing marks.

    A source can opt back in with `"include_external": true` in the registry, for the
    real case this was meant to cover: a PDF Parker annotated in another app and
    re-imported. Nothing is dropped silently either way — excluded marks are counted
    and reported.
    """
    att_map, keyless = registered_attachments()

    con, tmp = S._open_db()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT a.key, a.dateAdded, a.libraryID, pa.key, ia.pageLabel, ia.position, "
            "       ia.color, ia.type, ia.sortIndex, ia.isExternal, ia.comment "
            "FROM itemAnnotations ia "
            "JOIN items a  ON a.itemID  = ia.itemID "
            "JOIN items pa ON pa.itemID = ia.parentItemID "
            f"WHERE ia.type IN ({','.join('?' * len(CARDABLE_TYPES))}) "
            "  AND a.itemID NOT IN (SELECT itemID FROM deletedItems) "
            "ORDER BY pa.key, ia.sortIndex",
            CARDABLE_TYPES)
        rows = cur.fetchall()
        # Attachment filenames, for naming unregistered books in the report.
        cur.execute("SELECT i.key, ia.path FROM itemAttachments ia "
                    "JOIN items i ON i.itemID = ia.itemID")
        paths = {k: (p or "") for k, p in cur.fetchall()}
    finally:
        con.close()
        shutil.rmtree(tmp, ignore_errors=True)

    # Per-source palettes and shape, resolved once.
    palette, meta = {}, {}
    for akey, sid in att_map.items():
        src = S.get_source(sid)
        palette[akey] = (set(S.colors(src)), set(S.lexicon_colors(src)))
        meta[akey] = {"flat": S.load_segments(src) is None,
                      "include_external": bool(src.get("include_external", False))}
    default_pal = (set(S.colors({})), set(S.lexicon_colors({})))

    marks, unregistered, external = [], {}, {}
    for (key, date_added, lib, attach_key, page_label, position,
         color, atype, sort, is_external, comment) in rows:
        sid = att_map.get(attach_key)
        card_cols, lex_cols = palette.get(attach_key, default_pal)
        if color not in card_cols and color not in lex_cols:
            continue                      # blue and friends: ordinary reading emphasis

        if sid is None:
            name = re.sub(r"^storage:", "", paths.get(attach_key, "") or attach_key)
            u = unregistered.setdefault(attach_key,
                                        {"attachment_key": attach_key,
                                         "name": os.path.basename(name),
                                         "marks": 0, "external": 0})
            u["marks"] += 1
            u["external"] += 1 if is_external else 0
            continue

        if is_external and not meta[attach_key]["include_external"]:
            external[sid] = external.get(sid, 0) + 1
            continue

        lane = "define" if color in lex_cols else "card"
        # Purple is only defined on a TEXT mark. A purple area-selection or standalone
        # note has no agreed meaning, so it is surfaced rather than guessed at or
        # silently dropped (the no-silent-discard invariant, mirrored from the extractor).
        if lane == "define" and atype not in TEXT_TYPES:
            lane = "unsupported_purple"

        page = _phys_page(position, page_label)
        src = S.get_source(sid)
        seg, seg_name = (S.segment_of_page(src, page) if page is not None else (None, None))

        marks.append({
            "key": key, "source": sid, "attachment_key": attach_key,
            "library_id": lib, "date_added": date_added,
            "page": page, "page_label": str(page_label), "color": color,
            "type": atype, "lane": lane, "segment": seg, "segment_name": seg_name,
            "flat": meta[attach_key]["flat"], "sort": sort or "",
            "has_comment": bool((comment or "").strip()),
        })

    return (marks,
            sorted(unregistered.values(), key=lambda u: -u["marks"]),
            keyless,
            external)


# ---------------------------------------------------------------------------- units

def build_units(marks, cap=DEFAULT_CAP):
    """Group pending marks into the things a nightly session actually runs on.

    Two rules, in order:

    1. NEVER span a segment. The deck is per-segment (`sources.deck_name`), so marks
       from two chapters cannot share a unit — reading the end of ch. 7 and the start
       of ch. 8 in one sitting is two units, not one.
    2. Then split at `cap` marks. EMT ch. 8 was 32 marks and took 35 minutes of real
       wall clock; the cap is what keeps a heavy night (2026-08-11 was 115 marks across
       106 pages) from becoming one impossible run. It is also, not incidentally, what
       makes "the context window overflows" structurally impossible.

    A FLAT source (a lecture PDF, a paper — anything with no segment map) legitimately
    has segment=None, and its deck resolves without one. That is a normal unit, not a
    broken one. Only a SEGMENTED source with segment=None is a problem: the page didn't
    map to any chapter, and `deck_name` would produce "all::EMT::Chapter ::Book
    Highlights" — a real deck, silently wrong. Those are reported and never queued.
    """
    buckets = {}
    for m in marks:
        buckets.setdefault((m["source"], m["segment"]), []).append(m)

    units = []
    for (sid, seg), group in buckets.items():
        group.sort(key=lambda m: (m["page"] if m["page"] is not None else 10**9, m["sort"]))
        src = S.get_source(sid)
        flat = group[0].get("flat", False)

        # Does this source's deck template need a segment to resolve? If it does and we
        # haven't got one, the deck name comes out malformed, so the unit can't ship.
        template = src.get("deck") or src.get("promote") or "{root}::Book Highlights"
        needs_seg = "{segment}" in template or "{segment_name}" in template
        skip = None
        if seg is None and needs_seg:
            skip = ("registry: source is flat but its deck template wants a segment"
                    if flat else
                    "page did not map to any segment — check the mark, or the page map")

        for i in range(0, len(group), cap):
            chunk = group[i:i + cap]
            pages = [m["page"] for m in chunk if m["page"] is not None]
            lanes = {}
            for m in chunk:
                lanes[m["lane"]] = lanes.get(m["lane"], 0) + 1
            units.append({
                "source": sid,
                "source_label": src.get("label", sid),
                "owner": src.get("owner", "parker"),
                "delivery": (src.get("delivery") or {}).get("mode"),
                "segment": seg,
                "segment_noun": S.segment_noun(src),
                "segment_name": chunk[0].get("segment_name") or "",
                "flat": flat,
                "part": (i // cap) + 1,
                "parts": (len(group) + cap - 1) // cap,
                "marks": len(chunk),
                "lanes": lanes,
                "page_first": min(pages) if pages else None,
                "page_last": max(pages) if pages else None,
                "queueable": skip is None,
                "skip_reason": skip,
                # Newest mark's dateAdded — the orchestrator's "recent reading first"
                # ordering key, so tonight's chapter beats a three-week-old backlog.
                "newest_mark": max((str(m.get("date_added") or "") for m in chunk),
                                   default=""),
                "deck": None if skip else S.deck_name(src, seg),
                "tags": [] if skip else S.tags_for(src, seg),
                "keys": [m["key"] for m in chunk],
                "comments": sum(1 for m in chunk if m["has_comment"]),
            })

    units.sort(key=lambda u: (u["owner"] != "parker", u["source"],
                              u["segment"] if u["segment"] is not None else 10**9,
                              u["part"]))
    return units


# --------------------------------------------------------------------------- output

def _pages(u):
    if u["page_first"] is None:
        return "no page"
    if u["page_first"] == u["page_last"]:
        return f"p{u['page_first']}"
    return f"p{u['page_first']}-{u['page_last']}"


def _lanes(u):
    bits = []
    if u["lanes"].get("card"):
        bits.append(f"{u['lanes']['card']} to card")
    if u["lanes"].get("define"):
        bits.append(f"{u['lanes']['define']} to define")
    if u["lanes"].get("unsupported_purple"):
        bits.append(f"{u['lanes']['unsupported_purple']} purple-unsupported")
    return ", ".join(bits)


def _head(u):
    """The left-hand label for a unit: 'Chapter 6 [2/7]', or the source itself if flat."""
    part = f" [{u['part']}/{u['parts']}]" if u["parts"] > 1 else ""
    if u["segment"] is None:
        return ("  (whole document)" if u["flat"] else "  (unplaceable)") + part
    return f"  {u['segment_noun']} {u['segment']}{part}"


def render(units, unregistered, keyless, external, ledger_missing, total_pending):
    out = []
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    out.append(f"Night shift queue — {stamp}")
    out.append("")

    if ledger_missing:
        out.append("  NO LEDGER YET.")
        out.append("  Every mark in the library reads as pending, which is almost")
        out.append("  certainly wrong — most are already carded. Set the starting line:")
        out.append("")
        out.append("      python3 scripts/detect_pending.py --baseline")
        out.append("")
        out.append("  That records everything currently marked as done, so only marks")
        out.append("  made from now on are queued. To leave recent reading pending,")
        out.append("  baseline up to a date instead:")
        out.append("")
        out.append("      python3 scripts/detect_pending.py --baseline --before 2026-08-15")
        out.append("")
        out.append("  " + "-" * 66)
        out.append("")

    mine = [u for u in units if u["owner"] == "parker"]
    theirs = [u for u in units if u["owner"] != "parker"]

    runnable = [u for u in units if u["queueable"]]
    if not units:
        out.append("  Nothing pending. Every mark in every registered source is carded.")
    else:
        srcs = len({u["source"] for u in runnable})
        out.append(f"  {len(runnable)} unit(s) · {total_pending} mark(s) · {srcs} source(s)")
        out.append("")

    last = None
    for u in mine:
        if u["source"] != last:
            out.append(f"  {u['source_label']}")
            last = u["source"]
        out.append(f"  {_head(u):<26} {_pages(u):<14} {u['marks']:>3} marks  ({_lanes(u)})")
        if u["deck"]:
            out.append(f"  {'':<26} -> {u['deck']}")
        if u["comments"]:
            out.append(f"  {'':<26}    {u['comments']} carry a margin note — read them")
        if not u["queueable"]:
            out.append(f"  {'':<26}    NOT QUEUED: {u['skip_reason']}")
        out.append("")

    if theirs:
        out.append("  Not Parker's — has its own delivery, don't auto-run")
        for u in theirs:
            part = f" [{u['part']}/{u['parts']}]" if u["parts"] > 1 else ""
            label = f"{u['segment_noun']} {u['segment']}{part}" if u["segment"] is not None \
                else "(whole document)"
            out.append(f"    {u['source']:<18} {label:<18} {u['marks']:>3} marks  "
                       f"({u['delivery'] or 'manual'})")
            if not u["queueable"]:
                out.append(f"    {'':<18} {'':<18} NOT QUEUED: {u['skip_reason']}")
        out.append("")

    if external:
        out.append("  Excluded — already in the PDF when it arrived (isExternal), not his marks")
        for sid, n in sorted(external.items(), key=lambda kv: -kv[1]):
            out.append(f"    {n:>4} marks  {sid}")
        out.append('    Override per source with "include_external": true in sources.json')
        out.append("")

    if unregistered or keyless:
        out.append("  Skipped — not a registered source, so never carded")
        for u in unregistered:
            tail = f"   ({u['external']} of them external)" if u["external"] else ""
            out.append(f"    {u['marks']:>4} marks  {u['name'][:56]}{tail}")
        for sid in keyless:
            out.append(f"    (source '{sid}' has no attachment_key and cannot be scanned)")
        out.append("")
        out.append("    Register one with:  python3 scripts/add_source.py --search \"<title>\"")
        out.append("")

    return "\n".join(out)


# ------------------------------------------------------------------------ self-test

def self_test():
    """Cheap invariants. Run after touching this file; no Zotero needed."""
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {name}")
        ok = ok and bool(cond)

    def mk(src, seg, page, lane="card", key=None, flat=False):
        return {"key": key or f"K{page}{seg}{lane}", "source": src, "segment": seg,
                "segment_name": "", "page": page, "lane": lane, "sort": f"{page:05d}",
                "flat": flat, "has_comment": False}

    # A unit must never span two segments, however small each side is.
    u = build_units([mk("emt", 7, 200), mk("emt", 8, 300)], cap=30)
    check("segment boundary splits units", len(u) == 2)

    # The cap splits, and splitting preserves every mark exactly once.
    marks = [mk("emt", 7, 200 + i, key=f"K{i}") for i in range(70)]
    u = build_units(marks, cap=30)
    got = [k for unit in u for k in unit["keys"]]
    check("cap splits into 3 units", len(u) == 3)
    check("no mark lost or duplicated", sorted(got) == sorted(m["key"] for m in marks))
    check("no unit exceeds the cap", all(x["marks"] <= 30 for x in u))
    check("parts are numbered", [x["part"] for x in u] == [1, 2, 3])

    # Pageless marks bucket alone rather than joining a chapter, and don't ship:
    # emt's deck template needs {segment}, so a segment-less unit would resolve to
    # "all::EMT::Chapter ::Book Highlights" — a real deck, silently wrong.
    u = build_units([mk("emt", 7, 200), {**mk("emt", None, 0), "page": None}], cap=30)
    bad = [x for x in u if not x["queueable"]]
    check("unplaceable marks isolated", len(bad) == 1)
    check("unplaceable unit is blocked, not queued", bad and bad[0]["deck"] is None)
    check("placeable unit still ships", any(x["queueable"] and x["deck"] for x in u))

    # A FLAT source (isaacs17: a lecture PDF, no segment map) legitimately has
    # segment=None and its deck resolves without one. Regression: this was treated as
    # unplaceable and its six marks silently refused.
    u = build_units([mk("isaacs17", None, 3, flat=True),
                     mk("isaacs17", None, 5, flat=True, key="K2")], cap=30)
    check("flat source is queueable", len(u) == 1 and u[0]["queueable"])
    check("flat source resolves a deck", u[0]["deck"] and "Book Highlights" in u[0]["deck"])
    check("flat source keeps its pages", (u[0]["page_first"], u[0]["page_last"]) == (3, 5))

    # Physical page derivation matches the extractor's contract.
    check("pageIndex wins over label", _phys_page('{"pageIndex":230}', "209") == 231)
    check("label is the fallback", _phys_page(None, "p42") == 42)
    check("no page is None, not 0", _phys_page(None, None) is None)

    # The ledger must round-trip without disturbing an existing one.
    saved = load_ledger()
    try:
        led = new_ledger()
        led["processed"]["ZZTEST"] = {"source": "t", "run": "t", "at": "t", "note": "t"}
        save_ledger(led)
        check("ledger round-trips", "ZZTEST" in processed_keys())
    finally:
        if saved is None:
            os.path.exists(LEDGER) and os.remove(LEDGER)
        else:
            save_ledger(saved)
    check("ledger restored", load_ledger() == saved)

    print("\n  self-test:", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ------------------------------------------------------------------------------ cli

def main():
    ap = argparse.ArgumentParser(
        description="What has Parker marked that hasn't been turned into cards yet?")
    ap.add_argument("--source", help="restrict to one registered source id")
    ap.add_argument("--cap", type=int, default=DEFAULT_CAP,
                    help=f"max marks per unit (default {DEFAULT_CAP})")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--baseline", action="store_true",
                    help="record currently-pending marks as already done")
    ap.add_argument("--before", metavar="YYYY-MM-DD",
                    help="with --baseline, only baseline marks added before this date")
    ap.add_argument("--self-test", action="store_true", help="run invariants and exit")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())
    if args.before and not args.baseline:
        sys.exit("ERROR: --before only means something with --baseline.")

    led = load_ledger()
    ledger_missing = led is None
    done = processed_keys(led)

    marks, unregistered, keyless, external = scan_marks()
    pending = [m for m in marks if m["key"] not in done]
    if args.source:
        S.get_source(args.source)             # validates, exits with the known-ids list
        pending = [m for m in pending if m["source"] == args.source]

    if args.baseline:
        if args.before:
            try:
                datetime.strptime(args.before, "%Y-%m-%d")
            except ValueError:
                sys.exit(f"ERROR: --before wants YYYY-MM-DD, got {args.before!r}")
            chosen = [m for m in pending if str(m["date_added"])[:10] < args.before]
            scope = f"added before {args.before}"
        else:
            chosen = pending
            scope = "currently in the library"
        if not chosen:
            print(f"Nothing to baseline ({scope}). Ledger unchanged.")
            return
        led = led or new_ledger()
        stamp = datetime.now().astimezone().isoformat(timespec="seconds")
        for m in chosen:
            led["processed"][m["key"]] = {"source": m["source"], "run": "baseline",
                                          "at": stamp, "note": f"baseline: {scope}"}
        save_ledger(led)
        left = len(pending) - len(chosen)
        print(f"Baselined {len(chosen)} mark(s) {scope}.")
        print(f"{left} mark(s) remain pending." if left else "Queue is now empty.")
        print(f"Ledger: {LEDGER}")
        return

    units = build_units(pending, cap=args.cap)

    if args.json:
        print(json.dumps({
            "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
            "ledger": LEDGER,
            "ledger_missing": ledger_missing,
            "cap": args.cap,
            "pending_marks": len(pending),
            # The scheduler runs `units`; anything not queueable is in `blocked` with a
            # reason, so a broken unit is loud rather than absent.
            "units": [u for u in units if u["queueable"] and u["owner"] == "parker"],
            "blocked": [u for u in units if not u["queueable"]],
            "other_owners": [u for u in units if u["queueable"] and u["owner"] != "parker"],
            "external_excluded": external,
            "unregistered": unregistered,
            "sources_without_attachment_key": keyless,
        }, indent=1))
        return

    print(render(units, unregistered, keyless, external, ledger_missing, len(pending)))


if __name__ == "__main__":
    main()
