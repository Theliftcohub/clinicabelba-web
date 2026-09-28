import { chromium } from 'playwright';
const pages = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const p of pages) {
  for (const [dev, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
    const ctx = await b.newContext({ viewport: vp });
    const pg = await ctx.newPage();
    const errs = [];
    pg.on('response', r => { if (r.status() >= 400 && r.url().includes('localhost')) errs.push(r.status() + ' ' + r.url()); });
    await pg.route(/googletagmanager|typeform|trustindex|youtube|google\.com\/maps|maps\.google/, r => r.abort());
    await pg.goto('http://localhost:4321' + p, { waitUntil: 'load', timeout: 60000 });
    await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
    await pg.waitForTimeout(600);
    const name = (p.replace(/\//g, '_') || 'home');
    await pg.screenshot({ path: `/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/new${name}-${dev}.jpg`, fullPage: false, type: 'jpeg', quality: 60 });
    await pg.screenshot({ path: `/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/new${name}-${dev}-full.jpg`, fullPage: true, type: 'jpeg', quality: 40 });
    if (errs.length) console.log(p, dev, errs.slice(0, 10));
    await ctx.close();
  }
}
await b.close();
