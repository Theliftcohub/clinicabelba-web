import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://clinicabelba.com',
  trailingSlash: 'always',
  output: 'static',
  build: { format: 'directory', inlineStylesheets: 'never' },
  compressHTML: true,
});
