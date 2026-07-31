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
import argparse, json, os, re, subprocess, sys

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
CAPTION = re.compile(r"^\s*(FIGURE|TABLE|BOX|SKILL\s+DRILL|CHART)\s+([\dA-Z][\d\-.]*)\b", re.I)
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
    r"|(?:Reproduced|Adapted|Modified|Data)\s+(?:from|with|by)\b"
    r"|Photograph(?:ed)?\s+by\b"
    r"|[A-Z](?:\s*[,–-]\s*[A-Z])*\s*:\s*\S{0,3}\s*(?:©|\(c\)))", re.I)
CREDIT_MAX_CHARS = 200
DESC_STUB = "Description"
MIN_ART_PT = 40           # ignore rules, bullets, icons
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


def find_captions(page, next_page=None):
    """Caption blocks on a page, corroborated by the trailing credit/Description stub.

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
        if not any(is_credit(x) or x == DESC_STUB for x in tail):
            continue
        title = t
        for cont, _ in bl[i + 1:i + 3]:         # stitch a wrapped caption line
            if is_credit(cont) or cont == DESC_STUB:
                break
            title += " " + cont
        found.append({
            "label": f"{m.group(1).upper().replace('  ', ' ')} {m.group(2)}",
            "title": re.sub(r"\s+", " ", title).strip(),
            "bbox": bb,
        })
    return found


def pair_art(doc, pno, cap):
    """The art a caption belongs to.

    House style splits by kind: a FIGURE is captioned UNDERNEATH its plate, a TABLE is
    titled ABOVE its body. Getting this backwards is why the image-only tables (EMT
    TABLE 6-9/6-10) look like they have no art at all."""
    page = doc[pno - 1]
    cx0, cy0, cx1, cy1 = cap["bbox"]
    above = not cap["label"].startswith(("TABLE", "CHART"))
    best, bd = None, 1e9
    for a in art_on(page):
        ax0, ay0, ax1, ay1 = a["bbox"]
        gap = (cy0 - ay1) if above else (ay0 - cy1)
        if -5 <= gap <= CAPTION_GAP_PT and min(cx1, ax1) - max(cx0, ax0) > 0 and gap < bd:
            best, bd = a, gap
    if best:
        return best, pno
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


def study_copy(src_path, out_dir, max_px=1400, quality=88, pad_pct=4.0):
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
    a margin that drifts with aspect ratio."""
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, os.path.splitext(os.path.basename(src_path))[0] + ".jpg")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src_path):
        return out
    pad = int(round(max_px * pad_pct / 100.0))
    matte = matte_color(src_path)
    try:
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int)
    ap.add_argument("--pages", help="explicit physical page range, e.g. 515-680")
    ap.add_argument("--rerender", action="store_true")
    ap.add_argument("--dpi", type=int, default=300, help="only for vector figures")
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
        for cap in find_captions(page, nxt):
            art, art_page = pair_art(doc, pno, cap)
            slug = re.sub(r"[^A-Za-z0-9]+", "_", cap["label"]).strip("_")
            target = os.path.join(outdir, f"{slug}.png")
            path, how = save_art(doc, art, art_page, target, args.rerender)
            if not path:
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
                               pad_pct=args.pad_pct)
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
