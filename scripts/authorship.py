#!/usr/bin/env python3
"""authorship.py — who wrote what, so Parker's own work is never collateral damage.

Parker edits his own cards constantly. He adds mnemonics he invented, images he
pasted, TTS audio, clinical examples, notes to himself. None of that is visible
to the pipeline, and until now nothing recorded the difference between "the
generator wrote this" and "Parker wrote this."

The cost of that gap, 2026-07-30: a session rebuilding a card noticed its ETHICS
mnemonic was not in the textbook, concluded a previous run had fabricated it,
replaced it, and reported the catch. The mnemonic was Parker's. He had written it
himself and reordered the card's questions so the letters would spell. It was
only recovered because he said so.

THE BASELINE
------------
The pipeline records a fingerprint of EXACTLY what it wrote, at the moment it
writes it. Before any later write to that field, the live value is hashed and
compared against the record:

    owned    live == what we last wrote      -> safe to overwrite
    edited   live != what we last wrote      -> PARKER TOUCHED IT. Refuse.
    unknown  no record for this field        -> treat exactly like `edited`.

**Silence is not consent.** Every card written before this file existed is
`unknown`, which means the guard protects it. That is deliberate: the failure
mode we are fixing is an automated pass confidently overwriting something it did
not author, so absence of evidence must fail closed, not open.

WHITESPACE-ONLY REPAIRS
-----------------------
A layout repair (listify/paragraphize) cannot destroy content — it only re-joins
existing segments. Those pass `safe_transform=True` and are allowed through even
on `edited`/`unknown` fields, because the guard exists to protect *content*, and
blocking them would make the layout rules unenforceable on the existing deck.
The check is not a promise from the caller: `is_whitespace_only()` verifies it.

USAGE
    python3 scripts/authorship.py status --source emt     # owned / edited / unknown
    python3 scripts/authorship.py scan   --source emt     # notes bearing hand-edit marks
    python3 scripts/authorship.py check  --source emt --note <id>

    from authorship import guard, record
    ok, report = guard("emt", note_id, live_fields, {"Text": new_text})
    if not ok: ...show report, do NOT write...
"""
import argparse, hashlib, json, os, re, sys, urllib.request

ANKI = "http://localhost:8765"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Marks that strongly suggest a human hand touched the field. Retroactive only —
# a best-effort signal for the ~1,100 cards that predate the fingerprint store.
# NOT used by guard(); guard treats unknown as protected regardless.
HAND_MARKS = [
    (r"&nbsp;", "Anki editor whitespace artifact"),
    (r"\[sound:", "TTS audio Parker attached (HyperTTS)"),
    (r"<a\s+href", "pasted link wrapper (mobile paste)"),
    (r"<(?:div|span|ol|ul|li|table)\b", "rich HTML the generator never emits"),
]


def store_path(source):
    return os.path.join(ROOT, "work", source, "authorship.json")


def load(source):
    p = store_path(source)
    return json.load(open(p)) if os.path.exists(p) else {}


def save(source, store):
    p = store_path(source)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(store, open(p, "w"), indent=1, sort_keys=True)


def sha(value):
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()[:32]


def record(source, note_id, fields, run=None, store=None):
    """Call IMMEDIATELY after the pipeline successfully writes `fields` to a note.

    Only ever record what we actually wrote. Recording a field we did not author
    is worse than recording nothing: it converts one of Parker's edits into
    something a future pass believes it owns."""
    own = store if store is not None else load(source)
    entry = own.setdefault(str(note_id), {"fields": {}})
    for name, value in fields.items():
        entry["fields"][name] = sha(value)
    if run:
        entry["run"] = run
    if store is None:
        save(source, own)
    return own


def check(source, note_id, live_fields, store=None):
    """{field: 'owned'|'edited'|'unknown'} for the fields present in live_fields."""
    own = store if store is not None else load(source)
    entry = own.get(str(note_id), {}).get("fields", {})
    out = {}
    for name, value in live_fields.items():
        if name not in entry:
            out[name] = "unknown"
        else:
            out[name] = "owned" if entry[name] == sha(value) else "edited"
    return out


