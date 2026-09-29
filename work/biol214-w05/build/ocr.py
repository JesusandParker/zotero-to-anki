#!/usr/bin/env python3
"""
ocr.py — Apple Vision word boxes for a figure, in the figure's own PIXEL coordinates
(top-left origin), cached by file hash.

Vision reports normalised boxes with a BOTTOM-LEFT origin; everything here converts once,
so no caller ever has to remember that (the flip is the classic bug: masks land a label's
height away from the label).
"""
import hashlib, json, os, subprocess, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.dirname(HERE), "cache", "ocr")
VISION = os.path.expanduser("~/ocr-sandisk/bin/visionocr_words")


def _hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def words(path, upscale=2.0):
    """[{t, x0, y0, x1, y1, line}] for every word Vision reads, in pixels of `path`."""
    os.makedirs(CACHE, exist_ok=True)
    key = f"{os.path.basename(path)}.{_hash(path)}.{upscale}.json"
    cp = os.path.join(CACHE, key)
    if os.path.exists(cp):
        return json.load(open(cp))
    im = Image.open(path).convert("RGB")
    W, H = im.size
    src = path
    tmp = None
    if upscale and upscale != 1:
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        im.resize((round(W * upscale), round(H * upscale)), Image.LANCZOS).save(tmp)
        src = tmp
    out = subprocess.run([VISION, src], capture_output=True, text=True, check=True).stdout
    if tmp:
        os.unlink(tmp)
    data = json.loads(out)
    res = []
    for li, line in enumerate(data.get("lines", [])):
        for w in line.get("words", []):
            x, y, ww, hh = w["x"], w["y"], w["w"], w["h"]
            res.append(dict(t=w["t"], line=li,
                            x0=x * W, x1=(x + ww) * W,
                            y0=(1 - (y + hh)) * H, y1=(1 - y) * H))
    json.dump(res, open(cp, "w"))
    return res
