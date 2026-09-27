import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const url of ['https://clinicabelba.com/', 'http://localhost:4321/']) {
  const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await pg.goto(url, { waitUntil: 'load', timeout: 90000 });
  await pg.evaluate(() => document.querySelectorAll('#CybotCookiebotDialog,#CybotCookiebotDialogBodyUnderlay,.trp-ald-popup,#trp_ald_modal_container').forEach(e => e.remove()));
  const r = await pg.evaluate(() => {
    const sec = document.querySelector('.elementor-element-ce67a94, .k-element-ce67a94');
    const hdr = document.querySelector('[data-elementor-type="header"], [data-kt="header"]');
    const img = sec.querySelector('img');
    const cs = getComputedStyle(sec);
    return { hdrTop: hdr.getBoundingClientRect().top, secTop: sec.getBoundingClientRect().top, secH: sec.getBoundingClientRect().height, imgTop: img.getBoundingClientRect().top, mt: cs.marginTop, pt: cs.paddingTop, pos: cs.position, bodyPad: getComputedStyle(document.body).paddingTop, htmlMt: getComputedStyle(document.documentElement).marginTop, hdrPt: getComputedStyle(hdr).paddingTop };
  });
  console.log(url, JSON.stringify(r));
  await pg.close();
}
await b.close();
