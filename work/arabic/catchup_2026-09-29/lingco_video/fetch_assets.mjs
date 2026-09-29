// Download Lingco asset UUIDs through the logged-in lu-chrome (CDP 9222). Usage: node run.mjs want.json outdir
import { chromium } from 'playwright-core';
import fs from 'fs';
const [,, wantPath, outDir] = process.argv;
const want = JSON.parse(fs.readFileSync(wantPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = browser.contexts()[0];
let ok = 0, bad = [];
for (const w of want) {
  const dest = `${outDir}/${w.file}`;
  if (fs.existsSync(dest) && fs.statSync(dest).size > 1000) { ok++; continue; }
  try {
    const r = await ctx.request.get(`https://class.lingco.io/api/assets/${w.uuid}`, { timeout: 60000 });
    const ct = r.headers()['content-type'] || '';
    const body = await r.body();
    if (r.status() !== 200 || body.length < 1000) { bad.push({ uuid: w.uuid, status: r.status(), ct, len: body.length }); continue; }
    fs.writeFileSync(dest, body); ok++;
  } catch (e) { bad.push({ uuid: w.uuid, err: String(e).slice(0, 200) }); }
}
console.log(JSON.stringify({ ok, bad }));
process.exit(0);
