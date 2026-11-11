"""Remplace seulement l'accroche orale, recale le classement et retire le doublon du fun fact."""
import copy,math,shutil,json
from montage_reel import ROOT,run,SOURCES
from produire_lot_16_18 import read,save,speech
from revision_hpb_v12 import music
from alleger_ouvertures_top import seconds
from narrateur.assemble import _ass_time

w=next((ROOT/'out').glob('15-*'));rootm=w/'_montage';old=rootm/'revision-donnees-2025-rapide-v15/_montage';stage=rootm/'revision-accroche-claire-v16';stage.mkdir(exist_ok=True);m=stage/'_montage';m.mkdir(exist_ok=True)
if not (m/'timings.json').exists():
    phrase='Top trois des villes les plus embouteillées.'
    intro=stage/'intro';intro.mkdir(exist_ok=True);save(intro/'histoire.json',dict(scenes=[dict(narration_voix=phrase)]));speech(intro)
    it=read(intro/'_montage/timings-oraux.json');old_t=read(rootm/'timings.json');old_intro=old_t['scene_durations'][0]
    span=math.ceil(max(it['duration'],it['words'][-1]['end']+.08)*30)/30;delta=span-old_intro
    graph=f'[0:a]apad,atrim=duration={span},asetpts=PTS-STARTPTS[a];[1:a]atrim=start={old_intro},asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1[out]'
    run(['ffmpeg','-v','error','-y','-i',str(intro/'_montage/voix.mp3'),'-i',str(old/'voix.mp3'),'-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')])
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(m/'voix.mp3')]).strip())
    words=[dict(w='3' if x['w'].lower()=='trois' else x['w'],start=x['start'],end=x['end']) for x in it['words']]
    words += [dict(w=x['w'],start=x['start']+delta,end=x['end']+delta) for x in old_t['words'] if x['start']>=old_intro-.001]
    t=copy.deepcopy(old_t);t.update(duration=duration,words=words,scene_durations=[span]+old_t['scene_durations'][1:]);t['scene_durations'][-1]+=duration-sum(t['scene_durations']);save(m/'timings.json',t);save(m/'timings-oraux.json',t)
    story=read(w/'histoire.json');story['scenes'][0].update(narration='Top 3 des villes les plus embouteillées.',narration_voix=phrase);story['hook']=story['scenes'][0]['narration'];story['script']=' '.join(s['narration'] for s in story['scenes']);story['revision']='accroche-claire-v16'
    story['fun_fact_affichage']['debut']+=delta;story['fun_fact_affichage']['fin']+=delta
    story['depart_classement_secondes']=span;save(stage/'histoire.json',story)
    vf="scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.02+0.0007*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1"
    run(['ffmpeg','-v','error','-y','-loop','1','-i',str(SOURCES/'bouchons-hero-marc-nuit.png'),'-t',str(span),'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(m/'hero.mp4')])
    graph=f'[0:v]trim=end={span},setpts=PTS-STARTPTS[a];[1:v]trim=start={old_intro},setpts=PTS-STARTPTS,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]'
    run(['ffmpeg','-v','error','-y','-i',str(m/'hero.mp4'),'-i',str(old/'base.mp4'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(m/'base.mp4')])
    lines=[]
    for line in (old/'sous-titres-reference.ass').read_text(encoding='utf-8').splitlines():
        if 'PREMIER FEU AU GAZ' in line:continue
        if line.startswith('Dialogue:'):
            p=line.split(',',9)
            if seconds(p[2])<=old_intro:continue
            p[1]=_ass_time(max(span,seconds(p[1])+delta));p[2]=_ass_time(seconds(p[2])+delta);line=','.join(p)
        lines.append(line)
    (m/'sous-titres-reference.ass').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    shutil.copy2(m/'voix.mp3',m/'voix-hpb-v11.mp3');music('villes-plus-lentes-tomtom-2024',m,duration)
    save(stage/'recalage-accroche.json',dict(ancien_debut=old_intro,nouveau_debut=span,decalage=delta,texte=phrase,modele=it['model']))
    archive=rootm/'avant-accroche-claire';archive.mkdir(exist_ok=True)
    for name in ['histoire.json','script.txt']:
        if (w/name).exists() and not (archive/name).exists():shutil.copy2(w/name,archive/name)
    save(w/'histoire.json',story)
    for name in ['timings.json','timings-oraux.json','voix.mp3']:shutil.copy2(m/name,rootm/name)
    (w/'script.txt').write_text('\n\n'.join(s['narration'] for s in story['scenes']),encoding='utf-8')
    print('Accroche claire, premier rang à',span,'s ; décalage',delta,flush=True)
