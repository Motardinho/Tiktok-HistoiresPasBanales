import json
import requests
from photos_spectaculaires import DEST,HEADERS

choices={
 'denali':'File:View of Wonder Lake and its surrounding mountains in Denali National Park in late June, 2017. (bd44780c-93e9-42a6-bc92-905b78868472).JPG',
 'usa-city':'File:New York City skyline with Statue of Liberty at dusk aerial 2018.jpg',
 'falcon-stoop':'File:Peregrine Falcon at Appuldurcombe (5147160662).jpg',
}
r=requests.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',titles='|'.join(choices.values()),prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=960),headers=HEADERS,timeout=40);r.raise_for_status()
pages=r.json()['query']['pages'];manifest=json.loads((DEST/'sources.json').read_text(encoding='utf-8'))
for slug,title in choices.items():
 p=next(x for x in pages.values() if x['title']==title)
 if 'imageinfo' not in p:print(slug,'absent');continue
 i=p['imageinfo'][0];md=i.get('extmetadata',{})
 for url in [i.get('thumburl'),i['url']]:
  if not url:continue
  response=requests.get(url,headers=HEADERS,timeout=40)
  if response.ok:
   f=DEST/(slug+'.jpg');f.write_bytes(response.content)
   item=dict(slug=slug,title=title,url=i['url'].split('?')[0],download_url=url,page=i['descriptionurl'],width=i.get('width'),height=i.get('height'),license=md.get('LicenseShortName',{}).get('value'),license_url=md.get('LicenseUrl',{}).get('value'),artist=md.get('Artist',{}).get('value'),description=md.get('ImageDescription',{}).get('value'),file=f.name)
   manifest=[x for x in manifest if x['slug']!=slug]+[item];print(slug,'remplacé',len(response.content));break
(DEST/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
