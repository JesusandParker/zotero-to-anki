#!/usr/bin/env python3
"""Deterministic source-crop builder for the Arabic scan.

THE RULE (generalizes to any unit / any scanned source):

  1. ROUGH BOX  — a generous fractional box that CONTAINS the whole object and no neighbour.
  2. TRIM + ASSERT — trim to ink bounds, then assert the trimmed bbox does NOT touch any
                  rough-box edge. Touching means the box cut through the object and `-trim`
                  (which can only SHRINK, never grow) tightened around the clipped version —
                  producing a lopsided crop that looks deliberate. That is exactly how the
                  alphabet chart shipped with its right column sliced off (2026-08-08).
                  A margin of untouched whitespace on all four sides is the proof of
                  completeness, and it FAILS LOUD instead of shipping silently.
                  (Auto-growing the box was tried and abandoned: on these pages the gap
                  between a table and neighbouring body text is no larger than the gutters
                  BETWEEN its own cells, so no single probe distance can tell "still inside
                  the object" from "now touching the next paragraph".)
  3. UNIFORM MAT — one fixed white border on every crop, so all cards look like a set.
  4. VERSIONED FILENAME — Anki caches media BY FILENAME; new bytes under an old name keep
                  serving the stale image, on the Mac and on every synced device.

  The build FAILS LOUD if a crop cannot converge (still touching an edge at the expansion
  cap) — that means the object runs into a neighbour and needs a human decision, not a
  silently lopsided image.

Run:  python3 make_crops.py     -> crops + contact sheet at /tmp/crops_v3.png
"""
import subprocess, os, re, sys

W    = os.path.dirname(os.path.abspath(__file__))
VER  = "_v3"
PAD  = 18      # uniform white mat, px
FUZZ = 12      # % tolerance for "background" on a 110dpi scan
STEP = 0.025   # probe distance as a fraction of the page: MUST exceed the widest gap
               # inside an object (cell gutters) and stay under the gap to its neighbours
MAXIT = 40

# name -> (page render, seed box x0,y0,x1,y1) — only has to start inside the object.
TARGETS = {
    # Boxes below were MEASURED with `find_boxes.py` (fill-colour band segmentation), not
    # eyeballed, then padded ~1.5%. Measuring is what caught the real defect: the alphabet
    # chart runs to x=0.656 and the old hand-picked box cut it at 0.625 — one sliced column.
    "alphabet_chart":  ("page_16.png", 0.210, 0.452, 0.674, 0.755),
    "symbols_chart":   ("page_17.png", 0.210, 0.080, 0.890, 0.380),
    "consonants1":     ("page_25.png", 0.140, 0.437, 0.950, 0.920),
    "consonants2":     ("page_26.png", 0.040, 0.080, 0.860, 0.400),
    "vowels":          ("page_26.png", 0.076, 0.588, 0.678, 0.962),
    "arab_map":        ("page_27.png", 0.130, 0.600, 0.900, 0.930),
    "vocab_table":     ("page_29.png", 0.160, 0.200, 0.960, 0.850),
}

def trim_bbox(src, X, Y, CW, CH):
    """Ink bounds inside the given window, as (w,h,x,y) relative to the window."""
    out = subprocess.run(["magick", src, "-crop", f"{CW}x{CH}+{X}+{Y}", "+repage",
                          "-fuzz", f"{FUZZ}%", "-format", "%@", "info:"],
                         capture_output=True, text=True).stdout.strip()
    m = re.match(r"(\d+)x(\d+)\+(\d+)\+(\d+)", out)
    return tuple(map(int, m.groups())) if m else None

def build(name, src, x0, y0, x1, y1):
    pw, ph = map(int, subprocess.check_output(["identify", "-format", "%w %h", src]).split())
    X, Y = int(pw * x0), int(ph * y0)
    CW, CH = int(pw * (x1 - x0)), int(ph * (y1 - y0))
    dx, dy = int(pw * STEP), int(ph * STEP)

    tw, th, tx, ty = trim_bbox(src, X, Y, CW, CH)
    touching = [s for s, cond in (("left", tx == 0), ("top", ty == 0),
                                  ("right", tx + tw >= CW), ("bottom", ty + th >= CH)) if cond]
    if touching:
        sys.exit(f"FAIL {name}: rough box CLIPS the object on {touching} — trim can only "
                 f"shrink, so this would ship a lopsided crop. Widen those sides.")
    X, Y, CW, CH = X + tx, Y + ty, tw, th

    out = f"src_{name}{VER}.png"
    subprocess.run(["magick", src,
                    "-crop", f"{CW}x{CH}+{X}+{Y}", "+repage",
                    "-resize", "1400x1400>",
                    "-bordercolor", "white", "-border", str(PAD), out], check=True)
    dims = subprocess.check_output(["identify", "-format", "%wx%h", out]).decode()
    print(f"  {out:32s} {dims:12s} converged, no clipped side ✓")
    return out

if __name__ == "__main__":
    os.chdir(W)
    made = [build(n, *spec) for n, spec in TARGETS.items()]
    subprocess.run(["magick", made[0], made[1], "+append", "/tmp/r1.png"], check=True)
    subprocess.run(["magick", made[2], made[3], "+append", "/tmp/r2.png"], check=True)
    subprocess.run(["magick", made[4], made[5], "+append", "/tmp/r3.png"], check=True)
    subprocess.run(["magick", "/tmp/r1.png", "/tmp/r2.png", "/tmp/r3.png", made[6],
                    "-append", "-resize", "1500x", "/tmp/crops_v3.png"], check=True)
    print("contact sheet -> /tmp/crops_v3.png")
