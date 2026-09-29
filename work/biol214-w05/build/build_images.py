#!/usr/bin/env python3
"""
build_images.py — every picture the BIOL 214 W05 (axial skeleton) deck uses, built from the
original sources at the best resolution each one offers.

Sources, in order of preference:
  * pptx   — the slide's own embedded image, straight out of the .pptx (original pixels;
             the Zotero PDF re-encodes PNGs as JPEG)
  * pdfclip— a region of the Zotero slide PDF rendered at high DPI, used ONLY where the
             labels are PowerPoint text laid over a picture (slides 10, 11, 15), so the
             vector labels come out crisp
  * manual — a 600-dpi crop of the lab manual scan (the photos of the actual lab models)
  * popcorn— the Popcorn Points game images (numbered pins, instructor answer key in notes)

Every output is trimmed to its content, scaled to a common long edge, and MATTED at 4% of
that edge in the plate's own corner colour (parker-preferences: "a little bit of space").

Run:  ~/.claude/skills/zotero-to-anki/.venv/bin/python build_images.py [name ...]
"""
import os, sys, json
import fitz
from PIL import Image, ImageChops, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)                      # work/biol214-w05
CACHE = os.path.join(W, "cache")
OUT = os.path.join(W, "figures")
SLIDES_PDF = os.path.expanduser("~/Zotero/storage/GU75PZ5A/B214 04 Axial Skeleton 2026.pdf")
MANUAL_PDF = os.path.expanduser("~/Zotero/storage/6K6XWXMN/Anatomy & Physiology BIOL 214 "
                                "Laboratory Manual (600 dpi, searchable).pdf")
POPCORN_PDF = os.path.join(CACHE, "popcorn.pdf")

IO = 1600      # long edge for image-occlusion plates (they fill the card)
BACK = 1300    # long edge for back-of-card pictures
PAD = 0.04     # matte, fraction of the long edge

