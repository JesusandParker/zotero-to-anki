#!/usr/bin/env python3
"""
figure_run.py — check a figure run before it starts, and diagnose it after it finishes.

The figure pipeline is five stages across four scripts, and its evidence ends up spread
over an index, a proposals file, a verdicts file, an undo record and the live deck. That
is fine while one session holds it all in mind and useless afterwards. This reads those
artifacts back and says what actually happened.

    python3 figure_run.py --source emt --segment 7 --preflight
    python3 figure_run.py --source emt --segment 7 --report
    python3 figure_run.py --source emt --segment 7 --report --write-run

`--preflight` is the "am I ready" check: the things that have silently broken before, each
asserted rather than assumed. `--report` is the post-mortem: every stage's count, the
attrition between them, and a list of ANOMALIES — the numbers that historically meant
something was wrong. `--write-run` files the result in the run store so it survives the
session.

The anomaly thresholds are not invented. Each one is a defect that actually happened:
see reference/regression-cases.md R15-R23 and runs/emt/*/2026-07-30-figures/REPORT.md.
"""
import argparse, json, os, re, subprocess, sys
import sources as S

# Every chapter finished so far, so a new one has something to be compared against.
BASELINE = {  # segment: (cards, figures indexed, attached)
    1: (32, 9, 2), 2: (89, 34, 10), 3: (84, 13, 4),
    4: (105, 23, 16), 5: (587, 9, 8), 6: (202, 47, 51),
}


def load(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


def anki(action, **params):
    import urllib.request
    try:
        req = urllib.request.Request(
            "http://localhost:8765",
            json.dumps({"action": action, "version": 6, "params": params}).encode(),
            headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=30).read()).get("result")
    except Exception:
        return None


def preflight(src, seg, work):
    ok, bad = [], []

    def chk(cond, good, why):
        (ok if cond else bad).append(good if cond else why)

    chk(os.path.exists(os.path.join(S.SKILL, ".venv", "bin", "python")),
        "skill venv present (PyMuPDF)",
        "NO .venv — build_figure_index needs PyMuPDF: "
        "python3 -m venv .venv && .venv/bin/pip install PyMuPDF")
    chk(subprocess.run(["which", "magick"], capture_output=True).returncode == 0,
        "ImageMagick present (matting / study copies)", "NO `magick` on PATH")
    chk(anki("version") is not None, "Anki is running (AnkiConnect)",
        "Anki is NOT running — attaching and judging --strip-live both need it")

    _id, pdf = S.resolve_attachment(src)
    chk(os.path.exists(pdf), "source PDF resolves on disk", f"PDF missing: {pdf}")

    hl = load(os.path.join(work, f"{S.work_label(src, seg)}_highlights.json"))
    chk(bool(hl), f"highlights extracted ({len(hl) if hl else 0} marks)",
        "no highlights file — run extract_highlights.py first")
    if hl:
        chk(all("kind" in m for m in hl), "highlights use the modern schema",
            "highlights predate the kind/content/needs_visual fields — re-extract")

    cards = load(os.path.join(work, f"{S.work_label(src, seg)}_cards.json"))
    fresh = cards is None
    chk(True, f"cards: {'NOT YET GENERATED (fresh segment)' if fresh else str(len(cards)) + ' present'}", "")
    if cards:
        placed = sum(1 for c in cards if c.get("from_idx") or c.get("source_page"))
        chk(placed >= 0.75 * len(cards),
            f"cards placeable on a page ({placed}/{len(cards)})",
            f"only {placed}/{len(cards)} cards can be placed on a page — the matcher needs "
            f"from_idx or source_page; run backfill_provenance.py")

    idx = load(os.path.join(work, "figure_index.json"))
    if idx:
        first, last, _n = S.segment_range(src, seg)
        mine = [f for f in idx["figures"] if first <= f["caption_page"] <= last]
        chk(bool(mine), f"figure index covers this segment ({len(mine)} figures)",
            "figure_index.json has no figures in this segment's page range — "
            "run build_figure_index.py --segment N")
        if mine:
            nostudy = [f["label"] for f in mine if not f.get("study_file")]
            chk(not nostudy, "every figure has a matted study copy",
                f"no study copy for {nostudy[:5]} — rerun build_figure_index.py")
            vec = [f["label"] for f in mine if f.get("extraction") == "vector-render"]
            if vec:
                ok.append(f"NOTE: {len(vec)} vector-rendered figure(s) {vec[:4]} — this path "
                          f"has never run on a real chapter; eyeball those crops")
    else:
        bad.append("no figure_index.json — run build_figure_index.py")

    print(f"PREFLIGHT — {src['id']} segment {seg}\n")
    for m in ok:
        if m:
            print(f"  ok    {m}")
    for m in bad:
        print(f"  MISS  {m}")
    print(f"\n  {len(bad)} blocker(s)." if bad else "\n  ready.")
    return 1 if bad else 0


