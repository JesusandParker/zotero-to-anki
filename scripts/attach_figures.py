#!/usr/bin/env python3
"""
attach_figures.py — attach proposed figures to cards that ALREADY LIVE IN ANKI.

This is deliberately not part of `anki_write.py`. That script ADDS notes; a chapter whose
cards are already staged needs its existing notes UPDATED, and running the writer again
would produce 202 duplicates instead of 202 pictures.

What it does, per proposal:
  * finds the live note by matching its Text against the canon cards file
  * stores the STUDY-SIZE copy in Anki's media (not the native archive)
  * appends <img> to **Back Extra** — the back of the card, never the front, because a
    labelled plate on the front of a cloze is an answer key
  * is idempotent: a card that already carries this exact figure is left alone, so the
    script can be re-run safely after a partial pass

It never strips anything Parker added himself. A card that already has his own pasted
image keeps it and is REPORTED, so he can decide which to delete — matching the standing
rule that hand-added content is his, not the pipeline's to remove.

Every write is recorded to an undo file, so the whole pass is reversible:

    python3 attach_figures.py --source emt --segment 6 --dry-run
    python3 attach_figures.py --source emt --segment 6
    python3 attach_figures.py --undo work/emt/figure_attach_undo_seg6.json

Anki must be running.
"""
import argparse, base64, json, os, re, sys, urllib.request
import sources as S
import authorship

ANKI = "http://localhost:8765"


def call(action, **params):
    req = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(
                ANKI, req, {"Content-Type": "application/json"}), timeout=60) as r:
            out = json.load(r)
    except Exception as e:
        sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI} — is Anki running?\n  {e}")
    if out.get("error"):
        raise RuntimeError(f"{action}: {out['error']}")
    return out["result"]


