import sys, re, csv, os
os.environ["FETCH_CACHE"] = ".fetchcache"
os.makedirs(".fetchcache", exist_ok=True)
sys.path.insert(0, "scripts")
import extract_wp as X
from concurrent.futures import ThreadPoolExecutor

urls = set()
st, body, _ = X.fetch("https://clinicabelba.com/sitemap_index.xml")
for sm in re.findall(r"<loc>([^<]+)", body):
    s2, b2, _ = X.fetch(sm)
    urls.update(re.findall(r"<loc>([^<]+)", b2))
for r in csv.DictReader(open("migracion/screamingfrog/internal_html.csv")):
    urls.add(r["Address"])
urls = {u for u in urls if not re.search(r"\.(jpe?g|png|webp|gif|pdf|svg)$", u, re.I)}
print("urls", len(urls), flush=True)
done = 0


def go(u):
    global done
    X.fetch(u)
    done += 1
    if done % 50 == 0:
        print(done, flush=True)


with ThreadPoolExecutor(6) as ex:
    list(ex.map(go, sorted(urls)))
print("fin", flush=True)
