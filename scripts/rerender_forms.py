#!/usr/bin/env python3
"""Vuelve a generar in situ los formularios nativos que vienen de Typeform (data-form-id="tf-…") en todas las
páginas menos las portadas (esas las regenera home_nueva.py). Sirve para aplicar cambios de forms_native.py /
forms_i18n.py sin rehacer todo el pipeline. Uso: BELBA_ROOT=. python scripts/rerender_forms.py"""
import json, glob, re, os, sys
B = os.environ.get('BELBA_ROOT', '/home/claude/belba')
sys.path.insert(0, B + '/scripts')
import forms_native

# convert.py insertó los formularios con BeautifulSoup, que ordena los atributos alfabéticamente: no fiarse del orden
RX = re.compile(r'<form [^>]*class="belba-form[^"]*"[^>]*data-form-id="tf-([A-Za-z0-9]+)"[^>]*>.*?</form>', re.S)

def main():
    n_pages = n_forms = 0
    for f in sorted(glob.glob(B + '/src/content/pages/*/*.json')):
        doc = json.load(open(f, encoding='utf-8'))
        if re.fullmatch(r'/(\w\w/)?', doc['path']):
            continue
        changed = False
        for b in doc['blocks']:
            if 'data-form-id="tf-' not in b['html']:
                continue
            def sub(m):
                return forms_native.render(m.group(1), doc['lang'], doc['path'])
            new, k = RX.subn(sub, b['html'])
            if k:
                b['html'] = new; changed = True; n_forms += k
        if changed:
            json.dump(doc, open(f, 'w', encoding='utf-8'), ensure_ascii=False)
            n_pages += 1
    print('formularios regenerados:', n_forms, 'en', n_pages, 'páginas')

if __name__ == '__main__':
    main()
