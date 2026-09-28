import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1366, height: 900 } });
await pg.route(/googletagmanager|trustindex|youtube|google\.com\/maps/, (r) => r.abort());
await pg.goto('http://localhost:4321/consulta-online/', { waitUntil: 'load' });
console.log(JSON.stringify(await pg.evaluate(() => [...document.querySelectorAll('form')].map(f => {
  let p = f, chain = []; while (p && chain.length < 12) { const cs = getComputedStyle(p); if (cs.display === 'none' || cs.visibility === 'hidden') chain.push(p.tagName + '.' + p.className.slice(0, 80) + ' [' + cs.display + ']'); p = p.parentElement; }
  return { cls: f.className, name: f.getAttribute('data-form-name'), h: f.getBoundingClientRect().height, hiddenBy: chain };
})), null, 1));
await b.close();