# name -> (kind, source, options)
#   box   : crop box in SOURCE pixels (pptx/popcorn) or 600-dpi page pixels (manual)
#   clip  : crop box in PDF points (pdfclip)
#   trim  : auto-trim uniform border after cropping (default True)
#   long  : output long edge
#   fmt   : "png" | "jpg"
SPEC = {
    # ---------------- slides: bone basics ----------------
    "s02_bone_classes":      ("pptx", "image1.jpeg", dict(frac=(0, .11184, 0, .07268), long=1000)),
    "s03_long_bone":         ("pptx", "image2.jpeg", dict(frac=(.052, 0, .57335, .04197), long=IO)),
    "s04_compact_bone":      ("pptx", "image3.jpeg", dict(long=IO)),
    "s05_marrow_section":    ("pptx", "image4.jpeg", dict(long=IO)),
    "s06_epiphyseal_plate":  ("pptx", "image5.jpeg", dict(long=BACK, trim=False)),
    "s07_knee":              ("pptx", "image6.jpeg", dict(long=1000)),
    "s07_disc":              ("pptx", "image7.jpeg", dict(long=IO)),
    "s07_hyaline":           ("pptx", "image8.jpeg", dict(frac=(0, 0, 0, .12886), long=1000, trim=False, mat_colour=(255, 255, 255))),
    "s08_axial_appendicular":("pptx", "image9.jpeg", dict(long=1100)),
    # ---------------- slides: skull ----------------
    "s10_cranial_bones":     ("pdfclip", 10, dict(clip=(86, 128, 706, 462), scale=3.6, long=IO, fmt="png", unpink=(0.80, 0.70, 1, 1))),
    "s11_facial_bones":      ("pdfclip", 11, dict(clip=(40, 118, 728, 460), scale=3.6, long=IO, fmt="png", unpink=(0.80, 0.70, 1, 1))),
    "s12_cranial_foramina":  ("pptx", "image14.png", dict(frac=(0, 0, .12291, 0), long=IO, fmt="png")),
    "s13_hyoid":             ("pptx", "image15.jpeg", dict(long=IO)),
    # ---------------- slides: vertebral column ----------------
    "s14_spine_regions":     ("pptx", "image17.jpeg", dict(long=1400)),
    "s14_typical_vertebra":  ("pptx", "image16.gif", dict(long=IO, fmt="png")),
    "s15_atlas_axis":        ("pptx", "image18.jpeg", dict(long=IO)),
    "s15_cervical_superior": ("pptx", "image20.png", dict(long=1000, fmt="png", trim=False)),
    "s15_cervical_labeled":  ("pdfclip", 15, dict(clip=(372, 322, 772, 518), scale=5.0, long=IO, fmt="png", unpink=(0.62, 0.30, 1, 1))),
    "s16_thoracic":          ("pptx", "image21.png", dict(long=IO, fmt="png")),
    "s17_lumbar_photo":      ("pptx", "image22.jpeg", dict(long=1000, trim=False)),
    "s17_lumbar_superior":   ("pptx", "image23.jpeg", dict(long=IO)),
    "s18_sacrum_coccyx":     ("pptx", "image24.jpeg", dict(frac=(.10436, .11467, 0, 0), long=IO)),
    "s19_abnormal_curves":   ("pptx", "image25.png", dict(long=BACK, fmt="png")),
    "s20_sternum":           ("pptx", "image26.jpeg", dict(long=1100)),
    "s20_rib":               ("pptx", "image27.png", dict(box=(0, 0, 534, 460), long=IO, fmt="png")),
    # ---------------- lab manual (600-dpi scan; PDF page numbers) ----------------
    "m6_01_axial_appendicular": ("manual", 140, dict(box=(460, 3290, 4600, 5930), long=BACK, whiten=True)),
    "m6_03_bone_markings":   ("manual", 142, dict(box=(540, 460, 4420, 6010), long=BACK, whiten=True)),
    "m6_04_long_bone_model": ("manual", 144, dict(box=(460, 460, 2290, 3285), long=IO)),
    "m6_05_bone_tissue_400x":("manual", 144, dict(box=(2560, 330, 4560, 1990), long=BACK)),
    "m6_06_compact_bone":    ("manual", 144, dict(box=(2510, 4480, 4710, 6100), long=BACK, whiten=True)),
    "m6_07_gross_bone":      ("manual", 145, dict(box=(450, 3480, 3740, 5950), long=BACK, whiten=True)),
    "m6_08_tibia_forces":    ("manual", 146, dict(box=(1150, 470, 3980, 3360), long=BACK, whiten=True)),
    "m6_09_growth_plate":    ("manual", 147, dict(box=(140, 650, 4340, 2930), long=BACK, whiten=True)),
    "m6_12_cartilages":      ("manual", 149, dict(box=(320, 500, 4380, 3440), long=BACK, whiten=True)),
    "m7_01_axial_skeleton":  ("manual", 162, dict(box=(2670, 640, 4660, 3260), long=BACK, whiten=True)),
    "m7_02a_skull_post_lat": ("manual", 163, dict(box=(60, 800, 4440, 3235), long=IO, trim="dark")),
    "m7_02b_skull_obl_ant":  ("manual", 163, dict(box=(60, 3305, 4440, 5655), long=IO, trim="dark")),
    "m7_03_skull_inferior":  ("manual", 164, dict(box=(490, 3020, 4730, 5620), long=IO, trim="dark", paint=[(0.12, 0.0, 0.25, 0.035)])),
    "m7_04_cranial_floor":   ("manual", 165, dict(box=(230, 560, 4540, 3190), long=IO, trim="dark")),
    "m7_05_mandible":        ("manual", 165, dict(box=(2300, 4560, 4680, 5920), long=IO, trim="dark")),
    "m7_06_hyoid":           ("manual", 166, dict(box=(420, 500, 2365, 1750), long=BACK, trim="dark")),
    "m7_07_sinuses":         ("manual", 166, dict(box=(2510, 470, 4660, 3610), long=IO, trim="dark")),
    "m7_08_spinal_curves":   ("manual", 167, dict(box=(200, 470, 4660, 3085), long=BACK)),
    "m7_09_abnormal_curves": ("manual", 167, dict(box=(2300, 4790, 4600, 6010), long=BACK, whiten=True)),
    "m7_10_cervical_model":  ("manual", 168, dict(box=(2510, 440, 4630, 1960), long=IO, trim="dark")),
    "m7_11_atlas_axis_model":("manual", 168, dict(box=(500, 3520, 4660, 6100), long=IO, trim="dark")),
    "m7_12_thoracic_model":  ("manual", 169, dict(box=(2360, 500, 4400, 2360), long=BACK, trim="dark")),
    "m7_13_vertebra_regions":("manual", 169, dict(box=(2360, 3710, 4600, 6100), long=BACK, trim="dark")),
    "m7_14_giraffe_moose":   ("manual", 169, dict(box=(200, 470, 2080, 2050), long=BACK, trim="dark")),
    "m7_14_thoracic_side":   ("manual", 169, dict(box=(1090, 490, 2075, 1265), long=1000, trim="dark")),
    "m7_14_lumbar_side":     ("manual", 169, dict(box=(1090, 1285, 2075, 2045), long=1000, trim="dark")),
    "m7_14_giraffe_row":     ("manual", 169, dict(box=(200, 470, 2080, 1268), long=1100, trim="dark")),
    "m7_14_moose_row":       ("manual", 169, dict(box=(200, 1282, 2080, 2050), long=1100, trim="dark")),
    "m7_15_sacrum_photos":   ("manual", 170, dict(box=(2540, 470, 4680, 6010), long=BACK, trim="dark")),
    "m7_16_sternum_model":   ("manual", 172, dict(box=(620, 500, 4720, 3280), long=BACK, trim="dark")),
    "m7_17_rib_model":       ("manual", 172, dict(box=(440, 4070, 2440, 5410), long=BACK, trim="dark")),
    "m7_17_thoracic_cage":   ("manual", 172, dict(box=(2690, 3500, 4660, 5950), long=IO, trim="dark")),
    # ---------------- Popcorn Points game (instructor key in the slide notes) -----------
    "pp3_lower_trunk":       ("popcorn", "image4.png", dict(long=IO, fmt="png")),
    "pp7_vertebrae_abc":     ("popcorn", "image8.jpg", dict(long=BACK)),
    "pp7_a_thoracic":        ("popcorn", "image8.jpg", dict(box=(8, 20, 636, 488), long=1000)),
    "pp7_b_lumbar":          ("popcorn", "image8.jpg", dict(box=(660, 60, 1270, 444), long=1000)),
    "pp7_c_cervical":        ("popcorn", "image8.jpg", dict(box=(468, 508, 988, 1100), long=1000)),
    "pp3_front_trunk":       ("popcorn", "image4.png", dict(box=(0, 0, 1161, 1093), long=1200, fmt="png")),
    "s08_rib_counts":        ("pdfclip", 8, dict(clip=(128, 232, 352, 352), scale=4.0, long=900, fmt="png")),
    "s20_rib_groups":        ("pdfclip", 20, dict(clip=(384, 106, 724, 212), scale=4.0, long=1100, fmt="png")),
}


