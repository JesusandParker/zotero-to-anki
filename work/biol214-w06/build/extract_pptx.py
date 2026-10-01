#!/usr/bin/env python3
"""
extract_pptx.py — the W06 Appendicular Skeleton .pptx, verbatim: every slide's text, its
speaker notes, its hidden flag and the pictures it uses (-> ../source_slides.md), plus
every embedded picture copied out at original resolution (-> ../cache/pptx_media).
"""
import html, os, re, shutil, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
PPTX = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/"
                          "01_Liberty University /2026 - 2027 Year/Human Anatomy and Physiology I Lab/"
                          "08_Week 6 - Appendicular Skeleton/04_B214 05 Appendicular Skeleton 2026.pptx")


def paras(xml):
    out = []
    for p in re.findall(r"<a:p\b.*?</a:p>", xml, re.S):
        t = "".join(re.findall(r"<a:t>([^<]*)</a:t>", p))
        t = html.unescape(t).strip()
        if t:
            out.append(t)
    return out


def main():
    z = zipfile.ZipFile(PPTX)
    pres = z.read("ppt/presentation.xml").decode()
    rels = z.read("ppt/_rels/presentation.xml.rels").decode()
    rid2t = {}
    for rel in re.findall(r"<Relationship\b[^>]*/>", rels):
        i = re.search(r'Id="([^"]+)"', rel).group(1)
        t = re.search(r'Target="([^"]+)"', rel).group(1)
        rid2t[i] = t
    order = ["ppt/" + rid2t[i] for i in re.findall(r'<p:sldId [^>]*r:id="([^"]+)"', pres)]
    md = ["# BIOL 214 W06 — The Appendicular Skeleton: slide text + speaker notes (verbatim)", ""]
    for n, s in enumerate(order, 1):
        x = z.read(s).decode("utf8")
        hidden = ' show="0"' in x[:400]
        rel = s.replace("slides/", "slides/_rels/") + ".rels"
        media, notes = [], []
        if rel in z.namelist():
            r = z.read(rel).decode()
            media = re.findall(r'Target="\.\./media/([^"]+)"', r)
            nt = re.findall(r'Target="\.\./notesSlides/([^"]+)"', r)
            if nt:
                notes = paras(z.read("ppt/notesSlides/" + nt[0]).decode("utf8"))
                notes = [p for p in notes if not re.fullmatch(r"\d+", p)]   # slide-number field
        md.append(f"## Slide {n}" + ("  (HIDDEN)" if hidden else ""))
        for p in paras(x):
            md.append(f"- {p}")
        if media:
            md.append(f"  MEDIA: {', '.join(media)}")
        if notes:
            md.append("  SPEAKER NOTES:")
            md += [f"  > {p}" for p in notes]
        md.append("")
    open(os.path.join(W, "source_slides.md"), "w").write("\n".join(md))
    dst = os.path.join(W, "cache", "pptx_media")
    os.makedirs(dst, exist_ok=True)
    k = 0
    for m in z.namelist():
        if m.startswith("ppt/media/"):
            with z.open(m) as f, open(os.path.join(dst, os.path.basename(m)), "wb") as g:
                shutil.copyfileobj(f, g)
            k += 1
    print(f"{len(order)} slides -> source_slides.md; {k} media files -> cache/pptx_media")


if __name__ == "__main__":
    main()
