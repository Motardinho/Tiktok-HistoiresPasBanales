"""Révisions utilisateur : habitacle, prononciations, hook max et trois musiques."""
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

from montage_reel import ROOT,SOURCES,run
from narrateur.musique import mix_voice
from narrateur.musique_v11 import create_bed
from revision_hpb_v9 import ASTRO,CAR,TRAFFIC,export,read,save
from revision_hpb_v10 import NUMBERS,display_words,item_for,plans,render_shot

NUMBERS.update({'quatre cent quatre-vingt-dix virgule quarante-huit':'490,48',
                'bi waï di':'BYD','kilomètres heure':'KM/H'})


def audio(slug):
    w=ROOT/'out'/slug
    story=read(w/'histoire.json')
    # Toujours repartir des timings v10, associés à la voix source v10.
    original=read(w/'timings-hpb-v10.json')
    oral=read(w/'timings-oraux-hpb-v10.json')
    starts=[sum(original['scene_durations'][:i]) for i in range(len(story['scenes'])+1)]
    corrections={2:('correction-bugatti-v11',None),4:('correction-byd-v11',None)} if slug==CAR else {0:('correction-intro-v11',5.55)} if slug==ASTRO else {}
    words=[];durations=[];cursor=0
    for i,scene in enumerate(story['scenes']):
        if i in corrections:
            name,limit=corrections[i]
            part=read(w/(name+'.json'));source=w/(name+'.mp3')
            start=0;end=limit or part['duration']
            source_words=part['words']
        else:
            source=w/'voix-hpb-v10.mp3';source_words=oral['words']
            start=11.24 if slug==ASTRO and i==1 else starts[i]
            end=starts[i+1]
        span=end-start
        target=w/f'v11-oral-{i}.wav'
        run(['ffmpeg','-v','error','-y','-i',str(source),'-af',
             f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS,apad,atrim=duration={span},afade=t=in:d=0.002,afade=t=out:st={max(0,span-.002)}:d=0.002',
             '-ar','44100','-ac','1',str(target)])
        words.extend(dict(w=x['w'],start=x['start']-start+cursor,
                          end=min(x['end'],end)-start+cursor)
                     for x in source_words if start<=x['start']<end)
        durations.append(span);cursor+=span
    (w/'v11-oral.txt').write_text(''.join(f"file 'v11-oral-{i}.wav'\n" for i in range(len(durations))),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','v11-oral.txt',
         '-c:a','libmp3lame','-b:a','128k','voix-hpb-v11.mp3'],w)
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(w/'voix-hpb-v11.mp3')]).strip())
    durations[-1]+=duration-cursor
    if slug==CAR:
        story['scenes'][2]['narration_voix']=story['scenes'][2]['narration_voix'].replace('virgule quatre huit','virgule quarante-huit')
        story['scenes'][4]['narration_voix']=story['scenes'][4]['narration_voix'].replace('BYD','Bi Waï Di')
    elif slug==ASTRO:
        story['scenes'][0]['narration']=story['scenes'][0]['narration_voix']='C’est la pesée en apesanteur : un ressort fait osciller l’astronaute pour mesurer sa masse.'
        for key in ['narration','narration_voix']:
            story['scenes'][1][key]=story['scenes'][1][key].split('La fréquence',1)[-1]
            story['scenes'][1][key]='La fréquence'+story['scenes'][1][key]
        story['hook']=story['scenes'][0]['narration']
    t=dict(duration=duration,scene_durations=durations,words=display_words(words))
    save(w/'timings-hpb-v11.json',t)
    save(w/'histoire-hpb-v11.json',story)
    return w,story,t,[sum(durations[:i]) for i in range(len(durations))]


def car_plans():
    return [
      [('ssc-dash',118,2.6),('ssc-wheel',113,2.8),('ssc-dash',119,2.5),('ssc-wheel',115,3)],
      [('ssc-wheel',103,3),('ssc-dash',116,3),('ssc-wheel',120,3),('ssc-dash',118,3)],
      [('bugatti-record',80,2.5),('bugatti-dash',140,3),('bugatti-wheel',120,3),('bugatti-dash',146,3)],
      [('bugatti-wheel',120,3),('bugatti-dash',146,3),('bugatti-record',160,2.5),('bugatti-dash',140,3)],
      [('byd-cockpit',110,3),('byd-road',108,3),('byd-native-meter',115,3),('byd-cockpit',104,3)],
      [('byd-cockpit',104,3),('byd-road',108,2.5),('byd-native-meter',115,3.5),('byd-road',115,3)],
      [('byd-cockpit',110,3),('byd-road',115,3),('byd-cockpit',116,3)]]


