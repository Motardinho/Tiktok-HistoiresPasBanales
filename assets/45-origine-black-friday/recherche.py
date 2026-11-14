import requests,json
from pathlib import Path
p=Path('assets/45-origine-black-friday')
rows=[]
for q in ['Black Friday shopping','Philadelphia Market Street 1960','Philadelphia police 1960','Army Navy game 1961','Wanamaker Philadelphia interior']:
 r=requests.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',generator='search',gsrsearch=q,gsrnamespace=6,gsrlimit=8,prop='imageinfo',iiprop='url|extmetadata|size'),headers={'User-Agent':'HPB editorial research/1.0'},timeout=40)
 if not r.ok: print(q,r.status_code);continue
 for v in r.json().get('query',{}).get('pages',{}).values():
  i=v.get('imageinfo',[{}])[0];row=dict(query=q,title=v['title'],**i);rows.append(row)
  print(len(rows)-1,v['title'],i.get('width'),i.get('height'))
(p/'recherche-photos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
