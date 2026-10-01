// Capturas de una página de dist/ a un ancho dado, troceadas en bloques de 1200 px de alto (para revisar móvil sin un
// fullPage ilegible). Uso: node scripts/dev/shot_page.mjs /ruta/ 390 carpeta_salida [/otra-ruta/ ...]
// Recorre la página antes de capturar para que carguen las imágenes lazy. Si la ruta es una URL absoluta (https://…) captura esa web (p. ej. el WordPress en vivo, como referencia).
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const [W, OUT, ...PATHS] = [Number(process.argv[3] || 390), process.argv[4] || 'shots', process.argv[2], ...process.argv.slice(5)];
const DIST = path.resolve('dist');
const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.pdf': 'application/pdf' };
const srv = http.createServer((req, res) => { let p = decodeURIComponent(req.url.split('?')[0]); let f = path.join(DIST, p); if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html'); if (!fs.existsSync(f)) { res.writeHead(404); return res.end('404'); } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); });
await new Promise(r => srv.listen(0, r)); const base = `http://localhost:${srv.address().port}`;
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch(); const ctx = await browser.newContext({ viewport: { width: W, height: 844 }, deviceScaleFactor: 1, isMobile: W < 700, hasTouch: W < 700 });
const externo = PATHS.some(x => /^https?:/.test(x));
if (!externo) await ctx.route('**/*', r => r.request().url().startsWith(base) ? r.continue() : r.abort());
const p = await ctx.newPage();
for (const P of PATHS) {
  await p.goto(/^https?:/.test(P) ? P : base + P, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {}); await p.waitForTimeout(800);
  const H = await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 300)); return document.body.scrollHeight; });
  const slug = P.replace(/[^a-z0-9]+/gi, '_').replace(/^_|_$/g, '') || 'home';
  const n = Math.ceil(H / 1200);
  for (let i = 0; i < n; i++) await p.screenshot({ path: path.join(OUT, `${slug}-${String(i + 1).padStart(2, '0')}.png`), fullPage: true, clip: { x: 0, y: i * 1200, width: W, height: Math.min(1200, H - i * 1200) } });
  console.log(`${P}: ${H}px → ${n} capturas (${slug}-NN.png)`);
}
await browser.close(); srv.close();
