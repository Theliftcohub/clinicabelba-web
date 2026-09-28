import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 390, height: 900 } });
await pg.route(/googletagmanager|trustindex|youtube|google\.com\/maps/, (r) => r.abort());
await pg.goto('http://localhost:4321/abdominoplastia-barcelona/', { waitUntil: 'load' });
const f = pg.locator('form.k-form:not(.is-steps):visible').first();
await f.locator('input[type=text]:visible').first().fill('Prueba');
await f.locator('input[type=tel]:visible').first().fill('600000000');
await f.locator('[type=submit]').click(); await pg.waitForTimeout(500);
console.log(JSON.stringify(await f.evaluate((f) => {
  const w = f.querySelector('.k-form-fields-wrapper'); const bx = f.querySelector('.bf-follow'); const c = bx.querySelector('.bf-choice');
  return { forms: document.querySelectorAll('form.k-form').length, wHidden: w.hidden, wDisp: getComputedStyle(w).display, fw: f.getBoundingClientRect().width, bw: bx.getBoundingClientRect().width, cw: c.getBoundingClientRect().width, cDisp: getComputedStyle(c).display, bpad: getComputedStyle(bx).padding, cmin: getComputedStyle(c).minWidth, ws: getComputedStyle(c).whiteSpace };
})));
await b.close();
