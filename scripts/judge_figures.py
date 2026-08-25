#!/usr/bin/env python3
"""
judge_figures.py — the mandatory judge pass over figure proposals.

Word overlap can tell you a figure and a card share vocabulary. It cannot tell you the
figure DEPICTS what the card is about, and that is the only question that matters. Parker
found the gap live:

  * FIGURE 4-2 "the effectiveness of body language: happy / angry / sad" (three faces)
    attached to a card about holding your PALMS OUT toward a hostile patient. Zero shared
    words; it matched on page adjacency alone. Now blocked mechanically.
  * FIGURE 4-17, a radio transmission diagram (control center -> tower -> ambulance),
    attached to "a cellular telephone is a low-power portable radio". Shared vocabulary
    "radio" and "repeater" — genuinely distinctive words, so no frequency trick catches
    it — but the plate shows a base station and the card is about a phone.

His bar: *"if I see a picture and my first thought is 'why in the world is that picture
there?', it leads me to a root of confusion."* Judging that needs eyes on the picture.

This mirrors Stage 2.75's card judge exactly: a deterministic gate first, then an
independent pass that actually looks. Two steps, because looking is the expensive part:

  1. --emit    one entry per DISTINCT figure (not per proposal), with its image path and
               every card proposed for it. A chapter has ~16-38 distinct plates against
               ~30-100 proposals, so describing each figure once and then judging its
               cards from that description is 2-3x less looking for the same answer.
  2. --apply   filter the proposals by the verdicts, and optionally strip figures already
               attached to live notes that the judge rejected.

The verdict file also carries `depicts` — what the figure ACTUALLY shows, written from
looking at it. That is worth keeping on its own: it is the description the publisher never
supplied for 37 of 66 plates, and it feeds back into matching.

    python3 judge_figures.py --source emt --segment 4 --emit worklist.json
    (look at each figure; fill in `depicts` and each card's verdict)
    python3 judge_figures.py --source emt --segment 4 --apply verdicts.json
    python3 judge_figures.py --source emt --segment 4 --apply verdicts.json --strip-live
"""
import argparse, json, os, re, sys
import sources as S
import authorship


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int, required=True)
    ap.add_argument("--emit", help="write the judging worklist here")
    ap.add_argument("--apply", help="read verdicts from here and filter the proposals")
    ap.add_argument("--strip-live", action="store_true",
                    help="also remove rejected figures from the live Anki notes")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = S.get_source(args.source)
    work = os.path.join(S.SKILL, "work", src["id"])
    props_p = os.path.join(work, f"ch{args.segment}_figure_proposals.json")
    idx_p = os.path.join(work, "figure_index.json")
    if not os.path.exists(props_p):
        sys.exit(f"ERROR: missing {props_p} — run match_figures.py first")
    props = json.load(open(props_p))
    index = {f["label"]: f for f in json.load(open(idx_p))["figures"]}

    if args.emit:
        by_fig = {}
        for tier in ("teaches", "context"):
            for r in props.get(tier, []):
                by_fig.setdefault(r["figure"], []).append(r)
        out = []
        for label, rows in sorted(by_fig.items()):
            f = index.get(label, {})
            out.append({
                "figure": label,
                "image": os.path.join(work, f.get("study_file") or f.get("file", "")),
                "caption": f.get("title"),
                "publisher_description": f.get("description"),
                "depicts": "",          # <- FILL IN from looking at the image
                "cards": [{"card_index": r["card_index"], "tier": r["tier"],
                           "coverage": r["coverage"], "text": r["text"],
                           "verdict": "", "why": ""} for r in rows],
            })
        json.dump({"source": src["id"], "segment": args.segment, "figures": out},
                  open(args.emit, "w"), indent=1)
        print(f"{len(out)} distinct figure(s) covering "
              f"{sum(len(x['cards']) for x in out)} proposal(s) -> {args.emit}")
        print("\nFor each figure: LOOK at `image`, write what it actually shows in "
              "`depicts`,\nthen mark every card `keep` or `drop` with a one-line `why`.")
        print("Keep it only if the plate depicts what THAT card is about — not merely the "
              "same topic.")
        return

    if not args.apply:
        sys.exit("Give --emit <file> or --apply <file>.")

    v = json.load(open(args.apply))
    verdict = {}
    depicts = {}
    for f in v["figures"]:
        if f.get("depicts"):
            depicts[f["figure"]] = f["depicts"]
        for c in f["cards"]:
            if not c.get("verdict"):
                sys.exit(f"ERROR: {f['figure']} card #{c['card_index']} has no verdict. "
                         f"Every proposal must be judged.")
            verdict[(f["figure"], c["card_index"])] = (c["verdict"].strip().lower(),
                                                       c.get("why", ""))
    kept, dropped = {"teaches": [], "context": []}, []
    for tier in ("teaches", "context"):
        for r in props.get(tier, []):
            vd, why = verdict.get((r["figure"], r["card_index"]), ("drop", "unjudged"))
            if vd == "keep":
                kept[tier].append(r)
            else:
                r["rejected_because"] = why
                dropped.append(r)

    print(f"judged {len(verdict)} proposal(s)")
    print(f"  keep : {len(kept['teaches']) + len(kept['context'])}")
    print(f"  drop : {len(dropped)}")
    for r in dropped[:12]:
        print(f"     {r['figure']} (cov {r['coverage']:.2f}) — {r['rejected_because'][:70]}")

    # Fold what the judge SAW back into the index. This is the description the publisher
    # never gave for most plates, and it makes the next match smarter, not just this one.
    if depicts:
        idx = json.load(open(idx_p))
        n = 0
        for f in idx["figures"]:
            if f["label"] in depicts:
                f["seen_description"] = depicts[f["label"]]
                n += 1
        if not args.dry_run:
            json.dump(idx, open(idx_p, "w"), indent=1)
        print(f"  recorded what the judge saw on {n} figure(s) in figure_index.json")

    if args.dry_run:
        print("\n--dry-run: proposals not rewritten.")
        return

    props["teaches"], props["context"] = kept["teaches"], kept["context"]
    props["judged"] = True
    props["rejected"] = dropped
    json.dump(props, open(props_p, "w"), indent=1)
    print(f"\nrewrote {os.path.basename(props_p)} (rejects kept under \"rejected\")")

    if args.strip_live:
        # RECONCILE the deck to the kept set, rather than only removing what the judge
        # rejected. Proposals also disappear when the MATCHER tightens (the zero-coverage
        # rule alone dropped 8 already-attached ch4 figures), and those are just as wrong
        # to leave on a card. The invariant is simply: a live pipeline figure must be
        # justified by a surviving proposal. Parker's own pasted images are never touched.
        from attach_figures import call
        cards = json.load(open(os.path.join(work, f"{S.work_label(src, args.segment)}_cards.json")))
        deck = S.deck_name(src, args.segment)
        infos = call("notesInfo", notes=call("findNotes", query=f'"deck:{deck}"'))

        def media_for(label):
            f = index.get(label, {})
            base = os.path.basename(f.get("study_file") or f.get("file", ""))
            return re.sub(r"[^A-Za-z0-9._-]+", "_", f"{src['id']}_{base}")

        allowed = {}    # normalized card text -> the media it is allowed to carry
        for tier in ("teaches", "context"):
            for r in kept[tier]:
                allowed.setdefault(norm(cards[r["card_index"]]["Text"]), set()).add(
                    media_for(r["figure"]))
        removed, cleaned, refused = 0, 0, []
        store = authorship.load(src["id"])
        for note in infos:
            back = note["fields"]["Back Extra"]["value"]
            here = re.findall(rf'<img src="({re.escape(src["id"])}_[^"]+)"', back)
            if not here:
                continue
            ok = allowed.get(norm(note["fields"]["Text"]["value"]), set())
            drop_these = [m for m in here if m not in ok]
            if not drop_these:
                continue
            new = back
            for m in drop_these:
                new = re.sub(rf'(?:<br>\s*)*<img src="{re.escape(m)}">', "", new)
            new = re.sub(r"(<br>\s*){3,}", "<br><br>", new).strip()
            # Same guard as attaching. Removing a figure is surgical, but the field may
            # carry Parker's own work; `figure_only` passes only when nothing else moved.
            okw, report = authorship.guard(src["id"], note["noteId"],
                                           {"Back Extra": back}, {"Back Extra": new},
                                           figure_only=True, store=store)
            if not okw:
                refused.append(report)
                continue
            call("updateNoteFields", note={"id": note["noteId"],
                                           "fields": {"Back Extra": new}})
            authorship.record(src["id"], note["noteId"], {"Back Extra": new}, store=store)
            removed += len(drop_these); cleaned += 1
        authorship.save(src["id"], store)
        print(f"  reconciled the live deck: removed {removed} unjustified figure(s) "
              f"from {cleaned} note(s)")
        if refused:
            print(f"  {len(refused)} strip(s) REFUSED by the authorship guard "
                  f"(the field carries work this system did not author)")


if __name__ == "__main__":
    main()
