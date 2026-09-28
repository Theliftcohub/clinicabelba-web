#!/usr/bin/env python3
"""Convierte el HTML renderizado del WordPress (Elementor + TranslatePress) en JSON de página
para Astro, sin dependencias de WordPress. Contenido literal; maquetación reproducida con CSS local.

Salidas:
  src/content/pages/<lang>/<id>.json   una por URL 'mantener' del contrato
  src/content/layout/<lang>.json       cabecera y pie por idioma
  migracion/media_needed.json          medios referenciados (URL original -> ruta local)
  migracion/convert_log.json           avisos por página
"""
import csv, json, os, re, sys, hashlib, html as H
from urllib.parse import unquote, quote, urlparse, parse_qs
from bs4 import BeautifulSoup, Comment, NavigableString

B = '/home/claude/belba'
DOM = 'https://clinicabelba.com'
sys.path.insert(0, '/tmp/claude-0/-home-claude/aae1ead6-8dc9-546f-ae1d-382cc271829d/scratchpad')
from pages import pages as load_pages, html as load_html

LANGS = {'es-ES': 'es', 'ca': 'ca', 'en-US': 'en', 'fr-FR': 'fr', 'de-DE': 'de', 'it-IT': 'it', 'nl-NL': 'nl', 'ru-RU': 'ru', 'uk': 'uk'}

# ---------- contrato ----------
CONTRACT = {}
for r in csv.DictReader(open(B + '/migracion/urls.csv')):
    CONTRACT[unquote(r['url'].replace(DOM, '')).lower()] = r

LINK_MAP = json.load(open(B + '/migracion/link_map.json')) if os.path.exists(B + '/migracion/link_map.json') else {}

def enc_path(p):
    """ruta decodificada -> ruta publicada (percent-encoded en minúsculas, como WordPress)"""
    return quote(p, safe="/-_.~!$&'()*+,;=:@%").replace('%', '%').lower() if re.search(r'[^\x00-\x7f]', p) else p

def resolve_internal(path_q):
    """Devuelve (ruta_final, estado) para un enlace interno: sigue 301 del contrato."""
    path, _, frag = path_q.partition('#')
    path, _, qs = path.partition('?')
    key = unquote(path).lower()
    if key and not key.endswith('/') and '.' not in key.rsplit('/', 1)[-1]:
        key += '/'
    if key not in CONTRACT and key in LINK_MAP:
        return LINK_MAP[key] + (('#' + frag) if frag else ''), 'mantener'
    seen = 0
    r = CONTRACT.get(key)
    while r and r['decision'] == '301' and seen < 5:
        key = unquote(r['destino'].replace(DOM, '')).lower()
        r = CONTRACT.get(key); seen += 1
    st = r['decision'] if r else ('mantener' if seen else None)
    out = enc_path(unquote(key)) if st else path
    if st is None:
        out = path
    return out + (('?' + qs) if qs and not re.match(r'(utm_|fbclid|gclid)', qs) else '') + (('#' + frag) if frag else ''), st

# ---------- medios ----------
SEEN = {}
MEDIA = {}  # url original (sin query) -> ruta local /images/...
MEDIA_INDEX = {}
for m in json.load(open(B + '/migracion/media.json')):
    u = m['source_url']
    stem = os.path.splitext(os.path.basename(u))[0].lower()
    MEDIA_INDEX.setdefault(stem, u)

SIZE_RX = re.compile(r'-(\d+x\d+|\d+xh|scaled|e\d{10,})(?=\.\w+$)')

def original_of(u):
    u = u.split('?')[0].split('#')[0]
    if u.startswith('//'): u = 'https:' + u
    if u.startswith('/wp-content/'): u = DOM + u
    if '/elementor/thumbs/' in u:
        base = os.path.basename(u)
        stem = re.sub(r'-[a-z0-9]{40,}$', '', os.path.splitext(base)[0]).lower()
        if stem in MEDIA_INDEX: return MEDIA_INDEX[stem]
        return u
    o = SIZE_RX.sub('', u)
    o = SIZE_RX.sub('', o)
    return o

