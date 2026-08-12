#!/usr/bin/env python3
"""Cumulative per-block REQUIREMENTS checker.

Why this exists (2026-08-08, Arabic Unit 1): across four rounds of Parker's feedback, each
fix satisfied the newly-named defect and silently REGRESSED an earlier one. The country
cards went one-way -> two-way -> (adding the 'Arabic-speaking' property) back to one-way,
because the two-way requirement lived only in a past conversation, not in any artifact the
next rebuild had to satisfy.

`check_cards.py` asks "is this card well-formed?". This asks the other question:
**"does this card still satisfy every requirement Parker has ever established for its
block?"** Requirements only ever get ADDED here. A rebuild that drops one fails.

Usage:  python3 scripts/check_block_spec.py work/<source>/<file>_cards.json
"""
import json, re, sys, collections

def clozes(t):
    """{number: [answers]} for a card's Text."""
    out = collections.defaultdict(list)
    for n, a in re.findall(r'\{\{c(\d+)::(.*?)(?:::.*?)?\}\}', t, re.S):
        out[int(n)].append(a)
    return out

# ---------------------------------------------------------------------------
# Each rule: (id, applies-to predicate, test, message). Requirements ACCUMULATE.
# Every one traces to a specific thing Parker asked for; the date is when he asked.
# ---------------------------------------------------------------------------
def has(sub):      return lambda c: sub in c["Text"]
def block(*names): return lambda c: c.get("block") in names

def is_member_card(c):
    """A per-member card of a property-defined set: not the anchor, not a roster note.

    Deliberately structural. A predicate that keys on the feature being tested cannot
    catch that feature's removal — the failure that made the first version of C2 useless.
    """
    if c.get("block") != "G_countries":
        return False
    t = c["Text"]
    if "map shows" in t:                                   # the anchor note
        return False
    if re.search(r'countries in .+\(\d+\)', t):            # a roster note
        return False
    return True

RULES = [
 # --- universal -----------------------------------------------------------
 ("U1-lrm  (2026-08-08, R44)", lambda c: bool(re.match(r'\s*\{\{c\d+::[؀-ۿ]', c["Text"])),
  lambda c: c["Text"].startswith("‎"),
  "Arabic-first Text must begin with U+200E LRM or the whole card renders RTL"),

 ("U2-media-lower (2026-08-08, R47)", lambda c: True,
  lambda c: all(m == m.lower() for m in re.findall(r'\[sound:([^\]]+)\]|<img src="([^"]+)"',
                                                   c["Text"] + c["Back Extra"]) for m in [m[0] or m[1]] if m),
  "media filenames must be lowercase (case-sensitive on iOS)"),

 ("U3-no-dup-audio (2026-08-08)", block("A_letters", "C_vocab"),
  lambda c: "[sound:" not in c["Back Extra"] or "vocab" in c["Back Extra"],
  "the Audio-field clip must not ALSO sit in Back Extra (two play buttons)"),

 ("U4-no-boilerplate (2026-08-08)", lambda c: True,
  lambda c: "hear it and watch the mouth" not in c["Back Extra"],
  "no filler cue lines restating what the card obviously does"),

 # --- letters -------------------------------------------------------------
 ("L1-two-way (2026-08-08)", block("A_letters"),
  lambda c: set(clozes(c["Text"])) == {1, 2},
  "letter notes are two-way: c1 = produce the glyph, c2 = name + sound"),

 # --- symbols -------------------------------------------------------------
 ("S1-two-way (2026-08-08)", lambda c: c.get("block") == "B_symbols" and "{{c2::" in c["Text"],
  lambda c: set(clozes(c["Text"])) == {1, 2},
  "symbol notes are two-way: c1 = produce the mark, c2 = name"),

 # --- vocab ---------------------------------------------------------------
 ("V1-two-way (2026-08-08)", block("C_vocab"),
  lambda c: set(clozes(c["Text"])) == {1, 2},
  "vocab notes are two-way: c1 = produce the Arabic, c2 = produce the meaning"),
 ("V2-dialects (2026-08-08)", block("C_vocab"),
  lambda c: "Cue: MSA" in c["Back Extra"],
  "vocab notes name the MSA register (the course tests Formal)"),

 # --- countries / any property-defined set --------------------------------
 # the property may be named in the book's own words ("where Arabic is the main language")
 # or in the shorthand — what is forbidden is a stem that names neither.
 ("C1-property (2026-08-08, R49)", block("G_countries"),
  lambda c: "Arabic-speaking" in c["Text"] or "Arabic is the main language" in c["Text"],
  "every card from a property-defined set names the property in its stem"),
 # NB: this predicate must NOT key on the structure it is checking for. An earlier version
 # applied only when "its capital:" was in the Text — so the very regression it existed to
 # catch (collapsing to a one-way card without that line) made the rule silently inapplicable.
 # Identify member cards structurally instead: a countries card that is neither anchor nor roster.
 ("C2-two-way (2026-08-08)",
  lambda c: is_member_card(c) and "same name" not in c["Text"],
  lambda c: set(clozes(c["Text"])) == {1, 2},
  "member notes quiz BOTH ways: country from capital, AND capital from country"),
 ("C3-roster (2026-08-08, R48)", lambda c: c.get("block") == "G_countries"
                                           and "map shows" not in c["Text"],
  lambda c: "Roster:" in c["Back Extra"],
  "every note born of a chunked set carries the full Roster: with its members bolded"),
 ("C4-membership (2026-08-08, R48)", lambda c: False, lambda c: True, ""),  # set-level, below
]

