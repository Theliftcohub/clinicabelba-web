// Prueba de extremo a extremo de un formulario nativo: recorre los pasos, envía y comprueba el evento de medición.
// Uso: node scripts/test_form.mjs [base] [ruta]
import { chromium } from 'playwright';
const base = process.argv[2] || 'http://localhost:4321';
const ruta = process.argv[3] || '/test-paciente/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
await pg.route(/googletagmanager|trustindex|youtube|google\.com\/maps/, (r) => r.abort());
await pg.goto(base + ruta + '?utm_source=prueba&utm_medium=test', { waitUntil: 'load' });
const f = pg.locator('form.belba-form').first();
await f.scrollIntoViewIfNeeded();
for (let i = 0; i < 25; i++) {
  const step = f.locator('[data-step]:not([hidden])');
  const radios = step.locator('input[type=radio]');
  if (await radios.count()) {
    await radios.first().check({ force: true });
    await pg.waitForTimeout(350);
    const still = f.locator('[data-step]:not([hidden]) input[type=radio]');
    if ((await still.count()) && (await f.locator('[data-step]:not([hidden]) .bf-submit').count())) { await f.locator('[data-step]:not([hidden]) .bf-submit').click(); break; }
    continue;
  }
  const inputs = step.locator('input:not([type=hidden]):not([type=radio])');
  const n = await inputs.count();
  for (let k = 0; k < n; k++) {
    const t = await inputs.nth(k).getAttribute('type');
    await inputs.nth(k).fill(t === 'email' ? 'prueba@example.com' : t === 'tel' ? '600000000' : 'Prueba');
  }
  if (await step.locator('.bf-submit').count()) { await step.locator('.bf-submit').click(); break; }
  await step.locator('.bf-next').click();
  await pg.waitForTimeout(200);
}
await pg.waitForTimeout(800);
const r = await pg.evaluate(() => ({
  dl: (window.dataLayer || []).filter((x) => x.event === 'lead_form_submit'),
  gracias: !document.querySelector('form.belba-form .bf-thanks').hidden,
  url: location.pathname,
  atribucion: Object.fromEntries([...document.querySelectorAll('form.belba-form input[type=hidden]')].map((i) => [i.name, i.value]).filter((x) => x[1])),
}));
console.log(JSON.stringify(r, null, 1));
await pg.screenshot({ path: '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/form_done.jpg', type: 'jpeg', quality: 60 });
await b.close();
