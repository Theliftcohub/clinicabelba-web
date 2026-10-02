#!/usr/bin/env python3
"""Inyecta en bloque las traducciones de los lotes de `migracion/traducciones/_jobs/jobNNN.json`.

Para cada archivo de cada lote: exige `dst` con la misma longitud que `src`, guarda el esqueleto de etiquetas de la
página (nombres de etiqueta y atributos salvo alt/title, en orden) ANTES de inyectar, llama a translate_posts.inject
y comprueba que el esqueleto DESPUÉS es idéntico: la traducción solo puede cambiar texto, nunca marcado.
Uso: python -X utf8 scripts/inject_jobs.py [--dry] [jobNNN ...]"""
import glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import translate_posts as tp
from bs4 import BeautifulSoup

B = tp.B if hasattr(tp, 'B') else os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS = os.path.join(B, 'migracion', 'traducciones', '_jobs')


def esqueleto(d):
    out = []
    for b in d['blocks']:
        S = BeautifulSoup(b['html'], 'html.parser')
        for t in S.find_all(True):
            attrs = {k: v for k, v in t.attrs.items() if k not in ('alt', 'title')}
            out.append((t.name, json.dumps(attrs, sort_keys=True, ensure_ascii=False)))
    return out


def main():
    dry = '--dry' in sys.argv
    sel = [a for a in sys.argv[1:] if not a.startswith('--')]
    manifests = sorted(glob.glob(os.path.join(JOBS, 'job*.json')))
    if sel:
        manifests = [m for m in manifests if os.path.basename(m)[:-5] in sel]
    ok = fallos = textos = 0
    for m in manifests:
        man = json.load(open(m, encoding='utf-8'))
        lang = man['lang']
        for f, slug in zip(man['files'], man['slugs']):
            t = json.load(open(f, encoding='utf-8'))
            if not t.get('dst') or len(t['dst']) != len(t['src']):
                print(f'FALLO {lang}/{slug}: dst ausente o longitud distinta'); fallos += 1; continue
            doc_f, d = tp.find_doc(lang, slug)
            antes = esqueleto(d)
            if dry:
                ok += 1; continue
            try:
                tp.inject(lang, slug)
            except SystemExit as e:
                print(f'FALLO {lang}/{slug}: {e}'); fallos += 1; continue
            _, d2 = tp.find_doc(lang, slug)
            if esqueleto(d2) != antes:
                print(f'FALLO {lang}/{slug}: el esqueleto de etiquetas cambió'); fallos += 1; continue
            ok += 1; textos += len(t['dst'])
    print(f'inyección: {ok} páginas OK, {fallos} fallos, {textos} textos')
    sys.exit(1 if fallos else 0)


if __name__ == '__main__':
    main()
