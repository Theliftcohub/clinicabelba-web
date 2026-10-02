#!/usr/bin/env python3
"""Traducción de los posts y páginas que el WordPress servía (total o parcialmente) en español bajo un prefijo de idioma.

TranslatePress mostraba en /en/, /ru/… los textos sin traducir tal cual, en español, mezclados con los traducidos. La
migración los copió así. Este script separa el TEXTO del marcado para que la traducción no toque el HTML:

  scan [salida.csv]            → lista las páginas traducidas con fragmentos todavía en español (idénticos a un nodo de la
                                  página española equivalente, o con marcadores claros de español) y cuántas palabras son
  extract <lang> <slug> [--solo] → migracion/traducciones/<lang>/<slug>.json con {"src": [...]} (title, description, cada
                                  nodo de texto del cuerpo en orden y alt/title de imágenes; sin <style>/<script>).
                                  Con --solo solo van los fragmentos en español ("idx" = su posición en la lista completa)
                                  y, para los que forman parte de un encabezado mezclado, "ctx" = el encabezado español
                                  original entero, para traducir el encabezado con sentido.
  inject  <lang> <slug>        → lee el mismo archivo con "dst" (misma longitud que "src") y escribe la página con los
                                  textos sustituidos uno a uno. El marcado queda idéntico.
  check   <lang> <slug>        → comprueba longitud y que ningún texto largo quedó igual.

La URL no cambia. Toda traducción es de la agencia y se anota en NO_LITERAL.md; la clínica la revisa."""
import glob, json, os, re, sys
from urllib.parse import unquote

from bs4 import BeautifulSoup, NavigableString

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = B + '/migracion/traducciones'
SKIP_PARENTS = {'style', 'script', 'noscript', 'template'}

# marcadores de español que no son válidos en el idioma de destino (para fragmentos que no coinciden letra a letra con el ES)
_MARK = {'y', 'cirugía', 'cirugia', 'estética', 'para', 'los', 'las', 'más', 'pero', 'también', 'después', 'años', 'mujer', 'hombre',
         'precio', 'precios', 'cuerpo', 'rostro', 'pecho', 'senos', 'nariz', 'cuándo', 'cómo', 'qué', 'desde', 'hasta', 'mientras',
         'siempre', 'nuestros', 'nuestras', 'paciente', 'pacientes', 'resultados', 'semanas', 'meses', 'días', 'médico', 'médica',
         'criterio', 'cicatriz', 'recuperación', 'intervención', 'operación', 'quirófano', 'cirujano', 'cirujanos', 'tratamiento',
         'tratamientos', 'consulta', 'valoración', 'aumento', 'reducción', 'elevación', 'glúteos', 'brazos', 'muslos', 'párpados'}
_FUERTE = {'cirugía', 'cirugia', 'estética', 'precios', 'recuperación', 'valoración', 'quirófano', 'cirujano', 'cirujanos', 'glúteos',
           'párpados', 'muslos', 'cuándo', 'cómo', 'qué', 'después', 'también'}
_MARK_NO = {'ca': {'para', 'consulta', 'aumento'}, 'it': {'cirugia', 'consulta', 'aumento'}, 'fr': set(), 'en': set(), 'de': set(), 'nl': set(), 'ru': set(), 'uk': set()}
# textos que son iguales en todos los idiomas (marca, médicos, lugares, redes): nunca se marcan como «sin traducir»
_NOMBRES = re.compile(r"^(Cl[ií]nica Belba|Belba|Grupo Teknon|Teknon|Hospital Tres Torres|WhatsApp|Instagram|Facebook|YouTube|SECPRE|"
                      r"Barcelona|Badalona|Sabadell|Terrassa|L'Hospitalet|Eixample|Sarri[àa]-Sant Gervasi|Sant Cugat|V[ií]a Augusta[^A-Za-z]*|"
                      r"Dra?\.?\s+[A-ZÁÉÍÓÚ][\w\sáéíóúñ.·-]*|[\d\s+().,:€%/-]+|Lipovaser|Lipo ?HD|BRST|Mommy Makeover|Minimal Scar|BBL|Preservé|Motiva)$", re.I)


def find_doc(lang, slug):
    for f in glob.glob(B + f'/src/content/pages/{lang}/*.json'):
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        if unquote(d['path']).strip('/').split('/', 1)[-1] == slug:
            return f, d
    raise SystemExit(f'no encuentro la página {lang}/{slug}')


