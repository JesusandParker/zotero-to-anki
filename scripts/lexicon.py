#!/usr/bin/env python3
"""
lexicon.py — the toolbox for the PURPLE lane: "define this word for me" (2026-08-08).

Parker marks an unknown word in PURPLE while reading (usually a purple underline, which
sits cleanly under a yellow highlight when the word lives inside a span he also carded).
Each purple mark becomes ONE plain-language definition card in that segment's deck. The
doctrine, the card shape, and the gate contract live in card-rules #28 and card-recipes
§4b; this module owns the three mechanical pieces:

  1. TERM KEYS — `term_key()` normalizes a term so its morphological family collides:
     diaphoresis and diaphoretic are the same word to a reader, and carding both as
     strangers is exactly the duplicate Parker asked this lane to prevent. A key
     COLLISION never auto-merges anything — it summons a sense check (anatomic "process"
     and physiologic "process" are different cards) — so over-stripping is contained by
     design and under-stripping costs at most one redundant card.

  2. EVIDENCE — `--find` searches the source PDF itself for each term's own definition
     (the registered glossary range first, then a definition-shaped sentence anywhere in
     the book) and writes work/<source>/lexicon_evidence.json with MECHANICALLY EXTRACTED
     quotes. The card's definition is still AUTHORED plain (Parker: a textbook's formal
     definition often "overcomplicates" the thing worth knowing) — the quote is the
     verification anchor the authored definition is checked against, and the thing
     check_cards.py demands actually exists (R37). The model never types evidence; this
     script quotes the PDF or the entry does not exist.

  3. THE LEDGER — reference/lexicon-ledger.json remembers every lexicon card ever staged
     (term_key -> noteId + definition + where). `--dedup` consults it BEFORE drafting and
     verifies each remembered noteId still exists in Anki, so a card Parker deleted by
     hand never blocks a re-card (the drift lesson: Anki is ground truth, the ledger is a
     cache of it). No tag is ever added for this — Parker keeps cards at `ch<N>` only,
     and the repo-side link is the same design provenance.jsonl already uses. If the
     ledger is ever lost, rebuild it from runs/*/provenance.jsonl.

CLI:
    python3 scripts/lexicon.py key diaphoretic pathogenicity      # show term keys
    python3 scripts/lexicon.py --self-test                        # the merge/no-merge suite
    python3 scripts/lexicon.py --find <source> --terms-from work/<source>/<label>_highlights.json
    python3 scripts/lexicon.py --dedup work/<source>/<label>_highlights.json
    python3 scripts/lexicon.py --ledger-list [term_key]
"""
import argparse, json, os, re, subprocess, sys, unicodedata, urllib.error, urllib.request

import sources as S

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
LEDGER = os.path.join(SKILL, "reference", "lexicon-ledger.json")
ANKI = "http://localhost:8765"

# --------------------------------------------------------------------------- term keys
#
# Iterative suffix-strip, longest match first (sorted programmatically so list order can
# never reintroduce the bug the first self-test run caught), at most two rounds, never
# below a 4-char stem, then ONE trailing-vowel trim per word (diaphor·e, cyan·o — the
# Greek/Latin combining vowel). Curated for the morphology of Parker's actual reading
# (medical, biology, EMT) rather than general English — that is why -emia/-otic/-lysis
# are here and why bare -e and -ly are NOT (malaise must not become malais, and -ly once
# ate the middle of hemo·ly·sis). Under-merge is the cheap failure (one redundant card,
# caught at his review); over-merge is contained by the sense check that every collision
# triggers. Tune HERE, and add the pair to the self-test when you do.
_SUFFIXES = sorted([
    "ations", "ation", "ition", "iasis", "aemia", "rrhagia",
    "ology", "ologies", "ectomy", "otomy", "ostomy", "plasty", "plegia",
    "pathy", "rrhea", "osis", "esis", "asis", "itis", "uria",
    "emia", "emic", "etic", "otic", "lysis", "lytic", "atous",
    "ances", "ance", "ences", "ence", "ments", "ment", "ness",
    "ities", "ity", "ical", "eous", "ious", "ative",
    "ies", "ous", "ial", "ual", "ary", "ery", "ory", "eal",
    "al", "ar", "ic", "tic", "sis", "ses", "ion",
    "ent", "ents", "ant", "ants",
    "ive", "ize", "ise", "ist", "ism", "ing", "ed",
    "ia", "es", "s", "y", "a",
], key=len, reverse=True)
_MIN_STEM = 4
_VOWELS = "aeiou"


