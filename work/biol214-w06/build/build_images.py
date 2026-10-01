#!/usr/bin/env python3
"""
build_images.py — every picture the BIOL 214 W06 (appendicular skeleton) deck uses, built from
the original sources at the best resolution each one offers.

Sources:
  * pdfclip — a region of the W06 slides re-exported LOSSLESSLY (cache/w06_lossless.pdf:
              LibreOffice with UseLosslessCompression, so PNG line art stays PNG instead of
              the Zotero PDF's JPEG re-encode). Every slide figure comes this way because the
              lab's own additions are PowerPoint objects laid over the picture: the blue boxes
              on slides 6/9/10, the scapula call-outs on slide 4, the white boxes that hide
              parts of the femur (11) and foot (14) figures.
  * manual  — a 600-dpi crop of the lab manual scan, Chapter 8 (PDF pages 180-192)
  * pptx    — a slide's own embedded picture straight out of the .pptx, used only for the
              left/right quiz pictures, which must NOT carry the lab's overlay boxes/arrows
  * derived — an already-built figure mirrored left-right (the left/right quiz twins)
  * popcorn — the Popcorn Points game renders (numbered pins; appendicular pins carry no
              instructor key, so only unmistakable bones are asked)

Every output is trimmed to its content, scaled to a common long edge, and MATTED at 4% of
that edge in the plate's own ring colour (parker-preferences: "a little bit of space").
`erase=True` blanks every printed word (Vision OCR boxes, filled with the local background)
for the "is this a left or right bone?" cards, whose picture IS the question.

Run:  ~/.claude/skills/zotero-to-anki/.venv/bin/python build_images.py [name ...]
"""
import os, sys, json
import fitz
import numpy as np
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ocr  # noqa: E402

W = os.path.dirname(HERE)                      # work/biol214-w06
CACHE = os.path.join(W, "cache")
OUT = os.path.join(W, "figures")
SLIDES_PDF = os.path.join(CACHE, "w06_lossless.pdf")
MANUAL_PDF = os.path.expanduser("~/Zotero/storage/6K6XWXMN/Anatomy & Physiology BIOL 214 "
                                "Laboratory Manual (600 dpi, searchable).pdf")

IO = 1600      # long edge for image-occlusion plates (they fill the card)
BACK = 1300    # long edge for back-of-card pictures
PAD = 0.04     # matte, fraction of the long edge

