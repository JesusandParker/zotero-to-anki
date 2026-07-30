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
    python3 attach_figures.py --undo work/emt/figure_attach_undo.json

Anki must be running.
"""
import argparse, base64, json, os, re, sys, urllib.request
import sources as S

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

    if not args.source or args.segment is None:
        sys.exit("Give --source and --segment (or --undo <file>).")
    src = S.get_source(args.source)
    work = os.path.join(S.SKILL, "work", src["id"])
    props_p = args.proposals or os.path.join(work, f"ch{args.segment}_figure_proposals.json")
    cards_p = args.cards or os.path.join(work, f"chapter_{args.segment}_cards.json")
    for p in (props_p, cards_p):
        if not os.path.exists(p):
            sys.exit(f"ERROR: missing {p}")
    props = json.load(open(props_p))
    cards = json.load(open(cards_p))
    tiers = [t.strip() for t in args.tiers.split(",") if t.strip()]
    todo = [r for t in tiers for r in props.get(t, [])]

    staging, _promote = S.deck_names(src, args.segment)
    note_ids = call("findNotes", query=f'"deck:{staging}"')
    if not note_ids:
        sys.exit(f"ERROR: no notes found in {staging!r}. Nothing to attach to.")
    infos = call("notesInfo", notes=note_ids)
    by_text = {}
    for i in infos:
        by_text.setdefault(norm(i["fields"]["Text"]["value"]), []).append(i)

    print(f"{len(todo)} proposal(s) over tiers {tiers}")
    print(f"{len(infos)} live notes in {staging}\n")

    writes, skipped, unmatched, had_own = [], [], [], []
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
        if "<img" in back.lower():
            had_own.append((r, note["noteId"]))     # his own paste — keep it, report it
        tag = f'<img src="{fn}">'
        appended = ("<br><br>" + tag) if back.strip() else tag
        writes.append({"noteId": note["noteId"], "figure": r["figure"], "file": path,
                       "media": fn, "appended": appended,
                       "new_back": back + appended, "tier": r.get("tier")})

    print(f"  to attach : {len(writes)}")
    print(f"  already ok: {len(skipped)} (idempotent skip)")
    print(f"  unmatched : {len(unmatched)}")
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
    ok = 0
    for w in writes:
        if w["media"] not in media_done:
            call("storeMediaFile", filename=w["media"],
                 data=base64.b64encode(open(w["file"], "rb").read()).decode())
            media_done.add(w["media"])
        call("updateNoteFields", note={"id": w["noteId"],
             "fields": {"Back Extra": w["new_back"]}})
        ok += 1

    undo_p = os.path.join(work, f"figure_attach_undo.json")
    json.dump({"deck": staging, "writes": [
        {k: w[k] for k in ("noteId", "figure", "media", "appended", "tier")} for w in writes]},
        open(undo_p, "w"), indent=1)
    print(f"\nattached {ok} figure(s) to {len({w['noteId'] for w in writes})} note(s)")
    print(f"  distinct media files stored: {len(media_done)}")
    print(f"  undo record -> {undo_p}")
    print(f"\nSync when ready — these land on your phone on the next sync.")


if __name__ == "__main__":
    main()
