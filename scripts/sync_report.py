#!/usr/bin/env python3
"""
sync_report.py — read the difference between what was generated and what Parker actually
keeps, and treat that difference as feedback.

The naive framing is "the canon has drifted from Anki, resync it." That is wrong. Drift is
HEALTHY: Parker deletes cards he doesn't want, edits wording on his phone, and promotes
keepers. Forcing the two back into agreement would destroy the most honest quality signal
the system has.

Because when Parker EDITS a card, that edit is better feedback than any complaint — he has
already done the work of showing the correct version. Right now that is completely
invisible: nothing ever compares the generated card to the card as it now exists.

So this classifies divergence by MEANING:

    in canon, missing from Anki   -> he REJECTED it        -> selection/yield feedback
    text differs                  -> he CORRECTED it       -> card-craft feedback; the diff IS the lesson
    in Anki, not in canon         -> he WROTE it himself   -> a pattern worth imitating

Usage:
    python3 scripts/sync_report.py --source emt                 # every segment
    python3 scripts/sync_report.py --source emt --segment 4
    python3 scripts/sync_report.py --source emt --segment 4 --out work/emt/ch4_sync.md
"""
import argparse, difflib, glob, json, os, re, sys, unicodedata, urllib.request

import sources as S

ANKI = "http://localhost:8765"
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")


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


def readable(t):
    t = CLOZE.sub(lambda m: m.group(2), t)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


def key(t):
    return re.sub(r"[^a-z0-9 ]", "", unicodedata.normalize("NFKC", readable(t)).lower()).strip()


def compare(canon, live):
    """Classify every card as identical / edited / rejected / hand-written."""
    live_by = {key(n["fields"]["Text"]["value"]): n for n in live}
    canon_by = {key(c.get("Text", "")): c for c in canon}
    same, edited, rejected, handwritten = [], [], [], []
    used = set()

    for c in canon:
        k = key(c.get("Text", ""))
        if k in live_by:
            same.append(c); used.add(k); continue
        # fuzzy: same card, reworded by Parker
        best, score = None, 0.0
        for lk, n in live_by.items():
            if lk in used:
                continue
            r = difflib.SequenceMatcher(None, k, lk).ratio()
            if r > score:
                best, score = n, r
        if best is not None and score >= 0.70:
            edited.append((c, best, score)); used.add(key(best["fields"]["Text"]["value"]))
        else:
            rejected.append(c)

    for n in live:
        if key(n["fields"]["Text"]["value"]) not in used and \
           key(n["fields"]["Text"]["value"]) not in canon_by:
            handwritten.append(n)
    return same, edited, rejected, handwritten


def word_diff(a, b):
    aw, bw = readable(a).split(), readable(b).split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw).get_opcodes():
        if tag == "equal":
            continue
        if tag in ("replace", "delete"):
            out.append(f"-{' '.join(aw[i1:i2])}")
        if tag in ("replace", "insert"):
            out.append(f"+{' '.join(bw[j1:j2])}")
    return "  ".join(out)[:300]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    src = S.get_source(args.source)
    noun = S.segment_noun(src).lower()
    files = ([os.path.join(S.SKILL, "work", src["id"], f"{noun}_{args.segment}_cards.json")]
             if args.segment is not None
             else sorted(glob.glob(os.path.join(S.SKILL, "work", src["id"], "*_cards.json"))))

    report = [f"# {src['id']} — generated vs. kept", "",
              "What Parker changed after the cards were staged. Every line here is feedback:",
              "a rejection is selection signal, an edit is card-craft signal.", ""]
    totals = dict(same=0, edited=0, rejected=0, handwritten=0)

    for path in files:
        if not os.path.exists(path):
            print(f"  (no canon file: {path})"); continue
        canon = json.load(open(path))
        seg = next((c.get("segment", c.get("chapter")) for c in canon
                    if c.get("segment") is not None or c.get("chapter") is not None), None)
        deck = S.audit_deck(src, seg)
        ids = call("findNotes", query=f'deck:"{deck}"')
        live = call("notesInfo", notes=ids) if ids else []
        same, edited, rejected, handwritten = compare(canon, live)
        for k, v in (("same", same), ("edited", edited), ("rejected", rejected), ("handwritten", handwritten)):
            totals[k] += len(v)

        print(f"  {os.path.basename(path):<28} {len(same):>4} unchanged  {len(edited):>3} edited  "
              f"{len(rejected):>3} rejected  {len(handwritten):>3} hand-written   ({deck})")

        if not (edited or rejected or handwritten):
            continue
        report += [f"## {os.path.basename(path)} — `{deck}`", ""]
        if edited:
            report += [f"### Corrected by Parker ({len(edited)}) — the diff is the lesson", ""]
            for c, n, score in edited:
                report += [f"- **{readable(n['fields']['Text']['value'])[:120]}**",
                           f"    - changes: `{word_diff(c.get('Text',''), n['fields']['Text']['value'])}`", ""]
        if rejected:
            report += [f"### Rejected ({len(rejected)}) — generated, then deleted", "",
                       "Ask what these have in common; that is a yield/selection rule waiting to be written.", ""]
            for c in rejected:
                report += [f"- {readable(c.get('Text',''))[:140]}"]
            report += [""]
        if handwritten:
            report += [f"### Written by Parker himself ({len(handwritten)}) — imitate these", ""]
            for n in handwritten:
                report += [f"- {readable(n['fields']['Text']['value'])[:140]}"]
            report += [""]

    print(f"\n  TOTAL  {totals['same']} unchanged · {totals['edited']} edited · "
          f"{totals['rejected']} rejected · {totals['handwritten']} hand-written")
    if args.out:
        with open(args.out, "w") as f:
            f.write("\n".join(report) + "\n")
        print(f"  -> {args.out}")
    elif totals["edited"] or totals["rejected"]:
        print("\n  (pass --out <file.md> to write the full report with diffs)")


if __name__ == "__main__":
    main()
