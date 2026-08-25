#!/usr/bin/env python3
"""
check_cards.py — deterministic pre-flight GATE for generated cards (any source).

Runs the checks that CAN be mechanical, so they can never be skipped or
forgotten. Semantic checks (under-clozing, yield, subtle leaks) are the LLM
judge's job; this catches structure, format, literal leaks, missing flags, and
in-batch duplicates — including the exact shapes that have bitten us before
(see reference/regression-cases.md).

Three ways to run it:
  * GATE (default) — check a staged JSON file and, on a HARD-clean pass, write a
    `.verified` stamp so anki_write.py will let the file be staged. Strict HTML gate.
        python3 scripts/check_cards.py work/<source>/<file>_cards.json
  * AUDIT a file (--audit) — same, but for PRE-EXISTING/rich cards: skip the
    minimal-HTML HARD gate (embedded reference images/links, tables, the Ch5
    clinical-ex blocks) while keeping every meaningful check.
        python3 scripts/check_cards.py --audit work/emt/chapter_5_cards.json
  * LIVE AUDIT (--live) — pull cards straight from the Anki deck and check them, so
    cards HAND-EDITED in Anki (Mac + iPhone) still get audited. Relaxed HTML like
    --audit. Diagnostic only — it never stamps or writes.
        python3 scripts/check_cards.py --live 3   --source emt   # one segment
        python3 scripts/check_cards.py --live all --source emt   # the whole source
    (Added 2026-07-19 after a live audit found <a> anchor tags that had drifted
    into two cards via mobile paste-edits — the gate had never seen them because
    it only ever checked the pre-staging JSON.)

Exit 1 on any HARD error (blocks staging). WARNINGS print but don't block —
they are routed to the LLM judge / Parker.
"""
import argparse, hashlib, json, os, re, sys, unicodedata, urllib.request
from difflib import SequenceMatcher

import sources as S


def stamp_path(cards_json):
    return cards_json + ".verified"


def file_hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

ANKI = "http://localhost:8765"
ALLOWED_TAGS = {"b", "i", "br", "img"}
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")
TAG = re.compile(r"</?([a-zA-Z0-9]+)[^>]*>")
# a real VALUE/dose/threshold (number + unit, comparison, or range) — NOT a bare
# list ordinal like "1. Detection" or a year inside a name.
VALUE = re.compile(r"[<>≤≥]\s*\d|"
                   # a percentage gets its own branch: "%" is not a word character, so a
                   # trailing \b after it can never match and every percentage in the book
                   # escaped the numeric flag silently (found on ch7, 2026-07-31).
                   r"\d+\s*%|"
                   # a measured decimal (98.6 °F) — a bare "98.6" carries no unit word.
                   r"\d+\.\d|"
                   # rates written with the counted noun inline: 140 beats/min, 60 breaths/min.
                   r"\d+\s*[a-z]*\s*/\s*min|"
                   r"\d+\s*(?:mg|mcg|g|mmHg|mL|bpm|hours?|minutes?|seconds?|"
                   # ages and durations: this book states developmental facts as
                   # "28 months", "61 years and older", which are values, not ordinals.
                   r"days?|weeks?|months?|years?|"
                   r"pounds?|lbs?|kg|ounces?|oz|"
                   # plural + metric length forms: "10 inches (25 cm)" derived numeric=False
                   # because "inch" + \b cannot match "inches" and cm was absent (EMT ch8,
                   # 2026-08-12 — the power-grip hand-spacing card). R51.
                   r"mph|miles?|feet|ft|inch(?:es)?|in|cm|centimeters?|MHz|watts?|L/min|°|degrees?)\b|"
                   r"\d+\s*(?:to|-|–)\s*\d+", re.I)
# "N <list-noun>" where the card should then cloze exactly N items. A mismatch means
# the card states one count but tests another number of items — the exact shape of the
# Ch3 "consider 7 factors" bug (source had 8). Catch it mechanically.
NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
LIST_NOUNS = (r"factors|signs|steps|elements|questions|items|types|ways|routes|hazards|"
              r"circumstances|stages|consequences|forms|principles|functions|components|"
              r"categories|reasons|examples|cases|situations|conditions|features|actions|"
              r"criteria|rights|duties|methods|phases|properties|kinds|zones|levels|classes")
COUNT_RE = re.compile(r"\b(\d+|" + "|".join(NUMWORDS) + r")\s+(?:\w+\s+){0,2}?(?:" + LIST_NOUNS + r")\b", re.I)
# a single blank hiding this many words is almost never recallable verbatim: it is
# either a fuzzy scenario→action clause (R8) or a bloated two-way-definition c2 side
# that should be tightened to a crisp discriminator (card-recipes §4, parker-preferences).
LONG_CLOZE_WORDS = 9
# double-escaped markup that renders as literal "&lt;br&gt;" text (a real bug); &amp;
# inside a URL and &nbsp; are legitimate and NOT flagged.
BAD_ENTITY = re.compile(r"&(?:lt|gt);")


def readable(t):
    t = CLOZE.sub(lambda m: m.group(2), t)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s).lower()).strip()


def visible_stem(text, group):
    """The card's front for cloze GROUP: that group blanked, the others shown."""
    out, pos = [], 0
    for m in CLOZE.finditer(text):
        out.append(text[pos:m.start()])
        if m.group(1) == group:
            out.append("___")  # blank WITHOUT the hint: an answer inside its own
            # forced-choice hint ("federal or state?") is legitimate, not a leak
        else:
            out.append(m.group(2))
        pos = m.end()
    out.append(text[pos:])
    return re.sub(r"<[^>]+>", " ", "".join(out))


# --- Cold-Solve Gate mechanical proxies (card-rules #16-18 / regression R9-R11) ---
# R9 (open-set) is semantic and left to the LLM judge + the cold-solve test — no
# reliable mechanical proxy. R10 (husk) and R11 (letter-hint leak) are catchable.

ACRONYM = re.compile(r"\b[A-Z][A-Za-z]*[A-Z][A-Za-z/\-]*\b")  # SAMPLE, DCAP-BTLS, ABCs
LIST_MARKERS = re.compile(r"<br\s*/?>|(?:^|\s)\d+\.\s|:\s*$", re.I)


def first_letter_hint_leaks(text):
    """R11: a hint that is just the leading letter(s) of its own answer is a giveaway
    UNLESS the card is teaching a spelled mnemonic. The mere PRESENCE of an acronym in
    the stem licenses nothing (EMT/EMS/CPR sit in half this book's stems): the group's
    hint letters, joined in document order, must actually spell INTO a token visible in
    the stem — 'sample' into SAMPLE, 'dcapbtls' into DCAP-BTLS. Otherwise ::D/::B/::C
    on a plain list is the copout Parker ranted about, whatever else the stem mentions."""
    stem_plain = re.sub(r"<[^>]+>", " ", CLOZE.sub(lambda m: " ", text))
    tokens = [re.sub(r"[^a-z]", "", t.lower()) for t in ACRONYM.findall(stem_plain)]
    tokens = [t for t in tokens if len(t) >= 3]
    letter_hints = {}  # cloze group -> [(answer, hint, normalized letters)] in order
    for m in CLOZE.finditer(text):
        ans, hint = m.group(2), (m.group(3) or "")
        h = re.sub(r"[^a-z]", "", norm(hint))
        a = re.sub(r"[^a-z]", "", norm(ans))
        # a genuine forced-choice hint contains "/" or " or " (len guards those out)
        if 1 <= len(h) <= 2 and a.startswith(h) and "/" not in hint and " or " not in hint.lower():
            letter_hints.setdefault(m.group(1), []).append((ans, hint, h))
    def _subseq(needle, hay):
        it = iter(hay)
        return all(ch in it for ch in needle)

    leaks = []
    for g, items in letter_hints.items():
        joined = "".join(h for _, _, h in items)
        # licensed only if these letters, in order, spell into a stem token: a
        # contiguous run of >=2 (SAMPLE's 'sam'), or an in-order subsequence of >=3
        # (CHART's C-H-A-T, whose Rx item breaks contiguity). A lone letter never
        # self-licenses off e.g. 'EMT' — and when the acronym itself is co-clozed
        # (hidden), a letter hint leaks its spelling, so hidden answers are not tokens.
        licensed = any((len(joined) >= 3 and _subseq(joined, t)) or
                       (len(joined) >= 2 and joined in t) for t in tokens)
        if not licensed:
            leaks.extend((ans, hint) for ans, hint, _ in items)
    return leaks


STOP = set("a an the of to and or but in on at by for with as is are was were be been "
           "that this these those it its their his her they you your we our not only "
           "generally usually often may can will would should must also both either".split())