def local_media(u):
    """URL de uploads -> ruta local servida por la web nueva."""
    o = original_of(u)
    if '/wp-content/uploads/' not in o:
        return None
    rel = unquote(o.split('/wp-content/uploads/', 1)[1]).split('?')[0].split('#')[0]
    rel = re.sub(r'^elementor/thumbs/', 'thumbs/', rel)
    root, ext = os.path.splitext(rel)
    ext = ext.lower()
    if ext in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tif', '.tiff'):
        new = '/images/' + root + '.webp'
    else:
        new = '/images/' + rel  # svg, gif, pdf, mp4...
    MEDIA[o] = new
    SEEN.setdefault(o, set()).add(u.split('?')[0] if not u.startswith('/') else DOM + u.split('?')[0])
    return new

def rewrite_url(u):
    if not u: return u
    u = H.unescape(u.strip())
    if re.match(r'^(https?:)?//(www\.)?clinicabelba\.com', u) or u.startswith('/'):
        p = re.sub(r'^(https?:)?//(www\.)?clinicabelba\.com', '', u) or '/'
        if p.startswith('/wp-content/uploads/'):
            lm = local_media(p)
            return lm or p
        if p.startswith('/wp-content/') or p.startswith('/wp-includes/'):
            return None
        return resolve_internal(p)[0]
    return u

# ---------- clases ----------
def ren_cls(c):
    if c in ('elementor-invisible', 'animated', 'elementor-motion-effects-element', 'elementor-motion-effects-parent'):
        return None
    if c.startswith('animated-') or c in ('fadeInUp', 'fadeInLeft', 'fadeIn', 'zoomIn', 'fadeInDown', 'fadeInRight'):
        return None
    if c == 'elementor': return 'k'
    if c.startswith('elementor-'): return 'k-' + c[10:]
    if c.startswith('wp-image-') or c.startswith('attachment-') or c.startswith('size-'): return None
    if c.startswith('trp-'): return c
    return c

def ren_css(css):
    css = re.sub(r'\.elementor-', '.k-', css)
    css = re.sub(r'\.elementor(?=[\s,{:.>+~\[)])', '.k', css)
    css = re.sub(r'#elementor-', '#k-', css)
    css = re.sub(r'\[data-elementor-type=[\'"]?(\w[\w-]*)[\'"]?\]', r'.kt-\1', css)
    css = css.replace('elementor-', 'k-').replace('elementor', 'kel')
    def u(m):
        raw = m.group(1).strip('\'" ')
        nu = rewrite_url(raw) if not raw.startswith('data:') else raw
        return 'url("%s")' % (nu or '')
    css = re.sub(r'url\(([^)]+)\)', u, css)
    return css

ALLOWED_SCRIPT = re.compile(r'cdn\.trustindex\.io|trustindex', re.I)
import forms_native

def yt_id(url):
    m = re.search(r'(?:youtu\.be/|v=|shorts/|embed/)([\w-]{11})', url or '')
    return m.group(1) if m else None

def jsonld_of(b, warn):
    out = []
    for raw in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', b, re.S):
        try:
            j = json.loads(raw)
        except Exception:
            warn.append('JSON-LD roto en el original: descartado'); continue
        out.append(fix_ld(j, warn))
    return [o for o in out if o]

RETIRED = {'HowTo', 'HowToStep', 'HowToSection'}

def fix_ld(o, warn, parent_type=None):
    if isinstance(o, list):
        return [x for x in (fix_ld(i, warn, parent_type) for i in o) if x is not None]
    if isinstance(o, dict):
        t = o.get('@type')
        ts = set(t if isinstance(t, list) else [t]) if t else set()
        if ts & RETIRED:
            warn.append('schema HowTo retirado'); return None
        n = {}
        for k, v in o.items():
            if k == 'potentialAction':
                acts = v if isinstance(v, list) else [v]
                acts = [a for a in acts if not (isinstance(a, dict) and a.get('@type') == 'SearchAction')]
                if len(acts) != (len(v) if isinstance(v, list) else 1): warn.append('SearchAction (cuadro de búsqueda) retirado')
                if acts: n[k] = fix_ld(acts if isinstance(v, list) else acts[0], warn, t)
                continue
            if k in ('aggregateRating', 'review') and ts & {'LocalBusiness', 'Organization', 'MedicalClinic', 'MedicalBusiness', 'MedicalOrganization', 'Physician', 'Corporation'}:
                warn.append(f'{k} retirado de {"/".join(sorted(x for x in ts if x))} (regla: no heredar valoraciones propias)'); continue
            n[k] = fix_ld(v, warn, t)
        return n
    if isinstance(o, str):
        if re.match(r'^(https?:)?//(www\.)?clinicabelba\.com', o):
            p = re.sub(r'^(https?:)?//(www\.)?clinicabelba\.com', '', o) or '/'
            if p.startswith('/wp-content/uploads/'):
                lm = local_media(p); return DOM + lm if lm else o
            if p.startswith('/#') or p.startswith('#'):
                return o
            nu, st = resolve_internal(p)
            return DOM + nu if st else o
        return o
    return o

