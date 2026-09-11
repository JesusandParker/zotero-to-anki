#!/usr/bin/env python3
"""
render_page.py — render a page of a registered source to a PNG, or crop out the exact
region Parker area-selected.

Two jobs:

  * WHOLE PAGE — for a highlight whose fact lives in a table or figure (a hazmat placard,
    a vital-signs-by-age table, an anatomy plate, an Arabic script chart), or whenever
    grounding came back PARTIAL / NOT_FOUND and the writer needs to SEE the page.

        python3 render_page.py --source emt 198
        python3 render_page.py --source arabic 42 --dpi 220

  * CROPPED SELECTION — for an `kind: "image"` item in a highlights file: Parker drew a
    box around a diagram in Zotero and that box IS the card. Crops precisely to it.

        python3 render_page.py --source isaacs17 --crop-from work/isaacs17/all_highlights.json

Zotero stores the selection in PDF points with a bottom-left origin; PNGs are top-left,
so the y axis is flipped against the page height reported by pdfinfo.
"""
import argparse, json, os, re, subprocess, sys

import sources as S

PAD_PT = 6  # a little breathing room so the crop isn't flush against the diagram


def page_boxes(pdf, page):
    """(media, crop) boxes of one page in points, from `pdfinfo -box`.

    Why both, and why this function exists (hazard found 2026-09-11, genetics ch10):
    **pdftoppm renders the MEDIA box, while a Zotero/pdf.js/PyMuPDF rect is measured from
    the CROP box's origin.** On this genetics textbook the CropBox starts at (36.04, 36.03),
    so converting a rect to pixels without that offset lands the crop 225 px away at 450 dpi
    — measured: a box around "DNA gyrase" on p256 landed on blank artwork, and the corrected
    box landed on the phrase. It stayed invisible for two chapters because neither carded
    chapter has an area-selection mark, and invisible on the EMT book because its CropBox and
    MediaBox share an origin. Never scale a PDF rect by dpi/72 alone; go through here."""
    out = subprocess.run(["pdfinfo", "-box", "-f", str(page), "-l", str(page), pdf],
                         capture_output=True, text=True, timeout=60).stdout
    def box(name):
        m = re.search(rf"{name}:\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", out)
        return tuple(float(g) for g in m.groups()) if m else None
    media, crop = box("MediaBox"), box("CropBox")
    if not media:
        sys.exit(f"ERROR: could not read MediaBox of page {page} from `pdfinfo -box`.")
    return media, (crop or media)


def rect_to_px(rect, media, crop, dpi, pad_pt=0.0):
    """A PDF rect (crop-box origin, bottom-left, as Zotero stores it) -> pixel box in a
    pdftoppm render of the MEDIA box. Returns (left, top, width, height) in pixels."""
    s = dpi / 72.0
    x0, y0, x1, y1 = rect
    ax0, ay0 = x0 + crop[0], y0 + crop[1]          # -> absolute user space
    ax1, ay1 = x1 + crop[0], y1 + crop[1]
    left = max(media[0], ax0 - pad_pt) - media[0]
    top = media[3] - min(media[3], ay1 + pad_pt)
    return (left * s, top * s,
            (min(media[2], ax1 + pad_pt) - max(media[0], ax0 - pad_pt)) * s,
            (min(media[3], ay1 + pad_pt) - max(media[1], ay0 - pad_pt)) * s)


def _self_test():
    """Pure math, no PDF: the genetics book's real boxes at 450 dpi."""
    media = (0.0, 0.0, 738.0, 855.0)
    crop = (36.03519821166992, 36.03497314453125, 700.3359985351562, 817.2188720703125)
    # a 10x10pt rect at the crop-box origin must land at the crop offset, not at 0,0
    L, T, W, H = rect_to_px((0, 0, 10, 10), media, crop, 450)
    assert abs(L - 36.035 * 6.25) < 1, L
    assert abs(T - (855 - 46.035) * 6.25) < 1, T
    assert abs(W - 62.5) < 1 and abs(H - 62.5) < 1, (W, H)
    # a CropBox == MediaBox page must behave exactly as the old naive math did
    L2, T2, _, _ = rect_to_px((72, 100, 172, 200), media, media, 450)
    assert abs(L2 - 72 * 6.25) < 1e-6 and abs(T2 - (855 - 200) * 6.25) < 1e-6, (L2, T2)
    print("render_page self-test: rect_to_px honours the CropBox offset  ✓")
    return True


