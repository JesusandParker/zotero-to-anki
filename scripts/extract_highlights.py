#!/usr/bin/env python3
"""
extract_highlights.py — Stage 1 of the EMT card pipeline.

Pulls Parker's YELLOW (#ffd400) highlights from the EMT textbook in Zotero for a
given chapter, grounds each one in its surrounding page paragraph, and emits a
clean JSON work-file the card-writer reads.

READ-ONLY against Zotero: it copies the live DB and reads the copy in immutable
mode; it never touches the original DB or PDF.

Usage:
    python3 extract_highlights.py --chapter 1
    python3 extract_highlights.py --chapter 1 --out /path/to/ch1.json
    python3 extract_highlights.py --all
"""
import argparse, json, os, re, shutil, sqlite3, subprocess, sys, tempfile, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
ZOTERO_DB = os.path.expanduser("~/Zotero/zotero.sqlite")
PDF = "/Users/parkerregner/Zotero/storage/Z98PW7AT/Pollak et al. - 2021 - Emergency care and transportation of the sick and injured.pdf"
# Yellow = "make a card". Parker highlighted Ch1-7 in green under the old scheme,
# then switched to yellow around p526; on 2026-07-29 the whole book was normalized
# so yellow = memorize and blue = everything else. Both palette yellows are matched
# (#ffd400 is Zotero's own; #facd5a is the alternate palette from externally
# annotated PDFs). Any other color, blue included, is deliberately ignored.
YELLOW = ("#ffd400", "#facd5a")
CHAPTER_MAP = os.path.join(SKILL, "reference", "chapter_pages.json")
CTX_CHARS = 450  # paragraph context grabbed on each side of the highlight
# A list lead-in (a highlight that introduces an enumerated list, e.g. "...consider
# the following factors:") needs MUCH more forward context, or the list gets cut off
# mid-enumeration and the card-writer completes it from memory (ungrounded) or
# undercounts. This bit Ch3 card 4: the 450-char window caught only 4 of 8
# decision-making-capacity factors. When we detect a lead-in, grab the whole list.
LIST_FWD_CHARS = 1700
LIST_LEADIN = re.compile(r"(:\s*$|\bfollowing\b|\binclude[sd]?\b|\bare[:]?\s*$|\bconsider\b)", re.I)


