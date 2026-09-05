import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(f"{HERE}/review_data.json",encoding="utf-8"))
CSS = """
:root{
  --ground:#f5f2ec; --panel:#fffdf9; --ink:#1a1c22; --dim:#6b6a66; --faint:#98958e;
  --rule:#e2ddd2; --hair:#eeeae0;
  --ink-accent:#1c5e63; --ink-accent-soft:#dcecec;
  --good:#2f6b45; --good-soft:#e2efe6;
  --bad:#a8342c; --bad-soft:#f6e4e1;
  --book:#7a6320; --book-soft:#f2eada;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --ground:#14161a; --panel:#1b1e24; --ink:#eceae4; --dim:#a3a099; --faint:#77746e;
  --rule:#2e323a; --hair:#252932;
  --ink-accent:#5cc7cd; --ink-accent-soft:#123236;
  --good:#7cc29a; --good-soft:#16301f;
  --bad:#f0837a; --bad-soft:#331a18;
  --book:#d3b664; --book-soft:#2b2413;
}}
:root[data-theme="dark"]{
  --ground:#14161a; --panel:#1b1e24; --ink:#eceae4; --dim:#a3a099; --faint:#77746e;
  --rule:#2e323a; --hair:#252932;
  --ink-accent:#5cc7cd; --ink-accent-soft:#123236;
  --good:#7cc29a; --good-soft:#16301f;
  --bad:#f0837a; --bad-soft:#331a18;
  --book:#d3b664; --book-soft:#2b2413;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"Instrument Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
main{max-width:60rem;margin:0 auto;padding:1.75rem 1rem 5rem}
.ar{font-family:"Noto Naskh Arabic","Geeza Pro",serif;direction:rtl;unicode-bidi:isolate;line-height:1.6}
.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}
.serif{font-family:"Newsreader",Georgia,serif}

header{margin-bottom:1.5rem}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin:0 0 .5rem}
h1{font-family:"Newsreader",Georgia,serif;font-size:2rem;line-height:1.1;margin:0 0 .5rem;
  font-weight:600;letter-spacing:-.01em;text-wrap:balance}
.lede{color:var(--dim);max-width:42rem;margin:0 0 1.25rem;font-size:.98rem}

.bar{position:sticky;top:0;z-index:20;background:var(--ground);
  border-bottom:1px solid var(--rule);padding:.7rem 0 .65rem;margin-bottom:1.25rem;
  display:flex;align-items:center;gap:.9rem;flex-wrap:wrap}
.track{flex:1 1 12rem;height:5px;border-radius:3px;background:var(--hair);overflow:hidden;min-width:8rem}
.fill{height:100%;width:0%;background:var(--ink-accent);transition:width .3s ease}
.tally{font-family:"IBM Plex Mono",monospace;font-size:.78rem;color:var(--dim);
  font-variant-numeric:tabular-nums;white-space:nowrap}
.tally b{color:var(--ink);font-weight:600}
.savestate{font-family:"IBM Plex Mono",monospace;font-size:.68rem;color:var(--faint);white-space:nowrap}

.card{background:var(--panel);border:1px solid var(--rule);border-radius:10px;
  padding:1rem 1.1rem;margin-bottom:.7rem;transition:border-color .15s,box-shadow .15s}
.card[data-v="good"]{border-color:var(--good);box-shadow:inset 3px 0 0 var(--good)}
.card[data-v="bad"]{border-color:var(--bad);box-shadow:inset 3px 0 0 var(--bad)}
.card.cur{outline:2px solid var(--ink-accent);outline-offset:2px}

.top{display:flex;gap:1rem;align-items:flex-start;flex-wrap:wrap}
.word{flex:1 1 15rem;min-width:0}
.wordar{font-family:"Noto Naskh Arabic","Geeza Pro",serif;direction:rtl;unicode-bidi:isolate;
  text-align:left;font-size:1.75rem;line-height:1.5;margin:0 0 .15rem;overflow-wrap:anywhere}
.wordtr{font-family:"IBM Plex Mono",monospace;font-size:.9rem;color:var(--ink-accent);margin:0 0 .3rem;
  overflow-wrap:anywhere}
.wordmean{font-family:"Newsreader",Georgia,serif;font-size:1.02rem;color:var(--dim);margin:0;
  overflow-wrap:break-word}
.play{flex:0 0 auto;display:flex;flex-direction:column;gap:.4rem;align-items:stretch}

button{font:inherit;cursor:pointer;border-radius:7px;border:1px solid var(--rule);
  background:var(--panel);color:var(--ink);transition:background .12s,border-color .12s,color .12s}
button:focus-visible{outline:2px solid var(--ink-accent);outline-offset:2px}
.pbtn{display:flex;align-items:center;gap:.5rem;padding:.5rem .8rem;
  border-color:var(--ink-accent);color:var(--ink-accent);background:var(--ink-accent-soft);
  font-size:.86rem;white-space:nowrap}
.pbtn:hover{filter:brightness(.97)}
.pbtn .tri{font-size:.7rem;line-height:1}
.pbtn .who{font-family:"IBM Plex Mono",monospace;font-size:.7rem;letter-spacing:.03em}
.pbtn.book{border-color:var(--book);color:var(--book);background:var(--book-soft)}
.pbtn.on{background:var(--ink-accent);color:var(--panel)}
.pbtn.book.on{background:var(--book);color:var(--panel)}

.heard{font-family:"IBM Plex Mono",monospace;font-size:.7rem;color:var(--faint);
  margin:.55rem 0 0;line-height:1.6;overflow-wrap:anywhere}
.heard .k{color:var(--dim)}

.verdict{display:flex;gap:.5rem;margin-top:.75rem;flex-wrap:wrap;align-items:center}
.vbtn{padding:.4rem .85rem;font-size:.85rem;display:flex;gap:.4rem;align-items:center}
.vbtn.g[aria-pressed="true"]{background:var(--good-soft);border-color:var(--good);color:var(--good);font-weight:600}
.vbtn.b[aria-pressed="true"]{background:var(--bad-soft);border-color:var(--bad);color:var(--bad);font-weight:600}
.slug{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-size:.68rem;color:var(--faint)}

.fixbox{margin-top:.7rem;padding:.75rem;border:1px dashed var(--bad);border-radius:8px;background:var(--bad-soft)}
.fixq{font-size:.8rem;color:var(--dim);margin:0 0 .5rem}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.55rem}
.chip{padding:.3rem .6rem;font-size:.76rem;border-radius:20px}
.chip[aria-pressed="true"]{background:var(--bad);border-color:var(--bad);color:var(--panel);font-weight:600}
textarea{width:100%;min-height:3.2rem;padding:.5rem .6rem;border-radius:7px;border:1px solid var(--rule);
  background:var(--panel);color:var(--ink);font:inherit;font-size:.86rem;resize:vertical}
textarea:focus-visible{outline:2px solid var(--ink-accent);outline-offset:1px}

h2{font-family:"Newsreader",Georgia,serif;font-size:1.2rem;margin:2.25rem 0 .3rem;
  padding-top:1.1rem;border-top:1px solid var(--rule);font-weight:600}
.sub{color:var(--dim);font-size:.9rem;margin:0 0 .9rem;max-width:44rem}
.noaud{background:none;border:1px solid var(--hair);border-radius:8px;padding:.7rem .9rem;margin-bottom:.5rem}
.noaud .wordar{font-size:1.35rem;text-align:left}
.noaud .why{font-size:.8rem;color:var(--faint);margin:.35rem 0 0}
.hint{font-family:"IBM Plex Mono",monospace;font-size:.7rem;color:var(--faint);margin-top:1.5rem;line-height:1.7}
kbd{font-family:"IBM Plex Mono",monospace;font-size:.9em;border:1px solid var(--rule);
  border-radius:4px;padding:.05em .3em;background:var(--hair);color:var(--dim)}
@media (max-width:560px){ .top{flex-direction:column} .play{width:100%} .pbtn{justify-content:center} h1{font-size:1.6rem} }
"""

