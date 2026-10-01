#!/usr/bin/env python3
"""Sirve dist/ en local aplicando las reglas de dist/_redirects (301, 301! y 410) como harían Apache o Netlify, para poder
pasar validate_migration.py en Windows sin Apache. Uso:
    python -X utf8 scripts/dev/serve_dist.py dist 8099
    python -X utf8 scripts/validate_migration.py migracion/inventory.json --base http://127.0.0.1:8099 --redirects public/_redirects ...
Hay que haber copiado antes public/_redirects a dist/ (lo hace pipeline.sh) o pasar la carpeta public como raíz de las reglas."""
import os, sys, mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, urlsplit, quote
ROOT = sys.argv[1]; PORT = int(sys.argv[2])
R = {}
REGLAS = os.path.join(ROOT, '_redirects') if os.path.exists(os.path.join(ROOT, '_redirects')) else os.path.join(os.path.dirname(ROOT), 'public', '_redirects')
for line in open(REGLAS, encoding='utf-8'):
    p = line.split()
    if len(p) >= 3 and not line.startswith('#'):
        R[unquote(' '.join(p[:-2])).lower()] = (p[-2], int(p[-1].rstrip('!')))
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_HEAD(self): self.do_GET(head=True)
    def do_GET(self, head=False):
        path = unquote(urlsplit(self.path).path)
        key = path.lower()
        if key in R or (key + '/') in R:
            dst, code = R.get(key) or R.get(key + '/')
            if code == 410:
                self.send_response(410); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers()
                if not head:
                    f = os.path.join(ROOT, '410.html')
                    self.wfile.write(open(f, 'rb').read() if os.path.exists(f) else b'410')
                return
            self.send_response(code); self.send_header('Location', quote(dst, safe='/%?=&:')); self.end_headers(); return
        f = os.path.join(ROOT, path.lstrip('/'))
        if os.path.isdir(f):
            if not path.endswith('/'):
                self.send_response(301); self.send_header('Location', path + '/'); self.end_headers(); return
            f = os.path.join(f, 'index.html')
        if not os.path.isfile(f):
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers()
            if not head:
                n = os.path.join(ROOT, '404.html'); self.wfile.write(open(n, 'rb').read() if os.path.exists(n) else b'404')
            return
        data = open(f, 'rb').read()
        ct = mimetypes.guess_type(f)[0] or 'application/octet-stream'
        if ct.startswith('text/') or ct in ('application/javascript', 'application/xml', 'application/json'): ct += '; charset=utf-8'
        self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(data))); self.end_headers()
        if not head: self.wfile.write(data)
ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
