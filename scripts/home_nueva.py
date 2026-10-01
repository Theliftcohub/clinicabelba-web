#!/usr/bin/env python3
"""Home nueva (portada en 9 idiomas; v3 «clínica premium clara», 30/09) a partir del diseño de Figma Make de Oscar (28/09),
con TODOS los textos, datos, fotos y reseñas sacados de la web actual (nada inventado).
Cambios respecto al diseño, decididos con Oscar: hero con foto real de quirófano en vez de la modelo;
selector Mujer / Hombre que filtra las tarjetas de procedimientos; sin cifras ni reseñas inventadas;
médicos, dirección y teléfono reales; formulario nativo (sin Typeform)."""
import json, glob, html, re, os, sys, io, functools
from bs4 import BeautifulSoup
open = functools.partial(io.open, encoding='utf-8')  # en Windows open() usa cp1252 por defecto
B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raíz del repo (o BELBA_ROOT)
sys.path.insert(0, B + '/scripts')
import forms_native
from home_i18n import T
I18N = json.load(open(B + '/migracion/i18n-map.json'))
def href(es_path, lang):
    return I18N.get(es_path, {}).get(lang) or es_path
def menu_labels(header_html):
    from urllib.parse import unquote
    out = {}
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', header_html, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if t: out.setdefault(unquote(m.group(1)).lower(), t)
    return out

home = json.load(open(glob.glob(B + '/src/content/pages/es/home-*.json')[0]))
H = ''.join(b['html'] for b in home['blocks'])
S = BeautifulSoup(H, 'html.parser')
def text_after(h3_text):
    h3 = S.find(lambda t: t.name in ('h2', 'h3') and t.get_text(strip=True) == h3_text)
    return h3
e = html.escape

# ---------- datos literales de la web actual ----------
HERO_H1 = 'Clínica de cirugía plástica en Barcelona'
HERO_SUB = 'Acompañamiento médico real antes, durante y después de la cirugía'
HERO_P = ('En Clínica Belba entendemos la cirugía plástica como un proceso médico, no como un producto. '
          'Por eso, el mismo cirujano que te valora es quien te opera y quien te acompaña durante todo el postoperatorio, '
          'en un entorno hospitalario de referencia en Barcelona.')
CTA = 'Solicita tu valoración médica'
FILO_H = '¿Por qué Clínica Belba no es una clínica comercial?'
FILO_P = ['En Clínica Belba no trabajamos con cirugías estándar ni decisiones precipitadas.',
          'Cada paciente es valorado de forma individual y solo recomendamos una intervención si realmente es la opción adecuada.']
FILO_LIST = ['El mismo cirujano te valora, te opera y realiza el seguimiento',
             'El postoperatorio forma parte del tratamiento',
             'Operamos en entornos hospitalarios de referencia en Barcelona']
FILO_FIN = 'Nuestro compromiso es médico, no comercial.'
PROC_H = 'Procedimientos y cirugías plásticas en Barcelona'
PROC_P = ('En Clínica Belba realizamos cirugías plásticas y reparadoras en Barcelona siempre tras una valoración médica personalizada. '
          'Nuestro objetivo no es transformar, sino mejorar de forma natural, respetando la anatomía y las expectativas reales de cada paciente.')
# Tarjetas: las de la home actual (mujer) + páginas existentes para hombre
# Tarjetas: las de la home actual (mujer) + páginas existentes para hombre.
# Fotos (30/09, petición de Nicols): la imagen propia de la página de destino (versión -800 ya generada), en vez de los iconos de línea.
CARDS_MUJER = [
    ('Corporal', '/lipo-vaser/', '/images/2026/06/seccion_bg-800.webp'),
    ('Liposucción', '/liposuccion-barcelona/', '/images/thumbs/liposuccion-barcelona-rh2s3fr124vdy0y4by4q77hk3kznbneg4c7blqzcp4.webp'),
    ('Piernas', '/lifting-de-muslos/', '/images/2026/03/Lifting-de-muslos-800.webp'),
    ('Senos', '/aumento-pecho-barcelona/', '/images/2026/01/aumento-de-pecho-en-barcelona-800.webp'),
    ('Rostro', '/lifting-facial-barcelona/', '/images/2026/03/Lifting-facial-BELBA-800.webp'),
    ('Brazos', '/lifting-de-brazos/', '/images/2026/03/Lifting-de-brazos-800.webp'),
]
CARDS_HOMBRE = [
    ('Ginecomastia', '/ginecomastia-barcelona/', '/images/2025/11/ginecomastia-barcelona-2-800.webp'),
    ('Rinoplastia', '/rinoplastia-barcelona/', '/images/2026/06/Rinoplastia-en-hombres-800.webp'),
    ('Lipo HD', '/liposuccion-de-alta-definicion/', '/images/2025/11/liposuccion-alta-definicion-barcelona.webp'),
    ('Blefaroplastia', '/blefaroplastia/', '/images/2026/03/BLEFAROPLASTIA-SUPERIOR-800.webp'),
    ('Otoplastia', '/otoplastia/', '/images/thumbs/descarga-20-rkehqg2z3vfiyr9drlgx6wf7q74nzr9uiqk5wuyqyk.webp'),
    ('Mentoplastia', '/mentoplastia-barcelona/', '/images/thumbs/mentoplastia-Barcelona-rifb4486vi7jabtk95kvhyj8hsz56pzbe7akd1dn24.webp'),
]
TRAT_H = 'Nuestros Tratamientos de Cirugía plástica y reparadora'
TRAT_SUB = 'No es solo un cambio. Es sentirte bien contigo.'
TRAT = [
    ('Cirugia de la mama', '/cirugia-de-la-mama/', 'Naturalidad, seguridad y acompañamiento médico real.', '/images/2023/05/cirugia-de-pecho.webp',
     [('Aumento de pecho', '/aumento-pecho-barcelona/'), ('Aumento de pecho Preservé', '/aumento-pecho-preserve/'), ('Aumento de pecho Técnica BRST', '/aumento-de-pecho-tecnica-brst/'),
      ('Elevación mamaria (mastopexia)', '/elevacion-de-mama/'), ('Reducción mamaria', '/reduccion-de-mama/'), ('Recambio de prótesis', '/recambio-de-protesis/')]),
    ('Cirugía corporal', '/cirugia-corporal/', 'Resultados naturales con criterio médico.', '/images/2026/06/bg_belba-1.webp',
     [('Cirugía Liposucción', '/liposuccion-barcelona/'), ('Abdominoplastia', '/abdominoplastia-barcelona/'), ('Mommy Makeover', '/mommy-makeover-barcelona/'), ('Lipovaser en Barcelona', '/lipo-vaser/'),
      ('Ginecomastia en Barcelona', '/ginecomastia-barcelona/'), ('Aumento de Glúteos', '/aumento-de-gluteos-barcelona/'), ('Remodelacion Costal', '/remodelacion-costal/')]),
    ('Cirugía facial', '/cirugia-facial/', 'El rostro no se cambia, se cuida.', '/images/2026/06/facial_02.webp',
     [('Rinoplastia Ultrasonica en Barcelona', '/rinoplastia-barcelona/'), ('Blefaroplastia', '/blefaroplastia/'), ('Lifting facial', '/lifting-facial-barcelona/'), ('Mini Lifting facial en Barcelona', '/mini-lifting-facial-barcelona/'),
      ('Lobuloplastia Barcelona', '/lobuloplastia-barcelona/'), ('Otoplastia en Barcelona', '/otoplastia/'), ('Mentoplastia Barcelona', '/mentoplastia-barcelona/')]),
    ('Cirugía íntima', '/cirugia-intima/', '', '/images/2023/05/cirugia-intima.webp',
     [('Labioplastia', '/labioplastia/'), ('Vaginoplastia', '/vaginoplastia/'), ('Himenoplastia', '/himenoplastia-barcelona/')]),
]
HOSP_H = 'Clínica de cirugía plástica en Barcelona con entorno hospitalario de referencia'
HOSP_SUB = 'Ubicación, seguridad médica y acompañamiento real'
HOSP_P = ('Nuestra clínica se encuentra en Barcelona ubicada en Via Augusta, 281, planta 4A y trabaja en colaboración con centros hospitalarios premium del '
          '<a href="/cirujanos-plasticos-barcelona/">Grupo Teknon</a>, garantizando los máximos estándares de seguridad médica. '
          'Atendemos a pacientes de Barcelona y de toda España que buscan una clínica de cirugía plástica en Barcelona con criterio médico, experiencia y seguimiento real.')
