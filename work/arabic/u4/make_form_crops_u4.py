#!/usr/bin/env python3
"""Unit 4 letter-form plates (daal, dhaal, raa, zaay, hamza) — same doctrine as u2/make_form_crops.py:
MEASURED boxes (find_red_bands.py on the 400 dpi render of the 600 dpi scan SPRRWAP7), red-only
composite over the page's own paper (no bleed-through), NO-CLIP assertion, uniform mat, lossless PNG."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "u2"))
import numpy as np
from PIL import Image
import make_form_crops as M   # ink_mask, redonly, GROW_PX, MAT

PAGES = os.path.expanduser("~/arabic-catchup/letters/pages")
# letter -> (physical page, x0, y0, x1, y1) page fractions of the measured red INK band
BOXES = {
    "daal":  (95,  0.1329, 0.5184, 0.3259, 0.5350),
    "dhaal": (97,  0.1329, 0.7039, 0.3268, 0.7275),
    "raa":   (99,  0.1326, 0.6502, 0.3271, 0.6689),
    "zaay":  (101, 0.1329, 0.1452, 0.3276, 0.1718),
    "hamza": (86,  0.1629, 0.5757, 0.2344, 0.6202),
}
def build(name, spec, outdir):
    page, x0, y0, x1, y1 = spec
    im = Image.open(f"{PAGES}/hi_p{page}-{page:03d}.png").convert("RGB")
    W, H = im.size
    box = (max(0, int(x0 * W) - M.GROW_PX), max(0, int(y0 * H) - M.GROW_PX),
           min(W, int(x1 * W) + M.GROW_PX), min(H, int(y1 * H) + M.GROW_PX))
    cut = im.crop(box); m = M.ink_mask(np.asarray(cut)); ys, xs = np.where(m)
    if not len(ys): sys.exit(f"{name}: no ink in box")
    top, bot, left, right = ys.min(), ys.max(), xs.min(), xs.max()
    touches = [n for n, v in (("top", top), ("left", left)) if v == 0]
    if bot == m.shape[0] - 1: touches.append("bottom")
    if right == m.shape[1] - 1: touches.append("right")
    if touches: sys.exit(f"{name}: ink touches {touches} -- box clips the row")
    cut = M.redonly(cut.crop((left, top, right + 1, bot + 1)), im)
    paper = tuple(np.asarray(im)[40:80, 40:80].reshape(-1, 3).mean(0).astype(int))
    pad = int(M.MAT * max(cut.size))
    plate = Image.new("RGB", (cut.size[0] + 2 * pad, cut.size[1] + 2 * pad), paper); plate.paste(cut, (pad, pad))
    out = f"{outdir}/arabic_u4_forms_{name}_v1.png"; plate.save(out, "PNG", optimize=True)
    print(f"  {name:6} p{page} {plate.size[0]}x{plate.size[1]} -> {out}")
if __name__ == "__main__":
    for k, v in BOXES.items(): build(k, v, os.path.join(os.path.dirname(__file__), "media"))
