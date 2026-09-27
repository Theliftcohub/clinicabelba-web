import { allPages, SITE } from '../lib/data.mjs';
export async function GET() {
  const es = allPages().filter((d) => d.lang === 'es' && !/noindex/i.test(d.seo.robots || ''));
  const pages = es.filter((d) => d.kind === 'page').sort((a, b) => a.path.localeCompare(b.path));
  const posts = es.filter((d) => d.kind === 'post').sort((a, b) => a.path.localeCompare(b.path));
  const line = (d) => `- [${d.seo.title}](${SITE.domain}${d.path})${d.seo.description ? ': ' + d.seo.description : ''}`;
  const body = `# ${SITE.name}\n\n> Clínica de cirugía plástica, estética y reparadora en Barcelona (Via Augusta, 281, planta 4A, 08017 Barcelona · +34 613 16 34 47). Cirujanos certificados SECPRE; intervenciones en el Grupo Teknon y el Hospital Tres Torres.\n\nLa web está disponible en español (principal), catalán, inglés, francés, alemán, italiano, neerlandés, ruso y ucraniano.\n\n## Páginas\n${pages.map(line).join('\n')}\n\n## Artículos\n${posts.map(line).join('\n')}\n`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
