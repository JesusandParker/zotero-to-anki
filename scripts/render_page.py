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
    h_pt = page_height_pt(pdf, page)
    full = out.replace(".png", "_full.png")
    render(pdf, page, full, dpi)
    scale = dpi / 72.0
    x0, y0, x1, y1 = rect
    left = max(0, (x0 - PAD_PT)) * scale
    top = max(0, (h_pt - y1 - PAD_PT)) * scale
    width = (x1 - x0 + 2 * PAD_PT) * scale
    height = (y1 - y0 + 2 * PAD_PT) * scale
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
    ap.add_argument("--dpi", type=int, default=150,
                    help="150 suits tables; raise to ~220 for dense figures or script")
    args = ap.parse_args()

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
