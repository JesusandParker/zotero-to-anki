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
import argparse, json, os, re, sys

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
# Every genuine caption in this book is trailed by the publisher credit and an
# accessibility "Description" stub. That pairing is what separates a caption from prose.
CREDIT_LINE = re.compile(r"^\s*(©|\(c\))\s*\S", re.I)
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


def find_captions(page):
    """Caption blocks on a page, corroborated by the trailing credit/Description stub."""
    bl = blocks(page)
    found = []
    for i, (t, bb) in enumerate(bl):
        m = CAPTION.match(t)
        if not m:
            continue
        # look ahead a few blocks for the credit line or the Description stub; a caption
        # may wrap onto a second block before the credit appears.
        tail = [x[0] for x in bl[i + 1:i + 5]]
        if not any(CREDIT_LINE.match(x) or x == DESC_STUB for x in tail):
            continue
        title = t
        for nxt, _ in bl[i + 1:i + 3]:          # stitch a wrapped caption line
            if CREDIT_LINE.match(nxt) or nxt == DESC_STUB:
                break
            title += " " + nxt
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
    elif not above and cy1 > page.rect.height - 140 and pno < doc.page_count:
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


def save_art(doc, art, page_no, out_png, rerender):
    """Write the plate. Prefer the ORIGINAL embedded bytes (no resample, no recompress);
    fall back to rendering the placed region for vector art or exotic colorspaces."""
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

    for pno in range(first, min(last, doc.page_count)):
        page = doc[pno - 1]
        for cap in find_captions(page):
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
            recs.append({
                "label": cap["label"],
                "title": cap["title"],
                "caption_page": pno,
                "art_page": art_page,
                "file": os.path.relpath(path, os.path.join(S.SKILL, "work", src["id"])),
                "px": list(art["px"]) if art and art.get("px") else None,
                "extraction": how,
                "description": desc,
                "terms": terms_of(cap["title"], desc),
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
