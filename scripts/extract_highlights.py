#!/usr/bin/env python3
"""
extract_highlights.py — Stage 1: pull the highlights Parker marked "card me" out of ANY
registered Zotero source, ground each one in its surrounding page paragraph, and emit
the JSON work-file the card-writer reads.

Which PDF, which highlight colors, and which page->segment map all come from the source
registry (reference/sources.json), so this one script serves the EMT textbook, an Arabic
textbook, a lecture PowerPoint, or anything else Parker registers.

Parker's color convention (normalized 2026-07-29): YELLOW = memorize this, everything
else (blue especially) = ordinary reading emphasis, deliberately ignored. Both palette
yellows are matched by default — #ffd400 is Zotero's own, #facd5a comes from externally
annotated PDFs — and a source may override `colors` when its book uses a different scheme.
PURPLE (`lexicon_colors`, default #a28ae5/#c885da) is the second lane: "define this word
for me" — emitted as `kind: "lexicon"` with a cleaned `term` + dedup `term_key`, and
carded per card-rules #28 / card-recipes §4b rather than the yellow contract.

READ-ONLY against Zotero: it copies the live DB and reads the copy in immutable mode; it
never touches the original DB or the PDF.

Usage:
    python3 extract_highlights.py --source emt --segment 6         # one chapter
    python3 extract_highlights.py --source emt --all               # every highlight
    python3 extract_highlights.py --source isaacs16                # a flat source, whole doc
    python3 extract_highlights.py --source arabic --pages 40-58    # an explicit page range
"""
import argparse, json, os, re, shutil, subprocess, sys, unicodedata

import sources as S
import lexicon as L

# Zotero annotation types. "Card me" is decided by COLOR, not by markup style: Parker
# HIGHLIGHTS in the EMT textbook but UNDERLINES on lecture slides, and both mean exactly
# the same thing to him. Reading only type=1 is why a lecture deck would come back empty
# (Isaacs Ch17: six yellow underlines, zero highlights).
#
# COLOR picks the LANE, type picks the treatment within it (2026-08-08):
#   yellow  -> the card lane ("this matters; make a card")
#   purple  -> the LEXICON lane ("I don't know this word; define it plainly") — his
#              habit is a purple UNDERLINE, which stacks cleanly under a yellow
#              highlight; a purple highlight means exactly the same thing.
# Purple is only defined for TEXT marks. A purple area-selection or standalone note has
# no agreed meaning yet, so it is EMITTED with kind "unsupported_purple" and surfaced at
# hand-off — never silently dropped (the no-silent-discard invariant).
TEXT_TYPES = (1, 5)    # highlight, underline -> a grounded span of source text
IMAGE_TYPES = (3,)     # area selection      -> a figure/diagram to crop and card
NOTE_TYPES = (6,)      # standalone note     -> Parker's own words, no source span
SKIP_TYPES = (2, 4)    # sticky note, ink    -> no cardable content
KIND = {**{t: "text" for t in TEXT_TYPES}, **{t: "image" for t in IMAGE_TYPES},
        **{t: "note" for t in NOTE_TYPES}}

