#!/usr/bin/env python3
"""Formularios nativos que sustituyen a los Typeform (decisión Oscar 28/09: nada de Typeform,
todo medible en el propio dominio). Las preguntas son literales de cada Typeform
(migracion/typeform_forms.json, sacado de su definición pública).

Cada formulario:
- es un <form data-belba-form> por pasos (una pregunta por paso, como el Typeform);
- envía a /form-handler.php (que lo reenvía a n8n y, si falla, por email);
- lleva campos ocultos de atribución que rellena /js/site.js (UTM, gclid, fbclid, ad_id...,
  primera fuente, referrer, landing, client_id de GA4);
- al terminar hace dataLayer.push({event:'lead_form_submit', ...}) y muestra el mensaje de
  gracias literal o redirige a la página de gracias que ya mide GTM."""
import json, html, re, hashlib, unicodedata

B = '/home/claude/belba'
TF = json.load(open(B + '/migracion/typeform_forms.json'))
PRIV = json.load(open(B + '/migracion/i18n-map.json')).get('/politica-de-privacidad/', {})
LIVE = {  # data-tf-live -> id del formulario
    '01JEVNSW0E50QTP28CV7GMGQ2P': 'iOSo1PBX',
    '01KEF5HK8JC590A93QPQFYQ2FM': 'eQ3VBLE2',
    '01JVWC4G11G723P7PMM3JZR83R': 'tCXPyaGW',
    '01HWQHDVZZE6DFETGTA8NRJAPK': 'vwHofvjc',
}
# Typeform que ya no existen (el enlace da "formulario no encontrado" hoy): se usa el general
ROTOS = {'iwX5RRyg': 'iOSo1PBX', 'x0zEJ3x1': 'iOSo1PBX'}
# Adónde va cada formulario al terminar (las de gracias las mide GTM hoy)
REDIRECT = {
    'BdYhxQFV': '/drdewevercirugiaplastica/gracias/?ref=form',
    'vwHofvjc': '/drfelixchavarriacirugiaplastica/gracias/',
}
UI = {
    'es': ('Siguiente', 'Atrás', 'Enviar', 'Obligatorio', 'Al enviar aceptas la', 'política de privacidad', '/politica-de-privacidad/', 'Enviando…', 'No se ha podido enviar. Inténtalo de nuevo o escríbenos por WhatsApp.', 'Paso'),
    'ca': ('Següent', 'Enrere', 'Envia', 'Obligatori', 'En enviar acceptes la', 'política de privacitat', '/ca/politica-de-privacitat/', 'Enviant…', "No s'ha pogut enviar. Torna-ho a provar o escriu-nos per WhatsApp.", 'Pas'),
    'en': ('Next', 'Back', 'Send', 'Required', 'By sending you accept the', 'privacy policy', '/en/privacy-policy/', 'Sending…', 'It could not be sent. Please try again or message us on WhatsApp.', 'Step'),
    'fr': ('Suivant', 'Retour', 'Envoyer', 'Obligatoire', 'En envoyant, vous acceptez la', 'politique de confidentialité', '/fr/politique-de-confidentialite/', 'Envoi…', "L'envoi a échoué. Réessayez ou écrivez-nous sur WhatsApp.", 'Étape'),
    'de': ('Weiter', 'Zurück', 'Senden', 'Pflichtfeld', 'Mit dem Absenden akzeptieren Sie die', 'Datenschutzerklärung', '/de/datenschutzrichtlinie/', 'Wird gesendet…', 'Senden fehlgeschlagen. Bitte erneut versuchen oder per WhatsApp schreiben.', 'Schritt'),
    'it': ('Avanti', 'Indietro', 'Invia', 'Obbligatorio', 'Inviando accetti la', 'informativa sulla privacy', '/it/politica-sulla-privacy/', 'Invio…', 'Invio non riuscito. Riprova o scrivici su WhatsApp.', 'Passo'),
    'nl': ('Volgende', 'Terug', 'Versturen', 'Verplicht', 'Door te versturen ga je akkoord met het', 'privacybeleid', '/nl/privacybeleid/', 'Versturen…', 'Versturen mislukt. Probeer opnieuw of stuur ons een WhatsApp.', 'Stap'),
    'ru': ('Далее', 'Назад', 'Отправить', 'Обязательно', 'Отправляя форму, вы принимаете', 'политику конфиденциальности', '/ru/', 'Отправка…', 'Не удалось отправить. Попробуйте ещё раз или напишите нам в WhatsApp.', 'Шаг'),
    'uk': ('Далі', 'Назад', 'Надіслати', "Обов'язково", 'Надсилаючи форму, ви приймаєте', 'політику конфіденційності', '/uk/', 'Надсилання…', 'Не вдалося надіслати. Спробуйте ще раз або напишіть нам у WhatsApp.', 'Крок'),
}
HIDDEN = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'ad_id', 'adgroup_id',
          'campaign_id', 'first_source', 'first_medium', 'first_landing', 'first_referrer', 'first_ts', 'referrer', 'landing', 'ga_client_id']

