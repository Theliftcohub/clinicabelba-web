# CLAUDE.md · Clínica Belba (clinicabelba.com)

Este archivo es el contrato del proyecto. Se lee al empezar cada sesión. Cuando cometas un error y lo corrijas, añade aquí la regla que lo evita. Cuando el usuario tome una decisión, apúntala aquí.

## Qué es este proyecto
Web estática de Clínica Belba migrada desde WordPress (Elementor + MetForm, Yoast SEO, TranslatePress) a Astro. Preview de aprobación en Netlify (noindex); producción en Plesk (Apache + nginx) detrás de Cloudflare. Repositorio: PENDIENTE (GitHub privado de The Lift). Sin CMS: el contenido vive en `src/content/` y se edita con Claude Code. Agencia: The Lift Co. Playbook: skill `migracion-wp-theliftv2`. Item Monday: https://liftcorp.monday.com/boards/2067844042/pulses/13144641815

## Decisiones fijas
- Dominio canónico: `https://clinicabelba.com/` (sin www, barra final: sí). Cloudflare delante: el DNS se cambia en Cloudflare.
- Idiomas actuales: es (por defecto, sin prefijo), ca, en, fr, de, it, nl, ru, uk con prefijo `/xx/`. Slugs traducidos: sí (TranslatePress). **Qué idiomas se conservan: PENDIENTE, se decide con datos de GSC + Ahrefs por idioma (decisión Oscar 27/09).**
- Tipo de negocio para schema: MedicalClinic (confirmar sede principal y NAP con la ficha de Google Business Profile).
- Formularios: hoy MetForm → Kommo (integración a replicar y probar antes del DNS; detalle PENDIENTE).
- Analítica actual: GTM-M6RC6ST + GTM-TCR5FXL (dos contenedores: decidir cuál queda), GA4 G-K8WB1WZK6H, píxel de Meta, Cookiebot como CMP.
- Política de bots de IA en robots.txt: permitir bots de búsqueda; bots de entrenamiento: permitir (por defecto, pendiente confirmar).
- Fecha de lanzamiento prevista: PENDIENTE.
- Datos médicos en schema (colegiado, credenciales): solo si figuran literalmente en la web.

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

## Errores ya cometidos y sus reglas
<!-- fecha · qué pasó · regla -->
- 27/09 · `/wp-admin` devuelve 404 (login oculto por plugin de seguridad) · no dar por roto el WordPress; pedir la URL de login real.

## Modelos
Opus para fases 0-2 y decisiones de arquitectura. Sonnet para fases 3-7.