EQUIPO_H = 'Nuestro equipo de cirujanos'
EQUIPO_P = ['El Doctor será tu cirujano en cada fase del proceso.', 'No delegamos valoraciones, ni seguimientos, ni postoperatorios.',
            'El mismo especialista te acompaña antes, durante y después de la cirugía para asegurar un resultado natural, seguro y coherente con tus expectativas.']
DOCS = [
    ('Dr. Mike Dewever', 'Cirujano plástico, reparador y estético', '/images/2026/05/mike.webp', '/drdewevercirugiaplastica/',
     '«La mejor cirugía es la que se decide con calma, criterio médico y expectativas realistas.»',
     'Especialista en cirugía corporal y facial con un enfoque preciso y respetuoso con la anatomía de cada paciente. En el ámbito de la cirugía mamaria, aplica técnicas avanzadas de mamoplastia que priorizan la preservación de tejidos, la naturalidad del resultado y la seguridad durante todo el proceso, con seguimiento médico continuo desde la primera consulta hasta la última revisión.'),
    ('Dra. Marel Gómez', 'Especialista en procedimientos de estética facial y corporal', '/images/2026/05/marel.webp', '/cirujanos-plasticos-barcelona/',
     '«Cada paciente es única. Escuchar y acompañar forma parte del resultado.»',
     'Especializada en cirugía mamaria estética con un enfoque personalizado y orientado a resultados naturales. Su prioridad es que cada decisión de operación de pecho esté completamente informada, cuidando tanto el resultado estético como el bienestar y la tranquilidad de la paciente antes, durante y después de la intervención.'),
    ('Dra. Laura Torrano Romero', 'Cirujana plástica, reparadora y estética', '/images/2026/05/laura.webp', '/cirujanos-plasticos-barcelona/', '',
     'Especialista en cirugía plástica y reconstructiva con experiencia específica en unidades de mama y linfedema en hospitales de Barcelona. Formada en la Universidad de Navarra con estancias internacionales en Stanford y Mayo Clinic. Doctoranda en microcirugía y autora de publicaciones científicas en el campo de la cirugía mamaria reconstructiva. Una de las pocas cirujanas plásticas en España con formación combinada en cirugía mamaria estética y oncológica.'),
    ('Dr. Félix Chavarría', 'Cirujano plástico, reparador y estético', '/images/2026/06/Dr-felix.webp', '/drfelixchavarriacirugiaplastica/',
     '«No se trata de hacer más cirugía, sino de hacer la adecuada.»',
     'Con amplia experiencia en cirugía plástica y reparadora, destaca por su criterio médico y su enfoque conservador cuando el caso lo permite. En mamoplastia, trabaja con técnicas que reducen el impacto quirúrgico, minimizan el tiempo de recuperación y favorecen una evolución postoperatoria controlada, siempre dentro del entorno hospitalario seguro del Grupo Teknon y el Hospital Tres Torres.'),
]
# palabras del H1 que van en turquesa (solo un <em>, el texto no cambia)
HL = {'es': 'cirugía plástica', 'ca': 'cirurgia plàstica', 'en': 'Plastic surgery', 'fr': 'chirurgie plastique', 'de': 'plastische Chirurgie',
      'it': 'chirurgia plastica', 'nl': 'plastische chirurgie', 'ru': 'пластической хирургии', 'uk': 'пластичної хірургії'}
import datetime
YEAR = datetime.date.today().year
NAP = {'dir1': 'Via Augusta, 281, planta 4A', 'dir2': '08017 Barcelona', 'tel': '+34 613 16 34 47', 'tel_href': 'tel:34613163447',
       'wa': 'https://api.whatsapp.com/send?phone=34613163447', 'email': 'info@clinicabelba.com',
       'horario': 'Lunes a jueves: 10:00–14:00 y 16:00–20:00 · Viernes: 10:00–14:00',
       'maps': 'https://www.google.com/maps/place/Cirujano+Pl%C3%A1stico+Barcelona+-+Cl%C3%ADnica+Belba/@41.3975168,2.1273671,17z/data=!3m1!4b1!4m6!3m5!1s0x12a4a3ee246f334d:0x2588af9f9008aa3b!8m2!3d41.3975128!4d2.129942!16s%2Fg%2F11h60f9631?entry=ttu',
       'embed': 'https://maps.google.com/maps?q=Clinica%20Belba&t=m&z=14&output=embed&iwloc=near'}
# Reseñas reales: el widget de Google (Trustindex) tal cual está en la home actual
ti = S.find(class_='ti-widget')
TRUSTINDEX = re.sub(r'data-css-url="[^"]*"', 'data-css-url="/css/trustindex-google-widget.css"', str(ti.find_parent(class_='k-widget-container') or ti))
ti_head = re.search(r'A base de\s*(\d+)\s*rese', BeautifulSoup(TRUSTINDEX, 'html.parser').get_text(' ', strip=True))
N_RESENAS = ti_head.group(1) if ti_head else ''

# Botón flotante de WhatsApp: el mismo widget literal del pie del WordPress
_lay = json.load(open(B + '/src/content/layout/es.json'))
_wa = BeautifulSoup(_lay['footer'], 'html.parser').select_one('section.k-element-1a3720f')
WA_FLOTANTE = str(_wa) if _wa else ''