import numpy as np


def corner_colour(im):
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    px = [im.getpixel(p) for p in pts]
    # the most common-ish corner (median per channel)
    return tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))


def ring_colour(im, px=6):
    """Median colour of the outermost ring — what a matte should continue."""
    a = np.asarray(im.convert("RGB"))
    ring = np.concatenate([a[:px].reshape(-1, 3), a[-px:].reshape(-1, 3),
                           a[:, :px].reshape(-1, 3), a[:, -px:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(ring, axis=0))


def trim(im, mode=True, fuzz=28):
    """Crop to content: everything that differs from the border colour by > fuzz.
    mode="dark" keeps the black photo panel and trims the PAGE (and any caption) around
    it: a row/column belongs to the panel when most of its pixels are dark, so a line of
    caption text below the panel can never stretch the box the way a plain bbox would."""
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


def unpink(im, region):
    """Erase the slide template's magenta decoration lines inside `region` (fractions)."""
    a = np.asarray(im).copy()
    h, w = a.shape[:2]
    x0, y0, x1, y1 = (int(region[0] * w), int(region[1] * h), int(region[2] * w), int(region[3] * h))
    sub = a[y0:y1, x0:x1].astype(int)
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    pink = ((r - g > 35) & (b - g > 5) & (r > 140)) | ((r - g > 10) & (b >= g) & (r > 185))
    sub[pink] = 255
    a[y0:y1, x0:x1] = sub
    return Image.fromarray(a.astype("uint8"))


def whiten(im, floor=196, spread=34):
    """Flatten a scanned page's grey paper (and faint reverse-side bleed) to white.
    Only near-neutral light pixels move, so coloured labels and line art are untouched."""
    a = np.asarray(im).astype(int)
    mn, mx = a.min(axis=2), a.max(axis=2)
    paper = (mn > floor) & ((mx - mn) < spread)
    a[paper] = 255
    return Image.fromarray(a.astype("uint8"))


def paint(im, boxes):
    """Fill stray fragments (a neighbouring figure's label) with the local background."""
    im = im.copy()
    w, h = im.size
    for (x0, y0, x1, y1) in boxes:
        box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        c = ring_colour(im.crop((max(0, box[0] - 6), max(0, box[1] - 6),
                                 min(w, box[2] + 6), min(h, box[3] + 6))), px=4)
        im.paste(c, box)
    return im


def mat(im, frac=PAD, colour=None):
    w, h = im.size
    p = max(8, round(max(w, h) * frac))
    out = Image.new("RGB", (w + 2 * p, h + 2 * p), colour or ring_colour(im))
    out.paste(im, (p, p))
    return out


def load(kind, src, o):
    if kind == "pptx":
        im = Image.open(os.path.join(CACHE, "pptx_media", src))
        im = im.convert("RGB")
        if o.get("box"):
            im = im.crop(o["box"])
        return im
    if kind == "popcorn":
        im = Image.open(os.path.join(CACHE, "popcorn_media", src)).convert("RGB")
        if o.get("box"):
            im = im.crop(o["box"])
        return im
    if kind == "pdfclip":
        d = fitz.open(SLIDES_PDF)
        page = d[src - 1]
        x0, y0, x1, y1 = o["clip"]
        pm = page.get_pixmap(matrix=fitz.Matrix(o.get("scale", 3), o.get("scale", 3)),
                             clip=fitz.Rect(x0, y0, x1, y1), alpha=False)
        return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    if kind == "manual":
        d = fitz.open(MANUAL_PDF)
        page = d[src - 1]
        x0, y0, x1, y1 = o["box"]              # 600-dpi pixels
        k = 72.0 / 600.0
        pm = page.get_pixmap(dpi=600, clip=fitz.Rect(x0 * k, y0 * k, x1 * k, y1 * k), alpha=False)
        return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    raise ValueError(kind)


def build(name):
    kind, src, o = SPEC[name]
    im = load(kind, src, o)
    if o.get("frac"):                       # PowerPoint <a:srcRect> crop (l, t, r, b)
        l, t_, r, b = o["frac"]
        w, h = im.size
        im = im.crop((round(l * w), round(t_ * h), round(w - r * w), round(h - b * h)))
    native = im.size
    if o.get("unpink"):
        im = unpink(im, o["unpink"])
    if o.get("whiten"):
        im = whiten(im)
    t = o.get("trim", True)
    if t:
        im = trim(im, t)
    if o.get("paint"):
        im = paint(im, o["paint"])
    long_edge = o.get("long", BACK)
    w, h = im.size
    s = long_edge / max(w, h)
    if abs(s - 1) > 0.02:
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    im = mat(im, colour=o.get("mat_colour"))
    fmt = o.get("fmt", "jpg")
    path = os.path.join(OUT, f"{name}.{fmt}")
    if fmt == "png":
        im.save(path, optimize=True)
    else:
        im.save(path, quality=92, optimize=True)
    return dict(name=name, file=os.path.basename(path), kind=kind, source=src,
                native=list(native), out=list(im.size), scale=round(s, 3),
                bytes=os.path.getsize(path))


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(SPEC)
    man_path = os.path.join(W, "figures_manifest.json")
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {}
    for n in names:
        r = build(n)
        manifest[n] = r
        print(f"{n:28s} {r['kind']:8s} native {r['native'][0]}x{r['native'][1]} -> "
              f"{r['out'][0]}x{r['out'][1]} (x{r['scale']}) {r['bytes'] // 1024} KB")
    json.dump(manifest, open(man_path, "w"), indent=1)


if __name__ == "__main__":
    main()