JS = r"""
const DATA = __DATA__;
const AUDIO = __MEDIA__;
const REASONS = [
  ["early",  "starts too late — clips the beginning"],
  ["late",   "ends too early — cuts the word off"],
  ["extra",  "extra sound / another word attached"],
  ["wrong",  "that is not the word"],
  ["nother", "that is not her voice"],
  ["quiet",  "too quiet or muddy to use"],
];
let db=null, cur=0, state={};
const $=(s,r=document)=>r.querySelector(s);
const url = f => "data:audio/mpeg;base64," + AUDIO[f];

/* ---------- persistence: db when granted, localStorage always ---------- */
const LS="arab_clip_verdicts_v1";
function loadLocal(){ try{ return JSON.parse(localStorage.getItem(LS)||"{}"); }catch(e){ return {}; } }
function saveLocal(){ try{ localStorage.setItem(LS, JSON.stringify(state)); }catch(e){} }
async function save(slug){
  saveLocal();
  const rec = state[slug];
  if(!db || !rec) return;
  try{
    await db.doc("verdicts/"+slug).set({
      slug, verdict: rec.verdict||"", reasons: rec.reasons||[], note: rec.note||"",
      at: new Date().toISOString()
    });
    setSave("saved");
  }catch(e){ setSave("saved on this device only"); }
}
function setSave(t){ const el=$("#savestate"); if(el) el.textContent=t; }

/* ---------- audio ---------- */
let playing=null;
function play(file, btn){
  if(playing){ playing.a.pause(); playing.btn.classList.remove("on"); }
  const a=new Audio(url(file));
  playing={a,btn}; btn.classList.add("on");
  a.onended=()=>{ btn.classList.remove("on"); playing=null; };
  a.play().catch(()=>{ btn.classList.remove("on"); playing=null; });
}

/* ---------- render ---------- */
function tally(){
  const withAudio = DATA.words.filter(w=>w.clips.length);
  const done = withAudio.filter(w=>state[w.slug]&&state[w.slug].verdict).length;
  const bad  = withAudio.filter(w=>state[w.slug]&&state[w.slug].verdict==="bad").length;
  $("#fill").style.width = (100*done/withAudio.length)+"%";
  $("#tally").innerHTML = `<b>${done}</b> of ${withAudio.length} checked` + (bad?` · <b>${bad}</b> to fix`:"");
}
function cardHTML(w,i){
  const clips = w.clips.map((c,j)=>`
    <button class="pbtn ${c.label==='book'?'book':''}" data-play="${c.file}" title="${c.note}">
      <span class="tri">▶</span><span>${c.dur??""}s</span><span class="who">${c.label}</span>
    </button>`).join("");
  const heard = w.clips.map(c=>`<div><span class="k">whisper heard</span> ar ${c.ar?`“${c.ar}”`:"—"} · en ${c.en?`“${c.en}”`:"—"}</div>`).join("");
  return `<div class="card" data-i="${i}" data-slug="${w.slug}">
    <div class="top">
      <div class="word">
        ${w.ar?`<p class="wordar">${w.ar}</p>`:""}
        ${w.tr?`<p class="wordtr">${w.tr}</p>`:""}
        <p class="wordmean">${w.mean}</p>
      </div>
      <div class="play">${clips}</div>
    </div>
    <div class="heard">${heard}<div><span class="k">from</span> ${w.where||""}</div></div>
    <div class="verdict">
      <button class="vbtn g" data-v="good" aria-pressed="false">✓ Sounds right</button>
      <button class="vbtn b" data-v="bad" aria-pressed="false">✗ Something’s off</button>
      <span class="slug">${w.slug}</span>
    </div>
    <div class="fixbox" hidden>
      <p class="fixq">What’s wrong with it? Tap any that apply — this is what I’ll use to recut it.</p>
      <div class="chips">${REASONS.map(([k,l])=>`<button class="chip" data-r="${k}" aria-pressed="false">${l}</button>`).join("")}</div>
      <textarea placeholder="Anything else — what you actually hear, or where it should start and stop."></textarea>
    </div>
  </div>`;
}
function render(){
  const withA = DATA.words.filter(w=>w.clips.length);
  const without = DATA.words.filter(w=>!w.clips.length);
  $("#list").innerHTML = withA.map((w,i)=>cardHTML(w,i)).join("");
  $("#noaudio").innerHTML = without.map(w=>`<div class="noaud">
      ${w.ar?`<p class="wordar">${w.ar}</p>`:""}
      ${w.tr?`<p class="wordtr">${w.tr}</p>`:""}
      <p class="wordmean">${w.mean}</p>
      <p class="why">${w.why.replace(/^NO AUDIO — /,"")}</p>
    </div>`).join("");
  withA.forEach(w=>{ const rec=state[w.slug]; if(rec&&rec.verdict) paint(w.slug); });
  tally(); focus(0);
}
function paint(slug){
  const card=$(`.card[data-slug="${slug}"]`); if(!card) return;
  const rec=state[slug]||{};
  card.dataset.v=rec.verdict||"";
  card.querySelectorAll(".vbtn").forEach(b=>b.setAttribute("aria-pressed", String(b.dataset.v===rec.verdict)));
  const fix=card.querySelector(".fixbox");
  fix.hidden = rec.verdict!=="bad";
  card.querySelectorAll(".chip").forEach(c=>c.setAttribute("aria-pressed", String((rec.reasons||[]).includes(c.dataset.r))));
  const ta=card.querySelector("textarea"); if(ta && ta.value!==(rec.note||"")) ta.value=rec.note||"";
}
function focus(i){
  const cards=[...document.querySelectorAll(".card")]; if(!cards.length) return;
  cur=Math.max(0,Math.min(i,cards.length-1));
  cards.forEach((c,j)=>c.classList.toggle("cur",j===cur));
}
function setVerdict(slug,v){
  const rec = state[slug] || (state[slug]={reasons:[],note:""});
  rec.verdict = rec.verdict===v ? "" : v;
  if(rec.verdict!=="bad"){ rec.reasons=[]; rec.note=""; }
  paint(slug); tally(); save(slug);
}
document.addEventListener("click",e=>{
  const p=e.target.closest("[data-play]"); if(p){ play(p.dataset.play,p); focus(+p.closest(".card").dataset.i); return; }
  const v=e.target.closest(".vbtn"); if(v){ setVerdict(v.closest(".card").dataset.slug, v.dataset.v); return; }
  const c=e.target.closest(".chip");
  if(c){ const slug=c.closest(".card").dataset.slug, rec=state[slug]||(state[slug]={reasons:[],note:""});
    rec.reasons=rec.reasons||[];
    const k=c.dataset.r, at=rec.reasons.indexOf(k);
    if(at>-1) rec.reasons.splice(at,1); else rec.reasons.push(k);
    paint(slug); save(slug); return; }
  const card=e.target.closest(".card"); if(card) focus(+card.dataset.i);
});
document.addEventListener("input",e=>{
  if(e.target.tagName!=="TEXTAREA") return;
  const slug=e.target.closest(".card").dataset.slug;
  const rec=state[slug]||(state[slug]={reasons:[],note:""});
  rec.note=e.target.value; saveLocal();
  clearTimeout(rec._t); rec._t=setTimeout(()=>save(slug),700);
});
document.addEventListener("keydown",e=>{
  if(e.target.tagName==="TEXTAREA"||e.metaKey||e.ctrlKey) return;
  const cards=[...document.querySelectorAll(".card")]; if(!cards.length) return;
  const k=e.key.toLowerCase();
  if(k==="j"){ focus(cur+1); cards[cur].scrollIntoView({block:"center",behavior:"smooth"}); e.preventDefault(); }
  else if(k==="k"){ focus(cur-1); cards[cur].scrollIntoView({block:"center",behavior:"smooth"}); e.preventDefault(); }
  else if(k===" "){ const b=cards[cur].querySelector("[data-play]"); if(b) b.click(); e.preventDefault(); }
  else if(k==="g"){ setVerdict(cards[cur].dataset.slug,"good"); e.preventDefault(); }
  else if(k==="b"){ setVerdict(cards[cur].dataset.slug,"bad"); e.preventDefault(); }
});

/* ---------- boot: render immediately, light up db when it answers ---------- */
state = loadLocal();
render();
(async()=>{
  try{
    const d = await claude.use("db");
    if(!d) { setSave("saved on this device"); return; }
    db = d;
    const snap = await db.collection("verdicts").get();
    let merged=false;
    snap.docs.forEach(doc=>{
      const v=doc.data(); if(!v) return;
      if(!state[v.slug] || !state[v.slug].verdict){
        state[v.slug]={verdict:v.verdict||"",reasons:v.reasons||[],note:v.note||""}; merged=true;
      }
    });
    if(merged){ Object.keys(state).forEach(paint); tally(); saveLocal(); }
    setSave("saved · Claude can read this");
  }catch(e){ setSave("saved on this device"); }
})();
"""