CTX_CHARS = 450  # paragraph context grabbed on each side of the highlight
# A list lead-in (a highlight that introduces an enumerated list, e.g. "...consider the
# following factors:") needs MUCH more forward context, or the list gets cut off
# mid-enumeration and the card-writer completes it from memory (ungrounded) or
# undercounts. This bit EMT Ch3 card 4: the 450-char window caught only 4 of 8
# decision-making-capacity factors. When we detect a lead-in, grab the whole list.
LIST_FWD_CHARS = 1700
# A caption needs MORE forward reach than a list. Its body is a whole table, and the
# caption often sits at the TOP of a page — so the remainder of that page alone can eat a
# list-sized budget before the body is reached. EMT TABLE 4-7's caption is on p403 (1,704
# chars) and the "receiving facility / room number" row is on p404, which a 1,700-char
# window could never see. Sized to span the caption's page plus the next, which is the
# widest a single table runs in this book.
CAPTION_FWD_CHARS = 3800
LIST_LEADIN = re.compile(r"(:\s*$|\bfollowing\b|\binclude[sd]?\b|\bare[:]?\s*$|\bconsider\b)", re.I)
# A highlighted TABLE/FIGURE/BOX title is a POINTER, not content: the material Parker
# wants is the body, which sits below the caption or on the next page, and is often a
# rendered image with no text layer at all. Locating the caption tells you nothing about
# whether you have the body — that conflation is what let 31 title highlights across
# ch1-6 be handed to the card-writer with a context paragraph about something else
# entirely (EMT ch4 TABLE 4-4: grounding EXACT, context about not touching a patient's
# torso). These get the same next-page widening as a list lead-in, plus a content flag.
CAPTION_TITLE = re.compile(r"^\s*(TABLE|FIGURE|BOX|SKILL\s+DRILL|CHART|APPENDIX)\s+[\dA-Z][\d\-.]*\b", re.I)
# A page whose text layer is far thinner than this source's typical page is mostly image.
# Relative, not absolute, so it adapts on its own: a 2,000-char textbook page and a
# 300-char lecture slide are both "normal" for their own source.
SPARSE_PAGE_RATIO = 0.40