def e(s):
    return html.escape(s or '', quote=True)

def md(s):
    """Texto de Typeform: *negrita* y saltos de línea."""
    t = e(s).replace('\n', '<br>')
    return re.sub(r'\*(.+?)\*', r'<strong>\1</strong>', t)

def resolve_id(tf_id):
    tf_id = LIVE.get(tf_id, tf_id)
    return ROTOS.get(tf_id, tf_id)

def render(tf_id, lang, page_path, uid=''):
    fid = resolve_id(tf_id)
    f = TF.get(fid) or TF['iOSo1PBX']
    ui = UI.get(lang, UI['es'])
    uid = uid or hashlib.sha1((fid + page_path).encode()).hexdigest()[:6]
    steps = []
    fields = f['fields']
    i = 0
    n_q = sum(1 for x in fields if x['type'] not in ('statement', 'contact_info') and x['lvl'] == 0) + sum(1 for x in fields if x['type'] == 'contact_info')
    welcome = f.get('welcome') or []
    if welcome and welcome[0]:
        steps.append(f'<div class="bf-step bf-intro" data-step><p class="bf-title">{md(welcome[0])}</p>'
                     f'<div class="bf-nav"><button type="button" class="bf-next">{e(ui[0])}</button></div></div>')
    qn = 0
    while i < len(fields):
        x = fields[i]
        if x['lvl'] > 0:
            i += 1; continue
        t = x['type']; title = x['title'] or ''
        req = ' required' if x.get('required') else ''
        name = 'q_' + re.sub(r'[^a-z0-9]+', '_', unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower())[:48].strip('_')
        if t == 'statement':
            steps.append(f'<div class="bf-step bf-statement" data-step><p class="bf-text">{md(title)}</p>'
                         f'<div class="bf-nav"><button type="button" class="bf-back">{e(ui[1])}</button><button type="button" class="bf-next">{e(ui[0])}</button></div></div>')
            i += 1; continue
        qn += 1
        head = f'<p class="bf-count">{qn} / {n_q}</p><label class="bf-title" for="{uid}-{name}">{md(title)}</label>' if t not in ('multiple_choice', 'picture_choice', 'contact_info') else f'<p class="bf-count">{qn} / {n_q}</p><legend class="bf-title">{md(title)}</legend>'
        if t in ('multiple_choice', 'picture_choice'):
            opts = []
            seen = set()
            for j, c in enumerate(x['choices']):
                if c in seen: continue
                seen.add(c)
                opts.append(f'<label class="bf-choice"><input type="radio" name="{name}" value="{e(c)}"{req if j == 0 else ""}><span>{e(c)}</span></label>')
            body = f'<fieldset class="bf-fieldset">{head}<div class="bf-choices">{"".join(opts)}</div></fieldset>'
        elif t == 'contact_info':
            subs = []
            k = i + 1
            while k < len(fields) and fields[k]['lvl'] > 0:
                s = fields[k]; stitle = s['title']
                typ = {'email': 'email', 'phone_number': 'tel'}.get(s['type'], 'text')
                sname = {'First name': 'nombre', 'Last name': 'apellidos', 'Phone number': 'telefono', 'Email': 'email'}.get(stitle, 'q_' + re.sub(r'[^a-z0-9]+', '_', stitle.lower()))
                lbl = {'First name': 'Nombre', 'Last name': 'Apellidos', 'Phone number': 'Teléfono', 'Email': 'Email'}.get(stitle, stitle)
                ac = {'nombre': 'given-name', 'apellidos': 'family-name', 'telefono': 'tel', 'email': 'email'}.get(sname, 'on')
                subs.append(f'<label class="bf-sub"><span>{e(lbl)}</span><input type="{typ}" name="{sname}" autocomplete="{ac}"{" required" if s.get("required") else ""}></label>')
                k += 1
            desc = ''
            body = f'<fieldset class="bf-fieldset">{head}{desc}<div class="bf-subs">{"".join(subs)}</div></fieldset>'
            i = k - 1
        else:
            typ = {'email': 'email', 'phone_number': 'tel'}.get(t, 'text')
            fname = {'email': 'email', 'phone_number': 'telefono'}.get(t, 'nombre' if 'llamas' in title.lower() else name)
            ac = {'email': 'email', 'telefono': 'tel', 'nombre': 'name'}.get(fname, 'on')
            body = f'{head}<input class="bf-input" id="{uid}-{name}" type="{typ}" name="{fname}" autocomplete="{ac}"{req}>'
        last = i >= len(fields) - 1 or all(y['lvl'] > 0 for y in fields[i + 1:])
        nav = (f'<div class="bf-nav">' + (f'<button type="button" class="bf-back">{e(ui[1])}</button>' if steps else '') +
               (f'<button type="submit" class="bf-submit">{e(ui[2])}</button>' if last else f'<button type="button" class="bf-next">{e(ui[0])}</button>') + '</div>')
        legal = f'<p class="bf-legal">{e(ui[4])} <a href="{PRIV.get(lang, "/politica-de-privacidad/")}">{e(ui[5])}</a>.</p>' if last else ''
        steps.append(f'<div class="bf-step" data-step>{body}{legal}{nav}</div>')
        i += 1
    hidden = ''.join(f'<input type="hidden" name="{h}">' for h in HIDDEN)
    thanks = f.get('thanks_text') or ''
    if thanks.startswith('http') or '{{' in thanks:
        thanks = ''
    redirect = REDIRECT.get(fid, '')
    return (f'<form class="belba-form" id="form-{uid}" data-belba-form data-form-id="tf-{fid}" data-form-name="{e(f["title"])}" '
            f'data-redirect="{e(redirect)}" data-error="{e(ui[8])}" data-sending="{e(ui[7])}" action="/form-handler.php" method="post" novalidate>'
            f'<input type="hidden" name="form_id" value="tf-{fid}"><input type="hidden" name="form_name" value="{e(f["title"])}">'
            f'<input type="hidden" name="page" value="{e(page_path)}"><input type="hidden" name="lang" value="{lang}">{hidden}'
            f'<div class="hp-field" aria-hidden="true"><label>No rellenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
            f'<div class="bf-progress" aria-hidden="true"><span></span></div>'
            f'{"".join(steps)}'
            f'<div class="bf-thanks" hidden><p>{md(thanks) if thanks else "✓"}</p></div>'
            f'<p class="bf-error" role="alert" hidden></p></form>')

if __name__ == '__main__':
    print(render('01KEF5HK8JC590A93QPQFYQ2FM', 'es', '/test-paciente/')[:3000])
