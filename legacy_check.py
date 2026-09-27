"""URLs con clics/impresiones en GSC o backlinks en Ahrefs que no están en el inventario:
comprueba a dónde responden hoy (estado final tras redirecciones) para darles fila en el contrato."""
import csv, json, urllib.parse, subprocess
from concurrent.futures import ThreadPoolExecutor

inv = json.load(open("migracion/inventory.json"))["items"]
norm = {urllib.parse.unquote(i["url"]).lower(): i["url"] for i in inv}
cand = {}
for r in csv.DictReader(open("migracion/gsc.csv")):
    u = r["page"].split("#")[0]
    k = urllib.parse.unquote(u).lower()
    c, im = int(float(r["clicks"])), int(float(r["impressions"]))
    if k not in norm and (c > 0 or im > 100):
        e = cand.setdefault(k, {"url": u, "clics": 0, "impresiones": 0, "backlinks": 0})
        e["clics"] += c; e["impresiones"] += im
for r in csv.DictReader(open("migracion/ahrefs_backlinks.csv")):
    k = urllib.parse.unquote(r["url_to"]).lower()
    if k not in norm:
        e = cand.setdefault(k, {"url": r["url_to"], "clics": 0, "impresiones": 0, "backlinks": 0})
        e["backlinks"] = int(r["refdomains_target"])


def check(e):
    u = urllib.parse.quote(e["url"], safe=":/?#[]@!$&'()*+,;=%")
    out = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "--max-redirs", "5", "-w",
                          "%{http_code} %{num_redirects} %{url_effective}", u],
                         capture_output=True, text=True, timeout=60).stdout.split(" ", 2)
    first = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", u],
                           capture_output=True, text=True, timeout=60).stdout
    e["estado_hoy"] = int(first or 0)
    e["estado_final"], e["saltos"], e["destino_hoy"] = int(out[0]), int(out[1]), out[2]
    e["destino_en_inventario"] = urllib.parse.unquote(out[2]).lower() in norm
    return e


with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(check, cand.values()))
json.dump(res, open("migracion/legacy_urls.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(res), Counter((e["estado_hoy"], e["estado_final"], e["destino_en_inventario"]) for e in res))