# name -> (kind, source, options)
#   clip  : crop box in PDF points (pdfclip)      box : 600-dpi page pixels (manual) or
#   scale : render scale for pdfclip                    source pixels (popcorn)
#   trim  : True (uniform border) | "dark" (black photo panel) | False
#   long  : output long edge        fmt : "png" | "jpg"
#   erase : blank every printed word (left/right quiz pictures)
#   paint : extra fractional boxes to blank (a word OCR missed)   up : pre-enlarge (pptx)
SPEC = {
    # ---------------- slides (lossless re-export; overlays included) ----------------
    "s02_overview":          ("pdfclip", 2, dict(clip=(526, 126, 830, 451), scale=3.0, long=1000)),
    "s03_clavicle":          ("pdfclip", 3, dict(clip=(164, 122, 620, 448), scale=3.6, long=IO, fmt="png")),
    "s04_scapula":           ("pdfclip", 4, dict(clip=(242, 122, 778, 436), scale=3.2, long=IO, fmt="png")),
    "s05_humerus":           ("pdfclip", 5, dict(clip=(330, 114, 764, 518), scale=3.4, long=IO, fmt="png")),
    "s06_forearm":           ("pdfclip", 6, dict(clip=(367, 132, 742, 480), scale=3.6, long=IO, fmt="png")),
    "s07_hand":              ("pdfclip", 7, dict(clip=(264, 100, 586, 446), scale=3.6, long=IO, fmt="png")),
    "s08_coxal_netter":      ("pdfclip", 8, dict(clip=(357, 80, 880, 530), scale=3.2, long=IO, fmt="png")),
    "s09_hip_lateral":       ("pdfclip", 9, dict(clip=(171, 40, 790, 501), scale=2.8, long=IO, fmt="png")),
    "s10_hip_medial":        ("pdfclip", 10, dict(clip=(171, 40, 790, 501), scale=2.8, long=IO, fmt="png")),
    "s11_femur":             ("pdfclip", 11, dict(clip=(305, 88, 797, 522), scale=3.4, long=IO, fmt="png")),
    "s12_patella":           ("pdfclip", 12, dict(clip=(148, 150, 636, 438), scale=3.4, long=IO, fmt="png")),
    "s13_tibia_fibula":      ("pdfclip", 13, dict(clip=(372, 130, 776, 502), scale=4.0, long=IO, fmt="png")),
    "s14_foot":              ("pdfclip", 14, dict(clip=(327, 106, 663, 485), scale=4.2, long=IO, fmt="png")),
    # ---------------- lab manual Ch 8 (600-dpi scan; PDF page numbers) ----------------
    "m8_01_appendicular":    ("manual", 180, dict(box=(2560, 500, 4820, 3240), long=BACK, whiten=True)),
    "m8_02_scapula":         ("manual", 181, dict(box=(150, 3440, 4800, 6150), long=IO, trim="dark")),
    "m8_03_clavicles":       ("manual", 181, dict(box=(150, 380, 2360, 2230), long=BACK, trim="dark")),
    "m8_04a_joints":         ("manual", 182, dict(box=(420, 640, 4800, 2740), long=BACK, trim="dark")),
    "m8_04b_humerus":        ("manual", 182, dict(box=(420, 2800, 2640, 5700), long=IO, trim="dark")),
    "m8_04c_forearm":        ("manual", 182, dict(box=(2620, 2800, 4800, 5700), long=IO, trim="dark")),
    "m8_06a_hand_palmar":    ("manual", 183, dict(box=(200, 450, 1870, 2050), long=IO, trim="dark")),
    "m8_06b_hand_dorsum":    ("manual", 183, dict(box=(1930, 450, 4650, 2050), long=IO, trim="dark")),
    "m8_07_hip_lateral":     ("manual", 184, dict(box=(420, 460, 4730, 3080), long=IO, trim="dark")),
    "m8_08_hip_medial":      ("manual", 184, dict(box=(300, 3640, 4640, 5700), long=IO, trim="dark")),
    "m8_09_femur_patella":   ("manual", 185, dict(box=(2290, 2920, 4690, 6120), long=IO, trim="dark")),
    "m8_10_gluteal":         ("manual", 185, dict(box=(262, 4370, 2290, 5985), long=IO, whiten=True)),
    "m8_11_q_carrying":      ("manual", 186, dict(box=(390, 390, 2400, 2900), long=BACK, whiten=True)),
    "m8_12_leg_foot":        ("manual", 186, dict(box=(2490, 2640, 4710, 6120), long=IO, trim="dark")),
    "m8_13_foot":            ("manual", 187, dict(box=(2300, 430, 4800, 3330), long=IO, whiten=True)),
    "m8_14_arches":          ("manual", 188, dict(box=(2560, 480, 4720, 4300), long=IO, whiten=True)),
    "m8_15_arch_height":     ("manual", 190, dict(box=(2530, 350, 4800, 3810), long=BACK, whiten=True)),
    "m8_16_q_measure":       ("manual", 191, dict(box=(280, 4140, 4650, 6150), long=BACK, trim="dark")),
    "m8_17_fetal":           ("manual", 192, dict(box=(2340, 350, 4650, 3120), long=BACK, whiten=True)),
    "m8_18_fetal_skull":     ("manual", 192, dict(box=(430, 3580, 4650, 5460), long=IO, trim="dark")),
    # ---------------- Popcorn Points renders (pins) ----------------
    "pp2_front_pins":        ("popcorn", "image3.png", dict(box=(180, 520, 1000, 1362), long=1100, fmt="png")),
    "pp2_back_pins":         ("popcorn", "image3.png", dict(box=(1300, 520, 2322, 1362), long=1100, fmt="png")),
    "pp3_lower_pins":        ("popcorn", "image4.png", dict(box=(0, 0, 1180, 1093), long=1200, fmt="png")),
    # ---------------- left/right quiz pictures (every printed word blanked) ----------------
    "lr_clavicle_superior":  ("pdfclip", 3, dict(clip=(398, 168, 618, 286), scale=5.0, long=1100, fmt="png", erase=True)),
    "lr_scapula_posterior":  ("pptx", "image4.jpeg", dict(box=(296, 0, 500, 288), up=4, long=1000, erase=True)),
    "lr_humerus_anterior":   ("pdfclip", 5, dict(clip=(334, 116, 500, 500), scale=5.0, long=1100, fmt="png", erase=True)),
    "lr_forearm_anterior":   ("pptx", "image7.png", dict(box=(150, 0, 385, 552), up=3, long=1100, fmt="png", erase=True)),
    "lr_hip_lateral":        ("manual", 184, dict(box=(420, 460, 3320, 3080), long=1100, trim="dark", erase=True)),
    "lr_femur_posterior":    ("manual", 185, dict(box=(2290, 2920, 3470, 6120), long=1100, trim="dark", erase=True, paint=[(0.84, 0.06, 0.99, 0.15)])),
    "lr_tibia_fibula":       ("pdfclip", 13, dict(clip=(372, 130, 766, 494), scale=4.0, long=1100, fmt="png", erase=True)),
    # mirrored twins: a mirrored right bone IS a left bone, so each drawing exists both ways
    # and the left/right cards can't be answered by recognising the drawing
    "lr_clavicle_superior_mirror": ("derived", "lr_clavicle_superior.png", dict(mirror=True, fmt="png")),
    "lr_scapula_posterior_mirror": ("derived", "lr_scapula_posterior.jpg", dict(mirror=True)),
    "lr_humerus_anterior_mirror":  ("derived", "lr_humerus_anterior.png", dict(mirror=True, fmt="png")),
    "lr_forearm_anterior_mirror":  ("derived", "lr_forearm_anterior.png", dict(mirror=True, fmt="png")),
    "lr_hip_lateral_mirror":       ("derived", "lr_hip_lateral.jpg", dict(mirror=True)),
    "lr_femur_posterior_mirror":   ("derived", "lr_femur_posterior.jpg", dict(mirror=True)),
    "lr_tibia_fibula_mirror":      ("derived", "lr_tibia_fibula.png", dict(mirror=True, fmt="png")),
}


