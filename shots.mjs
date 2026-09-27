import { chromium } from 'playwright';
import fs from 'fs';
const pages = {
  home: 'https://clinicabelba.com/',
  servicio: 'https://clinicabelba.com/aumento-pecho-barcelona/',
  precio: 'https://clinicabelba.com/aumento-pecho-precio/',
  categoria: 'https://clinicabelba.com/cirugia-corporal/',
  post: 'https://clinicabelba.com/asimetria-mamaria-cuando-operar/',
  blog: 'https://clinicabelba.com/blog/',
  contacto: 'https://clinicabelba.com/contacto/',
  equipo: 'https://clinicabelba.com/cirujanos-plasticos-barcelona/',
  en_servicio: 'https://clinicabelba.com/en/',
};
fs.mkdirSync('migracion/screenshots', { recursive: true });
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' in {} ? undefined : undefined });
const tokens = {};
for (const [name, url] of Object.entries(pages)) {
  for (const [dev, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    try {
      await p.goto(url, { waitUntil: 'load', timeout: 60000 });
      await p.evaluate(() => document.querySelectorAll('#CybotCookiebotDialog,#CybotCookiebotDialogBodyUnderlay').forEach(e => e.remove()));
      await p.screenshot({ path: `migracion/screenshots/${name}-${dev}.png`, fullPage: dev === 'desktop' ? false : false });
      await p.screenshot({ path: `migracion/screenshots/${name}-${dev}-full.jpg`, fullPage: true, type: 'jpeg', quality: 50 });
      if (dev === 'desktop') {
        tokens[name] = await p.evaluate(() => {
          const cs = getComputedStyle(document.documentElement);
          const vars = {};
          for (const s of document.styleSheets) { try { for (const r of s.cssRules) { if (r.selectorText && /elementor-kit|:root/.test(r.selectorText)) { for (const k of r.style) if (k.startsWith('--e-global')) vars[k] = r.style.getPropertyValue(k).trim(); } } } catch (e) {} }
          const pick = sel => { const e = document.querySelector(sel); if (!e) return null; const s = getComputedStyle(e); return { font: s.fontFamily, size: s.fontSize, weight: s.fontWeight, color: s.color, bg: s.backgroundColor }; };
          return { vars, body: pick('body'), h1: pick('h1'), h2: pick('h2'), a: pick('a'), button: pick('.elementor-button') };
        });
      }
    } catch (e) { console.log('ERR', name, dev, e.message); }
    await ctx.close();
  }
  console.log('ok', name);
}
fs.writeFileSync('migracion/design_tokens_raw.json', JSON.stringify(tokens, null, 1));
await browser.close();
