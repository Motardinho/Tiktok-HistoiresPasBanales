"""Un seul repère historique après l'arsenal chinois ; tous les autres passages restent intacts."""
import copy,math,shutil,json
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save,speech
from revision_hpb_v10 import NUMBERS,display_words
from monter_lot_16_18 import music
from alleger_ouvertures_top import seconds
from narrateur.assemble import _ass_time

w=next((ROOT/'out').glob('16-*'));root=w/'_montage';old=root/'revision-spectaculaire-v9/_montage';stage=root/'revision-impact-v10';stage.mkdir(exist_ok=True);m=stage/'_montage';m.mkdir(exist_ok=True)
if not (m/'timings.json').exists():
    oldt=read(root/'timings.json');story=read(w/'histoire.json');oldintro=oldt['scene_durations'][0];at=24.22
    phrases=['Top trois des armées les plus puissantes.','Pour mesurer l’échelle : une seule bombe a ravagé Hiroshima en mille neuf cent quarante-cinq.']
    voices=[];tim=[]
    for i,phrase in enumerate(phrases):
        folder=stage/f'ajout-{i}';folder.mkdir(exist_ok=True);save(folder/'histoire.json',dict(scenes=[dict(narration_voix=phrase)]));speech(folder)
        it=read(folder/'_montage/timings-oraux.json');span=math.ceil(max(it['duration'],it['words'][-1]['end']+.08)*30)/30;voices.append((folder/'_montage/voix.mp3',span));tim.append(it)
    intro,extra=voices[0][1],voices[1][1];delta=intro-oldintro
    graph=(f'[0:a]apad,atrim=duration={intro},asetpts=PTS-STARTPTS[a];[1:a]atrim=start={oldintro}:end={at},asetpts=PTS-STARTPTS[b];'
           f'[2:a]apad,atrim=duration={extra},asetpts=PTS-STARTPTS[c];[1:a]atrim=start={at},asetpts=PTS-STARTPTS[d];[a][b][c][d]concat=n=4:v=0:a=1[out]')
    run(['ffmpeg','-v','error','-y','-i',str(voices[0][0]),'-i',str(old/'voix.mp3'),'-i',str(voices[1][0]),'-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')])
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(m/'voix.mp3')]).strip())
    NUMBERS.update({'mille neuf cent quarante-cinq':'1945','une seule':'1 seule'})
    words=display_words(tim[0]['words'])
    words += [dict(w=x['w'],start=x['start']+delta+(extra if x['start']>=at else 0),end=x['end']+delta+(extra if x['start']>=at else 0)) for x in oldt['words'] if x['start']>=oldintro-.001]
    words += [dict(w=x['w'],start=x['start']+at+delta,end=x['end']+at+delta) for x in display_words(tim[1]['words'])];words.sort(key=lambda x:x['start'])
    t=copy.deepcopy(oldt);t.update(words=words,duration=duration);t['scene_durations'][0]=intro;t['scene_durations'][2]+=extra;t['scene_durations'][-1]+=duration-sum(t['scene_durations']);save(m/'timings.json',t);save(m/'timings-oraux.json',t)
    story['scenes'][0].update(narration='Top 3 des armées les plus puissantes.',narration_voix=phrases[0]);story['hook']=story['scenes'][0]['narration']
    for key in ['narration','narration_voix']:
        oldtext=story['scenes'][2][key];needle='ogives.';assert needle in oldtext;story['scenes'][2][key]=oldtext.replace(needle,needle+' '+phrases[1],1)
    story['script']=' '.join(s['narration'] for s in story['scenes']);story['revision']='impact-v10-repere-historique-unique';story['fun_fact_affichage']['debut']+=delta+extra;story['fun_fact_affichage']['fin']+=delta+extra
    story['repere_nucleaire']=dict(texte=phrases[1],debut=at+delta,fin=at+delta+extra,une_seule_fois=True,source='https://www.city.hiroshima.lg.jp/tourism-culture/history/1003068/1027532/1027533/1008360.html',precision='Repère historique Hiroshima 1945 ; ne prétend pas que toutes les ogives ont une puissance identique.')
    # Nouvelle première image et archive historique : pas de ralentissement des séquences.
    run(['ffmpeg','-v','error','-y','-i',str(old/'base.mp4'),'-t',str(intro),'-vf',f'tpad=stop_mode=clone:stop_duration={max(0,delta)},fps=30','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(m/'intro.mp4')])
    run(['ffmpeg','-v','error','-y','-loop','1','-i',str(ROOT/'assets/lot-16-18/photos-v2/hiroshima-1945.jpg'),'-t',str(extra),'-vf',"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.02+0.0004*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1",'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(m/'hiroshima.mp4')])
    graph=(f'[0:v]trim=end={intro},setpts=PTS-STARTPTS[a];[1:v]trim=start={oldintro}:end={at},setpts=PTS-STARTPTS,fps=30[b];[2:v]setpts=PTS-STARTPTS[c];[1:v]trim=start={at},setpts=PTS-STARTPTS,fps=30[d];[a][b][c][d]concat=n=4:v=1:a=0[v]')
    run(['ffmpeg','-v','error','-y','-i',str(m/'intro.mp4'),'-i',str(old/'base.mp4'),'-i',str(m/'hiroshima.mp4'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(m/'base.mp4')])
    lines=[]
    def shift(v):return v+delta+(extra if v>=at else 0)
    for line in (root/'sous-titres-ponctuation-liee.ass').read_text(encoding='utf-8').splitlines():
        if line.startswith('Dialogue:'):
            p=line.split(',',9);a,b=seconds(p[1]),seconds(p[2])
            if b<=oldintro:continue
            p[1]=_ass_time(shift(max(a,oldintro)));p[2]=_ass_time(shift(b))
            if '620' in p[9] and p[3]!='Default':p[2]=_ass_time(min(shift(b),at+delta))
            line=','.join(p)
        lines.append(line)
    lines.append(f'Dialogue: 1,{_ass_time(at+delta)},{_ass_time(at+delta+extra)},Fact,,0,0,0,,{{\\an8\\pos(540,250)\\fs52}}HIROSHIMA - 1945')
    (m/'sous-titres-reference.ass').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    effects=read(old/'effets-zoom.json');effects['accents_budget_secondes']=[shift(v) for v in effects['accents_budget_secondes']];save(m/'effets-zoom.json',effects);music(w,m,t,16)
    archive=root/'avant-repere-hiroshima';archive.mkdir(exist_ok=True)
    for name in ['histoire.json','script.txt']:
        if (w/name).exists() and not (archive/name).exists():shutil.copy2(w/name,archive/name)
    save(stage/'histoire.json',story);save(w/'histoire.json',story)
    for name in ['timings.json','timings-oraux.json','voix.mp3']:shutil.copy2(m/name,root/name)
    (w/'script.txt').write_text('\n\n'.join(s['narration'] for s in story['scenes']),encoding='utf-8')
    save(stage/'recalage.json',dict(intro_delta=delta,insertion=at,duree_insertion=extra))
    with (w/'verification.md').open('a',encoding='utf-8') as f:f.write('\nRepère historique ajouté une seule fois après la Chine : une bombe a ravagé Hiroshima le 6 août 1945. Source officielle : '+story['repere_nucleaire']['source']+'\nIl ne s’agit pas d’une équivalence de puissance avec chaque ogive chinoise.\n')
    with (w/'CREDITS.md').open('a',encoding='utf-8') as f:f.write('\nHiroshima 1945 : photographie U.S. Navy, domaine public, identifiée via Wikimedia Commons (Hiroshima Aftermath - cropped Version.jpg), copie de consultation https://tiogatours.nl/dynamic/img/geschiedenis/amerika/1945-atoombommen-op-hiroshima-en-nagasaki-4.6.b958.jpg\n')
    print('16 : repère historique unique ajouté,',round(duration,2),'s',flush=True)
