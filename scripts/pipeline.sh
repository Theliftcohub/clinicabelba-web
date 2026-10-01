#!/usr/bin/env bash
# Regenera todo desde la caché del WordPress. Uso: scripts/pipeline.sh [preview|staging|produccion]
set -euo pipefail
cd "$(dirname "$0")/.."
ENT="${1:-preview}"
rm -rf src/content/pages
python3 scripts/convert.py > migracion/convert.out 2>&1 && tail -1 migracion/convert.out
python3 scripts/fetch_media.py | tail -1
python3 scripts/build_footer.py
python3 scripts/postprocess.py | head -3
python3 scripts/fix_lang.py | tail -1
python3 scripts/fix_alternates.py
python3 scripts/build_blog.py
python3 scripts/fix_srcset.py
python3 scripts/home_nueva.py
python3 scripts/build_assets.py
python3 scripts/build_form_handler.py
PUBLIC_ENTORNO="$ENT" npx astro build 2>&1 | tail -1
python3 scripts/build_redirects.py migracion/inventory.json --new-routes dist/ --target both --domain clinicabelba.com \
  --contract migracion/urls.csv --media migracion/media.json --map migracion/url-map.csv --public public --sin-rss 2>&1 | tail -3 || true
python3 scripts/fix_htaccess.py
cp public/.htaccess public/_redirects public/_headers dist/
cp dist/410/index.html dist/410.html
mkdir -p dist/_astro && cp public/_astro/.htaccess dist/_astro/ 2>/dev/null || true
echo "listo: dist/ ($ENT)"
