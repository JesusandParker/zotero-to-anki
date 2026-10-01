#!/usr/bin/env python3
"""
build_io.py — turn io_spec.NOTES into Anki Image Occlusion notes: exact mask rectangles
over each printed label (found by Vision OCR, never hand-placed), plus a preview of every
plate with its masks drawn on, for the mandatory LOOK before anything is written.

Writes  io/io_notes.json   (one object per note: fields + per-card answers)
        io/preview/<id>.png

Fails loudly if any label cannot be found the expected number of times — a missing mask
is a card that silently never exists.
"""
import json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ocr, labels, io_spec  # noqa: E402

W = os.path.dirname(HERE)
FIG = os.path.join(W, "figures")
OUT = os.path.join(W, "io")
PREV = os.path.join(OUT, "preview")
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)


def parse(entry):
    """'Label@x,y' -> (label, (x, y)); ('Label', n) -> [(label, None)] * n."""
    if isinstance(entry, tuple):
        lab, n = entry
        return [(lab, None)] * n
    mb = re.match(r"^#box:(\d+),(\d+),(\d+),(\d+)$", entry)
    if mb:
        return [("#box", tuple(int(v) for v in mb.groups()))]
    m = re.match(r"^(.*)@(\d+),(\d+)$", entry)
    if m:
        return [(m.group(1), (int(m.group(2)), int(m.group(3))))]
    return [(entry, None)]


def groups(masks):
    out = []
    for g in masks:
        items = g if isinstance(g, list) else [g]
        flat = []
        for it in items:
            flat += parse(it)
        out.append(flat)
    return out


def main():
    os.makedirs(PREV, exist_ok=True)
    notes, problems = [], []
    for spec in io_spec.NOTES:
        path = os.path.join(FIG, spec["image"])
        im = Image.open(path).convert("RGB")
        IW, IH = im.size
        words = ocr.words(path, upscale=2.0)
        used = set()
        rects, answers, tboxes = [], [], []
        for gi, grp in enumerate(groups(spec["masks"]), start=1):
            texts = []
            # how many of each identical (label, no-hint) we need in this group
            need = {}
            for lab, hint in grp:
                need[(lab, hint)] = need.get((lab, hint), 0) + 1
            for (lab, hint), n in need.items():
                if lab == "#box":                      # a region drawn by hand, in pixels
                    x0, y0, x1, y1 = hint
                    rects.append((gi, x0, y0, x1, y1))
                    tboxes.append((x0, y0, x1, y1))
                    texts.append("(box)")
                    continue
                hits = labels.find(words, lab, max_hits=n, exclude=used, hint=hint)
                if len(hits) < n:
                    problems.append(f"{spec['id']}: found {len(hits)}/{n} of {lab!r}")
                    continue
                for (x0, y0, x1, y1), chain in hits:
                    # A label that wraps continues at the START of its next line. If the
                    # word it jumps to has another word right before it on that line, the
                    # chain has cut through a neighbouring label: "Ischial" (of "Ischial
                    # body") + "spine" (of "Ischial spine", one line down) once masked both.
                    for a, b in zip(chain, chain[1:]):
                        if b["line"] != a["line"]:
                            hh = b["y1"] - b["y0"]
                            pre = [w for w in words if w["line"] == b["line"]
                                   and w["x1"] <= b["x0"] + 2 and b["x0"] - w["x1"] < 1.2 * hh
                                   and labels.norm(w["t"]) and w not in chain]
                            if pre:
                                problems.append(f"{spec['id']}: {lab!r} wraps onto "
                                                f"{b['t']!r}, which follows {pre[0]['t']!r} "
                                                f"on its line — add an @x,y hint")
                    used |= {id(c) for c in chain}
                    h = float(np.median([c["y1"] - c["y0"] for c in chain]))
                    px, py = 0.18 * h + 2, 0.12 * h + 2
                    X0, Y0 = max(0, x0 - px), max(0, y0 - py)
                    X1, Y1 = min(IW, x1 + px), min(IH, y1 + py)
                    rects.append((gi, X0, Y0, X1, Y1))
                    tboxes.append((x0, y0, x1, y1))
                    texts.append(" ".join(c["t"] for c in chain))
            answers.append({"c": gi, "printed": texts})
        # Tightly stacked labels (a numbered key, a two-line pair) overlap once padded.
        # Split each such pair at the midpoint of the gap between their TEXT boxes, so the
        # masks tile the space instead of one mask covering the edge of its neighbour.
        R = [list(r) for r in rects]
        for i in range(len(R)):
            for j in range(len(R)):
                a, b = R[i], R[j]
                if i >= j or a[0] == b[0]:
                    continue
                if a[3] <= b[1] or b[3] <= a[1] or a[4] <= b[2] or b[4] <= a[2]:
                    continue
                ta, tb = tboxes[i], tboxes[j]
                v_ov = min(ta[3], tb[3]) - max(ta[1], tb[1])
                h_ov = min(ta[2], tb[2]) - max(ta[0], tb[0])
                if v_ov < 0.3 * min(ta[3] - ta[1], tb[3] - tb[1]):   # stacked vertically
                    (top, tt), (bot, tb_) = sorted([(a, ta), (b, tb)], key=lambda z: z[1][1])
                    mid = (tt[3] + tb_[1]) / 2
                    top[4] = min(top[4], mid)
                    bot[2] = max(bot[2], mid)
                elif h_ov < 0.3 * min(ta[2] - ta[0], tb[2] - tb[0]):  # side by side
                    (lft, tl), (rgt, tr) = sorted([(a, ta), (b, tb)], key=lambda z: z[1][0])
                    mid = (tl[2] + tr[0]) / 2
                    lft[3] = min(lft[3], mid)
                    rgt[1] = max(rgt[1], mid)
                else:
                    problems.append(f"{spec['id']}: TEXT of c{a[0]} and c{b[0]} overlaps — "
                                    f"one label was matched onto another's words")
        rects = [tuple(r) for r in R]
        occl = "<br>".join(
            "{{c%d::image-occlusion:rect:left=%.4f:top=%.4f:width=%.4f:height=%.4f:oi=1}}"
            % (g, x0 / IW, y0 / IH, (x1 - x0) / IW, (y1 - y0) / IH)
            for g, x0, y0, x1, y1 in rects)
        notes.append(dict(id=spec["id"], deck=spec["deck"], image=spec["image"],
                          header=spec["header"], back=spec["back"],
                          tags=spec.get("tags", []), occlusion=occl,
                          cards=len(answers), answers=answers, size=[IW, IH]))
        # preview
        pv = im.copy()
        ov = Image.new("RGBA", pv.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for g, x0, y0, x1, y1 in rects:
            d.rectangle([x0, y0, x1, y1], fill=(255, 216, 0, 150), outline=(220, 0, 0, 255), width=3)
            d.text((x0 + 3, y0 + 1), str(g), fill=(180, 0, 0, 255), font=FONT)
        Image.alpha_composite(pv.convert("RGBA"), ov).convert("RGB").save(
            os.path.join(PREV, f"{spec['id']}.jpg"), quality=85)
        print(f"{spec['id']:24s} {len(answers):3d} cards  {len(rects):3d} rects")
    json.dump(notes, open(os.path.join(OUT, "io_notes.json"), "w"), indent=1)
    print(f"\n{len(notes)} IO notes, {sum(n['cards'] for n in notes)} cards")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  " + p)
        sys.exit(1)


if __name__ == "__main__":
    main()
