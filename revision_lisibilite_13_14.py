"""Nouvelles prises démonstratives, titres 2026 et sous-titres compréhensibles sans son."""
import copy,hashlib,re,shutil
from concurrent.futures import ThreadPoolExecutor
import yaml
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
from habillage_reference import layers
from resserrer_titres import LEGACY
from narrateur import assemble
from narrateur.validation import validate_duration
from comparer_lot_16_18 import compare

def seconds(s):
    h,m,x=s.split(':');return int(h)*3600+int(m)*60+float(x)

def render(n):
    w=next((ROOT/'out').glob(f'{n}-*'));m=w/'_montage';story=read(w/'histoire.json');t=read(m/'timings.json')
    archive=m/'avant-lisibilite-2026';archive.mkdir(exist_ok=True)
    for name in ['final.mp4','comparaison.mp4','histoire.json']:
        if not (archive/name).exists():shutil.copy2(w/name,archive/name)
    old=(m/'sous-titres-reference.ass').read_text(encoding='utf-8')
    if not (archive/'sous-titres-reference.ass').exists():(archive/'sous-titres-reference.ass').write_text(old,encoding='utf-8')
    cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=88,words_per_caption=5,subtitle_wrap=19)
    assemble.YELLOW='&H4AE2FF&';assemble.RED='&H4E62FF&';tmp=m/'captions-lisibles-2026.ass';assemble.write_subtitles(cfg,t['words'],tmp)
    header=old.split('[Events]')[0]+'[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
    captions=[]
    oldevents=[line.split(',',9) for line in old.splitlines() if line.startswith('Dialogue:')]
    for line in tmp.read_text(encoding='utf-8').splitlines():
        if not line.startswith('Dialogue:'):continue
        p=line.split(',',9);at=seconds(p[1]);prefix=''
        if seconds(p[2])<=1.5:continue
        if at<1.5:p[1]=assemble._ass_time(1.5)
        if n==13 and at<4:prefix=r'{\an8\pos(540,550)\fs72}'
        elif n==14 and at<2.5:prefix=r'{\an8\pos(540,560)\fs72}'
        else:
            previous=next((x for x in oldevents if x[3]=='Default' and seconds(x[1])<=at<seconds(x[2])),None)
            if previous:
                match=re.search(r'\{\\an8\\pos\([^}]+\}',previous[9])
                if match:prefix=match.group()
        p[9]=prefix+p[9];captions.append(','.join(p))
    for x in oldevents:
        if x[3]=='Default' or seconds(x[2])<=1.5 or 'POINTES EN UN SEUL SENS' in x[9]:continue
        if seconds(x[1])<1.5:x[1]=assemble._ass_time(1.5)
        captions.append(','.join(x))
    (m/'sous-titres-reference.ass').write_text(header+'\n'.join(captions)+'\n',encoding='utf-8')
    item=dict(title=LEGACY[n],series='COMMENT C’EST POSSIBLE ?' if n==13 else 'TOP 3 - VITESSE',credits='JAXA - ASC - NASA' if n==13 else 'SSC - Bugatti - BYD',title_top=750 if n==14 else 1138)
    layers(m,item)
    intro=m/('intro-pesee-demonstrative.mp4' if n==13 else 'intro-ssc-kmh-original.mp4');replace=8 if n==13 else 4
    base=m/('base-hpb-v11.mp4' if n==13 else 'base-hpb-v13.mp4')
    hook=1.5;fade=hook-.2
    graph=(f'[0:v]trim=end={replace},fps=30,setpts=PTS-STARTPTS[a];[1:v]trim=start={replace},fps=30,setpts=PTS-STARTPTS[b];'
           f'[a][b]concat=n=2:v=1:a=0,ass=sous-titres-reference.ass:fontsdir=.[cap];[4:v]format=rgba,fade=t=out:st={fade}:d=0.2:alpha=1[hook];'
           f'[cap][hook]overlay=0:0:enable=lt(t\\,{hook}):shortest=1[h];[h][3:v]overlay=0:0:shortest=1[v]')
    target=m/'final-lisibilite-2026.mp4'
    run(['ffmpeg','-v','error','-y','-i',str(intro),'-i',str(base),'-i',str(w/'final.mp4'),'-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','2:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
    duration=validate_duration(target);assert abs(duration-t['duration'])<.1;run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    target.replace(w/'final.mp4');compare(w)
    if n==14:story['titre']='TOP 3 DES VOITURES LES PLUS RAPIDES - 2026';story['edition_video']=2026
    story['revision_visuelle']='Lisibilité sans son, titres et prise démonstrative 2026';save(w/'histoire.json',story)
    control=read(m/'controle.json');control.update(sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest(),sous_titres_des_premiers_mots=True,compteur_unite='KM/H' if n==14 else None,source_intro=read(m/'nouvelle-intro-source.json'));save(m/'controle.json',control)
    run(['ffmpeg','-v','error','-y','-ss','0.5','-i',str(w/'final.mp4'),'-frames:v','1',str(w/'apercu.png')])
    print(n,'nouvelle prise et lisibilité rendues',flush=True)

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(render,[13,14]))