def norm(s):
    """Compare card text ignoring markup and whitespace — Anki round-trips both."""
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source")
    ap.add_argument("--segment", type=int)
    ap.add_argument("--proposals")
    ap.add_argument("--cards")
    ap.add_argument("--tiers", default="teaches,context",
                    help="which proposal tiers to attach (default: both)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--undo", help="revert a previous run from its undo file")
    ap.add_argument("--refresh-media", action="store_true",
                    help="re-upload the image files only, leaving every note untouched")
    ap.add_argument("--to-cards", action="store_true",
                    help="write the figures into the CARDS FILE (for a segment not yet "
                         "staged) instead of updating live notes")
    ap.add_argument("--allow-multiple", action="store_true",
                    help="let a card carry more than one pipeline figure")
    ap.add_argument("--replace", action="store_true",
                    help="swap a card's existing pipeline figure for the current best")
    args = ap.parse_args()

    if args.refresh_media:
        # Rebuilding the study copies (a new matte, a different size) changes the FILES
        # but not their names, and the notes already reference those names. So replacing
        # the media is the whole job — re-running the attach would correctly skip all of
        # them as already-present and the cards would keep the stale images forever.
        if not args.source or args.segment is None:
            sys.exit("--refresh-media needs --source and --segment.")
        src = S.get_source(args.source)
        work = os.path.join(S.SKILL, "work", src["id"])
        props_p = args.proposals or os.path.join(
            work, f"ch{args.segment}_figure_proposals.json")
        props = json.load(open(props_p))
        seen, n, missing = set(), 0, []
        for t in ("teaches", "context"):
            for r in props.get(t, []):
                path = os.path.join(work, r["file"])
                fn = re.sub(r"[^A-Za-z0-9._-]+", "_",
                            f"{src['id']}_{os.path.basename(path)}")
                if fn in seen:
                    continue
                seen.add(fn)
                if not os.path.exists(path):
                    missing.append(fn); continue
                if not args.dry_run:
                    call("storeMediaFile", filename=fn,
                         data=base64.b64encode(open(path, "rb").read()).decode())
                n += 1
        verb = "would replace" if args.dry_run else "replaced"
        print(f"{verb} {n} media file(s); notes untouched")
        if missing:
            print(f"  MISSING on disk ({len(missing)}): {missing[:5]}")
        return

    if args.undo:
        recs = json.load(open(args.undo))
        n = 0
        for r in recs["writes"]:
            info = call("notesInfo", notes=[r["noteId"]])
            if not info or not info[0]:
                continue
            cur = info[0]["fields"]["Back Extra"]["value"]
            if r["appended"] not in cur:
                continue
            call("updateNoteFields", note={"id": r["noteId"],
                 "fields": {"Back Extra": cur.replace(r["appended"], "")}})
            n += 1
        print(f"reverted {n}/{len(recs['writes'])} notes (the rest were already clean)")
        return

    if args.to_cards:
        # A segment that has NOT been staged yet needs its figures in the cards FILE, so
        # that anki_write.py embeds them when it creates the notes. Live-note updating
        # (the default path below) is for a chapter whose notes already exist. Chapter 7
        # and everything after it takes this route; chapters 1-6 took the other one.
        if not args.source or args.segment is None:
            sys.exit("--to-cards needs --source and --segment.")
        src = S.get_source(args.source)
        work = os.path.join(S.SKILL, "work", src["id"])
        props = json.load(open(args.proposals or os.path.join(
            work, f"ch{args.segment}_figure_proposals.json")))
        cards_p = args.cards or os.path.join(work, f"{S.work_label(src, args.segment)}_cards.json")
        cards = json.load(open(cards_p))
        if not props.get("judged"):
            sys.exit("REFUSING: these proposals have not been judged. Run judge_figures.py "
                     "first — word overlap alone attaches pictures that are merely nearby.")
        idx_p = os.path.join(work, "figure_index.json")
        figpage = {}
        if os.path.exists(idx_p):
            figpage = {f["label"]: f.get("art_page") or f.get("caption_page")
                       for f in json.load(open(idx_p)).get("figures", [])}
        n = 0
        for tier in ("teaches", "context"):
            for r in props.get(tier, []):
                c = cards[r["card_index"]]
                path = os.path.join(work, r["file"])
                if not os.path.exists(path):
                    continue
                c["image"] = path
                c["image_side"] = "back"     # a labelled plate on the front is an answer key
                c["visual_source"] = {
                    "pages": [str(figpage.get(r["figure"]))],
                    "figures": [r["file"]], "labels": [r["figure"]],
                    "note": "figure extracted from the source PDF and attached to this card "
                            "(scripts/attach_figures.py --to-cards).",
                }
                n += 1
        if args.dry_run:
            print(f"--dry-run: would set image on {n} card(s) in {os.path.basename(cards_p)}")
            return
        json.dump(cards, open(cards_p, "w"), indent=1)
        stamp = cards_p + ".verified"
        if os.path.exists(stamp):
            os.remove(stamp)
        print(f"set image + image_side=back on {n} card(s) in {os.path.basename(cards_p)}")
        print("  .verified stamp cleared — re-run check_cards.py, then anki_write.py")
        return

    if not args.source or args.segment is None:
        sys.exit("Give --source and --segment (or --undo <file>).")
    src = S.get_source(args.source)
    work = os.path.join(S.SKILL, "work", src["id"])
    props_p = args.proposals or os.path.join(work, f"ch{args.segment}_figure_proposals.json")
    cards_p = args.cards or os.path.join(work, f"{S.work_label(src, args.segment)}_cards.json")
    for p in (props_p, cards_p):
        if not os.path.exists(p):
            sys.exit(f"ERROR: missing {p}")
    props = json.load(open(props_p))
    cards = json.load(open(cards_p))
    idx_p = os.path.join(work, "figure_index.json")
    figpage = {}
    if os.path.exists(idx_p):
        figpage = {f["label"]: f.get("art_page") or f.get("caption_page")
                   for f in json.load(open(idx_p)).get("figures", [])}
    tiers = [t.strip() for t in args.tiers.split(",") if t.strip()]
    todo = [r for t in tiers for r in props.get(t, [])]

    target = S.deck_name(src, args.segment)
    note_ids = call("findNotes", query=f'"deck:{target}"')
    if not note_ids:
        sys.exit(f"ERROR: no notes found in {target!r}. Nothing to attach to.")
    infos = call("notesInfo", notes=note_ids)
    by_text = {}
    for i in infos:
        by_text.setdefault(norm(i["fields"]["Text"]["value"]), []).append(i)

    print(f"{len(todo)} proposal(s) over tiers {tiers}")
    print(f"{len(infos)} live notes in {target}\n")

    writes, skipped, unmatched, had_own, superseded = [], [], [], [], []
    for r in todo:
        c = cards[r["card_index"]]
        key = norm(c["Text"])
        cands = by_text.get(key) or []
        if len(cands) != 1:
            unmatched.append((r, "no unique live note" if not cands else "ambiguous match"))
            continue
        note = cands[0]
        path = os.path.join(work, r["file"])
        if not os.path.exists(path):
            unmatched.append((r, f"image missing: {r['file']}"))
            continue
        fn = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{src['id']}_{os.path.basename(path)}")
        back = note["fields"]["Back Extra"]["value"]
        if fn in back:
            skipped.append(r)                       # already attached; idempotent
            continue
        # A card gets ONE pipeline figure. Guarding only on "this exact file" is too weak:
        # improve the matcher, re-run, and any card whose best figure CHANGED silently
        # gains a second picture instead of swapping. That is clutter arrived at by
        # accident rather than by decision. (Six Chapter 6 cards did exactly this after
        # the crossref change.) --allow-multiple opts in deliberately.
        if not args.allow_multiple and re.search(rf'<img src="{re.escape(src["id"])}_', back):
            existing = re.findall(rf'<img src="({re.escape(src["id"])}_[^"]+)"', back)
            superseded.append((r, note["noteId"], existing, fn))
            continue
        if "<img" in back.lower():
            had_own.append((r, note["noteId"]))     # his own paste — keep it, report it
        tag = f'<img src="{fn}">'
        appended = ("<br><br>" + tag) if back.strip() else tag
        writes.append({"noteId": note["noteId"], "figure": r["figure"], "file": path,
                       "media": fn, "appended": appended, "card_index": r["card_index"],
                       "fig_page": r.get("page_dist") is not None and figpage.get(r["figure"]),
                       "new_back": back + appended, "live_back": back,
                       "tier": r.get("tier")})

    print(f"  to attach : {len(writes)}")
    print(f"  already ok: {len(skipped)} (idempotent skip)")
    print(f"  unmatched : {len(unmatched)}")
    if superseded:
        print(f"  superseded: {len(superseded)} card(s) already carry a different figure "
              f"(kept; --replace to swap, --allow-multiple to add)")
        for r, nid, have, want in superseded[:6]:
            print(f"      note {nid}: has {have}, matcher now prefers {want}")
    if unmatched:
        for r, why in unmatched[:6]:
            print(f"      {r['figure']}: {why}")
    if had_own:
        print(f"  {len(had_own)} card(s) already carry YOUR OWN pasted image — kept, not replaced:")
        for r, nid in had_own:
            print(f"      note {nid}: adding {r['figure']} alongside it")
    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return
    if not writes:
        print("\nNothing to do.")
        return

    media_done = set()
    ok, refused = 0, []
    store = authorship.load(src["id"])
    for w in writes:
        # Attaching is additive, but it still writes a field this system may not have
        # authored. `figure_only` is a VERIFIED predicate, not a bypass: it passes only
        # when the sole difference is pipeline `<img>` tags. If Parker has touched the
        # rest of the field, the guard blocks and we leave his work alone.
        live = {"Back Extra": w["live_back"]}
        okw, report = authorship.guard(src["id"], w["noteId"], live,
                                       {"Back Extra": w["new_back"]},
                                       figure_only=True, store=store)
        if not okw:
            refused.append((w, report))
            continue
        if w["media"] not in media_done:
            call("storeMediaFile", filename=w["media"],
                 data=base64.b64encode(open(w["file"], "rb").read()).decode())
            media_done.add(w["media"])
        call("updateNoteFields", note={"id": w["noteId"],
             "fields": {"Back Extra": w["new_back"]}})
        authorship.record(src["id"], w["noteId"], {"Back Extra": w["new_back"]},
                          store=store)
        ok += 1
    authorship.save(src["id"], store)
    if refused:
        print(f"\n  {len(refused)} write(s) REFUSED by the authorship guard:")
        for w, report in refused[:3]:
            print("    " + report.splitlines()[0])
        print("    (the field changed in a way that is not just a pipeline figure)")

    # The undo record ACCUMULATES. Because the attach is idempotent, a second run only
    # ever carries the handful of cards that newly qualified — so overwriting would
    # silently shrink the record to those few and strand every earlier write as
    # unrevertable. (Seen for real: a re-run after a matcher improvement replaced 99
    # entries with 7.) Keyed by note+media so a repeat is not double-recorded.
    # Record the attachment in the CANON cards file too, not just in Anki. The gate reads
    # the file, so a figure that exists only in the deck is invisible to R13 — which then
    # HARD-blocks a card for lacking the very evidence now sitting on it. (EMT ch4 #105
    # cites an image-only table, carries FIGURE 4-20 in Anki, and was still blocked.)
    canon_touched = 0
    for w in writes:
        c = cards[w["card_index"]]
        vs = c.get("visual_source") or {}
        figs = list(vs.get("figures") or [])
        rel = os.path.relpath(w["file"], work)
        if rel not in figs:
            figs.append(rel)
        pages = sorted({str(p) for p in (vs.get("pages") or [])} | {str(w["fig_page"])})
        c["visual_source"] = {
            "pages": pages, "figures": figs, "labels":
                sorted(set((vs.get("labels") or []) + [w["figure"]])),
            "note": "figure extracted from the source PDF and attached to this card "
                    "(scripts/attach_figures.py); the plate is the visual evidence.",
        }
        canon_touched += 1
    if canon_touched:
        json.dump(cards, open(cards_p, "w"), indent=1)
        stamp = cards_p + ".verified"
        if os.path.exists(stamp):
            os.remove(stamp)     # the file changed; the gate must be re-run before writing
        print(f"  recorded visual_source on {canon_touched} card(s) in {os.path.basename(cards_p)}")
        print("  .verified stamp cleared — re-run check_cards.py")

    undo_p = os.path.join(work, f"figure_attach_undo_seg{args.segment}.json")
    prior = []
    if os.path.exists(undo_p):
        try:
            prior = json.load(open(undo_p)).get("writes", [])
        except Exception:
            prior = []
    merged = {(w["noteId"], w["media"]): w for w in prior}
    merged.update({(w["noteId"], w["media"]):
                   {k: w[k] for k in ("noteId", "figure", "media", "appended", "tier")}
                   for w in writes})
    json.dump({"deck": target, "writes": list(merged.values())},
              open(undo_p, "w"), indent=1)
    print(f"\nattached {ok} figure(s) to {len({w['noteId'] for w in writes})} note(s)")
    print(f"  distinct media files stored: {len(media_done)}")
    print(f"  undo record -> {undo_p}")
    print(f"\nSync when ready — these land on your phone on the next sync.")


if __name__ == "__main__":
    main()
