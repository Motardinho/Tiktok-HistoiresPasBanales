import json
import requests
from photos_spectaculaires import DEST,HEADERS

QUERIES={
 'russia-jets':'filetype:bitmap Su-35S flying',
 'russia-tank':'filetype:bitmap Russian T-90 parade',
 'usa-carrier-two':'filetype:bitmap USS Ronald Reagan flight deck aerial',
 'cheetah-one':'filetype:bitmap cheetah running',
 'falcon-stoop':'filetype:bitmap peregrine falcon diving',
 'usa-city':'filetype:bitmap Manhattan skyline aerial',
 'usa-canyon':'filetype:bitmap Grand Canyon National Park vertical',
 'canada-forest':'filetype:bitmap Banff Canada forest lake',
 'russia-volcano':'filetype:bitmap Kamchatka volcano eruption',
}

def main():
    manifest=json.loads((DEST/'sources.json').read_text(encoding='utf-8'));all=[]
    for slug,q in QUERIES.items():
        response=requests.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',generator='search',gsrsearch=q,gsrnamespace=6,gsrlimit=5,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=960),headers=HEADERS,timeout=35)
        if not response.ok:print(slug,response.status_code,flush=True);continue
        candidates=[]
        for page in response.json().get('query',{}).get('pages',{}).values():
            if 'imageinfo' not in page:continue
            i=page['imageinfo'][0];md=i.get('extmetadata',{})
            item=dict(slug=slug,title=page['title'],url=i['url'].split('?')[0],thumb=i.get('thumburl'),page=i['descriptionurl'],width=i.get('width'),height=i.get('height'),license=md.get('LicenseShortName',{}).get('value'),license_url=md.get('LicenseUrl',{}).get('value'),artist=md.get('Artist',{}).get('value'),description=md.get('ImageDescription',{}).get('value'))
            if item['license'] and any(x in item['license'] for x in ['Public domain','CC BY','CC0']):candidates.append(item);all.append(item)
        print(slug,[(x['title'],x['license']) for x in candidates],flush=True)
        for item in candidates:
            f=DEST/(slug+'.jpg')
            if f.exists():break
            for url in [item['thumb'],item['url']]:
                if not url:continue
                r=requests.get(url,headers=HEADERS,timeout=30)
                if r.ok:
                    f.write_bytes(r.content);item['download_url']=url;item['file']=f.name
                    manifest=[x for x in manifest if x['slug']!=slug]+[item]
                    print('choisi',slug,item['title'],flush=True);break
            if f.exists():break
        (DEST/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        (DEST/'recherche-complement.json').write_text(json.dumps(all,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
