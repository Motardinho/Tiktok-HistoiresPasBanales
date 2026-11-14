"""Télécharge des vidéos Pexels repérées par recherche.py : python telecharger.py <dossier assets> id1 id2 ..."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from curl_cffi import requests

p = Path(sys.argv[1])
wanted = {int(x) for x in sys.argv[2:]}
data = {}
for f in list(p.glob('*-search.json')) + list(Path('assets/35-crashgate').glob('*-search.json')) + list(Path('assets/36-spygate').glob('*-search.json')):
    for x in json.loads(f.read_text(encoding='utf8')):
        data[int(x['id'])] = x


def get(i):
    a = data[i]['attributes']
    v = max(a['video']['video_files'], key=lambda v: (v['width'] or 0) * (v['height'] or 0))
    out = p / f'pexels-{i}.mp4'
    if not out.exists():
        r = requests.get(v['link'], impersonate='chrome', timeout=600)
        r.raise_for_status()
        out.write_bytes(r.content)
    rec = dict(id=i, source=f'https://www.pexels.com/video/{a["slug"]}-{i}/',
               auteur=((a['user']['first_name'] or '') + ' ' + (a['user']['last_name'] or '')).strip(), licence=a['license'],
               description=a['description'], width=v['width'], height=v['height'], url=v['link'])
    (p / f'pexels-{i}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding='utf8')
    print(i, v['width'], v['height'], round(out.stat().st_size / 1e6), 'Mo', flush=True)


missing = wanted - set(data)
assert not missing, missing
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(get, sorted(wanted)))
