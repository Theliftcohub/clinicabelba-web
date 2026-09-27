import csv,json,urllib.parse,re
inv={urllib.parse.unquote(urllib.parse.urlparse(i['url']).path):i for i in json.load(open('migracion/inventory.json'))['items']}
M={'/en/rib-removal-surgery/':'/en/rib-remodeling/','/en/resection-of-the-rib/':'/en/rib-remodeling/',
'/fr/reamenagement-cotier/':'/fr/resection-costale/','/en/mini-facelift-barcelona/':'/en/mini-lifting-facial-barcelona/',
'/en/tummy-tuck-recovery/':'/abdominoplastia-recuperacion/','/en/lipovaser-before-and-after/':'/en/lipolaser-before-and-after/',
'/en/vaser-liposuction-before-and-after/':'/en/lipolaser-before-and-after/','/ca/reduccio-de-pit/':'/ca/reduccio-de-mama/',
'/fr/augmentation-mammaire-preserve/':'/fr/augmentation-mammaire-sans-alteration-de-laspect-naturel/',
'/en/what-is-bbl-brazilian-butt-lift/':'/que-es-un-bbl-brazilian-butt-lift/','/ca/que-es-bbl-brazilian-butt-lift/':'/que-es-un-bbl-brazilian-butt-lift/',
'/en/tummy-tuck-before-and-after/':'/en/abdominoplasty-before-and-after/','/ca/augment-pit-tecnica-brst/':'/ca/augment-de-pit-tecnica-brst/',
'/presupuesto/':'/precio-cirugia-estetica-barcelona/','/ca/botox/':'/ca/','/medicina-estetica/':'/',
'/uk/liposuccion/':'/uk/ліпосакція-в-барселоні/','/ru/liposuccion/':'/ru/липосакция-барселона/','/ca/liposuccio/':'/ca/liposuccio-barcelona/',
'/en/author/webbelba/page/3/':'/en/author/webbelba/'}
LOOP={'/en/blepharoplasty-before-and-after/','/en/buttock-augmentation-barcelona/','/en/arm-lift/','/en/gynecomastia-barcelona/'}
T410=re.compile(r'test-paciente|test-patient|patient-test|patiententest|test-post-|elementor-3065|prueba-belba|wpbc-booking|plantilla-facial|metform(in)?-form')
bad=[d for d in M.values() if d not in inv or inv[d].get('status')!=200]
print('destinos que no están a 200 en inventario:',bad)
rows=list(csv.DictReader(open('migracion/urls.csv')))
for r in rows:
    if r['decision']!='REVISAR': continue
    p=urllib.parse.unquote(r['url'])
    enc=lambda x: urllib.parse.quote(x,safe='/')
    if p in M:
        r.update(decision='301',destino=enc(M[p]),estado_esperado='301',notas=r['notas']+' · OK Oscar 27/09: 301 a equivalente')
    elif p in LOOP:
        r.update(decision='mantener',destino=r['url'],estado_esperado='200',notas='Hoy en BUCLE de redirecciones (bug de slugs de TranslatePress) pese a ser la URL del hreflang. Se reconstruye con la traducción EN de TranslatePress (SQL) · OK Oscar 27/09')
    elif T410.search(p):
        r.update(decision='410',destino='',estado_esperado='410',notas='Página de prueba/plantilla/formulario sin contenido real, 0 clics, 0 backlinks · OK Oscar 27/09: 410')
    else:
        r.update(decision='mantener',destino=r['url'],estado_esperado='200',notas=(r['notas']+' · ' if r['notas'] else '')+'OK Oscar 27/09: se mantiene literal')
w=csv.DictWriter(open('migracion/urls.csv','w',newline=''),fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
import collections; print(collections.Counter(r['decision'] for r in rows))
