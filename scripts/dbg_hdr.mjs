import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const m = await b.newPage({ viewport: { width: 390, height: 844 } });
await m.goto('http://localhost:4321/en/breast-surgery/', { waitUntil: 'load' });
await m.locator('.k-menu-toggle').first().click(); await m.waitForTimeout(300);
console.log(JSON.stringify(await m.evaluate(() => {
  const r = (el) => { const q = el.getBoundingClientRect(); return [Math.round(q.top), Math.round(q.bottom), Math.round(q.height)]; };
  const h = document.querySelector('header.k-38'), s = h.querySelector('.k-section'), dd = h.querySelector('.k-nav-menu--dropdown'), w = h.querySelector('.k-widget-nav-menu');
  return { header: r(h), section: r(s), widget: r(w), dropdown: r(dd), ddTop: getComputedStyle(dd).top, ddPos: getComputedStyle(dd).position, ddMargin: getComputedStyle(dd).marginTop, hPos: getComputedStyle(h).position, secPad: getComputedStyle(s).padding, hMB: getComputedStyle(h).marginBottom, sMB: getComputedStyle(s).marginBottom };
})));
await b.close();