def is_whitespace_only(before, after):
    """True if the change cannot have altered a single character of content."""
    strip = lambda s: re.sub(r"\s+", "", re.sub(r"<br\s*/?>", "", s or "", flags=re.I))
    return strip(before) == strip(after)


def is_figure_only_change(before, after, source_id):
    """True if the ONLY difference is pipeline-attached <img> tags coming or going.

    Attaching a figure and stripping one are surgical: they add or remove a single
    `<img src="<source_id>_...">` and touch nothing else. But they are content
    changes, so `is_whitespace_only` correctly refuses them, and every card
    predating the store is `unknown` — which would leave the figure stages unable
    to run on the existing deck at all.

    The answer is a SECOND verified predicate, not a bypass: delete every
    pipeline-owned <img> from both sides, normalise the break runs those tags sat
    in, and require the residue to be identical. Anything Parker added — his own
    pasted images (which never carry the `<source_id>_` prefix), his mnemonics,
    his `[sound:]` audio — survives into the residue, so if he touched a single
    character of it the comparison fails and the guard blocks, exactly as it should.
    """
    pat = re.compile(rf'<img src="{re.escape(source_id)}_[^"]*">', re.I)
    def residue(s):
        s = pat.sub("", s or "")
        s = re.sub(r"(?:\s*<br\s*/?>\s*)+", "<br>", s, flags=re.I)
        return re.sub(r"\s+", " ", s).strip(" ").strip("<br>").strip()
    return residue(before) == residue(after)


CLOZE_SPAN = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")


def is_hint_only_change(before, after):
    """True if the ONLY difference is slot-label `::hint`s being ADDED to cloze spans.

    The third verified predicate, and it exists for the same reason the second one
    does: card-rules #27 (R34) repairs a whole class of live cards by adding a hint
    that names what the blank wants, and every card predating the store is
    `unknown` — so without this the rule Parker asked to have applied "for all the
    cards" could not be applied to any of them.

    Deliberately DIRECTIONAL. Adding a hint where there was none is licensed;
    changing or removing an existing one is not, because a hint may be Parker's own
    and there is no prefix to tell his apart from ours (the trick that makes
    `is_figure_only_change` able to protect his pasted images). The repair never
    needs to touch an existing hint anyway — a hinted blank is already exempt from
    the rule — so the safe direction is also the sufficient one.

    Everything else must be byte-identical: the prose between the spans, and every
    span's cloze number and answer. If a single character of his content moved, the
    residue differs and the guard blocks, exactly as it should.
    """
    b, a = list(CLOZE_SPAN.finditer(before or "")), list(CLOZE_SPAN.finditer(after or ""))
    if len(b) != len(a):
        return False

    def skeleton(s, ms):                       # the card with every hint removed
        out, pos = [], 0
        for m in ms:
            out.append(s[pos:m.start()])
            out.append("{{c%s::%s}}" % (m.group(1), m.group(2)))
            pos = m.end()
        out.append(s[pos:])
        return "".join(out)

    if skeleton(before or "", b) != skeleton(after or "", a):
        return False
    for mb, ma in zip(b, a):
        if mb.group(3) == ma.group(3):
            continue                           # untouched
        if mb.group(3) is None and ma.group(3):
            continue                           # a hint ADDED where there was none
        return False                           # changed or removed: not licensed
    return True


