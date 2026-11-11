"""Dernières consignes HPB : heures/CTA, durée contrôlée, top auto vérifié.

Le top auto est un aperçu en voix Edge, séparé des exports dans la voix validée.
"""
import copy
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

from habillage_reference import ITEMS, compare, layers, subs
from montage_reel import ROOT, SOURCES, run
from narrateur import assemble
from narrateur.validation import validate_duration

ASTRO = 'astronautes-sport-en-orbite'
TRAFFIC = 'villes-plus-lentes-tomtom-2024'
CAR = 'trois-records-voitures-vitesse'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def numeric_words(words):
    """Collapser uniquement les nombres connus, en conservant leur intervalle audio."""
    replacements = {
        'deux mille vingt-quatre': '2024',
        'deux mille dix-neuf': '2019',
        'mille huit cent dix-sept': '1\u202f817',
        'quatre cent quatre-vingt-dix': '490',
        'trois cent quatre-vingts': '380',
        'quatre-vingt-dix-sept': '97',
        'cent une': '101', 'cent deux': '102',
        'f cinq': 'F5', 'v huit': 'V8',
        'trois cents plus': '300+',
    }
    def clean(s):
        return s.lower().strip('.,;:!?«»')
    out, i = [], 0
    patterns = sorted(replacements, key=lambda x: -len(x.split()))
    while i < len(words):
        for phrase in patterns:
            n = len(phrase.split())
            group = words[i:i+n]
            if ' '.join(clean(x['w']) for x in group) == phrase:
                suffix = re.search(r'[.,;:!?]+$', group[-1]['w'])
                out.append(dict(w=replacements[phrase] + (suffix.group() if suffix else ''),
                                start=group[0]['start'], end=group[-1]['end']))
                i += n
                break
        else:
            out.append(copy.deepcopy(words[i]))
            i += 1
    return out


def traffic_audio(w):
    old = w/'avant-chute-hpb-v8'
    source_t = read(old/'timings.json')
    cta = read(w/'cta-bouchons-debut-timings.json')
    astro = ROOT/'out'/ASTRO
    sig = read(astro/'chute-timings-hpb-v8.json')
    # Conserver la dernière explication utile, remplacer l'ancienne fermeture.
    segments = [
        (old/'voix.mp3', source_t, 0, 62.107),
        (w/'cta-bouchons-debut.mp3', cta, 0, cta['duration']),
        (old/'voix.mp3', source_t, 66.08, 67.04),
        (astro/'chute-hpb-v8.mp3', sig, 3.282, sig['duration']),
    ]
    words, duration = [], 0.0
    for i, (audio, timing, start, end) in enumerate(segments):
        span = end-start
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(audio), '-af',
             f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS,apad,atrim=duration={span}',
             '-ar', '44100', '-ac', '1', str(w/f'oral-v9-{i}.wav')])
        words.extend(dict(w=x['w'], start=x['start']-start+duration,
                          end=min(x['end'], end)-start+duration)
                     for x in timing['words'] if start <= x['start'] < end)
        duration += span
    (w/'oral-v9.txt').write_text(''.join(f"file 'oral-v9-{i}.wav'\n" for i in range(4)), encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','oral-v9.txt',
         '-c:a','libmp3lame','-b:a','128k','voix-hpb-v9.mp3'],w)
    t = dict(words=words, duration=duration,
             scene_durations=source_t['scene_durations'][:-1]+[duration-57.6])
    save(w/'timings-hpb-v9.json', t)
    d = read(old/'histoire.json')
    d['scenes'][-1]['narration'] = (
        'Retenir la source, l’année et le critère change la lecture d’un top. '
        'Ta pire expérience de bouchon en commentaire. Pas banal, hein ?')
    d['titre_fixe'] = '102 H DANS LES BOUCHONS'
    d['hashtags'] = [x.replace('#DossiersHorsNormes','#HistoiresPasBanales') for x in d['hashtags']]
    save(w/'histoire-hpb-v9.json', d)
    return t, 62.107


def captions(w, t, item, cfg, cta_start=None):
    display = copy.deepcopy(t)
    display['words'] = numeric_words(t['words'])
    subs(w, display, item, cfg)
    p = w/'sous-titres-reference.ass'
    s = p.read_text(encoding='utf-8')
    if item.get('caption_zones'):
        adjusted=[]
        for line in s.splitlines():
            if line.startswith('Dialogue:'):
                parts=line.split(',',9)
                if parts[3]=='Default':
                    h,m,sec=parts[1].split(':');at=int(h)*3600+int(m)*60+float(sec)
                    for begin,end,y in item['caption_zones']:
                        if begin<=at<end:
                            parts[9]=f'{{\\an8\\pos(540,{y})}}'+parts[9]
                            line=','.join(parts);break
            adjusted.append(line)
        s='\n'.join(adjusted)+'\n'
    # CTA et signature restent dans la transcription, sans panneau en doublon.
    forbidden = ['horsepower','F cinq','V huit','Dossier clos','hors normes']
    assert not any(x.lower() in s.lower() for x in forbidden)
    p.write_text(s,encoding='utf-8')


