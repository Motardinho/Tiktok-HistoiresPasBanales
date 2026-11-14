import json
from pathlib import Path
from curl_cffi import requests
from bs4 import BeautifulSoup
p=Path(__file__).parent
d=json.loads((p/'phone-search.json').read_text(encoding='utf8'))
def get(x):
 a=x['attributes'];i=x['id'];v=max(a['video']['video_files'],key=lambda v:v['width']*v['height']);out=p/f'pexels-{i}.mp4'
 if not out.exists():
  r=requests.get(v['link'],impersonate='chrome',timeout=120);r.raise_for_status();out.write_bytes(r.content)
 record=dict(id=i,source=f'https://www.pexels.com/video/{a["slug"]}-{i}/',auteur=(a['user']['first_name'] or '')+' '+(a['user']['last_name'] or ''),licence=a['license'],description=a['description'],width=v['width'],height=v['height'],url=v['link'])
 (p/f'pexels-{i}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8');print(i,v['width'],v['height'],flush=True)
for x in d:
 if int(x['id']) in {39494839,9898435,7362704}:get(x)
for term in ['computer keyboard','phone table']:
 r=requests.get('https://www.pexels.com/search/videos/'+term.replace(' ','%20')+'/',impersonate='chrome',timeout=40)
 h=BeautifulSoup(r.text,'html.parser');d=json.loads(h.find('script',id='__NEXT_DATA__').string)['props']['pageProps']['initialData']['data']
 (p/(term.replace(' ','-')+'-search.json')).write_text(json.dumps(d,ensure_ascii=False),encoding='utf8')
 print(term,[(x['id'],x['attributes']['width'],x['attributes']['height'],x['attributes']['description']) for x in d],flush=True)
