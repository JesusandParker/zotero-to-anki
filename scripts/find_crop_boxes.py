#!/usr/bin/env python3
"""MEASURE where a scanned page's tables/charts actually sit, instead of eyeballing a box.

Why (2026-08-08, Arabic Unit 1): three rounds of hand-picked crop boxes each shipped a
defect, the worst being the alphabet chart with its entire right-hand column sliced off.
Measuring showed why instantly — the chart runs to x=0.656 and the box cut it at 0.625.
Eyeballing a box off a rendered page is not a reliable way to find an object's edge; the
page's own pixels are.

Method: a coloured table's fill is a narrow RGB band, so mask for it and segment the page
into contiguous horizontal BANDS of fill. Each band is one object (or one row-group of an
object); the printed header/heading decorations show up as their own thin bands and are
easy to discard by height. Report each band's bounds as page FRACTIONS, ready to paste
into a crop config.

    .venv/bin/python scripts/find_crop_boxes.py work/<source>/page_16.png

Limits: works on colour-filled tables. A black-on-white table or a photo has no fill band —
measure those by rendering the page and reading coordinates, then still let the crop
builder's no-clip assertion prove the box is right.
"""
import sys
import numpy as np
from PIL import Image

# the printed fill of these charts; widen only if a source uses a different palette
LO = dict(r=225, g_lo=165, g_hi=230, b_lo=135, b_hi=210)

def bands(path, min_px=25, gap=12, min_h=30):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    fill = (r > LO["r"]) & (g > LO["g_lo"]) & (g < LO["g_hi"]) & (b > LO["b_lo"]) & (b < LO["b_hi"])
    H, W = fill.shape
    on = fill.sum(1) > min_px
    out, start, last = [], None, -999
    for y, v in enumerate(on):
        if v:
            if start is None:
                start = y
            last = y
        elif start is not None and y - last > gap:
            out.append((start, last)); start = None
    if start is not None:
        out.append((start, last))

    print(f"{path}  ({W}x{H})")
    keep = []
    for s, e in out:
        cols = fill[s:e + 1].sum(0)
        xs = np.where(cols > 3)[0]
        if not len(xs):
            continue
        tag = "" if (e - s) >= min_h else "   <- thin: probably a heading rule, not the object"
        print(f"   y {s/H:.3f}-{e/H:.3f}   x {xs.min()/W:.3f}-{xs.max()/W:.3f}   h={e-s}px{tag}")
        if (e - s) >= min_h:
            keep.append((xs.min()/W, s/H, xs.max()/W, e/H))
    if keep:
        x0 = min(k[0] for k in keep); y0 = min(k[1] for k in keep)
        x1 = max(k[2] for k in keep); y1 = max(k[3] for k in keep)
        pad = 0.015
        print(f"\n   union of substantial bands, padded {pad:.3f}:")
        print(f"   ({max(0,x0-pad):.3f}, {max(0,y0-pad):.3f}, "
              f"{min(1,x1+pad):.3f}, {min(1,y1+pad):.3f})")
        print("   NB: a page with two separate objects gives two band groups — crop them "
              "separately rather than taking this union.")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        bands(p); print()