def export(slug,w,t,item,audio,base,cta_start=None,draft=False,version=9):
    cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
    cfg['render'].update(subtitle_size=88,words_per_caption=5,subtitle_wrap=19)
    shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',w/'police.ttf')
    layers(w,item)
    captions(w,t,item,cfg,cta_start)
    graph=('[0:v]fps=30,setpts=PTS-STARTPTS,ass=sous-titres-reference.ass:fontsdir=.[cap];'
           '[3:v]format=rgba,fade=t=out:st=3.8:d=0.2:alpha=1[hook];'
           '[cap][hook]overlay=0:0:enable=lt(t\\,4):shortest=1[h];'
           '[h][2:v]overlay=0:0:shortest=1[v]')
    run(['ffmpeg','-v','error','-y','-i',base,'-i',audio,
         '-loop','1','-framerate','30','-i','header-footer-reference.png',
         '-loop','1','-framerate','30','-i','titre-hook-reference.png',
         '-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0',
         '-t',str(t['duration']),'-c:v','libx264','-preset','fast','-crf','19','-threads','3',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',f'final-hpb-v{version}.mp4'],w)
    duration=validate_duration(w/f'final-hpb-v{version}.mp4')
    if abs(duration-t['duration']) > .2:
        raise ValueError(f'Durée vidéo {duration} incohérente avec la narration {t["duration"]}')
    run(['ffmpeg','-v','error','-i',str(w/f'final-hpb-v{version}.mp4'),'-f','null','-'])
    print(slug,'rendu',duration,'brouillon' if draft else 'voix validée',flush=True)
    compare(slug,w,duration,version=version)
    if not draft:
        for src,dst in [(f'final-hpb-v{version}.mp4','final.mp4'),(f'comparaison-hpb-v{version}.mp4','comparaison.mp4')]:
            shutil.copy2(w/src,w/dst)
        if slug==TRAFFIC and version==9:
            for src,dst in [('voix-hpb-v9.mp3','voix.mp3'),('timings-hpb-v9.json','timings.json'),('histoire-hpb-v9.json','histoire.json')]:
                shutil.copy2(w/src,w/dst)
    save(w/f'controle-hpb-v{version}.json',dict(duration_mp4=duration,minimum_strict_60=True,
         miroir=False,header_footer_permanents=True,bandeau_centre=True,
         ancienne_signature=False,voix='Edge, brouillon distinct de la voix validée' if draft else 'ElevenLabs validée',
         statut='Brouillon visuel ; narration finale à régénérer' if draft else 'Rendu décodé et durée vérifiée'))


def other(slug):
    w=ROOT/'out'/slug
    if slug==TRAFFIC:
        t,cta_start=traffic_audio(w)
        item=copy.deepcopy(ITEMS[slug])
        item.update(title=['102 H','DANS LES','BOUCHONS'],facts=[
            (0,4,'NEW YORK • 2024'),
            (17.88,25.24,'LONDRES • 2024\\N101 H DANS LES BOUCHONS'),
            (25.24,33.96,'NEW YORK • 2024\\N102 H DANS LES BOUCHONS'),
            (33.96,41.44,'PARIS • 2024\\N97 H DANS LES BOUCHONS')])
        export(slug,w,t,item,'voix-hpb-v9.mp3','base-reference.mp4',cta_start)
    else:
        t=read(w/'timings-hpb-v8.json')
        export(slug,w,t,ITEMS[slug],'voix-hpb-v8.mp3','base-reference.mp4')


def car():
    w=ROOT/'out'/CAR/'brouillon-top3-2026'
    t=read(w/'timings.json')
    # Chaque groupe suit la scène parlée. Les vues/compteurs d'une même prise sont
    # différents cadrages informatifs, jamais une duplication en miroir.
    groups=[
        [('byd-meter',115,2.8),('bugatti-record',160,2.4),('ssc-meter',153,None)],
        [('ssc-tuatara',116,3.2),('ssc-tuatara',121,3.2),('ssc-meter',151,None)],
        [('ssc-tuatara',6,3.2),('ssc-tuatara',10,2.8),('ssc-tuatara',103,3.3),('ssc-meter',152,None)],
        [('bugatti-record',80,3.2),('bugatti-emb',120,3.8),('bugatti-emb',146,None)],
        [('bugatti-record',80,3),('bugatti-record',160,3.2),('bugatti-emb',128,None)],
        [('byd-meter',112,3.8),('byd-road',105,3.5),('byd-meter',114,None)],
        [('byd-driver',104,3),('byd-road',108,2.5),('byd-meter',110,None)],
        [('ssc-meter',153,2.8),('bugatti-record',160,2.8),('byd-road',115,None)],
    ]
    files=[];cursor=0;edits=[]
    for scene,(group,duration) in enumerate(zip(groups,t['scene_durations'])):
        end=round(sum(t['scene_durations'][:scene+1])*30)
        for name,start,length in group:
            frames=round(length*30) if length else end-cursor
            # Les prises comportant un compteur ont leur propre cache : ne pas
            # réutiliser un ancien cadrage qui couperait l'instrument.
            suffix='-compteur' if name=='byd-meter' else '-compteur-route' if name=='ssc-meter' else '-30fps' if name=='byd-road' else ''
            # Début et nature du cadrage font partie de la clé du plan.
            if name in ('bugatti-record','bugatti-emb'):
                suffix=f'-{name}-{start}'
            target=w/f'top3-plan{len(files):02d}{suffix}.mp4'
            if name.startswith('byd-'):
                source=SOURCES/'yangwang-u9-xtreme-2026.mp4'
                # La vue routière et l'appareil Racelogic se lisent simultanément.
                graph=('[0:v]split=2[a][b];'
                       '[a]crop=1920:582:0:84,crop=328:582:796:0,scale=1080:1920[road];')
                if name=='byd-meter':
                    graph+='[b]crop=388:326:1510:709,scale=800:672[detail];[road][detail]overlay=140:400,fps=30,setsar=1[v]'
                elif name=='byd-driver':
                    graph+='[b]crop=440:326:22:709,scale=800:592[detail];[road][detail]overlay=140:475,fps=30,setsar=1[v]'
                else:
                    graph=graph.replace('[0:v]split=2[a][b];','[0:v]')
                    graph=graph.replace('[a]','').replace('[road];',',fps=30,setsar=1[v]')
                opts=['-filter_complex',graph,'-map','[v]']
            elif name=='ssc-meter':
                source=SOURCES/'ssc-tuatara.mp4'
                graph=('[0:v]split=2[a][b];'
                       '[a]crop=1920:700:0:0,crop=394:700:763:0,scale=1080:1920[road];'
                       '[b]crop=880:370:0:700,scale=940:395[detail];'
                       '[road][detail]overlay=70:620,fps=30,setsar=1[v]')
                opts=['-filter_complex',graph,'-map','[v]']
            elif name=='bugatti-emb':
                source=SOURCES/'bugatti-record.mp4'
                # La source monte plusieurs caméras ; isoler la grande vue
                # embarquée du bas pour retirer la grille de miniatures.
                vf='crop=1920:550:0:400,crop=310:550:805:0,scale=1080:1920,fps=30,setsar=1'
                opts=['-vf',vf]
            else:
                source=SOURCES/(name+'.mp4')
                lead='crop=iw:trunc(ih*0.74/2)*2:0:(ih-oh)/2,'
                vf=lead+'crop=trunc(ih*9/16/2)*2:ih:(iw-ow)/2:0,scale=1080:1920,fps=30,setsar=1'
                opts=['-vf',vf]
            if not target.exists():
                run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(source),*opts,
                     '-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19',
                     '-threads','3','-pix_fmt','yuv420p','-r','30','-video_track_timescale','15360',str(target)])
            files.append(target.name)
            edits.append(dict(scene=scene,source=name,source_start=start,start=cursor/30,duration=frames/30))
            cursor+=frames
            print('top3 plan',len(files),flush=True)
    (w/'top3-concat.txt').write_text(''.join(f"file '{f}'\n" for f in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','top3-concat.txt','-c','copy','base-top3.mp4'],w)
    save(w/'montage-top3.json',edits)
    starts=[sum(t['scene_durations'][:i]) for i in range(9)]
    item=dict(title=['TOP 3','DES VOITURES','LES PLUS RAPIDES'],
              series='TOP 3 • VITESSE',credits='SSC / Bugatti / BYD • BROUILLON VOIX',facts=[
                  (starts[1],starts[3],'3 • SSC TUATARA\\N474,8 KM/H'),
                  (starts[3],starts[5],'2 • CHIRON SUPER SPORT 300+\\N490,484 KM/H'),
                  (starts[5],starts[7],'1 • YANGWANG U9 XTREME\\N503,17 KM/H')])
    export(CAR,w,t,item,'voix-brouillon.mp3','base-top3.mp4',draft=True)


if __name__=='__main__':
    for slug in sys.argv[1:]:
        if slug==CAR:car()
        else:other(slug)
