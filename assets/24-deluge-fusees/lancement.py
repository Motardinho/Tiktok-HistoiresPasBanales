import requests,json,concurrent.futures
from pathlib import Path
p=Path('assets/24-deluge-fusees')
d=requests.get('https://images-api.nasa.gov/search',params={'q':'Artemis I launch','media_type':'video','page_size':30},timeout=30).json()
a=[d['collection']['items'][i] for i in [0,9,21]]
(p/'recherche-lancement.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
def dl(pair):
 x,name=pair;fs=requests.get(x['href'],timeout=30).json();url=next(u for u in fs if u.endswith('~large.mp4'));r=requests.get(url,timeout=180);r.raise_for_status();(p/name).write_bytes(r.content);print(name,len(r.content),flush=True)
with concurrent.futures.ThreadPoolExecutor(3) as ex:list(ex.map(dl,zip(a,['lancement-suivi.mp4','lancement-angles.mp4','lancement-plateforme.mp4'])))
