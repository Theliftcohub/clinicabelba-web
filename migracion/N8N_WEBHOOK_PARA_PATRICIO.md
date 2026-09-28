# Webhook de n8n para los formularios de clinicabelba.com (para Patricio)

La web nueva (estática) manda **todos** los leads de formularios a un webhook de n8n desde el servidor (`/form-handler.php` en Plesk). El navegador nunca ve la URL del webhook.

## Qué necesito
1. Un webhook **POST** en n8n (producción), p. ej. `.../webhook/belba-web-lead`.
2. Opcional pero recomendado: una cabecera secreta `X-Belba-Token` para rechazar lo que no venga de la web.
3. Que el flujo responda **2xx** si ha recibido el lead. Si responde otra cosa o tarda más de 8 s, la web envía el lead por email a los destinatarios de siempre (no se pierde nada).

La URL y el token se guardan en Plesk en `secrets/smtp.php`, un nivel por encima de `httpdocs`, nunca en el repo:
```php
<?php
define('N8N_WEBHOOK_URL', 'https://…/webhook/belba-web-lead');
define('N8N_WEBHOOK_TOKEN', '…');
// y el SMTP de respaldo:
define('SMTP_HOST', '…'); define('SMTP_PORT', 587); define('SMTP_USER', '…'); define('SMTP_PASS', '…'); define('SMTP_SEGURIDAD', 'tls');
```

## Qué llega (JSON)
```json
{
  "form_id": "tf-eQ3VBLE2",                 // tf-* = antiguo Typeform; e2de0b0, 5ff55c52... = formularios de Elementor
  "form_name": "Paciente ideal",
  "page": "https://clinicabelba.com/test-paciente/",
  "lang": "es",
  "datos": { "nombre": "…", "apellidos": "…", "telefono": "…", "email": "…",
             "q_que_intervencion_te_estas_planteando_principalmente": "Liposucción", "...": "..." },
  "atribucion": {
    "utm_source": "", "utm_medium": "", "utm_campaign": "", "utm_term": "", "utm_content": "",
    "gclid": "", "fbclid": "", "ad_id": "", "adgroup_id": "", "campaign_id": "",
    "first_source": "google.com", "first_medium": "organic",           // primera visita (90 días)
    "first_landing": "/aumento-pecho-barcelona/", "first_referrer": "https://www.google.com/", "first_ts": "2026-09-28T07:41:14Z",
    "referrer": "", "landing": "/test-paciente/", "ga_client_id": "123456789.1700000000"
  },
  "ip": "…", "user_agent": "…", "fecha": "2026-09-28T09:41:14+02:00",
  "destinatarios": ["info@clinicabelba.com"]                          // a quién iba el email en WordPress
}
```
`first_medium` puede ser: `organic` (buscadores), `ai` (ChatGPT, Perplexity, Gemini…), `social`, `referral`, `cpc` (gclid), `paid_social` (fbclid), `(none)` (directo) o el `utm_medium` de la campaña.

## Qué debería hacer el flujo
1. Crear o actualizar el lead en **Kommo**: nombre, teléfono, email, fuente = `first_source`/`first_medium`, UTM y gclid en campos, formulario y página en la nota.
2. Avisar a los destinatarios de `destinatarios` (sustituye al email de WordPress).
3. Responder 200.

## Formularios y preguntas
Están en `migracion/typeform_forms.json` (5 antiguos Typeform) y `migracion/forms_elementor.json` (los de Elementor). Cada campo llega con su nombre en `datos`.
