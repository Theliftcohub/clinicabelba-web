import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
await pg.goto('http://localhost:4321/home-nueva/', { waitUntil: 'networkidle', timeout: 60000 });
await pg.locator('#resenas').scrollIntoViewIfNeeded(); await pg.waitForTimeout(2500);
await pg.locator('#resenas').screenshot({ path: '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/hn-resenas.jpg', type: 'jpeg', quality: 60 });
// probar selector Hombre
await pg.locator('.hn-hero .hn-sel__btn[data-sel=hombre]').click(); await pg.waitForTimeout(400);
await pg.locator('#procedimientos').scrollIntoViewIfNeeded(); await pg.waitForTimeout(800);
await pg.locator('#procedimientos').screenshot({ path: '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/hn-hombre.jpg', type: 'jpeg', quality: 60 });
console.log(await pg.evaluate(() => (window.dataLayer||[]).filter(x=>x.event==='home_selector')));
await b.close();
