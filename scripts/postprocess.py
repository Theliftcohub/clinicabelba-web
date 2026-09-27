#!/usr/bin/env python3
"""Tras convert.py + fetch_media.py:
 - quita del HTML/CSS las imágenes que ya daban 404 en el WordPress (se anotan en NO_LITERAL.md);
 - comprueba que todos los recursos locales existen en public/;
 - lista enlaces internos a rutas que no existen en la web nueva ni en el contrato."""
import json, glob, os, re, csv
from urllib.parse import unquote
B = '/home/claude/belba'
fail = {f[0] for f in json.load(open(B + '/migracion/media_fail.json'))}
need = json.load(open(B + '/migracion/media_needed.json'))
failed_local = {need[u] for u in fail if u in need}
contract = {unquote(r['url']).lower(): r for r in csv.DictReader(open(B + '/migracion/urls.csv'))}
docs = {}
for f in glob.glob(B + '/src/content/pages/*/*.json'):
    docs[f] = json.load(open(f))
built = {unquote(d['path']).lower() for d in docs.values()}
extra_ok = {'/', '/sitemap.xml', '/robots.txt', '/llms.txt', '/form-handler.php'}
no_literal = []
missing_res = {}
broken_links = {}
for f, d in docs.items():
    changed = False
    for b in d['blocks']:
        h = b['html']
        for loc in failed_local:
            if loc in h:
                h2 = re.sub(r'<img[^>]*src="%s"[^>]*/?>' % re.escape(loc), '', h)
                h2 = h2.replace('url("%s")' % loc, 'none')
                if h2 != h:
                    no_literal.append((d['path'], 'imagen', loc, '(retirada)', 'La imagen ya daba 404 en el WordPress'))
                    h = h2; changed = True
        b['html'] = h
    for loc in failed_local:
        if loc in d['css']:
            d['css'] = d['css'].replace('url("%s")' % loc, 'none'); changed = True
    if d['seo'].get('ogImage') in failed_local:
        d['seo']['ogImage'] = None; changed = True
    if changed:
        json.dump(d, open(f, 'w'), ensure_ascii=False)
    allh = ''.join(b['html'] for b in d['blocks']) + d['css']
    for m in re.findall(r'(?:src|href)="(/images/[^"]+)"|url\("(/images/[^"]+)"\)|(/images/[^\s",]+-800\.webp)', allh):
        p = next(x for x in m if x)
        if not os.path.exists(B + '/public' + unquote(p)):
            missing_res.setdefault(p, []).append(d['path'])
    for href in re.findall(r'<a[^>]*href="(/[^"#?]*)', allh):
        k = unquote(href).lower()
        if k.startswith('/images/') or k in extra_ok: continue
        if k not in built:
            r = contract.get(k)
            broken_links.setdefault(href, set()).add(d['path'])
for lg in glob.glob(B + '/src/content/layout/*.json'):
    l = json.load(open(lg))
    for part in ('header', 'footer'):
        for href in re.findall(r'<a[^>]*href="(/[^"#?]*)', l[part]):
            k = unquote(href).lower()
            if k.startswith('/images/') or k in extra_ok: continue
            if k not in built:
                broken_links.setdefault(href, set()).add('layout:' + os.path.basename(lg) + ':' + part)
# NO_LITERAL.md
nl = B + '/NO_LITERAL.md'
if not os.path.exists(nl):
    open(nl, 'w').write('# Cambios no literales respecto al WordPress\n\n| URL | Campo | Original | Nuevo | Motivo |\n|---|---|---|---|---|\n')
cur = open(nl).read()
with open(nl, 'a') as fo:
    for row in no_literal:
        line = '| %s |\n' % ' | '.join(row)
        if line not in cur:
            fo.write(line)
json.dump({'missing': missing_res, 'broken': {k: sorted(v)[:5] for k, v in broken_links.items()}}, open(B + '/migracion/postprocess.json', 'w'), ensure_ascii=False, indent=1)
print('imagenes retiradas', len(no_literal), '| recursos locales que faltan', len(missing_res), '| enlaces internos rotos', len(broken_links))
for k, v in list(broken_links.items())[:40]:
    print('  ', unquote(k), '<-', sorted(v)[:3])
for k, v in list(missing_res.items())[:10]:
    print(' falta', k, v[:2])
