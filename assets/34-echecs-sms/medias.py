import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests
from bs4 import BeautifulSoup

p=Path(__file__).parent
data=json.loads((p/'pexels-data.json').read_text(encoding='utf8'))['props']['pageProps']['initialData']['data']
chosen={6058628,10388941,6599643,6689890,7688807,33688494,6689107,10586234}
def get(x):
 a=x['attributes'];i=x['id'];v=max(a['video']['video_files'],key=lambda v:v['width']*v['height']);out=p/f'pexels-{i}.mp4'
 if not out.exists():
  r=requests.get(v['link'],impersonate='chrome',timeout=120);r.raise_for_status();out.write_bytes(r.content)
 record=dict(id=i,source=f'https://www.pexels.com/video/{a["slug"]}-{i}/',auteur=(a['user']['first_name'] or '')+' '+(a['user']['last_name'] or ''),licence=a['license'],description=a['description'],width=v['width'],height=v['height'],url=v['link'])
 (p/f'pexels-{i}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8');print(i,v['width'],v['height'],flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(get,[x for x in data if int(x['id']) in chosen]))
url='https://commons.wikimedia.org/wiki/File:Sebastien_Feller.jpg'
r=requests.get(url,impersonate='chrome',timeout=40);r.raise_for_status();(p/'feller-page.html').write_text(r.text,encoding='utf8');h=BeautifulSoup(r.text,'html.parser');link=h.select_one('.fullImageLink a')['href'];r=requests.get(link,impersonate='chrome',timeout=60);r.raise_for_status();(p/'feller.jpg').write_bytes(r.content);print('Feller',link,flush=True)
