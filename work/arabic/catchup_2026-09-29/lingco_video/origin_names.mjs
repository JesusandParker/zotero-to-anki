import { chromium } from 'playwright-core';
import fs from 'fs';
const [,, wantPath, outPath] = process.argv;
const want = JSON.parse(fs.readFileSync(wantPath, 'utf8'));
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = browser.contexts()[0];
const out = {};
for (const w of want) {
  try {
    const r = await ctx.request.get(`https://class.lingco.io/api/assets/${w.uuid}`, { maxRedirects: 0, timeout: 30000 });
    const loc = r.headers()['location'] || '';
    out[w.uuid] = { status: r.status(), origin: decodeURIComponent((loc.split('?')[0] || '').split('/').pop() || '') };
  } catch (e) { out[w.uuid] = { err: String(e).slice(0, 150) }; }
}
fs.writeFileSync(outPath, JSON.stringify(out, null, 0));
console.log(Object.keys(out).length, Object.values(out).filter(v => v.origin).length);
process.exit(0);
