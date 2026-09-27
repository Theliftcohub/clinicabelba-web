#!/usr/bin/env python3
"""Reescribe los enlaces internos que en el WordPress pasaban por una redirección (o daban 404 por
una errata) para que apunten directamente al destino final, y añade esas URLs al contrato como 301."""
import json, glob, csv, re, subprocess, os
from urllib.parse import unquote, quote
B = '/home/claude/belba'
res = json.load(open(B + '/migracion/broken_resolved.json'))
i18n = json.load(open(B + '/migracion/i18n-map.json'))
grp = {}
for g, m in i18n.items():
    for l, p in m.items():
        grp[unquote(p).lower()] = m
docs = {f: json.load(open(f)) for f in glob.glob(B + '/src/content/pages/*/*.json')}
built = {unquote(d['path']).lower(): d['path'] for d in docs.values()}
C = list(csv.DictReader(open(B + '/migracion/urls.csv'))); F = list(C[0].keys())
cidx = {unquote(r['url']).lower(): r for r in C}
def lang_of(p):
    m = re.match(r'^/(ca|en|fr|de|it|nl|ru|uk)/', p)
    return m.group(1) if m else 'es'
def final_of_es(e):
    r = cidx.get(e); seen = 0
    while r and r['decision'] == '301' and seen < 6:
        e = unquote(r['destino']).lower(); r = cidx.get(e); seen += 1
    return e
def translate(es_path, lang):
    m = grp.get(es_path)
    if m and m.get(lang) and unquote(m[lang]).lower() in built:
        return built[unquote(m[lang]).lower()]
    return built.get(es_path)
mapping = {}; notes = {}
for h, v in res.items():
    k = unquote(h).lower(); lg = lang_of(k)
    fin = unquote(v['final'].split('?')[0]).lower()
    if v['status'] == 200 and fin in built:
        mapping[k] = built[fin]; notes[k] = f'enlace interno que en WordPress redirigía ({v["saltos"]} saltos)'; continue
    if 'precio cirugía plástica-barcelona' in k:
        t = translate('/precio-cirugia-estetica-barcelona/', lg)
        if t: mapping[k] = t; notes[k] = 'ERRATA: enlace roto (404) en el pie del WordPress; se apunta a la página de precios'
        continue
    if k == '/page-sitemap.xml':
        mapping[k] = '/sitemap.xml'; notes[k] = 'sitemap de Yoast'; continue
    # página huérfana (200) o 500: buscar su equivalente ES por hreflang en vivo
    u = 'https://clinicabelba.com' + quote(unquote(h), safe='/%')
    html = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '40', u], capture_output=True, text=True).stdout
    m = re.search(r'<link[^>]+hreflang="es(?:-ES)?"[^>]+href="https://clinicabelba\.com([^"]+)"', html) or re.search(r'<link[^>]+href="https://clinicabelba\.com([^"]+)"[^>]+hreflang="es(?:-ES)?"', html)
    es = unquote(m.group(1)).lower() if m else None
    if not es and lg != 'es':
        es = '/' + k.split('/', 2)[2]
    t = translate(final_of_es(es), lg) if es else None
    if t:
        mapping[k] = t; notes[k] = f'traducción huérfana de {es} en TranslatePress; 301 a la traducción del destino'
    else:
        print('SIN DESTINO', k, v, es)
json.dump(mapping, open(B + '/migracion/link_map.json', 'w'), ensure_ascii=False, indent=0)
# aplicar a páginas y cabeceras/pies
def rep(html):
    def f(mm):
        href = mm.group(1); key = unquote(href.split('#')[0].split('?')[0]).lower()
        if key in mapping:
            tail = href[len(href.split('#')[0].split('?')[0]):]
            return 'href="%s%s"' % (mapping[key], tail)
        return mm.group(0)
    return re.sub(r'href="(/[^"]*)"', f, html)
n = 0
for fn, d in docs.items():
    ch = False
    for b in d['blocks']:
        nh = rep(b['html'])
        if nh != b['html']: b['html'] = nh; ch = True
    if ch: json.dump(d, open(fn, 'w'), ensure_ascii=False); n += 1
for fn in glob.glob(B + '/src/content/layout/*.json'):
    l = json.load(open(fn)); l['header'] = rep(l['header']); l['footer'] = rep(l['footer']); json.dump(l, open(fn, 'w'), ensure_ascii=False)
# contrato
added = 0
for k, t in mapping.items():
    if 'precio cirugía plástica' in k or k in cidx: continue
    row = dict.fromkeys(F, ''); row.update(url=quote(k, safe='/%'), decision='301', destino=t, estado_esperado='301', tipo='enlace-interno', backlinks='0', trafico='0', notas='28/09: ' + notes[k])
    C.append(row); added += 1
w = csv.DictWriter(open(B + '/migracion/urls.csv', 'w', newline=''), fieldnames=F); w.writeheader(); w.writerows(C)
nl = B + '/NO_LITERAL.md'
with open(nl, 'a') as fo:
    for k, t in mapping.items():
        if 'ERRATA' in notes[k]:
            fo.write(f'| (pie, idioma {lang_of(k)}) | enlace | {k} | {unquote(t)} | Enlace roto (404) en el WordPress: errata en la URL del pie |\n')
print('mapeados', len(mapping), 'páginas tocadas', n, 'filas añadidas al contrato', added)
