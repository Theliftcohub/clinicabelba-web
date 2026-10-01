#!/usr/bin/env python3
"""Listado completo del blog. La página /blog/ del WordPress (y sus traducciones) era un widget de Elementor con los 5 últimos
posts y sin paginación, así que la copia estática solo enlazaba 5 de los 55 artículos. Este script vuelve a generar el
contenedor de posts de cada página de blog con TODOS los posts de su idioma (los `mantener` del contrato, ya migrados),
de más reciente a más antiguo, usando el mismo marcado de tarjeta del widget (miniatura, título, fecha, «Leer más»).
Título, H1, textos, SEO y URL de la página no cambian. Idempotente; va en el pipeline tras postprocess.py y fix_lang.py."""
import glob, json, os, re
from datetime import datetime
from bs4 import BeautifulSoup
from fix_srcset import srcset_for

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# formato del widget del WordPress en cada idioma: «{mes} {día}, {año}»
MESES = {
    'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
    'fr': ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
    'it': ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'],
    'nl': ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
    'ca': ['gener', 'febrer', 'març', 'abril', 'maig', 'juny', 'juliol', 'agost', 'setembre', 'octubre', 'novembre', 'desembre'],
    'ru': ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'],
    'uk': ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'],
}


def fecha(iso, lang):
    dt = datetime.fromisoformat(iso[:19])
    return f'{MESES.get(lang, MESES["es"])[dt.month - 1]} {dt.day}, {dt.year}'


def titulo(p):
    """El título del post tal como aparece en su H1 (el widget del WordPress mostraba el título de la entrada)."""
    for b in p['blocks']:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', b['html'], re.S)
        if m:
            return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip()
    return p['seo']['title'].split(' | ')[0]


def main():
    docs = []
    for f in glob.glob(B + '/src/content/pages/*/*.json'):
        with open(f, encoding='utf-8') as fh:
            docs.append((f, json.load(fh)))
    posts = {}
    for f, d in docs:
        if d.get('kind') == 'post' and (d.get('post') or {}).get('date') and not re.search(r'noindex', d['seo'].get('robots') or '', re.I):
            posts.setdefault(d['lang'], []).append(d)
    for lang in posts:
        posts[lang].sort(key=lambda d: d['post']['date'], reverse=True)
    for f, d in docs:
        if not d['path'].endswith('/blog/'):
            continue
        lang = d['lang']
        cambiado = False
        for b in d['blocks']:
            if 'k-widget-posts' not in b['html']:
                continue
            S = BeautifulSoup(b['html'], 'html.parser')
            cont = S.select_one('.k-widget-posts .k-posts-container')
            modelo = cont.select_one('article.k-post') if cont else None
            if cont is None or modelo is None:
                continue
            plantilla = str(modelo)
            cont.clear()
            for p in posts.get(lang, []):
                art = BeautifulSoup(plantilla, 'html.parser').select_one('article')
                for a in art.select('a'):
                    a['href'] = p['path']
                img = art.select_one('img')
                src = (p.get('post') or {}).get('image') or p['seo'].get('ogImage')
                if img is not None and src:
                    img['src'] = src
                    base, ext = os.path.splitext(src)
                    ss = srcset_for(src)  # anchos reales (fix_srcset.py)
                    if ss:
                        img['srcset'] = ss
                    elif img.has_attr('srcset'):
                        del img['srcset']
                    img['alt'] = ''
                    for k in ('fetchpriority',):
                        if img.has_attr(k):
                            del img[k]
                    img['loading'] = 'lazy'
                t = art.select_one('.k-post__title a')
                if t is not None:
                    t.string = titulo(p)
                fd = art.select_one('.k-post-date')
                if fd is not None:
                    fd.string = fecha(p['post']['date'], lang)
                cont.append(art)
            b['html'] = str(S)
            cambiado = True
        if cambiado:
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False)
            print(f'· {d["path"]}: {len(posts.get(lang, []))} posts')


if __name__ == '__main__':
    main()
