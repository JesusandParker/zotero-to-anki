#!/usr/bin/env python3
"""
fix_labels.py — repair printed labels that are wrong or unreadable IN THE SOURCE ART,
by erasing the old words and typesetting the right text crisply in the same place.

  * s20_sternum        the slide's plate is 213x250 px; upscaled, every label is mush.
                       All seven labels are re-set in Arial at the size they occupied.
  * s18_sacrum_coccyx  "Sacral cana" — the source image itself cuts the label off.
  * m7_10_cervical     the lab manual prints "pedical"; the term is "pedicle".

Idempotent: it always starts again from the pristine copy build_images.py wrote
(<name>.orig.<ext>), so re-running never erases already-repaired text twice.
"""
import os, shutil, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocr, labels  # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"

# figure -> [(text as printed now, text to print, align)]
FIXES = {
    "s20_sternum.jpg": [
        ("Jugular notch", "Jugular notch", "left"),
        ("Clavicular notch", "Clavicular notch", "left"),
        ("Manubrium", "Manubrium", "left"),
        ("Sternal angle", "Sternal angle", "left"),
        ("Body", "Body", "left"),
        ("Facets for attachment of costal cartilages 1-7",
         "Facets for\nattachment\nof costal\ncartilages 1-7", "left"),
        ("Xiphoid process", "Xiphoid process", "left"),
    ],
    "s18_sacrum_coccyx.jpg": [("Sacral cana", "Sacral canal", "left")],
    "m7_10_cervical_model.jpg": [("pedical", "pedicle", "left")],
    "m7_02b_skull_obl_ant.jpg": [("mastoid processs", "mastoid process", "left")],
}

# figure -> [(box, mode)]  — erase something the source art gets WRONG.
#   s16_thoracic: the slide's "Pedicle" pointer ends on the transverse process (the real
#   pedicle is the bar between the two vertebral notches). Teaching the wrong spot is worse
#   than not labelling it, and the pedicle is drilled on four other plates.
ERASE = {
    "s16_thoracic.png": [((1422, 312, 1562, 364), "white"), ((1398, 352, 1447, 426), "neutral")],
}


def local_bg(a, box, pad=6):
    x0, y0, x1, y1 = box
    H, W = a.shape[:2]
    ring = np.concatenate([
        a[max(0, y0 - pad):y0, max(0, x0 - pad):min(W, x1 + pad)].reshape(-1, 3),
        a[y1:min(H, y1 + pad), max(0, x0 - pad):min(W, x1 + pad)].reshape(-1, 3),
        a[y0:y1, max(0, x0 - pad):x0].reshape(-1, 3),
        a[y0:y1, x1:min(W, x1 + pad)].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(ring, axis=0))


def ink(a, box):
    """The text colour: the pixels furthest from the local background inside the box."""
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    bg = np.array(local_bg(a, box))
    d = np.abs(sub - bg).sum(axis=1)
    return tuple(int(v) for v in np.median(sub[d >= np.percentile(d, 92)], axis=0))


def fit_size(text, box_w):
    """Largest Arial size whose rendered width of `text` fits the printed label's width.
    Width is what Vision measures tightly; its box HEIGHT carries padding, and fitting on
    height set the sternum's labels ~20% too large (they ran into their leader lines)."""
    lo, hi = 6, 200
    while lo < hi:
        mid = (lo + hi + 1) // 2
        l, t, r, b = ImageFont.truetype(ARIAL, mid).getbbox(text)
        if r - l <= box_w:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main():
    for name, fixes in FIXES.items():
        path = os.path.join(FIG, name)
        stem, ext = os.path.splitext(path)
        orig = f"{stem}.orig{ext}"
        if not os.path.exists(orig):
            shutil.copy(path, orig)
        im = Image.open(orig).convert("RGB")
        a = np.asarray(im).copy()
        W = ocr.words(orig, upscale=3.0 if im.size[0] < 1300 else 2.0)
        draw_jobs = []
        for old, new, align in fixes:
            hits = labels.find(W, old, max_hits=1)
            if not hits:
                sys.exit(f"{name}: could not find the printed label {old!r} — check OCR")
            (x0, y0, x1, y1), chain = hits[0]
            box = (int(x0) - 3, int(y0) - 3, int(x1) + 4, int(y1) + 4)
            fg = ink(a, box)
            bg = local_bg(a, box)
            lines_old = {}
            for w in chain:
                lines_old.setdefault(w["line"], []).append(w)
            # width-fit on the widest printed line, using that line's own words
            widest = max(lines_old.values(), key=lambda ws: max(w["x1"] for w in ws) - min(w["x0"] for w in ws))
            wtxt = " ".join(w["t"] for w in sorted(widest, key=lambda w: w["x0"]))
            size = fit_size(wtxt, max(w["x1"] for w in widest) - min(w["x0"] for w in widest))
            n_lines = len(lines_old)
            line_h = np.median([w["y1"] - w["y0"] for w in chain])
            pitch = (y1 - y0 - line_h) / (n_lines - 1) if n_lines > 1 else 0
            light_bg = sum(bg) / 3 > 128
            fg = tuple(min(c, 45) for c in fg) if light_bg else fg   # crisp near-black on paper
            a[box[1]:box[3], box[0]:box[2]] = bg
            draw_jobs.append([new, x0, y0, y1, size, fg, pitch, n_lines])
        # labels on one plate share one type size in the original art — use their median
        common = int(np.median([j[4] for j in draw_jobs]))
        for j in draw_jobs:
            j[4] = common
            print(f"{name}: -> {j[0]!r} at ({j[1]:.0f},{j[2]:.0f}) size {common} ink {j[5]}")
        out = Image.fromarray(a)
        d = ImageDraw.Draw(out)
        for new, x0, y0, y1, size, fg, pitch, n_lines in draw_jobs:
            f = ImageFont.truetype(ARIAL, size)
            rows = new.split("\n")
            _, t0, _, b0 = f.getbbox("Hg")
            step = pitch if (len(rows) > 1 and pitch) else (b0 - t0) * 1.2
            # vertically centre the block on the printed label's box
            block = (b0 - t0) + step * (len(rows) - 1)
            top = (y0 + y1) / 2 - block / 2
            for k, line in enumerate(rows):
                d.text((x0 - f.getbbox(line)[0], top + k * step - t0), line, font=f, fill=fg)
        if ext.lower() in (".jpg", ".jpeg"):
            out.save(path, quality=92, optimize=True)
        else:
            out.save(path, optimize=True)


def erase():
    for name, ops in ERASE.items():
        path = os.path.join(FIG, name)
        stem, ext = os.path.splitext(path)
        orig = f"{stem}.orig{ext}"
        if not os.path.exists(orig):
            shutil.copy(path, orig)
        a = np.asarray(Image.open(orig).convert("RGB")).copy()
        for (x0, y0, x1, y1), mode in ops:
            sub = a[y0:y1, x0:x1]
            if mode == "white":
                sub[:] = 255
            elif mode == "neutral":      # grey leader-line ink only; coloured anatomy stays
                mx, mn = sub.max(axis=2).astype(int), sub.min(axis=2).astype(int)
                # dark core of the line, then its light anti-aliased fringe (near-grey only)
                sub[((mx < 175) & (mx - mn < 32)) | ((mx < 250) & (mx - mn < 22))] = 255
            print(f"{name}: erased {mode} box {(x0, y0, x1, y1)}")
        out = Image.fromarray(a)
        out.save(path, quality=92, optimize=True) if ext.lower() in (".jpg", ".jpeg") \
            else out.save(path, optimize=True)


if __name__ == "__main__":
    main()
    erase()
