import requests,json,concurrent.futures,subprocess
from pathlib import Path
p=Path('assets/24-deluge-fusees');items=json.loads((p/'recherche-nasa.json').read_text(encoding='utf8'))
def dl(pair):
 i,name=pair; url=next(x for x in items[i]['files'] if x.endswith('~large.mp4'));r=requests.get(url,timeout=180);r.raise_for_status();(p/name).write_bytes(r.content);print(name,len(r.content),flush=True)
with concurrent.futures.ThreadPoolExecutor(3) as ex:list(ex.map(dl,[(0,'deluge-sol-2023.mp4'),(1,'deluge-drone-2023.mp4'),(2,'deluge-drone2-2023.mp4'),(7,'artemis-2022.mp4')]))
