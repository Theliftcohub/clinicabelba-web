# CLAUDE.md · Clínica Belba (clinicabelba.com)

Este archivo es el contrato del proyecto. Se lee al empezar cada sesión. Cuando cometas un error y lo corrijas, añade aquí la regla que lo evita. Cuando el usuario tome una decisión, apúntala aquí.

## Qué es este proyecto
Web estática de Clínica Belba migrada desde WordPress (Elementor + MetForm, Yoast SEO, TranslatePress) a Astro. Preview de aprobación en Netlify (noindex); producción en Plesk (Apache + nginx) detrás de Cloudflare. Repositorio: https://github.com/Theliftcohub/clinicabelba-web (privado). Sin CMS: el contenido vive en `src/content/` y se edita con Claude Code. Agencia: The Lift Co. Playbook: skill `migracion-wp-theliftv2`. Item Monday: https://liftcorp.monday.com/boards/2067844042/pulses/13144641815

## Decisiones fijas
- Dominio canónico: `https://clinicabelba.com/` (sin www, barra final: sí). Cloudflare delante: el DNS se cambia en Cloudflare.
- Idiomas: se conservan LOS 9 (decisión Oscar 27/09, vistos los datos de GSC): es (por defecto, sin prefijo), ca, en, fr, de, it, nl, ru, uk con prefijo `/xx/`. Slugs traducidos: sí (TranslatePress). Mapa en `migracion/i18n-map.json`. hreflang recíproco + x-default → es.
- Tipo de negocio para schema: MedicalClinic (confirmar sede principal y NAP con la ficha de Google Business Profile).
- Formularios (decisión Oscar 28/09): **todos nativos, nada de Typeform**. Los 5 Typeform se rehacen como formularios por pasos con sus preguntas literales (`scripts/forms_native.py`, datos en `migracion/typeform_forms.json`); los de Elementor se conservan. Todos envían a `/form-handler.php` → **n8n** (webhook en `secrets/`, fuera del repo) y, si n8n falla o no está configurado, email a los destinatarios del WordPress. Nunca se pierde un lead: último recurso `secrets/leads-no-enviados.log`.
- Medición de leads: todos los formularios lanzan `dataLayer.push({event:'lead_form_submit', form_id, form_name, form_page, form_lang, lead_source, lead_medium})` y mandan a n8n la atribución (UTM, gclid, fbclid, ad_id, primera fuente/medio/landing/referrer de los últimos 90 días y client_id de GA4). En GTM hay que crear el activador de ese evento antes del DNS (ver `migracion/tracking_decisiones.md`).
- Hoy (WordPress) los formularios NO llegaban a Kommo: solo email (y el de las páginas de mama, solo a la base de datos). 1 de cada 6 emails fallaba.
- Analítica: solo GTM-TCR5FXL (M6RC6ST era de felixchavarria.es). GA4 y píxel de Meta solo vía GTM (antes se duplicaban por plugins). Cookiebot lo carga GTM, como hoy.
- Política de bots de IA en robots.txt: permitir bots de búsqueda; bots de entrenamiento: permitir (por defecto, pendiente confirmar).
- Fecha de lanzamiento prevista: PENDIENTE.
- Datos médicos en schema (colegiado, credenciales): solo si figuran literalmente en la web.

- Home nueva (decisión Oscar 28/09, a partir de su diseño de Figma; **28/09 tarde: pasa a ser LA PORTADA en los 9 idiomas**, `scripts/home_nueva.py` sobrescribe el doc de `/` y `/xx/` conservando title/description/canonical/alternates/schema del inventario). Hero = foto real de quirófano + asistente conversacional (Mujer/Hombre → `sel_persona` con valor fijo ES y etiqueta traducida → preguntas literales del Typeform "Belba Gral"), selector que filtra procedimientos y manda `home_selector` al dataLayer. Cero datos inventados. Textos ES originales; traducciones a 8 idiomas en `scripts/home_i18n.py` hechas por Claude, **pendientes de revisión de la clínica** (anotado en NO_LITERAL.md). Nombres de cirugías/páginas: del menú traducido del WordPress. Pendiente de la clínica: fotos de hombre y quirófano en alta resolución.
- Estilo global (decisión Oscar 28/09: "toda la web con el mismo estilo"): (1) pie compacto en todas las páginas y los 9 idiomas (`scripts/build_footer.py`, sustituye el pie del WP; el original queda en `layout/<lang>.json` → `footer_wp`); (2) tema CSS global en `build_assets.py` (botones, campos, tarjetas, acordeones, radios) sobre las clases `k-*`; solo presentación, textos y URLs intactos. Las plantillas de Elementor no se rehacen.
- 184 traducciones de páginas `noindex` no estaban en sitemap ni rastreo (solo en hreflang); se añadieron al inventario/contrato con la misma decisión que su versión ES (48 → 410, resto → mantener noindex). Entre ellas las páginas de gracias por idioma, que GTM usa como conversión.