def _content_words(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return [w for w in re.findall(r"[a-zA-Z]+", s.lower()) if w not in STOP]


def _cloze_spans(text):
    """[(num, open_idx, content_start, content_end, close_end)], nesting-aware.

    The module CLOZE regex is non-greedy and cannot see nesting, so this walks the
    string with a stack instead."""
    opener = re.compile(r"\{\{c(\d+)::")
    out, stack, i = [], [], 0
    while i < len(text):
        m = opener.match(text, i)
        if m:
            stack.append((m.group(1), m.start(), m.end()))
            i = m.end()
            continue
        if text.startswith("}}", i):
            if stack:
                num, o, cs = stack.pop()
                out.append((num, o, cs, i, i + 2))
            i += 2
            continue
        i += 1
    return out


def nested_clozes(text):
    """R53: a cloze deletion sitting INSIDE another one.

    Anki's cloze shortcut assigns the NEXT UNUSED number, so selecting a word that is
    already inside a cloze and pressing it again wraps the selection in a brand-new
    number rather than reusing the old one:

        {{c1::Barotrauma}}  --select the word, press Cmd+Shift+C-->  {{c1::{{c4::Barotrauma}}}}

    When the inner span covers the WHOLE outer answer, the two cards are identical in the
    reviewer — both fronts read '[...] is pressure-induced trauma to the lungs' — so the
    note silently grows a duplicate card that can never teach anything the other doesn't.
    That is the hard case. A PARTIAL nest (`{{c1::the {{c2::mitral}} valve}}`) produces
    two genuinely different fronts, so it only warns: nothing in card-rules sanctions it,
    but it is not automatically wrong.

    Returns (identical, partial) as lists of (outer_num, inner_num).
    """
    spans = _cloze_spans(text)
    identical, partial = [], []
    for num, o, cs, ce, end in spans:
        for onum, oo, ocs, oce, oend in spans:
            if (oo, oend) == (o, end):
                continue
            if oo < o and end <= oce:          # this span is nested inside that one
                inner_full = text[o:end].strip()
                outer_body = text[ocs:oce].strip()
                (identical if outer_body == inner_full else partial).append((onum, num))
                break
    return identical, partial


def husk_groups(text):
    """R10: a single cloze number hiding EXACTLY 2 multi-word spans that sit in
    different clausal roles of an inline template — 'the ___ of X applies to ___' —
    so each blank's only cue is the other (the governmental-immunity husk).

    The discriminator vs a legitimate grouped PAIR (verbal/nonverbal; the two goals of
    therapeutic communication) is the CONNECTIVE between the two blanks: a coordinate
    pair is joined by 'and'/'or'/',' (~0 content words between them) and stays; a husk
    has a substantial templating phrase between the spans ('applies only to EMS systems
    operated by' = 5 content words). Also excludes <br>-listed or counted sets.

    Deliberately GENEROUS on multi-number contrast cards (cover/concealment, women one
    drink/men two drinks): it may flag a group whose sibling cloze number would anchor
    it. Suppressing those risks a FALSE NEGATIVE — a real husk that merely coexists with
    an unrelated cloze — which is the costly error on the exact class Parker rants about.
    So the checker over-flags and the LLM judge (editor #19) clears the benign ones."""
    if LIST_MARKERS.search(text):
        return []
    if COUNT_RE.search(readable(text)):
        return []
    # positions of each deletion, grouped by cloze number; s[4] = forced-choice hint?
    def is_forced(hint):
        return bool(hint) and ("/" in hint or " or " in hint.lower())
    spans = [(m.group(1), m.start(), m.end(), m.group(2), is_forced(m.group(3) or ""))
             for m in CLOZE.finditer(text)]
    hits = []
    for g in {s[0] for s in spans}:
        gs = [s for s in spans if s[0] == g]
        multiword = [s for s in gs if len(s[3].split()) >= 2]
        if len(gs) != 2 or len(multiword) < 2:
            continue  # a coordinate pair of short items, or a 3+ list — not a husk
        if all(s[4] for s in gs):
            continue  # both blanks carry a forced-choice hint — answerable by design
        between = text[gs[0][2]:gs[1][1]]
        if len(_content_words(between)) >= 2:  # real templating between the spans
            hits.append(g)
    return hits


ROW_RESIDUE_MAX = 8
BR_RUN = re.compile(r"(?:\s*<br\s*/?>\s*)+", re.I)


def _row_residue(seg):
    residue = re.sub(r"\s+", " ", CLOZE.sub("", seg)).strip()
    return re.sub(r"^\s*(?:\d+[.)]|[-•*])\s*", "", residue)  # ordinals/bullets are layout


def _is_list_row(seg):
    if not CLOZE.search(seg):
        return False
    return len(_row_residue(seg).split()) <= ROW_RESIDUE_MAX


def _is_header_lead_in(seg):
    """A lead-in that ends in a colon announces the list that follows."""
    return bool(re.search(r":\s*(?:</[a-zA-Z]+>\s*)*$", seg.strip()))


def segments(text):
    return [s.strip() for s in BR_RUN.split(text) if s.strip()]


def list_shaped(text):
    """Is this <br>-separated Text a LIST of things to produce, or prose?

    TWO independent signals. The second is the original rule; the FIRST was added
    2026-07-30 to close a real hole: requiring EVERY line to be a short row let ONE
    long line veto the whole card, so `listify()` and this checker both went silent on
    12 genuinely list-shaped live cards — including the EMS-radio card Parker
    complained about (3 of its 6 rows were "too wordy") and the ETHICS checklist
    (5 of 6 rows qualified; one 9-word row killed it).
      1. a colon-terminated lead-in heading >=2 lines that ALL carry a cloze — the
         author literally announced a list, so trust that over a word count; or
      2. every line after the lead-in is a short cloze-row (a list with no header).
    Prose that merely uses <br> between sentences satisfies neither: it has no colon
    header, and its lines carry too much residue to be rows."""
    segs = segments(text)
    if len(segs) < 2:
        return False
    body = segs[1:]
    if _is_header_lead_in(segs[0]) and len(body) >= 2 and all(CLOZE.search(s) for s in body):
        return True
    return (sum(1 for s in segs if _is_list_row(s)) >= 2
            and all(_is_list_row(s) for s in body))


def _has_single_br_separator(text):
    """True if ANY separator joining two non-empty segments is a lone <br>.

    Replaces a coarser "contains no <br><br> anywhere" test, which let a MIXED card
    (one spaced gap + two packed ones — EMT's upper-airway card) pass as already-spaced."""
    for m in BR_RUN.finditer(text):
        if not text[:m.start()].strip() or not text[m.end():].strip():
            continue   # a leading/trailing break, not a separator between rows
        if len(re.findall(r"<br", m.group(0), re.I)) < 2:
            return True
    return False


def packed_list_layout(text):
    """R14: a Text that is a LIST of things to produce, but whose rows are packed with a
    single <br> so they read as one block.

    Parker studies these to answer "how many things do I owe?" — the count should be
    visible at a glance, and single-<br> rows hide it. `anki_write.listify()` repairs this
    at write time (it imports `list_shaped` from here, so the repairer and the warning can
    never drift apart), so this is a WARNING that tells the drafter to author it correctly,
    not a block. Prose that merely uses <br> between sentences is deliberately untouched."""
    if not text or "<img" in text.lower() or not re.search(r"<br", text, re.I):
        return False
    return list_shaped(text) and _has_single_br_separator(text)


# ---------------------------------------------------------------------------
# The row-level Cold-Solve detectors (R15/R16/R17, added 2026-07-30).
#
# The Cold-Solve Gate (card-rules #16-18) was written and enforced at CARD
# granularity. Two of the three complaints that created these rules are ROW-level
# failures on cards that look fine whole — which is exactly how they slipped a
# 20-point human-agent pass and a green checker. These three run per ROW.
# ---------------------------------------------------------------------------

ROW_CONNECTIVE = r"(?:→|->|=|—|–)"
ROW_LABEL = re.compile(r"^\s*(?:<[^>]+>\s*)*([^{}<>]{3,80}?)\s*(?:\(\d+\)\s*)?"
                       + ROW_CONNECTIVE + r"\s*(?=.*\{\{c)")
# A classify/match/sort card's visible side is a DESCRIPTION that legitimately cues the
# answer — that is the archetype, not a leak. Its lead-in says so in the imperative.
CLASSIFY_LEAD = re.compile(r"\b(classif|sort|match|name the|name each|identify|which of|"
                           r"label each|where each|each \w+ (?:matches|belongs))", re.I)


def _stems(s):
    return {w[:5] for w in _content_words(s) if len(w) > 3}


def row_label_tautology(text):
    """R15: in a `LABEL → {{answer}}` row, the visible label restates its own hidden
    answer, so the label that is supposed to CUE the blank instead hands it over.

    Parker, 2026-07-30, on the EMS-radio card: "the return to service is the thing I'm
    supposed to say, so you're giving away the answer while trying to give me a hint."

    Deliberately GENEROUS, like the husk detectors: a shared word stem is evidence, not
    proof (`Initial receipt of call → acknowledge the call` shares "call" but still tests
    "acknowledge"). It fires ~8 times across a 1,100-card deck, so the cost of routing
    those to the judge is trivial and the cost of missing a real one is a card Parker
    cannot learn from. It is NOT suppressed on classify/match cards — the clotting row of
    EMT's blood-components card (`Clotting (coagulation) → platelets and clotting
    factors`) is a real leak sitting inside an otherwise legitimate match card."""
    hits = []
    for seg in BR_RUN.split(text):
        m = ROW_LABEL.match(seg)
        if not m:
            continue
        label = _stems(m.group(1))
        if not label:
            continue
        for a in CLOZE.finditer(seg):
            shared = label & _stems(a.group(2))
            if shared:
                hits.append((m.group(1).strip(), a.group(2), sorted(shared)))
    return hits


ABSOLUTE = re.compile(r"\b(never|always|only|must not|do not|don't|cannot|can't|"
                      r"should not|shouldn't)\b", re.I)
CONTRAST_TAIL = re.compile(r"\b(not|rather than|instead of|never)\b", re.I)


def open_set_absolute(text):
    """R16: a mechanical proxy for the highest-frequency corner of R9 (open-set cloze) —
    an absolute/prohibition sentence whose ONE unhinted blank is the thing prohibited.

    "You must never attribute a patient's altered mental status to {{c1::old age}}."
    Parker: "there are a lot of things I could fit in that blank… since there was no
    hint, no other cues, nothing else, how am I supposed to know it?"

    R9 has always been judge-only ("no reliable mechanical proxy"), and that is precisely
    why it walked back into Chapters 4 and 6 after being ruled out in July. This does not
    decide R9 in general; it closes the one shape that keeps recurring, and the fix it
    asks for is the one Parker asked for himself: a slot-label hint, or a visible
    contrast that forces the answer.

    Exempted: a hinted blank (the drafter constrained the slot), a numeric answer
    (self-constraining HERE, because an absolute sentence is not the shape that fails —
    but see `unlabeled_quantity_blank` below: that exemption was stated too broadly and
    a whole class of bare counts walked through it until 2026-08-03), a contrast anchor
    AFTER the blank
    that names the rejected alternative — "'right' and 'left' always refer to the
    {{c1::patient's}} perspective, not the provider's" is forced, not open — and an
    absolute that occurs only inside QUOTED SPEECH, which is dialogue in a vignette, not
    a rule the card is stating ("I am afraid I will never see my kids again" → which
    therapeutic technique is this? is a forced question, not an open blank)."""
    spans = list(CLOZE.finditer(text))
    if len(spans) != 1:
        return False           # a sibling cloze can anchor the blank
    m = spans[0]
    if m.group(3) or re.search(r"\d", m.group(2)):
        return False
    visible = re.sub(r"<[^>]+>", " ", CLOZE.sub(" ", text))
    visible = re.sub(r"[\"“][^\"”]*[\"”]", " ", visible)   # drop quoted dialogue
    if not ABSOLUTE.search(visible):
        return False
    return not CONTRAST_TAIL.search(re.sub(r"<[^>]+>", " ", text[m.end():]))


# --- R34: the numeric hole inside R16's exemption (added 2026-08-03) ---------------
# `open_set_absolute` above exempts a numeric answer as "self-constraining, and already
# numeric-flagged", and R16 records the same reasoning. It has a hole, and Parker walked
# straight into it: a number is only self-constraining ONCE YOU KNOW THE SLOT WANTS A
# NUMBER. A bare blank never says so, and an attributive slot takes adjectives just as
# happily as counts — `the {{c1::eight}} bones that form the wrist` and `the
# {{c1::short}} bones that form the wrist` are the SAME FRONT.

# A pure quantity: digits or number-words, optionally a range or an approximator. An
# answer carrying its own unit ("100 to 180 beats/min") is not bare — the unit travels
# with the answer and the drafter has already said what kind of thing it is.
BARE_QUANTITY = re.compile(
    r"^(?:about|approximately|roughly|around|up to|at least|"
    r"no more than|over|under|nearly)?\s*"
    r"(?:\d{1,4}(?:\.\d+)?|" + "|".join(NUMWORDS) + r")"
    r"(?:\s*(?:to|-|–|or)\s*(?:\d{1,4}(?:\.\d+)?|" + "|".join(NUMWORDS) + r"))?\s*$", re.I)

# A UNIT immediately after the blank labels the slot on its own: nothing but a number
# fits before "beats/min" or "mg". A plain head NOUN does not, which is the entire
# complaint — "bones" takes short, long, carpal, sesamoid without blinking.
UNIT_AFTER = re.compile(r"^\s*(?:%|°|mg|mcg|g|kg|mm|cm|mmHg|mL|L|bpm|beats|breaths|"
                        r"hours?|minutes?|seconds?|days?|weeks?|months?|years?|"
                        r"pounds?|lbs?|ounces?|oz|mph|miles?|feet|ft|inch(?:es)?|"
                        r"MHz|watts?|percent|degrees?)\b", re.I)

# A visible word that announces a quantity is being asked for.
QUANTITY_ASKED = re.compile(r"\b(how many|how much|how long|how old|how often|"
                            r"number|count|total|percent|percentage|dose|dosage|"
                            r"ratio|fraction|amount|quantity)\b", re.I)

# The defect is ATTRIBUTIVE — a count standing directly in front of the thing it counts,
# which is the one position where an adjective fits just as comfortably ("the ___ bones").
# So the blank only qualifies when a function word puts it in that slot. When a CONTENT
# word precedes instead, that word has already named what kind of number this is and the
# slot is labelled: `Type ___ diabetes`, `HPV ___`, `chromosome ___`, `a pKa of ___`,
# `on day ___`. Anything unrecognized is treated as labelled, so the detector only fires
# where it can see the attributive frame.
COUNT_SLOT_LEAD = {"the", "a", "an", "is", "are", "was", "were", "has", "have", "had",
                   "form", "forms", "contain", "contains", "include", "includes",
                   "comprise", "comprises", "its", "their", "these", "those", "all",
                   "only", "about", "approximately", "roughly", "some"}
# and it must actually modify a noun — a word, not punctuation or the end of the card.
NOUN_AFTER = re.compile(r"^\s*(?:<[^>]+>\s*)*[a-z][a-z\-]{2,}", re.I)


def unlabeled_quantity_blank(text):
    """R34: a blank whose answer is a bare quantity, with nothing visible telling Parker
    that a quantity is what the slot wants.

    Parker, 2026-08-03, on the carpals/metacarpals card: *"a good hint here would be
    something like {{c1::five::number of bones}} — that would make it so i can know what
    im guessing... just say like 'long bones!' or 'short bones!'"* He is describing the
    front exactly: `the ___ bones that form the wrist` invites a bone CLASSIFICATION as
    readily as a count, and he has no way to tell which the card wants.

    Five things count as announcing the slot, and any one of them exempts the blank:
      * a `::hint` — the canonical fix, and what Parker asked for by name;
      * a UNIT immediately after the blank (`___ beats/min`, `___ mg`, `___ months`);
      * a CONTENT WORD immediately before it, which has already named the kind of number
        — `Type ___ diabetes`, `HPV ___`, `chromosome ___`, `a pKa of ___`, `on day ___`.
        Only a function word ("the", "are", "form") leaves the slot genuinely attributive;
      * a quantity word visible in the stem (`how many`, `the number of`, `the dose of`);
      * another number left VISIBLE in a parallel slot, which shows the pattern —
        `{{c1::eight}} bones … {{c2::five}} bones` announces itself on both cards, while
        the same card with BOTH numbers under c1 announces nothing on either.

    Deliberately a WARNING. The judge clears the cases where ordinary English already
    forces a count ("there are ___ types of shock"), which is a real category this cannot
    separate mechanically. Scoped to BARE quantities in an ATTRIBUTIVE slot for the same
    reason R28 is scoped to numeric answers: it is what the evidence covers, and widening
    it to every unhinted blank would be a war on cards rather than a fix for one."""
    hits = []
    for m in CLOZE.finditer(text):
        if m.group(3):
            continue                                   # hinted: the slot is labelled
        ans = re.sub(r"<[^>]+>", " ", m.group(2)).strip()
        if not BARE_QUANTITY.match(ans):
            continue
        after = re.sub(r"<[^>]+>", " ", text[m.end():]).lstrip()
        if UNIT_AFTER.match(after):
            continue                                   # "___ beats/min": only a number fits
        if not NOUN_AFTER.match(after):
            continue                                   # modifies nothing; not a count slot
        before = re.sub(r"<[^>]+>", " ", text[:m.start()]).split()
        if not before or before[-1].strip("(,;:—–-").lower() not in COUNT_SLOT_LEAD:
            continue                                   # a content word already labelled it
        stem = visible_stem(text, m.group(1))
        if QUANTITY_ASKED.search(stem):
            continue                                   # the stem asks in words
        if re.search(r"\d|\b(?:" + "|".join(NUMWORDS) + r")\b", stem, re.I):
            continue                                   # a visible number in a parallel slot
        hits.append((m.group(1), ans))
    return hits


def fragment_clozed_list(text):
    """R17: a card that announces a list of things to produce, shows every item, and
    hides only a filler word inside each one — so it drills recognition of the frames
    while never training the recall that matters.

    Parker, 2026-07-30, on the 8-self-check-questions card: "I can pretty much guess most
    of these and get it right… it doesn't actually help me remember this card, it just
    helps me remember the CONTEXT of the card." The knowledge is *which 8 questions to
    ask*; all 8 question-frames are visible and one obvious word per row is hidden.

    Two exemptions keep the legitimate neighbours safe:
      * a classify/match lead-in — there the visible description IS the intended cue;
      * a row that LEADS with its cloze (`{{c1::Nasopharynx}} — above the soft palate`,
        every SAMPLE/SBAR mnemonic row) — there the item itself is the answer.
    What is left is the genuine inversion: a prose frame carrying the knowledge with a
    fragment punched out of it."""
    segs = segments(text)
    if len(segs) < 4:                                   # a lead-in + >=3 rows
        return False
    if CLASSIFY_LEAD.search(re.sub(r"<[^>]+>", " ", segs[0])):
        return False
    rows = [s for s in segs[1:] if CLOZE.search(s)]
    if len(rows) < 3:
        return False
    frag = 0
    for r in rows:
        if re.match(r"^\s*(?:<[^>]+>\s*)*\{\{c", r):
            continue                                    # the item IS the answer
        hidden = sum(len(m.group(2).split()) for m in CLOZE.finditer(r))
        visible = len(_row_residue(r).split())
        if visible >= 2 and hidden < visible:
            frag += 1
    return frag >= 3 and frag >= 0.6 * len(rows)


# ---------------------------------------------------------------------------
# R25/R26 — retrieval load (added 2026-08-02).
#
# The Cold-Solve Gate asks whether a blank is ANSWERABLE. These two ask whether a
# card is *passable*: a grouped reveal is graded all-or-nothing, so a card hiding N
# items is only "Good" when every one of the N is produced. At a realistic 90% per
# item that is 0.9^N — 59% at five items, 35% at ten — so a card can be built from
# facts Parker knows cold and still fail forever. Anki then reschedules the WHOLE
# card on its worst item, re-drilling nine known items to chase one unknown.
#
# Measured on his live collection, EMT decks only (same runs, same maturity), scored
# on each card's FIRST review so new-card bias cannot explain it:
#     ordinary (1-2 blanks)   1027 notes   56% failed first review   24.9 s/review
#     3-4 items                 90 notes   78%                       33.3 s/review
#     5-6 items                 34 notes   89%                       42.7 s/review
#     7+ items                   7 notes   80%                       49.3 s/review
# The 10-element radio-report card he reported: 5 reviews, 5 "Again", 54 s each —
# never once answered correctly.
# ---------------------------------------------------------------------------

# How many answers a group may hide with NO per-item cue before it stops being one
# retrieval. Cowan's working-memory estimate is 4±1 chunks; a spelled mnemonic buys
# more because the letters regenerate the set, which is why licensing exists below.
UNCUED_WARN = 6      # verify it is genuinely one chunk
UNCUED_HARD = 8      # no legitimate card shape hides this many uncued answers at once


def _spelled_mnemonic_license(text, group):
    """Does a spelled acronym visible in the stem generate this group's items?

    Reuses R11's rule exactly: the group's per-item first-letter hints, joined in
    document order, must spell INTO a token that is VISIBLE in the stem (SAMPLE,
    DCAP-BTLS). Such a set is ONE chunk however long it is — the acronym is the
    retrieval handle, so the load cap does not apply to it."""
    stem_plain = re.sub(r"<[^>]+>", " ", CLOZE.sub(lambda m: " ", text))
    tokens = [re.sub(r"[^a-z]", "", t.lower()) for t in ACRONYM.findall(stem_plain)]
    tokens = [t for t in tokens if len(t) >= 3]
    letters = []
    for m in CLOZE.finditer(text):
        if m.group(1) != group:
            continue
        h = re.sub(r"[^a-z]", "", norm(m.group(3) or ""))
        a = re.sub(r"[^a-z]", "", norm(m.group(2)))
        if 1 <= len(h) <= 2 and a.startswith(h):
            letters.append(h)
    joined = "".join(letters)
    if len(joined) < 2:
        return False

    def _subseq(needle, hay):
        it = iter(hay)
        return all(ch in it for ch in needle)

    return any((len(joined) >= 3 and _subseq(joined, t)) or
               (len(joined) >= 2 and joined in t) for t in tokens)


CUE_CONNECTIVE = re.compile(r"(?:→|->|—|–|=|:)\s*$")


def _cued_span(text, m):
    """Does THIS span carry its own visible cue, or is it one of a bare set?

    A match/classify row (`Transports oxygen → {{c1::red blood cells}}`), a keyed row
    (`Neonate — {{c1::100 to 180}}`) and a trend-panel row (`Heart rate: {{c1::Increased}}`)
    each hand the blank a private cue, so the card is N small independently-cued
    retrievals rather than one N-wide recall. A bare row (`{{c1::Smoke}}`,
    `3. {{c1::Receiving hospital and ETA}}`) has only the set's own name — numbering and
    bullets are layout, not cues.

    The trap this guards against: the card's LEAD-IN also ends in a colon ("…is composed
    of 10 structures:"), so the first item of an inline list would inherit the
    announcement as if it were a per-item label. A lead-in announces the set; it never
    labels one member. So a label only counts inside a row of its own — never in the
    same segment the card opens with."""
    seg_start = 0
    for sep in BR_RUN.finditer(text):
        if sep.end() <= m.start():
            seg_start = sep.end()
    if seg_start == 0:
        return False          # same segment as the lead-in: an announcement, not a label
    seg = text[seg_start:m.start()]
    if CLOZE.search(seg):
        return False          # a later span on a row already spoken for by the first
    label = re.sub(r"<[^>]+>", " ", seg)
    label = re.sub(r"^\s*(?:\d+[.)]|[-•*])\s*", "", label)   # numbering/bullets are layout
    label = re.sub(r"[\s→\->—–=:,;]+$", "", label).strip()
    # Any word of row-local text is a cue: `Neonate — {{c1::100 to 180}}` and
    # `cervical {{c1::7}}` both hand the blank something private to work from, with or
    # without a connective between them. What is NOT a cue is an empty row
    # (`{{c1::Smoke}}`) or bare numbering (`3. {{c1::Receiving hospital and ETA}}`).
    return len(label.split()) >= 1


def overloaded_group(text):
    """R25: one cloze number hiding more parallel answers than a single retrieval can
    carry, so the card is all-or-nothing on a set that must instead be CHUNKED.

    Returns a list of (group, uncued_count, total_count, licensed) for any group at or
    over UNCUED_WARN. Only UNCUED answers count: a per-row cue turns one N-wide recall
    into N cued ones (see `_cued_span`), and a spelled mnemonic the card teaches makes
    the whole set one chunk (see `_spelled_mnemonic_license`).

    Deliberately NOT flagged: a long single blank (that is R12's fuzzy-clause case), a
    two-way definition, and any group under the cap — the defect is retrieval LOAD, not
    list length as such. Parker's own line: a real list stays whole; what he cannot do
    is produce ten things at once and be graded on all ten."""
    by_group = {}
    for m in CLOZE.finditer(text):
        by_group.setdefault(m.group(1), []).append(m)
    hits = []
    for g, spans in by_group.items():
        if len(spans) < UNCUED_WARN:
            continue
        uncued = sum(1 for m in spans if not _cued_span(text, m))
        if uncued < UNCUED_WARN:
            continue
        hits.append((g, uncued, len(spans), _spelled_mnemonic_license(text, g)))
    return hits


# How many keyed numeric rows before a panel must become one note per key.
QUANT_PANEL_WARN = 3
QUANT_PANEL_HARD = 4


def quantitative_panel(text):
    """R28: a keyed panel of NUMBERS — 'Neonate — {{c1::100 to 180}}, Infant — {{c1::100 to
    160}}, …' — which must become one NOTE PER KEY instead of one card hiding the column.

    This is the correction to R25's cued-row exemption. A per-item cue makes each row
    *answerable*, and R25 therefore excused keyed panels at any length. That was wrong,
    for two independent reasons, and a quantitative panel is where both bite hardest:

      1. **Grading.** Every row still hides and reveals together under one cloze number, so
         the card is graded all-or-nothing on N values however well each row is cued. A cue
         fixes cold-solve; it does nothing for passability.
      2. **Interpolation.** Ordered keys with values that trend produce a column that gives
         itself away. Parker: *"if I see infant heart rate, I can guess what the neonate
         heart rate is… it's already given me half of the solution."* The card this rule
         comes from proved it in its own Back Extra — *"the lower bound walks down in clean
         tens — 100, then 90, 80, 70, and 60"* — an excellent mnemonic that is also an exact
         recipe for answering without recall.

    The fix is one note per key, each asking for a single value, with the SOURCE TABLE in
    Back Extra so the set stays visible after he answers. Parker's own framing: *"the cards
    are disconnected in the sense of memorizing, but they're connected in the sense of the
    table."*

    Deliberately scoped to NUMERIC answers. A match card whose answers are words (blood
    function → component) cannot be interpolated and is not caught here; it is judged on
    load alone by `overloaded_group`."""
    hits = []
    for g in {m.group(1) for m in CLOZE.finditer(text)}:
        spans = [m for m in CLOZE.finditer(text) if m.group(1) == g]
        if len(spans) < QUANT_PANEL_WARN:
            continue
        cued = sum(1 for m in spans if _cued_span(text, m))
        numeric = sum(1 for m in spans if VALUE.search(m.group(2)))
        # nearly every row must be BOTH keyed and quantitative: a panel with one stray
        # numeric row is not a value column, and a bare numeric list has no keys to split on
        if cued >= 0.8 * len(spans) and numeric >= 0.8 * len(spans):
            hits.append((g, len(spans)))
    return hits


# The shape a naive "just split it up" fix produces, and the reason chunking must mean
# separate NOTES. Parker named this himself before it was ever written down: "if it's a
# hide-one-but-show-all-the-rest, I can just figure that out."
def sibling_split_leak(text):
    """R26: an enumerated list split across DIFFERENT cloze numbers on ONE note, so
    every resulting card shows the rest of the list as free context.

    card-rules #4 already banned `{{c1::A}}, B, C` (cloze one, reveal the rest). This is
    the same defect wearing a fix's clothes: c1..cN over N rows generates N cards that
    each reveal N-1 answers, which lets the whole set be recovered by elimination and
    recognition instead of recall. The legitimate ways to split a list are separate
    notes — never separate numbers on one note."""
    by_group = {}
    for m in CLOZE.finditer(text):
        by_group.setdefault(m.group(1), []).append(m)
    if len(by_group) < 4 or any(len(v) != 1 for v in by_group.values()):
        return False
    segs = segments(text)
    rows = [s for s in segs[1:] if CLOZE.search(s)] if len(segs) > 1 else []
    if len(rows) < 4:
        return False
    # every row must be a parallel MEMBER of one set, not a distinct prose fact
    return sum(1 for s in rows if _is_list_row(s)) >= 4


PROCEDURE_LEAD = re.compile(
    r"\b(steps?|procedure|protocol|algorithm|technique|drill|perform(?:ing|ed)?|"
    r"how to|method|sequence)\b", re.I)


def step_recitation(text):
    """R30: a card that asks him to RECITE a procedure's steps, cued only by their number.

    Measured across Parker's own 85,212-note collection (2026-08-03), professional medical
    decks essentially never do this: "next step in management" cards are 93% single-span
    and 0% carry five or more, and `"how do you perform"` / `"steps to perform"` return
    ZERO hits across all 85k notes including 10,907 anesthesia cards. What they card is the
    DECISION — the state of the world in the stem, one action in the blank — or a decision
    TABLE whose rows are cued by their conditions rather than by their positions.

    A row cued only by "3." teaches position, which is not knowledge and is not what he
    will be asked for on a call. A row cued by a CONDITION ("FAST (+) and unstable?") is a
    different card entirely and is not flagged.

    This is a WARNING, not a block: an ordered protocol short enough to hold, whose order
    genuinely IS the knowledge, is a legitimate card — Parker's five-point handover method
    is one, and card-rules #26 licenses the forward-chain shape. The judge clears those."""
    segs = segments(text)
    if len(segs) < 4:                                  # a lead-in + >=3 rows
        return False
    if not PROCEDURE_LEAD.search(re.sub(r"<[^>]+>", " ", segs[0])):
        return False
    rows = [s for s in segs[1:] if CLOZE.search(s)]
    if len(rows) < 3:
        return False
    numbered = 0
    for r in rows:
        lead = re.sub(r"<[^>]+>", " ", CLOZE.split(r)[0])
        if not re.match(r"^\s*(?:\d+[.)]|step\s+\d+\s*[:.)]?)\s*$", lead.strip(), re.I):
            return False                               # some row carries a real cue
        numbered += 1
    return numbered >= 3


EQ_CONNECTIVE = re.compile(r"=|also called|also known as|\baka\b|stands for", re.I)


def equation_husk_groups(text):
    """R10 variant the word-count husk misses: a single cloze number hiding BOTH sides
    of an identity/synonym equation — '___ = also called ___' — regardless of span
    length or count (the off-line/indirect + online/direct card, and the Expressed =
    actual consent card). Blank the group; if a synonym connective ends up flanked by
    two blanks, flag it.
    Deliberately GENEROUS: it cannot tell 'the two hidden spans are synonyms of each
    other' (a real husk) from 'they are different things each anchored by a visible
    label' (an acronym card, POLST/MOLST stands-for; a grouped two-way def, SOAP
    Subjective=/Objective=) without semantics. So it over-flags those two shapes, and the
    LLM judge / human clears them — the same review-not-block contract as the word-count
    husk. Missing a real synonym husk is the costly error; a spare 'verify' warning is not."""
    hits = []
    for g in {m.group(1) for m in CLOZE.finditer(text)}:
        blanked = re.sub(r"<[^>]+>", " ",
                         re.sub(CLOZE, lambda m: (" ¤ " if m.group(1) == g else m.group(2)), text))
        if re.search(r"¤[^¤]{0,40}?(?:" + EQ_CONNECTIVE.pattern + r")[^¤]{0,40}?¤",
                     blanked, re.I):
            hits.append(g)
    return hits


def per_card(idx, c, strict_html=True):
    """All per-card mechanical checks. Returns (hard_list, warn_list) of message
    strings. `strict_html=False` (set by --audit and --live) downgrades the
    disallowed-HTML check from HARD to a warning, because pre-existing / hand-edited
    cards (esp. Chapter 5's clinical-example blocks, or a reference image Parker pasted)
    legitimately carry richer HTML; the default strict gate keeps NEW generated cards on
    b/i/br/img."""
    t, be = c.get("Text", ""), c.get("Back Extra", "")
    hard, warn = [], []
    # disallowed HTML
    bad = [g for g in (TAG.findall(t) + TAG.findall(be)) if g.lower() not in ALLOWED_TAGS]
    if bad:
        msg = f"#{idx}: disallowed HTML tag(s): {sorted(set(bad))}"
        if strict_html:
            hard.append(msg)
        else:
            warn.append(msg + " (rich/pre-existing: verify it renders; the generator must stay on b/i/br/img)")
    # must contain a cloze
    if not CLOZE.search(t):
        hard.append(f"#{idx}: no cloze markup in Text")
    # nested cloze — almost always an accidental re-cloze in the editor (R53)
    _ident, _partial = nested_clozes(t)
    for onum, inum in _ident:
        hard.append(f"#{idx}: cloze c{inum} is nested inside c{onum} and covers ALL of it — "
                    f"both cards render the SAME front, so c{inum} is a pure duplicate. "
                    f"Unwrap it back to a single {{{{c{onum}::…}}}} (card-rules #33)")
    for onum, inum in _partial:
        warn.append(f"#{idx}: cloze c{inum} is nested inside c{onum} — verify this is "
                    f"deliberate; Anki's cloze shortcut assigns the next unused number, so "
                    f"this is usually an accidental re-cloze of text already inside a cloze")
    # empty/whitespace cloze answer
    for m in CLOZE.finditer(t):
        if not m.group(2).strip():
            hard.append(f"#{idx}: empty cloze c{m.group(1)}")
    # double-escaped markup rendering as literal text
    if BAD_ENTITY.search(t) or BAD_ENTITY.search(be):
        warn.append(f"#{idx}: contains &lt;/&gt; — markup may be double-escaped and rendering as literal text")
    # literal answer visible in the stem (a leak)
    for g in {m.group(1) for m in CLOZE.finditer(t)}:
        stem = norm(visible_stem(t, g))
        for m in CLOZE.finditer(t):
            if m.group(1) == g:
                a = norm(m.group(2))
                if a and len(a.split()) <= 4 and re.search(r"\b" + re.escape(a) + r"\b", stem):
                    warn.append(f"#{idx}: answer '{m.group(2)}' is visible in its own stem (leak)")
    # parenthetical hanging right off a cloze (the pathway-card leak shape)
    if re.search(r"\}\}\s*\(", t):
        warn.append(f"#{idx}: parenthetical right after a cloze — verify it is NOT the answer's definition (leak risk)")
    # first-letter hint on a non-mnemonic list (R11, the ::r/::k/::s leak)
    for ans, hint in first_letter_hint_leaks(t):
        warn.append(f"#{idx}: hint '::{hint}' is the first letter of its answer '{ans}' with no acronym in the stem — first-letter leak (card-rules #18)")
    # all-blanks-at-once husk — mutually-dependent spans under one number (R10)
    for g in husk_groups(t):
        warn.append(f"#{idx}: cloze c{g} hides 2 multi-word spans in an inline template — possible husk; verify each blank is answerable with the other shown, else split into c1/c2 (card-rules #17)")
    # packed list layout — a list of things to produce, crammed into one block (R14)
    if packed_list_layout(t):
        warn.append(f"#{idx}: Text is a LIST of things to produce but its rows are packed with a "
                    f"single <br> — separate them with <br><br> so the number of answers owed is "
                    f"visible at a glance (card-rules #19; anki_write.listify() repairs it at write time)")
    # row-label restates its own answer — the label meant to CUE the blank leaks it (R15)
    for label, ans, shared in row_label_tautology(t):
        warn.append(f"#{idx}: row label '{label}' shares {shared} with its own answer "
                    f"'{readable(ans)}' — the label leaks the blank it is supposed to cue; "
                    f"re-word the label, or test what the label does NOT already say "
                    f"(card-rules #20)")
    # absolute statement whose lone unhinted blank is wide open (R16 — proxy for R9)
    if open_set_absolute(t):
        warn.append(f"#{idx}: an absolute/prohibition sentence with ONE unhinted blank — "
                    f"many true things may fit it; add a slot-label ::hint or a visible "
                    f"contrast that forces exactly one answer (card-rules #21)")
    # a bare number in a slot that never says it wants a number (R34 — closes the
    # "numeric answers are self-constraining" exemption R16 above claims)
    for g, ans in unlabeled_quantity_blank(t):
        warn.append(f"#{idx}: cloze c{g} hides the bare quantity '{ans}' with nothing visible "
                    f"saying a quantity is wanted — an attributive slot takes an adjective "
                    f"just as readily ('the ___ bones' → short? long? eight?); add a "
                    f"slot-label ::hint naming what is counted (card-rules #27)")
    # an announced list whose items are visible and only a filler word is clozed (R17)
    if fragment_clozed_list(t):
        warn.append(f"#{idx}: the rows of this list are VISIBLE and only a word inside each "
                    f"is hidden — this drills the frames, not the recall; cloze the unit of "
                    f"knowledge or change the archetype (card-rules #22)")
    # too many uncued answers under one number — an all-or-nothing set (R25).
    # A spelled-mnemonic license is a VERIFIED predicate (the hint letters demonstrably
    # spell into a token visible in the stem), so a licensed group is silent, not
    # re-flagged for a human to confirm what the code already proved — the duplicated-
    # predicate smell R14b was written about.
    for g, uncued, total, licensed in overloaded_group(t):
        if licensed:
            continue
        detail = (f"cloze c{g} hides {uncued} answers with no per-item cue"
                  + (f" (of {total} spans)" if total != uncued else ""))
        if uncued >= UNCUED_HARD:
            hard.append(f"#{idx}: {detail} — graded all-or-nothing, so this card fails "
                        f"even when every fact on it is known. CHUNK it into separate "
                        f"NOTES of <=4 (never c1..cN on one note, which reveals the rest) "
                        f"and give each one the full set in Back Extra (card-rules #23)")
        else:
            warn.append(f"#{idx}: {detail} — at the edge of one retrieval; keep it whole "
                        f"ONLY if a mnemonic or a derivable structure makes the set one "
                        f"chunk, else chunk it into separate notes (card-rules #23)")
    # a procedure recited by step number rather than carded as decisions (R30)
    if step_recitation(t):
        warn.append(f"#{idx}: this recites a procedure with every row cued only by its step "
                    f"NUMBER — position is not knowledge, and it is the one shape "
                    f"professional decks never use. Prefer a decision-point vignette (the "
                    f"state in the stem, one blank on the action) or a decision table whose "
                    f"rows are cued by their CONDITIONS. Keep it only if the order genuinely "
                    f"is the knowledge and the set is short (card-rules #26, recipes §12)")
    # a keyed column of NUMBERS that must become one note per key (R28)
    for g, rows in quantitative_panel(t):
        detail = (f"cloze c{g} is a keyed panel of {rows} numeric values hidden together")
        if rows >= QUANT_PANEL_HARD:
            hard.append(f"#{idx}: {detail} — graded all-or-nothing, and an ordered column of "
                        f"numbers gives itself away by interpolation. Split it into one NOTE "
                        f"PER KEY, each asking for a single value, and put the source table "
                        f"in Back Extra so the set stays visible after he answers "
                        f"(card-rules #25)")
        else:
            warn.append(f"#{idx}: {detail} — verify the values do not interpolate from one "
                        f"another; if they trend with the key, split into one note per key "
                        f"(card-rules #25)")
    # a list split across cloze NUMBERS on one note — every card reveals the rest (R26)
    if sibling_split_leak(t):
        hard.append(f"#{idx}: an enumerated list is split across different cloze numbers on "
                    f"ONE note, so each generated card shows the other answers as free "
                    f"context — recoverable by elimination, not recall. Split a list into "
                    f"separate NOTES instead (card-rules #24)")
    # synonym-equation husk — both sides of 'X = also called Y' under one number (R10)
    for g in equation_husk_groups(t):
        warn.append(f"#{idx}: cloze c{g} hides BOTH sides of a synonym/equation ('___ = also called ___') — husk; renumber so each card shows one side as the anchor (card-rules #17)")
    # a single blank hiding a whole clause — fuzzy (R8) or a bloated two-way-def c2 side
    by_group = {}
    for m in CLOZE.finditer(t):
        by_group.setdefault(m.group(1), []).append(m.group(2))
    for g, answers in by_group.items():
        if len(answers) == 1 and len(answers[0].split()) >= LONG_CLOZE_WORDS:
            warn.append(f"#{idx}: cloze c{g} hides {len(answers[0].split())} words in ONE blank — hard to recall verbatim; "
                        f"tighten to the load-bearing words (R8), or if this is a two-way definition, crisp up the c2 meaning side (card-recipes §4)")
    # looks numeric but not flagged. A card that RECORDS what it was verified against is
    # the one legitimate exception, and it is not a bypass: verify_report.py derives the
    # same exemption (`(numeric or weak) and not verified`) and still lists the card in
    # "Section B: verified, skim", so Parker sees it either way. Without this the two
    # scripts disagree on every verified table-derived card and the checker emits a
    # standing false warning — the duplicated-predicate smell R14b was written about.
    if (VALUE.search(readable(t)) and not c.get("needs_human_check")
            and not c.get("verified_against")):
        warn.append(f"#{idx}: looks numeric/dose but needs_human_check is false")
    # stated list-count != number of clozed items (the "7 vs 8 factors" bug).
    # A CHUNKED note (rule 23) legitimately states the FULL set's count while clozing only
    # its own sub-group — "the report's 10 elements … 8. …, 9. …, 10. …" is correct, not an
    # undercount. Its `Roster:` line is the reliable marker, because rule 23 requires one on
    # every note born from a chunk. Without this exemption the two rules fight, and the
    # drafter is pushed into checker-shaped phrasing ("10-element" to dodge the regex)
    # instead of writing what is true — found while chunking the radio report, 2026-08-02.
    m = COUNT_RE.search(readable(t))
    if m and re.search(r"(?:^|>|\s)Roster:", be):
        m = None
    if m:
        stated = NUMWORDS.get(m.group(1).lower(), None)
        if stated is None:
            try:
                stated = int(m.group(1))
            except ValueError:
                stated = None
        if stated and 2 <= stated <= 20:
            # Count members of the dominant cloze group (the list group) and warn only
            # on an UNDERCOUNT — fewer clozed items than the stated number (a dropped
            # list item). An OVERCOUNT is almost always a branch/alternative and is safe.
            gc = {}
            for cm in CLOZE.finditer(t):
                gc[cm.group(1)] = gc.get(cm.group(1), 0) + 1
            dom = max(gc.values()) if gc else 0
            if dom > 1 and dom < stated:
                warn.append(f"#{idx}: says '{m.group(0)}' but clozes only {dom} items "
                            f"— a list item may be missing; verify against the full source page")
    return hard, warn


# --- R13: the grounding check — the first mechanical enforcement of Rule 1 -----------
# "Always ground in the page paragraph" has been the system's #1 rule since day one and
# has never been machine-checked: `grounding: EXACT` only ever meant "I found your marked
# text," never "the claims on this card are supported." A card carrying provenance
# (`from_idx`) can finally be tested against the very context it claims to come from.
#
# The escape valve is deliberate and important: material that lives in an image (a table
# with no text layer, an anatomy plate, a hazmat placard) is legitimately ungroundable in
# text. Such a card passes ONLY if it carries visual evidence — `image` or `visual_source`
# — which is also what makes the grounding auditable months later instead of requiring
# archaeology through agent logs.

GROUND_STOP = set("""a an the of to and or but in on at by for with as is are was were be been being
that this these those it its their his her they you your we our not only also both either
each any some such other more most less least than then when while which who whom whose
into onto from over under above below between within during through across about
can could will would shall should may might must do does did done have has had
very much many few several one two three first second next last same different""".split())


def _stem(w):
    for suf in ("ies", "ing", "es", "ed", "s"):
        if len(w) > 4 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def _content_set(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return {_stem(w) for w in re.findall(r"[a-zA-Z]{3,}", s.lower()) if w not in GROUND_STOP}


PREFIX_MIN = 5


def _supported(word, pool, pool_prefixes):
    """Is this answer-word present in the source pool, allowing for morphology?

    Deliberately GENEROUS. This detector HARD-blocks, so a false positive stops good
    work, while a false negative merely falls through to the LLM judge and the human —
    the same review-not-block contract the husk detectors use. Naive suffix stripping
    already produced one: the source says 'symphyses', the card answers 'symphysis',
    and a strict compare called a correctly-grounded card ungrounded. Prefix matching
    at >=5 characters absorbs that whole class of morphological variation while still
    catching the real target, where the answer word is absent from the source entirely
    ('pectoralis' nowhere in a table CAPTION's context)."""
    if word in pool:
        return True
    if len(word) >= PREFIX_MIN:
        head = word[:PREFIX_MIN]
        if head in pool_prefixes:
            return True
    return False


def highlights_for(cards, explicit=None):
    """Find the highlights file these cards were generated from."""
    if explicit:
        return json.load(open(explicit)), explicit
    src_id = next((c.get("source") for c in cards if c.get("source")), None)
    if not src_id:
        return None, None
    seg = next((c.get("segment", c.get("chapter")) for c in cards
                if c.get("segment") is not None or c.get("chapter") is not None), None)
    try:
        src = S.get_source(src_id)
    except SystemExit:
        return None, None
    noun = S.segment_noun(src).lower()
    label = f"{noun}_{seg}" if seg is not None else "all"
    path = os.path.join(S.SKILL, "work", src_id, f"{label}_highlights.json")
    if os.path.exists(path):
        return json.load(open(path)), path
    return None, None


def _visual_evidence_exists(card, source_root=None):
    """Does this card's claimed visual evidence actually EXIST?

    R13's HARD block is the only mechanical enforcement of Rule 1, and it is skipped for a
    card that carries visual evidence — the material genuinely lives in a picture, so an
    unsupported answer is fine *provided the picture is attached*. But `visual_source` is a
    free-text field the drafter writes itself, so testing only for its presence let any
    card switch off the check by asserting it had. The claim now has to be true: an `image`
    path that resolves, or a `visual_source.figures` entry that resolves under the source's
    work directory. A `visual_source` carrying only prose proves nothing and no longer
    exempts anything."""
    img = card.get("image")
    if img and os.path.exists(img):
        return True
    vs = card.get("visual_source") or {}
    if not isinstance(vs, dict):
        return False
    figs = vs.get("figures") or []
    roots = [r for r in (source_root, os.getcwd()) if r]
    for f in figs:
        if not isinstance(f, str):
            continue
        if os.path.isabs(f) and os.path.exists(f):
            return True
        for r in roots:
            if os.path.exists(os.path.join(r, f)):
                return True
    return False


def grounding_check(cards, highlights, require_provenance=False, source_root=None):
    """(hard, warn) — is every claim supported by the source it cites?"""
    hard, warn = [], []
    if highlights is None:
        return hard, warn
    have_prov = [c for c in cards if c.get("from_idx")]
    if not have_prov:
        if require_provenance:
            hard.append("no card in this file carries `from_idx` — provenance is required "
                        "(see reference/provenance.md). Regenerate with the run store.")
        else:
            warn.append(f"{len(cards)} card(s) carry no `from_idx`, so Rule 1 (grounding) "
                        f"CANNOT be verified for this file — legacy pre-provenance batch")
        return hard, warn

    for i, c in enumerate(cards):
        if c.get("kind") == "lexicon":
            continue  # the purple lane has its own contract — lexicon_check (R35–R37)
        idxs = c.get("from_idx")
        if not idxs:
            msg = f"#{i}: no `from_idx` — grounding unverifiable in a file that otherwise has provenance"
            (hard if require_provenance else warn).append(msg)
            continue
        # The visual exemption must be VERIFIED, not self-asserted. `visual_source` is a
        # free-text field the drafter writes itself, so treating its mere presence as proof
        # let any card opt out of R13's HARD block on every answer by typing a sentence —
        # the one check that enforces Rule 1 could be switched off by the thing it checks.
        # Now the claimed evidence must actually exist on disk (found 2026-08-03 by a
        # drafting agent reading the checker while following the docs).
        visual = _visual_evidence_exists(c, source_root)
        src_text = []
        for j in idxs:
            if isinstance(j, int) and 0 <= j < len(highlights):
                h = highlights[j]
                src_text.append(h.get("context", ""))
                src_text.append(h.get("highlight", ""))
        pool = _content_set(" ".join(src_text))
        pool_prefixes = {w[:PREFIX_MIN] for w in pool if len(w) >= PREFIX_MIN}
        if not pool and not visual:
            hard.append(f"#{i}: cites highlight(s) {idxs} whose context is EMPTY and carries no "
                        f"visual evidence — nothing grounds this card (card-rules Rule 1)")
            continue
        # Does this card cite a mark the extractor already KNOWS is text-insufficient?
        # That is the high-precision case: the material provably lives in an image, so an
        # unsupported claim means the agent read it visually and left no proof. Anything
        # else is a paraphrase judgement call, which belongs to the LLM judge, not a
        # hard block — the same review-not-block contract the husk detectors use.
        cites_visual_gap = any(
            highlights[j].get("needs_visual")
            for j in idxs if isinstance(j, int) and 0 <= j < len(highlights))

        for m in CLOZE.finditer(c.get("Text", "")):
            ans = m.group(2)
            aset = _content_set(ans)
            if not aset:
                continue
            support = sum(1 for w in aset if _supported(w, pool, pool_prefixes)) / len(aset)
            if support > 0 and support >= 0.5:
                continue
            if visual:
                continue  # grounded in an image, and the card carries the proof
            if support == 0 and cites_visual_gap:
                hard.append(
                    f"#{i}: answer {ans[:58]!r} is absent from the text of the mark(s) it cites "
                    f"({idxs}), and that mark is flagged `needs_visual` — the material lives in a "
                    f"table/figure image. Render the page, confirm the fact, and attach the crop "
                    f"via `image`/`visual_source` so the grounding is auditable (Rule 1, R13)")
            elif support == 0:
                warn.append(
                    f"#{i}: answer {ans[:48]!r} appears nowhere in its cited context ({idxs}) "
                    f"— verify it is a paraphrase and not an addition (R13)")
            else:
                warn.append(
                    f"#{i}: answer {ans[:48]!r} is only {support:.0%} supported by its cited "
                    f"context — verify it is a paraphrase and not an addition (R13)")
    return hard, warn


def synthetic_marks_check(cards, highlights):
    """(hard, warn) — cards may cite ONLY extractor-produced marks (R40).

    2026-08-08: a session read Parker's "I've only highlighted a little bit so please
    do this for me" as license to SELECT content itself, appended 99 agent-authored
    'coverage marks' to the highlights file (labeled selected_by: "claude"), and staged
    80 cards he never asked for. He retracted every one: the marks ARE the request —
    yellow says card it, purple says define it, and nothing else is card material,
    however sparse the marking. Sparse marking is a small batch, not a delegation.
    Any mark carrying a provenance key the extractor never writes is synthetic, and a
    card citing it is blocked outright."""
    hard, warn = [], []
    if highlights is None:
        return hard, warn
    synth = {j for j, h in enumerate(highlights) if h.get("selected_by")}
    if not synth:
        return hard, warn
    warn.append(f"highlights file contains {len(synth)} synthetic (non-extractor) mark(s) "
                f"— the extractor never writes `selected_by`; regenerate the file "
                f"(card-rules #29, R40)")
    for i, c in enumerate(cards):
        bad = [j for j in (c.get("from_idx") or []) if j in synth]
        if bad:
            hard.append(f"#{i}: cites synthetic mark(s) {bad} — cards come ONLY from "
                        f"Parker's own marks; the agent never selects content for him "
                        f"(card-rules #29, R40)")
    return hard, warn


def _lexicon_evidence(source_root):
    """work/<source>/lexicon_evidence.json, produced by lexicon.py --find. {} if absent."""
    if not source_root:
        return {}
    p = os.path.join(source_root, "lexicon_evidence.json")
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p)).get("terms", {}) or {}
    except json.JSONDecodeError:
        return {}


