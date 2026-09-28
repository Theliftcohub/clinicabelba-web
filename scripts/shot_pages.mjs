import { chromium } from 'playwright';
const SC = '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/qa/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [p, name, w] of [['/', 'home_es', 1366], ['/en/', 'home_en', 390], ['/aumento-pecho-barcelona/', 'landing', 1366], ['/blog/', 'blog', 1366], ['/precio-cirugia-estetica-barcelona/', 'precio', 390]]) {
  const pg = await b.newPage({ viewport: { width: w, height: 900 } });
  await pg.route(/googletagmanager|trustindex|facebook|cookiebot/, (r) => r.abort());
  await pg.goto('http://localhost:4321' + p, { waitUntil: 'load' });
  await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
  await pg.waitForTimeout(2500);
  await pg.screenshot({ path: SC + name + '.jpg', fullPage: true, type: 'jpeg', quality: 45 });
  await pg.close();
}
await b.close();
