// Diagnóstico de desbordes: para cada URL lista los elementos HOJA que sobresalen del viewport (sin hijos que sobresalgan),
// con su cadena de clases, anchos y CSS relevante. Uso: node scripts/dev/diag_overflow.mjs <ancho> <url1> <url2> ...
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const DIST = path.resolve('dist'); const W = parseInt(process.argv[2] || '390', 10); const URLS = process.argv.slice(3);
const MIME = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2'};
const srv = http.createServer((req,res)=>{ let p=decodeURIComponent(req.url.split('?')[0]); let f=path.join(DIST,p); if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); if(!fs.existsSync(f)){res.writeHead(404);return res.end('404');} res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r=>srv.listen(0,r)); const base=`http://localhost:${srv.address().port}`;
const browser = await chromium.launch(); const ctx = await browser.newContext({ viewport: { width: W, height: 844 } });
await ctx.route('**/*', route => route.request().url().startsWith(base) ? route.continue() : route.abort());
const p = await ctx.newPage();
for (const u of URLS) {
  await p.goto(base + u, { waitUntil: 'load' }); await p.waitForTimeout(200);
  const r = await p.evaluate(() => {
    const iw = innerWidth; const bad = [...document.querySelectorAll('body *')].filter(el => { if (el.closest('.hp-field')) return false; const b = el.getBoundingClientRect(); return b.width > 0 && b.right > iw + 2 && getComputedStyle(el).position !== 'fixed'; });
    const leaves = bad.filter(el => !bad.some(o => o !== el && el.contains(o)));
    const desc = el => { const cs = getComputedStyle(el); const b = el.getBoundingClientRect(); const chain = []; let n = el; for (let i = 0; i < 4 && n && n !== document.body; i++) { chain.push(n.tagName.toLowerCase() + (n.className ? '.' + String(n.className).trim().split(/\s+/).slice(0, 3).join('.') : '')); n = n.parentElement; } return { chain: chain.join(' < '), w: Math.round(b.width), right: Math.round(b.right), css: { width: cs.width, minW: cs.minWidth, ws: cs.whiteSpace, disp: cs.display, pad: cs.padding, ml: cs.marginLeft }, html: el.outerHTML.replace(/\s+/g, ' ').slice(0, 140) }; };
    return { scrollW: document.documentElement.scrollWidth, leaves: leaves.slice(0, 4).map(desc) };
  });
  console.log('==', u, 'scrollW', r.scrollW); for (const l of r.leaves) console.log('  ', JSON.stringify(l));
}
await browser.close(); srv.close();
