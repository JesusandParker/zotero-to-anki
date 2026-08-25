#!/usr/bin/env python3
"""Post-stage media audit — every reference must resolve, byte-for-byte, lowercase.

Created 2026-08-08 (Arabic Unit 1) after two invisible-on-the-Mac failures shipped:
  R45  same-filename media replacement kept serving the STALE image (webview caches by name)
  R47  five videos referenced as `..._Saad.mp4` while the collection held `..._saad.mp4` —
       plays on macOS (case-insensitive fs), silently BROKEN audio on iPhone.
Both are exactly the kind of defect a Mac-side visual check can never catch, and exactly the
kind a set-difference catches in milliseconds. Run after EVERY stage/update pass.

    python3 scripts/media_audit.py --deck 'all::...::Unit 1::Book Highlights' --prefix arabic_

Exit 0 only when: no broken refs, no uppercase names, no pipeline-prefixed orphans.
"""
import json, re, sys, argparse, urllib.request

def anki(action, **params):
    r = urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765",
        json.dumps({"action": action, "version": 6, "params": params}).encode()))
    out = json.load(r)
    if out.get("error"):
        raise SystemExit(f"AnkiConnect {action}: {out['error']}")
    return out["result"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True, help="deck query to audit (children included)")
    ap.add_argument("--prefix", required=True, help="pipeline media prefix, e.g. arabic_")
    a = ap.parse_args()

    nids = anki("findNotes", query=f'deck:"{a.deck}"')
    if not nids:
        raise SystemExit(f"no notes found in deck: {a.deck}")
    refs = set()
    for n in anki("notesInfo", notes=nids):
        blob = "".join(f["value"] for f in n["fields"].values())
        refs |= set(re.findall(r"\[sound:([^\]]+)\]", blob))
        refs |= set(re.findall(r'<img src="([^"]+)"', blob))
    refs = {r for r in refs if r.startswith(a.prefix)}
    have = set(anki("getMediaFilesNames", pattern=f"{a.prefix}*"))

    broken   = sorted(refs - have)
    upper    = sorted(r for r in refs | have if r != r.lower())
    orphans  = sorted(have - refs)

    print(f"media audit: {len(nids)} notes, {len(refs)} prefixed refs, {len(have)} files")
    ok = True
    for label, items, why in (
        ("BROKEN refs", broken, "reference does not resolve byte-for-byte (R45/R47)"),
        ("UPPERCASE names", upper, "breaks on case-sensitive mobile filesystems (R47)"),
        ("ORPHANED files", orphans, "staged media attached to nothing — missed attachment or waste"),
    ):
        if items:
            ok = False
            print(f"  {label} ({why}):")
            for i in items:
                print(f"    {i}")
    print("  all clear ✓" if ok else "  FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