# ---------- Home v3 «clínica premium clara» (decisión Nicols 30/09 noche, elegida con AskUserQuestion) ----------
# Fondos blanco/marfil, fotos grandes a sangre, tarjetas con sombra suave, acentos turquesa, títulos Montserrat 800.
# Sliders: hero a pantalla completa (fundido + zoom lento), carrusel de procedimientos (flechas + arrastre),
# tratamientos con foto de fondo y lista al pasar el ratón. Textos, enlaces, formularios y medición: literales.
IMG = {
    'hero': ['/images/2026/04/Primera-consulta-de-cirugia-estetica-BELBA.webp',
             '/images/2026/03/Honorarios-medicos-quirofano-y-anestesia.webp',
             '/images/2025/12/centro-medico-teknon-1.webp'],
    'filo': '/images/2026/04/Primera-consulta-de-cirugia-estetica-BELBA-800.webp',
    'filo_small': '/images/2026/03/Honorarios-medicos-quirofano-y-anestesia.webp',
    'hosp_big': '/images/2025/12/centro-medico-teknon-1.webp',
    'hosp_small': '/images/2025/12/edificio-via-augusta.webp',
}
# Tarjetas de procedimientos: la foto propia de la página de destino (versión -800), no las miniaturas de 119-214 px de la portada del WP
CARD_IMG = {
    '/lipo-vaser/': '/images/2026/06/corporal_bg-800.webp',
    '/liposuccion-barcelona/': '/images/2026/06/seccion_bg-800.webp',
    '/lifting-de-muslos/': '/images/2026/04/cirugia-de-lifting-de-muslos-800.webp',
    '/aumento-pecho-barcelona/': '/images/2026/03/aumento-de-pecho-brst-barcelona.webp',
    '/lifting-facial-barcelona/': '/images/2026/03/lifting-facial-800.webp',
    '/lifting-de-brazos/': '/images/2026/04/lifting-de-brazos-800.webp',
    '/ginecomastia-barcelona/': '/images/2026/04/ginecomastia-precio-barcelona.webp',
    '/rinoplastia-barcelona/': '/images/2026/06/Rinoplastia-en-hombre-800.webp',
    '/liposuccion-de-alta-definicion/': '/images/2025/11/liposuccion-alta-definicion-barcelona-800.webp',
    '/blefaroplastia/': '/images/2026/06/valoracion-blefaroplastia-800.webp',
    '/otoplastia/': '/images/thumbs/descarga-20-rkehqg2z3vfiyr9drlgx6wf7q74nzr9uiqk5wuyqyk.webp',
    '/mentoplastia-barcelona/': '/images/2026/01/objetivo-mentoplastia-800.webp',
}
TRAT_IMG = {'/cirugia-de-la-mama/': '/images/2023/05/cirugia-de-pecho.webp', '/cirugia-corporal/': '/images/2026/06/bg_belba-1-800.webp',
            '/cirugia-facial/': '/images/2026/06/facial_02-800.webp', '/cirugia-intima/': '/images/thumbs/cirugia-intima-rlo7mqgfd64x4s5yfmxdbvcxmccsf7yq64nclbhh44.webp'}
# nombre de la clínica tal como aparece en el H2 de la filosofía (solo para colorearlo; el texto no cambia)
BRAND = {'ru': 'клиника Belba', 'uk': 'клініка Belba'}


def hl(text, phrase):
    """Devuelve el texto escapado con la primera aparición de `phrase` (sin distinguir mayúsculas) dentro de <em>."""
    if not phrase:
        return e(text)
    i = text.lower().find(phrase.lower())
    if i < 0:
        return e(text)
    return e(text[:i]) + '<em>' + e(text[i:i + len(phrase)]) + '</em>' + e(text[i + len(phrase):])


def card(t, href, img, n):
    return (f'<a class="hn-card" href="{href}"><img src="{img}" alt="{e(t)}" loading="lazy" decoding="async">'
            f'<span class="hn-card__n" aria-hidden="true">{n:02d}</span><span class="hn-card__t">{e(t)}</span><span class="hn-card__go" aria-hidden="true">→</span></a>')


