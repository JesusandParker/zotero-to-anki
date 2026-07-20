#!/usr/bin/env python3
"""Apply audit verdicts to Anki, then re-sync the JSON canon from the live deck.

Usage:
  python3 apply_audit.py --apply combined_verdicts.json     # write REWRITE fixes to Anki
  python3 apply_audit.py --resync 1 2 3 4 5                  # dump chapters -> chapter_N_cards.json

Verdict schema (combined): {"verdicts": [ {"noteId": int, "verdict": "REWRITE"|"DROP",
"fix": {"Text": "...", "Back Extra": "..."}, "needs_human_check": bool, "reason": "..."} ]}
Only the fields present in `fix` are written (updateNoteFields merges). DROP is NOT auto-applied
(printed for manual review). Preserves everything not touched, incl. Ch5 clinical-ex HTML + audio.
"""
import html, json, re, sys, urllib.request

HERE = __file__.rsplit("/", 1)[0]
VALUE = re.compile(r"[<>≤≥]\s*\d|\d+\s*(?:mg|mcg|g|mmHg|mL|%|/min|bpm|hours?|minutes?|seconds?|mph|miles?|feet|ft|inch|in|MHz|watts?|L/min)\b|\d+\s*(?:to|-|–)\s*\d+", re.I)
CLOZE = re.compile(r"\{\{c\d+::(.*?)(?:::.*?)?\}\}")


def call(action, **p):
    req = urllib.request.Request("http://localhost:8765",
        json.dumps({"action": action, "version": 6, "params": p}).encode())
    r = json.load(urllib.request.urlopen(req))
    if r.get("error"):
        raise RuntimeError(r["error"])
    return r["result"]


def readable(t):
    return re.sub(r"<[^>]+>", " ", CLOZE.sub(lambda m: m.group(1), t))


def apply_fixes(path):
    data = json.load(open(path))
    verdicts = data["verdicts"] if isinstance(data, dict) else data
    rewrites = [v for v in verdicts if v.get("verdict", "REWRITE") == "REWRITE" and v.get("fix")]
    drops = [v for v in verdicts if v.get("verdict") == "DROP"]
    ok = 0
    for v in rewrites:
        fields = {k: val for k, val in v["fix"].items() if k in ("Text", "Back Extra")}
        # Agents HTML-escaped their tags one level (&lt;br&gt; for <br>, &amp;nbsp; for
        # &nbsp;). Reverse exactly one level so real markup lands in the field.
        fields = {k: html.unescape(val) for k, val in fields.items()}
        if not fields:
            continue
        call("updateNoteFields", note={"id": int(v["noteId"]), "fields": fields})
        ok += 1
    print(f"applied {ok} REWRITE fix(es) to Anki")
    if drops:
        print(f"\n{len(drops)} DROP proposal(s) — REVIEW MANUALLY (not auto-deleted):")
        for d in drops:
            print(f"  noteId {d['noteId']}: {d.get('reason','')}")
    return ok


def resync(chapters):
    for ch in chapters:
        ids = call("findNotes", query=f'deck:"all::EMT::Chapter {ch}"')
        notes = call("notesInfo", notes=ids)
        cards = []
        for n in notes:
            f = n["fields"]
            text = f.get("Text", {}).get("value", "")
            be = f.get("Back Extra", {}).get("value", "")
            cards.append({
                "Text": text,
                "Back Extra": be,
                "chapter": ch,
                "needs_human_check": bool(VALUE.search(readable(text))),
                "image": None,
            })
        out = f"{HERE}/chapter_{ch}_cards.json"
        json.dump(cards, open(out, "w"), indent=1, ensure_ascii=False)
        print(f"ch{ch}: resynced {len(cards)} -> chapter_{ch}_cards.json")


if __name__ == "__main__":
    if sys.argv[1] == "--apply":
        apply_fixes(sys.argv[2])
    elif sys.argv[1] == "--resync":
        resync([int(x) for x in sys.argv[2:]])
