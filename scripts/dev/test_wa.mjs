// Prueba del botón «Continuar por WhatsApp» tras enviar (entorno preview: el envío es simulado). Uso: node scripts/dev/test_wa.mjs
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const DIST = path.resolve('dist');
const MIME = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2'};
const srv = http.createServer((req,res)=>{ let p=decodeURIComponent(req.url.split('?')[0]); let f=path.join(DIST,p); if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); if(!fs.existsSync(f)){res.writeHead(404);return res.end('404');} res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r=>srv.listen(0,r)); const base=`http://localhost:${srv.address().port}`;
const browser = await chromium.launch(); const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
await ctx.route('**/*', r => r.request().url().startsWith(base) ? r.continue() : r.abort());
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
const wa = async () => p.$$eval('.bf-wa', as => as.map(a => ({ txt: a.textContent, href: decodeURIComponent(a.href).slice(0, 400) })));
// 1) formulario corto de Elementor (nombre + teléfono) → cualificación → gracias + WhatsApp
await p.goto(base + '/de/armheben/'); await p.waitForTimeout(400);
const f1 = await p.$('form[data-form-id="el-5ff55c52"]');
await (await f1.$('#form-field-name')).fill('Prueba QA'); await (await f1.$('#form-field-tel')).fill('600000000'); // el primer input[type=text] es el honeypot «website»
await f1.$eval('[type=submit]', b => b.click()); await p.waitForTimeout(700);
const skip = await f1.$('.bf-skip'); if (skip) { await skip.click(); await p.waitForTimeout(300); }
console.log('1 corto DE:', JSON.stringify(await wa()));
// 2) formulario por pasos del hero (ES)
await p.goto(base + '/'); await p.waitForTimeout(400);
const f2 = await p.$('#form-hero');
async function next() { const s = (await f2.$$('[data-step]:not([hidden])'))[0]; const n = await s.$('.bf-next, .bf-submit'); await n.click(); await p.waitForTimeout(250); }
await (await f2.$('input[name=sel_persona][value=Mujer]')).check(); await p.waitForTimeout(400);
await (await f2.$('[data-step]:not([hidden]) input[type=text]')).fill('Prueba QA'); await next();
await (await f2.$('[data-step]:not([hidden]) input[type=radio]')).check(); await p.waitForTimeout(400);
await (await f2.$('[data-step]:not([hidden]) input[type=radio]')).check(); await p.waitForTimeout(400);
await (await f2.$('[data-step]:not([hidden]) input[type=email]')).fill('qa@example.com'); await next();
await (await f2.$('[data-step]:not([hidden]) input[type=tel]')).fill('600000000'); await next(); await p.waitForTimeout(500);
console.log('2 hero ES:', JSON.stringify(await wa()));
await p.screenshot({ path: 'migracion/screenshots/whatsapp-tras-formulario-hero.png', clip: { x: 780, y: 120, width: 560, height: 520 } });
// 3) formulario con redirección a página de gracias (Dr. Dewever) → tarjeta en la página de gracias
await p.goto(base + '/drdewevercirugiaplastica/'); await p.waitForTimeout(400);
const f3 = await p.$('form[data-form-id="tf-BdYhxQFV"]');
async function next3() { const s = (await f3.$$('[data-step]:not([hidden])'))[0]; const n = await s.$('.bf-next, .bf-submit'); await n.click(); await p.waitForTimeout(250); }
await (await f3.$('[data-step]:not([hidden]) input[type=radio]')).check(); await p.waitForTimeout(400);
await (await f3.$('[data-step]:not([hidden]) input[type=text]')).fill('Prueba QA'); await next3();
await (await f3.$('[data-step]:not([hidden]) input[type=radio]')).check(); await p.waitForTimeout(400);
await (await f3.$('[data-step]:not([hidden]) input[type=radio]')).check(); await p.waitForTimeout(400);
await (await f3.$('[data-step]:not([hidden]) input[type=email]')).fill('qa@example.com'); await next3();
await (await f3.$('[data-step]:not([hidden]) input[type=tel]')).fill('600000000'); await next3();
await p.waitForTimeout(1200); console.log('3 redirección → url:', p.url().replace(base, ''), '| tarjeta:', JSON.stringify(await p.$$eval('.wa-card .bf-wa', as => as.map(a => decodeURIComponent(a.href).slice(0, 400)))));
await p.screenshot({ path: 'migracion/screenshots/whatsapp-pagina-gracias.png' });
console.log('errores JS:', JSON.stringify(errs));
await browser.close(); srv.close();