def _en_resenas(s):
    """Las reseñas de Google (widget Trustindex) y el honeypot son texto literal: no se traducen."""
    for p in s.parents:
        c = ' '.join(p.get('class') or []) if hasattr(p, 'get') else ''
        if 'ti-widget' in c or 'ti-review' in c or 'hp-field' in c:
            return True
    return False


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


def es_espanol(texto, lang):
    t = ' '.join(texto.split())
    if _NOMBRES.match(t):
        return False
    w = re.findall(r"[a-záéíóúñü]+", t.lower())
    if not w:
        return False
    marks = _MARK - _MARK_NO.get(lang, set())
    n = sum(1 for x in w if x in marks)
    fuerte = any(x in _FUERTE - _MARK_NO.get(lang, set()) for x in w)
    if '¿' in t or '¡' in t:
        return True
    if fuerte and len(w) >= 2:
        return True
    return len(w) >= 3 and n >= 2 and n / len(w) >= 0.1


def _lista(d):
    """Lista completa de textos (como extract) y, para cada índice, el encabezado (h1-h3) que lo contiene, si lo hay."""
    src = [d['seo'].get('title') or '', d['seo'].get('description') or '']
    heading_of = [None, None]
    for b in d['blocks']:
        S = BeautifulSoup(b['html'], 'html.parser')
        for s in text_nodes(S):
            if _en_resenas(s):
                continue
            src.append(str(s))
            h = s.find_parent(['h1', 'h2', 'h3'])
            heading_of.append(h)
        for img, a in img_attrs(S):
            src.append(img[a]); heading_of.append(None)
    return src, heading_of


def _headings(d):
    out = []
    for b in d['blocks']:
        S = BeautifulSoup(b['html'], 'html.parser')
        for h in S.find_all(['h1', 'h2', 'h3']):
            out.append((h.name, ' '.join(h.get_text(' ').split())))
    return out


def nodos_es(lang, d, es_docs):
    """Índices (en la lista de extract) de los fragmentos que siguen en español, más el contexto de encabezado."""
    es_path = (d.get('alternates') or {}).get('es')
    esd = es_docs.get(es_path)
    es_nodes = set()
    if esd:
        # el title y la description del español también cuentan como «sigue en español» si son idénticos
        for t_ in (esd['seo'].get('title') or '', esd['seo'].get('description') or ''):
            t_ = ' '.join(t_.split())
            if len(t_.split()) >= 2:
                es_nodes.add(t_)
        for b in esd['blocks']:
            for s_ in text_nodes(BeautifulSoup(b['html'], 'html.parser')):
                t = ' '.join(s_.split())
                if len(t.split()) >= 2 and not _NOMBRES.match(t):
                    es_nodes.add(t)
    src, heading_of = _lista(d)
    flag = set()
    for i, t in enumerate(src):
        tt = ' '.join(t.split())
        if (len(tt.split()) >= 3 and tt in es_nodes) or es_espanol(tt, lang):
            flag.add(i)
    # un encabezado con algún fragmento en español se traduce entero (p. ej. «Cirugía plástica <span>у мамы</span>»)
    ctx = {}
    es_heads = _headings(esd) if esd else []
    my_heads = _headings(d)
    for i in list(flag):
        h = heading_of[i]
        if h is None:
            continue
        for j, hh in enumerate(heading_of):
            if hh is h:
                flag.add(j)
        txt = ' '.join(h.get_text(' ').split())
        # el encabezado español equivalente: el que ocupa la misma posición entre los del mismo nivel, si cuadran en número
        mine = [t for n, t in my_heads if n == h.name]
        theirs = [t for n, t in es_heads if n == h.name]
        if txt in mine and len(mine) == len(theirs):
            ctx_txt = theirs[mine.index(txt)]
            for j, hh in enumerate(heading_of):
                if hh is h:
                    ctx[j] = ctx_txt
    return sorted(flag), src, ctx


def _es_docs():
    out = {}
    for g in glob.glob(B + '/src/content/pages/es/*.json'):
        with open(g, encoding='utf-8') as fh:
            e = json.load(fh)
        out[e['path']] = e
    return out


