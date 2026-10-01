// QA de render de TODAS las páginas de dist/ en escritorio (1440) y móvil (390): desborde horizontal, imágenes locales rotas,
// errores de JS, iframes mal proporcionados, textos con restos de plantilla, H1 y elementos que sobresalen del viewport.
// Uso: node scripts/qa_render.mjs <salida.jsonl> [filtro de ruta]   (sirve dist/ en un puerto libre; bloquea peticiones externas)
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const DIST = path.resolve('dist'); const OUT = process.argv[2] || 'migracion/qa_render.jsonl'; const FILTER = process.argv[3] || '';
const MIME = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json','.ico':'image/x-icon','.gif':'image/gif','.mp4':'video/mp4'};
const srv = http.createServer((req,res)=>{ let p=decodeURIComponent(req.url.split('?')[0]); let f=path.join(DIST,p); if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); if(!fs.existsSync(f)){res.writeHead(404);return res.end('404');} res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r=>srv.listen(0,r)); const base=`http://localhost:${srv.address().port}`;
function walk(dir, acc) { for (const e of fs.readdirSync(dir, { withFileTypes: true })) { const p = path.join(dir, e.name); if (e.isDirectory()) walk(p, acc); else if (e.name === 'index.html') acc.push(p); } return acc; }
let pages = walk(DIST, []).map(f => '/' + path.relative(DIST, path.dirname(f)).split(path.sep).join('/')).map(u => u === '/.' ? '/' : (u.endsWith('/') ? u : u + '/')).filter(u => !u.startsWith('/410') && !u.startsWith('/404'));
if (FILTER) pages = pages.filter(u => u.includes(FILTER));
console.log('páginas:', pages.length);
const browser = await chromium.launch();
const out = fs.createWriteStream(OUT); let done = 0; const t0 = Date.now();
const CHECK = () => {
  const iw = innerWidth; const r = {};
  r.scrollW = document.documentElement.scrollWidth; r.innerW = iw;
  const over = [];
  for (const el of document.querySelectorAll('body *')) { const b = el.getBoundingClientRect(); if (b.width > 0 && (b.right > iw + 2 || b.left < -2) && getComputedStyle(el).position !== 'fixed') { over.push((el.tagName.toLowerCase() + '.' + String(el.className || '').split(' ').slice(0, 2).join('.')).slice(0, 60)); if (over.length >= 4) break; } }
  r.over = over;
  r.brokenImg = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && /^\/|^http:\/\/localhost/.test(i.getAttribute('src') || '')).map(i => i.getAttribute('src')).slice(0, 5);
  r.iframes = [...document.querySelectorAll('iframe')].map(f => { const b = f.getBoundingClientRect(); return { src: (f.getAttribute('src') || f.getAttribute('data-src') || '').replace(/^https?:\/\/(www\.)?/, '').slice(0, 50), w: Math.round(b.width), h: Math.round(b.height) }; }).slice(0, 6);
  r.h1 = document.querySelectorAll('h1').length;
  const txt = document.body.innerText || '';
  r.tpl = (txt.match(/\{\{[^}]*\}\}|\[object |undefined|NaN\b|\{\w+\}/g) || []).slice(0, 4);
  r.maskEmpty = document.querySelectorAll('[style*="mask-image: url(\\"\\")"],[style*="mask-image:url(\\"\\")"]').length;
  r.emptyHref = document.querySelectorAll('a[href=""],a[href="#"]:not([role])').length;
  r.wpContent = document.documentElement.outerHTML.split('wp-content').length - 1;
  r.bodyH = document.body.scrollHeight;
  return r;
};
async function worker(list, vp, tag) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
  await ctx.route('**/*', route => { const u = route.request().url(); if (u.startsWith(base)) route.continue(); else route.abort(); });
  const p = await ctx.newPage(); let errs = [];
  p.on('pageerror', e => errs.push(String(e.message).slice(0, 120)));
  for (const u of list) {
    errs = [];
    try { await p.goto(base + u, { waitUntil: 'load', timeout: 30000 }); await p.waitForTimeout(150); const r = await p.evaluate(CHECK); r.url = u; r.vp = tag; r.errs = errs.slice(0, 3); out.write(JSON.stringify(r) + '\n'); }
    catch (e) { out.write(JSON.stringify({ url: u, vp: tag, fail: String(e.message).slice(0, 120) }) + '\n'); }
    done++; if (done % 200 === 0) console.log(done, 'hechas', Math.round((Date.now() - t0) / 1000) + 's');
  }
  await ctx.close();
}
const N = 4; const chunks = Array.from({ length: N }, (_, i) => pages.filter((_, k) => k % N === i));
await Promise.all([...chunks.map(c => worker(c, { width: 1440, height: 900 }, 'desk')), ...chunks.map(c => worker(c, { width: 390, height: 844 }, 'mob'))]);
out.end(); await browser.close(); srv.close(); console.log('FIN', done, 'resultados en', OUT, Math.round((Date.now() - t0) / 1000) + 's');