def norm(s):
    """Normalize text so a highlight (from the DB) and page text (from pdftotext) match."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("−", "-")
    s = s.replace("­", "")          # soft hyphen
    s = s.replace(" ", " ")         # nbsp
    s = re.sub(r"-\s*\n\s*", "", s)      # de-hyphenate across line breaks
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def norm_loose(s):
    s = norm(s).lower()
    return re.sub(r"\s*-\s*", "-", s)


# --- Column-aware page text -------------------------------------------------
# A TWO-COLUMN page read straight across interleaves the columns into prose that
# looks superficially fine and is actually nonsense:
#
#   "of how to survive. Instead spective on what the rest of this text will of
#    living for itself, however, each cell cooperates cover in detail..."
#
# That is fatal here rather than merely ugly: `context` is what Rule 1 grounds
# every card in, and what R13 tests each cloze answer against. Garbage context
# means either fabricated cards or a gate that blocks correct ones. `-layout`
# DOES preserve the gutter spatially — it is the later whitespace normalization
# that merges the columns — so the fix is to crop the columns apart before the
# text is ever joined.
#
# Opt-in per source (`text_columns`, `column_split_pts`). A source that does not
# set them takes the single-pass path and is byte-for-byte unaffected.
_COLUMNS = 1
_COLUMN_SPLIT = None      # x split in points; None = derive the page midpoint
_WIDTH_CACHE: dict = {}


def _page_width(pdf, p):
    """Page width in points, for deriving a midpoint split."""
    if pdf in _WIDTH_CACHE:
        return _WIDTH_CACHE[pdf]
    try:
        out = subprocess.run(["pdfinfo", "-f", str(p), "-l", str(p), pdf],
                             capture_output=True, text=True, timeout=30).stdout
        m = re.search(r"[Pp]age +\d+ +size: +([0-9.]+) +x", out) or \
            re.search(r"Page size: +([0-9.]+) +x", out)
        w = float(m.group(1)) if m else 0.0
    except Exception:
        w = 0.0
    _WIDTH_CACHE[pdf] = w
    return w


def page_text(pdf, page_label):
    """pdftotext -layout for a single physical page; column-aware when configured."""
    try:
        p = int(re.sub(r"[^0-9]", "", str(page_label)))
    except (TypeError, ValueError):
        return ""

    def run(*extra):
        out = subprocess.run(
            ["pdftotext", "-layout", "-f", str(p), "-l", str(p), *extra, pdf, "-"],
            capture_output=True, text=True, timeout=60,
        )
        return out.stdout

    if _COLUMNS < 2:
        return run()

    split = _COLUMN_SPLIT or (_page_width(pdf, p) / 2.0)
    if not split:
        return run()          # geometry unknown — degrade to the old behavior

    # This book's pages are MIXED: some paragraphs are two-column, others run the
    # full width. Cropping unconditionally at the gutter therefore truncates every
    # full-width line at the split — the first attempt at this dropped grounding
    # from 50/51 to 43/51. So emit all three readings and let locate_context pick
    # whichever one contains the highlight contiguously: the full-width pass keeps
    # the spanning paragraphs whole, and the two column passes keep the columnar
    # ones from interleaving. Redundancy is cheap; a lost paragraph is not.
    # ORDER MATTERS: locate_context takes the FIRST match, so the coherent column
    # readings must come before the full-width pass. With `full` first, a columnar
    # highlight still matched inside the interleaved text and carried the garbled
    # paragraph forward as its context — grounded by the counter, useless in fact.
    # Columns first means columnar text grounds from its own column; genuinely
    # full-width paragraphs miss in both column crops and fall through to `full`.
    left = run("-x", "0", "-y", "0", "-W", str(int(split)), "-H", "100000")
    right = run("-x", str(int(split)), "-y", "0", "-W", "100000", "-H", "100000")
    full = run()
    return left + "\n" + right + "\n" + full


def locate_context(hl_text, raw_page):
    """Find the highlight inside the page text and return the surrounding paragraph."""
    page_n = norm(raw_page)
    page_loose = norm_loose(raw_page)
    hl_loose = norm_loose(hl_text)
    idx = page_loose.find(hl_loose)
    status = "EXACT"
    if idx < 0:
        words = hl_loose.split()
        status = "PARTIAL"
        for take in (12, 10, 8, 6, 5, 4):
            if len(words) >= take and page_loose.find(" ".join(words[:take])) >= 0:
                idx = page_loose.find(" ".join(words[:take])); break
        else:
            if len(words) >= 6 and page_loose.find(" ".join(words[2:8])) >= 0:
                idx = page_loose.find(" ".join(words[2:8]))
            else:
                return "NOT_FOUND", ""
    # map back into the readable (non-loose) page via a short anchor
    anchor = " ".join(norm(hl_text).split()[:5])
    ni = page_n.lower().find(anchor.lower())
    if ni < 0:
        ni = max(0, int(idx * len(page_n) / max(1, len(page_loose))))
    hln = norm(hl_text)
    # A list lead-in gets a wide forward window so the WHOLE enumerated list is captured —
    # and so does a TABLE/FIGURE caption, for exactly the same reason: the thing being
    # pointed at is the body that follows, and a table's body is long.
    #
    # These two had drifted apart. `wants_next_page()` already treats a caption like a list
    # lead-in and fetches the following page, but this window did not — so the extra page
    # was fetched and then immediately discarded by a 450-character cut. EMT TABLE 4-3's
    # context stopped mid-table at "Reflection", four rows short of Empathy, Clarification,
    # Confrontation and Interpretation, and the four cards built from those rows were
    # HARD-blocked by R13 as ungrounded — while their text sat, verbatim, just past the cut.
    if is_caption_title(hl_text):
        fwd = CAPTION_FWD_CHARS
    elif LIST_LEADIN.search(hln):
        fwd = LIST_FWD_CHARS
    else:
        fwd = CTX_CHARS
    start = max(0, ni - CTX_CHARS)
    end = min(len(page_n), ni + len(hln) + fwd)
    if start > 0:
        start = page_n.find(" ", start) + 1
    if end < len(page_n):
        end = page_n.rfind(" ", 0, end)
    return status, page_n[start:end].strip()


def is_list_leadin(hl_text):
    return bool(LIST_LEADIN.search(norm(hl_text)))


def is_caption_title(hl_text):
    return bool(CAPTION_TITLE.match(norm(hl_text)))


def wants_next_page(hl_text):
    """Both list lead-ins and caption titles continue past their own page."""
    return is_list_leadin(hl_text) or is_caption_title(hl_text)


SKILL_DRILL_TITLE = re.compile(r"^\s*SKILL\s+DRILL\b", re.I)
STEP_HEAD_TXT = re.compile(r"\bStep\s+\d+\b", re.I)
SKILL_DRILL_MAX_PAGES = 12


def is_skill_drill(hl_text):
    """A SKILL DRILL is a procedure whose steps run ONE PER PAGE, not a one-page body.

    Every other caption's material sits on its own page or the next one, so a single
    look-ahead covers it. A drill does not: EMT Skill Drill 8-11 has three steps across
    three pages, and reading one next page returned 172 characters covering Steps 1 and 2
    — a card built from that would silently drop the last step of the procedure. Found
    2026-08-03 while preparing Chapter 8, whose drills are most of what Parker marked."""
    return bool(SKILL_DRILL_TITLE.match(norm(hl_text)))


def pages_forward(hl_text):
    """How many pages past the caption's own to append."""
    if is_skill_drill(hl_text):
        return SKILL_DRILL_MAX_PAGES
    return 1 if wants_next_page(hl_text) else 0