LOG = {}

def clean(soup, page_path, lang, warn, posts_index):
    # Typeform -> formulario nativo (decisión 28/09)
    for tfn in soup.find_all(attrs={'data-tf-live': True}) + soup.find_all(attrs={'data-tf-widget': True}):
        tid = tfn.get('data-tf-live') or tfn.get('data-tf-widget')
        nf = BeautifulSoup(forms_native.render(tid, lang, page_path), 'html.parser')
        tfn.replace_with(nf)
        warn.append('Typeform %s sustituido por formulario nativo' % tid)
    # comentarios
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    # scripts
    for s in soup.find_all('script'):
        src = s.get('src', '')
        if s.get('type') == 'application/ld+json':
            s.decompose(); continue
        if src and ALLOWED_SCRIPT.search(src):
            s.attrs = {'src': src if not src.startswith('//') else 'https:' + src, 'async': ''}
            continue
        if not src and s.find_parent(attrs={'data-widget_type': 'html.default'}) and not re.search(r'wp-|jQuery|elementor', s.string or ''):
            continue
        s.decompose()
    for t in soup.find_all(['noscript', 'link', 'meta']):
        t.decompose()
    for st in soup.find_all('style'):
        if st.string is not None:
            st.string = ren_css(st.string)
        else:
            txt = ren_css(st.get_text()); st.clear(); st.append(txt)
    # widgets especiales antes de limpiar atributos
    for w in soup.find_all(attrs={'data-widget_type': True}):
        wt = w['data-widget_type']
        try:
            st = json.loads(w.get('data-settings') or '{}')
        except Exception:
            st = {}
        if wt == 'video.default':
            vid = yt_id(st.get('youtube_url', ''))
            box = w.find(class_='elementor-video') or w.find(class_='elementor-wrapper')
            if vid and box:
                box.clear()
                box.append(BeautifulSoup(f'<iframe class="k-video-iframe" loading="lazy" src="https://www.youtube-nocookie.com/embed/{vid}" title="YouTube" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', 'html.parser'))
                if 'shorts/' in st.get('youtube_url', ''):
                    w['style'] = (w.get('style', '') + ';--video-aspect-ratio:0.5625').strip(';')
            elif st.get('video_type') == 'hosted' and st.get('hosted_url', {}).get('url') if isinstance(st.get('hosted_url'), dict) else False:
                pass
            else:
                warn.append('video sin youtube_url')
        elif wt == 'accordion.default':
            for item in w.find_all(class_='elementor-accordion-item'):
                title = item.find(class_='elementor-tab-title'); content = item.find(class_='elementor-tab-content')
                if not (title and content): continue
                d = soup.new_tag('details'); d['class'] = ['k-accordion-item']
                sm = soup.new_tag('summary'); sm['class'] = ['k-tab-title']
                a = title.find(class_='elementor-accordion-title')
                ico = title.find(class_='elementor-accordion-icon')
                if ico: sm.append(ico)
                # conserva el nivel de encabezado del título
                hn = soup.new_tag(title.name if title.name in ('h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div') else 'span'); hn['class'] = ['k-accordion-title']
                for ch in list((a or title).contents): hn.append(ch)
                sm.append(hn); d.append(sm)
                c2 = soup.new_tag('div'); c2['class'] = ['k-tab-content', 'k-clearfix']
                for ch in list(content.contents): c2.append(ch)
                d.append(c2)
                item.replace_with(d)
        elif wt == 'posts.classic':
            cont = w.find(class_='elementor-posts-container')
            arts = cont.find_all('article') if cont else []
            n = len(arts)
            if cont and n:
                tmpl = str(arts[0])
                keep = []
                for a in arts:
                    href = (a.find('a', href=True) or {}).get('href', '')
                    p = unquote(re.sub(r'^https?://clinicabelba\.com', '', href)).lower()
                    r = CONTRACT.get(p)
                    if r and r['decision'] == 'mantener':
                        keep.append(a)
                    else:
                        a.decompose()
                if len(keep) < n:
                    warn.append(f'lista de posts: {n - len(keep)} entradas de prueba retiradas')
            pag = w.find(class_='elementor-pagination')
            if pag: pag.decompose()
        elif wt == 'table-of-contents.default':
            body = w.find(class_='elementor-toc__body')
            if body is not None:
                ms = []
                page_root = soup.find(attrs={'data-elementor-type': re.compile('single-post|wp-page|single-page|wp-post')}) or soup
                for hh in page_root.find_all(['h2', 'h3']):
                    if hh.find_parent(attrs={'data-widget_type': 'table-of-contents.default'}): continue
                    t = hh.get_text(' ', strip=True)
                    if not t: continue
                    hid = hh.get('id') or ('toc-' + re.sub(r'[^\w]+', '-', t.lower())[:60].strip('-'))
                    hh['id'] = hid
                    ms.append((hh.name, hid, t))
                ol = soup.new_tag('ol'); ol['class'] = ['k-toc__list-wrapper']
                for tag, hid, t in ms:
                    li = soup.new_tag('li'); li['class'] = ['k-toc__list-item'] + (['k-toc__sub'] if tag == 'h3' else [])
                    a = soup.new_tag('a', href='#' + hid); a['class'] = ['k-toc__list-item-text']; a.string = t
                    li.append(a); ol.append(li)
                body.clear(); body.append(ol)
                sp = w.find(class_='elementor-toc__spinner-container')
                if sp: sp.decompose()
        elif wt == 'form.default':
            f = w.find('form')
            if f:
                f['action'] = '/form-handler.php'; f['method'] = 'post'
                f['data-belba-form'] = ''
                for hid in f.find_all('input', type='hidden'):
                    if hid.get('name') in ('referer_title', 'queried_id'): hid.decompose()
                hp = BeautifulSoup('<div class="hp-field" aria-hidden="true"><label>No rellenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>', 'html.parser')
                f.insert(0, hp)
                pg = soup.new_tag('input', type='hidden'); pg['name'] = 'page'; pg['value'] = page_path; f.insert(0, pg)
                lg = soup.new_tag('input', type='hidden'); lg['name'] = 'lang'; lg['value'] = lang; f.insert(0, lg)
                f['data-form-id'] = 'el-' + ((f.find('input', attrs={'name': 'form_id'}) or {}).get('value') or '')
                f['data-form-name'] = f.get('name') or 'Formulario'
                for hn in forms_native.HIDDEN:
                    hi = soup.new_tag('input', type='hidden'); hi['name'] = hn; f.insert(0, hi)
        elif wt == 'nav-menu.default':
            pass
        if st.get('sticky') in ('top',) :
            w['class'] = w.get('class', []) + ['k-sticky-top']
    for sec in soup.find_all(attrs={'data-settings': True}):
        try:
            st = json.loads(sec['data-settings'])
        except Exception:
            continue
        if st.get('sticky') == 'top':
            sec['class'] = sec.get('class', []) + ['k-sticky-top']
        if st.get('background_slideshow_gallery'):
            warn.append('fondo con pase de diapositivas (se usa la primera imagen)')
    # formularios MetForm (si queda alguno)
    # clases que Elementor añade por JS en el navegador (sin ellas se ocultan fondos o se descuadran rejillas)
    for t in soup.find_all(class_=['e-con', 'elementor-section', 'elementor-column']):
        t['class'] = t.get('class', []) + ['e-lazyloaded']
    for t in soup.find_all(class_='elementor-posts-container'):
        t['class'] = t.get('class', []) + ['elementor-has-item-ratio']
    # imágenes: elegir el mejor candidato del srcset como fuente (algunos src del original dan 404)
    for img in soup.find_all(['img', 'source']):
        ss = img.get('srcset') or img.get('data-srcset') or ''
        cands = []
        for part in ss.split(','):
            bits = part.strip().split()
            if not bits: continue
            w = int(re.sub(r'\D', '', bits[1]) or 0) if len(bits) > 1 and bits[1].endswith('w') else 0
            cands.append((w, bits[0]))
        if cands:
            cands.sort(reverse=True)
            img['data-alt-src'] = ' '.join(c[1] for c in cands)
            for _, cu in cands:
                if '/wp-content/uploads/' in cu:
                    local_media(cu)
    # atributos
    for t in soup.find_all(True):
        attrs = {}
        for k, v in t.attrs.items():
            if k in ('data-settings', 'data-e-type', 'data-widget_type', 'data-id', 'data-elementor-id',
                     'data-elementor-post-type', 'data-elementor-settings', 'data-no-translation', 'data-trp-original-href', 'data-model-cid',
                     'data-trp-placeholder', 'data-trpgettextoriginal', 'data-rocket-lazyload', 'srcset', 'sizes', 'data-alt-src', 'data-srcset', 'data-e-action-hash', 'data-elementor-open-lightbox', 'data-elementor-lightbox-slideshow') and not (k == 'sizes' and t.name == 'source'):
                if k == 'data-elementor-type':
                    pass
                continue
            if k == 'data-elementor-type':
                attrs['data-kt'] = v; continue
            if k.startswith('data-elementor'):
                continue
            if k == 'class':
                cl = [x for x in (ren_cls(c) for c in (v if isinstance(v, list) else v.split())) if x]
                if cl: attrs['class'] = cl
                continue
            if k in ('id', 'aria-controls', 'aria-labelledby', 'for', 'data-tab-title-id') and isinstance(v, str):
                v = v.replace('elementor-', 'k-')
            if k == 'href' and isinstance(v, str) and v.startswith('#elementor-'):
                v = '#k-' + v[11:]
            if k == 'data-css-url':
                v = '/css/trustindex-google-widget.css'
            if k in ('href',) and isinstance(v, str):
                nv = rewrite_url(v)
                if nv is None:
                    warn.append('enlace a wp-content/wp-includes eliminado: ' + v[:80]); continue
                if t.name == 'a':
                    p0 = re.sub(r'^(https?:)?//(www\.)?clinicabelba\.com', '', v)
                    if p0.startswith('/') and not p0.startswith('/wp-content'):
                        _, stt = resolve_internal(p0)
                        if stt == '410':
                            warn.append('enlace a URL 410 convertido en texto: ' + p0[:80]); t.name = 'span'; continue
                v = nv
            if k in ('src', 'data-src', 'poster') and isinstance(v, str):
                nv = rewrite_url(v)
                if nv is None:
                    warn.append('recurso wp eliminado: ' + v[:80]); continue
                v = nv
            if k == 'style' and isinstance(v, str):
                v = ren_css(v)
            if k == 'target' and v == '"_blank"':
                v = '_blank'
            attrs[k] = v
        if 'data-kt' in attrs:
            attrs['class'] = attrs.get('class', []) + ['kt-' + attrs['data-kt']]
        t.attrs = attrs
    # imágenes: srcset a partir de la local
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.startswith('/images/') and src.endswith('.webp'):
            img['srcset'] = f"{src[:-5]}-800.webp 800w, {src} 1600w"
            img['sizes'] = img.get('sizes') or '(max-width: 800px) 100vw, 800px'
        if not img.get('loading') and not img.get('fetchpriority'):
            img['loading'] = 'lazy'
        img['decoding'] = 'async'
        if 'alt' not in img.attrs:
            img['alt'] = ''
            warn.append('imagen sin alt: ' + src[:80])
    return soup


