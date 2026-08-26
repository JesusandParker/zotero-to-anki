#!/usr/bin/env python3
"""
test_figures.py — the executable half of the figure-pipeline regression library.

`test_regressions.py` covers card QUALITY (what check_cards.py must catch). This covers
the FIGURE pipeline: what build_figure_index.py must find, and what attach_figures.py must
refuse to do twice. Same doctrine — every case asserts in BOTH directions: catch the bad,
and do not over-flag the good.

Cases here are referenced by id from `reference/regression-cases.md` and from run
manifests, which `check_hazards.py` enforces.

    .venv/bin/python scripts/test_figures.py
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_figure_index as B


CASES = []


def case(cid, name, fn):
    CASES.append((cid, name, fn))


# ---------------------------------------------------------------- R15: credit lines
# A caption only counts once a rights line corroborates it. Matching only on © silently
# lost EMT FIGURE 4-8 and 4-12, whose credit is "Courtesy of the Guide Dog Foundation".
# The fix then needed a length guard so body prose could not pose as a credit -- but
# applying that guard to the © tier dropped FIGURE 4-4, because the extractor welds the
# credit onto the following paragraph.
CREDIT_MUST_MATCH = [
    ("plain publisher credit", "© Jones & Bartlett Learning."),
    ("welded onto the next paragraph (EMT p370, 643 chars)",
     "© Jones & Bartlett Learning. 7.  Always speak slowly, clearly, and distinctly. "
     + "Pay close attention to the patient's response and repeat back what you heard. " * 6),
    ("photo credit", "Courtesy of the Guide Dog Foundation for the Blind."),
    ("photo credit, other preposition", "Courtesy from the Utah Department of Health."),
    ("panel-letter credit", "A, C:  © Photodisc;  B:  © Photodisc/Thinkstock."),
    ("source line", "Source: National Highway Traffic Safety Administration."),
    ("adapted line", "Modified from the American Heart Association guidelines."),
]
CREDIT_MUST_NOT_MATCH = [
    ("ordinary body prose", "Communicating With Visually Impaired Patients Like patients "
                            "who are hard of hearing, visually impaired patients need extra care."),
    ("a sentence that merely mentions courtesy",
     "Courtesy is a professional obligation, and you should extend it to every patient you "
     "meet on every call, regardless of how they treat you in return, because the way you "
     "carry yourself sets the tone for the entire encounter and shapes whether the patient "
     "will trust you with the information you need to treat them safely and effectively."),
    ("empty", ""),
    ("a caption is not its own credit", "FIGURE 4-8  A guide dog is easily identified."),
]


def r15():
    bad = []
    for what, text in CREDIT_MUST_MATCH:
        if not B.is_credit(text):
            bad.append(f"MISSED a real credit line: {what}")
    for what, text in CREDIT_MUST_NOT_MATCH:
        if B.is_credit(text):
            bad.append(f"OVER-FLAGGED non-credit text: {what}")
    return bad


case("R15", "credit-line detection: photo credits count, prose does not", r15)


# ---------------------------------------------------------------- R16: stale-cache art
# save_art used to check its cache BEFORE checking whether art was found, so a caption
# whose art stopped resolving silently adopted whatever file a previous run left at that
# path. The count stayed flat while the index pointed at the wrong picture.
def r16():
    import tempfile
    bad = []
    with tempfile.TemporaryDirectory() as d:
        target = os.path.join(d, "FIGURE_9_9.png")
        with open(target, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n stale bytes from an earlier run")
        path, how = B.save_art(None, None, 1, target, rerender=False)
        if path is not None:
            bad.append("returned a CACHED file for a caption with no art "
                       f"(got {how!r}) — a stale image would be indexed as this figure")
        # and the good direction: with art present the cache is still used
        path2, how2 = B.save_art(None, {"xref": 1, "px": (10, 10)}, 1, target, rerender=False)
        if path2 != target or how2 != "cached":
            bad.append(f"failed to reuse a valid cached file (got {path2!r}/{how2!r})")
    return bad


case("R16", "no art means no record — never adopt a stale cached image", r16)


# ---------------------------------------------------------------- R17: one figure per card
# Guarding only on "is THIS file already attached" is too weak: improve the matcher,
# re-run, and any card whose best figure changed silently gains a second picture instead
# of swapping. Six Chapter 6 cards did exactly this.
HAS_FIGURE = re.compile(r'<img src="emt_')


def r17():
    bad = []
    already = 'Why: the cranium encases the brain.<br><br><img src="emt_FIGURE_6_6.jpg">'
    if not HAS_FIGURE.search(already):
        bad.append("failed to notice a card that already carries a pipeline figure")
    # a card carrying only Parker's OWN pasted image is not 'already done' -- his image is
    # never stripped, but it must not block the pipeline from adding its own.
    his_own = 'Cue: ...<br><br><img src="Screenshot 2026-07-30 at 12.18.36.png">'
    if HAS_FIGURE.search(his_own):
        bad.append("mistook Parker's own pasted screenshot for a pipeline figure")
    if HAS_FIGURE.search("Why: plain back extra with no image at all."):
        bad.append("false positive on a card with no image")
    return bad


case("R17", "one pipeline figure per card; a re-run swaps, never stacks", r17)


# ---------------------------------------------------------------- R22: judged gate
# Two ways to attach, and the fresh-segment route (--to-cards) writes the cards FILE that
# anki_write.py then stages. If it accepted unjudged proposals, every merely-nearby figure
# the judge exists to catch would ship straight into a new chapter with nothing in between.
def r22():
    import json, subprocess, tempfile
    bad = []
    here = os.path.dirname(os.path.abspath(__file__))
    with tempfile.TemporaryDirectory() as d:
        unjudged = os.path.join(d, "p.json")
        json.dump({"teaches": [], "context": []}, open(unjudged, "w"))
        r = subprocess.run([sys.executable, os.path.join(here, "attach_figures.py"),
                            "--source", "emt", "--segment", "1", "--to-cards",
                            "--proposals", unjudged, "--dry-run"],
                           capture_output=True, text=True)
        if r.returncode == 0 or "not been judged" not in (r.stdout + r.stderr):
            bad.append("--to-cards accepted proposals with no `judged` flag")
        judged = os.path.join(d, "q.json")
        json.dump({"teaches": [], "context": [], "judged": True}, open(judged, "w"))
        r2 = subprocess.run([sys.executable, os.path.join(here, "attach_figures.py"),
                             "--source", "emt", "--segment", "1", "--to-cards",
                             "--proposals", judged, "--dry-run"],
                            capture_output=True, text=True)
        if r2.returncode != 0:
            bad.append(f"--to-cards refused a JUDGED file: {(r2.stdout + r2.stderr)[:120]}")
    return bad


case("R22", "the fresh-segment route refuses unjudged proposals", r22)


# ------------------------------------------------- R29: SKILL DRILLs are multi-page
# A Skill Drill is a procedure whose steps run ONE PER PAGE, and three separate things
# were wrong about it. On EMT Chapter 8 — a chapter that is mostly drills, and where four
# of the five marks Parker made are drills — the three together indexed 1 of 12.
def r29():
    bad = []

    # (a) A drill banner is titled ABOVE its body, like a TABLE. Classing it with FIGURE
    #     (caption-below) made pair_art search upward into the preceding prose.
    for label, want_above in (("SKILL DRILL 8-9", False), ("TABLE 5-1", False),
                              ("CHART 2-1", False), ("FIGURE 7-2", True)):
        above = not label.startswith(("TABLE", "CHART", "SKILL"))
        if above != want_above:
            bad.append(f"{label}: caption orientation should be "
                       f"{'above' if want_above else 'title-above-body'}")

    # (b) A drill banner has no credit line; a `Step N` heading is its corroboration.
    class P:
        def __init__(self, rows): self.rows = rows
        def get_text(self, _):
            return {"blocks": [{"type": 0, "bbox": (0, i * 10, 100, i * 10 + 9),
                                "lines": [{"spans": [{"text": t}]}]}
                               for i, t in enumerate(self.rows)]}
    drill = P(["Skill Drill 8-9 Performing the Extremity Lift"])
    steps = P(["Step 1", "The patient's hands are crossed over the chest."])
    if not B.find_captions(drill, steps):
        bad.append("a drill banner followed by 'Step 1' was not accepted as a caption")
    prose = P(["As described in SKILL DRILL 8-9, the extremity lift is useful here."])
    plain = P(["Other Carries", "Other carries are performed in the following manner:"])
    if B.find_captions(prose, plain):
        bad.append("body prose merely naming a drill was accepted as a caption")

    # (c) Step 1 sits on the caption's OWN page as often as on the next one. Starting the
    #     walk at cap+1 lost the first step of 3 of the 4 drills Parker marked.
    class Doc:
        def __init__(self, pages): self.pages = pages; self.page_count = len(pages)
        def __getitem__(self, i): return P(self.pages[i])
    d = Doc([["Skill Drill 8-11 Using a Scoop Stretcher", "Step 1", "Adjust the length."],
             ["Step 2", "Lift the patient slightly."],
             ["Step 3", "Lock the ends together."],
             ["Other Carries", "Other carries are performed as follows:"]])
    got = B.skill_drill_pages(d, 1)
    if got != [1, 2, 3]:
        bad.append(f"steps starting on the banner page: expected [1,2,3], got {got}")
    d2 = Doc([["Skill Drill 8-9 Performing the Extremity Lift"],
              ["Step 1", "Cross the hands."], ["Step 2", "Move between the legs."],
              ["FIGURE 8-17 The draw sheet method.", "© Jones & Bartlett Learning."]])
    got2 = B.skill_drill_pages(d2, 1)
    if got2 != [2, 3]:
        bad.append(f"banner alone on its page: expected [2,3], got {got2}")
    return bad


case("R29", "SKILL DRILLs: titled above, Step-corroborated, and multi-page", r29)


# ------------------------------------- R31: a TEXT table must not adopt the art above it
# Not every table is a raster. When a table is typeset as live text, `pair_art` correctly
# finds nothing — and the fallback chain then decided what happened next. `vector_region`
# searches ABOVE the caption, which is right for a FIGURE (captioned below its plate) and
# exactly backwards for a TABLE (titled above its body). EMT TABLE 7-2 was handed the
# "Special Populations" box sitting above its title, and that plate was one build away
# from landing on the 11 live cards that carry TABLE 7-2 on their backs.
def r31():
    bad = []
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "build_figure_index.py")).read()

    # the text-table render must be attempted BEFORE the above-the-caption vector search
    i_txt = src.find("text_table_render(doc, pno")
    i_vec = src.find("vector_region(page, cap[\"bbox\"])")
    if i_txt < 0 or i_vec < 0:
        bad.append("could not locate the fallback chain")
    elif i_txt > i_vec:
        bad.append("vector_region runs before text_table_render — a TEXT table can adopt "
                   "the art sitting ABOVE its title")
    if "not is_titled_above" not in src:
        bad.append("vector_region is not gated away from TABLE/CHART captions")

    # a table caption is corroborated by a credit far below it, but only when it is a TITLE
    class P:
        def __init__(self, rows): self.rows = rows
        def get_text(self, _):
            return {"blocks": [{"type": 0, "bbox": (0, i * 10, 100, i * 10 + 9),
                                "lines": [{"spans": [{"text": t}]}]}
                               for i, t in enumerate(self.rows)]}
    rows = ["TABLE 7-2 Noticeable Characteristics at Various Ages",
            "Age Characteristic"] + [f"{m} months  a milestone" for m in range(2, 9)]
    if not B.find_captions(P(rows), P(["9 months", "© Jones & Bartlett Learning."])):
        bad.append("a text table whose credit lands on the next page was rejected")
    # A realistic body page: the cross-reference sits MID-page with prose after it, so the
    # pre-existing near-the-foot rule cannot fire and the widened TABLE window is what is
    # actually under test. It must refuse, because the block is a sentence, not a title.
    prose = ["The Muscular System",
             "TABLE 6-3 and FIGURE 6-15 show the major muscles of the body, which are "
             "described in detail throughout the remainder of this section and summarized "
             "for review in the tables that follow this discussion of the skeleton.",
             "Skeletal muscle is under voluntary control and attaches to bone by tendons.",
             "Smooth muscle is found in the walls of hollow organs and is involuntary.",
             "Cardiac muscle has its own automaticity and is found only in the heart."]
    if B.find_captions(P(prose), P(["© Jones & Bartlett Learning."])):
        bad.append("body prose cross-referencing a table was accepted as a caption")
    return bad


case("R31", "a TEXT table renders its own body, never the art above its title", r31)


# ------------------- R32: a text table's last rows can sit above the NEXT caption
# EMT TABLE 8-3 runs onto p804, whose top carries its final two situations and its credit
# line — and then the Skill Drill 8-7 banner. Breaking on "a caption appears on this page"
# abandoned the page and produced a plate showing FOUR of the table's SIX situations, which
# is worse than no plate: it looks complete. The caption bounds the body from BELOW.
def r32():
    bad = []
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "build_figure_index.py")).read()
    fn = src[src.index("def text_table_render"):src.index("def _chunks")]
    if "stop_at" not in fn:
        bad.append("text_table_render has no lower bound for a continuation page — a "
                   "caption there will abandon the table's remaining rows")
    if "min(caps)" not in fn:
        bad.append("the continuation page is not clipped to the FIRST caption on it")
    # the page must still be abandoned when the caption opens it (nothing of the table left)
    if "<= y_from + 8" not in fn:
        bad.append("a continuation page whose caption sits at the very top is not skipped")
    return bad


case("R32", "a text table's continuation page is clipped to the next caption, not skipped", r32)


# --------------- R54: credit-less books (Giancoli) — caps-label captions + odd separators
# Giancoli 7e prints NO per-figure credit line anywhere (photo credits live in the back
# matter), so every corroboration path failed and chapter 1 indexed ZERO figures. Its
# labels are also set with an en dash that PyMuPDF returns as "–" or ";" depending on the
# embedded font ("TABLE 1;4" and "TABLE 1–5" on the same page), which truncated every id
# at the chapter digit. Two fixes: `norm_fig_num` normalizes the separator, and the
# registry's `caption_style: "caps-label"` accepts a block-initial ALL-CAPS keyword as its
# own corroboration — safe because such books cross-reference as "Fig. 1-8" / Title Case,
# never block-initial caps (R15 intact: prose must still be refused, flag on or off).
def r54():
    bad = []
    for raw, want in (("1;1", "1-1"), ("1–4", "1-4"), ("1—2", "1-2"),
                      ("9.3", "9.3"), ("6-15", "6-15"), ("1;", "1"),
                      ("1 ; 12", "1-12"), ("1 – 5", "1-5")):
        got = B.norm_fig_num(raw)
        if got != want:
            bad.append(f"norm_fig_num({raw!r}) = {got!r}, wanted {want!r}")

    class P:
        def __init__(self, rows): self.rows = rows
        def get_text(self, _):
            return {"blocks": [{"type": 0, "bbox": (0, i * 10, 100, i * 10 + 9),
                                "lines": [{"spans": [{"text": t}]}]}
                               for i, t in enumerate(self.rows)]}
    cap = P(["FIGURE 1;1 Aristotle is the central figure (dressed in blue) at the top of",
             "the stairs in this famous Renaissance portrayal of The School of Athens."])
    got = B.find_captions(cap, None, caps_label=True)
    if not got:
        bad.append("caps-label: a credit-less ALL-CAPS caption was rejected")
    elif got[0]["label"] != "FIGURE 1-1":
        bad.append(f"caps-label: separator not normalized — got {got[0]['label']!r}")
    spaced = P(["FIGURE 1 ; 12 Example 1–8. Diagrams are really useful for estimating."])
    got2 = B.find_captions(spaced, None, caps_label=True)
    if not got2 or got2[0]["label"] != "FIGURE 1-12":
        got2_label = repr(got2[0]["label"]) if got2 else "nothing"
        bad.append(f"span-level spaces around the separator broke the id — got {got2_label}")
    if B.find_captions(cap, None):
        bad.append("a credit-less caption was accepted WITHOUT the registry flag")
    prose = P(["Consider how two great minds interpreted motion; see Figure 1–1 for a",
               "Renaissance portrayal of Aristotle among the Greek philosophers."])
    if B.find_captions(prose, None, caps_label=True):
        bad.append("caps-label promoted a Title-Case prose cross-reference (R15 broken)")
    return bad


case("R54", "credit-less caps-label captions are corroborated; separator glyphs normalize", r54)


def main():
    fails = 0
    for cid, name, fn in CASES:
        problems = fn()
        if problems:
            fails += 1
            print(f"FAIL  {cid}  {name}")
            for p in problems:
                print(f"        {p}")
        else:
            print(f"PASS  {cid}  {name}")
    print(f"\n{len(CASES) - fails}/{len(CASES)} figure regression cases pass")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
