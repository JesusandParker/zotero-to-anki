#!/usr/bin/env python3
"""
build_figure_index.py — inventory every figure in a registered source, once.

Textbook figures are not screenshots waiting to be taken: in a real publisher PDF each
plate is already a discrete embedded raster at its ORIGINAL resolution (the EMT skull
plate is 2133x1035, ~336 dpi). Rendering the page and cropping it throws that away. This
pulls the original asset out untouched.

For each figure it records:
  * the extracted image file (native resolution, no re-encode where possible)
  * its label ("FIGURE 6-6") and caption title
  * the publisher's accessibility LONG DESCRIPTION -- prose naming everything labeled in
    the plate. This is the key to matching a figure to a card without guessing: it turns
    "what is in this picture" into text you can actually test a card's answers against.

Usage
    python3 build_figure_index.py --source emt --segment 6
    python3 build_figure_index.py --source emt --pages 515-680
    python3 build_figure_index.py --source emt --segment 6 --rerender   # redo the files

Writes work/<source>/figures/*.png and work/<source>/figure_index.json.
Needs the skill venv (PyMuPDF):  .venv/bin/python scripts/build_figure_index.py ...
"""
import argparse, hashlib, json, os, re, subprocess, sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("ERROR: PyMuPDF is missing. Run this with the skill venv:\n"
             "  .venv/bin/python scripts/build_figure_index.py ...\n"
             "(create it once: python3 -m venv .venv && .venv/bin/pip install PyMuPDF)")

import sources as S

# A caption STARTS a block: "FIGURE 6-6  The skull." Body text that merely cross-references
# a figure ("FIGURE 6-15 and TABLE 6-3 show the major muscles...") matches this too, which
# is why a hit only counts as a caption once CREDIT_LINE corroborates it.
CAPTION = re.compile(r"^\s*(?:[◾■▪●]\s*)?(FIGURE|TABLE|BOX|SKILL\s+DRILL|CHART)"
                     r"\s+([\dA-Z][\d.]*(?:\s?[-.;–—]\s?[\dA-Z][\d.]*)*)", re.I)


def norm_fig_num(num):
    """Normalize a caption number's separator glyphs to a plain hyphen.

    Giancoli 7e sets its labels with an en dash ("FIGURE 1–1"), which PyMuPDF hands back
    as either "–" or ";" depending on the embedded font's glyph map — the same book yields
    "TABLE 1;4" and "TABLE 1–5" on one page — and its span layout puts SPACES around the
    glyph at block level ("FIGURE 1 ; 1"). Without normalization every such label
    truncated to its chapter digit ("FIGURE 1"), so all of a chapter's figures collided
    on one id. Trailing separators are stripped so a wrapped label can't leave one."""
    num = re.sub(r"\s*[;–—-]\s*", "-", num)
    return re.sub(r"\s+", "", num).strip("-.;–—")
# Some books (Snustad's genetics) prefix every true caption with a marker glyph and set
# the keyword in ALL CAPS ("◾ FIGURE 9.1 …"), while inline cross-references are Title
# Case inside parentheses ("(◾ Figure 9.1)"). Marker + caps is therefore as strong a
# corroboration as a credit line — and those line-art figures carry no credit at all.
CAPTION_MARKED = re.compile(r"^\s*[◾■▪●]\s*(?:FIGURE|TABLE|BOX|SKILL\s+DRILL|CHART)\b")
# A genuine caption is trailed by a rights line (and often an accessibility "Description"
# stub); that is what separates a caption from prose that merely opens with "FIGURE 4-9".
#
# The rights line is NOT always a copyright symbol. Illustration-heavy chapters use
# "© Jones & Bartlett Learning." (27 of 42 sampled), but PHOTO-heavy chapters credit the
# photographer instead -- "Courtesy of the Guide Dog Foundation for the Blind." -- and
# multi-panel photos lead with the panel letters, "A, C: © Photodisc; B: ...". Matching
# only on © silently lost EMT FIGURE 4-8 and 4-12, and would lose more of any chapter
# built on photographs rather than diagrams.
#
# Two tiers, because they need different guards. A block OPENING with © is a rights line
# no matter what follows it -- the extractor routinely welds the credit to the next
# paragraph (EMT p370 hands back a 643-char block that begins "© Jones & Bartlett
# Learning. 7. Always speak slowly..."), so length-capping this tier drops real figures.
CREDIT_STRICT = re.compile(r"^\s*(?:©|\(c\))", re.I)
# These could plausibly open a sentence of body prose, so they only count on a SHORT
# block -- a photo credit is a fragment, never a paragraph.
CREDIT_LOOSE = re.compile(
    r"^\s*(?:Courtesy\s+(?:of|from)\b"
    r"|Source\s*:"
    # one optional word between the head and its preposition: "Data adapted from ..."
    # (EMT TABLE 10-7's credit, missed 2026-08-29 — the caption was never corroborated,
    # so the table vanished from the index entirely)
    r"|(?:Reproduced|Adapted|Modified|Data)\s+(?:\w+\s+)?(?:from|with|by)\b"
    r"|Photograph(?:ed)?\s+by\b"
    # panel letters may carry periods: "A., B., C: © ..." (EMT FIGURE 10-23, same day)
    r"|[A-Z]\.?(?:\s*[,–-]\s*[A-Z]\.?)*\s*:\s*\S{0,3}\s*(?:©|\(c\)))", re.I)
