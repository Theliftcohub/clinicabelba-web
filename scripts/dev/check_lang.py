#!/usr/bin/env python3
"""Auditoría de idioma: páginas bajo un prefijo de idioma cuyo texto visible está en español (herencia de TranslatePress:
servía la página española en /en/, /ru/… cuando no había traducción). Mide la proporción de palabras funcionales
españolas en el cuerpo y compara el title con el de la página española equivalente. Uso:
    python -X utf8 scripts/dev/check_lang.py            → tabla de sospechosas
    python -X utf8 scripts/dev/check_lang.py --csv out  → además, CSV"""
import glob, json, os, re, sys
from urllib.parse import unquote

B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ES = {'el', 'la', 'los', 'las', 'de', 'del', 'que', 'y', 'en', 'un', 'una', 'es', 'por', 'para', 'con', 'se', 'su',
      'al', 'como', 'más', 'pero', 'también', 'cuando', 'sobre', 'este', 'esta', 'tras', 'entre', 'desde', 'hasta', 'o'}
OTHER = {'the', 'and', 'of', 'to', 'la', 'le', 'les', 'des', 'et', 'und', 'der', 'die', 'das', 'il', 'di', 'che', 'e',
         'het', 'van', 'een', 'en', 'и', 'в', 'на', 'с', 'і', 'та', 'з', 'els', 'amb', 'per', 'és', 'els', 'dels'}


def texto(d):
    h = ''.join(b['html'] for b in d['blocks'])
    h = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', h)


def main():
    docs = {}
    for f in glob.glob(B + '/src/content/pages/*/*.json'):
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        docs[d['path']] = d
    es_por_slug = {d['path'].strip('/'): d for d in docs.values() if d['lang'] == 'es'}
    filas = []
    for p, d in docs.items():
        if d['lang'] == 'es':
            continue
        words = re.findall(r"[a-záéíóúñüçàèòïıа-яёіїє']+", texto(d).lower())
        if len(words) < 80:
            continue
        es = sum(1 for w in words if w in ES) / len(words)
        slug = unquote(p).split('/', 2)[2].strip('/')
        esd = es_por_slug.get(slug)
        mismo_title = bool(esd) and esd['seo']['title'] == d['seo']['title']
        if es > 0.18 or mismo_title:
            filas.append((d['lang'], unquote(p), d.get('kind'), round(es, 2), mismo_title, (d['seo'].get('robots') or '')[:7], d['seo']['title'][:60]))
    filas.sort()
    print(f'{len(filas)} páginas traducidas con texto o title en español:')
    for r in filas:
        print('  %s %-62s %-5s es=%.2f title=ES:%-5s %s | %s' % r)
    if '--csv' in sys.argv:
        import csv
        out = sys.argv[sys.argv.index('--csv') + 1]
        with open(out, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh); w.writerow(['lang', 'path', 'kind', 'ratio_es', 'title_igual_es', 'robots', 'title']); w.writerows(filas)
        print('CSV:', out)


if __name__ == '__main__':
    main()