html_out = f"""<title>Khouri Clip Check</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<main>
<header>
  <p class="eyebrow">ARAB 101 &middot; Dr. Khouri &middot; audio check</p>
  <h1>Does she actually say the word?</h1>
  <p class="lede">Every clip on your new cards, in one place. Play it, then tell me if it sounds right.
  If it doesn&rsquo;t, say what&rsquo;s wrong and I&rsquo;ll recut it from the recording. Your answers save as you go.</p>
</header>
<div class="bar">
  <div class="track"><div class="fill" id="fill"></div></div>
  <div class="tally" id="tally">&nbsp;</div>
  <div class="savestate" id="savestate">&hellip;</div>
</div>
<div id="list"></div>
<h2>No clip to check</h2>
<p class="sub">These {sum(1 for w in D['words'] if not w['clips'])} cards ship silent on purpose. She only ever says these
words inside a running English sentence, and the book has no isolated recording, so I attached nothing rather than
something doubtful. If you want a voice on any of them, say which and I&rsquo;ll find one.</p>
<div id="noaudio"></div>
<p class="hint"><kbd>J</kbd> / <kbd>K</kbd> move &middot; <kbd>Space</kbd> plays &middot; <kbd>G</kbd> sounds right &middot; <kbd>B</kbd> something&rsquo;s off</p>
</main>
<script>{JS.replace("__DATA__", json.dumps({"words":D["words"]}, ensure_ascii=False)).replace("__MEDIA__", json.dumps(D["media"]))}</script>"""
open(f"{HERE}/khouri_clip_check.html","w",encoding="utf-8").write(html_out)
print("wrote", round(len(html_out.encode())/1024), "KB")