CREDIT_MAX_CHARS = 200
DESC_STUB = "Description"
MIN_ART_PT = 40           # ignore rules, bullets, icons
STEP_HEAD = re.compile(r"^\s*Step\s+\d+\b", re.I)
SKILL_DRILL_MAX_PAGES = 12       # the longest drill in this book is well under this
CAPTION_GAP_PT = 60       # how far under the art a caption may sit
STOPWORDS = {
    "the", "and", "with", "from", "that", "this", "are", "for", "its", "into", "which",
    "illustration", "shows", "labeled", "view", "left", "right", "top", "bottom", "figure",
    "image", "side", "part", "parts", "above", "below", "between", "front", "back", "each",
}


def blocks(page):
    """Text blocks, top-to-bottom, as (text, bbox)."""
    out = []
    for b in sorted(page.get_text("dict")["blocks"], key=lambda b: b["bbox"][1]):
        if b.get("type") != 0:
            continue
        t = " ".join(s["text"] for l in b["lines"] for s in l["spans"]).strip()
        if t:
            out.append((t, b["bbox"]))
    return out


def art_on(page):
    """Raster art on a page, big enough to be a figure, with its placed bbox."""
    out = []
    for im in page.get_images(full=True):
        try:
            bb = page.get_image_bbox(im)
        except Exception:
            continue
        if bb.width < MIN_ART_PT or bb.height < MIN_ART_PT:
            continue
        out.append({"xref": im[0], "px": (im[2], im[3]), "bbox": tuple(bb)})
    return out


def is_credit(x):
    """Is this block a figure's rights line? (R15 — exercised by test_figures.py)"""
    if not x:
        return False
    return bool(CREDIT_STRICT.match(x)) or (
        len(x) <= CREDIT_MAX_CHARS and bool(CREDIT_LOOSE.match(x)))


def absorb_wrap_tails(bl, k, bottom, gap_pt=16, max_chars=100):
    """Extend a credit's bottom edge over its own wrapped tail blocks.

    A long credit line wraps, and the extractor sometimes splits the wrap into its own
    tiny block ("TX." under TABLE 10-6's credit; "Jones & Bartlett Learning; 2019:298-301."
    under TABLE 10-1's). Stopping at the matched block's bottom then ships a plate whose
    credit is cut mid-glyph — caught three times while hand-building Chapter 10's tables
    (2026-08-29). A tail block is absorbed when it starts within `gap_pt` of the current
    bottom and is short enough to be a fragment, never a paragraph. The publisher's
    accessibility "Description" stub also sits right under credits and is short — it is
    exactly the bleed this function must never ship, so it always stops the absorption.
    (R60 — exercised by test_figures.py)"""
    for t2, bb2 in bl[k + 1:]:
        ts = " ".join(t2.split())
        if ts == "Description":
            break
        if bb2[1] - bottom < gap_pt and len(ts) <= max_chars:
            bottom = bb2[3]
        else:
            break
    return bottom


