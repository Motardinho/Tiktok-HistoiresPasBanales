"""Conserve la première phrase de teasing et coupe le reste de l'intro, sans nouvelle synthèse."""
import copy,shutil
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save

def shorten(w,oldstage,newstage):
    if (newstage/'intro-raccourcie.json').exists():return
    shutil.copytree(oldstage,newstage,dirs_exist_ok=True)
    m=newstage/'_montage';t=read(m/'timings-oraux.json');d=read(newstage/'histoire.json')
    first=d['scenes'][0]['narration'].split('. ')[0].rstrip('.')+'.'
    count=len(first.split());word=t['words'][count-1];following=t['words'][count]['start']
    keep=word['end']+max(0,min(.06,(following-word['end'])/2));old_intro=t['scene_durations'][0];delta=old_intro-keep
    original=oldstage/'_montage/voix.mp3';target=m/'voix-courte.mp3'
    graph=f'[0:a]atrim=end={keep},asetpts=PTS-STARTPTS[a];[0:a]atrim=start={old_intro},asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1[out]'
    run(['ffmpeg','-v','error','-y','-i',str(original),'-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(target)])
    target.replace(m/'voix.mp3')
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(m/'voix.mp3')]).strip())
    words=copy.deepcopy(t['words'][:count])
    words.extend(dict(w=x['w'],start=x['start']-delta,end=x['end']-delta) for x in t['words'] if x['start']>=old_intro-.001)
    t.update(words=words,duration=duration,scene_durations=[keep]+t['scene_durations'][1:])
    t['scene_durations'][-1]+=duration-sum(t['scene_durations']);save(m/'timings-oraux.json',t)
    d['scenes'][0]['narration']=first;d['scenes'][0]['narration_voix']=first;d['hook']=first;d['script']=' '.join(s['narration'] for s in d['scenes'])
    d['revision']=d.get('revision','')+'-depart-rapide';d['depart_classement_secondes']=keep
    save(newstage/'histoire.json',d);(newstage/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']),encoding='utf-8')
    save(newstage/'intro-raccourcie.json',dict(ancienne_duree=old_intro,nouvelle_duree=keep,texte=first,duree_finale=duration,voix='Hugo ElevenLabs conservé ; coupe PCM des segments puis nouvel alignement des mots'))
    print(w.name,'entrée 3 à',round(keep,2),'s',flush=True)

if __name__=='__main__':
    mapping={16:('revision-spectaculaire-v8','revision-spectaculaire-v9'),17:('revision-spectaculaire-v4','revision-spectaculaire-v5'),18:('revision-spectaculaire-v4','revision-spectaculaire-v5'),15:('revision-donnees-2025-v14','revision-donnees-2025-rapide-v15')}
    for n,(old,new) in mapping.items():
        w=next((ROOT/'out').glob(f'{n}-*'));shorten(w,w/'_montage'/old,w/'_montage'/new)
