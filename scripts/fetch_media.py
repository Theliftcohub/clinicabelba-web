#!/usr/bin/env python3
"""Descarga los medios usados (original de WordPress) y los deja en public/ con el nombre original.
Imágenes raster -> WebP (máx. 1600 px) + variante -800. SVG, GIF, PDF, vídeo: tal cual.
Registra el mapeo en migracion/media_map.json (url original -> ruta nueva) para las redirecciones."""
import json, os, sys, io, subprocess, concurrent.futures as cf
from urllib.parse import quote
from PIL import Image, ImageOps

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raíz del repo (o BELBA_ROOT)
CACHE = B + '/migracion/media_orig'
os.makedirs(CACHE, exist_ok=True)
need = json.load(open(B + '/migracion/media_needed.json'))
seen = json.load(open(B + '/migracion/media_seen.json')) if os.path.exists(B + '/migracion/media_seen.json') else {}
extra = sys.argv[1:]

def dl(url):
    fn = os.path.join(CACHE, url.split('/wp-content/uploads/', 1)[1].replace('/', '__'))
    if os.path.exists(fn) and os.path.getsize(fn) > 0:
        return fn, 200
    u = quote(url, safe=':/%?=&')
    r = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '60', '-o', fn, '-w', '%{http_code}', u], capture_output=True, text=True)
    code = int(r.stdout or 0)
    if code != 200 and os.path.exists(fn):
        os.remove(fn)
    return fn, code

def process(item):
    url, new = item
    fn, code = dl(url)
    if code != 200:
        # probar con la variante "-scaled" (WordPress >= 5.3 guarda así los originales grandes)
        root, ext = os.path.splitext(url)
        fn2, code2 = dl(root + '-scaled' + ext)
        if code2 == 200:
            fn, code = fn2, 200
        else:
            ok = False
            def area(v):
                m = __import__('re').search(r'-(\d+)x(\d+)\.\w+$', v)
                return int(m.group(1)) * int(m.group(2)) if m else 0
            for v in sorted(seen.get(url, []), key=area, reverse=True):
                if v == url: continue
                fn3, code3 = dl(v.rstrip('/'))
                if code3 == 200:
                    fn, code, ok = fn3, 200, True; break
            if not ok:
                return url, new, f'HTTP {code}'
    out = B + '/public' + new
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if new.endswith('.webp'):
        if os.path.exists(out) and os.path.exists(out[:-5] + '-800.webp'):
            return url, new, 'ok'
        try:
            im = Image.open(fn)
            im = ImageOps.exif_transpose(im)
            if im.mode in ('P', 'LA', 'RGBA') or 'transparency' in im.info:
                im = im.convert('RGBA')
            elif im.mode != 'RGB':
                im = im.convert('RGB')
            w, h = im.size
            big = im if w <= 1600 else im.resize((1600, round(h * 1600 / w)), Image.LANCZOS)
            big.save(out, 'WEBP', quality=80, method=5)
            sm = im if w <= 800 else im.resize((800, round(h * 800 / w)), Image.LANCZOS)
            sm.save(out[:-5] + '-800.webp', 'WEBP', quality=78, method=5)
        except Exception as e:
            return url, new, 'ERR ' + str(e)[:80]
    else:
        if not os.path.exists(out):
            with open(fn, 'rb') as a, open(out, 'wb') as b:
                b.write(a.read())
    return url, new, 'ok'

def main():
    items = list(need.items())
    res = {}
    bad = []
    with cf.ThreadPoolExecutor(8) as ex:
        for i, (url, new, st) in enumerate(ex.map(process, items)):
            if st == 'ok':
                res[url] = new
            else:
                bad.append((url, st))
            if i % 200 == 0:
                print(i, len(items), flush=True)
    old = {}
    fnm = B + '/migracion/media_map.json'
    if os.path.exists(fnm):
        old = json.load(open(fnm))
    old.update(res)
    json.dump(old, open(fnm, 'w'), indent=0, ensure_ascii=False)
    json.dump(bad, open(B + '/migracion/media_fail.json', 'w'), indent=1)
    print('ok', len(res), 'fallos', len(bad))

if __name__ == '__main__':
    main()