def body(lang, t, lb, ti_html, n_res, page_path):
    """t = textos del idioma (home_i18n.T), lb = etiquetas del menú traducido (href -> texto)."""
    H = lambda p: href(p, lang)
    L = lambda p, fb: lb.get(__import__('urllib.parse').parse.unquote(H(p)).lower(), fb)
    ui = forms_native.UI.get(lang, forms_native.UI['es'])
    form = forms_native.render('iOSo1PBX', lang, page_path, uid='hnform', intro=False)
    form_hero = forms_native.render('iOSo1PBX', lang, page_path, uid='hero', compact=True,
                                    pre_steps=[(t['pre_q'], [('Mujer', t['mujer']), ('Hombre', t['hombre'])], 'sel_persona')])
    todas = list(zip(t['cards_m'], CARDS_MUJER)) + list(zip(t['cards_h'], CARDS_HOMBRE))
    cards = ''.join(card(n, H(h), CARD_IMG.get(h, img), i + 1) for i, (n, (_, h, img)) in enumerate(todas))
    trat = ''.join(
        f'<article class="hn-trat"><a class="hn-trat__bg" href="{H(hr)}" tabindex="-1" aria-hidden="true"><img src="{TRAT_IMG.get(hr, img)}" alt="{e(L(hr, name))}" loading="lazy" decoding="async"></a>'
        f'<div class="hn-trat__body"><h3><a href="{H(hr)}">{e(L(hr, name))}</a></h3>' + (f'<p class="hn-trat__claim">{e(claim)}</p>' if claim else '') +
        '<ul>' + ''.join(f'<li><a href="{H(h2)}">{e(L(h2, n))}</a></li>' for n, h2 in items) + '</ul></div></article>'
        for (name, hr, _, img, items), claim in zip(TRAT, t['claims']))
    docs = ''.join(
        f'<article class="hn-doc"><div class="hn-doc__media"><a href="{H(hr)}"><img src="{img}" alt="{e(n)}" loading="lazy" decoding="async"></a>'
        f'<div class="hn-doc__over"><h3><a href="{H(hr)}">{e(n)}</a></h3><p class="hn-doc__rol">{e(rol)}</p></div></div>'
        f'<div class="hn-doc__body">' + (f'<p class="hn-doc__cita">{e(cita)}</p>' if cita else '') + f'<p class="hn-doc__bio">{e(bio)}</p></div></article>'
        for (n, _, img, hr, _, _), (rol, cita, bio) in zip(DOCS, t['docs']))
    eb = t['hero_eyebrow'].rsplit(' · ', 1)
    eyebrow = (e(eb[0]) + ' · <span class="hn-badge">' + e(eb[1]) + '</span>') if len(eb) == 2 else e(t['hero_eyebrow'])
    hlp = HL.get(lang)
    avatars = ''.join(f'<img src="{img}" alt="" loading="lazy" decoding="async">' for (_, _, img, _, _, _) in DOCS)
    hosp_p = e(t['hosp_p']).replace('{teknon}', f'<a href="{H("/cirujanos-plasticos-barcelona/")}">{e(t["teknon"])}</a>')
    filo_items = ''.join(f'<li><span class="hn-steps__n" aria-hidden="true"></span><p>{e(x)}</p></li>' for x in t['filo_list'])
    slides = ''.join(f'<img src="{src}" alt="" class="{"is-on" if i == 0 else ""}" loading="{"eager" if i == 0 else "lazy"}" decoding="async"{" fetchpriority=\"high\"" if i == 0 else ""}>' for i, src in enumerate(IMG['hero']))
    dots = ''.join(f'<button type="button" class="hn-dot{" is-on" if i == 0 else ""}" aria-label="{i + 1}"></button>' for i in range(len(IMG['hero'])))
    return f"""
<div class="hn">
<section class="hn-hero">
  <div class="hn-hero__bg" data-slider aria-hidden="true">{slides}</div>
  <div class="hn-hero__shade" aria-hidden="true"></div>
  <div class="hn-wrap hn-hero__grid">
    <div class="hn-hero__txt">
      <p class="hn-eyebrow hn-eyebrow--hero">{eyebrow}</p>
      <h1>{hl(t['hero_h1'], hlp)}</h1>
      <p class="hn-hero__sub">{e(t['hero_sub'])}</p>
      <p class="hn-hero__p">{e(t['hero_p'])}</p>
      <p class="hn-hero__actions"><a class="hn-cta hn-cta--lg" href="#valoracion">{e(t['cta'])}<span class="hn-arrow" aria-hidden="true">→</span></a><a class="hn-hero__tel" href="{NAP['tel_href']}"><span class="hn-tel-ico" aria-hidden="true"></span>{e(NAP['tel'])}</a></p>
      <div class="hn-hero__trust">
        <a class="hn-trust hn-trust--g" href="#resenas"><span class="hn-g" aria-hidden="true">G</span><span class="hn-stars" aria-hidden="true">★★★★★</span><span>{e(t['proof'].format(n=n_res))}</span></a>
        <a class="hn-trust" href="{H('/cirujanos-plasticos-barcelona/')}"><span class="hn-avatars" aria-hidden="true">{avatars}</span><span>{e(t['equipo_h'])}</span></a>
        <a class="hn-trust hn-trust--link" href="#procedimientos">{e(t['ver_proc'])}</a>
      </div>
      <nav class="hn-pills" aria-label="{e(t['areas'])}">
        <a href="{H('/cirugia-facial/')}">{e(L('/cirugia-facial/', 'Cirugía facial'))}</a><a href="{H('/cirugia-de-la-mama/')}">{e(L('/cirugia-de-la-mama/', 'Cirugía de la mama'))}</a><a href="{H('/cirugia-corporal/')}">{e(L('/cirugia-corporal/', 'Cirugía corporal'))}</a><a href="{H('/cirugia-intima/')}" data-only="mujer">{e(L('/cirugia-intima/', 'Cirugía íntima'))}</a><a href="{H('/ginecomastia-barcelona/')}" data-only="hombre">{e(t['gineco'])}</a>
      </nav>
    </div>
    <div class="hn-hero__form" id="valoracion">
      <p class="hn-hero__formtitle">{e(t['cta'])}</p>
      <p class="hn-hero__formsub">{e(t['form_sub'])}</p>
      {form_hero}
    </div>
  </div>
  <div class="hn-wrap hn-hero__foot">
    <div class="hn-dots">{dots}</div>
    <span class="hn-logos"><span>{e(t['logos'])}</span><img src="/images/2025/12/quiron-salud-tekon.webp" alt="Quirónsalud y Centro Médico Teknon" loading="lazy" decoding="async"></span>
  </div>
</section>

<section class="hn-filo">
  <div class="hn-wrap hn-filo__grid">
    <div class="hn-filo__media">
      <img class="hn-filo__big" src="{IMG['filo']}" alt="{e(t['filo_alt'])}" loading="lazy" decoding="async">
      <img class="hn-filo__small" src="{IMG['filo_small']}" alt="" loading="lazy" decoding="async">
    </div>
    <div class="hn-filo__txt">
      <p class="hn-eyebrow">{e(t['filo_eyebrow'])}</p>
      <h2>{hl(t['filo_h'], BRAND.get(lang, 'Clínica Belba'))}</h2>
      {''.join(f'<p class="hn-lead">{e(p)}</p>' for p in t['filo_p'])}
      <ol class="hn-steps">{filo_items}</ol>
      <p class="hn-strong">{e(t['filo_fin'])}</p>
    </div>
  </div>
</section>

<section class="hn-proc" id="procedimientos" data-carousel>
  <div class="hn-wrap">
    <div class="hn-proc__head">
      <div><p class="hn-eyebrow">{e(t['proc_eyebrow'])}</p><h2>{e(t['proc_h'])}</h2></div>
      <div class="hn-proc__tools"><p class="hn-lead">{e(t['proc_p'])}</p>
        <div class="hn-nav"><button type="button" class="hn-arrowbtn" data-prev aria-label="{e(ui[1])}"><span aria-hidden="true">←</span></button><button type="button" class="hn-arrowbtn" data-next aria-label="{e(ui[0])}"><span aria-hidden="true">→</span></button></div>
      </div>
    </div>
  </div>
  <div class="hn-track">{cards}</div>
</section>

<section class="hn-trats">
  <div class="hn-wrap">
    <div class="hn-trats__head">
      <div><p class="hn-eyebrow">{e(t['trat_eyebrow'])}</p><h2>{hl(t['trat_h'], hlp)}</h2></div>
      <p class="hn-lead">{e(t['trat_sub'])}</p>
    </div>
    <div class="hn-trats__grid">{trat}</div>
  </div>
</section>

<section class="hn-hosp">
  <div class="hn-wrap hn-hosp__grid">
    <div class="hn-hosp__txt">
      <p class="hn-eyebrow">{e(t['hosp_eyebrow'])}</p>
      <h2>{hl(t['hosp_h'], hlp)}</h2>
      <h3>{e(t['hosp_sub'])}</h3>
      <p>{hosp_p}</p>
      <a class="k-button k-button-link k-size-sm hn-cta" href="{H('/consulta-online/')}"><span class="k-button-text">{e(t['cita'])}</span></a>
    </div>
    <div class="hn-hosp__media">
      <img class="hn-hosp__big" src="{IMG['hosp_big']}" alt="{e(t['hosp_alt'])}" loading="lazy" decoding="async">
      <img class="hn-hosp__small" src="{IMG['hosp_small']}" alt="" loading="lazy" decoding="async">
    </div>
  </div>
</section>

<section class="hn-equipo">
  <div class="hn-wrap">
    <div class="hn-equipo__head">
      <div><p class="hn-eyebrow">{e(t['equipo_eyebrow'])}</p><h2>{e(t['equipo_h'])}</h2></div>
      <p class="hn-lead">{e(t['equipo_p'])}</p>
    </div>
    <div class="hn-docs">{docs}</div>
  </div>
</section>

<section class="hn-resenas" id="resenas">
  <div class="hn-wrap">
    <div class="hn-resenas__head">
      <div><p class="hn-eyebrow">{e(t['res_eyebrow'])}</p><h2>{e(t['res_h'])}</h2></div>
      <a class="hn-trust hn-trust--g hn-trust--lg" href="{NAP['maps']}" target="_blank" rel="noopener"><span class="hn-g" aria-hidden="true">G</span><span class="hn-stars" aria-hidden="true">★★★★★</span><span>{e(t['proof'].format(n=n_res))}</span></a>
    </div>
    {ti_html}
  </div>
</section>

<section class="hn-form" id="contacto-rapido">
  <div class="hn-wrap hn-form__grid">
    <div class="hn-form__txt">
      <p class="hn-eyebrow">{e(t['form_eyebrow'])}</p>
      <h2>{e(t['form_h'])}</h2>
      <p class="hn-lead">{e(t['form_p'])}</p>
      <ul class="hn-nap">
        <li class="hn-nap__dir"><span><a href="{NAP['maps']}" target="_blank" rel="noopener">{e(NAP['dir1'])}, {e(NAP['dir2'])}</a></span></li>
        <li class="hn-nap__tel"><span><a href="{NAP['tel_href']}">{e(NAP['tel'])}</a> · <a href="{NAP['wa']}" target="_blank" rel="noopener">WhatsApp</a></span></li>
        <li class="hn-nap__mail"><span><a href="mailto:{NAP['email']}">{NAP['email']}</a></span></li>
        <li class="hn-nap__hor"><span>{e(t['horario'])}</span></li>
      </ul>
    </div>
    {form}
  </div>
</section>

<section class="hn-mapa">
  <div class="hn-wrap hn-mapa__grid">
    <div class="hn-mapa__txt">
      <p class="hn-eyebrow">{e(t['mapa_eyebrow'])}</p>
      <h2>{e(t['mapa_h'])}</h2>
      <p>{e(t['mapa_p'])}</p>
      <a class="k-button k-button-link k-size-sm hn-cta hn-cta--ghost" href="{NAP['maps']}" target="_blank" rel="noopener"><span class="k-button-text">{e(t['ver_maps'])}</span></a>
    </div>
    <div class="hn-mapa__card"><iframe class="hn-mapa__iframe" loading="lazy" src="{NAP['embed']}" title="{e(t['mapa_title'])}" aria-label="Clínica Belba"></iframe></div>
  </div>
</section>
</div>
"""


_ICO = {
    'pin': "M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z",
    'tel': "M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z",
    'mail': "M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z",
    'clock': "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm.5-13H11v6l5.2 3.1.8-1.2-4.5-2.7V7z",
}