## Reglas de contenido
1. Los textos son **literales** del WordPress. Cualquier cambio de texto se registra en `NO_LITERAL.md` (URL, campo, original, nuevo, motivo). Sin excepciones.
2. Las URLs no cambian. Si una URL nueva es inevitable, se añade a `migracion/urls.csv` y se regeneran las redirecciones.
3. Contenido eliminado o spam: 410 en el contrato. Nunca 301 a la portada.
4. Title, description, canonical y robots por página vienen del inventario (`migracion/inventory.json`). No se "mejoran" durante la migración.
5. Imágenes: siempre en el proyecto, WebP, con el alt original y el nombre de archivo original. Nunca enlazar a `clinicabelba.com/wp-content/`.
6. Nunca se responden ni se redactan contenidos médicos nuevos: la migración copia, no escribe.

## Arquitectura (no cambiar sin hablarlo)
- Una página = un JSON en `src/content/pages/<lang>/` con `path`, `seo`, `schema`, `breadcrumbs`, `blocks[]`.
- Un post = un `.md` en `src/content/posts/` con frontmatter completo (author, datePublished, dateModified).
- La plantilla solo reparte bloques. Toda la lógica de presentación está en `src/blocks/`.
- No crear componentes por página. Bloques nuevos solo si se usan en más de una página.
- Colores, tipografías y espaciados solo desde `src/styles/tokens.css`.
- Textos de interfaz por idioma en `src/i18n/ui.json`.

## Bloques disponibles
| Tipo | Campos | Variantes |
|---|---|---|
| `hero` | title, text, image, imageAlt, cta{text,href} | `imagen-derecha`, `fondo`, `simple` |
| `texto` | html | — |
| `tarjetas` | columns, items[{title,text,icon,href}] | — |
| `faq` | items[{q,a}] (FAQPage solo si ya existía) | — |
| `cta` | title, text, button{text,href} | `banda`, `caja` |
| `galeria` | images[{src,alt}] | — |
| `formulario` | name, fields[], destination | — |
| `lista-posts` | limit, category | — |

## Flujo de trabajo
- Un commit por página migrada: `feat(page): migrar /ruta/`.
- Antes de cada commit: `npm run build` sin errores y validación de enlaces.
- Credenciales solo en `.env` / `secrets/` (ignorados por git). Nunca leerlas en el chat ni imprimirlas.
- Medics no se toca.
- Los scripts de `scripts/` toman la raíz del repo de la variable `BELBA_ROOT` (por defecto `/home/claude/belba`, el contenedor Linux de Claude). En Windows: `BELBA_ROOT=$PWD python -X utf8 scripts/<script>.py` (sin `-X utf8`, Python abre los JSON en cp1252 y rompe los acentos).
- `scripts/rerender_forms.py` regenera in situ los formularios rehechos desde Typeform en todas las páginas (menos las portadas, que regenera `home_nueva.py`) sin rehacer el pipeline completo. Tras tocar `forms_native.py` o `forms_i18n.py`: ejecutarlo, luego `home_nueva.py`, luego `npm run build`.

