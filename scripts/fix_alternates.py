#!/usr/bin/env python3
"""Alternates (hreflang + selector de idioma) que apuntan a URLs que ya no son páginas.

El mapa de traducciones viene del hreflang del WordPress (TranslatePress). Algunas de esas URLs están hoy en el contrato
como 301 (p. ej. la antigua /abdominoplastia/ → /abdominoplastia-barcelona/, o las «traducciones huérfanas» de
/cirujano-plastico/nosotros/, que redirigen a la propia página en español) o como 410. Un hreflang o un enlace del
selector a una URL que redirige lo ignora Google y hace pasar al visitante por un salto innecesario.

Regla: si el destino existe como página, se conserva; si es un 301, se sigue la cadena y se sustituye por el destino
final SOLO si es una página del mismo idioma; en cualquier otro caso (410, idioma distinto, no existe) se quita.
Idempotente; va en el pipeline tras fix_lang.py."""
import csv, glob, json, os
from urllib.parse import unquote

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ('ca', 'en', 'fr', 'de', 'it', 'nl', 'ru', 'uk')


def norm(u):
    return unquote(u or '').lower()


def lang_de(path):
    p = path.split('/')
    return p[1] if len(p) > 2 and p[1] in LANGS else 'es'


def main():
    contrato = {}
    with open(B + '/migracion/urls.csv', encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            contrato[norm(r['url'])] = (r['decision'], r['destino'])

    docs = []
    for f in glob.glob(B + '/src/content/pages/*/*.json'):
        with open(f, encoding='utf-8') as fh:
            docs.append((f, json.load(fh)))
    existe = {norm(d['path']): d['path'] for _, d in docs}

    def final(url):
        """Sigue la cadena de 301 del contrato; devuelve la ruta final si es una página, o None."""
        vistos = set()
        u = norm(url)
        while u not in existe and u in contrato and contrato[u][0] == '301' and u not in vistos:
            vistos.add(u)
            u = norm(contrato[u][1])
        return existe.get(u)

    sustituidos = quitados = paginas = 0
    for f, d in docs:
        alts = d.get('alternates')
        if not alts:
            continue
        nuevo, cambio = {}, False
        for lang, url in alts.items():
            if norm(url) in existe:
                nuevo[lang] = url
                continue
            dest = final(url)
            if dest and lang_de(dest) == lang:
                nuevo[lang] = dest
                sustituidos += 1
            else:
                quitados += 1
            cambio = True
        if cambio:
            d['alternates'] = nuevo
            paginas += 1
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False)
    print(f'alternates: {paginas} páginas corregidas · {sustituidos} sustituidos por el destino del 301 · {quitados} quitados (410, huérfanos o idioma distinto)')

    # el mapa de traducciones (fuente del contrato y del validador --i18n) sigue la misma regla
    pm = B + '/migracion/i18n-map.json'
    with open(pm, encoding='utf-8') as fh:
        mapa = json.load(fh)
    cambios = 0
    for clave, alts in list(mapa.items()):
        nuevo = {}
        for lang, url in alts.items():
            if norm(url) in existe:
                nuevo[lang] = url
            else:
                dest = final(url)
                if dest and lang_de(dest) == lang:
                    nuevo[lang] = dest
        if nuevo != alts:
            mapa[clave] = nuevo
            cambios += 1
    if cambios:
        with open(pm, 'w', encoding='utf-8') as fh:
            json.dump(mapa, fh, ensure_ascii=False, indent=1)
    print(f'i18n-map.json: {cambios} entradas corregidas')


if __name__ == '__main__':
    main()