def _strip_diacritics(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def clean_term(raw):
    """Display form: what the card prints. Straightens quotes, trims the punctuation a
    twitchy word-level drag drags along, collapses whitespace. Case is preserved —
    'pH' and 'Golgi' must not be flattened on the card face."""
    t = unicodedata.normalize("NFKC", raw or "")
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"\s+", " ", t).strip()
    t = t.strip(" \t\"'()[]{}<>.,;:!?–—-·•")
    return t


def _stem(word):
    w = word
    for _round in range(2):
        for suf in _SUFFIXES:
            # One-letter suffixes (-s, -a, -y) are round-1 only: after a real suffix has
            # come off, a trailing letter is usually part of the stem, not morphology
            # (perfus·ion must not continue to perfu).
            if _round > 0 and len(suf) == 1:
                continue
            if w.endswith(suf) and len(w) - len(suf) >= _MIN_STEM:
                w = w[: len(w) - len(suf)]
                break
        else:
            break
    # Canonical trim: one trailing combining vowel, so 'diaphore' (from -tic strips)
    # and 'diaphor' (from -esis) land on the same key. Applies to unstripped words too
    # ('perfuse' -> 'perfus' meets 'perfusion' -> 'perfus').
    if len(w) > _MIN_STEM and w[-1] in _VOWELS:
        w = w[:-1]
    return w


def term_key(term):
    """Normalized dedup key. Multi-word terms ('pulsus paradoxus') keep every word,
    each stemmed, joined with '_' — the phrase is the unit, not its head word."""
    t = _strip_diacritics(clean_term(term)).lower()
    words = [w for w in re.split(r"[^a-z0-9]+", t) if w]
    return "_".join(_stem(w) for w in words)


# Pairs that MUST share a key (the reader meets them as one word), and pairs that must
# NOT (different words that a greedy stemmer would crush together). Run after ANY edit
# to _SUFFIXES — this is the same two-directional contract the regression suite uses.
SELF_TEST_MERGE = [
    ("diaphoresis", "diaphoretic"),
    ("virulent", "virulence"),
    ("pathogen", "pathogenicity"),
    ("pathogenic", "pathogen"),
    ("hemolysis", "hemolytic"),
    ("ischemia", "ischemic"),
    ("cyanosis", "cyanotic"),
    ("aorta", "aortic"),
    ("vertebra", "vertebral"),
    ("stenosis", "stenotic"),
    ("thrombosis", "thrombotic"),
    ("edema", "edematous"),
    ("necrosis", "necrotic"),
    ("Pulsus Paradoxus", "pulsus paradoxus"),
    ("perfusion", "perfuse"),
    ("pneumonia", "pneumonic"),
]
SELF_TEST_NO_MERGE = [
    ("process", "procedure"),
    ("malaise", "malaria"),
    ("tendon", "tender"),
    ("sternum", "sternal_close_enough_not_required"),  # under-merge is acceptable
    ("colon", "column"),
    ("ligament", "ligature"),
]


def self_test():
    ok = True
    for a, b in SELF_TEST_MERGE:
        ka, kb = term_key(a), term_key(b)
        if ka != kb:
            print(f"  FAIL  {a} ({ka})  should merge with  {b} ({kb})")
            ok = False
    for a, b in SELF_TEST_NO_MERGE:
        if "_close_enough" in b:
            continue
        ka, kb = term_key(a), term_key(b)
        if ka == kb:
            print(f"  FAIL  {a} and {b} wrongly merge at ({ka})")
            ok = False
    print("lexicon self-test:", "OK" if ok else "FAILED")
    return ok


# --------------------------------------------------------------- evidence (the anchor)