def corner_colour(im):
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    px = [im.getpixel(p) for p in pts]
    return tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))


def ring_colour(im, px=6):
    """Median colour of the outermost ring — what a matte should continue."""
    a = np.asarray(im.convert("RGB"))
    ring = np.concatenate([a[:px].reshape(-1, 3), a[-px:].reshape(-1, 3),
                           a[:, :px].reshape(-1, 3), a[:, -px:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(ring, axis=0))


def trim(im, mode=True, fuzz=28):
    """Crop to content. mode="dark" keeps the black photo panel and trims the PAGE (and any
    caption) around it: a row/column belongs to the panel when most of its pixels are dark."""
    if mode == "dark":
        g = np.asarray(im.convert("L")) < 90
        rows = np.where(g.mean(axis=1) > 0.55)[0]
        cols = np.where(g.mean(axis=0) > 0.55)[0]
        if len(rows) and len(cols):
            return im.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1))
        return im
    bg = Image.new("RGB", im.size, corner_colour(im))
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > fuzz else 0)
    box = diff.getbbox()
    return im.crop(box) if box else im


def whiten(im, floor=196, spread=34):
    """Flatten a scanned page's grey paper to white; coloured labels and line art untouched."""
    a = np.asarray(im).astype(int)
    mn, mx = a.min(axis=2), a.max(axis=2)
    paper = (mn > floor) & ((mx - mn) < spread)
    a[paper] = 255
    return Image.fromarray(a.astype("uint8"))