def clean_comment(c):
    """Parker's margin comments can carry HTML (he bolds/italicizes inside them) and
    non-breaking spaces. Flatten to plain text so the card-writer reads his intent, not
    markup."""
    if not c:
        return None
    c = re.sub(r"<br\s*/?>", "\n", c, flags=re.I)
    c = re.sub(r"<[^>]+>", "", c)
    c = c.replace("\xa0", " ")
    c = re.sub(r"\n{3,}", "\n\n", c)
    return c.strip() or None


def assert_pdf(path, source_id):
    """Zotero's contentType is not trustworthy: 'Isaacs Chapter 16.pptx' is registered as
    application/pdf but is really a zip. Poppler would emit garbage rather than fail, so
    check the magic bytes and stop with an actionable message instead."""
    try:
        with open(path, "rb") as f:
            magic = f.read(5)
    except OSError as e:
        sys.exit(f"ERROR: cannot read the file for source '{source_id}': {e}")
    if magic != b"%PDF-":
        kind = "a PowerPoint/zip file" if magic[:2] == b"PK" else f"magic {magic!r}"
        sys.exit(
            f"ERROR: the attachment for source '{source_id}' is not a PDF — it is {kind}:\n"
            f"  {path}\n"
            f"Zotero's stored contentType can be wrong. Text extraction needs a real PDF.\n"
            f"Fix: open the file, export/print it to PDF, attach THAT to the Zotero item, "
            f"re-highlight it, and point the source at the new attachment key.")


def parse_rects(position):
    """(pageIndex, [x1,y1,x2,y2]) for an area annotation, in PDF points (origin
    bottom-left). Zotero stores this as JSON: {"pageIndex":8,"rects":[[...]]}"""
    try:
        p = json.loads(position) if isinstance(position, str) else (position or {})
        rects = p.get("rects") or []
        if not rects:
            return p.get("pageIndex"), None
        xs0 = min(r[0] for r in rects); ys0 = min(r[1] for r in rects)
        xs1 = max(r[2] for r in rects); ys1 = max(r[3] for r in rects)
        return p.get("pageIndex"), [xs0, ys0, xs1, ys1]
    except (json.JSONDecodeError, TypeError, KeyError, IndexError, ValueError):
        return None, None


def work_path(source, label, kind):
    """work/<source>/<label>_<kind>.json — per-source subdirectories, so a growing
    library of books and lectures never collides in one flat folder."""
    d = os.path.join(S.SKILL, "work", source["id"])
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{label}_{kind}.json")