def find_captions(page, next_page=None, caps_label=False):
    """Caption blocks on a page, corroborated by the trailing credit/Description stub.

    `caps_label` is the registry's `caption_style: "caps-label"` — for books that print NO
    per-figure credit line at all (Giancoli 7e collects photo credits in the back matter),
    an ALL-CAPS keyword opening the block is itself the caption typography: such books
    cross-reference in prose as "Fig. 1-8" / "Table 1-1", never block-initial caps, so the
    caps keyword cannot promote a cross-reference (R15 intact). Default off; the credit
    corroboration stays authoritative for every source that doesn't declare the style.

    `next_page` matters for TABLES. House style titles a table ABOVE its body, so a title
    landing near the foot of a page leaves its body — and therefore its credit line — on
    the following page. Looking for corroboration only on the caption's own page rejected
    the title before `pair_art` (which already handles the split) ever ran. That silently
    lost every one of EMT Chapter 5's twelve terminology tables: TABLE 5-1's title is the
    LAST block on p459, its 1060x1062 body sits at the top of p460, and the credit follows
    it there."""
    bl = blocks(page)
    nxt = blocks(next_page) if next_page is not None else []
    found = []
    for i, (t, bb) in enumerate(bl):
        m = CAPTION.match(t)
        if not m:
            continue
        # look ahead a few blocks for the credit line or the Description stub; a caption
        # may wrap onto a second block before the credit appears.
        tail = [x[0] for x in bl[i + 1:i + 5]]
        if len(bl) - i <= 2 and nxt:          # near the foot: the body ran onto the next page
            tail += [x[0] for x in nxt[:5]]
        corroborated = any(is_credit(x) or x == DESC_STUB for x in tail)
        # Marker-glyph + ALL-CAPS keyword is a caption by the book's own typography
        # (Snustad); inline references are Title Case, so they can never take this path.
        if not corroborated and CAPTION_MARKED.match(t):
            corroborated = True
        # Registry-declared caps-label typography (see docstring): the ALL-CAPS keyword
        # opening the block IS the caption, in books with no credit lines anywhere.
        if not corroborated and caps_label and m.group(1).isupper():
            corroborated = True
        # A block that IS the bare label ("TABLE 9.1") is a table header in books whose
        # tables carry no credit line (Snustad) — prose never opens a block with the bare
        # label and nothing else, so this cannot promote a cross-reference (R15 intact).
        if (not corroborated and m.group(1).isupper()
                and m.group(1).upper().startswith(("TABLE", "CHART"))
                and len(t.strip()) <= 16):
            corroborated = True
        # A SKILL DRILL banner carries no credit line — its body is a run of numbered step
        # panels, and the credit (if any) lands pages later. Its own corroboration is that
        # a `Step N` heading follows, which is exactly as strong a signal as a credit: body
        # prose that merely name-drops a drill is never followed by one. Without this, 10 of
        # EMT Chapter 8's 12 drills were rejected here before pair_art ever ran, including
        # all four Parker highlighted. Found 2026-08-03.
        if not corroborated and m.group(1).upper().startswith("SKILL"):
            corroborated = any(STEP_HEAD.match(x[0]) for x in (bl[i + 1:] + nxt))
        # A TABLE typeset as live TEXT fills its own page with row blocks, so its credit
        # line lands far past the 5-block window — EMT TABLE 7-2's caption is on p691 and
        # its credit is under the last row on p692. Widen the search for TABLE/CHART only,
        # and only for a block short enough to be a TITLE: that is what keeps body prose
        # opening "TABLE 6-3 and FIGURE 6-15 show the major muscles…" from qualifying,
        # which is the whole reason the credit requirement exists (R15).
        if (not corroborated and m.group(1).upper().startswith(("TABLE", "CHART"))
                and len(t) <= 140):
            corroborated = any(is_credit(x[0]) or x[0] == DESC_STUB
                               for x in (bl[i + 1:] + nxt[:12]))
        if not corroborated:
            continue
        title = t
        for cont, _ in bl[i + 1:i + 3]:         # stitch a wrapped caption line
            if is_credit(cont) or cont == DESC_STUB:
                break
            title += " " + cont
        found.append({
            "label": f"{m.group(1).upper().replace('  ', ' ')} {norm_fig_num(m.group(2))}",
            "title": re.sub(r"\s+", " ", title).strip(),
            "bbox": bb,
        })
    return found


def pair_art(doc, pno, cap):
    """The art a caption belongs to.

    House style splits by kind: a FIGURE is captioned UNDERNEATH its plate, a TABLE is
    titled ABOVE its body. Getting this backwards is why the image-only tables (EMT
    TABLE 6-9/6-10) look like they have no art at all.

    A **SKILL DRILL** is titled above its body exactly like a table — its header is a
    banner announcing the procedure, and the step panels follow it. Classifying it with
    FIGURE (caption-below) made the pairing search upward into the preceding prose and
    find nothing: on EMT Chapter 8 that lost **11 of 12 drills**, including all four
    Parker had highlighted. Found 2026-08-03 while preparing that chapter."""
    page = doc[pno - 1]
    cx0, cy0, cx1, cy1 = cap["bbox"]
    above = not cap["label"].startswith(("TABLE", "CHART", "SKILL"))
    best, bd = None, 1e9
    for a in art_on(page):
        ax0, ay0, ax1, ay1 = a["bbox"]
        gap = (cy0 - ay1) if above else (ay0 - cy1)
        if -5 <= gap <= CAPTION_GAP_PT and min(cx1, ax1) - max(cx0, ax0) > 0 and gap < bd:
            best, bd = a, gap
    if best:
        return best, pno
    # Margin-caption layouts (Snustad) put the caption beside its plate, outside the
    # vertical-gap window. When the page carries exactly ONE art object there is no
    # ambiguity about which plate the caption means — pair them. Multi-art pages keep
    # the strict geometry so a caption can never grab a neighbour's plate.
    solo = art_on(page)
    if len(solo) == 1:
        return solo[0], pno
    # A full-page plate pushes its caption onto the next page's top; a table titled at the
    # foot of a page has its body on the next.
    if above and cy0 < 140 and pno > 1:
        neigh, npno = doc[pno - 2], pno - 1
    elif not above and pno < doc.page_count:
        # A TABLE title with no body beneath it on this page has its body on the next one.
        # This used to require the title to sit in the bottom 140pt, which is wrong for a
        # reflowed PDF: EMT TABLE 5-1's title lands at y=324 on a 792pt page with nothing
        # after it but white space, and that geometry test lost all twelve of Chapter 5's
        # terminology tables. "No body under it here" is the actual condition — we only
        # reach this branch once the same-page search has already come up empty.
        neigh, npno = doc[pno], pno + 1
    else:
        return None, None
    cands = art_on(neigh)
    if cands:
        return max(cands, key=lambda a: a["bbox"][3] - a["bbox"][1]), npno
    return None, None


