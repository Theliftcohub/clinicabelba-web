// Capturas de las secciones de la home en móvil (390 px). Uso: node scripts/shots_mobile.mjs <carpeta de salida>
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const DIST = path.resolve('dist'); const OUT = process.argv[2] || 'migracion/screenshots'; fs.mkdirSync(OUT, { recursive: true });
const MIME = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2'};
const srv = http.createServer((req,res)=>{ let p=decodeURIComponent(req.url.split('?')[0]); let f=path.join(DIST,p); if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); if(!fs.existsSync(f)){res.writeHead(404);return res.end('404');} res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r=>srv.listen(0,r)); const base=`http://localhost:${srv.address().port}`;
const browser = await chromium.launch();
for (const [name,url] of [['mob','/'],['mob-ru','/ru/']]) {
  const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:2}); const p=await ctx.newPage();
  await p.goto(base+url,{waitUntil:'load'}); await p.waitForTimeout(600);
  await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));
  for (const sel of ['.hn-hero','.hn-filo','.hn-proc','.hn-trats','.hn-hosp','.hn-equipo','.hn-resenas','.hn-form']) { const el=await p.$(sel); if(!el) continue; await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(400); await el.screenshot({path:`${OUT}/${name}-${sel.slice(4)}.png`}); }
  console.log(name,'scrollW',await p.evaluate(()=>document.documentElement.scrollWidth));
  await ctx.close();
}
await browser.close(); srv.close();
