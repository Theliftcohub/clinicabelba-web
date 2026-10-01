#!/usr/bin/env python3
"""Home nueva (/home-nueva/, noindex) a partir del diseño de Figma Make de Oscar (28/09),
con TODOS los textos, datos, fotos y reseñas sacados de la web actual (nada inventado).
Cambios respecto al diseño, decididos con Oscar: hero con foto real de quirófano en vez de la modelo;
selector Mujer / Hombre que filtra las tarjetas de procedimientos; sin cifras ni reseñas inventadas;
médicos, dirección y teléfono reales; formulario nativo (sin Typeform)."""
import json, glob, html, re, os, sys, io, functools
from bs4 import BeautifulSoup
open = functools.partial(io.open, encoding='utf-8')  # en Windows open() usa cp1252 por defecto
B = os.environ.get('BELBA_ROOT', '/home/claude/belba')
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

def card(t, href, img):
    return f'<a class="hn-card" href="{href}"><img src="{img}" alt="{e(t)}" loading="lazy" decoding="async"><span>{e(t)}</span></a>'

def body(lang, t, lb, ti_html, n_res, page_path):
    """t = textos del idioma (home_i18n.T), lb = etiquetas del menú traducido (href -> texto).
    Diseño editorial premium (30/09, petición de Nicols): estructura y aspecto nuevos; textos, enlaces y formularios literales."""
    H = lambda p: href(p, lang)
    L = lambda p, fb: lb.get(__import__('urllib.parse').parse.unquote(H(p)).lower(), fb)
    form = forms_native.render('iOSo1PBX', lang, page_path, uid='hnform')
    form_hero = forms_native.render('iOSo1PBX', lang, page_path, uid='hero', compact=True,
                                    pre_steps=[(t['pre_q'], [('Mujer', t['mujer']), ('Hombre', t['hombre'])], 'sel_persona')])
    cards_m = ''.join(card(n, H(h), img) for n, (_, h, img) in zip(t['cards_m'], CARDS_MUJER))
    cards_h = ''.join(card(n, H(h), img) for n, (_, h, img) in zip(t['cards_h'], CARDS_HOMBRE))
    trat = ''.join(
        f'<article class="hn-trat"><a href="{H(hr)}" class="hn-trat__img"><img src="{img}" alt="{e(L(hr, name))}" loading="lazy" decoding="async"></a>'
        f'<div class="hn-trat__body"><h3><a href="{H(hr)}">{e(L(hr, name))}</a></h3>' + (f'<p class="hn-trat__claim">{e(claim)}</p>' if claim else '') +
        '<ul>' + ''.join(f'<li><a href="{H(h2)}">{e(L(h2, n))}</a></li>' for n, h2 in items) + '</ul></div></article>'
        for (name, hr, _, img, items), claim in zip(TRAT, t['claims']))
    docs = ''.join(
        f'<article class="hn-doc"><a href="{H(hr)}" class="hn-doc__img"><img src="{img}" alt="{e(n)}" loading="lazy" decoding="async"></a>'
        f'<h3><a href="{H(hr)}">{e(n)}</a></h3><p class="hn-doc__rol">{e(rol)}</p>' + (f'<p class="hn-doc__cita">{e(cita)}</p>' if cita else '') +
        f'<p class="hn-doc__bio">{e(bio)}</p></article>'
        for (n, _, img, hr, _, _), (rol, cita, bio) in zip(DOCS, t['docs']))
    eb = t['hero_eyebrow'].rsplit(' · ', 1)
    eyebrow = (e(eb[0]) + ' · <span class="hn-badge">' + e(eb[1]) + '</span>') if len(eb) == 2 else e(t['hero_eyebrow'])
    hl = HL.get(lang)
    h1 = e(t['hero_h1']).replace(e(hl), '<em>' + e(hl) + '</em>', 1) if hl and hl in t['hero_h1'] else e(t['hero_h1'])
    avatars = ''.join(f'<img src="{img}" alt="" loading="lazy" decoding="async">' for (_, _, img, _, _, _) in DOCS)
    hosp_p = e(t['hosp_p']).replace('{teknon}', f'<a href="{H("/cirujanos-plasticos-barcelona/")}">{e(t["teknon"])}</a>')
    filo_items = ''.join(f'<li><p>{e(x)}</p></li>' for x in t['filo_list'])
    return f"""
<div class="hn">
<section class="hn-hero">
  <div class="hn-wrap hn-hero__grid">
    <div class="hn-hero__txt">
      <p class="hn-eyebrow hn-eyebrow--hero">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="hn-hero__sub">{e(t['hero_sub'])}</p>
      <p class="hn-hero__p">{e(t['hero_p'])}</p>
      <p class="hn-hero__actions"><a class="hn-cta hn-cta--lg" href="#valoracion">{e(t['cta'])}<span class="hn-arrow" aria-hidden="true">→</span></a></p>
      <p class="hn-hero__tel"><a href="{NAP['tel_href']}"><span class="hn-tel-ico" aria-hidden="true"></span>{e(NAP['tel'])}</a></p>
      <div class="hn-hero__trust">
        <a class="hn-trust hn-trust--g" href="#resenas"><span class="hn-g" aria-hidden="true">G</span><span class="hn-stars" aria-hidden="true">★★★★★</span><span>{e(t['proof'].format(n=n_res))}</span></a>
        <a class="hn-trust" href="{H('/cirujanos-plasticos-barcelona/')}"><span class="hn-avatars" aria-hidden="true">{avatars}</span><span>{e(t['equipo_h'])}</span></a>
        <a class="hn-trust hn-trust--link" href="#procedimientos">{e(t['ver_proc'])}</a>
      </div>
      <nav class="hn-pills" aria-label="{e(t['areas'])}">
        <a href="{H('/cirugia-facial/')}">{e(L('/cirugia-facial/', 'Cirugía facial'))}</a><a href="{H('/cirugia-de-la-mama/')}">{e(L('/cirugia-de-la-mama/', 'Cirugía de la mama'))}</a><a href="{H('/cirugia-corporal/')}">{e(L('/cirugia-corporal/', 'Cirugía corporal'))}</a><a href="{H('/cirugia-intima/')}" data-only="mujer">{e(L('/cirugia-intima/', 'Cirugía íntima'))}</a><a href="{H('/ginecomastia-barcelona/')}" data-only="hombre">{e(t['gineco'])}</a>
      </nav>
    </div>
    <div class="hn-hero__side">
      <div class="hn-slider" data-slider aria-hidden="true">
        <img src="/images/2026/03/Honorarios-medicos-quirofano-y-anestesia.webp" alt="" class="is-on" loading="eager" decoding="async">
        <img src="/images/2026/04/Primera-consulta-de-cirugia-estetica-BELBA.webp" alt="" loading="lazy" decoding="async">
        <img src="/images/2025/12/centro-medico-teknon-1.webp" alt="" loading="lazy" decoding="async">
        <span class="hn-slider__dots"><i class="is-on"></i><i></i><i></i></span>
        <span class="hn-logos"><span>{e(t['logos'])}</span><img src="/images/2025/12/quiron-salud-tekon.webp" alt="Quirónsalud y Centro Médico Teknon" loading="lazy" decoding="async"></span>
      </div>
      <div class="hn-hero__form" id="valoracion">
        <p class="hn-hero__formtitle">{e(t['cta'])}</p>
        <p class="hn-hero__formsub">{e(t['form_sub'])}</p>
        {form_hero}
      </div>
    </div>
  </div>
</section>

<section class="hn-filo">
  <div class="hn-wrap hn-filo__grid">
    <div class="hn-filo__txt">
      <p class="hn-eyebrow">{e(t['filo_eyebrow'])}</p>
      <h2>{e(t['filo_h'])}</h2>
      {''.join(f'<p class="hn-lead">{e(p)}</p>' for p in t['filo_p'])}
      <ol class="hn-steps">{filo_items}</ol>
      <p class="hn-strong">{e(t['filo_fin'])}</p>
    </div>
    <figure class="hn-filo__img"><img src="/images/2026/04/Primera-consulta-de-cirugia-estetica-BELBA.webp" alt="{e(t['filo_alt'])}" loading="lazy" decoding="async"></figure>
  </div>
</section>

<section class="hn-proc" id="procedimientos">
  <div class="hn-wrap">
    <div class="hn-proc__head">
      <div><p class="hn-eyebrow">{e(t['proc_eyebrow'])}</p><h2>{e(t['proc_h'])}</h2></div>
      <p class="hn-lead">{e(t['proc_p'])}</p>
    </div>
    <div class="hn-cards">{cards_m}{cards_h}</div>
  </div>
</section>

<section class="hn-trats">
  <div class="hn-wrap">
    <div class="hn-trats__head">
      <div><p class="hn-eyebrow">{e(t['trat_eyebrow'])}</p><h2>{e(t['trat_h'])}</h2></div>
      <p class="hn-lead">{e(t['trat_sub'])}</p>
    </div>
    <div class="hn-trats__grid">{trat}</div>
  </div>
</section>

<section class="hn-hosp">
  <div class="hn-wrap">
    <div class="hn-hosp__band">
      <img src="/images/2025/12/centro-medico-teknon-1.webp" alt="{e(t['hosp_alt'])}" loading="lazy" decoding="async">
      <div class="hn-hosp__card">
        <p class="hn-eyebrow">{e(t['hosp_eyebrow'])}</p>
        <h2>{e(t['hosp_h'])}</h2>
        <h3>{e(t['hosp_sub'])}</h3>
        <p>{hosp_p}</p>
        <a class="k-button k-button-link k-size-sm hn-cta" href="{H('/consulta-online/')}"><span class="k-button-text">{e(t['cita'])}</span></a>
      </div>
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
  <div class="hn-wrap"><p class="hn-eyebrow">{e(t['res_eyebrow'])}</p><h2>{e(t['res_h'])}</h2>{ti_html}</div>
</section>

<section class="hn-form" id="contacto-rapido">
  <div class="hn-wrap hn-form__grid">
    <div>
      <p class="hn-eyebrow">{e(t['form_eyebrow'])}</p>
      <h2>{e(t['form_h'])}</h2>
      <p class="hn-lead">{e(t['form_p'])}</p>
      <ul class="hn-nap">
        <li><a href="{NAP['maps']}" target="_blank" rel="noopener">{e(NAP['dir1'])}, {e(NAP['dir2'])}</a></li>
        <li><a href="{NAP['tel_href']}">{e(NAP['tel'])}</a> · <a href="{NAP['wa']}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="mailto:{NAP['email']}">{NAP['email']}</a></li>
        <li>{e(t['horario'])}</li>
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
    <iframe class="hn-mapa__iframe" loading="lazy" src="{NAP['embed']}" title="{e(t['mapa_title'])}" aria-label="Clínica Belba"></iframe>
  </div>
</section>
</div>
"""