def lexicon_check(cards, highlights, source_root=None):
    """(hard, warn) — the PURPLE lane's own grounding contract (card-rules #28).

    A lexicon card's answer is an AUTHORED plain-language definition (Parker: the book's
    formal definition often overcomplicates the thing worth knowing), so R13's
    word-overlap test is the wrong instrument — the source is precisely where the word
    appears UNdefined. What can be mechanical, is:

      * the lane cannot be SELF-asserted: a card's `kind` must agree with the kind of the
        marks it cites, and the marks' kind was set by the EXTRACTOR from the color. A
        yellow-mark card claiming `kind: lexicon` would be dodging R13's word-overlap
        block; a pure-purple card claiming `kind: text` would smuggle an authored
        definition past this contract. Both HARD (R36).
      * a claimed glossary/in_source anchor must RESOLVE to mechanically-extracted
        evidence (lexicon_evidence.json — quote + page written by lexicon.py, never
        typed by the drafter). Same lesson the visual exemption learned (R33 → R37).
      * an `external` anchor (the book never defines the word) must arrive with
        `needs_human_check` — verify_report.py derives it; the gate enforces the two
        scripts agree, so an authored definition can never land unflagged (R35).
    """
    hard, warn = [], []
    if highlights is None:
        return hard, warn
    evidence = _lexicon_evidence(source_root)

    def mark_kinds(idxs):
        return [highlights[j].get("kind") for j in idxs
                if isinstance(j, int) and 0 <= j < len(highlights)]

    for i, c in enumerate(cards):
        idxs = c.get("from_idx") or []
        kinds = mark_kinds(idxs)
        if c.get("kind") != "lexicon":
            if kinds and all(k == "lexicon" for k in kinds):
                hard.append(f"#{i}: cites ONLY purple lexicon mark(s) {idxs} but is not "
                            f"kind: lexicon — a normal card may not be built purely from "
                            f"purple marks (card-rules #28, R36). A fold-in must cite at "
                            f"least one yellow mark.")
            continue

        # ---- kind: lexicon from here on
        if not idxs:
            hard.append(f"#{i}: lexicon card with no `from_idx` — the purple lane always "
                        f"has provenance (card-rules #28)")
            continue
        if any(k != "lexicon" for k in kinds):
            hard.append(f"#{i}: kind: lexicon but cites non-purple mark(s) {idxs} — the "
                        f"lane is set by the extractor's color, never by the drafter "
                        f"(card-rules #28, R36)")
            continue
        lex = c.get("lexicon") or {}
        term, key = lex.get("term"), lex.get("term_key")
        method = (lex.get("anchor") or {}).get("method")
        if not (term and key and method):
            hard.append(f"#{i}: lexicon card missing its contract block — needs "
                        f"lexicon.term, lexicon.term_key, lexicon.anchor.method "
                        f"(card-rules #28)")
            continue
        cited_keys = {highlights[j].get("term_key") for j in idxs
                      if isinstance(j, int) and 0 <= j < len(highlights)}
        if key not in cited_keys:
            hard.append(f"#{i}: lexicon.term_key {key!r} does not match the cited "
                        f"mark's term_key {sorted(k for k in cited_keys if k)} — "
                        f"card/mark drift (card-rules #28)")
            continue
        if method in ("glossary", "in_source"):
            ev = evidence.get(key)
            if not (ev and ev.get("quote") and ev.get("page")):
                hard.append(f"#{i}: anchor claims {method!r} but lexicon_evidence.json "
                            f"has no resolving entry for {key!r} — evidence must be "
                            f"mechanically extracted by lexicon.py --find, never "
                            f"asserted (card-rules #28, R37)")
            elif ev.get("method") != method:
                warn.append(f"#{i}: anchor says {method!r} but the evidence entry says "
                            f"{ev.get('method')!r} — use the evidence's own tier")
        elif method == "external":
            if not c.get("needs_human_check"):
                hard.append(f"#{i}: external-anchored definition without "
                            f"needs_human_check — an authored definition the source "
                            f"cannot confirm must reach Parker's eyes; run "
                            f"verify_report.py before the gate (card-rules #28, R35)")
            if evidence.get(key):
                warn.append(f"#{i}: anchor says external but an in-source definition "
                            f"EXISTS for {key!r} (p{evidence[key].get('page')}) — anchor "
                            f"to it, or record why it does not fit this sense")
        else:
            hard.append(f"#{i}: unknown lexicon anchor method {method!r} — must be "
                        f"glossary, in_source, or external (card-rules #28)")

    # In-batch duplicate keys: the consolidation stage must merge same-sense repeats or
    # sense-split them with a visible domain cue — never ship both blind (card-rules #28).
    seen = {}
    for i, c in enumerate(cards):
        k = (c.get("lexicon") or {}).get("term_key")
        if not k:
            continue
        if k in seen:
            warn.append(f"#{seen[k]} & #{i}: same lexicon term_key {k!r} in one batch — "
                        f"merge if same sense, or add a domain cue to each if the senses "
                        f"differ (card-rules #28)")
        else:
            seen[k] = i
    return hard, warn


