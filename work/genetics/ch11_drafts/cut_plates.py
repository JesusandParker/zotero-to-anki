"""Cut chapter 11's plates as COMPLETE figures (art + caption) from 450-dpi PyMuPDF renders.
Boxes were measured by eye on 100-dpi PyMuPDF page renders (CropBox-relative), so px*0.72 = pt
in the same space page.get_pixmap(clip=...) uses (R64: never scale a pdftoppm pixel)."""
import fitz, json, os, sys
sys.path.insert(0, 'scripts')
from PIL import Image
import build_figure_index as B

PDF = "/Users/parkerregner/Zotero/storage/4JYSPKBJ/02_GENETICS Textbook - Principles of Genetics 7e By D. Peter Snustad Michael J. Simmons (1).pdf"
BASE = "work/genetics"
FULL = os.path.join(BASE, "figures/full"); STUDY = os.path.join(BASE, "figures/study_v2")
os.makedirs(FULL, exist_ok=True); os.makedirs(STUDY, exist_ok=True)
DPI = 450
# label -> list of (page, box_px100) parts stacked top-to-bottom
PLATES = {
 "FIGURE 11.1":  [(275, (420, 475, 890, 1045))],
 "FIGURE 11.2":  [(276, (245, 65, 835, 885))],
 "FIGURE 11.3":  [(278, (130, 65, 835, 1035))],
 "FIGURE 11.4":  [(279, (540, 70, 885, 385))],
 "FIGURE 11.7":  [(281, (515, 570, 885, 1045))],
 "FIGURE 11.8":  [(282, (45, 70, 370, 360))],
 "FIGURE 11.9":  [(282, (45, 520, 370, 1045))],
 "FIGURE 11.10": [(283, (360, 70, 885, 1045)), (283, (95, 825, 355, 1040))],
 "FIGURE 11.11": [(284, (160, 700, 830, 1040))],
 "FIGURE 11.12": [(286, (45, 70, 565, 663)), (286, (45, 665, 305, 715))],
 "TABLE 11.1":   [(286, (325, 840, 830, 1052))],
 "FIGURE 11.13": [(287, (95, 775, 605, 1052))],
 "FIGURE 11.14": [(288, (45, 70, 375, 970))],
 "FIGURE 11.16": [(289, (515, 560, 885, 1048))],
 "FIGURE 11.17": [(290, (45, 70, 400, 420)), (290, (398, 75, 835, 142))],
 "FIGURE 11.18": [(291, (520, 70, 885, 500))],
 "FIGURE 11.20": [(294, (45, 655, 385, 1052))],
 "FIGURE 11.21": [(295, (250, 335, 885, 745)), (295, (608, 745, 885, 982))],
 "FIGURE 11.22": [(296, (45, 70, 460, 825))],
}
doc = fitz.open(PDF)
import sys as _s
ONLY=_s.argv[1:]
if ONLY: PLATES={k:v for k,v in PLATES.items() if k in ONLY}
def render(page_no, box):
    x0,y0,x1,y1 = [v*0.72 for v in box]
    pg = doc[page_no-1]
    pix = pg.get_pixmap(clip=fitz.Rect(x0,y0,x1,y1), dpi=DPI, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
def trim(im, thresh=245):
    g = im.convert("L").point(lambda v: 0 if v > thresh else 255)
    bb = g.getbbox()
    return im.crop(bb) if bb else im
manifest = []
for label, parts in PLATES.items():
    ims = [trim(render(p, b)) for p, b in parts]
    if len(ims) == 1:
        out = ims[0]
    else:
        gap = 40
        W = max(i.width for i in ims); H = sum(i.height for i in ims) + gap*(len(ims)-1)
        out = Image.new("RGB", (W, H), "white")
        y = 0
        for i in ims:
            out.paste(i, (0, y)); y += i.height + gap
    fname = label.replace(" ", "_").replace(".", "_") + ".png"
    full_path = os.path.join(FULL, fname)
    out.save(full_path, optimize=True)
    study = B.study_copy(full_path, STUDY, pad_pct=4.0, lossless=True)
    sz = Image.open(study).size if study else None
    manifest.append({"label": label, "parts": [{"page": p, "box_px100": b} for p, b in parts],
                     "full_file": os.path.relpath(full_path, BASE), "study_file": os.path.relpath(study, BASE) if study else None,
                     "study_px": sz, "dpi": DPI, "date": "2026-09-19", "kind": "line-art" if label != "FIGURE 11.11" else "photo"})
    print(f"{label:14s} full={out.size} study={sz} -> {study}")
mp=os.path.join(BASE, "figures/crops_manifest_ch11.json")
old=json.load(open(mp)) if os.path.exists(mp) else []
new={m["label"]:m for m in old}
for m in manifest: new[m["label"]]=m
json.dump(list(new.values()), open(mp,"w"), indent=1)
print("manifest written")
