#!/usr/bin/env python3
"""Traducción de los posts que el WordPress servía en español bajo un prefijo de idioma.

TranslatePress mostraba en /en/, /ru/… los artículos nuevos sin traducir: la misma página en español con otra URL. La
migración los copió así. Este script separa el TEXTO del marcado para que la traducción no toque el HTML:

  extract <lang> <slug>  → escribe migracion/traducciones/<lang>/<slug>.json con {"src": [...]} (title, description,
                            alt/title de imágenes y cada nodo de texto del cuerpo, en orden; sin <style>/<script>)
  inject  <lang> <slug>  → lee el mismo archivo, que debe tener "dst" con la misma longitud, y escribe el JSON de la página
                            con los textos sustituidos uno a uno. El marcado queda idéntico (misma estructura, mismos atributos).
  check   <lang> <slug>  → comprueba que "dst" existe, tiene la misma longitud y que ningún texto quedó en español.

La URL no cambia (el slug español bajo el prefijo es el que Google ya conoce). Toda traducción es de la agencia y se
anota en NO_LITERAL.md; la clínica la revisa."""
import glob, json, os, re, sys
from urllib.parse import unquote

from bs4 import BeautifulSoup, NavigableString

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = B + '/migracion/traducciones'
SKIP_PARENTS = {'style', 'script', 'noscript', 'template'}


def find_doc(lang, slug):
    for f in glob.glob(B + f'/src/content/pages/{lang}/*.json'):
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        if unquote(d['path']).strip('/').split('/', 1)[-1] == slug and d.get('kind') == 'post':
            return f, d
    raise SystemExit(f'no encuentro el post {lang}/{slug}')


def text_nodes(soup):
    """Nodos de texto traducibles, en orden de documento (sin los de style/script ni los vacíos)."""
    out = []
    for s in soup.find_all(string=True):
        if not isinstance(s, NavigableString) or type(s).__name__ in ('Comment', 'Doctype', 'CData'):
            continue
        if s.parent and s.parent.name in SKIP_PARENTS:
            continue
        if not s.strip():
            continue
        out.append(s)
    return out


def img_attrs(soup):
    out = []
    for img in soup.find_all('img'):
        for a in ('alt', 'title'):
            if img.get(a, '').strip():
                out.append((img, a))
    return out


def extract(lang, slug):
    f, d = find_doc(lang, slug)
    src = [d['seo'].get('title') or '', d['seo'].get('description') or '']
    for b in d['blocks']:
        S = BeautifulSoup(b['html'], 'html.parser')
        src += [str(s) for s in text_nodes(S)]
        src += [img[a] for img, a in img_attrs(S)]
    os.makedirs(f'{OUT}/{lang}', exist_ok=True)
    p = f'{OUT}/{lang}/{slug}.json'
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump({'lang': lang, 'slug': slug, 'path': d['path'], 'src': src}, fh, ensure_ascii=False, indent=0)
    print(f'{lang}/{slug}: {len(src)} textos, {sum(len(s.split()) for s in src)} palabras → {p}')


def inject(lang, slug):
    f, d = find_doc(lang, slug)
    p = f'{OUT}/{lang}/{slug}.json'
    with open(p, encoding='utf-8') as fh:
        t = json.load(fh)
    src, dst = t['src'], t.get('dst')
    if not dst or len(dst) != len(src):
        raise SystemExit(f'{lang}/{slug}: dst ausente o con otra longitud ({len(dst or [])} ≠ {len(src)})')
    i = 0
    d['seo']['title'] = dst[0]; i += 1
    if d['seo'].get('description'):
        d['seo']['description'] = dst[1]
    i = 2
    for b in d['blocks']:
        S = BeautifulSoup(b['html'], 'html.parser')
        nodes = text_nodes(S)
        for s in nodes:
            # conservar el espacio inicial/final del nodo original (separa palabras entre etiquetas)
            orig = str(s)
            lead = orig[:len(orig) - len(orig.lstrip())]; trail = orig[len(orig.rstrip()):]
            s.replace_with(NavigableString(lead + dst[i].strip() + trail)); i += 1
        for img, a in img_attrs(S):
            img[a] = dst[i]; i += 1
        b['html'] = str(S)
    assert i == len(dst), (i, len(dst))
    with open(f, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False)
    print(f'{lang}/{slug}: {i} textos inyectados en {os.path.basename(f)}')


def check(lang, slug):
    p = f'{OUT}/{lang}/{slug}.json'
    with open(p, encoding='utf-8') as fh:
        t = json.load(fh)
    src, dst = t['src'], t.get('dst') or []
    ok = len(dst) == len(src)
    iguales = sum(1 for a, b in zip(src, dst) if a.strip() == b.strip() and len(a.split()) > 3)
    print(f'{lang}/{slug}: longitud {"OK" if ok else "MAL"} ({len(dst)}/{len(src)}) · textos largos sin traducir: {iguales}')
    return ok and iguales == 0


if __name__ == '__main__':
    cmd, lang, slug = sys.argv[1:4]
    {'extract': extract, 'inject': inject, 'check': check}[cmd](lang, slug)
