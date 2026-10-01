#!/usr/bin/env python3
"""El idioma de una página lo dice su URL (sin prefijo = español), no el <html lang> del WordPress: TranslatePress servía
46 posts en español con lang="en-US", y la migración los había guardado como inglés (cabecera y pie en inglés, sin hreflang).
Corrige lang, carpeta y alternates de cualquier página cuyo idioma no coincida con su URL. Idempotente; forma parte del pipeline."""
import glob, json, os, re, sys
from urllib.parse import unquote

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ('ca', 'en', 'fr', 'de', 'it', 'nl', 'ru', 'uk')


def lang_de_url(path):
    m = re.match(r'/(%s)/' % '|'.join(LANGS), unquote(path).lower())
    return m.group(1) if m else 'es'


def main():
    n = 0
    for f in glob.glob(B + '/src/content/pages/*/*.json'):
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        lu = lang_de_url(d['path'])
        if d.get('lang') == lu and os.path.basename(os.path.dirname(f)) == lu:
            continue
        d['lang'] = lu
        alts = d.get('alternates') or {}
        if lu not in alts:
            alts[lu] = d['path']
        d['alternates'] = alts
        dest_dir = os.path.join(B, 'src', 'content', 'pages', lu)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(f))
        with open(dest, 'w', encoding='utf-8') as fh:
            json.dump(d, fh, ensure_ascii=False)
        if os.path.abspath(dest) != os.path.abspath(f):
            os.remove(f)
        n += 1
        print('·', d['path'], '->', lu)
    print('páginas con idioma corregido:', n)


if __name__ == '__main__':
    main()
