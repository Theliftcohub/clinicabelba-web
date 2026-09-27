import fs from 'node:fs';
import { SITE } from '../lib/data.mjs';
// Generado desde la plantilla de la agencia (assets/robots.txt.template). Nunca a mano.
export async function GET() {
  let body;
  if (SITE.entorno !== 'produccion') {
    body = 'User-agent: *\nDisallow: /\n';
  } else {
    body = fs.readFileSync('scripts/robots.txt.template', 'utf8')
      .split('\n').filter((l) => !l.startsWith('#')).join('\n').replace(/\n{3,}/g, '\n\n')
      .replace('{{SITEMAP_URL}}', `${SITE.domain}/sitemap.xml`);
  }
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
