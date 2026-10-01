#!/usr/bin/env python3
"""sheet.py OUT.jpg img1 img2 ... — a labelled contact sheet (3 per row) for eyeballing."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
out, files = sys.argv[1], sys.argv[2:]
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
cell, cols = 640, 3
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cell * cols, (cell + 34) * rows), "white")
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB"); im.thumbnail((cell - 10, cell - 10))
    x, y = (i % cols) * cell, (i // cols) * (cell + 34)
    sheet.paste(im, (x + 5, y + 34))
    ImageDraw.Draw(sheet).text((x + 6, y + 4), os.path.basename(f), fill="red", font=font)
sheet.save(out, quality=85)
