# Migración clinicabelba.com · Fases 0-1 (27/09/2026)

Item Monday: https://liftcorp.monday.com/boards/2067844042/pulses/13144641815
Datos vivos consultados hoy: sitio en vivo, Screaming Frog (export del equipo), GSC y GA4 vía Windsor (últimos 3 meses), Google Business Profile vía Windsor, Ahrefs (backlinks), Plesk (solo la vista de dominios).

## 1. Inventario
- **1.170 URLs HTML únicas** (sitemap 829 + API 178 + Screaming Frog 163), 2.022 medios y 95 metadescripciones vacías.
- 9 idiomas con TranslatePress: ES sin prefijo; ca, en, fr, de, it, nl, ru, uk con prefijo y **slugs traducidos**. El mapa de hreflang sale del export de Screaming Frog (`screamingfrog/hreflang.csv`).
- Sin spam ni indicios de hackeo en el contenido. El único aviso del detector (`/nl/rhinoplastiek-man-voor-en-na-verbeterd/`) es un falso positivo.
- 4 URLs del sitemap EN ya responden con 301: hay que sacarlas del sitemap y conservar esa 301.

## 2. Contrato de URLs (`urls.csv`): 1.335 filas
| Decisión | Filas |
|---|---|
| mantener | 1.137 |
| 301 | 163 (146 son redirecciones que ya existen hoy y siguen recibiendo clics o impresiones; 17 son archivos de autor y paginación) |
| REVISAR | 35 (bloquean el lanzamiento) |
| 410 | 0 |

Detalle de las REVISAR:
- **16 URLs que hoy dan 404 y Google sigue mostrando.** Ejemplos: `/en/rib-removal-surgery/`, `/en/tummy-tuck-recovery/` y `/en/what-is-bbl-brazilian-butt-lift/` (1.870 impresiones). También `/presupuesto/`, `/medicina-estetica/` y `/ca/botox/`, que tienen backlinks. Propuesta: 301 a su equivalente. Es SEO que hoy se está perdiendo.
- **3 páginas huérfanas que responden 200**: `/uk/liposuccion/`, `/ru/liposuccion/` y `/ca/liposuccio/`. Son slugs sin traducir o duplicados.
- **9 formularios de MetForm indexados por error.** Propuesta: 410.
- Los archivos de autor. `/author/webbelba/` es en realidad "Artículos del Dr. Mike Dewever" y recibe clics: propuesta, mantenerlo como página de autor.

## 3. Idiomas: datos para decidir
Clics de GSC en 3 meses: **ES 19.168 (79 %) · traducciones 5.042 (21 %)**.

| Idioma | Clics | De ellos, artículo "labios vaginales" | Resto (comercial) |
|---|---|---|---|
| en | 891 | 443 | 448 |
| ca | 245 | 37 | 208 |
| it | 1.269 | 1.109 | 160 |
| fr | 812 | 673 | 139 |
| ru | 1.333 | 1.196 | 137 |
| de | 235 | 146 | 89 |
| nl | 72 | 13 | 59 |
| uk | 185 | 162 | 23 |

- El **75 % del tráfico traducido es un solo artículo informativo** (labios vaginales).
- Conversiones web en GA4 de páginas traducidas en 3 meses: unas 6, frente a unas 95 en ES. La mayoría de key events de GA4 vienen de Calendly y Typeform, no de la web.
- Coste: cada idioma que se conserva son unas 88 páginas más que construir y validar, con hreflang recíproco.
- **Propuesta (decide Oscar):** mantener ES y EN (y CA si se quiere por marca local). El resto de idiomas pasa con 301 a su equivalente en ES. Excepción posible: conservar solo el artículo de labios en it, ru y fr si se valora su tráfico informativo.
- Ojo: WhatsApp y las llamadas podrían no estar medidas como key event. Conviene confirmarlo antes de dar por buenas las conversiones.

## 4. Medición y formularios
- **Dos contenedores GTM** (GTM-M6RC6ST y GTM-TCR5FXL), GA4 G-K8WB1WZK6H, píxel de Meta 1101212624029420 y Cookiebot. No hay etiqueta AW- en el HTML.
- Formularios detectados en 352 URLs. Hoy van a Kommo, pero desde fuera no se ve cómo (MetForm lo hace en el servidor). Sale del export SQL o de los ajustes de MetForm.
- Dos WhatsApp distintos en la web (+34 613… y +34 936…). La ficha de Google usa el 613 16 34 47.

## 5. NAP (Google Business Profile, vía Windsor)
- **Clínica Belba | Cirujanos plásticos**: Via Augusta, 281, planta 4A, 08017 Barcelona · 613 16 34 47 · L-J 10-14 y 16-20, V 10-14 · categoría "Clínica de cirugía plástica".
- La web configurada en la ficha es `http://www.clinicabelba.com/`: se cambia a `https://clinicabelba.com/` en el checklist previo al DNS.
- La ficha de Teknon (Marquesa de Vilallonga 12, consultorio 39) apunta a otra web, cirujanosplasticosteknon.es.

## 6. Servidor y técnica
- Plesk Obsidian en theliftco.nubaltec.net. IP de origen 49.12.238.251, usuario de sistema `clinicabelba`, BD `wp_ducla`. Hay además una BD `wordpress_3` sin asignar, que parece un resto.
- **La suscripción ocupa 33 GB** (seguramente backups o uploads) y comparte espacio con los subdominios preserve, presupuesto y rinoplastia, que **no se pueden romper** en la migración.
- `staging.clinicabelba.com` resuelve directo a la IP de origen: se salta Cloudflare y deja expuesto el origen.
- TTFB de 2,7 s en WordPress (sin caché de página). La versión estática lo resuelve.
- El login de WordPress está oculto (`/wp-admin` y `/wp-login.php` dan 404) y `xmlrpc.php` da 403.
- **AhrefsBot está bloqueado (403)**, así que los datos de Ahrefs sobre la web están desfasados. Googlebot, Bingbot, OAI-SearchBot y PerplexityBot entran bien.
- GSC ya está verificado por DNS (TXT google-site-verification en Cloudflare).

## 7. Pendiente para cerrar la fase 1
1. Decisión de idiomas (§3).
2. Firmar las 35 filas REVISAR.
3. Export SQL de `wp_ducla` (lo hace el equipo: Plesk → Databases → Export dump). Hace falta para el mapa de slugs, la integración MetForm→Kommo y el export de redirecciones.
4. Export JSON de los 2 GTM y decidir cuál queda.
5. Revisar los propietarios de GSC (alerta de junio).