CSS = '''
/* Home · editorial premium (30/09). Solo presentación: textos, enlaces, formularios y medición literales. */
.hn{--ivory:#F7F4EF;--sand:#EFE9E1;--line:#E3DCD2;--navy:#172239;--navy2:#2C3A52;--teal:#008488;--teal-d:#006d70;--muted:#6B6560;--text:#2E2A26;
font-family:Montserrat,sans-serif;color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased;background:#fff}
.hn .hn-wrap{max-width:1240px;margin:0 auto;padding:0 32px}
.hn h1,.hn h2,.hn h3{font-family:Montserrat,sans-serif;color:var(--navy);margin:0 0 .5em;line-height:1.1}
.hn h1{font-size:64px;font-weight:300;letter-spacing:-2.5px}
.hn h2{font-size:44px;font-weight:300;letter-spacing:-1.6px;max-width:15em}
.hn h3{font-size:19px;font-weight:500;letter-spacing:-.2px}
.hn p{margin:0 0 1em}.hn a{color:var(--teal)}
.hn .hn-eyebrow{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--teal);font-weight:600;margin:0 0 20px}
.hn .hn-lead{font-size:16px;color:var(--muted);max-width:34em;font-weight:400}
.hn .hn-cta{display:inline-flex;align-items:center;background:var(--navy);color:#fff;border-radius:999px;padding:16px 30px;font-weight:500;text-decoration:none;font-size:14px;letter-spacing:.02em;transition:background .25s,color .25s}
.hn .hn-cta:hover{background:var(--teal);color:#fff}
.hn .hn-cta--ghost{background:transparent;color:var(--navy);box-shadow:inset 0 0 0 1px var(--navy)}
.hn .hn-cta--ghost:hover{background:var(--navy);color:#fff}
.hn section{padding:88px 0}
.hn [hidden]{display:none!important}
/* cabeceras de sección a dos columnas */
.hn-proc__head,.hn-trats__head,.hn-equipo__head{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:end;margin-bottom:36px;padding-bottom:24px;border-bottom:1px solid var(--line)}
.hn-proc__head h2,.hn-trats__head h2,.hn-equipo__head h2{margin-bottom:0;font-size:38px}
.hn-proc__head .hn-lead,.hn-trats__head .hn-lead,.hn-equipo__head .hn-lead{margin-bottom:.4em}
/* hero */
.hn-hero{background:var(--ivory);padding:40px 0 48px!important;min-height:calc(100vh - 104px);display:flex;align-items:center;overflow:hidden}
.hn-hero>.hn-wrap{width:100%}
.hn-hero__grid{display:grid;grid-template-columns:1.05fr .95fr;gap:64px;align-items:center}
.hn-hero h1{font-size:62px;font-weight:800;letter-spacing:-2.4px;line-height:.98;margin:0 0 20px;color:var(--navy)}
.hn-hero h1 em{font-style:normal;color:var(--teal);display:block}
.hn-eyebrow--hero{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.hn-badge{display:inline-block;background:var(--teal);color:#fff;border-radius:999px;padding:5px 12px;font-size:11px;letter-spacing:.14em}
.hn-hero__sub{font-size:18px;font-weight:600;color:var(--navy);letter-spacing:-.3px;max-width:26em;margin-bottom:.5em}
.hn-hero__p{font-size:15px;color:var(--muted);max-width:34em;margin-bottom:18px;line-height:1.6}
.hn-hero__actions{display:flex;flex-wrap:wrap;align-items:center;gap:14px 28px;margin:0 0 20px}
.hn .hn-cta--lg{background:var(--teal);font-size:16px;font-weight:700;padding:20px 34px;gap:10px;letter-spacing:0}
.hn .hn-cta--lg:hover{background:var(--navy)}
.hn-arrow{font-family:Montserrat,sans-serif;transition:transform .2s}.hn-cta--lg:hover .hn-arrow{transform:translateX(4px)}
.hn-hero__tel{margin:0}
.hn-hero__tel a{display:inline-flex;align-items:center;gap:10px;font-size:26px;font-weight:800;letter-spacing:-1px;color:var(--navy);text-decoration:none}
.hn-hero__tel a:hover{color:var(--teal)}
.hn-tel-ico{width:20px;height:20px;background:var(--teal);-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z'/%3E%3C/svg%3E") center/contain no-repeat}
.hn-hero__trust{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid var(--line)}
.hn-trust{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:var(--navy);font-size:13px;font-weight:600}
.hn-trust--g{background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 12px}
.hn-trust--link{color:var(--teal);text-decoration:underline;text-underline-offset:3px}
.hn-g{font-weight:800;font-size:16px;color:#4285F4}.hn-stars{color:#F5B301;letter-spacing:1px;font-size:13px}
.hn-avatars{display:inline-flex}.hn-avatars img{width:30px;height:30px;border-radius:50%;object-fit:cover;object-position:top;border:2px solid #fff;margin-left:-10px;background:var(--sand)}
.hn-avatars img:first-child{margin-left:0}
.hn-pills{display:flex;flex-wrap:wrap;gap:8px;margin:0}
.hn-pills a{color:var(--navy);text-decoration:none;border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 14px;font-size:12.5px;font-weight:600;white-space:nowrap;transition:background .2s,color .2s,border-color .2s}
.hn-pills a:hover{background:var(--navy);border-color:var(--navy);color:#fff}
/* columna derecha: slider + formulario */
.hn-hero__side{position:relative}
.hn-slider{position:relative;aspect-ratio:16/10;border-radius:16px;overflow:hidden;background:var(--navy)}
.hn-slider>img{position:absolute;inset:-12% 0;height:124%;width:100%;object-fit:cover;object-position:center 35%;opacity:0;transition:opacity 1.2s ease;will-change:transform}
.hn-slider>img.is-on{opacity:1}
.hn-slider__dots{position:absolute;right:18px;bottom:18px;display:flex;gap:6px}
.hn-slider__dots i{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.5);transition:background .3s,width .3s}
.hn-slider__dots i.is-on{background:#fff;width:20px;border-radius:4px}
.hn .hn-logos{position:absolute;left:18px;top:18px;display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);padding:8px 12px;border-radius:10px}
.hn-logos span{font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:700}
.hn-logos img{height:28px;width:auto;display:block}
.hn-hero__form{position:relative;margin:-48px 24px 0;background:#fff;border-radius:16px;padding:22px 24px 8px;box-shadow:0 1px 0 var(--line),0 30px 60px -20px rgba(23,34,57,.25)}
.hn-hero__formtitle{font-weight:700;color:var(--navy);font-size:20px;margin:0 0 4px;letter-spacing:-.4px}.hn-hero__formsub{font-size:13px;color:var(--muted);margin:0 0 12px}
.hn-hero__form .belba-form{box-shadow:none;padding:0 0 12px;max-width:none;border-radius:0}
.belba-form--compact .bf-title{font-size:17px}.belba-form--compact .bf-choice{padding:11px 14px;font-size:14px}.belba-form--compact .bf-choices{grid-template-columns:1fr 1fr}
.belba-form--compact .bf-progress{margin-bottom:14px}
/* filosofía */
.hn-filo__grid{display:grid;grid-template-columns:1fr 1fr;gap:96px;align-items:center}
.hn-filo__img{margin:0}.hn-filo__img img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center;display:block;border-radius:6px}
.hn-steps{list-style:none;padding:0;margin:36px 0 28px;border-top:1px solid var(--line);counter-reset:hnstep}
.hn-steps li{display:grid;grid-template-columns:56px 1fr;gap:16px;align-items:baseline;padding:20px 0;border-bottom:1px solid var(--line);counter-increment:hnstep}
.hn-steps li::before{content:counter(hnstep,decimal-leading-zero);font-size:12px;letter-spacing:.2em;color:var(--teal);font-weight:600}
.hn-steps li p{margin:0;font-size:16px;color:var(--navy);font-weight:500;line-height:1.5}
.hn-strong{font-size:20px;font-weight:300;color:var(--navy);letter-spacing:-.4px}
/* procedimientos */
.hn-proc{background:var(--ivory)}
.hn-sel{display:inline-flex;gap:36px;margin:-12px 0 36px;border-bottom:1px solid var(--line)}
.hn-sel__btn{position:relative;border:0;background:none;padding:12px 2px 16px;font:500 15px Montserrat,sans-serif;color:var(--muted);cursor:pointer;transition:color .2s}
.hn-sel__btn::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--navy);transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.hn .hn-sel__btn:hover,.hn .hn-sel__btn:focus{background:none;color:var(--navy)}
.hn-sel__btn.is-on{color:var(--navy)}.hn-sel__btn.is-on::after{transform:scaleX(1)}
.hn-cards{display:grid;grid-template-columns:repeat(6,1fr);gap:18px 16px;counter-reset:hncard}
.hn-card{display:block;text-decoration:none;counter-increment:hncard;min-width:0}
.hn-card span{overflow-wrap:anywhere}
.hn-card img{width:100%;aspect-ratio:1;object-fit:cover;object-position:center 30%;display:block;border-radius:6px;background:var(--sand);transition:transform .6s cubic-bezier(.2,.7,.2,1),opacity .3s}
.hn-card:hover img{opacity:.92;transform:scale(1.04)}
.hn-card span{display:flex;align-items:baseline;gap:8px;padding:10px 2px 0;color:var(--navy);font-weight:600;font-size:14px;letter-spacing:-.1px}
.hn-card span::before{content:counter(hncard,decimal-leading-zero);font-size:11px;letter-spacing:.2em;color:var(--teal);font-weight:600}
/* tratamientos */
.hn-trats__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.hn-trat{display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1)}.hn-trat:hover{transform:translateY(-4px)}
.hn-trat__img{display:block;aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--sand)}
.hn-trat__img img{width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.hn-trat:hover .hn-trat__img img{transform:scale(1.03)}
.hn-trat__body{padding-top:18px}
.hn-trat h3{margin-bottom:6px}.hn-trat h3 a{color:var(--navy);text-decoration:none;transition:color .2s}.hn-trat h3 a:hover{color:var(--teal)}
.hn-trat__claim{font-size:13px;color:var(--muted);margin-bottom:10px!important;font-style:italic;min-height:2.6em}
.hn-trat ul{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.hn-trat li{border-bottom:1px solid var(--line);font-size:13.5px}
.hn-trat li a{display:block;padding:8px 0;color:var(--navy2);text-decoration:none;transition:color .2s,padding .2s}
.hn-trat li a:hover{color:var(--teal);padding-left:6px}
/* hospital */
.hn-hosp{padding-top:0!important}
.hn-hosp__band{position:relative;min-height:560px;border-radius:6px;overflow:hidden;display:flex;align-items:center;padding:64px}
.hn-hosp__band>img{position:absolute;inset:-15% 0;width:100%;height:130%;object-fit:cover;object-position:center;display:block;will-change:transform}
.hn-hosp__card{position:relative;background:rgba(255,255,255,.94);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border-radius:6px;padding:48px 44px 40px;max-width:560px}
.hn-hosp__card h2{font-size:34px;letter-spacing:-1px}
.hn-hosp h3{font-size:16px;color:var(--teal);font-weight:500;margin-bottom:16px}
.hn-hosp p{color:var(--muted);font-size:15px}
/* equipo */
.hn-docs{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.hn-doc{background:#fff;border:1px solid var(--line);border-radius:18px;padding:14px 14px 22px;display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.hn-doc:hover{transform:translateY(-6px);box-shadow:0 30px 60px -24px rgba(23,34,57,.28);border-color:transparent}
.hn-doc h3,.hn-doc p{padding:0 6px}
.hn-doc__img{display:block;aspect-ratio:1;overflow:hidden;border-radius:12px;background:var(--sand);margin-bottom:16px}
.hn-doc__img img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.hn-doc:hover .hn-doc__img img{transform:scale(1.03)}
.hn-doc h3{font-size:17px;margin-bottom:2px}.hn-doc h3 a{color:var(--navy);text-decoration:none}.hn-doc h3 a:hover{color:var(--teal)}
.hn-doc__rol{color:var(--teal);font-weight:600;font-size:12px;margin-bottom:10px}
.hn-doc__cita{font-style:italic;color:var(--navy);font-size:14px;font-weight:400;line-height:1.5;padding:12px 14px!important;background:var(--ivory);border-radius:10px;margin:0 0 14px;border:0}
.hn-doc__bio{font-size:13.5px;color:var(--muted);line-height:1.6;margin:0}
/* reseñas */
.hn-resenas{background:var(--ivory)}
.hn-resenas h2{margin-bottom:40px}
/* formulario */
.hn-form__grid{display:grid;grid-template-columns:1fr 1fr;gap:96px;align-items:start}
.hn-nap{list-style:none;padding:0;margin:32px 0 0;border-top:1px solid var(--line)}.hn-nap li{padding:14px 0;border-bottom:1px solid var(--line);font-size:15px;color:var(--navy)}
.hn-nap a{color:var(--navy);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .2s}.hn-nap a:hover{border-color:var(--navy)}
.hn-form .belba-form{border:1px solid var(--line);box-shadow:none;border-radius:6px;padding:36px 32px;background:#fff}
/* mapa */
.hn-mapa{background:var(--sand);padding:0!important}
.hn-mapa__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:0;align-items:stretch;padding:0 32px}
.hn-mapa__txt{padding:96px 64px 96px 0}
.hn-mapa p{color:var(--muted);max-width:26em}
.hn-mapa__iframe{width:100%;height:100%;min-height:480px;border:0;display:block;filter:saturate(.7);background:var(--line)}
/* aparición al hacer scroll y parallax (site JS de la home) */
.hn .rv{opacity:0;transform:translateY(28px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1);transition-delay:calc(var(--i,0)*70ms)}
.hn .rv.in{opacity:1;transform:none}
.hn .rv.in:hover{transition-delay:0s}
/* accesibilidad y movimiento */
.hn a:focus-visible,.hn button:focus-visible{outline:2px solid var(--teal);outline-offset:3px}
@media(prefers-reduced-motion:reduce){.hn *{transition:none!important}.hn .rv{opacity:1;transform:none}.hn-card:hover img,.hn-trat:hover .hn-trat__img img,.hn-doc:hover .hn-doc__img img{transform:none}}
/* responsive */
@media(max-width:1100px){.hn h1{font-size:52px}.hn h2{font-size:38px}
.hn-hero h1{font-size:56px;letter-spacing:-2px}.hn-hero__tel a{font-size:24px}
.hn-cards{grid-template-columns:repeat(4,1fr)}.hn-trats__grid,.hn-docs{grid-template-columns:repeat(2,1fr);gap:40px 28px}
.hn-proc__head h2,.hn-trats__head h2,.hn-equipo__head h2{font-size:32px}
.hn-filo__grid,.hn-form__grid{gap:56px}.hn-hero__grid{gap:48px}}
@media(max-width:820px){.hn .hn-wrap{padding:0 20px}.hn h1{font-size:38px;letter-spacing:-1.5px}.hn h2{font-size:30px;letter-spacing:-1px}.hn section{padding:72px 0}
.hn-hero{padding:40px 0 64px!important;min-height:0;display:block}.hn-hero h1{font-size:42px;letter-spacing:-1.5px;margin-bottom:20px}.hn-hero__tel a{font-size:22px}
.hn-hero__grid,.hn-filo__grid,.hn-proc__head,.hn-trats__head,.hn-equipo__head,.hn-form__grid,.hn-mapa__grid{grid-template-columns:1fr;gap:28px}
.hn-proc__head,.hn-trats__head,.hn-equipo__head{margin-bottom:32px}
.hn-hero__form{padding:22px 18px 8px;margin:-40px 12px 0}
.hn-pills a{white-space:normal}.hn-hero__trust{gap:8px 14px}
.hn-slider{border-radius:12px}.hn .hn-logos{left:12px;top:12px;padding:6px 10px;gap:10px}.hn-logos img{height:22px}
.hn-filo__grid{display:flex;flex-direction:column-reverse}.hn-filo__img img{aspect-ratio:4/3}
.hn-cards{grid-template-columns:repeat(3,1fr);gap:12px}.hn-card span{font-size:12px;gap:5px}
.hn-trats__grid,.hn-docs{grid-template-columns:1fr;gap:40px}
.hn-hosp__band{min-height:0;padding:0;display:block}.hn-hosp__band>img{position:static;aspect-ratio:4/3;height:auto}
.hn-hosp__card{padding:28px 22px;border-radius:0 0 6px 6px;max-width:none;background:#fff}
.hn-mapa__grid{padding:0 20px}.hn-mapa__txt{padding:64px 0 32px}.hn-mapa__iframe{min-height:320px;margin:0 -20px;width:calc(100% + 40px)}
.hn-form .belba-form{padding:24px 18px}}
'''