def scan(csv_out=None):
    docs = {}
    for f in glob.glob(B + '/src/content/pages/*/*.json'):
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        docs[d['path']] = d
    es_docs = {p: d for p, d in docs.items() if d['lang'] == 'es'}
    filas = []
    for p, d in sorted(docs.items()):
        if d['lang'] == 'es' or re.fullmatch(r'/\w\w/', p):
            continue
        idx, src, _ = nodos_es(d['lang'], d, es_docs)
        if not idx:
            continue
        palabras = sum(len(src[i].split()) for i in idx)
        filas.append((d['lang'], unquote(p), d.get('kind'), (d['seo'].get('robots') or '')[:7], len(idx), len(src), palabras, unquote(p).strip('/').split('/', 1)[-1]))
    print(f'{len(filas)} páginas traducidas con fragmentos en español · {sum(r[6] for r in filas)} palabras en total')
    for r in filas:
        print('  %s %-58s %-4s %-7s %3d/%3d fragmentos · %5d palabras' % r[:7])
    if csv_out:
        import csv
        with open(csv_out, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh); w.writerow(['lang', 'path', 'kind', 'robots', 'frag_es', 'frag_total', 'palabras', 'slug']); w.writerows(filas)
    return filas


def extract(lang, slug, solo=False):
    f, d = find_doc(lang, slug)
    src, _ = _lista(d)
    os.makedirs(f'{OUT}/{lang}', exist_ok=True)
    p = f"{OUT}/{lang}/{slug.replace('/', '__')}.json"
    datos = {'lang': lang, 'slug': slug, 'path': d['path'], 'src': src}
    if solo:  # solo los fragmentos que siguen en español: el traductor recibe menos y no toca lo ya traducido
        idx, _, ctx = nodos_es(lang, d, _es_docs())
        datos['idx'] = idx
        datos['src'] = [src[i] for i in idx]
        datos['ctx'] = {str(k): v for k, v in sorted(ctx.items()) if k in idx}
        datos['total'] = len(src)
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=0)
    print(f'{lang}/{slug}: {len(datos["src"])} textos, {sum(len(x.split()) for x in datos["src"])} palabras → {p}')


def inject(lang, slug):
    f, d = find_doc(lang, slug)
    p = f"{OUT}/{lang}/{slug.replace('/', '__')}.json"
    with open(p, encoding='utf-8') as fh:
        t = json.load(fh)
    src, dst = t['src'], t.get('dst')
    if not dst or len(dst) != len(src):
        raise SystemExit(f'{lang}/{slug}: dst ausente o con otra longitud ({len(dst or [])} ≠ {len(src)})')
    if 'idx' in t:  # modo solo: dst cubre únicamente los índices idx del listado completo; el resto no se toca
        full = [None] * t['total']
        for k, i in enumerate(t['idx']):
            full[i] = dst[k]
        dst = full
    if dst[0] is not None:
        d['seo']['title'] = dst[0]
    if d['seo'].get('description') and dst[1] is not None:
        d['seo']['description'] = dst[1]
    i = 2
    for b in d['blocks']:
        S = BeautifulSoup(b['html'], 'html.parser')
        for s in text_nodes(S):
            if _en_resenas(s):
                continue
            if dst[i] is not None:
                # conservar el espacio inicial/final del nodo original (separa palabras entre etiquetas)
                orig = str(s)
                lead = orig[:len(orig) - len(orig.lstrip())]; trail = orig[len(orig.rstrip()):]
                s.replace_with(NavigableString(lead + dst[i].strip() + trail))
            i += 1
        for img, a in img_attrs(S):
            if dst[i] is not None:
                img[a] = dst[i]
            i += 1
        b['html'] = str(S)
    assert i == len(dst), (i, len(dst))
    with open(f, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False)
    print(f'{lang}/{slug}: {sum(1 for x in dst if x is not None)} textos inyectados en {os.path.basename(f)}')


def check(lang, slug):
    p = f"{OUT}/{lang}/{slug.replace('/', '__')}.json"
    with open(p, encoding='utf-8') as fh:
        t = json.load(fh)
    src, dst = t['src'], t.get('dst') or []
    ok = len(dst) == len(src)
    iguales = sum(1 for a, b in zip(src, dst) if a.strip() == b.strip() and len(a.split()) > 3 and not _NOMBRES.match(a.strip()))
    print(f'{lang}/{slug}: longitud {"OK" if ok else "MAL"} ({len(dst)}/{len(src)}) · textos largos sin traducir: {iguales}')
    return ok and iguales == 0


if __name__ == '__main__':
    if sys.argv[1] == 'scan':
        scan(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        cmd, lang, slug = sys.argv[1:4]
        if cmd == 'extract':
            extract(lang, slug, solo='--solo' in sys.argv)
        else:
            {'inject': inject, 'check': check}[cmd](lang, slug)
