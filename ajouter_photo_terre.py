import json
import requests
from photos_spectaculaires import DEST,HEADERS

title='File:The Earth seen from Apollo 17.jpg'
r=requests.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',titles=title,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=1280),headers=HEADERS,timeout=40);r.raise_for_status()
p=next(iter(r.json()['query']['pages'].values()));i=p['imageinfo'][0];md=i['extmetadata']
for url in [i.get('thumburl'),i['url']]:
 if not url:continue
 response=requests.get(url,headers=HEADERS,timeout=40)
 if response.ok:
  target=DEST/'earth-hero.jpg';target.write_bytes(response.content)
  item=dict(slug='earth-hero',file=target.name,title=title,url=i['url'],download_url=url,page=i['descriptionurl'],license=md.get('LicenseShortName',{}).get('value'),license_url=md.get('LicenseUrl',{}).get('value'),artist=md.get('Artist',{}).get('value'),description=md.get('ImageDescription',{}).get('value'))
  manifest=json.loads((DEST/'sources.json').read_text(encoding='utf-8'));manifest=[x for x in manifest if x['slug']!='earth-hero']+[item];(DEST/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print('Terre Apollo 17',len(response.content));break
else:raise RuntimeError('Photo de la Terre indisponible')