def skill_drill_pages(doc, cap_pno):
    """The pages carrying a Skill Drill's step panels.

    A Skill Drill is not one plate. In this reflowed PDF the procedure runs across
    several pages, **one numbered step per page** (photo, then "Step N", then the step's
    text). Pairing a single art object with the caption therefore yields one step and
    silently drops the rest — a card about a four-step carry would carry a picture of its
    first move.

    **Step 1 sits on the caption's OWN page as often as on the next one.** EMT Skill Drill
    8-9's banner ends its page with Step 1 overleaf, but 8-10, 8-11 and 8-12 all put Step 1
    directly under their banner — so starting the walk at cap_pno+1 lost the first step of
    three of the four drills Parker marked. The caption page is included only when it
    actually carries a step heading, and is returned separately so the render can be
    clipped to the banner rather than dragging in the section prose above it.

    A page belongs to the drill while it opens a `Step N` heading and has not started a
    NEW caption. That is the author's own marker, so it needs no geometry."""
    pages = []
    cap_texts = [t for t, _bb in blocks(doc[cap_pno - 1])]
    starts_on_caption_page = any(STEP_HEAD.match(t) for t in cap_texts)
    if starts_on_caption_page:
        pages.append(cap_pno)
    for p in range(cap_pno + 1, min(cap_pno + 1 + SKILL_DRILL_MAX_PAGES, doc.page_count + 1)):
        texts = [t for t, _bb in blocks(doc[p - 1])]
        if any(CAPTION.match(t) for t in texts):
            break
        if not any(STEP_HEAD.match(t) for t in texts):
            break
        pages.append(p)
    return pages


