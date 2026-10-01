# Lanzamiento · sustituir el WordPress de clinicabelba.com por la web estática

Estado a 01/10/2026. Producción = el mismo servidor Plesk que hoy sirve el WordPress (theliftco.nubaltec.net, origen
49.12.238.251, detrás de Cloudflare). Como el servidor no cambia, **el DNS no se toca**: el cambio es de carpeta (document
root) dentro de Plesk, y la vuelta atrás es volver a apuntar al WordPress.

## Paquete
`npm run build` con `PUBLIC_ENTORNO=produccion` (o `scripts/pipeline.sh` con `ENT=produccion`). El zip del 01/10 está en
`C:\Users\Usuario\Documents\TRABAJO\clinicabelba-produccion-2026-10-01.zip` (2783 archivos, 124 MB). Contiene `.htaccess`,
`_astro/.htaccess`, `410.html`, `form-handler.php`, `robots.txt`, `sitemap.xml`, `llms.txt` y la clave de IndexNow.
Validado antes de empaquetar: 1354 URLs del inventario, 0 FAIL propios de la web, 0 enlaces internos rotos (ver CLAUDE.md,
«Validación completa en Windows»).

## 1 · Staging en el mismo Plesk (hoy mismo, media hora)
1. Plesk → suscripción clinicabelba.com → **Subdominios → añadir `staging.clinicabelba.com`** con document root propio
   (p. ej. `staging/`). En Cloudflare, registro A `staging` → 49.12.238.251 (nube gris, sin proxy, para no cachear).
2. Subir el zip al document root del subdominio y extraerlo (Plesk → Archivos → Subir → Extraer). Comprobar que
   `.htaccess` está en la raíz (el gestor de archivos oculta los que empiezan por punto: activar «mostrar ocultos»).
3. **Hosting → Apache & nginx**: Apache en «Proxy mode» (nginx delante). Si está «solo nginx», el `.htaccess` no se aplica.
4. **Hosting → PHP**: 8.1 o superior (para `form-handler.php`).
5. **Directorios protegidos con contraseña** sobre `/` del subdominio. Hasta que no esté protegido, no se enlaza a nadie.
6. Comprobación rápida con curl (debe dar lo que dice el `.htaccess`):
   ```
   curl -I -u usuario:clave https://staging.clinicabelba.com/abdominoplastia/          → 301 a /abdominoplastia-barcelona/
   curl -I -u usuario:clave https://staging.clinicabelba.com/ca/elementor-3065/        → 410
   curl -I -u usuario:clave "https://staging.clinicabelba.com/?p=16938"                → 301 al post
   curl -I -u usuario:clave https://staging.clinicabelba.com/wp-admin/                 → 410
   ```
7. Validación completa (la hace Claude; la contraseña va en una variable de entorno, nunca en el chat):
   ```
   set VALIDATOR_AUTH=usuario:clave
   python -X utf8 scripts/validate_migration.py migracion/inventory.json --base https://staging.clinicabelba.com --entorno staging --redirects public/_redirects --no-literal NO_LITERAL.md --i18n migracion/i18n-map.json --contract migracion/urls.csv --media migracion/media.json --report migracion/informe-staging.html
   ```
8. **Formularios con PHP real**: enviar el del hero, uno corto de landing (p. ej. /aumento-pecho-barcelona/) y el del
   Dr. Dewever (redirige a gracias). En los tres debe abrirse WhatsApp con los datos y, en el servidor, el handler debe
   responder `{"ok":true}`. Decisión Nicols 01/10: por ahora el lead llega por WhatsApp; el email de respaldo sigue con los
   destinatarios heredados del WordPress hasta que la clínica fije el suyo.

## 2 · Antes de cambiar (quién)
- [ ] Oscar valida la portada (diseño del 30/09) y `NO_LITERAL.md`. — Oscar
- [ ] GTM TCR5FXL: área de trabajo con el activador `lead_form_submit`, etiqueta `generate_lead` en GA4, conversión de Ads
      y evento Lead de Meta; se publica el día del cambio. Detalle en `migracion/tracking_decisiones.md`. — quien lleve GTM
- [ ] URLs finales de los anuncios activos (Google Ads, Meta) comprobadas contra `migracion/urls.csv`. — paid media
- [ ] Search Console verificada por DNS (propiedad de dominio) antes del cambio. — Nicols
- [ ] Copia completa del WordPress (archivos + base de datos `wordpress_3`) guardada fuera del hosting. — Nicols/Nubaltec
- [ ] Aviso a la clínica de la hora del cambio y de que desde ese momento los leads llegan por WhatsApp. — Nicols

## 3 · El cambio (10 minutos, reversible)
1. En Plesk, **no borrar nada**: renombrar `httpdocs` → `httpdocs_wp_2026-10-01` (el WordPress queda intacto, con su BD).
2. Crear `httpdocs` nuevo y extraer ahí el mismo zip validado en staging (o cambiar el document root del dominio a la
   carpeta de staging ya validada: es el camino más rápido y la vuelta atrás es cambiarlo de nuevo).
3. Crear `secrets/` un nivel por encima de `httpdocs` (vacío por ahora; ahí irán `smtp.php` y el webhook de n8n/Make).
4. Mismos ajustes que en staging: Proxy mode, PHP 8.1+, **sin** directorio protegido.
5. Cloudflare: purgar caché completa del dominio.
6. Comprobar en vivo: portada, una traducción, un 301, un 410, `robots.txt` (debe permitir), `sitemap.xml`, un formulario.
7. Validación de producción (Claude):
   ```
   python -X utf8 scripts/validate_migration.py migracion/inventory.json --base https://clinicabelba.com --entorno produccion --production --redirects public/_redirects --no-literal NO_LITERAL.md --i18n migracion/i18n-map.json --contract migracion/urls.csv --media migracion/media.json --report migracion/informe-produccion.html
   python -X utf8 scripts/indexnow.py --sitemap https://clinicabelba.com/sitemap.xml --key public/f6e9e3a09612dd99083a4a54ee825667acc960d96e04b21a689ddd68f2114954.txt
   ```
8. Sitemap enviado en Search Console y Bing (importar desde GSC). Publicar el área de trabajo de GTM.
9. Preview de Netlify protegida con contraseña o borrada.
10. `informe-produccion.html` como update en el item de Monday, mencionando a Oscar. Horas del día en el time-tracking.

**Vuelta atrás**: renombrar `httpdocs` → `httpdocs_static` y `httpdocs_wp_2026-10-01` → `httpdocs`, purgar Cloudflare.
Dos minutos; el WordPress y su base de datos no se han tocado.

## 4 · Seguimiento
Días 3, 7, 14, 30 y 90 según el playbook (`lanzamiento.md` de la skill): clics e impresiones por grupo de páginas en GSC
frente al mismo periodo del año anterior, cobertura del sitemap, errores de rastreo, conversiones, CWV y backlinks a 404
(Ahrefs a las 48 h). Recordatorios en el item de Monday.