def _ico(name, color='%23008488'):
    return f"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='{color}' d='{_ICO[name]}'/%3E%3C/svg%3E\")"


CSS = '''
/* Home v3 · clínica premium clara (30/09). Solo presentación: textos, enlaces, formularios y medición literales. */
.hn{--ivory:#F7F4EF;--sand:#EFE9E1;--line:#E6E0D6;--navy:#172239;--navy2:#2C3A52;--teal:#008488;--teal-d:#006d70;--teal-l:#E6F3F3;--teal-x:#3FC4C7;--muted:#6B6560;--text:#2E2A26;
--r:20px;--sh:0 24px 60px -28px rgba(23,34,57,.28);--sh2:0 10px 30px -18px rgba(23,34,57,.22);
font-family:Montserrat,sans-serif;color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased;background:#fff}
.hn .hn-wrap{max-width:1240px;margin:0 auto;padding:0 32px}
.hn h1,.hn h2,.hn h3{font-family:Montserrat,sans-serif;color:var(--navy);margin:0 0 .5em;line-height:1.1}
.hn h2{font-size:42px;font-weight:800;letter-spacing:-1.4px;max-width:16em}
.hn h2 em{font-style:normal;color:var(--teal)}
.hn h3{font-size:19px;font-weight:700;letter-spacing:-.2px}
.hn p{margin:0 0 1em}.hn a{color:var(--teal)}
.hn .hn-eyebrow{display:flex;align-items:center;gap:12px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--teal);font-weight:700;margin:0 0 18px}
.hn .hn-eyebrow::before{content:"";width:28px;height:2px;background:var(--teal);border-radius:2px;flex:0 0 auto}
.hn .hn-lead{font-size:17px;color:var(--muted);max-width:34em;font-weight:400}
.hn .hn-cta{display:inline-flex;align-items:center;gap:10px;background:var(--teal);color:#fff;border-radius:999px;padding:16px 30px;font-weight:700;text-decoration:none;font-size:15px;letter-spacing:0;transition:background .25s,color .25s,transform .25s,box-shadow .25s;box-shadow:0 14px 30px -14px rgba(0,132,136,.6)}
.hn .hn-cta:hover{background:var(--navy);color:#fff;transform:translateY(-2px)}
.hn .hn-cta--ghost{background:transparent;color:var(--navy);box-shadow:inset 0 0 0 1.5px var(--navy)}
.hn .hn-cta--ghost:hover{background:var(--navy);color:#fff}
.hn section{padding:100px 0}
.hn [hidden]{display:none!important}
/* cabeceras de sección a dos columnas */
.hn-proc__head,.hn-trats__head,.hn-equipo__head,.hn-resenas__head{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:end;margin-bottom:40px}
.hn-proc__head h2,.hn-trats__head h2,.hn-equipo__head h2,.hn-resenas__head h2{margin-bottom:0}
.hn-proc__head .hn-lead,.hn-trats__head .hn-lead,.hn-equipo__head .hn-lead{margin-bottom:.3em}
/* ---------- hero a pantalla completa ---------- */
.hn-hero{position:relative;min-height:calc(100vh - 85px);display:flex;flex-direction:column;justify-content:center;padding:56px 0 36px!important;background:var(--navy);color:#fff;overflow:hidden;isolation:isolate}
.hn-hero__bg{position:absolute;inset:0;z-index:-2}
.hn-hero__bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 40%;opacity:0;transition:opacity 1.6s ease;transform:scale(1)}
.hn-hero__bg img.is-on{opacity:1;animation:hnKb 9s ease-out forwards}
@keyframes hnKb{from{transform:scale(1)}to{transform:scale(1.08)}}
.hn-hero__shade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(12,20,36,.9) 0%,rgba(12,20,36,.78) 38%,rgba(12,20,36,.42) 66%,rgba(12,20,36,.3) 100%),linear-gradient(180deg,rgba(12,20,36,.15) 0%,rgba(12,20,36,0) 30%,rgba(12,20,36,.55) 100%)}
.hn-hero>.hn-wrap{width:100%}
.hn-hero__grid{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.hn-hero h1{font-size:64px;font-weight:800;letter-spacing:-2.6px;line-height:.98;margin:0 0 20px;color:#fff;text-shadow:0 2px 24px rgba(0,0,0,.25)}
.hn-hero h1 em{font-style:normal;color:var(--teal-x);display:block}
.hn-eyebrow--hero{flex-wrap:wrap;color:#9fd8d9;margin-bottom:18px}.hn-eyebrow--hero::before{display:none}
.hn-badge{display:inline-block;background:var(--teal);color:#fff;border-radius:999px;padding:5px 12px;font-size:11px;letter-spacing:.14em}
.hn-hero__sub{font-size:19px;font-weight:600;color:#fff;letter-spacing:-.3px;max-width:26em;margin-bottom:.6em}
.hn-hero__p{font-size:15.5px;color:rgba(255,255,255,.82);max-width:34em;margin-bottom:22px;line-height:1.65}
.hn-hero__actions{display:flex;flex-wrap:wrap;align-items:center;gap:14px 28px;margin:0 0 22px}
.hn .hn-cta--lg{font-size:16px;padding:20px 34px}
.hn-arrow{font-family:Montserrat,sans-serif;transition:transform .2s}.hn-cta--lg:hover .hn-arrow{transform:translateX(4px)}
.hn .hn-hero__tel{display:inline-flex;align-items:center;gap:10px;font-size:24px;font-weight:800;letter-spacing:-.8px;color:#fff;text-decoration:none}
.hn-hero__tel:hover{color:var(--teal-x)}
.hn-tel-ico{width:20px;height:20px;background:var(--teal-x);-webkit-mask:''' + _ICO['tel'].join(['url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\'%3E%3Cpath fill=\'%23000\' d=\'', '\'/%3E%3C/svg%3E") center/contain no-repeat']) + ''';mask:''' + _ICO['tel'].join(['url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\'%3E%3Cpath fill=\'%23000\' d=\'', '\'/%3E%3C/svg%3E") center/contain no-repeat']) + '''}
.hn-hero__trust{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,.18)}
.hn .hn-trust{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:#fff;font-size:13px;font-weight:600}
.hn .hn-trust--g{background:#fff;color:var(--navy);border-radius:12px;padding:9px 13px;box-shadow:var(--sh2)}
.hn .hn-trust--link{color:#fff;text-decoration:underline;text-underline-offset:3px}
.hn-g{font-weight:800;font-size:16px;color:#4285F4}.hn-stars{color:#F5B301;letter-spacing:1px;font-size:13px}
.hn-avatars{display:inline-flex}.hn-avatars img{width:30px;height:30px;border-radius:50%;object-fit:cover;object-position:top;border:2px solid #fff;margin-left:-10px;background:var(--sand)}
.hn-avatars img:first-child{margin-left:0}
.hn-pills{display:flex;flex-wrap:wrap;gap:8px;margin:0}
.hn-pills a{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border-radius:999px;padding:7px 14px;font-size:12.5px;font-weight:600;white-space:nowrap;transition:background .2s,color .2s,border-color .2s}
.hn-pills a:hover{background:#fff;border-color:#fff;color:var(--navy)}
.hn-hero__form{position:relative;background:#fff;border-radius:24px;padding:24px 26px 10px;box-shadow:0 40px 90px -30px rgba(0,0,0,.55);color:var(--text)}
.hn-hero__formtitle{font-weight:800;color:var(--navy);font-size:21px;margin:0 0 4px;letter-spacing:-.5px}.hn-hero__formsub{font-size:13px;color:var(--muted);margin:0 0 12px}
.hn-hero__form .belba-form{box-shadow:none;padding:0 0 12px;max-width:none;border-radius:0}
.belba-form--compact .bf-title{font-size:17px}.belba-form--compact .bf-choice{padding:11px 14px;font-size:14px}.belba-form--compact .bf-choices{grid-template-columns:1fr 1fr}
.belba-form--compact .bf-progress{margin-bottom:14px}
.hn-hero__foot{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:40px}
.hn-dots{display:flex;gap:8px}
.hn-dot{width:10px;height:10px;border-radius:999px;border:0;padding:0;background:rgba(255,255,255,.45);cursor:pointer;transition:background .3s,width .3s}
.hn-dot.is-on{background:#fff;width:28px}
.hn .hn-logos{display:inline-flex;align-items:center;gap:14px;background:rgba(255,255,255,.94);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);padding:8px 14px;border-radius:12px}
.hn-logos span{font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:700}
.hn-logos img{height:28px;width:auto;display:block}
/* ---------- filosofía: collage + pasos ---------- */
.hn-filo__grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:88px;align-items:center}
.hn-filo__media{position:relative;padding:0 48px 48px 0}
.hn .hn-filo__big{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;border-radius:var(--r);box-shadow:var(--sh)}
.hn .hn-filo__small{position:absolute;right:0;bottom:0;width:44%;aspect-ratio:1;object-fit:cover;border-radius:18px;border:6px solid #fff;box-shadow:var(--sh)}
.hn-steps{list-style:none;padding:0;margin:32px 0 28px;counter-reset:hnstep;display:grid;gap:12px}
.hn-steps li{display:grid;grid-template-columns:46px 1fr;gap:16px;align-items:center;padding:16px 18px;background:var(--ivory);border-radius:16px;counter-increment:hnstep}
.hn-steps__n{width:46px;height:46px;border-radius:14px;background:var(--teal);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;letter-spacing:.05em}
.hn-steps__n::before{content:counter(hnstep,decimal-leading-zero)}
.hn-steps li p{margin:0;font-size:16px;color:var(--navy);font-weight:600;line-height:1.45}
.hn-strong{font-size:21px;font-weight:700;color:var(--navy);letter-spacing:-.4px}
/* ---------- procedimientos: carrusel ---------- */
.hn-proc{background:var(--ivory);overflow:hidden;padding-bottom:84px!important}
.hn-proc__tools{display:flex;align-items:flex-end;gap:24px}
.hn-proc__tools .hn-lead{flex:1 1 auto;margin:0}
.hn-nav{display:flex;gap:8px;flex:0 0 auto}
.hn-arrowbtn{width:48px;height:48px;border-radius:50%;border:1.5px solid var(--line);background:#fff!important;color:var(--navy)!important;font:700 18px Montserrat,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s,color .2s,border-color .2s;padding:0}
.hn-arrowbtn:hover{background:var(--navy)!important;color:#fff!important;border-color:var(--navy)}
.hn-arrowbtn:disabled{opacity:.35;cursor:default;background:#fff!important;color:var(--navy)!important;border-color:var(--line)}
.hn-track{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x proximity;padding:6px max(32px,calc(50vw - 588px)) 28px;scroll-padding-left:max(32px,calc(50vw - 588px));scrollbar-width:none;cursor:grab;-webkit-overflow-scrolling:touch}
.hn-track::-webkit-scrollbar{display:none}
.hn-track.is-drag{cursor:grabbing;scroll-snap-type:none;scroll-behavior:auto}
.hn-track.is-drag .hn-card{pointer-events:none}
.hn-card{position:relative;flex:0 0 262px;aspect-ratio:3/4;border-radius:18px;overflow:hidden;background:var(--navy);text-decoration:none;scroll-snap-align:start;box-shadow:var(--sh2);isolation:isolate}
.hn-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 30%;display:block;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.hn-card::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(23,34,57,0) 40%,rgba(23,34,57,.85) 100%);transition:opacity .3s}
.hn-card:hover img{transform:scale(1.06)}
.hn-card__n{position:absolute;left:16px;top:14px;z-index:1;font-size:11px;letter-spacing:.2em;color:#fff;font-weight:700;background:rgba(23,34,57,.45);padding:4px 8px;border-radius:999px;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
.hn-card__t{position:absolute;left:18px;right:56px;bottom:18px;z-index:1;color:#fff;font-weight:700;font-size:17px;letter-spacing:-.2px;line-height:1.2;overflow-wrap:anywhere}
.hn-card__go{position:absolute;right:14px;bottom:14px;z-index:1;width:36px;height:36px;border-radius:50%;background:#fff;color:var(--navy);display:flex;align-items:center;justify-content:center;font-weight:700;transform:translateY(8px);opacity:0;transition:transform .3s,opacity .3s}
.hn-card:hover .hn-card__go{transform:none;opacity:1}
/* ---------- tratamientos: tarjetas con foto de fondo ---------- */
.hn-trats__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.hn-trat{position:relative;min-height:440px;border-radius:var(--r);overflow:hidden;background:var(--navy);box-shadow:var(--sh);isolation:isolate}
.hn-trat__bg{position:absolute;inset:0;display:block}
.hn-trat__bg img{width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.hn-trat:hover .hn-trat__bg img,.hn-trat:focus-within .hn-trat__bg img{transform:scale(1.05)}
.hn-trat__body{position:absolute;left:0;right:0;bottom:0;padding:120px 24px 22px;color:#fff;background:linear-gradient(180deg,rgba(23,34,57,0) 0%,rgba(23,34,57,.72) 38%,rgba(23,34,57,.96) 100%)}
.hn-trat h3{font-size:22px;font-weight:800;letter-spacing:-.5px;margin-bottom:6px;color:#fff}.hn-trat h3 a{color:#fff;text-decoration:none}
.hn-trat__claim{font-size:13.5px;color:rgba(255,255,255,.82);margin-bottom:0!important;font-style:italic}
.hn-trat ul{list-style:none;margin:0;padding:0;max-height:0;opacity:0;overflow:hidden;transition:max-height .45s cubic-bezier(.2,.7,.2,1),opacity .35s,margin .35s}
.hn-trat:hover ul,.hn-trat:focus-within ul{max-height:320px;opacity:1;margin-top:12px}
.hn-trat li{border-top:1px solid rgba(255,255,255,.16);font-size:13.5px}
.hn-trat li a{display:flex;align-items:center;justify-content:space-between;padding:7px 0;color:#fff;text-decoration:none;transition:color .2s,padding .2s}
.hn-trat li a::after{content:"→";opacity:.5;font-size:12px}
.hn-trat li a:hover{color:var(--teal-x);padding-left:4px}
/* ---------- presentación (Teknon): texto + collage ---------- */
.hn-hosp{background:var(--ivory)}
.hn-hosp__grid{display:grid;grid-template-columns:1fr 1fr;gap:88px;align-items:center}
.hn-hosp h3{font-size:17px;color:var(--teal);font-weight:600;margin:0 0 18px;letter-spacing:0}
.hn-hosp__txt>p{color:var(--muted);font-size:16px;max-width:36em}
.hn-hosp__txt .hn-cta{margin-top:8px}
.hn-hosp__media{position:relative;padding:0 0 56px 56px}
.hn .hn-hosp__big{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;border-radius:var(--r);box-shadow:var(--sh)}
.hn .hn-hosp__small{position:absolute;left:0;bottom:0;width:46%;aspect-ratio:4/3;object-fit:cover;border-radius:18px;border:6px solid #fff;box-shadow:var(--sh)}
/* ---------- equipo: tarjetas con retrato ---------- */
.hn-docs{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.hn-doc{background:#fff;border-radius:var(--r);overflow:hidden;box-shadow:var(--sh2);display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}
.hn-doc:hover{transform:translateY(-6px);box-shadow:var(--sh)}
.hn-doc__media{position:relative;aspect-ratio:4/5;background:var(--sand);overflow:hidden}
.hn-doc__media a{display:block;height:100%}
.hn-doc__media img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.hn-doc:hover .hn-doc__media img{transform:scale(1.04)}
.hn-doc__over{position:absolute;left:0;right:0;bottom:0;padding:70px 20px 18px;background:linear-gradient(180deg,rgba(23,34,57,0),rgba(23,34,57,.9))}
.hn-doc__over h3{font-size:19px;font-weight:800;margin:0 0 2px;letter-spacing:-.4px}.hn-doc__over h3 a{color:#fff;text-decoration:none}
.hn-doc__rol{color:#9fd8d9;font-weight:600;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;margin:0}
.hn-doc__body{padding:20px 20px 24px;display:flex;flex-direction:column;gap:12px}
.hn-doc__cita{font-style:italic;color:var(--navy);font-size:14px;line-height:1.5;padding:12px 14px;background:var(--ivory);border-radius:12px;margin:0;border-left:3px solid var(--teal)}
.hn-doc__bio{font-size:13.5px;color:var(--muted);line-height:1.65;margin:0}
/* ---------- reseñas: widget de Google integrado ---------- */
.hn-resenas{background:var(--ivory)}
.hn .hn-trust--lg{font-size:14px;padding:12px 16px;border-radius:12px;margin-bottom:4px;color:var(--navy)}
.hn-resenas__head{justify-self:start;grid-template-columns:1fr auto}
.hn-resenas__head .hn-trust{justify-self:start}
.hn-resenas .ti-widget.ti-goog .ti-footer{display:none!important}
.hn-resenas .ti-widget.ti-goog .ti-widget-container:not(.ti-col-1) .ti-reviews-container{flex:0 0 100%!important;max-width:100%!important}
.hn-resenas .ti-widget.ti-goog .ti-review-item>.ti-inner{background:#fff!important;border:0!important;border-radius:18px!important;box-shadow:0 14px 40px -24px rgba(23,34,57,.3)!important;padding:26px 26px 22px!important}
.hn-resenas .ti-widget.ti-goog .ti-profile-img{display:none!important}
.hn-resenas .ti-widget.ti-goog .ti-name{font:700 15px/1.3 Montserrat,sans-serif!important;color:var(--navy)!important}
.hn-resenas .ti-widget.ti-goog .ti-date{font:400 12px/1.4 Montserrat,sans-serif!important;color:var(--muted)!important}
.hn-resenas .ti-widget.ti-goog .ti-review-content{font:400 14.5px/1.65 Montserrat,sans-serif!important;color:var(--text)!important}
.hn-resenas .ti-widget.ti-goog .ti-read-more{color:var(--teal)!important;font-weight:600!important;font-family:Montserrat,sans-serif!important}
.hn-resenas .ti-widget.ti-goog .ti-controls .ti-next,.hn-resenas .ti-widget.ti-goog .ti-controls .ti-prev{background:#fff!important;border:1px solid var(--line)!important;box-shadow:var(--sh2)!important}
/* ---------- primer paso ---------- */
.hn-form{background:#fff}
.hn-form__grid{display:grid;grid-template-columns:1fr 1fr;gap:88px;align-items:start}
.hn-nap{list-style:none;padding:0;margin:32px 0 0;display:grid;gap:12px}
.hn-nap li{display:grid;grid-template-columns:46px 1fr;gap:14px;align-items:center;padding:12px 16px 12px 12px;background:var(--ivory);border-radius:16px;font-size:15px;color:var(--navy);line-height:1.5}
.hn-nap li::before{content:"";width:46px;height:46px;border-radius:14px;background:#fff var(--ico) center/22px no-repeat;box-shadow:var(--sh2)}
.hn-nap__dir{--ico:''' + _ico('pin') + '''}
.hn-nap__tel{--ico:''' + _ico('tel') + '''}
.hn-nap__mail{--ico:''' + _ico('mail') + '''}
.hn-nap__hor{--ico:''' + _ico('clock') + '''}
.hn-nap a{color:var(--navy);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .2s}.hn-nap a:hover{border-color:var(--navy)}
.hn-form .belba-form{border:0;box-shadow:var(--sh);border-radius:24px;padding:36px 32px;background:#fff}
/* ---------- mapa ---------- */
.hn-mapa{background:var(--ivory)}
.hn-mapa__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:64px;align-items:center}
.hn-mapa p{color:var(--muted);max-width:26em}
.hn-mapa__card{border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);background:var(--line)}
.hn-mapa__iframe{width:100%;height:440px;border:0;display:block;filter:saturate(.75)}
/* aparición al hacer scroll */
.hn .rv{opacity:0;transform:translateY(26px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1);transition-delay:calc(var(--i,0)*70ms)}
.hn .rv.in{opacity:1;transform:none}
.hn .rv.in:hover{transition-delay:0s}
/* accesibilidad y movimiento */
.hn a:focus-visible,.hn button:focus-visible{outline:2px solid var(--teal);outline-offset:3px}
@media(hover:none){.hn-trat ul{max-height:none;opacity:1;margin-top:12px}.hn-trat__body{padding-top:90px}.hn-card__go{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.hn *{transition:none!important;animation:none!important}.hn .rv{opacity:1;transform:none}.hn-card:hover img,.hn-trat:hover .hn-trat__bg img,.hn-doc:hover .hn-doc__media img{transform:none}}
/* ---------- responsive ---------- */
@media(max-width:1100px){.hn h2{font-size:36px;letter-spacing:-1px}
.hn-hero h1{font-size:54px;letter-spacing:-2px}.hn-hero__grid{gap:40px}
.hn-trats__grid,.hn-docs{grid-template-columns:repeat(2,1fr)}
.hn-filo__grid,.hn-hosp__grid,.hn-form__grid{gap:48px}.hn-mapa__grid{grid-template-columns:1fr;gap:32px}
.hn-card{flex-basis:230px}}
@media(max-width:820px){.hn .hn-wrap{padding:0 20px}.hn h2{font-size:30px;letter-spacing:-.9px}.hn section{padding:72px 0}
.hn-hero{min-height:0;padding:44px 0 32px!important}.hn-hero h1{font-size:40px;letter-spacing:-1.5px;margin-bottom:16px}.hn-hero__tel{font-size:21px}
.hn-hero__grid,.hn-filo__grid,.hn-proc__head,.hn-trats__head,.hn-equipo__head,.hn-resenas__head,.hn-hosp__grid,.hn-form__grid,.hn-mapa__grid{grid-template-columns:1fr;gap:28px}
.hn-proc__head,.hn-trats__head,.hn-equipo__head,.hn-resenas__head{margin-bottom:28px}
.hn-hero__shade{background:linear-gradient(180deg,rgba(12,20,36,.82) 0%,rgba(12,20,36,.72) 60%,rgba(12,20,36,.9) 100%)}
.hn-hero__form{padding:22px 18px 8px;border-radius:20px}.hn-hero__foot{margin-top:28px;flex-wrap:wrap}
.hn-pills a{white-space:normal}.hn-hero__trust{gap:8px 14px}
.hn .hn-logos{padding:6px 10px;gap:10px}.hn-logos img{height:22px}
.hn-filo__media{padding:0 28px 28px 0}.hn .hn-filo__big{aspect-ratio:4/4}
.hn-proc__tools{flex-direction:column;align-items:flex-start;gap:14px}
.hn-track{padding:6px 20px 24px;gap:12px;scroll-padding-left:20px}.hn-card{flex-basis:68vw;max-width:300px}
.hn-trats__grid,.hn-docs{grid-template-columns:1fr;gap:18px}.hn-trat{min-height:360px}
.hn-hosp__media{padding:0 0 36px 28px}
.hn-mapa__iframe{height:320px}.hn-form .belba-form{padding:24px 18px}}
'''

