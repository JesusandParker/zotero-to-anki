#!/usr/bin/env python3
"""
labels.py — find a printed LABEL (one or more lines of words) among Vision word boxes.

Why not Vision's own lines: Vision happily merges words from two columns into one "line"
(`Control Knob Lever` on the microscope plate), and splits one label across lines. Labels
are therefore rebuilt from WORDS: start at a word matching the first token, then walk to
the next token on the same line (just to the right) or on the next line down (roughly
left-aligned or overlapping), always taking the nearest candidate.
"""
import re
from difflib import SequenceMatcher


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def tokens(label):
    return [t for t in (norm(x) for x in label.split()) if t]


def tok_match(a, b):
    if not a or not b:
        return False
    if a == b:
        return True
    if len(b) >= 4 and (a.startswith(b) or b.startswith(a)) \
            and min(len(a), len(b)) / max(len(a), len(b)) >= 0.7:
        return True
    return len(b) >= 3 and SequenceMatcher(None, a, b).ratio() >= 0.8


def _h(w):
    return max(1.0, w["y1"] - w["y0"])


def _next(prev, first, cands):
    """Best continuation of a label after word `prev` (first word of the label = `first`)."""
    best, bd = None, None
    h = _h(prev)
    pcy = (prev["y0"] + prev["y1"]) / 2
    for c in cands:
        ccy = (c["y0"] + c["y1"]) / 2
        # same line, to the right
        # (a word space is ~0.3 line-heights; a gap of 2h is the NEXT COLUMN's label —
        #  "styloid process" once grabbed the "(temporal bone)" of the label beside it)
        if abs(ccy - pcy) < 0.4 * h and c["x0"] > prev["x1"] - 0.4 * h and c["x0"] - prev["x1"] < 1.0 * h:
            d = c["x0"] - prev["x1"]
        # next line down, starting near the label's left edge (or overlapping it)
        elif 0.35 * h < c["y0"] - prev["y0"] and c["y0"] - prev["y1"] < 1.3 * h and (
                abs(c["x0"] - first["x0"]) < 4.5 * h or
                (c["x0"] < prev["x1"] and c["x1"] > first["x0"])):
            d = 3 * h + abs(c["x0"] - first["x0"]) * 0.2 + (c["y0"] - prev["y1"])
        else:
            continue
        if bd is None or d < bd:
            best, bd = c, d
    return best


def exactness(chain, toks):
    return sum(1 for c, t in zip(chain, toks) if norm(c["t"]) == t)


def find(words, label, max_hits=4, exclude=(), hint=None):
    """Occurrences of `label`: [(box, [word, ...]), ...].

    exclude : ids of words already claimed by another mask (a word belongs to one label)
    hint    : (x, y) pixel position of the label's first word; the nearest hit wins.
              Without a hint, exact spellings outrank fuzzy ones ("Periosteum" must not
              grab "Periosteal"), then top-to-bottom order.
    """
    toks = tokens(label)
    if not toks:
        return []
    pool = [w for w in words if id(w) not in exclude]
    hits = []
    for w in pool:
        if not tok_match(norm(w["t"]), toks[0]):
            continue
        chain = [w]
        ok = True
        for t in toks[1:]:
            cands = [c for c in pool if c not in chain and tok_match(norm(c["t"]), t)]
            nxt = _next(chain[-1], chain[0], cands)
            if nxt is None:
                ok = False
                break
            chain.append(nxt)
        if ok:
            box = (min(c["x0"] for c in chain), min(c["y0"] for c in chain),
                   max(c["x1"] for c in chain), max(c["y1"] for c in chain))
            hits.append((box, chain))
    if hint is not None:
        hx, hy = hint
        hits.sort(key=lambda h: (h[1][0]["x0"] - hx) ** 2 + (h[1][0]["y0"] - hy) ** 2)
    else:
        hits.sort(key=lambda h: (-exactness(h[1], toks), h[0][1], h[0][0]))
    out = []
    for box, chain in hits:
        ids = {id(c) for c in chain}
        if any(ids & {id(c) for c in ch} for _, ch in out):
            continue
        out.append((box, chain))
    return out[:max_hits]
