import { chromium } from 'playwright';
const url = process.argv[2] || 'http://localhost:4321/home-nueva/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
await pg.route(/googletagmanager|trustindex/, r => r.abort());
await pg.goto(url, { waitUntil: 'load' });
await pg.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await pg.waitForTimeout(2500);
const info = await pg.evaluate(() => {
  const i = document.querySelector('img[src*="financiado"]');
  const r = i.getBoundingClientRect();
  const sec = i.closest('section, .k-section, [data-element_type="container"]');
  return { nat: i.naturalWidth, ok: i.complete, top: r.top + scrollY, h: r.height, w: r.width, docH: document.body.scrollHeight, secH: sec ? sec.getBoundingClientRect().height : null, parents: (() => { let p = i, a = []; while (p && a.length < 6) { a.push(p.tagName + '.' + [...p.classList].slice(0, 3).join('.')); p = p.parentElement; } return a; })() };
});
console.log(JSON.stringify(info));
const H = info.docH;
await pg.screenshot({ path: '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/bottom_mob.jpg', type: 'jpeg', quality: 60, fullPage: true, clip: { x: 0, y: H - 1400, width: 390, height: 1400 } });
await b.close();
