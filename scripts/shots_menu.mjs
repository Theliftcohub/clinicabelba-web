import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const DIST = path.resolve('dist'); const OUT = process.argv[2];
const MIME = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json','.ico':'image/x-icon'};
const srv = http.createServer((req,res)=>{ let p=decodeURIComponent(req.url.split('?')[0]); let f=path.join(DIST,p); if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); if(!fs.existsSync(f)){res.writeHead(404);return res.end('404');} res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r=>srv.listen(0,r)); const base=`http://localhost:${srv.address().port}`;
const browser = await chromium.launch(); const errors=[];
const LI='header .k-nav-menu--main > ul.k-nav-menu > li';
for (const [name,url,vp] of [['es',  '/', {width:1440,height:900}], ['de','/de/',{width:1440,height:900}]]) {
  const ctx=await browser.newContext({viewport:vp}); const p=await ctx.newPage(); p.on('pageerror',e=>errors.push(name+': '+e.message));
  await p.goto(base+url,{waitUntil:'load'}); await p.waitForTimeout(600);
  await p.screenshot({path:`${OUT}/${name}-top.png`});
  const items=await p.$$(LI); console.log(name,'items',items.length, JSON.stringify(await p.$$eval(LI,ls=>ls.map(l=>{const r=l.getBoundingClientRect();return [l.textContent.trim().split('\n')[0].slice(0,18),Math.round(r.y),Math.round(r.height)]}))));
  // 1er nivel: "Cirugía Plástica" (2º li con hijos)
  const withKids=await p.$$(LI+'.menu-item-has-children'); const l1=withKids[1]||withKids[0];
  await l1.hover(); await p.waitForTimeout(700); await p.screenshot({path:`${OUT}/${name}-menu1.png`,clip:{x:0,y:0,width:1440,height:700}});
  const l2=await l1.$('ul.sub-menu > li.menu-item-has-children'); if(l2){ await l2.hover(); await p.waitForTimeout(600); await p.screenshot({path:`${OUT}/${name}-menu2.png`,clip:{x:0,y:0,width:1440,height:760}});
    const l3=await l2.$('ul.sub-menu > li.menu-item-has-children'); if(l3){ await l3.hover(); await p.waitForTimeout(600); await p.screenshot({path:`${OUT}/${name}-menu3.png`,clip:{x:0,y:0,width:1440,height:860}}); } }
  // selector de idioma abierto
  const ls=await p.$('.ls__cur'); if(ls){ await p.mouse.move(5,5); await p.waitForTimeout(400); try{await ls.click({timeout:3000});}catch(e){console.log('lang click:',e.message.split('
')[0]);} await p.waitForTimeout(400); await p.screenshot({path:`${OUT}/${name}-lang.png`,clip:{x:900,y:0,width:540,height:420}}); }
  await ctx.close();
}
{ const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}); const p=await ctx.newPage(); p.on('pageerror',e=>errors.push('mob: '+e.message));
  await p.goto(base+'/',{waitUntil:'load'}); await p.waitForTimeout(600);
  await p.screenshot({path:`${OUT}/mob-top.png`});
  const tg=await p.$('header .k-menu-toggle, header [class*=menu-toggle], header button'); console.log('toggle', !!tg, tg && await tg.evaluate(e=>e.className));
  if(tg){ try{await tg.click({timeout:3000});}catch(e){console.log('toggle click:',e.message.split('
')[0]);} await p.waitForTimeout(700); await p.screenshot({path:`${OUT}/mob-menu.png`}); const sub=await p.$('header .k-nav-menu--dropdown > li.menu-item-has-children > a'); if(sub){ try{await sub.click({timeout:3000});}catch(e){console.log('sub click:',e.message.split('
')[0]);} await p.waitForTimeout(500); await p.screenshot({path:`${OUT}/mob-menu2.png`}); } }
  await ctx.close(); }
console.log('ERRORS', JSON.stringify(errors)); await browser.close(); srv.close();