def _whole_pdf_pages(pdf):
    """List of page texts for the whole document, one pdftotext run (pages split on
    form-feed). Cached beside the source's other work files, keyed on the PDF's mtime,
    because the EMT book is ~1,300 pages and re-extracting per run is pure waste."""
    src_dir = os.path.join(SKILL, "work", "_fulltext")
    os.makedirs(src_dir, exist_ok=True)
    tag = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(pdf))
    cache = os.path.join(src_dir, tag + ".json")
    mtime = os.path.getmtime(pdf)
    if os.path.exists(cache):
        try:
            data = json.load(open(cache))
            if data.get("mtime") == mtime:
                return data["pages"]
        except (json.JSONDecodeError, KeyError):
            pass
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                         capture_output=True, text=True, timeout=600)
    pages = out.stdout.split("\f")
    with open(cache, "w") as f:
        json.dump({"mtime": mtime, "pages": pages}, f)
    return pages


def _norm_ws(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _sentences(text):
    """Rough sentence split — good enough to quote a definition-shaped sentence."""
    return re.split(r"(?<=[.!?])\s+(?=[A-Z(])", _norm_ws(text))


# Definition-shaped patterns for the IN-SOURCE pass, strongest first. Both tightened by
# the first live run (2026-08-08): a bare "term, X," appositive matched symptom LISTS
# ("diaphoresis, shortness of breath, …"), so the comma form now requires an explicit
# "or"; parenthetical stays. Group 'd' is the defining tail.
def _def_patterns(term):
    t = re.escape(term).replace(r"\ ", r"\s+")
    return [
        # "Term is/are/means/refers to ..." — the classic textbook definition sentence.
        re.compile(rf"\b{t}\b\s*(?:\([^)]*\)\s*)?(?:is|are|means|refers?\s+to|describes?)\s+(?P<d>[^.;]{{8,240}})", re.I),
        # Explicit appositive gloss: "term, or <gloss>," / "term (<gloss>)".
        re.compile(rf"\b{t}\b\s*(?:\(\s*(?P<d1>[^)]{{6,120}})\s*\)|,\s*or\s+(?P<d2>[^,.;]{{6,120}})[,.;])", re.I),
    ]


# A glossary headword line: "syncope:" / "xiphoid process: The narrow…". This PDF's
# layout sometimes puts the gloss on the SAME line and sometimes on the NEXT line(s)
# ("diaphoretic:" alone, definition following) — so the glossary is parsed structurally,
# once, into headword entries, and terms are matched by TERM KEY, not by regexing each
# term against raw pages. That is also what lets a marked "diaphoresis" find the
# glossary's "diaphoretic:" — the family is the unit, same as dedup.
_HEADWORD = re.compile(r"^([A-Za-z][\w /()'-]{0,60}?):\s*(.*)$")


def _parse_glossary(pages, gp, pdf=None):
    """{term_key(headword): {headword, page, gloss}} for the registered glossary range.

    Parsed as ONE continuous line stream across the whole range, not per page — a
    headword on a page's last line carries its gloss at the top of the NEXT page
    (EMT p4042 "diaphoretic:" / p4043 the definition), and a per-page walk lost every
    such entry."""
    entries = {}
    if not gp:
        return entries
    stream = []          # (page_number, line)
    for pnum in range(gp[0], min(gp[1], len(pages)) + 1):
        for line in (pages[pnum - 1] or "").splitlines():
            if line.strip():
                stream.append((pnum, line.strip()))
    for li, (pnum, line) in enumerate(stream):
        m = _HEADWORD.match(line)
        if not m:
            continue
        head, rest = m.group(1).strip(), m.group(2).strip()
        gloss = [rest] if rest else []
        for _pn, nxt in stream[li + 1: li + 4]:
            if _HEADWORD.match(nxt):
                break
            gloss.append(nxt)
        text = _norm_ws(" ".join(gloss))
        if len(text) < 6:
            continue
        key = term_key(head)
        if key:
            # A LIST per key: hypoxia and hypoxemia both key to 'hypox', and a dict
            # overwrite would silently lose one of two real glossary entries.
            entries.setdefault(key, []).append(
                {"headword": head, "page": str(pnum), "gloss": text[:300]})

    # Second style: "Headword. Definition …" (Snustad's genetics glossary). The cached
    # -layout text renders that glossary's two columns side by side, interleaving
    # entries beyond repair, so this pass re-extracts the glossary range in raw reading
    # order (no -layout) when it has the PDF path. Entries are blank-line-separated
    # BLOCKS whose headword ends at the first period OUTSIDE parentheses — "Allele
    # (allelomorph; adj., allelic, allelomorphic). One of a pair…" keeps its
    # parenthetical periods inside the headword. A headword containing a colon is
    # rejected so EMT-style "term: definition" blocks can never double-match here.
    raw_pages = []
    if pdf:
        try:
            out = subprocess.run(
                ["pdftotext", "-f", str(gp[0]), "-l", str(gp[1]), pdf, "-"],
                capture_output=True, text=True, timeout=120)
            raw_pages = out.stdout.split("\f")
        except (OSError, subprocess.SubprocessError):
            raw_pages = []
    def _head_split(text):
        """(head, rest) at the first depth-0 '. ', or (None, None). The paren guard keeps
        'Allele (allelomorph; adj., allelic…). One of…' whole through its inner periods."""
        depth = 0
        for i, ch in enumerate(text[:90]):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif ch == "." and depth == 0 and text[i + 1: i + 2] in ("", " "):
                head, rest = text[:i].strip(), text[i + 1:].strip()
                if (re.match(r"^[A-Z]", head) and ":" not in head
                        and 2 <= len(head) <= 70 and len(head.split()) <= 8):
                    return head, rest
                return None, None
        return None, None

    # Entries are scanned LINE-WISE, not block-wise: a column break drops the previous
    # entry's wrapped tail directly above the next headword with no blank line between,
    # and a block scan glues that fragment onto the headword and rejects the pair —
    # which is how Bacteriophage, Chromatin, and Phenotype all vanished on first try.
    for off, ptext in enumerate(raw_pages):
        pnum = gp[0] + off
        lines = [l.strip() for l in (ptext or "").splitlines()]
        starts = []
        for li, line in enumerate(lines):
            if not line or re.fullmatch(r"[A-Z]", line):
                continue
            h, _ = _head_split(_norm_ws(line))
            if h:
                starts.append(li)
        for si, li in enumerate(starts):
            stop = starts[si + 1] if si + 1 < len(starts) else len(lines)
            chunk = [lines[li]]
            for nxt in lines[li + 1: stop]:
                if not nxt:            # blank line = end of this entry
                    break
                chunk.append(nxt)
            text = re.sub(r"(\w)- (\w)", r"\1\2", _norm_ws(" ".join(chunk)))
            head, rest = _head_split(text)
            if not head or len(rest) < 6:
                continue
            key = term_key(head)
            if key and not any(e["headword"] == head for e in entries.get(key, [])):
                entries.setdefault(key, []).append(
                    {"headword": head, "page": str(pnum), "gloss": rest[:300]})
    return entries


def _pick_glossary_entry(term, cands):
    """Choose among same-key glossary entries. Exact surface match wins; otherwise the
    longest-common-prefix candidate is returned AND flagged (`headword` recorded) — a
    family variant (diaphoresis → 'diaphoretic:') is safe, but a CONFUSABLE collision
    (hypoxemia → 'hypoxia:') looks identical mechanically, so a differing headword is a
    SENSE-CHECK trigger for the drafter, never a free anchor (recipes §4b)."""
    if not cands:
        return None
    t = clean_term(term).lower()
    for c in cands:
        if clean_term(c["headword"]).lower() == t:
            return dict(c)
    def lcp(a, b):
        n = 0
        for x, y in zip(a, b):
            if x != y:
                break
            n += 1
        return n
    best = max(cands, key=lambda c: lcp(clean_term(c["headword"]).lower(), t))
    out = dict(best)
    out["differs"] = True
    return out


def find_evidence(source_id, terms):
    """For each term, hunt the source itself for its definition. Returns the evidence
    dict and writes work/<source>/lexicon_evidence.json (merging over any prior run —
    an evidence entry is stable unless the PDF changes).

    Tiers, and what they mean downstream:
      glossary   — found inside the registered glossary_pages range. Strongest anchor.
      in_source  — a definition-shaped sentence elsewhere in the book (Parker's Ch5
                   lesson generalized: the book often DOES define the word — three
                   chapters later. Search the whole document, never 'up to here').
      (absent)   — no entry: the card's anchor must say `external`, and verify_report
                   will put it in front of Parker's eyes (R35).
    """
    src = S.get_source(source_id)
    _item, pdf = S.resolve_attachment(src)
    pages = _whole_pdf_pages(pdf)
    gp = S.glossary_pages(src)

    out_path = os.path.join(SKILL, "work", source_id, "lexicon_evidence.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    evidence = {}
    if os.path.exists(out_path):
        try:
            evidence = json.load(open(out_path)).get("terms", {})
        except json.JSONDecodeError:
            evidence = {}

    glossary = _parse_glossary(pages, gp, pdf=pdf)
    for term in terms:
        key = term_key(term)
        entry, occurrences = None, 0
        # Tier 1 — the glossary, matched structurally by TERM KEY (finds "diaphoretic:"
        # for a marked "diaphoresis"; finds "xiphoid process:" for a marked "xiphoid"
        # only if the keys agree — a marked single word keys differently from a
        # two-word headword, so also try prefix containment on the headword's words).
        g = _pick_glossary_entry(term, glossary.get(key, []))
        if not g:
            tw = key.split("_")
            for gk, ges in glossary.items():
                gw = gk.split("_")
                contain = tw and all(w in gw for w in tw)      # marked "xiphoid" ⊆ "xiphoid process"
                rcontain = gw and all(w in tw for w in gw)     # marked "Bacteriophage T2" ⊇ "Bacteriophage"
                # Single-word morphological family the stemmer keys apart
                # (phenotypicall ~ phenotyp). ≥6 shared chars so short stems can
                # never cross-match the way type_iiis/type_iir would on raw prefixes.
                family = (len(tw) == 1 and len(gw) == 1
                          and (tw[0].startswith(gw[0]) or gw[0].startswith(tw[0]))
                          and min(len(tw[0]), len(gw[0])) >= 6)
                if contain or rcontain or family:
                    g = _pick_glossary_entry(term, ges)
                    break
        if g:
            entry = {"term": clean_term(term), "method": "glossary",
                     "page": g["page"], "quote": f"{g['headword']}: {g['gloss']}"}
            if g.get("differs") or clean_term(g["headword"]).lower() != clean_term(term).lower():
                # The anchor came through a DIFFERENT headword. Fine for a family
                # variant, dangerous for a confusable — record it so the drafter and
                # editor (check #30) must confirm the gloss fits THIS word's sense.
                entry["headword"] = g["headword"]
        # Tier 2 — a definition-shaped sentence anywhere in the book.
        pats = _def_patterns(clean_term(term))
        for pnum, ptext in enumerate(pages, start=1):
            if not ptext or clean_term(term).lower() not in ptext.lower():
                continue
            occurrences += 1
            if entry:
                continue  # still counting occurrences, but the glossary already won
            for pat in pats:
                m = pat.search(ptext)
                if m:
                    entry = {"term": clean_term(term), "method": "in_source",
                             "page": str(pnum), "quote": _norm_ws(m.group(0))[:300]}
                    break
        if entry:
            entry["occurrences"] = occurrences
            evidence[key] = entry
        else:
            # No entry AT ALL is the signal for `external` — do not write a stub, so the
            # gate's "entry exists with a non-empty quote" test stays meaningful (R37).
            evidence.pop(key, None)
        status = entry["method"] if entry else "external"
        via = f"  [via headword '{entry['headword']}' — SENSE-CHECK]" if entry and entry.get("headword") else ""
        print(f"  {clean_term(term):30s} -> {status:9s}"
              + (f"  p{entry['page']}  \"{entry['quote'][:60]}…\"{via}" if entry else
                 f"  ({occurrences} occurrence(s), none definition-shaped)"))

    with open(out_path, "w") as f:
        json.dump({"source": source_id, "produced_by": "lexicon.py", "terms": evidence},
                  f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {out_path} ({len(evidence)} anchored term(s))")
    return evidence


# ------------------------------------------------------------------------- the ledger

def _load_ledger():
    if not os.path.exists(LEDGER):
        return {"_comment": "term_key -> list of staged lexicon cards. Cache of Anki, "
                            "verified live before it ever blocks a card; rebuild from "
                            "runs/*/provenance.jsonl if lost.", "terms": {}}
    return json.load(open(LEDGER))


def _save_ledger(led):
    with open(LEDGER, "w") as f:
        json.dump(led, f, indent=1, ensure_ascii=False)
        f.write("\n")


def _anki(action, **params):
    req = urllib.request.Request(
        ANKI, data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res["result"]


def ledger_record(term, key, note_id, source_id, segment, definition):
    """Called by anki_write.py the moment a lexicon note lands. Appends, never
    overwrites — two senses of one key are two entries."""
    led = _load_ledger()
    led.setdefault("terms", {}).setdefault(key, []).append({
        "term": term, "noteId": note_id, "source": source_id,
        "segment": segment, "definition": definition,
    })
    _save_ledger(led)


def dedup_report(highlights_path):
    """For each lexicon item in a highlights file: is its key already in the ledger,
    and is that card still ALIVE in Anki? Prints a JSON verdict per item for the
    drafting session to act on. Requires Anki open — the liveness check is the whole
    point (a hand-deleted card must never block a re-card). Entries whose noteId no
    longer exists are pruned from the ledger on the spot."""
    items = json.load(open(highlights_path))
    lex = [i for i in items if i.get("kind") == "lexicon"]
    led = _load_ledger()
    verdicts, pruned = [], 0
    for it in lex:
        key = it.get("term_key") or term_key(it.get("term", it.get("highlight", "")))
        hits = led.get("terms", {}).get(key, [])
        live = []
        for h in hits:
            try:
                info = _anki("notesInfo", notes=[h["noteId"]])
            except (urllib.error.URLError, OSError) as e:
                sys.exit(f"ERROR: cannot reach AnkiConnect — the liveness check needs "
                         f"Anki open. ({e})")
            if info and info[0].get("fields"):
                live.append(h)
            else:
                pruned += 1
        if len(live) != len(hits):
            if live:
                led["terms"][key] = live
            else:
                led.get("terms", {}).pop(key, None)
        verdicts.append({
            "term": it.get("term"), "term_key": key, "page": it.get("page"),
            "duplicate": bool(live),
            "existing": [{"noteId": h["noteId"], "term": h["term"],
                          "source": h["source"], "segment": h.get("segment"),
                          "definition": h.get("definition")} for h in live],
            "note": ("key already carded — run the SENSE CHECK against this item's "
                     "context before skipping; a different sense is a NEW card with a "
                     "domain cue (card-rules #28)") if live else "new term",
        })
    if pruned:
        _save_ledger(led)
    print(json.dumps({"lexicon_items": len(lex), "pruned_dead_entries": pruned,
                      "verdicts": verdicts}, indent=1, ensure_ascii=False))
    return verdicts


# ------------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Purple-lane toolbox: term keys, evidence, ledger.")
    ap.add_argument("cmd", nargs="*", help="`key <terms...>` to show keys")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--find", metavar="SOURCE", help="hunt in-source definitions; writes lexicon_evidence.json")
    ap.add_argument("--terms", nargs="*", help="terms for --find")
    ap.add_argument("--terms-from", help="highlights JSON; --find every kind:lexicon item in it")
    ap.add_argument("--dedup", metavar="HIGHLIGHTS", help="ledger + liveness verdict per lexicon item")
    ap.add_argument("--ledger-list", nargs="?", const="", metavar="KEY", help="dump the ledger (or one key)")
    a = ap.parse_args()

    if a.self_test:
        sys.exit(0 if self_test() else 1)
    if a.find:
        terms = list(a.terms or [])
        if a.terms_from:
            items = json.load(open(a.terms_from))
            terms += [i.get("term") or i.get("highlight", "")
                      for i in items if i.get("kind") == "lexicon"]
        if not terms:
            sys.exit("ERROR: --find needs --terms or --terms-from")
        find_evidence(a.find, terms)
        return
    if a.dedup:
        dedup_report(a.dedup)
        return
    if a.ledger_list is not None:
        led = _load_ledger()
        if a.ledger_list:
            print(json.dumps(led.get("terms", {}).get(term_key(a.ledger_list), []), indent=1))
        else:
            print(json.dumps(led, indent=1, ensure_ascii=False))
        return
    if a.cmd and a.cmd[0] == "key":
        for t in a.cmd[1:]:
            print(f"  {t:30s} -> {term_key(t)}")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