def load_live(which, source_id):
    """Pull cards from the live Anki deck(s) for a --live audit.

    The deck to sweep comes from the source registry, so this works for any registered
    source, not just the EMT textbook. `--live all` sweeps the whole source root;
    `--live N` sweeps that segment INCLUDING both the staging deck and the deck Parker
    promotes into, since hand-edit drift happens in whichever one he is studying."""
    def call(action, **params):
        req = urllib.request.Request(
            ANKI, data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
            headers={"Content-Type": "application/json"})
        try:
            res = json.loads(urllib.request.urlopen(req, timeout=30).read())
        except Exception as e:
            sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI}. Is Anki open? ({e})")
        if res.get("error"):
            raise RuntimeError(res["error"])
        return res["result"]
    src = S.get_source(source_id)
    if which == "all":
        query = f'deck:{src["deck_root"]}::*'
    else:
        try:
            seg = int(which)
        except ValueError:
            sys.exit(f"ERROR: --live expects a segment number or 'all', got {which!r}")
        query = f'deck:"{S.audit_deck(src, seg)}"'
    # Suspended notes are out of Parker's rotation, so they are out of scope for a live
    # audit: the question this answers is "what will he actually be shown?" This is also
    # what lets `retire_notes.py` genuinely CLOSE the gate — retirement suspends rather
    # than deletes (his review history and his own edits survive), and a retired note
    # must then stop being reported, or the gate could never go green (card-rules #32).
    query = f"({query}) -is:suspended"
    ids = call("findNotes", query=query)
    notes = call("notesInfo", notes=ids)
    cards = []
    for n in notes:
        f = n["fields"]
        text = f.get("Text", {}).get("value", "")
        cards.append({"noteId": n["noteId"], "Text": text,
                      "Back Extra": f.get("Back Extra", {}).get("value", ""),
                      "needs_human_check": bool(VALUE.search(readable(text)))})
    return cards


