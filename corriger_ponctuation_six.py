"""Reconstruit les sous-titres, conserve voix, plans, accroches et fun facts approuvés."""
import argparse,copy,json,re,shutil,hashlib
from concurrent.futures import ThreadPoolExecutor
import yaml
from montage_reel import ROOT,run
from narrateur import assemble
from comparer_lot_16_18 import compare
from alleger_ouvertures_top import seconds

STAGES={15:'revision-accroche-claire-v16',16:'revision-impact-v10',17:'podium-mondial-v6',18:'revision-spectaculaire-v5'}

def render(n):
    w=next((ROOT/'out').glob(f'{n}-*'));m=w/'_montage';a=m/'avant-ponctuation-liee';a.mkdir(exist_ok=True)
    for name in ['final.mp4','comparaison.mp4','histoire.json']:
        if not (a/name).exists():shutil.copy2(w/name,a/name)
    src=m if n in (13,14) else m/STAGES[n]/'_montage'
    active=m/('voitures-sans-mention-pointes.ass' if n==14 else 'superficie-mention-breve.ass') if n in (14,18) else src/'sous-titres-reference.ass'
    old=active.read_text(encoding='utf-8');originals=[line.split(',',9) for line in old.splitlines() if line.startswith('Dialogue:')]
    t=json.loads((m/'timings.json').read_text(encoding='utf-8'))
    cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=83 if n>=16 else 88,words_per_caption=5,subtitle_wrap=20 if n>=16 else 19)
    assemble.YELLOW='&H4AE2FF&';assemble.RED='&H4E62FF&';tmp=m/'ponctuation-generee.ass';assemble.write_subtitles(cfg,t['words'],tmp)
    header=old.split('[Events]')[0]+'[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
    events=[]
    for line in tmp.read_text(encoding='utf-8').splitlines():
        if not line.startswith('Dialogue:'):continue
        p=line.split(',',9);at=seconds(p[1]);end=seconds(p[2])
        if end<=1.5:continue
        if at<1.5:p[1]=assemble._ass_time(1.5)
        prefix=r'{\an8\pos(540,350)\fs76}' if n==13 and at<8 else r'{\an8\pos(540,560)\fs76}' if at<4 else ''
        if at>=4 and not (n==13 and at<8):
            previous=next((x for x in originals if x[3]=='Default' and seconds(x[1])<=at<seconds(x[2])),None)
            if previous:
                match=re.search(r'\{\\an8\\pos\([^}]+\}',previous[9])
                if match:prefix=match.group()
        p[9]=prefix+p[9];events.append(','.join(p))
    events+= [','.join(x) for x in originals if x[3]!='Default' and not any(s in x[9].upper() for s in ['POINTES EN UN SEUL SENS','TA PIRE EXPÉRIENCE','PAS BANAL, HEIN','PREMIER FEU AU GAZ'])]
    # La première image est réservée au titre, sans rang prématuré.
    adjusted=[]
    for line in events:
        p=line.split(',',9)
        if seconds(p[2])<=1.5:continue
        if seconds(p[1])<1.5:p[1]=assemble._ass_time(1.5)
        adjusted.append(','.join(p))
    targetass=m/'sous-titres-ponctuation-liee.ass';targetass.write_text(header+'\n'.join(adjusted)+'\n',encoding='utf-8')
    for line in adjusted:
        text=re.sub(r'\{[^}]*\}','',line.split(',',9)[9])
        assert not re.search(r'\\N\s*[?!:;.,…](?:\s|$|\\N)',text),text
    base=m/('base-hpb-v11.mp4' if n==13 else 'base-hpb-v13.mp4') if n in (13,14) else src/'base.mp4'
    audio=src/'mix-hpb-v12.wav' if n==15 else src/'mix.wav' if n in (16,17) else a/'final.mp4'
    inputs=['-i',str(base),'-i',str(audio),'-loop','1','-framerate','30','-i','titre-hook-reference.png','-loop','1','-framerate','30','-i','header-footer-reference.png']
    if n>=14:inputs+=['-loop','1','-framerate','30','-i','funfact-visible.png']
    graph='';clean='[0:v]'
    if n in (13,14):
        idx=4 if n==13 else 5;cut=8 if n==13 else 4
        inputs+=['-i',str(m/('intro-pesee-demonstrative.mp4' if n==13 else 'intro-ssc-kmh-original.mp4'))]
        graph=f'[{idx}:v]trim=end={cut},setpts=PTS-STARTPTS,fps=30[a];[0:v]trim=start={cut},setpts=PTS-STARTPTS,fps=30[b];[a][b]concat=n=2:v=1:a=0[clean];';clean='[clean]'
    motion=''
    if n==16:
        accents=json.loads((src/'effets-zoom.json').read_text(encoding='utf-8'))['accents_budget_secondes']
        z='1'+''.join(f'+0.035*exp(-pow((on/30-{at:.3f})/0.28,2))' for at in accents)
        motion=f"scale=2160:3840,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,"
    graph+=clean+'fps=30,setpts=PTS-STARTPTS,'+motion+'ass=sous-titres-ponctuation-liee.ass:fontsdir=.[s];[s][2:v]overlay=0:0:enable=lt(t\\,1.5):shortest=1[h];[h][3:v]overlay=0:0:shortest=1[v0]'
    if n>=14:
        story=json.loads((w/'histoire.json').read_text(encoding='utf-8'));fact=story['fun_fact_affichage'];graph+=f';[v0][4:v]overlay=0:0:enable=between(t\\,{fact["debut"]}\\,{fact["fin"]}):shortest=1[v]'
    else:graph+=';[v0]null[v]'
    target=m/'final-ponctuation-liee.mp4';duration=t['duration']
    run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','aac' if n in (15,16,17) else 'copy','-movflags','+faststart',str(target)],m)
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-']);target.replace(w/'final.mp4');compare(w)
    story=json.loads((w/'histoire.json').read_text(encoding='utf-8'));story['ponctuation_liee']=True;(w/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
    control=m/('controle-funfact-visible.json' if n>=14 else 'controle.json');d=json.loads(control.read_text(encoding='utf-8'));d.update(sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest(),ponctuation_liee=True)
    if n>=14:d.update(debut=story['fun_fact_affichage']['debut'],fin=story['fun_fact_affichage']['fin'])
    control.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print(n,'ponctuation corrigée, comparaison actualisée',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('numeros',nargs='*',type=int);args=p.parse_args()
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,args.numeros or range(13,19)))
