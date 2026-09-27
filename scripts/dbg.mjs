import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
await pg.route(/googletagmanager|typeform|trustindex|youtube|google\.com\/maps/, r => r.abort());
await pg.goto('http://localhost:4321/', { waitUntil: 'load' });
const r = await pg.evaluate(() => {
  const q = (s) => { const e = document.querySelector(s); if (!e) return null; const c = getComputedStyle(e); return { s, cls: e.className, font: c.fontFamily, w: c.fontWeight, color: c.color, size: c.fontSize }; };
  return [q('.k-widget-text-editor'), q('.k-widget-text-editor p'), q('.k-nav-menu a'), q('h1'), q('body')];
});
console.log(JSON.stringify(r, null, 1));
await b.close();