# A set-level rule governs one specific block, so it may only judge a file that CONTAINS
# that block: the requirement "the countries set keeps its membership lane" says nothing
# about a chemistry chapter. Without the scope predicate these fired as false REGRESSIONS
# on the first non-Arabic file ever run through the checker (EMT ch8, 2026-08-12) —
# cross-source scope leakage, the exact class CLAUDE.md's scope reminder warns about.
# Each entry: (id, scope(cards) -> this file is governed, test(cards), message).
SET_LEVEL = [
 ("C4-membership (2026-08-08, R48)",
  lambda cards: any(c.get("block") == "G_countries" for c in cards),
  lambda cards: sum(1 for c in cards if c.get("block") == "G_countries"
                    and re.search(r'countries in .+\(\d+\)', c["Text"])) >= 3,
  "a marked SET needs a membership lane (>=3 roster notes), not only row cards"),
 ("C5-anchor (2026-08-08, R48)",
  lambda cards: any(c.get("block") == "G_countries" for c in cards),
  lambda cards: any(c.get("block") == "G_countries" and "map shows" in c["Text"] for c in cards),
  "the membership lane needs an anchor note naming the sub-groups"),
]

def main(path):
    cards = json.load(open(path))
    fails = []
    for i, c in enumerate(cards):
        for rid, applies, test, msg in RULES:
            if not msg:
                continue
            try:
                if applies(c) and not test(c):
                    fails.append(f"  [{rid}] card #{i} ({c.get('block')}): {msg}\n"
                                 f"      {c['Text'][:90]}")
            except Exception as e:                      # a broken rule must not pass silently
                fails.append(f"  [{rid}] card #{i}: RULE ERROR {e}")
    for rid, scope, test, msg in SET_LEVEL:
        if scope(cards) and not test(cards):
            fails.append(f"  [{rid}] SET-LEVEL: {msg}")

    print(f"block-spec: checked {len(cards)} cards against "
          f"{len([r for r in RULES if r[3]]) + len(SET_LEVEL)} accumulated requirements")
    if fails:
        print(f"\nREGRESSIONS ({len(fails)}) — a requirement Parker already established is no longer met:")
        print("\n".join(fails))
        return 1
    print("  all requirements still satisfied ✓")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
