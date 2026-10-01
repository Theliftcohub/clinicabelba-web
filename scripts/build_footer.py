#!/usr/bin/env python3
"""Pie compacto para TODA la web, en los 9 idiomas (decisión Oscar 28/09: "todo con el mismo estilo" que la home nueva).
Sustituye el pie del WordPress (CTA + contacto + mapa + 27 enlaces) por: marca + dirección, 3 columnas de enlaces,
legal, logo UE y el botón flotante de WhatsApp literal. Los nombres de los enlaces salen del menú traducido del
WordPress (cabecera de cada idioma); el resto de textos, de home_i18n. Se ejecuta tras convert.py.
Anota el cambio en NO_LITERAL.md."""
import json, html, re, os, sys, datetime
from urllib.parse import unquote
from bs4 import BeautifulSoup
B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raíz del repo (o BELBA_ROOT)
sys.path.insert(0, B + '/scripts')
from home_i18n import T

I18N = json.load(open(B + '/migracion/i18n-map.json'))
e = html.escape
YEAR = datetime.date.today().year
NAP = {'dir1': 'Via Augusta, 281, planta 4A', 'dir2': '08017 Barcelona', 'tel': '+34 613 16 34 47', 'tel_href': 'tel:34613163447',
       'wa': 'https://api.whatsapp.com/send?phone=34613163447', 'email': 'info@clinicabelba.com',
       'maps': 'https://www.google.com/maps/place/Cirujano+Pl%C3%A1stico+Barcelona+-+Cl%C3%ADnica+Belba/@41.3975168,2.1273671,17z/data=!3m1!4b1!4m6!3m5!1s0x12a4a3ee246f334d:0x2588af9f9008aa3b!8m2!3d41.3975128!4d2.129942!16s%2Fg%2F11h60f9631?entry=ttu'}

def href(es_path, lang):
    return I18N.get(es_path, {}).get(lang) or es_path

def menu_labels(header_html):
    out = {}
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', header_html, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if t and m.group(1) not in out:
            out[unquote(m.group(1)).lower()] = t
    return out

def label(labels, es_path, lang, fallback):
    return labels.get(unquote(href(es_path, lang)).lower(), fallback)

def render(lang, header_html, wa_html):
    t = T.get(lang, T['es'])
    lb = menu_labels(header_html)
    L = lambda p, fb: e(label(lb, p, lang, fb))
    H = lambda p: href(p, lang)
    home = H('/')
    cir = [('/cirugia-de-la-mama/', 'Cirugía de la mama'), ('/cirugia-corporal/', 'Cirugía corporal'), ('/cirugia-facial/', 'Cirugía facial'), ('/cirugia-intima/', 'Cirugía intima')]
    cli = [('/quienes-somos/', 'Quienes somos'), ('/cirujanos-plasticos-barcelona/', 'Cirujanos plásticos Barcelona'), ('/guia-del-paciente/', 'Guía del paciente'),
           ('/test-paciente/', 'Test paciente'), ('/consulta-online/', 'Consulta online'), ('/blog/', 'Blog')]
    return f'''<footer class="hn-footer">
  <div class="hn-wrap hn-footer__grid">
    <div class="hn-footer__brand">
      <a href="{home}"><img src="/images/2024/12/clinica-belba-200.webp" alt="Clinica Cirugía Plástica Barcelona" width="192" height="58" loading="lazy" decoding="async"></a>
      <p>{e(t['f_brand'])}</p>
      <p><a href="{NAP['maps']}" target="_blank" rel="noopener">{e(NAP['dir1'])}, {e(NAP['dir2'])}</a></p>
    </div>
    <div><p class="hn-footer__h">{e(t['f_cirugia'])}</p><ul>
      {''.join(f'<li><a href="{H(p)}">{L(p, fb)}</a></li>' for p, fb in cir)}
      <li><a href="{H('/precio-cirugia-estetica-barcelona/')}">{e(t['f_precios'])}</a></li>
    </ul></div>
    <div><p class="hn-footer__h">{e(t['f_clinica'])}</p><ul>
      {''.join(f'<li><a href="{H(p)}">{L(p, fb)}</a></li>' for p, fb in cli)}
    </ul></div>
    <div><p class="hn-footer__h">{e(t['f_contacto'])}</p><ul>
      <li><a href="{NAP['tel_href']}">{e(NAP['tel'])}</a></li>
      <li><a href="{NAP['wa']}" target="_blank" rel="noopener">{e(t['f_wa'])}</a></li>
      <li><a href="mailto:{NAP['email']}">{NAP['email']}</a></li>
      <li>{e(t['horario'])}</li>
    </ul></div>
  </div>
  <div class="hn-wrap hn-footer__bottom">
    <p>{e(t['f_copy'].format(y=YEAR))}</p>
    <ul class="hn-footer__legal"><li><a href="{H('/aviso-legal/')}">{e(t['f_legal'])}</a></li><li><a href="{H('/politica-de-cookies/')}">{e(t['f_cookies'])}</a></li><li><a href="{H('/politica-de-privacidad/')}">{e(t['f_priv'])}</a></li><li><a href="/sitemap.xml">{e(t['f_sitemap'])}</a></li></ul>
  </div>
  <div class="hn-wrap hn-footer__eu-row"><img class="hn-footer__eu" src="/images/2022/12/financiado-por-la-union-europea.webp" alt="Financiado por la Unión Europea - NextGenerationEU." width="250" height="63" loading="lazy" decoding="async"></div>
</footer>
<div class="k k-135 kt-footer" data-kt="footer">{wa_html}</div>'''

def main():
    rows = []
    for f in sorted(os.listdir(B + '/src/content/layout')):
        if not f.endswith('.json'): continue
        lang = f[:-5]
        p = B + '/src/content/layout/' + f
        L = json.load(open(p))
        if L.get('footer_wp') is None:
            L['footer_wp'] = L['footer']  # se conserva el original por si hay que volver atrás
        S = BeautifulSoup(L['footer_wp'], 'html.parser')
        wa = S.select_one('section.k-element-1a3720f')
        L['footer'] = render(lang, L['header'], str(wa) if wa else '')
        # Selector de idioma en la cabecera (arriba a la derecha, tras el menú): marca <!--LS--> que [...slug].astro sustituye por el componente
        if '<!--LS-->' not in L['header']:
            Hs = BeautifulSoup(L['header'], 'html.parser')
            nav = Hs.select_one('.k-widget-nav-menu')
            if nav:
                nav.insert_after(BeautifulSoup('<!--LS-->', 'html.parser'))
                L['header'] = str(Hs)
        json.dump(L, open(p, 'w'), ensure_ascii=False)
        rows.append('| %s | pie de página | pie del WordPress (CTA + contacto + mapa + 27 enlaces) | pie compacto: marca, 3 columnas de enlaces, legal, logo UE, WhatsApp | decisión Oscar 28/09: toda la web con el estilo de la home nueva; textos traducidos por la agencia, revisar |' % href('/', lang))
    nl = B + '/NO_LITERAL.md'
    cur = open(nl).read() if os.path.exists(nl) else ''
    with open(nl, 'a') as fo:
        for r in rows:
            if r + '\n' not in cur: fo.write(r + '\n')
    print('pie compacto en', len(rows), 'idiomas')

if __name__ == '__main__':
    main()
