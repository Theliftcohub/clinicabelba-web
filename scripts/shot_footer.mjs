import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [w,h,name] of [[1366,900,'desk'],[390,844,'mob']]) {
  const pg = await b.newPage({ viewport: { width: w, height: h } });
  await pg.route(/googletagmanager|trustindex|youtube|google\.com\/maps/, r => r.abort());
  await pg.goto('https://clinicabelba-web-preview.netlify.app/home-nueva/', { waitUntil: 'load' });
  await pg.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await pg.waitForTimeout(600);
  const info = await pg.evaluate(() => {
    const f = document.querySelector('footer, .kt-footer, [data-kt=footer]');
    const imgs = [...(f||document).querySelectorAll('img')].map(i => ({src:i.getAttribute('src'), w:i.clientWidth, h:i.clientHeight, ok:i.complete && i.naturalWidth>0, nat:i.naturalWidth}));
    return { fh: f ? f.getBoundingClientRect().height : null, imgs };
  });
  console.log(name, JSON.stringify(info, null, 1));
  const f = pg.locator('footer, .kt-footer, [data-kt=footer]').first();
  await f.screenshot({ path: `/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad/footer_prev_${name}.jpg`, type: 'jpeg', quality: 60 });
  await pg.close();
}
await b.close();
