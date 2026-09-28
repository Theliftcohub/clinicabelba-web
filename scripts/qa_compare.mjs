// QA visual: la misma página en WordPress (en vivo) y en la web nueva (local), escritorio y móvil.
import { chromium } from 'playwright';
const PAGES = process.argv.slice(2).length ? process.argv.slice(2) : ['/', '/aumento-pecho-barcelona/', '/blog/', '/rinoplastia-hombre-antes-y-despues-mejorado/', '/contacto/', '/en/', '/cirujanos-plasticos-barcelona/', '/precio-cirugia-estetica-barcelona/'];
const SC = '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/qa/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const out = [];
for (const [vw, vh, tag] of [[1366, 900, 'd'], [390, 844, 'm']]) {
  for (const p of PAGES) {
    for (const [base, who] of [['https://clinicabelba.com', 'wp'], ['http://localhost:4321', 'new']]) {
      if (who === 'wp' && (await import('fs')).existsSync(SC + `${tag}_${p.replace(/\W+/g, '_') || 'home'}_wp.jpg`)) continue;
      const ctx = await b.newContext({ viewport: { width: vw, height: vh } });
      const pg = await ctx.newPage();
      await pg.route(/googletagmanager|google-analytics|facebook|cookiebot|consent|hotjar|clarity|doubleclick/, (r) => r.abort());
      try {
        await pg.goto(base + p, { waitUntil: 'load', timeout: 45000 });
        await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
        await pg.waitForTimeout(800);
        const h = await pg.evaluate(() => document.documentElement.scrollHeight);
        const name = `${tag}_${p.replace(/\W+/g, '_') || 'home'}_${who}.jpg`;
        await pg.screenshot({ path: SC + name, fullPage: true, type: 'jpeg', quality: 45 });
        out.push({ tag, p, who, h, name });
      } catch (e) { out.push({ tag, p, who, err: String(e).slice(0, 120) }); }
      await ctx.close();
    }
  }
}
console.log(JSON.stringify(out));
await b.close();