def norm(s):
    """Normalize text so highlight (DB) and page (pdftotext) can be matched."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("−", "-")
    s = s.replace("­", "")          # soft hyphen
    s = s.replace(" ", " ")         # nbsp
    s = re.sub(r"-\s*\n\s*", "", s)      # de-hyphenate across line breaks
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def norm_loose(s):
    s = norm(s).lower()
    return re.sub(r"\s*-\s*", "-", s)


def resolve_attachment(cur):
    # Must be the Pollak PDF we also extract page text from (NOT the epub copies,
    # NOT the other emergency-care PDF). Path LIKE 'Pollak%.pdf' isolates it.
    cur.execute("SELECT itemID FROM itemAttachments WHERE path LIKE '%Pollak%' AND path LIKE '%.pdf' LIMIT 1")
    row = cur.fetchone()
    if row:
        return row[0]
    # fallback: whichever attachment actually holds the most yellow annotations
    cur.execute(
        "SELECT parentItemID FROM itemAnnotations WHERE type=1 AND color IN (?,?) "
        "GROUP BY parentItemID ORDER BY COUNT(*) DESC LIMIT 1", YELLOW)
    row = cur.fetchone()
    return row[0] if row else 2459  # known fallback (attachment key Z98PW7AT)


def page_text(page_label):
    """pdftotext -layout for a single physical page (pageLabel == physical page in this book)."""
    try:
        p = int(re.sub(r"[^0-9]", "", page_label))
    except ValueError:
        return ""
    out = subprocess.run(
        ["pdftotext", "-layout", "-f", str(p), "-l", str(p), PDF, "-"],
        capture_output=True, text=True, timeout=60,
    )
    return out.stdout


def locate_context(hl_text, raw_page):
    """Find the highlight inside the page text and return the surrounding paragraph."""
    page_n = norm(raw_page)
    page_loose = norm_loose(raw_page)
    hl_loose = norm_loose(hl_text)
    idx = page_loose.find(hl_loose)
    status = "EXACT"
    if idx < 0:
        words = hl_loose.split()
        status = "PARTIAL"
        for take in (12, 10, 8, 6, 5, 4):
            if len(words) >= take and page_loose.find(" ".join(words[:take])) >= 0:
                idx = page_loose.find(" ".join(words[:take])); break
        else:
            if len(words) >= 6 and page_loose.find(" ".join(words[2:8])) >= 0:
                idx = page_loose.find(" ".join(words[2:8]))
            else:
                return "NOT_FOUND", ""
    # map back into the readable (non-loose) page via a short anchor
    anchor = " ".join(norm(hl_text).split()[:5])
    ni = page_n.lower().find(anchor.lower())
    if ni < 0:
        ni = max(0, int(idx * len(page_n) / max(1, len(page_loose))))
    hln = norm(hl_text)
    # a list lead-in gets a wide forward window so the WHOLE enumerated list is captured
    fwd = LIST_FWD_CHARS if LIST_LEADIN.search(hln) else CTX_CHARS
    start = max(0, ni - CTX_CHARS)
    end = min(len(page_n), ni + len(hln) + fwd)
    # snap to word boundaries
    if start > 0:
        start = page_n.find(" ", start) + 1
    if end < len(page_n):
        end = page_n.rfind(" ", 0, end)
    return status, page_n[start:end].strip()


def is_list_leadin(hl_text):
    return bool(LIST_LEADIN.search(norm(hl_text)))


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--chapter", type=int, help="chapter number to extract")
    g.add_argument("--all", action="store_true", help="extract all highlighted chapters")
    ap.add_argument("--out", help="output JSON path (default: <skill>/work/chapter_<n>_highlights.json)")
    args = ap.parse_args()

    chap_map = json.load(open(CHAPTER_MAP))

    def chapter_of(page_label):
        try:
            p = int(re.sub(r"[^0-9]", "", page_label))
        except ValueError:
            return None, None
        for c in chap_map.values():
            if c["start"] <= p <= c["end"]:
                return c["chapter_num"], c["chapter_name"]
        return None, None

    # copy DB and read immutable
    tmp = tempfile.mkdtemp(prefix="emtcards_")
    db_copy = os.path.join(tmp, "z.sqlite")
    shutil.copy2(ZOTERO_DB, db_copy)
    con = sqlite3.connect(f"file:{db_copy}?immutable=1", uri=True)
    cur = con.cursor()
    att = resolve_attachment(cur)
    cur.execute(
        "SELECT pageLabel, position, text, comment, color, sortIndex "
        "FROM itemAnnotations WHERE parentItemID=? AND type=1 AND color IN (?,?) ORDER BY sortIndex",
        (att, YELLOW[0], YELLOW[1]),
    )
    rows = cur.fetchall()
    con.close()
    shutil.rmtree(tmp, ignore_errors=True)

    items = []
    page_cache = {}
    for page_label, position, text, comment, color, sort in rows:
        cnum, cname = chapter_of(page_label)
        if not args.all and cnum != args.chapter:
            continue
        if page_label not in page_cache:
            page_cache[page_label] = page_text(page_label)
        page_src = page_cache[page_label]
        # A list lead-in whose enumeration spills onto the NEXT page (e.g. the
        # decision-making-capacity factors run 272->273) would be truncated if we
        # only read one page. For lead-ins, append the next page so the whole list
        # is in context. (This is the real cause of the Ch3 "7 vs 8 factors" bug.)
        if is_list_leadin(text):
            try:
                nxt = str(int(re.sub(r"[^0-9]", "", page_label)) + 1)
                if nxt not in page_cache:
                    page_cache[nxt] = page_text(nxt)
                page_src = page_src + " " + page_cache[nxt]
            except ValueError:
                pass
        status, ctx = locate_context(text, page_src)
        items.append({
            "chapter_num": cnum,
            "chapter_name": cname,
            "page": page_label,
            "color": color,
            "highlight": norm(text),
            "context": ctx,
            "grounding": status,
            # true = this highlight introduces an enumerated list; the writer/editor
            # MUST count the list against the full page (not just this context) and
            # test every item — this is where undercounting/ungrounded completion hides.
            "list_lead_in": is_list_leadin(text),
            "user_comment": (comment or "").strip() or None,
            "sort": sort,
        })

    target_chap = "all" if args.all else str(args.chapter)
    out = args.out or os.path.join(SKILL, "work", f"chapter_{target_chap}_highlights.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(items, open(out, "w"), indent=1, ensure_ascii=False)

    found = sum(1 for i in items if i["grounding"] in ("EXACT", "PARTIAL"))
    missing = [i["page"] for i in items if i["grounding"] == "NOT_FOUND"]
    print(f"Chapter {target_chap}: {len(items)} yellow highlights")
    print(f"  grounded: {found}/{len(items)}  (EXACT/PARTIAL)")
    if missing:
        print(f"  NOT located (handle manually / image): pages {missing}")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