def split_page(b):
    soup = BeautifulSoup(b, 'lxml')
    body = soup.body
    header = body.find(attrs={'data-elementor-type': 'header'})
    footer = body.find(attrs={'data-elementor-type': 'footer'})
    return soup, body, header, footer


def page_css(b):
    m = re.search(r'<style id="elementor-frontend-inline-css">(.*?)</style>', b, re.S)
    css = m.group(1) if m else ''
    m2 = re.search(r'<style id="wp-custom-css">(.*?)</style>', b, re.S)
    extra = m2.group(1) if m2 else ''
    head = b[:b.find('<body')]
    for mm in re.finditer(r'<style(?![^>]*\sid=)[^>]*>(.*?)</style>', head, re.S):
        css += '\n' + mm.group(1)
    return css, extra


def main():
    P = load_pages()
    if os.environ.get('ONLY'):
        P = [p for p in P if p['path'] in os.environ['ONLY'].split(',')]
    i18n = json.load(open(B + '/migracion/i18n-map.json'))
    alt_of = {}
    for g, m in i18n.items():
        for lg, p in m.items():
            alt_of[unquote(p).lower()] = m
    inv = {unquote(i['url'].replace(DOM, '')).lower(): i for i in json.load(open(B + '/migracion/inventory.json'))['items']}
    outdir = B + '/src/content/pages'
    os.makedirs(outdir, exist_ok=True)
    layouts = {}
    custom_css = None
    n = 0
    for p in P:
        if not p['cache']:
            continue
        b = load_html(p)
        warn = []
        m = re.search(r'<html[^>]*\slang="([\w-]+)"', b)
        lang = LANGS.get(m.group(1) if m else 'es-ES', 'es')
        path = p['path']
        soup, body, header, footer = split_page(b)
        mb = re.search(r'<body[^>]*class="([^"]*)"', b)
        bodycls = [x for x in (ren_cls(c) for c in (mb.group(1).split() if mb else [])) if x and (x.startswith('k') or x in ('home','single-post','page'))]
        kind = 'post' if body.find(attrs={'data-elementor-type': 'single-post'}) else 'page'
        # retirar elementos globales
        for sel in [{'class': 'trp-language-switcher'}, {'id': 'trp-floater-ls'}, {'class': 'trp-ald-popup'}, {'id': 'trp_ald_modal_container'},
                    {'class': 'skip-link'}, {'id': 'wpadminbar'}]:
            for t in body.find_all(attrs=sel): t.decompose()
        for t in body.find_all(id=re.compile(r'^trp_ald|^trp-ald')): t.decompose()
        for t in body.find_all(class_=re.compile(r'^trp_ald|^trp-ald')): t.decompose()
        # layout (cabecera/pie)
        lay = 'none'
        if header is not None and footer is not None:
            lay = 'default'
            hk = header.extract(); fk = footer.extract()
            if lang not in layouts or path == ({'es': '/'}.get(lang) or f'/{lang}/'):
                hs = clean(BeautifulSoup(str(hk), 'html.parser'), path, lang, [], None)
                for im in hs.find_all('img'):
                    im['loading'] = 'eager'; im.attrs.pop('srcset', None); im.attrs.pop('sizes', None)
                fs = clean(BeautifulSoup(str(fk), 'html.parser'), path, lang, [], None)
                layouts[lang] = {'header': str(hs), 'footer': str(fs), 'from': path}
        css, extra = page_css(b)
        ld = jsonld_of(b, warn)
        if custom_css is None and extra: custom_css = extra
        # contenido: todo lo que queda en body salvo el tema
        main_el = body.find(attrs={'data-elementor-type': re.compile('wp-page|single-page|single-post|wp-post|archive|search-results|error-404|single')})
        if main_el is None:
            main_el = body.find('main') or body
            warn.append('sin plantilla Elementor reconocida: se toma el <main>/<body>')
        container = main_el
        # hijos de primer nivel = bloques
        csoup = clean(BeautifulSoup(str(container), 'html.parser'), path, lang, warn, None)
        root = csoup.find(True)
        blocks = []
        tops = [c for c in root.children if getattr(c, 'name', None)] if root else []
        if kind == 'post' or len(tops) == 0:
            blocks.append({'type': 'seccion', 'html': ''.join(str(c) for c in root.children)})
        else:
            for c in tops:
                blocks.append({'type': 'seccion', 'html': str(c)})
        root_attrs = {'class': ' '.join(root.get('class', [])) if root else '', 'data-kt': root.get('data-kt', '') if root else ''}
        # SEO desde el inventario (literal)
        it = inv.get(unquote(path).lower()) or {}
        seo = it.get('seo') or {}
        r = CONTRACT[unquote(path).lower()]
        ogimg = None
        mm = re.search(r'<meta property="og:image" content="([^"]+)"', b)
        if mm: ogimg = rewrite_url(mm.group(1))
        title = seo.get('title') or H.unescape((re.search(r'<title>(.*?)</title>', b, re.S) or [None, ''])[1]).strip()
        desc = seo.get('description')
        if desc is None:
            md = re.search(r'<meta name="description" content="([^"]*)"', b)
            desc = H.unescape(md.group(1)) if md else ''
        robots = seo.get('robots') or ''
        mr = re.search(r'<meta name=["\']robots["\'] content=["\']([^"\']*)', b)
        if mr: robots = mr.group(1)
        pub_path = enc_path(path)
        alts = alt_of.get(unquote(path).lower())
        post = None
        if kind == 'post':
            es_path = unquote((alts or {}).get('es', path)).lower()
            esit = inv.get(es_path) or it
            post = {'date': esit.get('date') or it.get('date'), 'modified': esit.get('modified') or it.get('modified'),
                    'author': esit.get('author'), 'image': ogimg}
            mp = re.search(r'"datePublished":"([^"]+)"', b); mo = re.search(r'"dateModified":"([^"]+)"', b)
            if mp and not post['date']: post['date'] = mp.group(1)
            if mo and not post['modified']: post['modified'] = mo.group(1)
            ma = re.search(r'"author":\{"@type":"Person","name":"([^"]+)"', b) or re.search(r'"author":\{[^}]*"name":"([^"]+)"', b)
            if ma: post['authorName'] = H.unescape(ma.group(1))
        doc = {
            'path': pub_path, 'lang': lang, 'kind': kind, 'layout': lay,
            'seo': {'title': H.unescape(title or ''), 'description': H.unescape(desc or ''), 'canonical': DOM + pub_path,
                    'robots': robots, 'ogImage': ogimg},
            'alternates': alts, 'post': post, 'root': root_attrs,
            'css': ren_css(css), 'blocks': blocks, 'bodyClass': ' '.join(bodycls), 'jsonld': ld,
        }
        allh = ''.join(x['html'] for x in blocks)
        doc['needs'] = [n for n, rx in (('trustindex', r'ti-widget|trustindex'), ('blocks', r'wp-block-')) if re.search(rx, allh)]
        fid = hashlib.sha1(pub_path.encode()).hexdigest()[:10]
        slug = re.sub(r'[^a-z0-9]+', '-', unquote(path).lower()).strip('-')[:80] or 'home'
        os.makedirs(f'{outdir}/{lang}', exist_ok=True)
        json.dump(doc, open(f'{outdir}/{lang}/{slug}-{fid}.json', 'w'), ensure_ascii=False)
        if warn: LOG[path] = warn
        n += 1
        if n % 100 == 0: print(n, flush=True)
    os.makedirs(B + '/src/content/layout', exist_ok=True)
    for lg, l in layouts.items():
        json.dump(l, open(f'{B}/src/content/layout/{lg}.json', 'w'), ensure_ascii=False)
    open(B + '/migracion/wp_custom_css.css', 'w').write(ren_css(custom_css or ''))
    json.dump(MEDIA, open(B + '/migracion/media_needed.json', 'w'), indent=0, ensure_ascii=False)
    json.dump({k: sorted(v) for k, v in SEEN.items()}, open(B + '/migracion/media_seen.json', 'w'), indent=0, ensure_ascii=False)
    json.dump(LOG, open(B + '/migracion/convert_log.json', 'w'), indent=1, ensure_ascii=False)
    print('paginas', n, 'layouts', list(layouts), 'medios', len(MEDIA), 'paginas con avisos', len(LOG))

if __name__ == '__main__':
    main()
