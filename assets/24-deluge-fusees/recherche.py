import requests,json
from pathlib import Path
p=Path('assets/24-deluge-fusees')
s=requests.Session()
items=[]
for q in ['water deluge','Artemis I launch close up']:
 d=s.get('https://images-api.nasa.gov/search',params={'q':q,'media_type':'video'},timeout=40).json()
 for x in d['collection']['items'][:8]:
  a=x['data'][0]; files=s.get(x['href'],timeout=40).json()
  print(a['nasa_id'],a['title'],[(f.split('/')[-1]) for f in files if f.endswith('.mp4')],flush=True)
  items.append(dict(data=a,files=files))
(p/'recherche-nasa.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf8')
url='https://upload.wikimedia.org/wikipedia/commons/0/02/Launch_Pad_Water_Deluge_System_Test_at_NASA_Kennedy_Space_Center.webm'
r=s.get(url,timeout=180);r.raise_for_status();(p/'deluge-2018.webm').write_bytes(r.content)
print('deluge 2018 téléchargé',len(r.content))
