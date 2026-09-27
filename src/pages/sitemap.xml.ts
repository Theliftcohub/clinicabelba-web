import { allPages, SITE, HREFLANG, LANGS } from '../lib/data.mjs';
// Un único sitemap con alternates hreflang. Solo URLs indexables.
export async function GET() {
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const rows = allPages()
    .filter((d) => !/noindex/i.test(d.seo.robots || ''))
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((d) => {
      const alts = d.alternates || {};
      const links = LANGS.filter((l) => alts[l]).map((l) => `<xhtml:link rel="alternate" hreflang="${HREFLANG[l]}" href="${esc(SITE.domain + alts[l])}"/>`).join('');
      const xd = alts.es ? `<xhtml:link rel="alternate" hreflang="x-default" href="${esc(SITE.domain + alts.es)}"/>` : '';
      const lm = d.post?.modified ? `<lastmod>${String(d.post.modified).slice(0, 10)}</lastmod>` : '';
      return `<url><loc>${esc(SITE.domain + d.path)}</loc>${lm}${links}${xd}</url>`;
    });
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${rows.join('\n')}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
