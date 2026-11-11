"""Sources photographiques réelles pour la révision des dossiers 16 à 18."""
import json
from pathlib import Path
import requests

DEST=Path(__file__).resolve().parent/'assets/lot-16-18/photos-v2'
TITLES={
 'china-tank':'File:Type 98 tank raised view.jpg',
 'china-carrier':'File:A PLAN Shenyang J-15 carrier-based fighter aircraft is preparing to land on Chinese aircraft carrier PLANS Liaoning (CV-16) 20220504.jpg',
 'russia-jets':'File:Sukhoi Su-35S, Su-34 and T-50 flying together.jpg',
 'usa-jets':'File:US Air Force A-10 Thunderbolt II formation flight over Wake Island - June 2025.jpg',
 'usa-carrier':'File:US Navy 110831-N-IC111-160 Sailors and Marines render honors as the aircraft carrier USS Ronald Reagan (CVN 76) passes the USS Arizona Memorial whi.jpg',
 'bat-one':'File:Mexican free-tailed bat (Tadarida brasiliensis) (32235326718).jpg',
 'bat-two':'File:Mexican free-tailed bat (Tadarida brasiliensis) (46106542351).jpg',
 'falcon-one':'File:Falco peregrinus -England -flying-8.jpg',
 'falcon-two':'File:Falco peregrinus -England -flying-8 (2).jpg',
 'denali':'File:Parque nacional y reserva Denali, Alaska, Estados Unidos, 2017-08-30, DD 49.jpg',
 'canada-lake':'File:Moraine Lake 17092005.jpg',
 'kamchatka-one':'File:Kamchatka Kamchatka Landscape (17539395548).jpg',
 'kamchatka-two':'File:Kamchatka Kamchatka Landscape (17540949539).jpg',
}
HEADERS={'User-Agent':'HistoiresPasBanales/1.0 editorial research'}

def main():
    DEST.mkdir(exist_ok=True)
    response=requests.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',titles='|'.join(TITLES.values()),prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=1280),headers=HEADERS,timeout=40)
    response.raise_for_status();pages=response.json()['query']['pages'];records=[]
    for slug,title in TITLES.items():
        page=next((p for p in pages.values() if p['title']==title),None)
        if not page or 'imageinfo' not in page:
            print(slug,'absent',flush=True);continue
        i=page['imageinfo'][0];md=i.get('extmetadata',{})
        item=dict(slug=slug,title=title,url=i['url'].split('?')[0],thumb=i.get('thumburl'),page=i['descriptionurl'],width=i.get('width'),height=i.get('height'),license=md.get('LicenseShortName',{}).get('value'),license_url=md.get('LicenseUrl',{}).get('value'),artist=md.get('Artist',{}).get('value'),description=md.get('ImageDescription',{}).get('value'))
        target=DEST/(slug+'.jpg')
        if not target.exists():
            for url in [item['thumb'],item['url']]:
                if not url:continue
                r=requests.get(url,headers=HEADERS,timeout=40)
                if r.ok:
                    target.write_bytes(r.content);item['download_url']=url;break
        if target.exists():
            item['file']=target.name;records.append(item);print(slug,target.stat().st_size,item['license'],flush=True)
        else:print(slug,'téléchargement indisponible',flush=True)
        (DEST/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
