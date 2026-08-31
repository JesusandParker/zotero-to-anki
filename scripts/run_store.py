#!/usr/bin/env python3
"""
run_store.py — the permanent record of every card-making run.

Parker's continuous-improvement principle: keep every piece of data from each run so you
can work backwards from a card in Anki and answer three questions —

    1. WHY was this card made?      -> which marked highlight(s) it came from, and its page
    2. WHAT did the agent do?       -> which stage produced it, what the editor changed,
                                       what the judge said, how its numbers were verified
    3. WHY that decision?           -> the merge/collapse/cut log, and every card that was
                                       made and then DROPPED, with the reason

Before this existed, a run computed all of that and then threw it away: Chapter 6 knew
each card's source highlight (`from_idx`) and grouping block, and neither field survived
into the staged file. The audit trail lived for about ten minutes.

Layout (one directory per run, never overwritten):

    runs/<source>/<segment>/<run_id>/
        manifest.json      run metadata, the skill's git SHA, counts, hazards found
        highlights.json    immutable snapshot of the extractor's output (the INPUT)
        cards.json         what actually shipped (the OUTPUT)
        provenance.jsonl   one record per card, incl. the Anki noteId once written
        decisions.jsonl    every merge / collapse / cut, with its reason
        dropped.jsonl      cards made and then killed, with the reason
        figures/           crops that are EVIDENCE a card was grounded visually

What is deliberately NOT stored: full-page renders. They are regenerable from the PDF at
any time. Crops attached to a card are kept because they are the proof that an image-only
table or figure was actually read, rather than recalled from the model's own knowledge.

Usage as a library (the normal case — the pipeline calls these):
    import run_store as R
    run = R.start_run("emt", 6, note="Ch6 rerun after the grounding fix")
    R.snapshot(run, "highlights.json", highlights)
    R.record(run, "decisions.jsonl", {"action": "merge", "kept": 94, "dropped": [98], "reason": "..."})
    R.finish(run, cards=cards, counts={...}, hazards=[...])

Usage as a CLI (inspection):
    python3 scripts/run_store.py list
    python3 scripts/run_store.py list emt
    python3 scripts/run_store.py show emt 6
    python3 scripts/run_store.py trace <ankiNoteId>       # a card in Anki -> its whole story
"""
import json, os, subprocess, sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
RUNS = os.path.join(SKILL, "runs")


# ------------------------------------------------------------------ writing a run

