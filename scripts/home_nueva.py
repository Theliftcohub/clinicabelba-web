#!/usr/bin/env python3
"""Home nueva (/home-nueva/, noindex) a partir del diseño de Figma Make de Oscar (28/09),
con TODOS los textos, datos, fotos y reseñas sacados de la web actual (nada inventado).
Cambios respecto al diseño, decididos con Oscar: hero con foto real de quirófano en vez de la modelo;
selector Mujer / Hombre que filtra las tarjetas de procedimientos; sin cifras ni reseñas inventadas;
médicos, dirección y teléfono reales; formulario nativo (sin Typeform)."""
import json, glob, html, re, os, sys
from bs4 import BeautifulSoup
B = '/home/claude/belba'
sys.path.insert(0, B + '/scripts')
import forms_native

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
CARDS_MUJER = [
    ('Corporal', '/lipo-vaser/', '/images/2025/12/corporales.webp'),
    ('Liposucción', '/liposuccion-barcelona/', '/images/2025/12/gluteos.webp'),
    ('Piernas', '/lifting-de-muslos/', '/images/2025/12/Piernas.webp'),
    ('Senos', '/aumento-pecho-barcelona/', '/images/2025/12/Senos.webp'),
    ('Rostro', '/lifting-facial-barcelona/', '/images/2025/12/Rostro.webp'),
    ('Brazos', '/lifting-de-brazos/', '/images/2025/12/Brazos.webp'),
]
CARDS_HOMBRE = [
    ('Ginecomastia', '/ginecomastia-barcelona/', '/images/2025/12/hombres.webp'),
    ('Rinoplastia', '/rinoplastia-barcelona/', '/images/2026/06/Rinoplastia-en-hombre.webp'),
    ('Lipo HD', '/liposuccion-de-alta-definicion/', '/images/2025/11/liposuccion-alta-definicion-barcelona.webp'),
    ('Blefaroplastia', '/blefaroplastia/', '/images/thumbs/Blefaroplastia-Editado-e1777911355146-rmyxdl8gpty8oq4q9pf2p0hjh447yhorhn83vtig3g.webp'),
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

def body():
    form = forms_native.render('iOSo1PBX', 'es', '/home-nueva/', uid='hnform')
    form_hero = forms_native.render('iOSo1PBX', 'es', '/home-nueva/', uid='hero', compact=True, pre_steps=[('¿Para quién buscas información?', ['Mujer', 'Hombre'], 'sel_persona')])
    cards_m = ''.join(card(*c) for c in CARDS_MUJER)
    cards_h = ''.join(card(*c) for c in CARDS_HOMBRE)
    trat = ''.join(
        f'<article class="hn-trat"><a href="{href}" class="hn-trat__img"><img src="{img}" alt="{e(t)}" loading="lazy" decoding="async"></a>'
        f'<h3><a href="{href}">{e(t)}</a></h3>' + (f'<p class="hn-trat__claim">{e(claim)}</p>' if claim else '') +
        '<ul>' + ''.join(f'<li><a href="{h2}">{e(n)}</a></li>' for n, h2 in items) + '</ul></article>'
        for t, href, claim, img, items in TRAT)
    docs = ''.join(
        f'<article class="hn-doc"><a href="{href}"><img src="{img}" alt="{e(n)}" loading="lazy" decoding="async"></a>'
        f'<h3><a href="{href}">{e(n)}</a></h3><p class="hn-doc__rol">{e(rol)}</p>' + (f'<p class="hn-doc__cita">{e(cita)}</p>' if cita else '') +
        f'<p class="hn-doc__bio">{e(bio)}</p></article>' for n, rol, img, href, cita, bio in DOCS)
    return f'''
<div class="hn">
<section class="hn-hero">
  <div class="hn-hero__bg" aria-hidden="true"></div>
  <div class="hn-wrap hn-hero__grid">
    <div class="hn-hero__txt">
      <p class="hn-eyebrow">Barcelona · Grupo Teknon · Cirujanos certificados SECPRE</p>
      <h1>{e(HERO_H1)}</h1>
      <p class="hn-hero__sub">{e(HERO_SUB)}</p>
      <p class="hn-hero__p">{e(HERO_P)}</p>
      <nav class="hn-pills" aria-label="Áreas de cirugía">
        <a href="/cirugia-facial/">Cirugía facial</a><a href="/cirugia-de-la-mama/">Cirugía de la mama</a><a href="/cirugia-corporal/">Cirugía corporal</a><a href="/cirugia-intima/" data-only="mujer">Cirugía íntima</a><a href="/ginecomastia-barcelona/" data-only="hombre">Ginecomastia</a>
      </nav>
      <p class="hn-hero__proof"><a href="#resenas">Excelente · {N_RESENAS} reseñas en Google</a> · <a href="#procedimientos">Ver procedimientos</a></p>
    </div>
    <div class="hn-hero__form" id="valoracion">
      <p class="hn-hero__formtitle">{e(CTA)}</p>
      <p class="hn-hero__formsub">Unas preguntas rápidas y nuestro equipo te escribirá para asesorarte. Sin compromiso.</p>
      {form_hero}
    </div>
  </div>
  <div class="hn-wrap hn-logos"><span>Colaboramos con</span><img src="/images/2025/12/quiron-salud-tekon.webp" alt="Quirónsalud y Centro Médico Teknon" loading="lazy" decoding="async"></div>
</section>

<section class="hn-filo">
  <div class="hn-wrap hn-filo__grid">
    <figure class="hn-filo__img"><img src="/images/2026/04/Primera-consulta-de-cirugia-estetica-BELBA.webp" alt="Primera consulta de cirugía estética en Clínica Belba" loading="lazy" decoding="async"></figure>
    <div>
      <p class="hn-eyebrow">Nuestra filosofía</p>
      <h2>{e(FILO_H)}</h2>
      {''.join(f'<p>{e(p)}</p>' for p in FILO_P)}
      <ul class="hn-checks">{''.join(f'<li>{e(x)}</li>' for x in FILO_LIST)}</ul>
      <p class="hn-strong">{e(FILO_FIN)}</p>
    </div>
  </div>
</section>

<section class="hn-proc" id="procedimientos">
  <div class="hn-wrap">
    <div class="hn-proc__head">
      <div><p class="hn-eyebrow">Especialidades</p><h2>{e(PROC_H)}</h2></div>
      <div><p>{e(PROC_P)}</p>
        <div class="hn-sel hn-sel--sm" role="tablist"><button type="button" class="hn-sel__btn is-on" data-sel="mujer" role="tab" aria-selected="true">Mujer</button><button type="button" class="hn-sel__btn" data-sel="hombre" role="tab" aria-selected="false">Hombre</button></div>
      </div>
    </div>
    <div class="hn-cards" data-for="mujer">{cards_m}</div>
    <div class="hn-cards" data-for="hombre" hidden>{cards_h}</div>
  </div>
</section>

<section class="hn-trats">
  <div class="hn-wrap">
    <p class="hn-eyebrow">Tratamientos</p>
    <h2>{e(TRAT_H)}</h2>
    <p class="hn-lead">{e(TRAT_SUB)}</p>
    <div class="hn-trats__grid">{trat}</div>
  </div>
</section>

<section class="hn-hosp">
  <div class="hn-wrap hn-hosp__grid">
    <div>
      <p class="hn-eyebrow">Presentación</p>
      <h2>{e(HOSP_H)}</h2>
      <h3>{e(HOSP_SUB)}</h3>
      <p>{HOSP_P}</p>
      <a class="k-button k-button-link k-size-sm hn-cta" href="/consulta-online/"><span class="k-button-text">Pide cita online</span></a>
    </div>
    <figure><img src="/images/2025/12/centro-medico-teknon-1.webp" alt="Clínica de cirugía plastica en Barcelona" loading="lazy" decoding="async"></figure>
  </div>
</section>

<section class="hn-equipo">
  <div class="hn-wrap">
    <p class="hn-eyebrow">Profesionales</p>
    <h2>{e(EQUIPO_H)}</h2>
    <p class="hn-lead">{' '.join(e(p) for p in EQUIPO_P)}</p>
    <div class="hn-docs">{docs}</div>
  </div>
</section>

<section class="hn-resenas" id="resenas">
  <div class="hn-wrap"><p class="hn-eyebrow">Reseñas</p><h2>Lo que dicen nuestros pacientes</h2>{TRUSTINDEX}</div>
</section>

<section class="hn-form" id="contacto-rapido">
  <div class="hn-wrap hn-form__grid">
    <div>
      <p class="hn-eyebrow">Primer paso</p>
      <h2>Da el primer paso con una valoración médica honesta</h2>
      <p>Resolver tus dudas es el primer paso para tomar una decisión segura. Nuestro equipo médico está aquí para ayudarte, sin compromiso.</p>
      <ul class="hn-nap">
        <li><a href="{NAP['maps']}" target="_blank" rel="noopener">{e(NAP['dir1'])}, {e(NAP['dir2'])}</a></li>
        <li><a href="{NAP['tel_href']}">{e(NAP['tel'])}</a> · <a href="{NAP['wa']}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="mailto:{NAP['email']}">{NAP['email']}</a></li>
        <li>{e(NAP['horario'])}</li>
      </ul>
    </div>
    {form}
  </div>
</section>

<section class="hn-mapa">
  <div class="hn-wrap hn-mapa__grid">
    <div>
      <p class="hn-eyebrow">Cómo llegar</p>
      <h2>Encuéntranos en Via Augusta, 281</h2>
      <p>Parking cercano: Parking NN Geigle Barcelona, Via Augusta 281. En metro: Les Tres Torres L6, S7, S7T. Autobús: 68, V9, V7, 70, H6, V11.</p>
      <a class="k-button k-button-link k-size-sm hn-cta" href="{NAP['maps']}" target="_blank" rel="noopener"><span class="k-button-text">Ver en Google Maps</span></a>
    </div>
    <iframe class="hn-mapa__iframe" loading="lazy" src="{NAP['embed']}" title="Clínica Belba en Google Maps" aria-label="Clínica Belba"></iframe>
  </div>
</section>

<footer class="hn-footer">
  <div class="hn-wrap hn-footer__grid">
    <div class="hn-footer__brand">
      <a href="/"><img src="/images/2024/12/clinica-belba-200.webp" alt="Clinica Cirugía Plástica Barcelona" width="192" height="58" loading="lazy" decoding="async"></a>
      <p>Cirujanos Plásticos Barcelona | Clínica Belba</p>
      <p><a href="{NAP['maps']}" target="_blank" rel="noopener">{e(NAP['dir1'])}, {e(NAP['dir2'])}</a></p>
    </div>
    <div><p class="hn-footer__h">Cirugía plástica</p><ul>
      <li><a href="/cirugia-de-la-mama/">Cirugía de la mama</a></li>
      <li><a href="/cirugia-corporal/">Cirugía corporal</a></li>
      <li><a href="/cirugia-facial/">Cirugía facial</a></li>
      <li><a href="/cirugia-intima/">Cirugía intima</a></li>
      <li><a href="/precio-cirugia-estetica-barcelona/">Precio de cirugías plásticas</a></li>
    </ul></div>
    <div><p class="hn-footer__h">Clínica</p><ul>
      <li><a href="/quienes-somos/">Quienes somos</a></li>
      <li><a href="/cirujanos-plasticos-barcelona/">Cirujanos plásticos Barcelona</a></li>
      <li><a href="/guia-del-paciente/">Guía del paciente</a></li>
      <li><a href="/test-paciente/">Test paciente</a></li>
      <li><a href="/consulta-online/">Consulta online</a></li>
      <li><a href="/blog/">Blog</a></li>
    </ul></div>
    <div><p class="hn-footer__h">Contacto</p><ul>
      <li><a href="{NAP['tel_href']}">{e(NAP['tel'])}</a></li>
      <li><a href="{NAP['wa']}" target="_blank" rel="noopener">O Llámanos vía Whatsapp</a></li>
      <li><a href="mailto:{NAP['email']}">{NAP['email']}</a></li>
      <li>{e(NAP['horario'])}</li>
    </ul></div>
  </div>
  <div class="hn-wrap hn-footer__bottom">
    <p>Clínica Belba © Todos los derechos {YEAR}.</p>
    <ul class="hn-footer__legal"><li><a href="/aviso-legal/">Aviso legal</a></li><li><a href="/politica-de-cookies/">Política de cookies</a></li><li><a href="/politica-de-privacidad/">Política de privacidad</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul>
  </div>
  <div class="hn-wrap hn-footer__eu-row"><img class="hn-footer__eu" src="/images/2022/12/financiado-por-la-union-europea.webp" alt="Financiado por la Unión Europea - NextGenerationEU." width="250" height="63" loading="lazy" decoding="async"></div>
</footer>
{WA_FLOTANTE}
</div>
'''

CSS = '''
.hn{--navy:#172239;--navy2:#143852;--teal:#008488;--sky:#D3E4EA;--grey:#F3F5F4;--text:#333;font-family:Montserrat,sans-serif;color:var(--text);line-height:1.6}
.hn .hn-wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.hn h1,.hn h2,.hn h3{font-family:Montserrat,sans-serif;color:var(--navy);margin:0 0 .5em;line-height:1.2}
.hn h1{font-size:44px;font-weight:700}.hn h2{font-size:32px;font-weight:600}.hn h3{font-size:20px;font-weight:600}
.hn p{margin:0 0 1em}.hn a{color:var(--teal)}
.hn .hn-eyebrow{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--teal);font-weight:700;margin-bottom:12px}
.hn .hn-lead{font-size:18px;max-width:760px}
.hn .hn-cta{display:inline-flex;align-items:center;background:var(--teal);color:#fff;border-radius:14px;padding:14px 26px;font-weight:600;text-decoration:none;font-size:15px}
.hn .hn-cta:hover{background:#006d70;color:#fff}
.hn section{padding:72px 0}
.hn [hidden]{display:none!important}
/* hero */
.hn-hero{position:relative;background:var(--navy);color:#fff;padding-bottom:0!important;overflow:hidden}
.hn-hero__bg{position:absolute;inset:0;background:url(/images/2026/03/Honorarios-medicos-quirofano-y-anestesia.webp) center 30%/cover no-repeat;filter:saturate(.85);opacity:.6;transform:scale(1.02)}
.hn-hero__bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(23,34,57,.95) 0%,rgba(23,34,57,.82) 50%,rgba(20,56,82,.35) 100%)}
.hn-hero .hn-wrap{position:relative}
.hn-hero__form{background:#fff;border-radius:22px;padding:22px 22px 8px;box-shadow:0 30px 60px rgba(0,0,0,.35);color:var(--text)}
.hn-hero__formtitle{font-weight:700;color:var(--navy);font-size:20px;margin:0 0 4px}.hn-hero__formsub{font-size:13px;color:#666;margin:0 0 10px}
.hn-hero__form .belba-form{box-shadow:none;padding:0 0 12px;max-width:none}
.belba-form--compact .bf-title{font-size:17px}.belba-form--compact .bf-choice{padding:10px 12px;font-size:14px}.belba-form--compact .bf-choices{grid-template-columns:1fr 1fr}
.belba-form--compact .bf-progress{margin-bottom:14px}
.hn-hero h1{color:#fff}.hn-hero .hn-eyebrow{color:#9fd8d9}
.hn-hero__grid{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center;padding-bottom:56px}
.hn-hero__sub{font-size:20px;font-weight:500;color:#e6f2f2}.hn-hero__p{color:#d3e4ea;font-size:16px}
.hn-hero__proof{margin-top:6px;font-size:14px}.hn-hero__proof a{color:#e6f2f2}
.hn-sel{display:inline-flex;background:rgba(255,255,255,.12);border-radius:999px;padding:4px;margin:8px 0 14px}
.hn-sel__btn{border:0;background:transparent;color:#fff;font:600 14px Montserrat,sans-serif;padding:8px 20px;border-radius:999px;cursor:pointer}
.hn-sel__btn.is-on{background:#fff;color:var(--navy)}
.hn-sel--sm{background:var(--grey)}.hn-sel--sm .hn-sel__btn{color:var(--navy)}.hn-sel--sm .hn-sel__btn.is-on{background:var(--teal);color:#fff}
.hn-pills{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
.hn-pills a{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:7px 14px;font-size:13px;font-weight:600}
.hn-pills a:hover{background:#fff;color:var(--navy)}
.hn-logos{display:flex;align-items:center;gap:24px;padding-top:20px;padding-bottom:20px;border-top:1px solid rgba(255,255,255,.15)}
.hn-logos span{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#9fd8d9}
.hn-logos img{height:44px;width:auto;background:#fff;border-radius:8px;padding:6px 14px}
/* filosofía */
.hn-filo__grid{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:center}
.hn-filo__img{margin:0}.hn-filo__img img{width:100%;height:auto;border-radius:20px;display:block}
.hn-checks{list-style:none;padding:0;margin:0 0 18px}.hn-checks li{padding:8px 0 8px 34px;position:relative;font-weight:500}
.hn-checks li::before{content:"";position:absolute;left:0;top:11px;width:20px;height:20px;border-radius:50%;background:var(--teal);-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z'/%3E%3C/svg%3E") center/70% no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z'/%3E%3C/svg%3E") center/70% no-repeat}
.hn-strong{font-weight:600;color:var(--navy)}
/* procedimientos */
.hn-proc{background:var(--grey)}
.hn-proc__head{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:end;margin-bottom:28px}
.hn-cards{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.hn-card{position:relative;display:block;aspect-ratio:3/4;border-radius:16px;overflow:hidden;background:var(--navy);text-decoration:none}
.hn-card img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.hn-card:hover img{transform:scale(1.05)}
.hn-card span{position:absolute;left:0;right:0;bottom:0;padding:44px 14px 14px;color:#fff;font-weight:600;font-size:15px;background:linear-gradient(180deg,transparent,rgba(23,34,57,.9))}
/* tratamientos */
.hn-trats__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:28px}
.hn-trat{background:#fff;border:1px solid #e6ecee;border-radius:18px;overflow:hidden}
.hn-trat__img{display:block;aspect-ratio:4/3;overflow:hidden}.hn-trat__img img{width:100%;height:100%;object-fit:cover;display:block}
.hn-trat h3{padding:18px 20px 0}.hn-trat h3 a{color:var(--navy);text-decoration:none}
.hn-trat__claim{padding:0 20px;font-size:14px;color:#666}
.hn-trat ul{list-style:none;margin:0;padding:6px 20px 20px}.hn-trat li{padding:5px 0;border-top:1px solid #eef2f3;font-size:14px}
.hn-trat li a{color:var(--navy2);text-decoration:none}.hn-trat li a:hover{color:var(--teal)}
/* hospital */
.hn-hosp{background:var(--sky)}
.hn-hosp__grid{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.hn-hosp figure{margin:0}.hn-hosp img{width:100%;height:auto;border-radius:20px;display:block}
.hn-hosp h3{font-size:18px;color:var(--teal);font-weight:500}
/* equipo */
.hn-docs{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:28px}
.hn-doc img{width:100%;aspect-ratio:1;object-fit:cover;object-position:top;border-radius:18px;display:block;margin-bottom:14px;background:var(--grey)}
.hn-doc h3{font-size:18px}.hn-doc h3 a{color:var(--navy);text-decoration:none}
.hn-doc__rol{color:var(--teal);font-weight:600;font-size:14px}.hn-doc__cita{font-style:italic;color:var(--navy2);font-size:14px}.hn-doc__bio{font-size:14px;color:#555}
/* reseñas */
.hn-resenas{background:var(--grey)}
/* formulario */
.hn-form__grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.hn-nap{list-style:none;padding:0;margin:0}.hn-nap li{padding:8px 0;border-top:1px solid #eef2f3}
.hn-form .belba-form{box-shadow:0 12px 40px rgba(23,34,57,.12)}
/* mapa */
.hn-mapa{background:var(--teal);color:#fff}.hn-mapa h2{color:#fff}.hn-mapa .hn-eyebrow{color:#cfeeee}
.hn-mapa__grid{display:grid;grid-template-columns:1fr 1.2fr;gap:48px;align-items:center}
.hn-mapa .hn-cta{background:#fff;color:var(--teal)}
.hn-mapa__iframe{width:100%;height:380px;border:0;border-radius:20px;display:block}
/* pie compacto (solo en esta página; el resto de la web conserva el pie literal del WordPress) */
.hn-footer{background:var(--navy);color:#c9d3df;padding:56px 0 90px;font-size:14px}
.hn-footer a{color:#e6f2f2;text-decoration:none}.hn-footer a:hover{color:#9fd8d9}
.hn-footer__grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.2fr;gap:40px}
.hn-footer__brand img{height:44px;width:auto;filter:brightness(0) invert(1);margin-bottom:14px}
.hn-footer__brand p{margin:0 0 6px}
.hn-footer__h{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#9fd8d9;font-weight:700;margin:0 0 12px}
.hn-footer ul{list-style:none;margin:0;padding:0}.hn-footer li{padding:4px 0}
.hn-footer__bottom{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 28px;margin-top:40px;padding-top:22px;border-top:1px solid rgba(255,255,255,.12);font-size:13px}
.hn-footer__bottom p{margin:0}.hn-footer__legal{display:flex;flex-wrap:wrap;gap:6px 18px}
.hn .hn-footer__eu{height:56px!important;width:auto!important;max-width:none;background:#fff;border-radius:8px;padding:6px 10px;flex:0 0 auto}
.hn-footer__eu-row{margin-top:18px}
@media(max-width:1024px){.hn-cards{grid-template-columns:repeat(3,1fr)}.hn-trats__grid,.hn-docs{grid-template-columns:repeat(2,1fr)}}
@media(max-width:820px){.hn h1{font-size:32px}.hn h2{font-size:26px}.hn section{padding:52px 0}
.hn-hero__grid,.hn-filo__grid,.hn-proc__head,.hn-hosp__grid,.hn-form__grid,.hn-mapa__grid{grid-template-columns:1fr;gap:28px}
.hn-cards{grid-template-columns:repeat(2,1fr)}.hn-trats__grid,.hn-docs{grid-template-columns:1fr}.hn-logos{flex-wrap:wrap}.hn-footer__grid{grid-template-columns:1fr 1fr;gap:28px}}
'''

JS = '''
(function(){var d=document;function sel(v){d.querySelectorAll('.hn .hn-sel__btn').forEach(function(b){var on=b.getAttribute('data-sel')===v;b.classList.toggle('is-on',on);b.setAttribute('aria-selected',on?'true':'false');});
d.querySelectorAll('.hn [data-for]').forEach(function(g){g.hidden=g.getAttribute('data-for')!==v;});
d.querySelectorAll('.hn [data-only]').forEach(function(a){a.hidden=a.getAttribute('data-only')!==v;});
try{localStorage.setItem('belba_sel',v);}catch(e){}
if(window.dataLayer)window.dataLayer.push({event:'home_selector',selector:v});}
d.querySelectorAll('.hn .hn-sel__btn').forEach(function(b){b.addEventListener('click',function(){sel(b.getAttribute('data-sel'));});});
d.querySelectorAll('.hn input[name=sel_persona]').forEach(function(r){r.addEventListener('change',function(){sel(r.value==='Hombre'?'hombre':'mujer');});});
var s=null;try{s=localStorage.getItem('belba_sel');}catch(e){}if(s==='hombre')sel('hombre');else sel('mujer');
var pre=d.querySelector('.hn input[name=sel_persona][value='+(s==='hombre'?'Hombre':'Mujer')+']');if(pre&&s){pre.checked=true;}})();
'''

def main():
    doc = {
        'path': '/home-nueva/', 'lang': 'es', 'kind': 'page', 'layout': 'header',
        'seo': {'title': home['seo']['title'], 'description': home['seo']['description'], 'canonical': 'https://clinicabelba.com/home-nueva/',
                'robots': 'noindex, nofollow', 'ogImage': '/images/2026/03/Honorarios-medicos-quirofano-y-anestesia.webp'},
        'alternates': None, 'post': None, 'root': {'class': 'k', 'data-kt': 'wp-page'},
        'css': CSS, 'blocks': [{'type': 'seccion', 'html': body() + '<script>' + JS + '</script>'}],
        'bodyClass': 'home page k-default k-kit-5 k-page', 'jsonld': home['jsonld'], 'needs': ['trustindex'],
    }
    os.makedirs(B + '/src/content/pages/es', exist_ok=True)
    json.dump(doc, open(B + '/src/content/pages/es/zz-home-nueva.json', 'w'), ensure_ascii=False)
    print('home-nueva ok · reseñas Google:', N_RESENAS)

if __name__ == '__main__':
    main()
