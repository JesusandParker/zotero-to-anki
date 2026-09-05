#!/usr/bin/env python3
"""Render review from the HP (night shift) — the same contract as scripts/render_check.py,
which is written for the Mac (its Chrome path and collection.media path). Anki is reached
through the SSH tunnel; media is pulled through AnkiConnect (retrieveMediaFile) instead of
read from disk; screenshots use the HP's google-chrome with a throwaway profile.

    python3 work/arabic/night_render_check_hp.py --notes 123 456 --out /tmp/rc.png

Every card of every listed note is rendered (question AND answer sides), wrapped in the
note type's real CSS inside a dir="auto" harness, then tiled into one contact sheet.
LOOK at it: direction (no flipped colons/periods), one play button per clip, crops
complete with even margins, no boilerplate, both cloze directions.
"""
import argparse, base64, json, os, re, subprocess, urllib.request

CHROME = "/usr/bin/google-chrome"

def anki(action, **params):
    r = urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765",
        json.dumps({"action": action, "version": 6, "params": params}).encode()), timeout=60)
    out = json.load(r)
    if out.get("error"):
        raise SystemExit(f"AnkiConnect {action}: {out['error']}")
    return out["result"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", nargs="+", type=int, required=True)
    ap.add_argument("--model", default="AnKing Cloze")
    ap.add_argument("--out", default="/tmp/night_render_check.png")
    a = ap.parse_args()
    css = anki("modelStyling", modelName=a.model)["css"]
    media = "/tmp/rc_media"; os.makedirs(media, exist_ok=True)
    prof = "/tmp/rc_chrome_profile"; os.makedirs(prof, exist_ok=True)

    def localize(html):
        def sub(m):
            fn = m.group(1)
            if fn.startswith(("http", "file", "_")):
                return m.group(0)
            p = os.path.join(media, fn)
            if not os.path.exists(p):
                data = anki("retrieveMediaFile", filename=fn)
                if data:
                    open(p, "wb").write(base64.b64decode(data))
            return f'src="file://{p}"'
        return re.sub(r'src="([^"]+)"', sub, html)

    shots = []
    for nid in a.notes:
        for ci in sorted(anki("cardsInfo", cards=anki("findCards", query=f"nid:{nid}")), key=lambda c: c["ord"]):
            for side in ("question", "answer"):
                html = localize(ci[side])
                # Anki's webview turns [anki:play:...] markers into play buttons; show a
                # visible stand-in so the COUNT of buttons per clip can be checked.
                html = re.sub(r"\[anki:play:[^\]]+\]", "<span style='border:1px solid #888;padding:0 6px;border-radius:4px'>&#9654;</span>", html)
                page = (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>'
                        f'<body class="card nightMode night_mode" style="background:#2f2f31" dir="auto">'
                        f'<div id="qa">{html}</div></body></html>')
                fn = f"/tmp/rc_{nid}_{ci['ord']}_{side[0]}"
                open(fn + ".html", "w", encoding="utf-8").write(page)
                subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}",
                                "--no-first-run", f"--screenshot={fn}.png", "--window-size=640,900",
                                "--hide-scrollbars", f"file://{fn}.html"], capture_output=True, timeout=120)
                if os.path.exists(fn + ".png"):
                    shots.append(fn + ".png")
    if not shots:
        raise SystemExit("no screenshots produced")
    rows = []
    for i in range(0, len(shots), 4):
        row = f"/tmp/rc_row{i}.png"
        subprocess.run(["magick", *shots[i:i+4], "+append", row], check=True)
        rows.append(row)
    subprocess.run(["magick", *rows, "-append", "-resize", "1600x", a.out], check=True)
    print(f"{len(shots)} rendered sides -> {a.out}")
    print("NOW LOOK AT IT: direction, one play button per clip, complete symmetric crops, no boilerplate, both cloze directions.")

if __name__ == "__main__":
    main()
