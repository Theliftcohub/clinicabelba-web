# Lanzamiento · sustituir el WordPress de clinicabelba.com por la web estática

Estado a 01/10/2026. Producción = el mismo servidor Plesk que hoy sirve el WordPress (theliftco.nubaltec.net, origen
49.12.238.251, detrás de Cloudflare). Como el servidor no cambia, **el DNS no se toca**: el cambio es de carpeta (document
root) dentro de Plesk, y la vuelta atrás es volver a apuntar al WordPress.

**Decisión Nicols 01/10: sin staging, directo a clinicabelba.com.** El playbook de la agencia pide un staging con
contraseña para probar los formularios con PHP real antes del cambio; se asume el riesgo y, a cambio, la primera prueba
de formulario se hace en los cinco minutos siguientes al cambio (paso 3.6), con la vuelta atrás preparada.

## Paquete
`npm run build` con `PUBLIC_ENTORNO=produccion` (o `scripts/pipeline.sh` con `ENT=produccion`). El zip del 01/10 está en
`C:\Users\Usuario\Documents\TRABAJO\clinicabelba-produccion-2026-10-01.zip` (2783 archivos, 124 MB). Contiene `.htaccess`,
`_astro/.htaccess`, `410.html`, `form-handler.php`, `robots.txt`, `sitemap.xml`, `llms.txt` y la clave de IndexNow.
Validado antes de empaquetar: 1354 URLs del inventario, 0 FAIL propios de la web, 0 enlaces internos rotos (ver CLAUDE.md,
«Validación completa en Windows»).

## 1 · Antes de cambiar (quién)
- [ ] Oscar valida la portada (diseño del 30/09) y `NO_LITERAL.md`. — Oscar
- [ ] GTM TCR5FXL: área de trabajo con el activador `lead_form_submit`, etiqueta `generate_lead` en GA4, conversión de Ads
      y evento Lead de Meta; se publica justo después del cambio. Detalle en `migracion/tracking_decisiones.md`. — quien lleve GTM
- [ ] URLs finales de los anuncios activos (Google Ads, Meta) comprobadas contra `migracion/urls.csv`. — paid media
- [ ] Search Console verificada por DNS (propiedad de dominio) antes del cambio. — Nicols
- [ ] Copia completa del WordPress (archivos + base de datos `wordpress_3`) guardada fuera del hosting. — Nicols/Nubaltec
- [ ] Aviso a la clínica de la hora del cambio y de que desde ese momento los leads llegan por WhatsApp. — Nicols
- [ ] Hora del cambio fuera del horario de la clínica (mañana temprano o tarde-noche), con alguien que pueda probar un
      formulario desde el móvil. — Nicols

## 2 · Preparar en el servidor, sin tocar la web en vivo (15 minutos)
1. Plesk → suscripción clinicabelba.com → Archivos. **No borrar ni mover `httpdocs` todavía.**
2. Crear la carpeta `httpdocs_nuevo` al mismo nivel que `httpdocs`, subir el zip y extraerlo dentro.
3. Comprobar que `httpdocs_nuevo/.htaccess` y `httpdocs_nuevo/_astro/.htaccess` existen (activar «mostrar archivos
   ocultos» en el gestor de archivos) y que `index.html`, `form-handler.php` y `410.html` están en la raíz, no en una
   subcarpeta `dist/`.
4. Crear `secrets/` al mismo nivel que `httpdocs` (vacío por ahora; ahí irán `smtp.php` y el webhook de n8n/Make).
5. **Hosting → Apache & nginx**: Apache en «Proxy mode» (nginx delante). Si está «solo nginx», el `.htaccess` no se aplica
   y las 4.800 redirecciones no funcionan. Anotar cómo está antes de cambiar nada.
6. **Hosting → PHP**: 8.1 o superior.
7. Cloudflare: modo desarrollo activado (3 horas sin caché) para no servir el WordPress cacheado tras el cambio.

## 3 · El cambio (un minuto, reversible)
1. Renombrar `httpdocs` → `httpdocs_wp_2026-10-01` (el WordPress queda intacto, con su base de datos).
2. Renombrar `httpdocs_nuevo` → `httpdocs`. Desde este segundo la web nueva está en vivo.
3. Comprobar en el navegador (ventana privada): portada, `/de/`, `/aumento-pecho-barcelona/`, `/blog/`, `/robots.txt`
   (debe permitir), `/sitemap.xml`.
4. Comprobar con curl que Apache aplica el `.htaccess`:
   ```
   curl -I https://clinicabelba.com/abdominoplastia/        → 301 a /abdominoplastia-barcelona/
   curl -I https://clinicabelba.com/ca/elementor-3065/      → 410
   curl -I "https://clinicabelba.com/?p=16938"              → 301 al post
   curl -I https://clinicabelba.com/wp-admin/               → 410
   ```
   Si el 301 o el 410 no salen, es el modo de nginx/Apache del paso 2.5: corregirlo o volver atrás.
5. Cloudflare: purgar toda la caché.
6. **Primera prueba real de formulario (antes de 5 minutos)**: el del hero desde un móvil. Debe abrirse WhatsApp con los
   datos y el formulario mostrar el gracias. Si la web muestra «No se ha podido enviar», el handler ha fallado: revisar
   la versión de PHP (paso 2.6); WhatsApp se abre igual, el lead no se pierde.
7. Validación de producción y aviso a buscadores (Claude):
   ```
   python -X utf8 scripts/validate_migration.py migracion/inventory.json --base https://clinicabelba.com --entorno produccion --production --redirects public/_redirects --no-literal NO_LITERAL.md --i18n migracion/i18n-map.json --contract migracion/urls.csv --media migracion/media.json --report migracion/informe-produccion.html
   python -X utf8 scripts/indexnow.py --sitemap https://clinicabelba.com/sitemap.xml --key public/f6e9e3a09612dd99083a4a54ee825667acc960d96e04b21a689ddd68f2114954.txt
   ```
8. Sitemap enviado en Search Console y Bing (importar desde GSC). Publicar el área de trabajo de GTM.
9. Preview de Netlify protegida con contraseña o borrada.
10. `informe-produccion.html` como update en el item de Monday, mencionando a Oscar. Horas del día en el time-tracking.

**Vuelta atrás**: renombrar `httpdocs` → `httpdocs_static` y `httpdocs_wp_2026-10-01` → `httpdocs`, purgar Cloudflare.
Un minuto; el WordPress y su base de datos no se han tocado. Las carpetas antiguas se conservan al menos 30 días.

## 4 · Seguimiento
Días 3, 7, 14, 30 y 90 según el playbook (`lanzamiento.md` de la skill): clics e impresiones por grupo de páginas en GSC
frente al mismo periodo del año anterior, cobertura del sitemap, errores de rastreo, conversiones, CWV y backlinks a 404
(Ahrefs a las 48 h). Recordatorios en el item de Monday.
