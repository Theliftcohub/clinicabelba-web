#!/usr/bin/env python3
"""Ajusta public/.htaccess para rutas no ASCII (ruso, ucraniano, acentos):
mod_rewrite compara el patrón con la ruta YA decodificada, así que el patrón se escribe en UTF-8;
y los destinos con %xx llevan [NE] para que Apache no los vuelva a codificar (%25d0...)."""
import os
import re
from urllib.parse import unquote
fn = os.path.join(os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', '.htaccess')
out = []; n1 = n2 = 0
for line in open(fn, encoding='utf-8'):
    m = re.match(r'^(RewriteRule\s+)(.+?)(\s+)(\S+)(\s+\[)([^\]]*)(\].*)$', line.rstrip('\n'))
    if m:
        pat, tgt, flags = m.group(2), m.group(4), m.group(6)
        if '%' in pat:
            pat = re.sub(r'(?:%[0-9A-Fa-f]{2})+', lambda mm: unquote(mm.group(0)), pat); n1 += 1
        pat = pat.replace(' ', '\\x20')
        if re.search(r'(?<!\\)%[0-9a-fA-F]{2}', tgt):
            tgt = re.sub(r'(?<!\\)%([0-9a-fA-F]{2})', r'\\%\1', tgt)  # %N es retro-referencia en mod_rewrite
            if 'NE' not in flags.split(','):
                flags += ',NE'
            n2 += 1
        line = m.group(1) + pat + m.group(3) + tgt + m.group(5) + flags + m.group(7) + '\n'
    out.append(line)
txt = ''.join(out)
FALLBACK = '''# 7-bis) Red de seguridad para miniaturas y variantes de medios no listadas arriba:
# /wp-content/uploads/AAAA/MM/nombre-300x200.jpg -> /images/AAAA/MM/nombre.webp si existe
RewriteCond %{REQUEST_URI} ^/wp-content/uploads/(.+?)(-[0-9]+x[0-9]+|-[0-9]+xh|-scaled|-e[0-9]{9,})*\\.(jpe?g|png|webp|bmp|tiff?)$ [NC]
RewriteCond %{DOCUMENT_ROOT}/images/%1.webp -f
RewriteRule ^ /images/%1.webp [R=301,L]
RewriteCond %{REQUEST_URI} ^/wp-content/uploads/(.+)$
RewriteCond %{DOCUMENT_ROOT}/images/%1 -f
RewriteRule ^ /images/%1 [R=301,L]

'''
if '7-bis)' not in txt:
    txt = txt.replace('# 8) Barra final y páginas de error', FALLBACK + '# 8) Barra final y páginas de error', 1)
open(fn, 'w', encoding='utf-8').write(txt)
print('patrones decodificados', n1, 'destinos con NE', n2)
