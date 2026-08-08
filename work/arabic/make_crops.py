#!/usr/bin/env python3
"""Deterministic source-crop builder for the Arabic scan.

THE RULE (generalizes to any unit / any scanned source):
  1. ROUGH BOX  — a generous fractional box that contains the target table/figure and
     NO neighbouring text. This is the only hand-picked input; it only has to be
     "inside the gutters", not pixel-accurate.
  2. AUTO-TRIM  — `-fuzz N% -trim` shrinks to the true ink bounds, so the exact edges
     of the artwork are found by the image itself, never by my eyeballing. This is what
     kills both failure modes at once: sliced neighbours (rough box excludes them) and
     dead whitespace / off-by-a-hair edges (trim fixes them).
  3. UNIFORM MAT — one fixed white border on every crop, so all cards look like a set.
  4. VERSIONED FILENAME — `_v2` suffix. Anki's webview caches media BY FILENAME; writing
     new bytes under an old name leaves the stale image on screen (and on synced devices).
     A new name is the only reliable cache-bust.

Run:  python3 make_crops.py            (writes crops + a contact sheet at /tmp/crops_v2.png)
"""
import subprocess, os

W = os.path.dirname(os.path.abspath(__file__))
VER = "_v2"
PAD = 18          # uniform white mat, px
FUZZ = 12         # % tolerance for "background" when trimming a 110dpi scan

# name -> (page render, rough fractional box x0,y0,x1,y1)
# Rough boxes only need to sit inside the page gutters around each object.
TARGETS = {
    "alphabet_chart":  ("page_16.png", 0.19, 0.45, 0.63, 0.74),
    "symbols_chart":   ("page_17.png", 0.21, 0.08, 0.89, 0.38),
    "consonants1":     ("page_25.png", 0.14, 0.437, 0.95, 0.92),
    "consonants2":     ("page_26.png", 0.04, 0.08, 0.86, 0.40),
    "vowels":          ("page_26.png", 0.04, 0.588, 0.73, 0.945),
    "arab_map":        ("page_27.png", 0.13, 0.60, 0.90, 0.93),
    "vocab_table":     ("page_29.png", 0.16, 0.20, 0.96, 0.85),
}

def build(name, src, x0, y0, x1, y1):
    w, h = map(int, subprocess.check_output(["identify", "-format", "%w %h", src]).split())
    X, Y = int(w * x0), int(h * y0)
    CW, CH = int(w * (x1 - x0)), int(h * (y1 - y0))
    out = f"src_{name}{VER}.png"
    subprocess.run([
        "magick", src,
        "-crop", f"{CW}x{CH}+{X}+{Y}", "+repage",   # 1. rough box
        "-fuzz", f"{FUZZ}%", "-trim", "+repage",     # 2. auto-trim to real ink bounds
        "-resize", "1400x1400>",
        "-bordercolor", "white", "-border", str(PAD),  # 3. uniform mat
        out,
    ], check=True)
    dims = subprocess.check_output(["identify", "-format", "%wx%h", out]).decode()
    print(f"  {out:34s} {dims}")
    return out

if __name__ == "__main__":
    os.chdir(W)
    made = [build(n, *spec) for n, spec in TARGETS.items()]
    # contact sheet for the mandatory human/visual QA pass
    subprocess.run(["magick", made[0], made[1], "+append", "/tmp/r1.png"], check=True)
    subprocess.run(["magick", made[2], made[3], "+append", "/tmp/r2.png"], check=True)
    subprocess.run(["magick", made[4], made[5], "+append", "/tmp/r3.png"], check=True)
    subprocess.run(["magick", "/tmp/r1.png", "/tmp/r2.png", "/tmp/r3.png", made[6],
                    "-append", "-resize", "1500x", "/tmp/crops_v2.png"], check=True)
    print("contact sheet -> /tmp/crops_v2.png")
