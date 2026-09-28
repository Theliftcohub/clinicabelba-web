import { chromium } from 'playwright';
const SC = '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/qa/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [base, who] of [['https://clinicabelba.com', 'wp'], ['http://localhost:4321', 'new']]) {
  const pg = await b.newPage({ viewport: { width: 1366, height: 900 } });
  await pg.route(/googletagmanager|trustindex|facebook|cookiebot|consent/, (r) => r.abort());
  await pg.goto(base + '/aumento-pecho-barcelona/', { waitUntil: 'load' });
  await pg.waitForTimeout(1000);
  const item = pg.locator('.k-nav-menu--main .menu-item-has-children > a, .elementor-nav-menu--main .menu-item-has-children > a').first();
  await item.hover(); await pg.waitForTimeout(900);
  await pg.screenshot({ path: SC + `menu_${who}.jpg`, type: 'jpeg', quality: 60 });
  const info = await pg.evaluate(() => {
    const sub = document.querySelector('.k-nav-menu--main .sub-menu, .elementor-nav-menu--main .sub-menu');
    if (!sub) return null; const r = sub.getBoundingClientRect(); const cs = getComputedStyle(sub);
    return { top: r.top, h: r.height, w: r.width, bottom: r.bottom, display: cs.display, overflow: cs.overflow, maxH: cs.maxHeight, items: sub.querySelectorAll('a').length, vh: innerHeight };
  });
  console.log(who, JSON.stringify(info));
  await pg.close();
}
await b.close();