JS = '''
(function(){var d=document,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function sel(v){d.querySelectorAll('.hn .hn-sel__btn').forEach(function(b){var on=b.getAttribute('data-sel')===v;b.classList.toggle('is-on',on);b.setAttribute('aria-selected',on?'true':'false');});
d.querySelectorAll('.hn [data-for]').forEach(function(g){g.hidden=g.getAttribute('data-for')!==v;});
d.querySelectorAll('.hn [data-only]').forEach(function(a){a.hidden=a.getAttribute('data-only')!==v;});
try{localStorage.setItem('belba_sel',v);}catch(e){}
if(window.dataLayer)window.dataLayer.push({event:'home_selector',selector:v});}
d.querySelectorAll('.hn .hn-sel__btn').forEach(function(b){b.addEventListener('click',function(){sel(b.getAttribute('data-sel'));});});
d.querySelectorAll('.hn input[name=sel_persona]').forEach(function(r){r.addEventListener('change',function(){sel(r.value==='Hombre'?'hombre':'mujer');});});
/* hero: fundido con zoom lento, puntos */
d.querySelectorAll('.hn [data-slider]').forEach(function(sl){var im=Array.prototype.filter.call(sl.querySelectorAll('img'),function(x){return x.parentNode===sl;}),dots=d.querySelectorAll('.hn .hn-dot'),i=0,tm;
function go(n){im[i].classList.remove('is-on');if(dots[i])dots[i].classList.remove('is-on');i=(n+im.length)%im.length;im[i].classList.add('is-on');if(dots[i])dots[i].classList.add('is-on');}
function auto(){clearInterval(tm);if(!rm&&im.length>1)tm=setInterval(function(){go(i+1);},6500);}
Array.prototype.forEach.call(dots,function(b,k){b.addEventListener('click',function(){go(k);auto();});});auto();});
/* carrusel de procedimientos: flechas, arrastre con ratón, deslizar en táctil */
d.querySelectorAll('.hn [data-carousel]').forEach(function(c){var tr=c.querySelector('.hn-track'),prev=c.querySelector('[data-prev]'),next=c.querySelector('[data-next]');if(!tr)return;
function step(){var k=tr.querySelector('.hn-card');return k?k.getBoundingClientRect().width+18:300;}
if(prev)prev.addEventListener('click',function(){tr.scrollBy({left:-step()*2,behavior:rm?'auto':'smooth'});});
if(next)next.addEventListener('click',function(){tr.scrollBy({left:step()*2,behavior:rm?'auto':'smooth'});});
var down=false,sx=0,sl=0,moved=false;
tr.addEventListener('pointerdown',function(ev){if(ev.pointerType!=='mouse')return;down=true;moved=false;sx=ev.clientX;sl=tr.scrollLeft;tr.classList.add('is-drag');});
tr.addEventListener('pointermove',function(ev){if(!down)return;var dx=ev.clientX-sx;if(Math.abs(dx)>4)moved=true;tr.scrollLeft=sl-dx;});
function up(){if(!down)return;down=false;setTimeout(function(){tr.classList.remove('is-drag');},50);}
tr.addEventListener('pointerup',up);tr.addEventListener('pointerleave',up);
tr.addEventListener('click',function(ev){if(moved){ev.preventDefault();ev.stopPropagation();moved=false;}},true);
function upd(){var max=tr.scrollWidth-tr.clientWidth-1;if(prev)prev.disabled=tr.scrollLeft<=0;if(next)next.disabled=tr.scrollLeft>=max;}
tr.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();});
/* aparición al hacer scroll */
if(!rm&&'IntersectionObserver' in window){var rvs='.hn-filo__media,.hn-filo__txt,.hn-proc__head,.hn-card,.hn-trats__head,.hn-trat,.hn-hosp__txt,.hn-hosp__media,.hn-equipo__head,.hn-doc,.hn-resenas__head,.hn-form__grid>*,.hn-mapa__grid>*';
var els=d.querySelectorAll('.hn '+rvs.split(',').join(',.hn '));var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
Array.prototype.forEach.call(els,function(el){var sib=el.parentNode.children,k=Array.prototype.indexOf.call(sib,el);el.style.setProperty('--i',Math.min(k,7));el.classList.add('rv');io.observe(el);});}
var s=null;try{s=localStorage.getItem('belba_sel');}catch(e){}if(s==='hombre')sel('hombre');else sel('mujer');
var pre=d.querySelector('.hn input[name=sel_persona][value='+(s==='hombre'?'Hombre':'Mujer')+']');if(pre&&s){pre.checked=true;}})();
'''

