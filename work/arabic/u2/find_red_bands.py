#!/usr/bin/env python3
"""Measure horizontal bands of the book's RED ink on a rendered page.

find_crop_boxes.py masks a pale TABLE FILL; Alif Baa's Writing rows are saturated red
GLYPHS on white, which that mask cannot see. Same doctrine (measure, never eyeball),
different ink: mask strong red, segment contiguous row-bands, report page fractions.
"""
import sys
import numpy as np
from PIL import Image

def red_mask(im):
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    # saturated red ink: red clearly dominant over both other channels, and not pale
    return (r > 110) & (r - g > 55) & (r - b > 45)

def bands(path, min_px=6, gap=14, min_h=14):
    im = np.asarray(Image.open(path).convert("RGB"))
    m = red_mask(im)
    H, W = m.shape
    on = m.sum(1) > min_px
    out, start, last = [], None, -999
    for y, v in enumerate(on):
        if v:
            if start is None: start = y
            last = y
        elif start is not None and y - last > gap:
            out.append((start, last)); start = None
    if start is not None: out.append((start, last))
    print(f"{path} ({W}x{H})")
    for s, e in out:
        if e - s < min_h: continue
        cols = m[s:e+1].sum(0)
        xs = np.where(cols > 1)[0]
        if not len(xs): continue
        print(f"   y {s/H:.4f}-{e/H:.4f}  x {xs.min()/W:.4f}-{xs.max()/W:.4f}  "
              f"h={e-s}px  w={xs.max()-xs.min()}px  px={int(m[s:e+1].sum())}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        bands(p); print()
