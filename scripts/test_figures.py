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