## Errores ya cometidos y sus reglas
<!-- fecha · qué pasó · regla -->
- 27/09 · 4 páginas EN del hreflang están hoy en bucle de redirecciones (TranslatePress) · no copiar redirecciones del WP a ciegas: resolver siempre el destino final.
- 27/09 · Screaming Frog exporta URLs decodificadas y el sitemap en %xx · comparar siempre normalizado (unquote + lower).
- 27/09 · `/wp-admin` devuelve 404 (login oculto por plugin de seguridad) · no dar por roto el WordPress; pedir la URL de login real.
- 27/09 · La BD `wp_ducla` (14 tablas) resultó ser la del subsitio `/presupuesto/` (siteurl=home=`https://clinicabelba.com/presupuesto`), no la principal · antes de dar una BD de Plesk por buena, comprobar `siteurl`/`home` en `wp_options`, no solo el número de tablas. La BD real es `wordpress_3` (confirmado 28/09: siteurl=https://clinicabelba.com).
- 28/09 · CAÍDA DE LA WEB causada por Claude: cambié en Plesk la contraseña de `wordpress_5` para poder exportar; ese usuario es el que usa WordPress en `wp-config.php` → "Error establishing a database connection" · NUNCA cambiar la contraseña de un usuario de BD sin haber leído antes `wp-config.php` (DB_USER). Si Plesk no exporta, se pide a hosting o se usa otra vía; no se tocan credenciales en uso. Causa de fondo: tras la limpieza del hackeo de agosto alguien rotó la contraseña en MySQL y en wp-config.php sin pasar por Plesk, y Plesk se quedó con la vieja.
- 28/09 · El panel Plesk (theliftco.nubaltec.net) está detrás de Cloudflare y su WAF bloquea cualquier petición que lleve `wp-config.php` (el editor de archivos devuelve la página de Cloudflare en rojo) · para tocar wp-config.php entrar por la IP de origen `https://49.12.238.251:8443/` (aviso de certificado, cifrado igual). NUNCA por `http://…:8880` (va sin cifrar). Avisar a Nubaltec de que 8880 está abierto al exterior.
- 28/09 · Restos del hackeo de agosto en httpdocs: `_CUARENTENA_HACK_20260806/`, `hitam.html.quar0903`, `wp-singup.php` (0 B, 02/09), `mantenimiento.html`, `clinicabelba.com_all.zip` (5,1 GB) · no tocar en la migración; anotar como posible siguiente paso (limpieza + revisar wp-login.php/wp-signup.php modificados el 03/09).

- 28/09 · La fase 1 marcó `/test-paciente/` (y 4 traducciones) como 410 por el patrón `test-`, pero es el botón "Test paciente" del menú de todas las páginas · antes de un 410, comprobar que la URL no está enlazada desde cabecera, pie o páginas `mantener` (el conversor lo avisa como "enlace a URL 410").
- 30/09 · Los 5 formularios rehechos desde Typeform salían con las preguntas en ESPAÑOL en las 8 traducciones (29 páginas por idioma, 232 en total; el WordPress también los tenía solo en ES). Ahora `forms_native.py` muestra las preguntas traducidas (`scripts/forms_i18n.py`) y conserva los VALORES en ES para n8n · al añadir un formulario o una pregunta, ejecutar `python scripts/forms_i18n.py`: lista lo que falta por traducir (debe devolver `[]`). Cualquier texto de interfaz que se genere por script se comprueba en los 9 idiomas, no solo en ES.
- 30/09 · La cabecera de la home salía en dos filas y estrecha: su `doc.css` (el de `home_nueva.py`) no trae el CSS del kit de Elementor (contenedor de 1280 px) que sí llevan las páginas interiores · lo global (cabecera, pie) nunca depende del CSS de la página: va en `build_assets.py` EXTRA **y** en `public/css/site.css` (build_assets.py no se puede ejecutar fuera del contenedor Linux porque convert.py importa `pages`; se editan los dos a mano, idénticos). Cabecera: menú completo ≥1280 px (compacto 1280-1439), desplegable por debajo; en RU/UK desplegable por debajo de 1440. Al tocar el menú, comprobar solapes en los 9 idiomas (DE, FR, RU y UK son los más largos).
- 30/09 · El menú de escritorio no abría el 3.er/4.º nivel (Cirugía plástica → Cirugía de la mama → …): `overflow:hidden` en `.sub-menu` lo recortaba y Elementor fuerza `top:100%` a todo `ul` anidado · los submenús anidados se abren a la derecha (`top:0;left:100%`), sin overflow hidden. Al validar el menú, pasar el ratón hasta el último nivel, no solo el primero.
- 30/09 · Home "editorial premium" (decisión Nicols 30/09, tras rechazar dos pulidos parciales; **pendiente de validar por Oscar**, que fijó el diseño Figma el 28/09): `home_nueva.py` con estructura y CSS nuevos. Fondo marfil/arena (#F7F4EF/#EFE9E1), Montserrat 300 en títulos grandes, esquinas de 6 px, líneas finas, sin sombras ni bloques de color. Hero: texto + formulario sobre marfil y debajo la foto de quirófano a todo el ancho con los logos encima. Tarjetas de "Procedimientos" con FOTO (imagen propia de la página de destino, versión -800), numeración 01-06 y 01-03 de la filosofía por CSS (`counter`), NO en el HTML, para que el texto siga literal. Selector Mujer/Hombre = pestañas con subrayado (nada de píldora). Lipo HD, Blefaroplastia y Mentoplastia (lista Hombre) siguen con fotos de mujer y la foto de quirófano (682 px) se ve algo blanda a todo el ancho: faltan fotos de la clínica (ya anotado).
- 30/09 · Hero (referencia de Nicols, 30/09 tarde): H1 en Montserrat 800 a 76 px con las palabras "cirugía plástica" en turquesa (`HL` por idioma en `home_nueva.py`, solo un `<em>`; texto literal), antetítulo con el último tramo ("Cirujanos certificados SECPRE") como píldora, subtítulo en negrita, párrafo, botón grande turquesa `Solicita tu valoración médica →` (ancla a `#valoracion`), teléfono real en grande, fila de confianza (Google + "Excelente · N reseñas" literal del widget; avatares de los 4 médicos + "Nuestro equipo de cirujanos" enlazando a /cirujanos-plasticos-barcelona/) y píldoras de áreas. Columna derecha: slider en fundido (quirófano, consulta, Teknon; 4,5 s; se para con `prefers-reduced-motion`) con el formulario conversacional superpuesto debajo. Sin cifras inventadas: la referencia traía "4.9 · +380 reseñas", "4 cirujanos SECPRE", "valoración gratuita" y un teléfono falso; NO se copian.
- 30/09 noche (Nicols): (1) **Sin selector Mujer/Hombre en "Procedimientos"**: las 12 tarjetas (6 mujer + 6 hombre) en una sola rejilla de 6×2. El filtro sigue existiendo solo vía la pregunta del formulario del hero (`sel_persona` → oculta/muestra las píldoras de íntima/ginecomastia y manda `home_selector`). **Contradice la decisión de Oscar 28/09 (selector que filtra): que lo valide él.** (2) Secciones Procedimientos/Tratamientos/Equipo compactas: cabecera en una fila con línea inferior, fotos cuadradas o 4:3, menos padding (88 px). (3) Hero: píldoras en una línea, "Ver procedimientos" como enlace en la fila de confianza. (4) Cabecera global refinada: menú en minúsculas 14 px (solo CSS, el texto sigue literal), "Consulta online" píldora turquesa, "Test paciente" píldora con borde, barra sticky con desenfoque, desplegables BLANCOS (hay que anular con `!important` el `background-color:#008488` del kit en `.k-nav-menu--dropdown` y en `a.k-sub-item`).
- 30/09 · En móvil (390 px) RU/UK desbordaban por las tarjetas: un grid `1fr` no encoge por debajo del ancho de la palabra más larga ("Липосакция") · siempre `min-width:0` en los hijos del grid y `overflow-wrap:anywhere` en etiquetas cortas; validar el ancho de scroll en RU/UK, no solo en ES.
- 30/09 noche (2) (Nicols): hero a pantalla completa (`min-height:calc(100vh - 104px)`, slider 16:10, formulario cabe en 1440×900 y 1366×768 **sin** la caja "Vista previa", que solo existe en Netlify); equipo en tarjetas blancas con hover; aparición al hacer scroll (`IntersectionObserver` → `.rv.in`, escalonado con `--i`) y parallax suave en el slider del hero y en la foto de Teknon (rAF sobre `scroll`, `translate3d`); todo desactivado con `prefers-reduced-motion`. En el JS de la home NO declarar variables llamadas `sel` (existe la función `sel()` del selector): rompió todo el script hasta que lo detectó `final.mjs` (pageerror).
- 30/09 · Lección: cuando alguien dice "no me gusta el diseño", no retocar; preguntar dirección y alcance (AskUserQuestion) y rehacer. Dos pulidos parciales costaron más que un rediseño.
- 30/09 · Al comparar HTML antes/después, el número decorativo (01, 02…) puesto en el HTML rompe el "texto literal": los adornos van siempre por CSS (`::before` + `counter`).
- 30/09 noche (3) (Nicols, tras rechazar la banda del Teknon con tarjeta flotante; elegido con AskUserQuestion): **Presentación** a dos columnas (texto | foto 4:5), sin tarjeta ni desenfoque; **Equipo** en filas editoriales (foto cuadrada | nombre, cargo en versalitas y cita con filete turquesa | biografía íntegra), sin tarjetas; **Reseñas**: mismo widget vivo de Trustindex/Google, pie del widget oculto y nota «Excelente · N reseñas» en la cabecera de sección, tarjetas blancas sin avatares, a todo el ancho (hay que superar `.ti-widget-container:not(.ti-col-1) .ti-reviews-container{…!important}` con más especificidad); **Primer paso** sobre arena, formulario sin la pantalla de bienvenida (`forms_native.render(..., intro=False)`) y datos de contacto con icono por CSS; **mapa** sobre marfil. **Cabecera**: misma estructura, barra de 85 px (el `<a>` del logo era inline y sumaba 8 px: `display:block;line-height:0`), logo en alta resolución (`/images/2024/04/logo-clinica-belba.webp`, mismo diseño; anotado en NO_LITERAL), botón de idioma sin el rosa (`[type=button]:focus/hover{background:#c36}` del tema), «Test paciente» con borde fino turquesa, menú móvil como panel blanco con los dos botones (el kit fija colores con `!important` y 5 clases: las reglas móviles llevan el prefijo `header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown`).
- 30/09 · En una `<li>` con `display:grid`, cada hijo (incluido un nodo de texto suelto como « · ») es un ítem del grid y salta de fila · envolver el contenido en un `<span>`.
- 30/09 · Capturas locales en Windows: `node scripts/shots_home.mjs <carpeta>` (secciones y cabecera en varios anchos), `shots_menu.mjs` (desplegables, idioma, menú móvil) y `shots_mobile.mjs` (secciones a 390 px); sirven `dist/` en un puerto libre, no necesitan Apache. El fullPage de Playwright no carga las imágenes `loading=lazy` fuera de pantalla: para juzgar una sección, usar su captura por selector.
- 30/09 · Para localizar formularios en el HTML de las páginas no fiarse del orden de atributos: BeautifulSoup (convert.py) los ordena alfabéticamente y serializa los booleanos como `data-belba-form=""`.

## Modelos
Decisión Oscar 28/09: TODA la migración con Opus 5.5 (también fases 3-7). Sin subagentes.

## Reglas de copy (decisión Oscar 28/09)
- El equipo NO llama a los leads: les escribe para asesorarles. Nunca "te llamamos / te llama nuestro equipo"; siempre "nuestro equipo te escribirá para asesorarte".
- Home y landings "conversacionales": el visitante avanza respondiendo preguntas (formulario por pasos) y entra en Kommo vía n8n; todo lead lleva atribución orgánico/pago.
- En la web actual NO existe ningún logo de red.es/Kit Digital: solo la imagen "Financiado por la Unión Europea + Plan de Recuperación". Si hay que añadir red.es, la clínica tiene que enviar el logo.
- 28/09 · 549 imágenes con máscara circular de Elementor (`mask-image: url(.../plugins/elementor/assets/mask-shapes/circle.svg)`) salían invisibles: el conversor dejaba `url("")` y una máscara vacía oculta la imagen · los assets de plugins referenciados desde CSS se copian a `public/images/mask-shapes/` (convert.py `rewrite_url`). Al validar visualmente, mirar `mask-image` si una imagen "carga" pero no se ve.
- 28/09 · El acordeón clásico de Elementor abre el primer elemento con JS; en `<details>` hay que ponerlo `open` en el HTML y sincronizar `k-active` (site.js).
- 28/09 · H1: una página = un H1. `postprocess.py` degrada H1 repetidos a H2, promueve el primer H2 a H1 si no hay, y en páginas que solo son formulario añade un H1 oculto con el título. Todo anotado en NO_LITERAL.md (mismo texto, solo cambia la etiqueta).
- 28/09 · Validación local: Apache (:8443) se para cuando el contenedor se recicla → `service apache2 start` antes de validar; y no dar por terminada una validación por un `FIN` de una ejecución anterior (comparar fechas del log).

## Formularios conversacionales (28/09)
- Formularios largos de Elementor: site.js los convierte en pasos (pregunta primero, datos de contacto al final). Hoy todos los largos visibles son nativos; la mejora queda para cualquiera que se añada.
- Formularios cortos (nombre + teléfono, landings de cirugía): el lead se captura al instante y después se hace UNA pregunta opcional literal del formulario general ("¿Cuándo tienes pensado operarte?") → segundo POST `tipo: cualificacion` con el mismo `lead_ref`. En los 9 idiomas (traducciones en `home_i18n.FOLLOW`, las inyecta `build_assets.py` en site.js entre /*FOLLOW-START*/ y /*FOLLOW-END*/).
- Eventos: `lead_form_start`, `lead_form_submit`, `lead_form_qualify`, `home_selector`.
- Hallazgo: los formularios "Consulta online" del WordPress tienen en "Email 2" `trabajos@comp1.gestionespowerdns.com` (resto de la instalación de 2023, sin envíos en el log). La web nueva NO lo usa.