def report(src, seg, work, write_run=False):
    first, last, segname = S.segment_range(src, seg)
    hl = load(os.path.join(work, f"{S.work_label(src, seg)}_highlights.json")) or []
    cards = load(os.path.join(work, f"{S.work_label(src, seg)}_cards.json")) or []
    idx = load(os.path.join(work, "figure_index.json")) or {"figures": []}
    figs = [f for f in idx["figures"] if first <= f["caption_page"] <= last]
    props = load(os.path.join(work, f"ch{seg}_figure_proposals.json")) or {}
    verd = load(os.path.join(work, f"ch{seg}_judge_verdicts.json"))

    kept = len(props.get("teaches", [])) + len(props.get("context", []))
    rejected = len(props.get("rejected", []) or [])
    proposed = kept + rejected
    judged = bool(props.get("judged"))

    deck = S.deck_name(src, seg)
    ids = anki("findNotes", query=f'"deck:{deck}"') or []
    infos = anki("notesInfo", notes=ids) or []
    live_fig, live_media, doubled, leaks = 0, set(), 0, 0
    for i in infos:
        imgs = re.findall(r'<img src="(%s_[^"]+)"' % re.escape(src["id"]),
                          i["fields"]["Back Extra"]["value"])
        if imgs:
            live_fig += 1
            live_media |= set(imgs)
            if len(imgs) > 1:
                doubled += 1
    cids = anki("findCards", query=f'"deck:{deck}" "Back Extra:*<img*"') or []
    for c in (anki("cardsInfo", cards=cids) or []):
        if "<img" in c.get("question", ""):
            leaks += 1

    placed = sum(1 for c in cards if c.get("from_idx") or c.get("source_page"))
    withdesc = sum(1 for f in figs if f.get("description"))
    withseen = sum(1 for f in figs if f.get("seen_description"))

    print(f"FIGURE RUN — {src['id']} segment {seg}: {segname}  (pdf {first}-{last})\n")
    print(f"  marks extracted        {len(hl)}")
    print(f"  cards                  {len(cards)}   placeable on a page: {placed}")
    print(f"  figures indexed        {len(figs)}   publisher description: {withdesc}"
          f"   judge description: {withseen}")
    print(f"  proposed               {proposed}")
    print(f"  judged                 {'yes' if judged else 'NO'}"
          f"   kept {kept} / rejected {rejected}")
    print(f"  attached (live deck)   {live_fig} note(s) from {len(live_media)} plate(s)")
    print(f"  coverage               {100*live_fig//max(1,len(infos))}% of {len(infos)} live notes")

    anomalies = []
    if cards and not judged and kept:
        anomalies.append("proposals were NEVER JUDGED — word overlap alone attaches "
                         "pictures that are merely nearby (R19).")
    if doubled:
        anomalies.append(f"{doubled} note(s) carry MORE THAN ONE pipeline figure — a re-run "
                         f"stacked instead of swapping (R17).")
    if leaks:
        anomalies.append(f"{leaks} card(s) show an image on the QUESTION side — a labelled "
                         f"plate on the front of a cloze is an answer key.")
    if cards and placed < 0.75 * len(cards):
        anomalies.append(f"only {placed}/{len(cards)} cards could be placed on a page; the "
                         f"matcher silently skips the rest (R20).")
    if figs and withdesc + withseen == 0:
        anomalies.append("no figure has any description — matching is running on captions "
                         "alone, which is the weakest signal (see ch4).")
    if judged and proposed and rejected / proposed > 0.7:
        anomalies.append(f"the judge rejected {rejected}/{proposed} — that much attrition "
                         f"usually means the matcher is proposing on proximity alone.")
    if kept and live_fig < kept - 2:
        anomalies.append(f"{kept} proposals kept but only {live_fig} notes carry a figure — "
                         f"the attach step may have been skipped or guard-refused.")
    if seg in BASELINE:
        bc, bf, ba = BASELINE[seg]
        if abs(len(figs) - bf) > max(2, 0.2 * bf):
            anomalies.append(f"figure count {len(figs)} vs baseline {bf} — the index changed "
                             f"materially; confirm that was intended.")

    print("\n  ANOMALIES")
    if anomalies:
        for a in anomalies:
            print(f"    ! {a}")
    else:
        print("    none — every historical failure mode checks out.")

    rec = {"run_id": "figures", "source": src["id"], "segment": seg, "stage": "figures",
           "status": "complete", "counts": {
               "marks": len(hl), "cards": len(cards), "cards_placeable": placed,
               "figures_indexed": len(figs), "proposed": proposed, "judged": judged,
               "kept": kept, "rejected": rejected, "attached_notes": live_fig,
               "distinct_plates": len(live_media), "doubled": doubled, "leaks": leaks},
           "anomalies": anomalies}
    if write_run:
        d = os.path.join(S.SKILL, "runs", src["id"], str(seg), "figures")
        os.makedirs(d, exist_ok=True)
        sha = subprocess.run(["git", "-C", S.SKILL, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        rec["skill_sha"] = sha
        rec["new_hazards_found"] = []
        json.dump(rec, open(os.path.join(d, "manifest.json"), "w"), indent=1)
        print(f"\n  filed -> runs/{src['id']}/{seg}/figures/manifest.json")
    return 1 if anomalies else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int, required=True)
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--write-run", action="store_true")
    args = ap.parse_args()
    src = S.get_source(args.source)
    work = os.path.join(S.SKILL, "work", src["id"])
    if args.preflight:
        sys.exit(preflight(src, args.segment, work))
    if args.report:
        sys.exit(report(src, args.segment, work, args.write_run))
    ap.error("give --preflight or --report")


if __name__ == "__main__":
    main()
