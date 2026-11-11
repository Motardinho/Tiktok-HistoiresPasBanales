"""Production HPB du lot 16-18. Étapes réutilisables, caches et provenance."""
import argparse
import base64
import copy
import json
import math
import re
import shutil
from pathlib import Path

import requests
import yaml

from montage_reel import ROOT, run
from narrateur.voice import _api_key

FOLDERS = sorted(p for p in (ROOT/'out').iterdir() if p.is_dir() and re.match(r'^(16|17|18)-',p.name))

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def norm(s): return s.lower().replace('’',"'").strip('.,;:!?«»')

def speech(w):
    m=w/'_montage';m.mkdir(exist_ok=True)
    if (m/'timings-oraux.json').exists() and (m/'voix.mp3').exists():return
    d=read(w/'histoire.json');cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))['voice']
    text=' '.join(s['narration_voix'] for s in d['scenes'])
    model=cfg['model_id'];stability=cfg['stability']
    for attempt in range(2):
        response=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice_id']}/with-timestamps",
            params={'output_format':cfg['output_format']},headers={'xi-api-key':_api_key()},
            json=dict(text=text,model_id=model,seed=7112026,voice_settings=dict(stability=stability,similarity_boost=.75)),timeout=300)
        if response.ok:break
        detail=response.json().get('detail',{})
        if attempt==0 and ('model' in str(detail).lower() or 'stability' in str(detail).lower()):
            model='eleven_v3';stability=.5;continue
        raise RuntimeError(f'TTS {response.status_code}: {str(detail)[:400]}')
    response.raise_for_status();data=response.json()
    (m/'voix.mp3').write_bytes(base64.b64decode(data['audio_base64']))
    al=data.get('alignment') or data['normalized_alignment'];save(m/'alignement-caracteres.json',al)
    words=[];current='';start=None;last=0
    for c,a,b in zip(al['characters'],al['character_start_times_seconds'],al['character_end_times_seconds']):
        if c.isspace():
            if current:words.append(dict(w=current,start=start,end=last));current='';start=None
        else:
            if start is None:start=a
            current+=c;last=b
    if current:words.append(dict(w=current,start=start,end=last))
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(m/'voix.mp3')]).strip())
    starts=[0.];cursor=0
    tokens=[norm(x['w']) for x in words]
    for s in d['scenes'][1:]:
        prefix=[norm(t) for t in s['narration_voix'].split()][:5]
        at=next((i for i in range(cursor+1,len(tokens)-len(prefix)+1) if tokens[i:i+len(prefix)]==prefix),None)
        if at is None:raise ValueError(f'Scène introuvable {prefix}')
        starts.append(words[at]['start']);cursor=at
    save(m/'timings-oraux.json',dict(duration=duration,scene_durations=[b-a for a,b in zip(starts,starts[1:]+[duration])],words=words,model=model,voice_id=cfg['voice_id'],stability=stability))
    print(w.name,'voix',round(duration,2),'s',model,flush=True)

def media_search():
    target=ROOT/'assets/lot-16-18';target.mkdir(exist_ok=True)
    queries=['filetype:video Chinese military parade','filetype:video Russian military aircraft','filetype:video US military aircraft takeoff',
             'filetype:video cheetah running','filetype:video Tadarida brasiliensis','filetype:video peregrine falcon flight',
             'filetype:video Alaska landscape','filetype:video Canada lake aerial','filetype:video Russia landscape']
    records=[]
    for q in queries:
        r=requests.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',generator='search',gsrsearch=q,gsrnamespace=6,gsrlimit=7,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=1280),headers={'User-Agent':'HistoiresPasBanales/1.0 editorial research'},timeout=40)
        r.raise_for_status()
        for p in r.json().get('query',{}).get('pages',{}).values():
            i=p['imageinfo'][0];md=i.get('extmetadata',{})
            item=dict(query=q,title=p['title'],url=i['url'].split('?')[0],page=i['descriptionurl'],size=i.get('size'),width=i.get('width'),height=i.get('height'),
                      license=md.get('LicenseShortName',{}).get('value'),license_url=md.get('LicenseUrl',{}).get('value'),artist=md.get('Artist',{}).get('value'),description=md.get('ImageDescription',{}).get('value'))
            records.append(item)
            print(q,p['title'],item['license'],item['size'],flush=True)
    save(target/'recherche-commons.json',records)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('step',choices=['speech','search']);p.add_argument('--numero',type=int);args=p.parse_args()
    if args.step=='search':media_search()
    else:
        for w in FOLDERS:
            if args.numero is None or int(w.name[:2])==args.numero:speech(w)
