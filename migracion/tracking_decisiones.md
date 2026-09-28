# Medición: decisiones para la web nueva (27/09/2026)

Fuente: GTM en vivo (cuenta "Clínica Belba Web", leída en el navegador) y `tracking.json` de la extracción.

## Decisión: la web nueva carga SOLO GTM-TCR5FXL
| Contenedor | Qué es | Decisión |
|---|---|---|
| **GTM-TCR5FXL** "clinicabelba.com" | Contenedor de Belba: 52 etiquetas, 31 activadores, versión 62 (publicada el 27/09/2026 por benitezjcruz@gmail.com) | **Se mantiene** |
| GTM-M6RC6ST "felixchavarria.es" | Contenedor de **otra web** (felixchavarria.es). Envía GA4 **G-JPN7CS51KW**, dos píxeles de Facebook y "Vinculación de conversiones" en todas las páginas | **Se retira** de clinicabelba.com |

Por qué se retira M6RC6ST: en clinicabelba.com mete el tráfico de Belba en la propiedad GA4 de felixchavarria.es y duplica los píxeles de Meta en cada página vista. Sus activadores dependen de clases del tema antiguo (`bt_bb_button_text`, `wpcf7-submit`) que ya no existen en Belba, así que sus eventos no aportan nada. Si alguien usa G-JPN7CS51KW para medir Belba, que lo diga antes del DNS.

## Lo que la web nueva TIENE que conservar para que TCR5FXL siga disparando
Los activadores de TCR5FXL leen el DOM. Si esto cambia, las conversiones de Google Ads y los eventos de GA4 se pierden sin ningún error visible:

| Activador | Condición | Qué hay que conservar en el HTML |
|---|---|---|
| Click WA General | Click URL contiene `34936293550` (fuera de preserve/rino) | enlace de WhatsApp con ese número |
| Activador WhatsApp linkclick | Click URL contiene `34613163447` | enlace de WhatsApp con ese número |
| WA Felix | Click URL contiene `34936096252` | enlace con ese número donde exista hoy |
| Click - Whatsapp | Click URL contiene `whatsapp` | enlaces `api.whatsapp.com/send?phone=…` (no pasarlos a `wa.me` sin revisar) |
| Activador Tel | Click URL contiene `tel:` | enlaces `tel:` |
| Activador cita-banner / cita-header / cita-footer | Click ID = `cita-banner` / contiene `cita-header` / `cita-footer` | **mismos `id`** en los botones de cita |
| Activador PresupuestoExpress | Click URL contiene `consulta-online` | enlaces a las URLs de consulta online |
| Click - Botones | solo enlaces | — |
| Typeform (Belba iOSo1PBX, Felix vwHofvjc, Mike BdYhxQFV, Paciente Ideal eQ3VBLE2, Consulta Online tCXPyaGW) | evento personalizado + Page Path/URL | mismos embeds y enlaces de Typeform, con el dataLayer del embed |
| Activador Typeform Enviado | Page URL empieza por `https://clinicabelba.com/drdewevercirugiaplastica/gracias/?ref=` | la página de gracias con esa ruta exacta |
| Vista Gracias Felix | Page URL contiene `drfelixchavarriacirugiaplastica/gracias` | ídem |

Etiquetas base (All Pages): GA4 G-K8WB1WZK6H y G-8FPT6PRR5K, Google Ads AW-10839002536, remarketing y los píxeles de Meta.

## Consentimiento
- CMP actual: **Cookiebot**. La web nueva carga el banner **antes** que GTM, con Consent Mode v2 y todo en `denied` por defecto (ver `references/medicion-y-formularios.md` de la skill).
- Prueba manual en staging: sin aceptar cookies no debe salir ninguna etiqueta.

## Problemas detectados en TCR5FXL (no se tocan en la migración: posible siguiente paso)
- **Píxeles de Meta duplicados en All Pages**: "Pixel Belba", "Pixel Belba 9420", "FacebookPixel_Belba", "Meta Pixel - Page View", "Pixel Meta 2962518767276471", "FacebookPixel_Mike" y "Pixel Felix". Seguramente cuentan varias veces cada PageView.
- Dos GA4 en todas las páginas (G-K8WB1WZK6H y G-8FPT6PRR5K), y "GA4 - G-K8WB1WZK6H" aparece dos veces (como etiqueta de Google y en "Initialization").
- La versión 62 la publicó hoy **benitezjcruz@gmail.com**. Confirmad que es alguien del equipo.
- El contenedor ha llegado al límite de áreas de trabajo (quedan 0).

## Paridad de IDs con la web vieja (validador, 28/09)
| ID en la web vieja | Cómo se cargaba | En la web nueva |
|---|---|---|
| GTM-TCR5FXL | snippet en `<head>` | **igual** (Base.astro) |
| GTM-M6RC6ST | snippet en `<head>` | **retirado** (contenedor de felixchavarria.es, ver arriba) |
| G-K8WB1WZK6H | `gtag.js` directo en el HTML (plugin) **y** etiqueta en TCR5FXL | solo vía GTM TCR5FXL (evita el doble conteo) |
| 1101212624029420 (píxel de Meta) | plugin PixelYourSite **y** etiqueta "Pixel Belba 9420" en TCR5FXL | solo vía GTM TCR5FXL (evita el doble conteo) |
| G-ED | falso positivo del extractor: bytes de una imagen en caché, no es un ID | — |
| analytics.ahrefs.com | script directo | retirado: Ahrefs Web Analytics no se usa para decisiones (Windsor/GA4). Si se quiere, se añade como etiqueta en GTM |

## Formularios nativos (28/09): qué cambia en GTM antes del DNS
Los Typeform se sustituyen por formularios nativos en el propio dominio. Motivo: con Typeform (iframe de otro dominio) GA4 no atribuía bien los leads, sobre todo el orgánico.

Todos los formularios de la web (nativos y los de Elementor que se conservan) lanzan **un único evento**:
```js
dataLayer.push({ event: 'lead_form_submit', form_id, form_name, form_page, form_lang, lead_source, lead_medium })
```
Hay que hacer esto en TCR5FXL (en un área de trabajo nueva, publicar el día del cambio de DNS):
1. Variables de capa de datos: `form_id`, `form_name`, `form_page`, `lead_source`, `lead_medium`.
2. Activador "Evento personalizado = lead_form_submit".
3. Etiqueta GA4 `generate_lead` (parámetros: form_id, form_name, form_page) y marcarlo como **evento clave** en GA4.
4. Conversión de Google Ads (AW-10839002536) y evento `Lead` de Meta con ese mismo activador.
5. Retirar los activadores de Typeform (`Activador Typeform Enviado`, eventos del embed) cuando el DNS ya apunte a la web nueva. Las páginas de gracias del Dr. Dewever (`/drdewevercirugiaplastica/gracias/?ref=form`) y del Dr. Chavarría (`/drfelixchavarriacirugiaplastica/gracias/`) se mantienen: el formulario redirige ahí, así que sus activadores actuales siguen disparando.

Hallazgo: el Typeform del Dr. Dewever (BdYhxQFV) redirigía al terminar a **recomendado.cirujanoplasticogirona.com**, un dominio ajeno. El formulario nativo redirige a la página de gracias de clinicabelba.com.
