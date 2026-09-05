"""Render inventory_final.json -> arab101_gap_audit.html (artifact) + ARAB 101 - Vocab Gap Audit.md (Drive)."""
import json, html, sys, os, re
OUT = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(f"{OUT}/inventory_final.json", encoding="utf-8"))
E = html.escape
def ar(s):  return f'<span class="ar" lang="ar" dir="rtl">{E(s)}</span>'
def tr(s):  return f'<code class="tr">{E(s)}</code>'
def chip(status):
    cls = {"REQUIRED":"req","TAUGHT":"taught","USED":"taught","OPTIONAL":"opt","INCIDENTAL":"opt","GATED":"gated","PRESENT":"ok","STALE":"stale"}.get(status,"opt")
    return f'<span class="chip {cls}">{E(status.lower())}</span>'
def table(rows, cols):
    th = "".join(f"<th>{E(c[0])}</th>" for c in cols)
    body = []
    for r in rows:
        tds = []
        for label, key, kind in cols:
            v = r.get(key, "")
            if kind == "ar": tds.append(f'<td class="c-ar">{ar(v)}</td>')
            elif kind == "tr": tds.append(f'<td class="c-tr">{tr(v)}</td>')
            elif kind == "chip": tds.append(f'<td class="c-chip">{chip(v)}</td>')
            else: tds.append(f'<td class="c-txt">{E(v)}</td>')
        body.append("<tr>" + "".join(tds) + "</tr>")
    widths = {5: (17,16,22,37,8), 4: (18,16,28,38)}.get(len(cols), None)
    cg = "".join(f'<col style="width:{w}%">' for w in widths) if widths else ""
    return f'<div class="tablewrap"><table><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
sec = inv["sections"]; counts = inv["counts"]
parts = []
parts.append(f"""<header class="masthead">
<p class="eyebrow">ARAB 101 · Dr. Khouri · through Thursday, September 3</p>
<h1>{E(inv['title'])}</h1>
<p class="lede">{E(inv['lede'])}</p>
<div class="strip">
  <div class="stat"><span class="n">{counts['required_missing']}</span><span class="l">required, missing</span></div>
  <div class="stat"><span class="n">{counts['taught_missing']}</span><span class="l">taught, missing</span></div>
  <div class="stat"><span class="n">{counts['gated']}</span><span class="l">in Anki but suspended</span></div>
  <div class="stat"><span class="n">{counts['present']}</span><span class="l">present and fine</span></div>
</div>
</header>""")
for s in sec:
    parts.append(f'<section id="{E(s["id"])}"><h2>{E(s["heading"])}</h2>')
    if s.get("intro"): parts.append(f'<p class="intro">{E(s["intro"])}</p>')
    if s.get("rows"):
        cols = [tuple(c) for c in s["cols"]]
        parts.append(table(s["rows"], cols))
    for p in s.get("paras", []): parts.append(f"<p>{E(p)}</p>")
    if s.get("bullets"):
        parts.append("<ul>" + "".join(f"<li>{E(b)}</li>" for b in s["bullets"]) + "</ul>")
    if s.get("drills"):
        parts.append('<div class="drills">')
        for d in s["drills"]:
            words = " ".join(f'{ar(w)}' for w in d["words"])
            parts.append(f'<div class="drill"><div class="drill-h">{E(d["label"])}</div><div class="drill-w" dir="rtl" lang="ar">{words}</div></div>')
        parts.append("</div>")
    parts.append("</section>")