def native_shot(w,index,name,start,frames,cx=.5,window=1):
    filters={
      'ssc-dash':('ssc-tuatara','crop=372:660:1390:140'),
      'ssc-wheel':('ssc-tuatara','crop=506:900:330:180'),
      'bugatti-dash':('bugatti-record','crop=164:290:1650:110'),
      'bugatti-wheel':('bugatti-record','crop=310:550:780:400'),
      'byd-cockpit':('yangwang-u9-xtreme-2026','crop=184:326:200:709'),
      'byd-native-meter':('yangwang-u9-xtreme-2026','crop=274:488:1570:592'),
    }
    if name not in filters:return render_shot(w,index,name,start,frames,cx,window)
    source,vf=filters[name]
    variant='/cadre2' if name=='ssc-dash' else ''
    key=hashlib.sha1(f'{name}/{start}/{frames}/v11{variant}'.encode()).hexdigest()[:10]
    p=w/f'v11-plan{index:02d}-{key}.mp4'
    if not p.exists():
        run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(SOURCES/(source+'.mp4')),
             '-vf',vf+',scale=1080:1920,fps=30,setsar=1','-frames:v',str(frames),'-an',
             '-c:v','libx264','-preset','fast','-crf','19','-threads','3','-pix_fmt','yuv420p',
             '-r','30','-video_track_timescale','15360',str(p)])
    return p


def main(slug):
    w,story,t,starts=audio(slug)
    files=[];edits=[];cursor=0
    groups=car_plans() if slug==CAR else plans(slug)
    for scene,group in enumerate(groups):
        end=round(sum(t['scene_durations'][:scene+1])*30);j=0
        while cursor<end:
            name,start,limit,*framing=group[j%len(group)]
            frames=min(round(limit*30),end-cursor)
            cx=framing[0] if framing else .5;window=framing[1] if len(framing)>1 else 1
            p=native_shot(w,len(files),name,start,frames,cx,window)
            # Métadonnées uniformes : pas de remise à zéro du filtre fps entre archives.
            uniform=w/('v11-couleur-'+p.name)
            if not uniform.exists():
                run(['ffmpeg','-v','error','-y','-i',str(p),'-c','copy',
                     '-bsf:v','h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1',
                     '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(uniform)])
            files.append(uniform.name)
            edits.append(dict(scene=scene,source=name,source_start=start,start=cursor/30,duration=frames/30))
            cursor+=frames;j+=1
        print(slug,'scène',scene+1,'prête',flush=True)
    (w/'concat-v11.txt').write_text(''.join(f"file '{p}'\n" for p in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat-v11.txt','-c','copy','base-hpb-v11.mp4'],w)
    save(w/'montage-hpb-v11.json',edits)
    kind={CAR:'voitures',ASTRO:'espace',TRAFFIC:'bouchons'}[slug]
    music=ROOT/'assets/musique'/f'{kind}-hpb-v11.wav'
    create_bed(music,t['duration'],kind)
    mix_voice(w/'voix-hpb-v11.mp3',music,w/'mix-hpb-v11.wav',t['duration'],run)
    item=item_for(slug,t,starts)
    if slug==CAR:
        item['facts']=[(a,b,text.replace('490,484','490,48')) for a,b,text in item['facts']]
        item['caption_zones']=[(starts[4],t['duration'],1470)]
    elif slug==ASTRO:item['title']=['SE PESER','DANS',"L'ESPACE"]
    else:
        item['title']=['JUSQU’À','102 H','DANS LES BOUCHONS']
        a,b,label=item['facts'][0]
        item['facts']=[(0,4,'3 - PARIS'),(4,b,label)]+item['facts'][1:]
    export(slug,w,t,item,'mix-hpb-v11.wav','base-hpb-v11.mp4',
           cta_start=starts[6] if slug==TRAFFIC else None,version=11)
    for src,dst in [('voix-hpb-v11.mp3','voix.mp3'),('timings-hpb-v11.json','timings.json')]:shutil.copy2(w/src,w/dst)
    story.update(statut='Version v11 terminée',musique=dict(fichier=str(music.relative_to(ROOT)),
                 origine='Nouvelle composition originale v11',style={'voitures':'électro D mineur, basse FM et batterie',
                 'espace':'ambient D majeur, nappes et cloches, aucune batterie',
                 'bouchons':'groove Mi bémol, marimba et percussions sèches'}[kind]))
    save(w/'histoire.json',story);save(w/'histoire-hpb-v11.json',story)
    control=read(w/'controle-hpb-v11.json')
    control.update(ordre=[3,2,1] if slug!=ASTRO else None,musique=story['musique'],
                   separateurs='tirets simples',prononciations='quarante-huit ; Bi Waï Di' if slug==CAR else 'français',
                   hook='JUSQU’À 102 H DANS LES BOUCHONS' if slug==TRAFFIC else 'la pesée explicitée dès la première phrase' if slug==ASTRO else 'tableau de bord et compteur, vues réelles sans incrustation flottante')
    save(w/'controle-hpb-v11.json',control)
    print(slug,'V11 + comparaison terminées',flush=True)


if __name__=='__main__':
    for slug in sys.argv[1:] or (CAR,ASTRO,TRAFFIC):main(slug)
