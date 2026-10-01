#!/usr/bin/env python3
"""Caché del HTML renderizado del WordPress, la que llena `scripts/fase1/prefetch.py` en `.fetchcache/`
(un JSON por URL, nombrado con el sha1 de la URL, como hace `extract_wp.fetch`). `convert.py` la lee desde aquí:

    pages()  -> [{'path': '/ruta/', 'url': 'https://…', 'cache': '<fichero o None>', 'decision': 'mantener'}] (las URL del contrato)
    html(p)  -> HTML de esa página

Sin `.fetchcache/` no se puede volver a convertir (haría falta volver a descargar el WordPress con prefetch.py)."""
import csv, hashlib, json, os
from urllib.parse import quote, unquote

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = 'https://clinicabelba.com'
CACHE = os.environ.get('FETCH_CACHE') or os.path.join(B, '.fetchcache')


def _cache_path(url):
    return os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest())


def _candidates(path):
    """La URL se pudo cachear decodificada o en %xx (el sitemap las da codificadas)."""
    dec = unquote(path)
    enc = quote(dec, safe='/%:')
    return [DOM + path, DOM + enc, DOM + dec, DOM + quote(dec, safe='/')]


def pages():
    out = []
    with open(os.path.join(B, 'migracion', 'urls.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r.get('decision') != 'mantener':
                continue
            cache = next((c for c in (_cache_path(u) for u in _candidates(r['url'])) if os.path.exists(c)), None)
            out.append({'path': r['url'], 'url': DOM + r['url'], 'cache': cache, 'decision': r['decision'], 'tipo': r.get('tipo', '')})
    return out


def html(p):
    with open(p['cache'], encoding='utf-8') as f:
        return json.load(f)['body']
