#!/usr/bin/env python3
"""
render_page.py — render a single textbook page to a PNG.

Used for highlights whose fact lives inside a TABLE or FIGURE (e.g. the hazmat
placard diagram, vital-signs-by-age tables), where plain text extraction is
insufficient and the card-writer needs to SEE the page to author the card.

Usage:
    python3 render_page.py 198            # writes <skill>/work/page_198.png
    python3 render_page.py 198 --out /tmp/p198.png
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
PDF = "/Users/parkerregner/Zotero/storage/Z98PW7AT/Pollak et al. - 2021 - Emergency care and transportation of the sick and injured.pdf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", type=int, help="physical page number (== pageLabel in this book)")
    ap.add_argument("--out", help="output PNG path")
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()

    out = args.out or os.path.join(SKILL, "work", f"page_{args.page}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prefix = out[:-4] if out.lower().endswith(".png") else out
    subprocess.run(
        ["pdftoppm", "-f", str(args.page), "-l", str(args.page),
         "-r", str(args.dpi), "-png", "-singlefile", PDF, prefix],
        check=True,
    )
    print(out)


if __name__ == "__main__":
    main()