def ti_of(doc):
    """Widget de reseñas de Google (Trustindex) literal de la portada de ese idioma."""
    Sd = BeautifulSoup(''.join(b['html'] for b in doc['blocks']), 'html.parser')
    w = Sd.find(class_='ti-widget')
    if not w: return TRUSTINDEX, N_RESENAS
    h = re.sub(r'data-css-url="[^"]*"', 'data-css-url="/css/trustindex-google-widget.css"', str(w.find_parent(class_='k-widget-container') or w))
    m = re.search(r'(\d{2,4})\s', BeautifulSoup(h, 'html.parser').get_text(' ', strip=True))
    return h, (m.group(1) if m else N_RESENAS)

def main():
    from urllib.parse import unquote
    rows = []
    for f in glob.glob(B + '/src/content/pages/*/*.json'):
        doc = json.load(open(f))
        if not re.fullmatch(r'/(\w\w/)?', doc['path']): continue
        lang = doc['lang']
        t = T.get(lang) or T['es']
        lay = json.load(open(B + f'/src/content/layout/{lang}.json'))
        lb = menu_labels(lay['header'])
        ti_html, n_res = ti_of(doc)
        doc['layout'] = 'default'
        doc['css'] = CSS
        doc['blocks'] = [{'type': 'seccion', 'html': body(lang, t, lb, ti_html, n_res, doc['path']) + '<script>' + JS + '</script>'}]
        doc['root'] = {'class': 'k', 'data-kt': 'wp-page'}
        doc['bodyClass'] = 'home page k-default k-kit-5 k-page'
        doc['needs'] = sorted(set((doc.get('needs') or []) + ['trustindex']))
        doc['seo']['ogImage'] = '/images/2026/03/Honorarios-medicos-quirofano-y-anestesia.webp'
        json.dump(doc, open(f, 'w'), ensure_ascii=False)
        rows.append('| %s | página completa | portada del WordPress | home nueva (diseño Figma de Oscar, datos reales) %s | decisión Oscar 28/09; %s |' % (
            unquote(doc['path']), '' if lang == 'es' else 'traducida por la agencia', 'textos originales en ES' if lang == 'es' else 'traducción pendiente de revisión de la clínica'))
    for f in glob.glob(B + '/src/content/pages/*/zz-home-nueva.json'):
        os.remove(f)
    nl = B + '/NO_LITERAL.md'
    cur = open(nl).read() if os.path.exists(nl) else ''
    with open(nl, 'a') as fo:
        for r in rows:
            if r + '\n' not in cur: fo.write(r + '\n')
    print('home nueva en', len(rows), 'idiomas · reseñas Google (ES):', N_RESENAS)

if __name__ == '__main__':
    main()
