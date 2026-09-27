// Carga los JSON de páginas y cabeceras/pies generados por scripts/convert.py
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PAGES_DIR = path.join(ROOT, 'src/content/pages');
const LAYOUT_DIR = path.join(ROOT, 'src/content/layout');

let _pages = null;
export function allPages() {
  if (_pages) return _pages;
  const out = [];
  for (const lang of fs.readdirSync(PAGES_DIR)) {
    const dir = path.join(PAGES_DIR, lang);
    if (!fs.statSync(dir).isDirectory()) continue;
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.json')) continue;
      const doc = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
      doc._file = `${lang}/${f}`;
      out.push(doc);
    }
  }
  _pages = out;
  return out;
}

const _layouts = {};
export function layoutFor(lang) {
  if (_layouts[lang]) return _layouts[lang];
  const fn = path.join(LAYOUT_DIR, `${lang}.json`);
  const fb = path.join(LAYOUT_DIR, `es.json`);
  _layouts[lang] = JSON.parse(fs.readFileSync(fs.existsSync(fn) ? fn : fb, 'utf8'));
  return _layouts[lang];
}

const _byPath = {};
export function pageByPath(p) {
  if (!Object.keys(_byPath).length) for (const d of allPages()) _byPath[decodeURIComponent(d.path).toLowerCase()] = d;
  return _byPath[decodeURIComponent(p).toLowerCase()];
}

export const SITE = {
  domain: 'https://clinicabelba.com',
  name: 'Clínica Belba',
  alternateName: 'Clinica Belba - Cirugía Plástica en Barcelona',
  logo: '/images/2024/12/clinica-belba-200.webp',
  gtm: 'GTM-TCR5FXL',
  entorno: process.env.PUBLIC_ENTORNO || 'preview',
};

export const LANGS = ['es', 'ca', 'en', 'fr', 'de', 'it', 'nl', 'ru', 'uk'];
export const HREFLANG = { es: 'es-ES', ca: 'ca', en: 'en-US', fr: 'fr-FR', de: 'de-DE', it: 'it-IT', nl: 'nl-NL', ru: 'ru-RU', uk: 'uk' };
export const LANG_NAME = { es: 'Spanish', ca: 'Catalan', en: 'English', fr: 'French', de: 'German', it: 'Italian', nl: 'Dutch', ru: 'Russian', uk: 'Ukrainian' };
export const FLAG = { es: 'es_ES', ca: 'ca', en: 'en_US', fr: 'fr_FR', de: 'de_DE', it: 'it_IT', nl: 'nl_NL', ru: 'ru_RU', uk: 'uk' };
