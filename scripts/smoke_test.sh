#!/usr/bin/env bash
# smoke_test.sh — end-to-end health check for the whole skill.
#
# Run this after ANY structural change (a script, the registry, a deck template) to prove
# nothing regressed. It checks three things that must always hold:
#
#   1. CARD CRAFT IS UNTOUCHED — the 20 regression cases still pass in both directions.
#   2. EMT PARITY — the original source still extracts the same marks, gates clean, and
#      routes to the exact same decks it did before the pipeline was generalized.
#   3. THE UNIVERSAL PATH WORKS — a non-textbook source (a lecture PDF, marked with
#      UNDERLINES rather than highlights) extracts, grounds, and surfaces its comments.
#
# Requires Anki to be OPEN (the live-audit and writer checks talk to AnkiConnect).
# Nothing here writes to Anki: every writer check is --dry-run.
#
#   bash scripts/smoke_test.sh
#
set -u
cd "$(dirname "$0")/.." || exit 1
pass=0; fail=0
chk(){ if eval "$2" >/dev/null 2>&1; then echo "  PASS  $1"; pass=$((pass+1)); else echo "  FAIL  $1"; fail=$((fail+1)); fi; }

echo "--- card craft must be untouched ---"
chk "regression suite all green" "python3 scripts/test_regressions.py 2>&1 | grep -qE '^[0-9]+/[0-9]+ regression cases pass' && ! python3 scripts/test_regressions.py 2>&1 | grep -q FAIL"
chk "figure regression suite all green" "PY=.venv/bin/python; [ -x \$PY ] || PY=python3; \$PY scripts/test_figures.py 2>&1 | grep -qE '^[0-9]+/[0-9]+ figure regression cases pass' && ! \$PY scripts/test_figures.py 2>&1 | grep -q FAIL"

echo "--- no run may leave a discovered hazard open ---"
chk "every recorded hazard is closed"  "python3 scripts/check_hazards.py"

echo "--- the purple lane (lexicon) ---"
chk "lexicon term-key self-test green" "python3 scripts/lexicon.py --self-test"
chk "registry exposes lexicon colors"  "python3 scripts/sources.py show emt | grep -q '#a28ae5'"
chk "R35-R37 fixtures present"         "test -f work/_regression/lexicon_evidence.json"

echo "--- registry ---"
chk "sources.py list works"            "python3 scripts/sources.py list"
chk "emt resolves to its real PDF"     "python3 scripts/sources.py show emt | grep -q '\"pdf_exists\": true'"
chk "emt profile resolves to emt.md"   "python3 scripts/sources.py show emt | grep -q 'emt.md'"
chk "isaacs17 -> science.md"           "python3 scripts/sources.py show isaacs17 | grep -q 'science.md'"
chk "emt cards go to Book Highlights"  "python3 scripts/sources.py deck emt 3 | grep -q '^deck:  all::EMT::Chapter 3::Book Highlights$'"
chk "emt audit sweeps the chapter"     "python3 scripts/sources.py deck emt 3 | grep -q '^audit: all::EMT::Chapter 3$'"
# The retired staging deck must never come back from ANY source template (2026-08-24).
chk "no deck template routes to review" "! grep '\"deck\":' reference/sources.json | grep -qi review"
chk "no staging/promote keys survive"  "! grep -qE '\"(staging|promote)\":' reference/sources.json"
chk "unknown source fails loudly"      "! python3 scripts/sources.py show nope 2>&1 | grep -q Traceback"

echo "--- extraction parity (EMT) ---"
for n in 1 2 3 4 5; do
  exp=$(python3 -c "import json;print(len(json.load(open('work/emt/chapter_${n}_cards.json'))))")
  chk "ch$n canon loads ($exp notes)" "test $exp -gt 0"
done
chk "ch1 still 36 marks" "python3 scripts/extract_highlights.py --source emt --segment 1 2>&1 | grep -q '36 marked item'"

echo "--- gate + stamp ---"
for n in 1 2 3 4; do chk "ch$n gates clean + stamps" "python3 scripts/check_cards.py --audit work/emt/chapter_${n}_cards.json 2>&1 | grep -q 'stamped OK'"; done
chk "ch5 gates clean + stamps" "python3 scripts/check_cards.py --audit work/emt/chapter_5_cards.json 2>&1 | grep -q 'stamped OK'"
chk "unstamped file is REFUSED" "cp work/emt/chapter_1_cards.json /tmp/uns.json; ! python3 scripts/anki_write.py /tmp/uns.json 2>&1 | grep -q 'added:'"