def skill_sha():
    """The exact version of the rules that produced these cards. Without this you cannot
    tell whether a bad card came from a bad rule or a rule that has since been fixed."""
    try:
        return subprocess.run(["git", "-C", SKILL, "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=10).stdout.strip() or None
    except Exception:
        return None


def run_id():
    return datetime.now().strftime("%Y-%m-%dT%H-%M")


def start_run(source, segment, note=None, rid=None):
    """Create the run directory and return its path. Never overwrites an existing run."""
    seg = "all" if segment is None else str(segment)
    rid = rid or run_id()
    path = os.path.join(RUNS, str(source), seg, rid)
    n = 2
    while os.path.exists(path):
        path = os.path.join(RUNS, str(source), seg, f"{rid}-{n}")
        n += 1
    os.makedirs(os.path.join(path, "figures"), exist_ok=True)
    manifest = {
        "run_id": os.path.basename(path),
        "source": source,
        "segment": segment,
        "started": datetime.now().isoformat(timespec="seconds"),
        "skill_sha": skill_sha(),
        "note": note,
        "status": "in_progress",
    }
    _write_json(os.path.join(path, "manifest.json"), manifest)
    return path


def snapshot(run, name, obj):
    """Store an immutable copy of an input or output (highlights.json / cards.json)."""
    _write_json(os.path.join(run, _named(name, ".json")), obj)


def _named(name, ext):
    """Callers pass either a bare stem ("provenance") or the full filename
    ("provenance.jsonl"); both must land on the same file. Bare stems used to write an
    extensionless `provenance`, and `anki_write.py --run` then hard-failed looking for
    `provenance.jsonl` with no hint that the name was the problem (hazard, 2026-08-31)."""
    return name if os.path.splitext(name)[1] else name + ext


def record(run, name, obj):
    """Append one JSONL record (provenance / decisions / dropped)."""
    name = _named(name, ".jsonl")
    with open(os.path.join(run, name), "a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def record_many(run, name, objs):
    for o in objs:
        record(run, name, o)


def finish(run, cards=None, counts=None, hazards=None, status="complete"):
    """Close the run. `hazards` is the list of NEW failure modes this run discovered.

    Every hazard must either name the regression case that now catches it, or say
    explicitly why it cannot be mechanized. smoke_test.sh enforces this — it is what
    stops a run from discovering a problem, writing prose about it, and moving on
    (which is exactly how the table-grounding gap survived Chapter 6)."""
    m = _read_json(os.path.join(run, "manifest.json"))
    if cards is not None:
        snapshot(run, "cards.json", cards)
    m["finished"] = datetime.now().isoformat(timespec="seconds")
    m["counts"] = counts or {}
    m["new_hazards_found"] = hazards or []
    m["status"] = status
    _write_json(os.path.join(run, "manifest.json"), m)
    return m


def attach_note_ids(run, pairs):
    """After anki_write, link each provenance record to the Anki note it became.

    The link lives HERE, in the repo — not as a tag on the card. Parker had the
    `claude_generated` tag removed as noise and keeps only `ch<N>`, so traceability must
    not cost him deck clutter. `pairs` is [(card_index, noteId), ...]."""
    p = os.path.join(run, "provenance.jsonl")
    if not os.path.exists(p):
        return 0
    recs = [json.loads(l) for l in open(p) if l.strip()]
    by_idx = dict(pairs)
    n = 0
    for r in recs:
        if r.get("card_index") in by_idx:
            r["anki_note_id"] = by_idx[r["card_index"]]
            n += 1
    with open(p, "w") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return n


def latest_run(source, segment):
    seg = "all" if segment is None else str(segment)
    d = os.path.join(RUNS, str(source), seg)
    if not os.path.isdir(d):
        return None
    runs = sorted(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)))
    return os.path.join(d, runs[-1]) if runs else None


# ------------------------------------------------------------------------- helpers

def _write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")


def _read_json(path):
    with open(path) as f:
        return json.load(f)


def _read_jsonl(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def all_runs():
    out = []
    if not os.path.isdir(RUNS):
        return out
    for src in sorted(os.listdir(RUNS)):
        sd = os.path.join(RUNS, src)
        if not os.path.isdir(sd):
            continue
        for seg in sorted(os.listdir(sd)):
            gd = os.path.join(sd, seg)
            if not os.path.isdir(gd):
                continue
            for rid in sorted(os.listdir(gd)):
                rd = os.path.join(gd, rid)
                if os.path.isfile(os.path.join(rd, "manifest.json")):
                    out.append(rd)
    return out


# ----------------------------------------------------------------------------- cli

def self_test():
    """R62 — a bare stem and a full filename must land on the SAME file."""
    ok = True
    for name, ext, want in [("provenance", ".jsonl", "provenance.jsonl"),
                            ("provenance.jsonl", ".jsonl", "provenance.jsonl"),
                            ("decisions", ".jsonl", "decisions.jsonl"),
                            ("cards", ".json", "cards.json"),
                            ("cards.json", ".json", "cards.json"),
                            ("highlights.json", ".json", "highlights.json")]:
        got = _named(name, ext)
        if got != want:
            print(f"  FAIL  _named({name!r}, {ext!r}) -> {got!r}, want {want!r}")
            ok = False
    print("run_store self-test:", "OK" if ok else "FAILED")
    return ok


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = args[0]

    if cmd in ("self-test", "self_test"):
        sys.exit(0 if self_test() else 1)

    if cmd == "list":
        want = args[1] if len(args) > 1 else None
        runs = [r for r in all_runs() if not want or f"/{want}/" in r]
        if not runs:
            print("No runs recorded yet." if not want else f"No runs recorded for '{want}'.")
            return
        for r in runs:
            m = _read_json(os.path.join(r, "manifest.json"))
            c = m.get("counts", {})
            haz = len(m.get("new_hazards_found") or [])
            print(f"  {m['source']:<10} seg {str(m.get('segment')):<4} {m['run_id']:<20} "
                  f"{c.get('cards','?')} cards  {c.get('dropped',0)} dropped  "
                  f"{haz} hazard(s)  [{m.get('status')}]")
        return

    if cmd == "show":
        src, seg = args[1], (args[2] if len(args) > 2 else None)
        run = latest_run(src, seg)
        if not run:
            sys.exit(f"no runs for {src} segment {seg}")
        m = _read_json(os.path.join(run, "manifest.json"))
        print(json.dumps(m, indent=2))
        for name in ("provenance.jsonl", "decisions.jsonl", "dropped.jsonl"):
            recs = _read_jsonl(os.path.join(run, name))
            print(f"\n--- {name}: {len(recs)} record(s)")
            for r in recs[:5]:
                print("   ", json.dumps(r, ensure_ascii=False)[:190])
        figs = os.listdir(os.path.join(run, "figures")) if os.path.isdir(os.path.join(run, "figures")) else []
        print(f"\n--- figures/: {len(figs)} visual-grounding artifact(s)")
        return

    if cmd == "trace":
        nid = int(args[1])
        for run in all_runs():
            for r in _read_jsonl(os.path.join(run, "provenance.jsonl")):
                if r.get("anki_note_id") == nid:
                    m = _read_json(os.path.join(run, "manifest.json"))
                    hl = _read_json(os.path.join(run, "highlights.json")) if os.path.exists(os.path.join(run, "highlights.json")) else []
                    print(f"note {nid}")
                    print(f"  run        : {m['source']} segment {m.get('segment')} · {m['run_id']}")
                    print(f"  skill @    : {m.get('skill_sha')}")
                    print(f"  block      : {r.get('block')}")
                    print(f"  stage      : {r.get('stage')}")
                    print(f"  verified   : {r.get('verified_against')} by {r.get('verified_by')}")
                    if r.get("visual_source"):
                        print(f"  visual     : {r['visual_source']}")
                    print(f"  judge      : {str(r.get('judge'))[:160]}")
                    for i in r.get("from_idx") or []:
                        if i < len(hl):
                            h = hl[i]
                            print(f"  <- mark[{i}] p{h.get('page')} ({h.get('grounding')}/{h.get('content','?')}): {h.get('highlight','')[:100]}")
                            if h.get("user_comment"):
                                print(f"       margin note: {h['user_comment'][:110]}")
                    return
        print(f"note {nid} not found in any run record.")
        return

    sys.exit(f"unknown command '{cmd}' — try: list [source] | show <source> [segment] | trace <noteId>")


if __name__ == "__main__":
    main()
