#!/usr/bin/env python3
"""Resuelve contra la web en vivo los enlaces internos que no existen en la web nueva."""
import json, subprocess, concurrent.futures as cf
from urllib.parse import quote, unquote
B = '/home/claude/belba'
pp = json.load(open(B + '/migracion/postprocess.json'))['broken']
def res(h):
    u = 'https://clinicabelba.com' + quote(unquote(h), safe='/%')
    r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-L', '--max-redirs', '6', '-A', 'Mozilla/5.0', '--max-time', '40', '-w', '%{http_code} %{url_effective} %{num_redirects}', u], capture_output=True, text=True)
    p = (r.stdout or '000 - 0').split()
    return h, {'status': int(p[0]), 'final': p[1].replace('https://clinicabelba.com', ''), 'saltos': int(p[2])}
out = {}
with cf.ThreadPoolExecutor(8) as ex:
    for h, v in ex.map(res, list(pp)):
        out[h] = v
json.dump(out, open(B + '/migracion/broken_resolved.json', 'w'), ensure_ascii=False, indent=1)
import collections
print(collections.Counter((v['status'], v['saltos'] > 0) for v in out.values()))