def guard(source, note_id, live_fields, new_fields, safe_transform=False, store=None,
          figure_only=False, hint_only=False):
    """(ok, report). ok is False when a write would clobber a field this system
    did not author. `safe_transform` / `figure_only` / `hint_only` are VERIFIED,
    not trusted."""
    status = check(source, note_id, {k: live_fields.get(k, "") for k in new_fields}, store)
    blocked = []
    for name, new in new_fields.items():
        if status[name] == "owned":
            continue
        if safe_transform and is_whitespace_only(live_fields.get(name, ""), new):
            continue
        if figure_only and is_figure_only_change(live_fields.get(name, ""), new, source):
            continue
        if hint_only and is_hint_only_change(live_fields.get(name, ""), new):
            continue
        blocked.append((name, status[name]))
    if not blocked:
        return True, ""
    lines = [f"REFUSING to overwrite note {note_id} — this system did not author it:"]
    for name, why in blocked:
        reason = ("Parker has edited it since we last wrote it" if why == "edited"
                  else "no record of us ever writing it (predates the authorship store)")
        lines.append(f"  · {name}: {why.upper()} — {reason}")
        lines.append(f"      LIVE: {(live_fields.get(name,'') or '')[:220]}")
        lines.append(f"      NEW : {(new or '')[:220]}")
    lines.append("  Read the live value. Preserve whatever he added, or ask him. "
                 "Do not pass this guard just to make the write succeed.")
    return False, "\n".join(lines)


