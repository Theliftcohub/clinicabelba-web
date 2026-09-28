import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
await pg.goto('file:///root/.claude/uploads/aae1ead6-8dc9-546f-ae1d-382cc271829d/31c61ad0-Figma_Make_App.mhtml', { waitUntil: 'load', timeout: 60000 }).catch(e => console.log('goto', e.message));
await pg.waitForTimeout(1500);
await pg.screenshot({ path: '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/figma/home-full.jpg', fullPage: true, type: 'jpeg', quality: 55 });
console.log(await pg.evaluate(() => document.body.innerText.slice(0, 3000)));
await b.close();
