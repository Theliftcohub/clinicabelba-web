// Prueba del formulario de Elementor por pasos: recorre, envía y comprueba eventos.
import { chromium } from 'playwright';
const base = process.argv[2] || 'http://localhost:4321';
const ruta = process.argv[3] || '/abdominoplastia-antes-y-despues/';
const w = +(process.argv[4] || 390);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: w, height: 900 } });
await pg.route(/googletagmanager|trustindex|youtube|google\.com\/maps/, (r) => r.abort());
await pg.goto(base + ruta + '?utm_source=google&utm_medium=cpc', { waitUntil: 'load' });
const f = pg.locator('form.k-form.is-steps:visible').first();
console.log('formularios por pasos:', await pg.locator('form.k-form.is-steps').count());
await f.scrollIntoViewIfNeeded();
const SC = 'migracion/screenshots/qa/';
for (let i = 0; i < 8; i++) {
  const st = f.locator('.k-step:not([hidden])');
  if (i < 2) await st.screenshot({ path: SC + `kstep${i}_${w}.jpg`, type: 'jpeg', quality: 60 });
  for (const el of await st.locator('input:not([type=hidden]):not([type=checkbox]), textarea').all()) {
    const t = await el.getAttribute('type');
    await el.fill(t === 'email' ? 'prueba@example.com' : t === 'tel' ? '600000000' : 'Prueba');
  }
  for (const c of await st.locator('input[type=checkbox]').all()) await c.check({ force: true });
  if (await st.locator('[type=submit]').count()) { await st.locator('[type=submit]').click(); break; }
  await st.locator('.bf-next').click(); await pg.waitForTimeout(150);
}
await pg.waitForTimeout(700);
console.log(JSON.stringify(await pg.evaluate(() => (window.dataLayer || []).filter((x) => /lead_form/.test(x.event)))));
await f.screenshot({ path: SC + `kstep_done_${w}.jpg`, type: 'jpeg', quality: 60 });
await b.close();