# ---------------------------------------------------------------- CLI ------
def call(action, **params):
    req = urllib.request.Request(ANKI, json.dumps(
        {"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if res.get("error"):
        sys.exit(f"AnkiConnect error: {res['error']}")
    return res["result"]


def live_notes(source):
    import sources as S
    deck = S.get_source(source).get("deck_root")
    if not deck:
        sys.exit(f"source '{source}' has no deck_root in the registry")
    notes = call("notesInfo", notes=call("findNotes", query=f'deck:{deck}::*'))
    return [{"noteId": n["noteId"],
             "fields": {k: v["value"] for k, v in n["fields"].items()},
             "tags": n["tags"]} for n in notes]


def self_test():
    """The guard is the only thing standing between an automated pass and Parker's
    work, so its behaviour is tested rather than assumed. Run after ANY change here."""
    S, fails = "t", []
    def eq(name, got, want):
        if got != want:
            fails.append(f"{name}: got {got!r}, want {want!r}")
    store = {}
    record(S, 1, {"Text": "ours", "Back Extra": "b"}, store=store)
    eq("owned", check(S, 1, {"Text": "ours"}, store)["Text"], "owned")
    eq("edited", check(S, 1, {"Text": "ours + his mnemonic"}, store)["Text"], "edited")
    eq("unknown", check(S, 99, {"Text": "never seen"}, store)["Text"], "unknown")
    eq("guard allows owned",
       guard(S, 1, {"Text": "ours"}, {"Text": "new"}, store=store)[0], True)
    eq("guard BLOCKS edited",
       guard(S, 1, {"Text": "his edit"}, {"Text": "new"}, store=store)[0], False)
    eq("guard BLOCKS unknown",
       guard(S, 99, {"Text": "legacy"}, {"Text": "new"}, store=store)[0], False)
    eq("whitespace repair allowed on unknown",
       guard(S, 99, {"Text": "a<br>b"}, {"Text": "a<br><br>b"},
             safe_transform=True, store=store)[0], True)
    eq("safe_transform does NOT license a content change",
       guard(S, 99, {"Text": "a<br>b"}, {"Text": "a<br><br>c"},
             safe_transform=True, store=store)[0], False)
    # figure_only: attaching / stripping a pipeline <img> and nothing else
    HIS = 'Why: fused bones.<br><br><img src="Screenshot 2026-07-30.png">'
    eq("figure_only allows ATTACHING a pipeline image on an unknown field",
       guard(S, 99, {"Back Extra": HIS},
             {"Back Extra": HIS + '<br><br><img src="t_FIGURE_6_6.jpg">'},
             figure_only=True, store=store)[0], True)
    eq("figure_only allows STRIPPING a pipeline image on an unknown field",
       guard(S, 99, {"Back Extra": HIS + '<br><br><img src="t_FIGURE_6_6.jpg">'},
             {"Back Extra": HIS}, figure_only=True, store=store)[0], True)
    eq("figure_only does NOT license removing PARKER'S OWN image",
       guard(S, 99, {"Back Extra": HIS}, {"Back Extra": "Why: fused bones."},
             figure_only=True, store=store)[0], False)
    eq("figure_only does NOT license a text change alongside the image",
       guard(S, 99, {"Back Extra": HIS},
             {"Back Extra": 'Why: REWRITTEN.<br><br><img src="Screenshot 2026-07-30.png">'
                            '<br><br><img src="t_FIGURE_6_6.jpg">'},
             figure_only=True, store=store)[0], False)
    eq("figure_only does not leak into an ordinary write",
       guard(S, 99, {"Back Extra": HIS}, {"Back Extra": "something else"},
             figure_only=True, store=store)[0], False)
    # hint_only: adding a card-rules #27 slot label and nothing else (R34)
    BARE = "The {{c2::carpals}} are the {{c1::eight}} bones that form the wrist."
    HINTED = ("The {{c2::carpals}} are the {{c1::eight::number of bones}} bones "
              "that form the wrist.")
    eq("hint_only allows ADDING a slot label on an unknown field",
       guard(S, 99, {"Text": BARE}, {"Text": HINTED}, hint_only=True, store=store)[0], True)
    eq("hint_only does NOT license REMOVING a hint (it may be Parker's)",
       guard(S, 99, {"Text": HINTED}, {"Text": BARE}, hint_only=True, store=store)[0], False)
    eq("hint_only does NOT license REWRITING an existing hint",
       guard(S, 99, {"Text": HINTED},
             {"Text": HINTED.replace("number of bones", "how many")},
             hint_only=True, store=store)[0], False)
    eq("hint_only does NOT license a prose change riding along",
       guard(S, 99, {"Text": BARE},
             {"Text": HINTED.replace("form the wrist", "form the ANKLE")},
             hint_only=True, store=store)[0], False)
    eq("hint_only does NOT license changing the ANSWER",
       guard(S, 99, {"Text": BARE},
             {"Text": HINTED.replace("{{c1::eight::", "{{c1::seven::")},
             hint_only=True, store=store)[0], False)
    eq("hint_only does not leak into an ordinary write",
       guard(S, 99, {"Text": BARE}, {"Text": "something else"},
             hint_only=True, store=store)[0], False)
    for m in fails:
        print("FAIL " + m)
    print(f"{19 - len(fails)}/19 authorship guard checks pass")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=["status", "scan", "check", "self-test"])
    ap.add_argument("--source", default="emt")
    ap.add_argument("--note", type=int)
    args = ap.parse_args()
    sys.path.insert(0, HERE)
    if args.command == "self-test":
        sys.exit(self_test())
    store = load(args.source)

    if args.command == "check":
        notes = {n["noteId"]: n for n in live_notes(args.source)}
        n = notes.get(args.note) or sys.exit(f"note {args.note} not in this source's decks")
        for f, s in check(args.source, args.note, n["fields"], store).items():
            print(f"  {f:14} {s}")
        return

    notes = live_notes(args.source)
    if args.command == "status":
        tally = {"owned": 0, "edited": 0, "unknown": 0}
        for n in notes:
            for s in check(args.source, n["noteId"],
                           {k: n["fields"].get(k, "") for k in ("Text", "Back Extra")},
                           store).values():
                tally[s] += 1
        print(f"{len(notes)} notes in '{args.source}' ({len(notes)*2} guarded fields)")
        for k in ("owned", "edited", "unknown"):
            print(f"  {k:9} {tally[k]}")
        print("\n'unknown' = written before the authorship store existed. The guard "
              "protects those exactly like Parker's own edits — content is never "
              "overwritten on a field we cannot prove we wrote.")
        return

    # scan — retroactive best effort for the pre-store backlog
    hits = []
    for n in notes:
        for field in ("Text", "Back Extra"):
            v = n["fields"].get(field, "")
            for pat, why in HAND_MARKS:
                if re.search(pat, v, re.I):
                    hits.append((n["noteId"], n["tags"], field, why))
                    break
    print(f"{len(hits)} field(s) bear a hand-edit mark "
          f"(heuristic — a signal that Parker touched it, not proof):\n")
    from collections import Counter
    for why, c in Counter(h[3] for h in hits).most_common():
        print(f"  {c:5}  {why}")
    print("\nThese predate the store, so they are already protected as 'unknown'. "
          "The marks just tell you WHERE his work most likely is.")


if __name__ == "__main__":
    main()