def _edge(band, axis, n):
    """Robust colour profile along one side of a box: median ACROSS the band (so a 1-2 px
    leader line crossing it is outvoted), then a running median ALONG it."""
    prof = np.median(band, axis=axis)                     # (n, 3)
    k = 7
    padded = np.pad(prof, ((k // 2, k // 2), (0, 0)), mode="edge")
    win = np.lib.stride_tricks.sliding_window_view(padded, k, axis=0)   # (n, 3, k)
    return np.median(win, axis=2)[:n]


def fill_box(a, box):
    """Fill `box` from the pixels around it. A flat background (white page, black photo
    panel) gets its median colour; a shaded one (a word printed ON the bone) gets a smooth
    left-right / top-bottom blend of robust edge profiles, so neither a flat patch nor a
    smeared leader line is left behind."""
    h, w = a.shape[:2]
    x0, y0, x1, y1 = box
    b = 5
    ring = np.concatenate([a[max(0, y0 - b):y0, x0:x1].reshape(-1, 3), a[y1:min(h, y1 + b), x0:x1].reshape(-1, 3),
                           a[y0:y1, max(0, x0 - b):x0].reshape(-1, 3), a[y0:y1, x1:min(w, x1 + b)].reshape(-1, 3)])
    if len(ring) == 0:
        return
    med = np.median(ring, axis=0)
    spread = np.median(np.abs(ring - med), axis=0).max()
    if spread < 6 or min(x0, y0) < b or x1 + b > w or y1 + b > h:
        a[y0:y1, x0:x1] = med
        return
    L = _edge(a[y0:y1, x0 - b:x0], 1, y1 - y0)[:, None, :]
    R = _edge(a[y0:y1, x1:x1 + b], 1, y1 - y0)[:, None, :]
    T = _edge(a[y0 - b:y0, x0:x1], 0, x1 - x0)[None, :, :]
    B = _edge(a[y1:y1 + b, x0:x1], 0, x1 - x0)[None, :, :]
    xs = np.linspace(0, 1, x1 - x0)[None, :, None]
    ys = np.linspace(0, 1, y1 - y0)[:, None, None]
    a[y0:y1, x0:x1] = ((L * (1 - xs) + R * xs) + (T * (1 - ys) + B * ys)) / 2


def erase_words(im, name):
    """Blank every word Vision can read (see fill_box for how the hole is filled)."""
    tmp = os.path.join(CACHE, f"_erase_{name}.png")
    im.save(tmp)
    words = ocr.words(tmp, upscale=2.0)
    a = np.asarray(im.convert("RGB")).astype(float).copy()
    h, w = a.shape[:2]
    for wd in words:
        hgt = wd["y1"] - wd["y0"]
        pad = 0.25 * hgt + 3
        box = (max(0, int(wd["x0"] - pad)), max(0, int(wd["y0"] - pad)),
               min(w, int(wd["x1"] + pad)), min(h, int(wd["y1"] + pad)))
        if box[2] > box[0] and box[3] > box[1]:
            fill_box(a, box)
    os.unlink(tmp)
    return Image.fromarray(a.clip(0, 255).astype("uint8")), len(words)


def mat(im, frac=PAD, colour=None):
    w, h = im.size
    p = max(8, round(max(w, h) * frac))
    out = Image.new("RGB", (w + 2 * p, h + 2 * p), colour or ring_colour(im))
    out.paste(im, (p, p))
    return out


def load(kind, src, o):
    if kind == "pptx":                     # the slide's own picture, WITHOUT its overlays
        im = Image.open(os.path.join(CACHE, "pptx_media", src)).convert("RGB")
        im = im.crop(o["box"]) if o.get("box") else im
        if o.get("up"):                    # tiny source: enlarge BEFORE OCR so every word reads
            im = im.resize((im.width * o["up"], im.height * o["up"]), Image.LANCZOS)
        return im
    if kind == "popcorn":
        im = Image.open(os.path.join(CACHE, "popcorn_media", src)).convert("RGB")
        return im.crop(o["box"]) if o.get("box") else im
    if kind == "pdfclip":
        page = fitz.open(SLIDES_PDF)[src - 1]
        s = o.get("scale", 3)
        pm = page.get_pixmap(matrix=fitz.Matrix(s, s), clip=fitz.Rect(*o["clip"]), alpha=False)
        return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    if kind == "manual":
        page = fitz.open(MANUAL_PDF)[src - 1]
        x0, y0, x1, y1 = o["box"]
        k = 72.0 / 600.0
        pm = page.get_pixmap(dpi=600, clip=fitz.Rect(x0 * k, y0 * k, x1 * k, y1 * k), alpha=False)
        return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    raise ValueError(kind)


def build(name):
    kind, src, o = SPEC[name]
    if kind == "derived":                     # an already-built figure, mirrored as-is
        from PIL import ImageOps
        im = Image.open(os.path.join(OUT, src)).convert("RGB")
        im = ImageOps.mirror(im) if o.get("mirror") else im
        fmt = o.get("fmt", "jpg")
        path = os.path.join(OUT, f"{name}.{fmt}")
        im.save(path, **({"optimize": True} if fmt == "png" else {"quality": 92, "optimize": True}))
        return dict(name=name, file=os.path.basename(path), kind=kind, source=src,
                    native=list(im.size), out=list(im.size), scale=1.0,
                    bytes=os.path.getsize(path), erased_words=None)
    im = load(kind, src, o)
    native = im.size
    if o.get("whiten"):
        im = whiten(im)
    t = o.get("trim", True)
    if t:
        im = trim(im, t)
    erased = None
    if o.get("erase"):
        im, erased = erase_words(im, name)
    if o.get("paint"):                     # leftovers OCR could not read (fractions of the image)
        a = np.asarray(im.convert("RGB")).astype(float).copy()
        h, w = a.shape[:2]
        for (x0, y0, x1, y1) in o["paint"]:
            fill_box(a, (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
        im = Image.fromarray(a.clip(0, 255).astype("uint8"))
    long_edge = o.get("long", BACK)
    w, h = im.size
    s = long_edge / max(w, h)
    if abs(s - 1) > 0.02:
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    im = mat(im)
    fmt = o.get("fmt", "jpg")
    path = os.path.join(OUT, f"{name}.{fmt}")
    if fmt == "png":
        im.save(path, optimize=True)
    else:
        im.save(path, quality=92, optimize=True)
    return dict(name=name, file=os.path.basename(path), kind=kind, source=src,
                native=list(native), out=list(im.size), scale=round(s, 3),
                bytes=os.path.getsize(path), erased_words=erased)


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(SPEC)
    man_path = os.path.join(W, "figures_manifest.json")
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {}
    for n in names:
        r = build(n)
        manifest[n] = r
        print(f"{n:24s} {r['kind']:8s} native {r['native'][0]}x{r['native'][1]} -> "
              f"{r['out'][0]}x{r['out'][1]} (x{r['scale']}) {r['bytes'] // 1024} KB"
              + (f"  erased {r['erased_words']} words" if r['erased_words'] is not None else ""))
    json.dump(manifest, open(man_path, "w"), indent=1)


if __name__ == "__main__":
    main()