def page_height_pt(pdf, page):
    """Page height in points, per page (a PDF can mix page sizes)."""
    out = subprocess.run(["pdfinfo", "-f", str(page), "-l", str(page), pdf],
                         capture_output=True, text=True, timeout=60).stdout
    m = re.search(r"Page\s+\d+\s+size:\s+([\d.]+)\s+x\s+([\d.]+)\s+pts", out)
    if not m:
        m = re.search(r"Page size:\s+([\d.]+)\s+x\s+([\d.]+)\s+pts", out)
    if not m:
        sys.exit(f"ERROR: could not read the page size of page {page} from pdfinfo.")
    return float(m.group(2))


def render(pdf, page, out, dpi):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prefix = out[:-4] if out.lower().endswith(".png") else out
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi),
                    "-png", "-singlefile", pdf, prefix], check=True)
    return out


def crop(pdf, page, rect, out, dpi):
    """Crop `rect` (PDF points, bottom-left origin) out of `page` into `out`."""
    media, cropbox = page_boxes(pdf, page)
    full = out.replace(".png", "_full.png")
    render(pdf, page, full, dpi)
    left, top, width, height = rect_to_px(rect, media, cropbox, dpi, PAD_PT)
    subprocess.run(["magick", full, "-crop",
                    f"{int(width)}x{int(height)}+{int(left)}+{int(top)}",
                    "+repage", out], check=True)
    os.remove(full)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", type=int, nargs="?", help="physical page number (whole-page mode)")
    ap.add_argument("--source", required=True, help="source id (see: sources.py list)")
    ap.add_argument("--crop-from", help="a highlights JSON: crop every kind:'image' item in it")
    ap.add_argument("--out", help="output PNG path (whole-page mode)")
    ap.add_argument("--self-test", action="store_true",
                    help="check the PDF-rect -> pixel conversion (CropBox offset)")
    ap.add_argument("--dpi", type=int, default=150,
                    help="150 suits tables; raise to ~220 for dense figures or script")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(0 if _self_test() else 1)

    src = S.get_source(args.source)
    _item_id, pdf = S.resolve_attachment(src)
    if not os.path.exists(pdf):
        sys.exit(f"ERROR: the PDF for source '{src['id']}' is not on disk:\n  {pdf}")

    if args.crop_from:
        items = json.load(open(args.crop_from))
        imgs = [i for i in items if i.get("kind") == "image" and i.get("crop", {}).get("rect")]
        if not imgs:
            print(f"No area selections in {args.crop_from} — nothing to crop.")
            return
        outdir = os.path.join(S.SKILL, "work", src["id"])
        for n, i in enumerate(imgs, 1):
            page = int(re.sub(r"[^0-9]", "", str(i["page"])))
            # Name by page AND ordinal: two area selections on the same page are common
            # (a figure and the table beside it), and keying on the page alone made the
            # second crop silently overwrite the first.
            same = [j for j in imgs
                    if int(re.sub(r"[^0-9]", "", str(j["page"]))) == page]
            suffix = f"_{same.index(i) + 1}" if len(same) > 1 else ""
            out = os.path.join(outdir, f"figure_p{page}{suffix}.png")
            crop(pdf, page, i["crop"]["rect"], out, args.dpi)
            note = i.get("user_comment")
            print(f"  p{page} -> {out}" + (f"   (Parker's note: {note[:70]})" if note else ""))
        print(f"\n{len(imgs)} figure(s) cropped. Attach each to its card via the \"image\" field.")
        return

    if args.page is None:
        ap.error("give a page number, or use --crop-from <highlights.json>")
    out = args.out or os.path.join(S.SKILL, "work", src["id"], f"page_{args.page}.png")
    print(render(pdf, args.page, out, args.dpi))


if __name__ == "__main__":
    main()