JS = '''
(function(){var d=document;function sel(v){d.querySelectorAll('.hn .hn-sel__btn').forEach(function(b){var on=b.getAttribute('data-sel')===v;b.classList.toggle('is-on',on);b.setAttribute('aria-selected',on?'true':'false');});
d.querySelectorAll('.hn [data-for]').forEach(function(g){g.hidden=g.getAttribute('data-for')!==v;});
d.querySelectorAll('.hn [data-only]').forEach(function(a){a.hidden=a.getAttribute('data-only')!==v;});
try{localStorage.setItem('belba_sel',v);}catch(e){}
if(window.dataLayer)window.dataLayer.push({event:'home_selector',selector:v});}
d.querySelectorAll('.hn .hn-sel__btn').forEach(function(b){b.addEventListener('click',function(){sel(b.getAttribute('data-sel'));});});
d.querySelectorAll('.hn input[name=sel_persona]').forEach(function(r){r.addEventListener('change',function(){sel(r.value==='Hombre'?'hombre':'mujer');});});
d.querySelectorAll('.hn [data-slider]').forEach(function(sl){var im=sl.querySelectorAll('img:not(.hn-logos img)'),dots=sl.querySelectorAll('.hn-slider__dots i'),i=0;im=Array.prototype.filter.call(im,function(x){return x.parentNode===sl;});if(im.length<2||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))return;setInterval(function(){im[i].classList.remove('is-on');dots[i].classList.remove('is-on');i=(i+1)%im.length;im[i].classList.add('is-on');dots[i].classList.add('is-on');},4500);});
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!rm&&'IntersectionObserver' in window){var rvs='.hn-filo__txt,.hn-filo__img,.hn-proc__head,.hn-trats__head,.hn-equipo__head,.hn-card,.hn-trat,.hn-hosp__band,.hn-doc,.hn-resenas .hn-wrap,.hn-form__grid>*,.hn-mapa__txt,.hn-mapa__iframe';var els=d.querySelectorAll('.hn '+rvs.split(',').join(',.hn '));var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
Array.prototype.forEach.call(els,function(el){var sib=el.parentNode.children,k=Array.prototype.indexOf.call(sib,el);el.style.setProperty('--i',Math.min(k,7));el.classList.add('rv');io.observe(el);});}
if(!rm){var px=[{el:d.querySelector('.hn-slider'),f:.12,sel:'img'},{el:d.querySelector('.hn-hosp__band'),f:.18,sel:':scope>img'}].filter(function(o){return o.el;}),tick=false;
function par(){tick=false;var vh=innerHeight;px.forEach(function(o){var r=o.el.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var c=(r.top+r.height/2-vh/2)/vh;var y=Math.round(-c*o.f*r.height);o.el.querySelectorAll(o.sel).forEach(function(im){if(im.parentNode===o.el)im.style.transform='translate3d(0,'+y+'px,0)';});});}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(par);}},{passive:true});par();}
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
            unquote(doc['path']), '' if lang == 'es' else 'traducida por Claude', 'textos originales en ES' if lang == 'es' else 'traducción pendiente de revisión de la clínica'))
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
