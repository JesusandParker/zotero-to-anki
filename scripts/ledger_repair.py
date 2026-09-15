#!/usr/bin/env python3
"""
ledger_repair.py — reconcile the processed-ledger against what is actually in Anki.

WHY THIS EXISTS (2026-09-15)
    detect_pending.py decides what still owes cards by asking one question: is this
    Zotero annotation key in reference/processed-ledger.json? Only two things ever
    advanced that ledger — the 2026-08-26 `--baseline` sweep, and automation/night_shift.py.
    The INTERACTIVE path (Parker says "make cards from genetics ch 10", the pipeline runs,
    anki_write.py writes) never did. So every chapter he asked for by hand stayed
    "pending" forever: 346 of 607 queued marks on the day this was found, with their
    cards sitting live in his collection the whole time. Re-running any of those units
    would have duplicated a whole chapter, and the real backlog was invisible underneath
    the phantom one.

    anki_write.py now advances the ledger itself (see advance_ledger, R66). This tool is
    the repair for everything written before that, and the standing audit afterwards.

WHAT IT TRUSTS
    Not the run manifest, which can say "complete" for a run whose notes were deleted,
    and not `added: N/N`, which is the exact claim R65 caught lying. A mark is recorded
    as carded only when a note that a run's provenance links to it RESOLVES IN THE
    COLLECTION RIGHT NOW. Verify the surface, not the call.

    The chain per mark is: runs/<source>/<seg>/<run>/highlights.json[i].zotero_key
    -> provenance.jsonl record whose from_idx contains i -> its anki_note_id
    -> notesInfo says that note exists.

USAGE
    python3 scripts/ledger_repair.py              # audit; prints the drift, writes nothing
    python3 scripts/ledger_repair.py --apply      # record the confirmed marks
    python3 scripts/ledger_repair.py --source emt # one source only
"""
import argparse, json, os, sys, urllib.request
from collections import defaultdict

import detect_pending as DP
import sources as S

RUNS = os.path.join(S.SKILL, "runs")
ANKI = "http://localhost:8765"


def call(action, **params):
    req = urllib.request.Request(
        ANKI, json.dumps({"action": action, "version": 6, "params": params}).encode(),
        {"Content-Type": "application/json"})
    try:
        res = json.load(urllib.request.urlopen(req, timeout=60))
    except Exception as e:
        sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI} ({e}). Anki must be running "
                 f"— this tool refuses to guess whether a note exists.")
    if res.get("error"):
        sys.exit(f"ERROR from AnkiConnect on {action}: {res['error']}")
    return res["result"]


def live_notes(nids):
    """Which of these note ids actually resolve? Chunked: notesInfo on thousands at once
    is one request the add-on can drop, and a dropped request would read as 'all gone'."""
    live = set()
    for i in range(0, len(nids), 500):
        for r in call("notesInfo", notes=nids[i:i + 500]) or []:
            if isinstance(r, dict) and r.get("noteId"):
                live.add(r["noteId"])
    return live


def scan(source_filter=None):
    """Every (source, segment) -> the marks whose cards are provably live in Anki."""
    confirmed = defaultdict(set)      # (source, segment) -> {zotero_key}
    orphaned = defaultdict(set)       # cards the run claims but Anki does not have
    for root, _dirs, files in os.walk(RUNS):
        if "provenance.jsonl" not in files or "highlights.json" not in files:
            continue
        man = os.path.join(root, "manifest.json")
        m = json.load(open(man)) if os.path.exists(man) else {}
        src = m.get("source") or os.path.relpath(root, RUNS).split(os.sep)[0]
        if source_filter and src != source_filter:
            continue
        seg = m.get("segment")
        keys = [h.get("zotero_key") for h in json.load(open(os.path.join(root, "highlights.json")))]
        by_nid = defaultdict(set)
        for line in open(os.path.join(root, "provenance.jsonl")):
            if not line.strip():
                continue
            p = json.loads(line)
            nid = p.get("anki_note_id")
            if not nid:
                continue
            for i in p.get("from_idx") or []:
                if 0 <= i < len(keys) and keys[i]:
                    by_nid[nid].add(keys[i])
        if not by_nid:
            continue
        alive = live_notes(list(by_nid))
        for nid, ks in by_nid.items():
            (confirmed if nid in alive else orphaned)[(src, seg)] |= ks
    # A mark carded twice (a chapter re-run) is confirmed if ANY of its notes survives.
    for k in confirmed:
        orphaned[k] -= confirmed[k]
    return confirmed, orphaned


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="record the confirmed marks in the ledger (default: audit only)")
    ap.add_argument("--source", help="restrict to one registered source id")
    args = ap.parse_args()

    ledger = DP.processed_keys()
    confirmed, orphaned = scan(args.source)

    gaps = {k: sorted(v - ledger) for k, v in confirmed.items()}
    gaps = {k: v for k, v in gaps.items() if v}

    if not gaps:
        print("ledger is in sync: every mark with a live card is already recorded.")
    else:
        total = sum(len(v) for v in gaps.values())
        print(f"{total} mark(s) have live cards in Anki but are missing from the ledger.")
        print("detect_pending is queueing them as work that is already done.\n")
        for (src, seg), ks in sorted(gaps.items(), key=lambda x: (x[0][0], x[0][1] or 0)):
            print(f"  {src:10} segment {str(seg):>4}  {len(ks):4} mark(s)")

    lost = {k: sorted(v) for k, v in orphaned.items() if v}
    if lost:
        print(f"\n{sum(len(v) for v in lost.values())} mark(s) have a run record whose note "
              f"is GONE from the collection — genuinely still pending, left alone:")
        for (src, seg), ks in sorted(lost.items(), key=lambda x: (x[0][0], x[0][1] or 0)):
            print(f"  {src:10} segment {str(seg):>4}  {len(ks):4} mark(s)")

    if not gaps:
        return
    if not args.apply:
        print("\nthis was an audit; re-run with --apply to record them.")
        return

    for (src, seg), ks in sorted(gaps.items()):
        DP.mark_processed(ks, src, f"ledger_repair::{src}-{seg}",
                          note="backfill: card verified live in the collection")
        print(f"  recorded {len(ks):4} mark(s) for {src} segment {seg}")
    after = DP.processed_keys()
    missed = [k for v in gaps.values() for k in v if k not in after]
    if missed:
        sys.exit(f"ERROR: {len(missed)} key(s) did not persist in the ledger: {missed[:10]}")
    print(f"\nledger now holds {len(after)} key(s); re-read it and every one is there.")


if __name__ == "__main__":
    main()
