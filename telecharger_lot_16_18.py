"""Télécharge les sources Wikimedia choisies avec crédits et licences."""
import json
import time
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'assets/lot-16-18'
HEADERS={'User-Agent':'HistoiresPasBanales/1.0 editorial research'}

def get(url,**kwargs):
    for attempt in range(2):
        r=requests.get(url,timeout=90,**kwargs)
        if r.status_code!=429:r.raise_for_status();return r
        time.sleep(min(20,int(r.headers.get('Retry-After','10'))))
    r.raise_for_status()

def download(url,file):
    if file.exists() and file.stat().st_size>10000:return
    partial=file.with_suffix(file.suffix+'.part')
    offset=partial.stat().st_size if partial.exists() else 0
    with partial.open('ab') as stream:
        while True:
            response=get(url,headers={**HEADERS,'Range':f'bytes={offset}-{offset+9999999}'})
            if response.status_code==200:
                stream.seek(0);stream.truncate();stream.write(response.content);break
            response.raise_for_status();stream.write(response.content);offset+=len(response.content)
            total=int(response.headers['Content-Range'].split('/')[-1])
            if offset>=total:break
    partial.rename(file)

def main():
    candidates=[]
    for name in ['recherche-commons.json','recherche-complement.json']:
        candidates+=json.loads((DEST/name).read_text(encoding='utf-8'))
    choices={
      'china-parade':'File:仪仗方队高擎党旗国旗军旗接受检阅.webm',
      'china-tanks':'File:Beijing-parade-rehearsal-tanks-tiananmen-20190923-VOA.webm',
      'russia-air':'File:Russian pilots in Tajikistan during the exercise provided air support to the advancing motorized infantry.webm',
      'usa-f16':'File:Exercise Sprint 26-2 F-16 Take Offs (993056).webm',
      'cheetah':'File:Rozi the cheetah running at the Cincinnati Zoo.webm',
      'cheetah-cinema':"File:Cheetahs on the Edge (Director's Cut).webm",
      'bats':'File:Bracken Bat Cave evening of 17 June 2017.ogv',
      'falcon':'File:Peregrine falcon (Falco peregrinus) in West Reno, Nevada, USA.webm',
      'alaska':'File:ABoVE Summer 2022 B-Roll (SVS14222 Murphy Dome Scenics 1080).webm',
      'canada':"File:Descending through the Haze of Distant Fires to Cameron Lake's Wetlands.webm",
    }
    manifest=[]
    for slug,title in choices.items():
        item=dict(next(x for x in candidates if x['title']==title))
        url=item['url'];suffix=Path(url).suffix
        if slug not in ('china-parade','china-tanks'):
            data=get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',titles=title,prop='videoinfo',viprop='derivatives'),headers=HEADERS).json()
            info=next(iter(data['query']['pages'].values()))['videoinfo'][0]
            derivatives=info['derivatives']
            keys=['720p.vp9.webm','480p.vp9.webm','1080p.vp9.webm','240p.vp9.webm']
            if slug=='bats':keys=['240p.vp9.webm','480p.vp9.webm']
            chosen=next((x for key in keys for x in derivatives if x['transcodekey']==key),None)
            if chosen:url=chosen['src'];suffix='.webm'
        file=DEST/(slug+suffix)
        try:download(url,file)
        except requests.RequestException as error:
            print(slug,'échec',str(error)[:160],flush=True);continue
        item.update(slug=slug,file=file.name,download_url=url);manifest.append(item)
        (DEST/'sources-visuelles.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        print(slug,file.stat().st_size,flush=True)

if __name__=='__main__':main()
