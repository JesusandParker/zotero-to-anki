#!/usr/bin/env python3
"""Self-test for check_block_spec.py — 'a checker that has never failed has never been tested.'

The GOOD fixture is a minimal set satisfying every accumulated requirement; the BAD fixture
reconstructs the actual defects Parker caught on 2026-08-08 (missing LRM, duplicate play
button, boilerplate cue, uppercase media, one-way vocab, the original property-less one-way
country card with no membership lane). The suite fails if the checker passes any BAD case
or flags the GOOD set. When adding a rule to check_block_spec.py, add its defect here too.
"""
import subprocess, sys, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(f):
    p = subprocess.run([sys.executable, os.path.join(H, "scripts/check_block_spec.py"),
                        os.path.join(H, f)], capture_output=True, text=True)
    return p.returncode, p.stdout
fails = []
rc, out = run("reference/fixtures/block_spec_good.json")
if rc != 0:
    fails.append("GOOD fixture was flagged:\n" + out)
rc, out = run("reference/fixtures/block_spec_bad.json")
if rc == 0:
    fails.append("BAD fixture PASSED — the checker caught nothing")
else:
    for must in ("U1-lrm", "U3-no-dup-audio", "U4-no-boilerplate", "U2-media-lower",
                 "V1-two-way", "C1-property", "C2-two-way", "C3-roster", "C4-membership"):
        if must not in out:
            fails.append(f"BAD fixture: rule {must} did not fire")
# A file from a DIFFERENT source, containing none of the governed blocks, must pass —
# set-level rules are scoped to files that contain their block. The defect this pins:
# C4/C5 fired as false REGRESSIONS on EMT chapter 8 (2026-08-12), the first non-Arabic
# file through the checker, because the set-level tests ran unscoped on every file.
rc, out = run("reference/fixtures/block_spec_other_source.json")
if rc != 0:
    fails.append("OTHER-SOURCE fixture was flagged — set-level rules leaked across sources:\n" + out)
if fails:
    print("test_block_spec: FAIL"); [print(" -", f) for f in fails]; sys.exit(1)
print("test_block_spec: good fixture passes, bad fixture trips every rule ✓")