def main():
    ap = argparse.ArgumentParser(description="Extract 'card me' highlights from a registered Zotero source.")
    ap.add_argument("--source", required=True, help="source id from reference/sources.json (see: sources.py list)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--segment", type=int, help="segment number (chapter/unit/lesson) for a mapped source")
    g.add_argument("--pages", help="explicit physical page range, e.g. 515-680")
    g.add_argument("--all", action="store_true", help="every highlight in the document")
    ap.add_argument("--out", help="output JSON path (default: work/<source>/<label>_highlights.json)")
    args = ap.parse_args()

    src = S.get_source(args.source)
    item_id, pdf = S.resolve_attachment(src)
    if not os.path.exists(pdf):
        sys.exit(f"ERROR: the PDF for source '{src['id']}' is not on disk:\n  {pdf}\n"
                 f"(Is the attachment stored locally in Zotero, or is it a linked file?)")
    assert_pdf(pdf, src["id"])

    # Column layout is a property of the BOOK, so it rides the registry entry.
    # Absent = single column = the original code path, unchanged.
    global _COLUMNS, _COLUMN_SPLIT
    _COLUMNS = int(src.get("text_columns", 1) or 1)
    _COLUMN_SPLIT = src.get("column_split_pts") or None
    if _COLUMNS >= 2:
        print(f"  note: reading this source as {_COLUMNS} columns"
              f"{f' (split at {_COLUMN_SPLIT}pt)' if _COLUMN_SPLIT else ' (midpoint split)'}"
              f" — a two-column page read straight across interleaves the columns.")

    wanted = S.colors(src)
    lex_wanted = [c for c in S.lexicon_colors(src) if c not in wanted]
    noun = S.segment_noun(src)
    has_map = S.load_segments(src) is not None

    # ---- what page window are we pulling?
    lo = hi = None
    if args.segment is not None:
        lo, hi, seg_name = S.segment_range(src, args.segment)
        label = f"{noun.lower()}_{args.segment}"
        scope = f"{noun} {args.segment}" + (f" — {seg_name}" if seg_name else "") + f" (p{lo}-{hi})"
    elif args.pages:
        m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", args.pages)
        if not m:
            sys.exit("ERROR: --pages expects a range like 515-680")
        lo, hi = int(m.group(1)), int(m.group(2))
        label = f"p{lo}-{hi}"
        scope = f"pages {lo}-{hi}"
    else:
        if has_map and not args.all:
            sys.exit(f"ERROR: source '{src['id']}' is segmented into {noun.lower()}s. "
                     f"Pass --segment N, --pages A-B, or --all.")
        label = "all"
        scope = "the whole document"

    # ---- pull annotations (read-only copy of the DB)
    con, tmp = S._open_db()
    try:
        cur = con.cursor()
        types = TEXT_TYPES + IMAGE_TYPES + NOTE_TYPES
        all_colors = wanted + lex_wanted
        cur.execute(
            "SELECT pageLabel, position, text, comment, color, sortIndex, type "
            f"FROM itemAnnotations WHERE parentItemID=? "
            f"AND type IN ({','.join('?' * len(types))}) "
            f"AND color IN ({','.join('?' * len(all_colors))}) ORDER BY sortIndex",
            (item_id, *types, *all_colors))
        rows = cur.fetchall()
    finally:
        con.close()
        shutil.rmtree(tmp, ignore_errors=True)

    items, page_cache = [], {}
    for page_label, position, text, comment, color, sort, atype in rows:
        # Zotero's pageLabel is the PRINTED page number; position.pageIndex is the
        # 0-based PHYSICAL page. Everything in this pipeline speaks physical pages
        # (segment maps, pdftotext, render_page, the figure stages), so derive the
        # physical page from pageIndex and keep the label for display only. The EMT
        # book's zero offset made the two identical and hid this distinction; the
        # genetics book (printed = physical - 22) is what exposed it.
        pidx, _ = parse_rects(position)
        if pidx is not None:
            phys = int(pidx) + 1
        else:
            try:
                phys = int(re.sub(r"[^0-9]", "", str(page_label)))
            except (TypeError, ValueError):
                phys = None
        if lo is not None and (phys is None or not (lo <= phys <= hi)):
            continue

        kind = KIND.get(atype, "text")
        note = clean_comment(comment)
        is_lex = color in lex_wanted

        # Purple means "define this word" ONLY on a text mark (highlight/underline).
        # A purple area-selection or standalone note has no defined semantic yet, so
        # surface it verbatim for Parker rather than guessing — or dropping it silently.
        if is_lex and kind != "text":
            items.append({
                "source": src["id"], "kind": "unsupported_purple", "purple_kind": kind,
                "segment": S.segment_of_page(src, phys)[0],
                "segment_name": S.segment_of_page(src, phys)[1],
                "page": phys, "page_label": str(page_label), "color": color, "highlight": note or "",
                "context": "", "grounding": "UNSUPPORTED",
                "list_lead_in": False, "user_comment": note, "sort": sort,
            })
            continue

        # An AREA selection has no source text — the fact lives in the figure. Record the
        # crop box so render_page.py can cut it out, and let the card-writer author from
        # the image. This is Parker's "I want to memorize this diagram" case.
        if kind == "image":
            page_index, rect = parse_rects(position)
            items.append({
                "source": src["id"], "kind": "image",
                "segment": S.segment_of_page(src, phys)[0],
                "segment_name": S.segment_of_page(src, phys)[1],
                "page": phys, "page_label": str(page_label), "color": color, "highlight": "",
                "context": "", "grounding": "IMAGE",
                "crop": {"page_index": page_index, "rect": rect},
                "list_lead_in": False, "user_comment": note, "sort": sort,
            })
            continue

        # A standalone NOTE is Parker's own words with no underlying source span, so it
        # cannot be grounded the usual way. Surface it rather than card it blindly.
        if kind == "note":
            items.append({
                "source": src["id"], "kind": "note",
                "segment": S.segment_of_page(src, phys)[0],
                "segment_name": S.segment_of_page(src, phys)[1],
                "page": phys, "page_label": str(page_label), "color": color, "highlight": note or "",
                "context": "", "grounding": "NOTE",
                "list_lead_in": False, "user_comment": note, "sort": sort,
            })
            continue

        if phys not in page_cache:
            page_cache[phys] = page_text(pdf, phys)
        page_src = page_cache[phys]
        # A list lead-in whose enumeration spills onto the NEXT page would be truncated
        # if we only read one page, so append the next page. (This is the real cause of
        # the EMT Ch3 "7 vs 8 factors" bug.) A caption title gets the same treatment: a
        # table's body routinely starts on the following page — EMT TABLE 6-3's caption
        # is on p548 and its 1,293-character body is on p549, which was never fetched.
        next_chars = None
        # A purple mark is a WORD, never a list lead-in or a caption pointer, so it
        # takes the plain context window and no forward pages.
        want = 0 if is_lex else pages_forward(text)
        if want:
            try:
                base = phys
                added = 0
                for step in range(1, want + 1):
                    nxt = base + step
                    if nxt not in page_cache:
                        page_cache[nxt] = page_text(pdf, nxt)
                    body = page_cache[nxt]
                    # A drill walks forward only while pages keep carrying its steps, so
                    # it stops at the procedure's end rather than swallowing the next
                    # section. Every other caption takes exactly one page, as before.
                    if step > 1 and not STEP_HEAD_TXT.search(body or ""):
                        break
                    page_src = page_src + " " + body
                    added += len(body or "")
                next_chars = added
            except (TypeError, ValueError):
                pass

        status, ctx = locate_context(text, page_src)
        seg_n, seg_name = S.segment_of_page(src, phys)

        # ---- the LEXICON lane: a purple word -> a plain-language definition card.
        # The context is kept for the SENSE CHECK and the card's `Ex:` line, NOT as the
        # definition's grounding — by definition the word appears here *undefined*; its
        # anchor comes from lexicon.py --find (glossary / in_source / external).
        if is_lex:
            term = L.clean_term(text)
            words = term.split()
            # Hygiene flags, both surfaced at hand-off (integrity triage only — the
            # purple mark itself is never vetoed):
            #   multiword — >4 words is almost certainly a drag slip, not a term;
            #   midword   — an edge falls inside a word ("iaphoresis"), so the term is
            #               probably clipped; check the page before carding it.
            midword = False
            pn = norm(page_src)
            pos = pn.lower().find(norm(text).lower())
            if pos >= 0:
                before = pn[pos - 1: pos]
                after = pn[pos + len(norm(text)): pos + len(norm(text)) + 1]
                midword = bool((before.isalpha()) or (after.isalpha()))
            items.append({
                "source": src["id"], "kind": "lexicon",
                "segment": seg_n, "segment_name": seg_name,
                "page": phys, "page_label": str(page_label), "color": color,
                "highlight": norm(text), "context": ctx,
                "term_raw": norm(text), "term": term, "term_key": L.term_key(term),
                "flags": {"multiword": len(words) > 4, "midword": midword},
                "grounding": status, "content": "FULL",
                "page_text_chars": len(page_cache.get(phys, "")),
                "next_page_text_chars": None,
                "list_lead_in": False, "user_comment": note, "sort": sort,
            })
            continue

        items.append({
            "source": src["id"],
            "kind": "text",
            "segment": seg_n,
            "segment_name": seg_name,
            "page": phys,
            "page_label": str(page_label),
            "color": color,
            "highlight": norm(text),
            "context": ctx,
            # `grounding` answers ONE question: did I find your marked text? It does NOT
            # mean the material you were pointing at is present. `content` answers that
            # second question, and the card-writer must read BOTH — see below.
            "grounding": status,
            "content": "CAPTION_ONLY" if is_caption_title(text) else "FULL",
            "page_text_chars": len(page_cache.get(phys, "")),
            "next_page_text_chars": next_chars,
            # true = this highlight introduces an enumerated list; the writer/editor MUST
            # count the list against the full page (not just this context) and test every
            # item — this is where undercounting / ungrounded completion hides.
            "list_lead_in": is_list_leadin(text),
            "user_comment": note,
            "sort": sort,
        })

    # ---- sufficiency post-pass: which marks point at material we do NOT actually have?
    # Done after the loop because "sparse" is relative to THIS source's typical page. A
    # 2,000-char textbook page and a 300-char lecture slide are each normal for their own
    # document; only the ratio is meaningful.
    densities = sorted(v for v in (len(t) for t in page_cache.values()) if v > 0)
    median = densities[len(densities) // 2] if densities else 0
    floor = median * SPARSE_PAGE_RATIO
    for it in items:
        sparse = bool(median) and 0 <= it.get("page_text_chars", 0) < floor
        it["page_sparse"] = sparse
        if sparse and it.get("content") == "FULL":
            it["content"] = "SPARSE_PAGE"
        # needs_visual = "the text layer does not contain what this mark points at, so
        # render the page and READ it — and attach the crop as evidence you did."
        it["needs_visual"] = bool(
            it.get("kind") == "image"
            or it.get("content") in ("CAPTION_ONLY", "SPARSE_PAGE")
            or it.get("grounding") == "NOT_FOUND"
        )

    # Make a printed-vs-physical offset visible whenever one exists, so nobody ever
    # again reads "0 marked items" at face value on an offset book.
    offsets = set()
    for it in items:
        try:
            offsets.add(int(it["page"]) - int(re.sub(r"[^0-9]", "", it.get("page_label", ""))))
        except (TypeError, ValueError):
            pass
    if offsets - {0}:
        off = ", ".join(f"+{o}" if o > 0 else str(o) for o in sorted(offsets))
        print(f"  note: printed page labels differ from physical pages (offset {off}); "
              f"physical pages are used throughout, labels kept in page_label.")

    out = args.out or work_path(src, label, "highlights")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(items, f, indent=1, ensure_ascii=False)

    txt = [i for i in items if i["kind"] == "text"]
    imgs = [i for i in items if i["kind"] == "image"]
    notes = [i for i in items if i["kind"] == "note"]
    lex = [i for i in items if i["kind"] == "lexicon"]
    unsup = [i for i in items if i["kind"] == "unsupported_purple"]
    found = sum(1 for i in txt if i["grounding"] in ("EXACT", "PARTIAL"))
    exact = sum(1 for i in txt if i["grounding"] == "EXACT")
    missing = [i["page"] for i in txt if i["grounding"] == "NOT_FOUND"]
    comments = [i for i in items if i["user_comment"]]
    print(f"{src['label']}")
    print(f"  scope:  {scope}")
    print(f"  colors: {', '.join(wanted)}  |  lexicon (purple): {', '.join(lex_wanted) or '(none)'}")
    print(f"  {len(items)} marked item(s): {len(txt)} text, {len(imgs)} figure, "
          f"{len(notes)} standalone note, {len(lex)} lexicon (purple)")
    if txt:
        print(f"  text grounded {found}/{len(txt)} ({exact} EXACT)")
    if missing:
        print(f"  NOT located (handle manually / render the page): pages {missing}")
    needs_vis = [i for i in items if i.get("needs_visual")]
    if needs_vis:
        caps = [i for i in needs_vis if i.get("content") == "CAPTION_ONLY"]
        sparse = [i for i in needs_vis if i.get("content") == "SPARSE_PAGE"]
        print(f"  *** {len(needs_vis)} mark(s) NEED A VISUAL READ — the text layer does not")
        print(f"      contain what they point at. Render the page, read it, and attach the")
        print(f"      crop to the card ('image'/'visual_source'); check_cards.py HARD-blocks")
        print(f"      a card whose claims are unsupported by text AND carry no visual proof.")
        if caps:
            print(f"      {len(caps)} table/figure CAPTION (body is elsewhere): pages "
                  f"{[c['page'] for c in caps][:12]}")
        if sparse:
            print(f"      {len(sparse)} on an image-heavy page: pages "
                  f"{[c['page'] for c in sparse][:12]}")
        print(f"      python3 scripts/render_page.py --source {src['id']} <page>")
    if imgs:
        print(f"  {len(imgs)} figure selection(s) — crop each and author from the image:")
        for i in imgs:
            print(f"     p{i['page']}:  python3 scripts/render_page.py --source {src['id']} "
                  f"{i['page']} --crop-from work/{src['id']}/{label}_highlights.json")
    if notes:
        print(f"  {len(notes)} standalone note(s) — Parker's own words, NOT source text. "
              f"Ground them before carding, or flag needs_human_check:")
        for i in notes:
            print(f"     p{i['page']}: {i['highlight'][:90]}")
    if lex:
        junk = [i for i in lex if i["flags"]["multiword"] or i["flags"]["midword"]]
        print(f"  {len(lex)} lexicon mark(s) — purple = 'define this word plainly' (card-rules #28).")
        print(f"     Next: python3 scripts/lexicon.py --find {src['id']} --terms-from {out}")
        print(f"           python3 scripts/lexicon.py --dedup {out}    (Anki must be open)")
        for i in lex:
            fl = []
            if i["flags"]["multiword"]:
                fl.append("MULTIWORD — probable drag slip")
            if i["flags"]["midword"]:
                fl.append("MIDWORD — edge clips a word")
            print(f"     p{i['page']}: {i['term']}" + (f"   *** {'; '.join(fl)}" if fl else ""))
    if unsup:
        print(f"  *** {len(unsup)} PURPLE mark(s) of a kind with no defined meaning "
              f"(area selection / standalone note) — ask Parker what he wants; never guess:")
        for i in unsup:
            print(f"     p{i['page']}: purple {i['purple_kind']}")
    if comments:
        print(f"  {len(comments)} margin comment(s) — Parker talking to you. Obey them; answer any question at hand-off:")
        for c in comments:
            print(f"     p{c['page']}: {c['user_comment'][:100]}")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