parts.append(f'<footer><p class="eyebrow">Method</p><p>{E(inv["method"])}</p></footer>')
CSS = """
:root{--ground:#ffffff;--ink:#1e1a16;--muted:#6b6259;--rule:#e6e0d8;--soft:#f6f2ec;--red:#b5232a;--red-ink:#ffffff;--blue:#2b5c8a;--olive:#7a6a2f;--green:#2f6b45;--chip-ink:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ground:#17191c;--ink:#ece7df;--muted:#a39b91;--rule:#33373d;--soft:#1f2226;--red:#f0616a;--red-ink:#17191c;--blue:#7fb0e0;--olive:#c9b45a;--green:#7cc29a;--chip-ink:#17191c}}
:root[data-theme="dark"]{--ground:#17191c;--ink:#ece7df;--muted:#a39b91;--rule:#33373d;--soft:#1f2226;--red:#f0616a;--red-ink:#17191c;--blue:#7fb0e0;--olive:#c9b45a;--green:#7cc29a;--chip-ink:#17191c}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:"Source Serif 4",Georgia,"Times New Roman",serif;font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased}
main{max-width:76ch;margin:0 auto;padding:2.5rem 1.25rem 4rem}
.ar{font-family:"Noto Naskh Arabic","Geeza Pro","Amiri",serif;font-size:1.3em;line-height:1.5;unicode-bidi:isolate;direction:rtl}
.tr{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:0.84em;background:var(--soft);padding:0.05em 0.35em;border-radius:3px;overflow-wrap:anywhere}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);margin:0 0 0.6rem}
h1{font-size:2.1rem;line-height:1.15;margin:0 0 0.8rem;font-weight:700;text-wrap:balance;letter-spacing:-0.01em}
h2{font-size:1.35rem;margin:2.6rem 0 0.6rem;padding-top:1.2rem;border-top:1px solid var(--rule);text-wrap:balance}
.lede{font-size:1.08rem;color:var(--ink);max-width:66ch;margin:0 0 1.4rem}
.intro{color:var(--muted);margin:0 0 0.9rem;max-width:66ch}
.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:1px solid var(--rule);border-radius:6px;overflow:hidden}
.stat{padding:0.8rem 0.9rem;border-right:1px solid var(--rule);display:flex;flex-direction:column;gap:0.15rem}
.stat:last-child{border-right:0}
.stat .n{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:1.7rem;font-weight:600;font-variant-numeric:tabular-nums;line-height:1}
.stat:first-child .n{color:var(--red)}
.stat .l{font-size:0.78rem;color:var(--muted);letter-spacing:0.02em}
@media (max-width:620px){.strip{grid-template-columns:repeat(2,1fr)}.stat:nth-child(2){border-right:0}.stat:nth-child(1),.stat:nth-child(2){border-bottom:1px solid var(--rule)}}
.tablewrap{overflow-x:auto;margin:0.4rem 0 1rem}
table{border-collapse:collapse;width:100%;min-width:640px;font-size:0.95rem;table-layout:fixed}
th{text-align:left;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--muted);font-weight:500;padding:0.45rem 0.6rem 0.45rem 0;border-bottom:1px solid var(--ink)}
td{vertical-align:top;padding:0.55rem 0.6rem 0.55rem 0;border-bottom:1px solid var(--rule)}
td.c-ar{text-align:right;overflow-wrap:anywhere}
td.c-tr{overflow-wrap:anywhere}
td.c-txt{overflow-wrap:break-word}
.chip{display:inline-block;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:0.66rem;letter-spacing:0.08em;text-transform:uppercase;padding:0.15em 0.5em;border-radius:3px;white-space:nowrap}
.chip.req{background:var(--red);color:var(--red-ink)}
.chip.taught{border:1px solid var(--blue);color:var(--blue)}
.chip.opt{border:1px solid var(--olive);color:var(--olive)}
.chip.gated{border:1px solid var(--muted);color:var(--muted)}
.chip.ok{border:1px solid var(--green);color:var(--green)}
.chip.stale{background:var(--olive);color:var(--chip-ink)}
ul{padding-left:1.2rem;margin:0.4rem 0 1rem}
li{margin:0.3rem 0}
.drills{display:grid;gap:0.8rem;margin:0.6rem 0 1rem}
.drill{display:grid;grid-template-columns:minmax(14ch,22ch) 1fr;gap:0.8rem;align-items:baseline;border-bottom:1px solid var(--rule);padding-bottom:0.6rem}
.drill-h{font-size:0.86rem;color:var(--muted)}
.drill-w{display:flex;flex-wrap:wrap;gap:0.4rem 1.2rem;justify-content:flex-start}
footer{margin-top:3rem;padding-top:1.2rem;border-top:1px solid var(--rule);color:var(--muted);font-size:0.9rem}
@media (max-width:620px){.drill{grid-template-columns:1fr}}
"""
page = f"""<title>{E(inv['title'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>
<main>{"".join(parts)}</main>"""
open(f"{OUT}/arab101_gap_audit.html","w",encoding="utf-8").write(page)
# ---- markdown twin
md = [f"# {inv['title']}", "", f"_ARAB 101, Dr. Khouri, through Thu 9/3 · audit run 2026-09-05_", "", inv["lede"], "",
      f"**{counts['required_missing']}** required + **{counts['taught_missing']}** taught words missing · **{counts['gated']}** notes suspended by the letter gate · **{counts['present']}** present and fine", ""]
for s in sec:
    md += [f"## {s['heading']}", ""]
    if s.get("intro"): md += [s["intro"], ""]
    if s.get("rows"):
        cols=[tuple(c) for c in s["cols"]]
        md.append("| " + " | ".join(c[0] for c in cols) + " |"); md.append("|" + "---|"*len(cols))
        for r in s["rows"]:
            cells=[]
            for label,key,kind in cols:
                v=str(r.get(key,"")).replace("|","／")
                cells.append(f"`{v}`" if kind=="tr" else v)
            md.append("| " + " | ".join(cells) + " |")
        md.append("")
    for p in s.get("paras", []): md += [p, ""]
    if s.get("bullets"): md += [f"- {b}" for b in s["bullets"]] + [""]
    if s.get("drills"):
        for d in s["drills"]: md.append(f"- **{d['label']}:** " + " · ".join(d["words"]))
        md.append("")
md += ["## Method", "", inv["method"], ""]
open(f"{OUT}/ARAB 101 - Vocab Gap Audit (2026-09-05).md","w",encoding="utf-8").write("\n".join(md))
print("rendered", len(page), "bytes html;", len("\n".join(md)), "bytes md")
