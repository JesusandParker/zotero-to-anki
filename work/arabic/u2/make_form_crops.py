#!/usr/bin/env python3
"""Crop each Unit-2 letter's printed 'Writing' forms row into a study plate.

Doctrine (playbook 7e / SKILL 2.9): boxes are MEASURED (find_red_bands.py), the crop is
proved by a NO-CLIP ASSERTION -- after trimming to true ink, the bbox must not touch any
window edge -- and every plate gets a uniform mat sampled from the page's own paper.
Line art => lossless PNG at full render resolution, never resized, never JPEG.
"""
import sys
import numpy as np
from PIL import Image

# letter -> (physical page, x0, y0, x1, y1) as page fractions of the INK bounds
BOXES = {
    "alif": (39, 0.1353, 0.6886, 0.5271, 0.7164),
    "baa":  (41, 0.1353, 0.3764, 0.5588, 0.3973),
    "taa":  (44, 0.1629, 0.5159, 0.5847, 0.5382),
    "thaa": (46, 0.1647, 0.4259, 0.5859, 0.4495),
    "waaw": (48, 0.1612, 0.2650, 0.5329, 0.2850),
    "yaa":  (49, 0.1347, 0.8368, 0.5176, 0.8650),
}
GROW_PX = 22      # grow the measured ink box by a FIXED small margin, in render pixels.
                  # A page-FRACTION grow is the wrong unit here: 0.012 of the page height
                  # is ~53px at 400 dpi, which swallows the 'Writing' heading sitting
                  # ~50px above the row, and the assertion then reports the heading being
                  # clipped rather than the row. 22px is ~1.4 mm at 400 dpi.
MAT   = 0.06      # mat as a fraction of the plate's long edge

def ink_mask(a):
    """The forms row is printed in the book's RED ink. Trim and assert on red ONLY:
    including black body text would let a neighbouring paragraph define the bbox, and
    then 'ink touches the edge' would report the paragraph being cut, not the row."""
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    return (r > 110) & (r - g > 55) & (r - b > 45)

def redonly(cut, page_im):
    """Erase the reverse side's bleed-through, keeping the red glyphs intact.

    Parker's figure bar forbids page-text bleed outright. These Writing rows are printed
    ENTIRELY in the book's red ink, so anything not red is the ghost of the page behind --
    compositing the red over flat paper removes exactly the artifact and nothing real.
    Blending on a continuous redness alpha (rather than thresholding) keeps the glyphs'
    anti-aliased edges, so the letters do not come out jagged.
    """
    a = np.asarray(cut).astype(float)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    alpha = np.clip(((r - np.maximum(g, b)) - 12) / 45.0, 0, 1)[:, :, None]
    paper = np.asarray(page_im)[40:80, 40:80].reshape(-1, 3).mean(0)
    out = a * alpha + paper[None, None, :] * (1 - alpha)
    return Image.fromarray(out.round().astype(np.uint8))

def build(name, spec, outdir):
    page, x0, y0, x1, y1 = spec
    im = Image.open(f"work/arabic/u2/hi_p{page}.png").convert("RGB")
    W, H = im.size
    box = (max(0, int(x0 * W) - GROW_PX), max(0, int(y0 * H) - GROW_PX),
           min(W, int(x1 * W) + GROW_PX), min(H, int(y1 * H) + GROW_PX))
    cut = im.crop(box)
    a = np.asarray(cut)
    m = ink_mask(a)
    ys, xs = np.where(m)
    if not len(ys):
        sys.exit(f"{name}: no ink found in box -- box is wrong")
    top, bot, left, right = ys.min(), ys.max(), xs.min(), xs.max()
    # NO-CLIP ASSERTION: trimmed ink must not touch the window edge.
    touches = [n for n, v in (("top", top), ("left", left)) if v == 0]
    if bot == m.shape[0] - 1: touches.append("bottom")
    if right == m.shape[1] - 1: touches.append("right")
    if touches:
        sys.exit(f"{name}: ink touches {touches} -- box clips the row, widen it")
    cut = cut.crop((left, top, right + 1, bot + 1))
    cut = redonly(cut, im)
    # uniform mat in the page's own paper colour (sampled from a corner of the render)
    paper = tuple(np.asarray(im)[40:80, 40:80].reshape(-1, 3).mean(0).astype(int))
    pad = int(MAT * max(cut.size))
    plate = Image.new("RGB", (cut.size[0] + 2 * pad, cut.size[1] + 2 * pad), paper)
    plate.paste(cut, (pad, pad))
    out = f"{outdir}/arabic_u2_forms_{name}_v1.png"
    plate.save(out, "PNG", optimize=True)   # lossless, not resized
    print(f"  {name:5} p{page}  {plate.size[0]}x{plate.size[1]}  mat={pad}px  paper={paper}  -> {out}")

if __name__ == "__main__":
    print("letter form plates (lossless, measured, no-clip asserted):")
    for k, v in BOXES.items():
        build(k, v, "work/arabic/u2/media")