def skill_drill_composite(doc, cap_pno, out_png, dpi=150, cols=2, cap_bbox=None):
    """Render a Skill Drill's steps into ONE plate showing the whole procedure.

    Each step page is rendered, trimmed to its own content box (these pages are mostly
    white below the panel), and tiled in reading order. The result is what belongs on the
    back of a card about the procedure: the steps in order, in the book's own photographs
    — the same part-and-whole design Parker asked for with tables."""
    step_pages = skill_drill_pages(doc, cap_pno)
    if not step_pages:
        return None, []
    try:
        from PIL import Image
    except ImportError:
        return None, []
    tiles = []
    for p in step_pages:
        # On the caption's own page, clip to the banner downward — everything above it is
        # the section's body prose, not part of the procedure.
        clip = None
        if p == cap_pno and cap_bbox:
            pr = doc[p - 1].rect
            clip = fitz.Rect(pr.x0, max(pr.y0, cap_bbox[1] - 4), pr.x1, pr.y1)
        pix = doc[p - 1].get_pixmap(dpi=dpi, clip=clip)
        tmp = os.path.splitext(out_png)[0] + f"_p{p}.png"
        pix.save(tmp)
        im = Image.open(tmp).convert("RGB")
        # Trim against the tile's OWN corner colour, not against white. A step panel sits
        # on a cream background that runs to the foot of the page, so a white-threshold
        # trim keeps a screenful of empty cream under every step.
        from PIL import ImageChops
        bg = Image.new("RGB", im.size, im.getpixel((1, 1)))
        bbox = ImageChops.difference(im, bg).convert("L").point(
            lambda v: 255 if v > 18 else 0).getbbox()
        if bbox:
            pad = 10
            im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                          min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)))
        tiles.append(im)
        os.remove(tmp)
    if not tiles:
        return None, []
    cols = 1 if len(tiles) == 1 else cols
    rows = (len(tiles) + cols - 1) // cols
    cw = max(t.width for t in tiles)
    rh = [max(t.height for t in tiles[r * cols:(r + 1) * cols]) for r in range(rows)]
    gap = max(12, cw // 60)
    W = cols * cw + (cols + 1) * gap
    H = sum(rh) + (rows + 1) * gap
    from PIL import Image as _I
    sheet = _I.new("RGB", (W, H), "white")
    y = gap
    for r in range(rows):
        x = gap
        for t in tiles[r * cols:(r + 1) * cols]:
            sheet.paste(t, (x + (cw - t.width) // 2, y))
            x += cw + gap
        y += rh[r] + gap
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    sheet.save(out_png)
    return out_png, step_pages


TABLE_MAX_PAGES = 4


def text_table_render(doc, cap_pno, cap_bbox, out_png, dpi=150):
    """Render a TABLE that is live TEXT rather than an embedded raster.

    Not every table in a publisher PDF is a picture. EMT's TABLE 7-2, 8-1, 8-3 and 6-11 are
    typeset text with coloured row bands, so `pair_art` correctly finds no art and the
    caption is recorded as "no locatable art" — which is honest but leaves the pipeline
    with nothing to attach. That matters because Parker's rule-25 design puts the SOURCE
    TABLE on the back of every per-key card: TABLE 7-2 is live on 11 of his cards.

    Rendering the caption's own page region is the right answer for this class, and it is
    what a human would do. The table's end is marked by its credit line (`is_credit`), the
    same signal `find_captions` already trusts; if the credit does not appear before the
    page ends, the body continues onto the next page and is followed there.

    Written 2026-08-03 after the TABLE 7-2 plate was produced by a throwaway script and was
    therefore not reproducible from the repo — a plate 11 live cards depended on."""
    try:
        from PIL import Image
    except ImportError:
        return None, []
    regions, pages = [], []
    y_from = cap_bbox[1] - 4
    for step in range(TABLE_MAX_PAGES):
        p = cap_pno + step
        if p > doc.page_count:
            break
        page = doc[p - 1]
        bl = blocks(page)
        stop_at = None
        if step > 0:
            y_from = page.rect.y0
            # A new caption bounds the table from BELOW — the body's last rows and its
            # credit line still sit ABOVE it on this page, so render down to the caption
            # rather than abandoning the page. EMT TABLE 8-3's last two situations and its
            # credit sit above the Skill Drill 8-7 banner on p804; breaking here first
            # produced a plate showing four of its six situations (2026-08-03).
            caps = [bb[1] for t, bb in bl if CAPTION.match(t)]
            if caps:
                stop_at = min(caps) - 4
                if stop_at <= y_from + 8:
                    break                      # the caption opens the page: nothing to take
        y_to, done = (stop_at if stop_at is not None else page.rect.y1), stop_at is not None
        for k, (t, bb) in enumerate(bl):
            if bb[1] < y_from - 2 or (stop_at is not None and bb[1] > stop_at):
                continue
            if is_credit(t):
                y_to, done = absorb_wrap_tails(bl, k, bb[3]) + 4, True
                break
        regions.append((p, y_from, y_to))
        pages.append(p)
        if done:
            break
    if not regions:
        return None, []
    tiles = []
    for p, y0, y1 in regions:
        pr = doc[p - 1].rect
        pix = doc[p - 1].get_pixmap(dpi=dpi, clip=fitz.Rect(pr.x0, max(pr.y0, y0),
                                                            pr.x1, min(pr.y1, y1)))
        tmp = os.path.splitext(out_png)[0] + f"_t{p}.png"
        pix.save(tmp)
        im = Image.open(tmp).convert("RGB")
        from PIL import ImageChops
        bg = Image.new("RGB", im.size, im.getpixel((1, 1)))
        bbox = ImageChops.difference(im, bg).convert("L").point(
            lambda v: 255 if v > 18 else 0).getbbox()
        if bbox:
            im = im.crop(bbox)
        tiles.append(im)
        os.remove(tmp)
    tiles = [t for t in tiles if t.width > 40 and t.height > 20]
    if not tiles:
        return None, []
    W = max(t.width for t in tiles)
    H = sum(t.height for t in tiles)
    sheet = Image.new("RGB", (W, H), "white")
    y = 0
    for t in tiles:
        sheet.paste(t, (0, y)); y += t.height
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    sheet.save(out_png)
    return out_png, pages


def _chunks(doc, first_page, span=2):
    """The appendix is a run of descriptions separated by 'Back to Figure' markers.
    Return each description on these pages as one string."""
    out, cur = [], []
    for step in range(span):
        if first_page + step >= doc.page_count:
            break
        for t, _bb in blocks(doc[first_page + step]):
            if t == "Back to Figure":
                if cur:
                    out.append(re.sub(r"\s+", " ", " ".join(cur)).strip())
                    cur = []
                continue
            cur.append(t)
    if cur:
        out.append(re.sub(r"\s+", " ", " ".join(cur)).strip())
    return [c for c in out if len(c) > 25]


def long_description(doc, page, cap_bbox, title):
    """Follow the 'Description' stub under a caption to the book's accessibility appendix.

    The stub's destination PAGE is reliable; its y offset is not (these are reflowed
    pages, and the y points at a scroll position rather than the text). So instead of
    trusting the offset, take every description on the destination page and pick the one
    that CORROBORATES the caption. A chunk that shares no vocabulary with its own caption
    is the wrong chunk, and is dropped rather than believed — a mismatched description
    would silently poison every figure-to-card match downstream."""
    cy1 = cap_bbox[3]
    cands = [l for l in page.get_links()
             if l.get("from") and l.get("page", -1) >= 0
             and 55 < l["from"].width < 120 and 0 <= l["from"].y0 - cy1 < 70]
    if not cands:
        return None
    l = min(cands, key=lambda x: x["from"].y0 - cy1)
    want = set(terms_of(title))
    if not want:
        return None
    best, score = None, 0.0
    for c in _chunks(doc, l["page"]):
        got = set(terms_of(c))
        ov = len(want & got) / len(want)
        if ov > score:
            best, score = c, ov
    # Require real corroboration. Captions and their descriptions always share the anatomy
    # they name; unrelated chunks land near zero.
    return best if score >= 0.25 else None


def terms_of(*texts):
    """Content words a card's answers can be tested against."""
    ws = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", " ".join(t for t in texts if t).lower())
    return sorted({w for w in ws if w not in STOPWORDS})


def crossrefs(doc, label, first, last, cap_page):
    """Sentences in the body that point AT this figure — "...as shown in (FIGURE 4-1)".

    Only 2 of Chapter 4's 21 figures carry a publisher long description, because its
    plates are photographs with nothing labelled to describe. That leaves the matcher
    seeing FIGURE 4-1 as just {shannon, weaver, communication, model} and blind to the
    Noise / Encoding / Decoding boxes drawn inside it — so the card that figure actually
    illustrates ("noise is anything that dampens or obscures a message") scored zero
    against it.

    The prose that cites a figure is where the book explains it, and it is sitting in the
    text layer for free. Harvesting it recovers the vocabulary the picture contains but
    the caption never says. Cheap, deterministic, and it needs no vision pass."""
    num = label.split(None, 1)[1] if " " in label else label
    kind = label.split(None, 1)[0]
    pat = re.compile(rf"\b{kind}\s+{re.escape(num)}\b", re.I)
    out = []
    lo, hi = max(1, cap_page - 3), min(doc.page_count, cap_page + 4)
    for pno in range(max(first, lo), min(last, hi)):
        for t, _bb in blocks(doc[pno - 1]):
            if not pat.search(t) or CAPTION.match(t):
                continue      # the caption itself is already indexed
            for sent in re.split(r"(?<=[.!?])\s+", t):
                if pat.search(sent) and len(sent) < 400:
                    out.append(pat.sub(" ", sent).strip())
    return " ".join(dict.fromkeys(out))[:900] or None


def save_art(doc, art, page_no, out_png, rerender):
    """Write the plate. Prefer the ORIGINAL embedded bytes (no resample, no recompress);
    fall back to rendering the placed region for vector art or exotic colorspaces."""
    # Check for art BEFORE reusing the cache. Reversed, a caption whose art no longer
    # resolves silently adopts whatever file a previous (buggier) run left at that path,
    # so the count stays flat while the index quietly points at the wrong picture.
    if not art:
        return None, "unavailable"
    if os.path.exists(out_png) and not rerender:
        return out_png, "cached"
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    if art:
        info = doc.extract_image(art["xref"])
        if info and info.get("image") and info.get("ext") in ("png", "jpg", "jpeg"):
            path = os.path.splitext(out_png)[0] + "." + ("png" if info["ext"] == "png" else "jpg")
            with open(path, "wb") as f:
                f.write(info["image"])
            return path, "native"
    return None, "unavailable"


def matte_color(path):
    """The plate's own background, sampled from a corner.

    Almost every figure in this book sits on white, but a few do not, and padding a
    dark-ground plate with white would frame it in a bright halo. Sampling means the
    margin always continues the picture's own background."""
    try:
        out = subprocess.run(
            ["magick", path + "[1x1+0+0]", "-format", "%[pixel:p{0,0}]", "info:"],
            check=True, capture_output=True, text=True).stdout.strip()
        return out or "white"
    except Exception:
        return "white"


def study_copy(src_path, out_dir, max_px=1400, quality=88, pad_pct=4.0, lossless=False):
    """A study-sized derivative — this is what actually gets attached to a card.

    The native plate is the archive: 2133px and ~3 MB for the skull. On a phone that is
    ~20x more pixels than the screen can show and it would push a whole book past a
    gigabyte of media. Re-encoded at 1400px it is ~160 KB with every label still crisp,
    which is what makes it cheap enough to attach figures generously rather than
    rationing them.

    It is also MATTED. Extraction cuts exactly to the artwork bounds, so a label like
    "Parietal bone" ends flush against the image edge and the card looks cramped — the
    thing Parker got for free when he screenshotted a region of the page. So: trim to the
    true content box (plates carry inconsistent built-in whitespace, and normalising first
    is what makes the final margin uniform), scale, then add a border of `pad_pct` of the
    NORMALISED long edge. Because every study copy is scaled to the same long edge, that
    percentage yields the same absolute margin on every figure, wide or tall, rather than
    a margin that drifts with aspect ratio.

    Line art is different (Parker, 2026-08-08, genetics ch9): a vector render re-encoded
    to JPEG grows ringing halos around every label and line, and downscaling throws away
    resolution the PDF gives for free. So `lossless=True` (the vector-render and
    text-table paths) keeps PNG at the FULL render resolution — no resize, no JPEG.
    Flat-color line art compresses well in PNG, so these stay a few hundred KB."""
    os.makedirs(out_dir, exist_ok=True)
    ext = ".png" if lossless else ".jpg"
    out = os.path.join(out_dir, os.path.splitext(os.path.basename(src_path))[0] + ext)
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src_path):
        return out
    matte = matte_color(src_path)
    try:
        if lossless:
            import PIL.Image
            pad = int(round(PIL.Image.open(src_path).size[0] * pad_pct / 100.0)) or 8
            subprocess.run(["magick", src_path,
                            "-background", matte, "-alpha", "remove", "-alpha", "off",
                            "-fuzz", "2%", "-trim", "+repage",
                            "-bordercolor", matte, "-border", str(pad),
                            "-strip", out],
                           check=True, capture_output=True)
        else:
            pad = int(round(max_px * pad_pct / 100.0))
            subprocess.run(["magick", src_path,
                            "-background", matte, "-alpha", "remove", "-alpha", "off",
                            "-fuzz", "2%", "-trim", "+repage",
                            "-resize", f"{max_px}x{max_px}>",
                            "-bordercolor", matte, "-border", str(pad),
                            "-strip", "-quality", str(quality), out],
                           check=True, capture_output=True)
    except Exception:
        return None
    return out


def render_region(doc, page_no, rect, out_png, dpi=300):
    """Rasterize a page region — used for vector figures with no embedded bitmap."""
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    page = doc[page_no - 1]
    pix = page.get_pixmap(clip=fitz.Rect(*rect), dpi=dpi)
    pix.save(out_png)
    return out_png


def vector_region(page, cap_bbox):
    """Bounding box of the vector drawing sitting above a caption, if any."""
    cy0 = cap_bbox[1]
    boxes = [d["rect"] for d in page.get_drawings()
             if d["rect"].y1 <= cy0 + 2 and d["rect"].width > MIN_ART_PT
             and d["rect"].height > 8]
    if not boxes:
        return None
    x0 = min(b.x0 for b in boxes); y0 = min(b.y0 for b in boxes)
    x1 = max(b.x1 for b in boxes); y1 = max(b.y1 for b in boxes)
    if (x1 - x0) < MIN_ART_PT or (y1 - y0) < MIN_ART_PT:
        return None
    return (x0 - 4, y0 - 4, x1 + 4, y1 + 4)


def strip_duplicate_art(recs, base):
    """One raster belongs to at most ONE caption — R55.

    pair_art searches outward from a caption, so on a page whose figures are live-text
    margin tables (Giancoli p31) EVERY caption walks to the same nearby photo: chapter 1
    handed the K2 mountain (FIGURE 1-9's art) to four TABLE captions, and the micrometer
    to both FIGURE 1-11 and 1-12. A plate that genuinely straddles pages is one image
    placed twice under ONE label, so it never trips this. Only 'native' extractions are
    checked — renders are caption-bounded and cannot adopt a neighbour's art. Records
    losing their art are returned as skipped entries; the files stay on disk for
    inspection."""
    by_hash = {}
    for r in recs:
        if r.get("extraction") != "native" or not r.get("file"):
            continue
        p = os.path.join(base, r["file"])
        if not os.path.exists(p):
            continue
        by_hash.setdefault(hashlib.sha256(open(p, "rb").read()).hexdigest(), []).append(r)
    doomed = {}
    for h, claimants in by_hash.items():
        labels = sorted({r["label"] for r in claimants})
        if len(labels) > 1:
            for r in claimants:
                doomed[r["label"]] = labels
    kept, stripped = [], []
    for r in recs:
        if r["label"] in doomed:
            others = [l for l in doomed[r["label"]] if l != r["label"]]
            stripped.append({"label": r["label"], "page": r["caption_page"],
                             "why": f"duplicate-art: the same raster was claimed by "
                                    f"{', '.join(others)} too — pair_art mispairing (R55)"})
        else:
            kept.append(r)
    return kept, stripped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int)
    ap.add_argument("--pages", help="explicit physical page range, e.g. 515-680")
    ap.add_argument("--rerender", action="store_true")
    ap.add_argument("--dpi", type=int, default=450, help="only for vector figures (450 = print-sharp; Parker's full-quality bar, 2026-08-08)")
    ap.add_argument("--dpi-steps", type=int, default=150,
                    help="render dpi per panel when compositing a multi-page SKILL DRILL")
    ap.add_argument("--max-px", type=int, default=1400,
                    help="long edge of the study-size copy that gets attached to cards")
    ap.add_argument("--pad-pct", type=float, default=4.0,
                    help="matte around the study copy, %% of the normalised long edge")
    args = ap.parse_args()

    src = S.get_source(args.source)
    _id, pdf = S.resolve_attachment(src)
    if not os.path.exists(pdf):
        sys.exit(f"ERROR: PDF not on disk: {pdf}")

    if args.pages:
        a, _, b = args.pages.partition("-")
        first, last = int(a), int(b or a)
    elif args.segment is not None:
        first, last, _name = S.segment_range(src, args.segment)
    else:
        sys.exit("Give --segment N or --pages A-B.")

    doc = fitz.open(pdf)
    outdir = os.path.join(S.SKILL, "work", src["id"], "figures")
    recs, skipped = [], []
    # What the judge SAW is the most valuable text about a plate — it is the description
    # the publisher never supplied for most of them, and it cost a human-reviewed vision
    # pass. Carry it across rebuilds and fold it into the match terms, or every rebuild
    # silently throws that work away and the next match is no smarter than the last.
    seen = {}
    _idx_p = os.path.join(S.SKILL, "work", src["id"], "figure_index.json")
    if os.path.exists(_idx_p):
        try:
            for f in json.load(open(_idx_p)).get("figures", []):
                if f.get("seen_description"):
                    seen[f["label"]] = f["seen_description"]
        except Exception:
            pass

    for pno in range(first, min(last, doc.page_count)):
        page = doc[pno - 1]
        nxt = doc[pno] if pno < doc.page_count else None
        for cap in find_captions(page, nxt,
                                 caps_label=src.get("caption_style") == "caps-label"):
            art, art_page = pair_art(doc, pno, cap)
            slug = re.sub(r"[^A-Za-z0-9]+", "_", cap["label"]).strip("_")
            target = os.path.join(outdir, f"{slug}.png")
            # A SKILL DRILL is a multi-page procedure, not a single plate: its steps run
            # one per page after the banner. Composite them so the card carries the WHOLE
            # procedure rather than its first move.
            step_pages = []
            if cap["label"].upper().startswith("SKILL"):
                if args.rerender or not os.path.exists(target):
                    cpath, step_pages = skill_drill_composite(
                        doc, pno, target, dpi=args.dpi_steps, cap_bbox=cap["bbox"])
                else:
                    cpath, step_pages = target, skill_drill_pages(doc, pno)
                if cpath:
                    path, how = cpath, f"skill-drill-composite({len(step_pages)} steps)"
                    art, art_page = {"px": None, "bbox": None}, (step_pages[0] if step_pages else pno)
                else:
                    path, how = save_art(doc, art, art_page, target, args.rerender)
            else:
                path, how = save_art(doc, art, art_page, target, args.rerender)
            is_titled_above = cap["label"].startswith(("TABLE", "CHART"))
            if not path and is_titled_above:
                # A table typeset as live TEXT has no raster to extract; render its body.
                # This MUST come before vector_region, which searches ABOVE the caption —
                # right for a figure, backwards for a table. EMT TABLE 7-2 was handed the
                # "Special Populations" box sitting above its title, and that plate was
                # one build away from landing on 11 live cards (2026-08-03).
                tpath, tpages = text_table_render(doc, pno, cap["bbox"], target,
                                                  dpi=args.dpi_steps)
                if tpath:
                    path, how = tpath, f"text-table-render({len(tpages)}p)"
                    art, art_page = {"px": None, "bbox": None}, pno
            if not path and not is_titled_above:
                vr = vector_region(page, cap["bbox"])
                if vr:
                    path = render_region(doc, pno, vr, target, args.dpi)
                    how = "vector-render"
                    art = {"px": None, "bbox": vr}
                    art_page = pno
            if not path:
                skipped.append({"label": cap["label"], "page": pno, "why": "no art located"})
                continue
            desc = long_description(doc, page, cap["bbox"], cap["title"])
            xref = crossrefs(doc, cap["label"], first, last, pno)
            base = os.path.join(S.SKILL, "work", src["id"])
            study = study_copy(path, os.path.join(outdir, "study"), args.max_px,
                               pad_pct=args.pad_pct,
                               lossless=("render" in how))
            recs.append({
                "label": cap["label"],
                "title": cap["title"],
                "caption_page": pno,
                "art_page": art_page,
                "file": os.path.relpath(path, base),                       # native archive
                "study_file": os.path.relpath(study, base) if study else None,  # what gets attached
                "px": list(art["px"]) if art and art.get("px") else None,
                "extraction": how,
                "description": desc,
                "crossrefs": xref,
                "seen_description": seen.get(cap["label"]),
                "terms": terms_of(cap["title"], desc, xref, seen.get(cap["label"])),
            })

    recs, dup_stripped = strip_duplicate_art(recs, base)
    for d in dup_stripped:
        skipped.append(d)

    label = f"segment_{args.segment}" if args.segment is not None else f"pages_{first}_{last}"
    index = {"source": src["id"], "scope": label, "pages": [first, last],
             "figures": recs, "skipped": skipped}
    out = os.path.join(S.SKILL, "work", src["id"], "figure_index.json")
    prev = {}
    if os.path.exists(out):
        try:
            prev = json.load(open(out))
        except Exception:
            prev = {}
    if prev.get("scope") and prev.get("scope") != label and prev.get("figures"):
        # keep earlier scopes; merge by label
        merged = {f["label"]: f for f in prev["figures"]}
        merged.update({f["label"]: f for f in recs})
        index["figures"] = sorted(merged.values(), key=lambda f: (f["caption_page"], f["label"]))
        index["scope"] = f"{prev['scope']}+{label}"
    json.dump(index, open(out, "w"), indent=1)

    withdesc = sum(1 for r in recs if r["description"])
    print(f"{len(recs)} figure(s) indexed from pages {first}-{last}")
    print(f"  native-resolution extractions: {sum(1 for r in recs if r['extraction']=='native')}")
    print(f"  vector renders               : {sum(1 for r in recs if r['extraction']=='vector-render')}")
    print(f"  with publisher long description: {withdesc}/{len(recs)}")
    if skipped:
        print(f"  {len(skipped)} caption(s) with no locatable art:")
        for s in skipped[:12]:
            print(f"    p{s['page']} {s['label']}")
    print(f"\n  images -> {outdir}")
    print(f"  index  -> {out}")


if __name__ == "__main__":
    main()
