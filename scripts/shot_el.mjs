import { chromium } from 'playwright';
const [,, url, sel, out, w = '1366'] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: +w, height: 900 } });
await pg.route(/googletagmanager|trustindex|facebook|cookiebot/, (r) => r.abort());
await pg.goto(url, { waitUntil: 'load' });
const el = pg.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(1200);
await el.screenshot({ path: out, type: 'jpeg', quality: 55 });
await b.close();
