import { chromium } from 'playwright';
const [,, url, sel] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1366, height: 900 } });
await pg.route(/googletagmanager|trustindex/, (r) => r.abort());
await pg.goto(url, { waitUntil: 'load' });
await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } });
console.log(JSON.stringify(await pg.evaluate((sel) => { const i = document.querySelector(sel); let p = i, out = []; while (p && out.length < 8) { const cs = getComputedStyle(p); out.push([p.tagName, p.className.slice(0, 70), cs.display, cs.opacity, cs.visibility, cs.width, cs.height, cs.transform].join(' | ')); p = p.parentElement; } return { nat: i.naturalWidth, complete: i.complete, cur: i.currentSrc, out }; }, sel), null, 1));
await b.close();
