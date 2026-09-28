import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
await pg.route(/googletagmanager|typeform|trustindex|youtube|google\.com\/maps/, r => r.abort());
await pg.goto('https://clinicabelba-web-preview.netlify.app/cirugia-corporal/', { waitUntil: 'load' });
const r = await pg.evaluate(() => {
  const c = document.querySelector('.k-element-f894759'); const im = c.querySelector('img'); const w = c.querySelector('.k-widget');
  const f = (e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return { w: r.width, h: r.height, disp: s.display, vis: s.visibility, op: s.opacity, pos: s.position, cls: e.className }; };
  return { col: f(c), widget: w && f(w), img: f(im), natural: im.naturalWidth, complete: im.complete, cur: im.currentSrc };
});
console.log(JSON.stringify(r, null, 1));
await b.close();