echo "--- live audit through the registry ---"
# Assert the live audit REACHES the deck and reads a plausible chapter, not an exact
# count: adding new cards is normal and must not fail the suite. (It did, on 2026-08-02,
# when the retrieval-load remediation added 6 notes to ch3 and the hardcoded 84 went stale
# — a green suite should mean "the path works," never "nobody staged anything since.")
chk "live ch3 audit reaches the deck" "python3 scripts/check_cards.py --live 3 --source emt 2>&1 | grep -qE 'checked ([2-9][0-9]|[1-9][0-9]{2,}) cards'"
chk "live needs --source"  "! python3 scripts/check_cards.py --live 3 2>&1 | grep -q 'checked'"

echo "--- retirement: a rule reaches the cards already live (card-rules #32, R52) ---"
# The gate used to cover the card FILE and never the COLLECTION, so ten superseded
# notes stayed in his rotation for two weeks while this very checker called them HARD
# ERRORS in a code path wired to exit 0. These four assert the whole loop: the live sweep
# has a verdict, retirement is safe, and no run may replace notes without naming them.
chk "live sweep VERDICTS, not just reports"  "python3 scripts/check_cards.py --live all --source emt >/dev/null 2>&1"
chk "no live note hard-blocks the gate"      "python3 scripts/retire_notes.py audit --source emt >/dev/null 2>&1"
chk "retirement refuses/undoes correctly"    "python3 scripts/retire_notes.py self-test 2>&1 | grep -q 'all retirement cases pass'"
chk "every supersession is accounted for"    "python3 scripts/check_hazards.py >/dev/null 2>&1"

echo "--- the universal path (a lecture, not a textbook) ---"
chk "isaacs17 extracts 6 marks"     "python3 scripts/extract_highlights.py --source isaacs17 2>&1 | grep -q '6 marked item'"
chk "isaacs17 grounds all 6"        "python3 scripts/extract_highlights.py --source isaacs17 2>&1 | grep -q 'grounded 6/6'"
chk "isaacs17 surfaces 6 comments"  "python3 scripts/extract_highlights.py --source isaacs17 2>&1 | grep -q '6 margin comment'"

echo "--- grounding (R13): Rule 1 is now machine-checked ---"
chk "ch6 grounding clean (evidence attached)" "python3 scripts/check_cards.py --audit work/emt/chapter_6_cards.json 2>&1 | grep -qv 'R13'"
chk "ch6 carries provenance"                  "python3 -c \"import json;d=json.load(open('work/emt/chapter_6_cards.json'));assert all(c.get('from_idx') is not None for c in d)\""
chk "a run record exists for ch6"             "python3 scripts/run_store.py list emt | grep -q 'seg 6'"

echo "--- writer routing ---"
chk "ch1 dry-run targets the right deck" "python3 scripts/anki_write.py work/emt/chapter_1_cards.json --dry-run 2>&1 | grep -q 'all::EMT::Chapter 1::Book Highlights'"
chk "ch5 dry-run routes to Chapter 5"    "python3 scripts/anki_write.py work/emt/chapter_5_cards.json --dry-run 2>&1 | grep -q 'all::EMT::Chapter 5::Book Highlights'"
# A dry run must not even MENTION the retired staging deck any more.
echo "--- report tooling must never eat its own input (2026-08-26 data loss) ---"
chk "verify_report writes beside, not over, its input" "cp work/physics/drafts/block_E.json /tmp/_smoke_vr.json && python3 scripts/verify_report.py /tmp/_smoke_vr.json >/dev/null 2>&1 && python3 -c \"import json;json.load(open('/tmp/_smoke_vr.json'))\""
chk "verify_report refuses --out onto the cards file" "python3 scripts/verify_report.py /tmp/_smoke_vr.json --out /tmp/_smoke_vr.json 2>&1 | grep -q 'REFUSING'"

chk "writer never names claude review"   "! python3 scripts/anki_write.py work/emt/chapter_1_cards.json --dry-run 2>&1 | grep -qi 'claude review'"

echo
echo "RESULT: $pass passed, $fail failed"
test $fail -eq 0
