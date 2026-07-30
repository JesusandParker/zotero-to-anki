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

# Zotero annotation types. "Card me" is decided by COLOR, not by markup style: Parker
# HIGHLIGHTS in the EMT textbook but UNDERLINES on lecture slides, and both mean exactly
# the same thing to him. Reading only type=1 is why a lecture deck would come back empty
# (Isaacs Ch17: six yellow underlines, zero highlights).
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


def page_text(pdf, page_label):
    """pdftotext -layout for a single physical page."""
    try:
        p = int(re.sub(r"[^0-9]", "", str(page_label)))
    except (TypeError, ValueError):
        return ""
    out = subprocess.run(
        ["pdftotext", "-layout", "-f", str(p), "-l", str(p), pdf, "-"],
        capture_output=True, text=True, timeout=60,
    )
    return out.stdout


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
    wanted = S.colors(src)
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
        cur.execute(
            "SELECT pageLabel, position, text, comment, color, sortIndex, type "
            f"FROM itemAnnotations WHERE parentItemID=? "
            f"AND type IN ({','.join('?' * len(types))}) "
            f"AND color IN ({','.join('?' * len(wanted))}) ORDER BY sortIndex",
            (item_id, *types, *wanted))
        rows = cur.fetchall()
    finally:
        con.close()
        shutil.rmtree(tmp, ignore_errors=True)

    items, page_cache = [], {}
    for page_label, position, text, comment, color, sort, atype in rows:
        try:
            pnum = int(re.sub(r"[^0-9]", "", str(page_label)))
        except (TypeError, ValueError):
            pnum = None
        if lo is not None and (pnum is None or not (lo <= pnum <= hi)):
            continue

        kind = KIND.get(atype, "text")
        note = clean_comment(comment)

        # An AREA selection has no source text — the fact lives in the figure. Record the
        # crop box so render_page.py can cut it out, and let the card-writer author from
        # the image. This is Parker's "I want to memorize this diagram" case.
        if kind == "image":
            page_index, rect = parse_rects(position)
            items.append({
                "source": src["id"], "kind": "image",
                "segment": S.segment_of_page(src, page_label)[0],
                "segment_name": S.segment_of_page(src, page_label)[1],
                "page": page_label, "color": color, "highlight": "",
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
                "segment": S.segment_of_page(src, page_label)[0],
                "segment_name": S.segment_of_page(src, page_label)[1],
                "page": page_label, "color": color, "highlight": note or "",
                "context": "", "grounding": "NOTE",
                "list_lead_in": False, "user_comment": note, "sort": sort,
            })
            continue

        if page_label not in page_cache:
            page_cache[page_label] = page_text(pdf, page_label)
        page_src = page_cache[page_label]
        # A list lead-in whose enumeration spills onto the NEXT page would be truncated
        # if we only read one page, so append the next page. (This is the real cause of
        # the EMT Ch3 "7 vs 8 factors" bug.) A caption title gets the same treatment: a
        # table's body routinely starts on the following page — EMT TABLE 6-3's caption
        # is on p548 and its 1,293-character body is on p549, which was never fetched.
        next_chars = None
        if wants_next_page(text):
            try:
                nxt = str(int(re.sub(r"[^0-9]", "", str(page_label))) + 1)
                if nxt not in page_cache:
                    page_cache[nxt] = page_text(pdf, nxt)
                page_src = page_src + " " + page_cache[nxt]
                next_chars = len(page_cache[nxt])
            except (TypeError, ValueError):
                pass

        status, ctx = locate_context(text, page_src)
        seg_n, seg_name = S.segment_of_page(src, page_label)
        items.append({
            "source": src["id"],
            "kind": "text",
            "segment": seg_n,
            "segment_name": seg_name,
            "page": page_label,
            "color": color,
            "highlight": norm(text),
            "context": ctx,
            # `grounding` answers ONE question: did I find your marked text? It does NOT
            # mean the material you were pointing at is present. `content` answers that
            # second question, and the card-writer must read BOTH — see below.
            "grounding": status,
            "content": "CAPTION_ONLY" if is_caption_title(text) else "FULL",
            "page_text_chars": len(page_cache.get(page_label, "")),
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

    out = args.out or work_path(src, label, "highlights")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(items, f, indent=1, ensure_ascii=False)

    txt = [i for i in items if i["kind"] == "text"]
    imgs = [i for i in items if i["kind"] == "image"]
    notes = [i for i in items if i["kind"] == "note"]
    found = sum(1 for i in txt if i["grounding"] in ("EXACT", "PARTIAL"))
    exact = sum(1 for i in txt if i["grounding"] == "EXACT")
    missing = [i["page"] for i in txt if i["grounding"] == "NOT_FOUND"]
    comments = [i for i in items if i["user_comment"]]
    print(f"{src['label']}")
    print(f"  scope:  {scope}")
    print(f"  colors: {', '.join(wanted)}")
    print(f"  {len(items)} marked item(s): {len(txt)} text, {len(imgs)} figure, {len(notes)} standalone note")
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
    if comments:
        print(f"  {len(comments)} margin comment(s) — Parker talking to you. Obey them; answer any question at hand-off:")
        for c in comments:
            print(f"     p{c['page']}: {c['user_comment'][:100]}")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
