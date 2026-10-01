import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const DIST = path.resolve('dist'); const OUT = process.argv[2];
const MIME = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json','.ico':'image/x-icon'};
const srv = http.createServer((req,res)=>{ let p=decodeURIComponent(req.url.split('?')[0]); let f=path.join(DIST,p); if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); if(!fs.existsSync(f)){res.writeHead(404);return res.end('404');} res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r=>srv.listen(0,r)); const port=srv.address().port; const base=`http://localhost:${port}`;
const browser = await chromium.launch();
const errors=[];
async function shot(url, name, vp, opts={}){
  const ctx=await browser.newContext({viewport:vp,deviceScaleFactor:1}); const p=await ctx.newPage();
  p.on('pageerror',e=>errors.push(name+': '+e.message)); p.on('console',m=>{ if(m.type()==='error') errors.push(name+' console: '+m.text().slice(0,160)); });
  await p.goto(base+url,{waitUntil:'load',timeout:60000}); await p.waitForTimeout(800);
  // forzar visibles los elementos con aparición al scroll
  await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));
  await p.screenshot({path:`${OUT}/${name}-header.png`,clip:{x:0,y:0,width:vp.width,height:Math.min(160,vp.height)}});
  if(opts.full) await p.screenshot({path:`${OUT}/${name}-full.jpg`,fullPage:true,type:'jpeg',quality:45});
  for(const sel of (opts.sections||[])){ const el=await p.$(sel); if(!el) continue; await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(300); await el.screenshot({path:`${OUT}/${name}-${sel.replace(/[^a-z]/g,'')}.png`}); }
  // diagnóstico de cabecera: ancho de scroll, filas del menú, elementos que sobresalen
  const diag=await p.evaluate(()=>{ const hdr=document.querySelector('header'); const items=[...document.querySelectorAll('header .k-nav-menu--main > li')].map(li=>{const r=li.getBoundingClientRect();return {t:li.textContent.trim().slice(0,22),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}});
    const over=[...document.querySelectorAll('header *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1||r.left<-1}).slice(0,5).map(e=>e.className&&String(e.className).slice(0,60));
    return {scrollW:document.documentElement.scrollWidth, innerW:innerWidth, hdrH:hdr&&Math.round(hdr.getBoundingClientRect().height), items, over, ls:!!document.querySelector('.ls-widget')}; });
  console.log(name, JSON.stringify(diag));
  if(opts.hover){ const li=await p.$('header .k-nav-menu--main > li.menu-item-has-children'); if(li){ await li.hover(); await p.waitForTimeout(700); await p.screenshot({path:`${OUT}/${name}-menu.png`,clip:{x:0,y:0,width:vp.width,height:Math.min(640,vp.height)}}); const sub=await p.$('header .k-nav-menu--main > li.menu-item-has-children .sub-menu li.menu-item-has-children'); if(sub){ await sub.hover(); await p.waitForTimeout(600); await p.screenshot({path:`${OUT}/${name}-menu3.png`,clip:{x:0,y:0,width:vp.width,height:Math.min(700,vp.height)}}); } } }
  await ctx.close();
}
await shot('/', 'es1440', {width:1440,height:900}, {full:true, hover:true, sections:['.hn-filo','.hn-proc','.hn-trats','.hn-hosp','.hn-equipo','.hn-resenas','.hn-form','.hn-mapa']});
await shot('/', 'es1366', {width:1366,height:768}, {hover:false});
await shot('/', 'es1920', {width:1920,height:1080}, {});
await shot('/de/', 'de1440', {width:1440,height:900}, {hover:true});
await shot('/ru/', 'ru1440', {width:1440,height:900}, {});
await shot('/', 'es390', {width:390,height:844}, {full:true});
console.log('ERRORS', JSON.stringify(errors.slice(0,12)));
await browser.close(); srv.close();