def main():
    ap = argparse.ArgumentParser(description="Deterministic gate / live audit for generated cards.")
    ap.add_argument("cards_json", nargs="?", help="staged JSON file to gate (default mode)")
    ap.add_argument("--live", metavar="N|all", help="audit live Anki cards instead of a file (diagnostic; no stamp)")
    ap.add_argument("--source", default=None,
                    help="source id for --live (see: sources.py list). Defaults to the "
                         "cards' own 'source' field in file mode.")
    ap.add_argument("--audit", action="store_true",
                    help="verifying PRE-EXISTING/rich cards: skip the minimal-HTML HARD gate (keep every other "
                         "check). Default (no flag) stays strict so NEW generated cards are held to b/i/br/img.")
    ap.add_argument("--highlights", default=None,
                    help="highlights JSON for the R13 grounding check (default: resolved from the "
                         "cards' source+segment)")
    ap.add_argument("--require-provenance", action="store_true",
                    help="HARD-fail cards missing `from_idx`. Default is lenient so the pre-provenance "
                         "chapter canons still gate; every NEW run should pass this.")
    ap.add_argument("--no-grounding", action="store_true",
                    help="skip the R13 grounding check (escape hatch; do not use for a real run)")
    args = ap.parse_args()
    if not args.cards_json and not args.live:
        sys.exit("usage: check_cards.py [--audit] <cards.json>   |   "
                 "check_cards.py --live <N|all> --source <id>")

    live = bool(args.live)
    strict_html = not (args.audit or live)  # rich pre-existing / hand-edited cards relax the HTML gate
    if live:
        if not args.source:
            sys.exit("ERROR: --live needs --source <id> so it knows which deck to sweep.\n"
                     "See: python3 scripts/sources.py list")
        cards = load_live(args.live, args.source)
        label = [str(c["noteId"]) for c in cards]  # identify by noteId in live mode
    else:
        cards = json.load(open(args.cards_json))
        label = None

    hard, warn, reads = [], [], []
    for i, c in enumerate(cards):
        ident = label[i] if label else i
        h, w = per_card(ident, c, strict_html=strict_html)
        hard += h
        warn += w
        reads.append(readable(c.get("Text", "")))
    # R13 — grounding: every claim supported by the source the card cites (file mode only;
    # a live audit has no provenance link back to the extractor's output).
    ground_note = ""
    if not live and not args.no_grounding:
        hl, hlpath = highlights_for(cards, args.highlights)
        if hl is None:
            ground_note = "  (grounding check skipped: no highlights file found for these cards)"
            if args.require_provenance:
                hard.append("--require-provenance was set but no highlights file could be resolved")
        else:
            _sid = next((c.get('source') for c in cards if c.get('source')), None)
            _root = os.path.join(S.SKILL, 'work', _sid) if _sid else None
            gh, gw = grounding_check(
                cards, hl, args.require_provenance, source_root=_root)
            hard += gh
            warn += gw
            # The purple lane's own contract (card-rules #28, R35–R37) — runs beside
            # R13, never instead of it: lexicon cards skip word-overlap and answer to
            # this; every other card must NOT be built purely from purple marks.
            lh, lw = lexicon_check(cards, hl, source_root=_root)
            hard += lh
            warn += lw
            # Cards come ONLY from Parker's marks — a synthetic (agent-authored) mark
            # in the highlights file blocks every card citing it (card-rules #29, R40).
            sh, sw = synthetic_marks_check(cards, hl)
            hard += sh
            warn += sw
            ground_note = f"  (grounding checked against {os.path.basename(hlpath)})"

    # in-batch near-duplicates.
    # Similar TEXT alone is not duplication. Rule 25 splits a value column into one note
    # per key, which deliberately gives every sibling the SAME stem template and a
    # different answer ("...for a neonate? 100 to 180" / "...for an infant? 100 to 160") —
    # 18 such notes produced 33 false "possible duplicate" warnings on Chapter 7's vitals.
    # The same shape is why Chapter 5's 587 word-root cards have always been noisy here.
    # A real duplicate tests the same FACT, so require the answers to overlap too.
    answers = [{norm(m.group(2)) for m in CLOZE.finditer(c.get("Text", ""))} for c in cards]
    for i in range(len(reads)):
        for j in range(i + 1, len(reads)):
            if len(reads[i]) < 20 or len(reads[j]) < 20:
                continue
            r = SequenceMatcher(None, norm(reads[i]), norm(reads[j])).ratio()
            if r <= 0.82:
                continue
            ai, aj = answers[i], answers[j]
            shared = len(ai & aj) / max(1, min(len(ai), len(aj)))
            if shared < 0.5:
                continue          # same frame, different fact — a split family, not a dupe
            a = label[i] if label else i
            b = label[j] if label else j
            warn.append(f"#{a} & #{b}: {r:.0%} similar Text and {shared:.0%} shared answers "
                        f"— possible duplicate")

    print(f"checked {len(cards)} cards" + (f" (live: {args.live})" if live else ""))
    if ground_note:
        print(ground_note)
    if hard:
        print("HARD ERRORS (block staging):")
        for h in hard:
            print("  x", h)
    if warn:
        print(f"WARNINGS ({len(warn)} — route to the LLM judge / human):")
        for w in warn:
            print("  !", w)
    if not hard and not warn:
        print("  deterministic checks clean")

    if live:
        # A live audit has no staged file to stamp — but "no stamp" is not "no verdict",
        # and reading those two as one thing is the hole this line used to be. The gate
        # protected the staging FILE and never the COLLECTION, so a rule written after a
        # card shipped never reached that card: ten notes that this very checker calls
        # HARD ERRORS sat in his decks for weeks while he studied them, and rules 23 and
        # 25 were both authored FROM those cards. Hard errors now set the exit code,
        # which is what makes --live usable as a gate (smoke_test, or a scheduled sweep)
        # instead of a diagnostic nobody reads. Still never stamps. (card-rules #32, R52)
        sys.exit(1 if hard else 0)

    # Verification stamp: on a HARD-clean pass, write a hash of THIS exact file so
    # anki_write.py can confirm the file it's about to stage is the one that passed
    # the gate. This makes Stage 2.75 physically unskippable (the writer refuses an
    # unstamped/edited file) without any global hook. Warnings don't block the stamp
    # — they're routed to the judge/human, per the pipeline contract.
    src = args.cards_json
    sp = stamp_path(src)
    if hard:
        if os.path.exists(sp):
            os.remove(sp)  # a previously-clean file went dirty; invalidate its stamp
    else:
        with open(sp, "w") as f:
            f.write(json.dumps({"sha256": file_hash(src), "warnings": len(warn)}))
        print(f"  stamped OK -> {os.path.basename(sp)}")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
