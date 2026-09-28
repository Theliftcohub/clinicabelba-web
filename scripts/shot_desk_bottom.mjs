import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1366, height: 900 } });
await pg.route(/googletagmanager|trustindex/, r => r.abort());
await pg.goto('http://localhost:4321/home-nueva/', { waitUntil: 'load' });
await pg.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await pg.waitForTimeout(1500);
const H = await pg.evaluate(() => document.body.scrollHeight);
await pg.screenshot({ path: '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/bottom_desk.jpg', type: 'jpeg', quality: 60, fullPage: true, clip: { x: 0, y: H - 1100, width: 1366, height: 1100 } });
console.log('docH', H); await b.close();
