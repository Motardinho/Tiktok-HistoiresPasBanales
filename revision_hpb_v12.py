"""Compteurs brefs, plans extérieurs distincts et pistes musicales de bibliothèque."""
import hashlib
import shutil
import sys
from montage_reel import ROOT,SOURCES,run
from narrateur.musique import mix_voice
from narrateur.validation import validate_duration
from revision_hpb_v11 import ASTRO,CAR,TRAFFIC,read,save,display_words,item_for,export,native_shot


def prepare_car():
    w=ROOT/'out'/CAR;t=read(w/'timings-hpb-v11.json');d=read(w/'histoire.json')
    start=sum(t['scene_durations'][:5]);end=start+t['scene_durations'][5]
    fix=read(w/'correction-sans-relance-compteur-v12.json');span=fix['duration']
    graph=(f'[0:a]atrim=0:{start},asetpts=PTS-STARTPTS[a];'
           f'[1:a]apad,atrim=duration={span},asetpts=PTS-STARTPTS[b];'
           f'[0:a]atrim=start={end}:end={t["duration"]},asetpts=PTS-STARTPTS[c];'
           '[a][b][c]concat=n=3:v=0:a=1[out]')
    run(['ffmpeg','-v','error','-y','-i',str(w/'voix-hpb-v11.mp3'),'-i',str(w/'correction-sans-relance-compteur-v12.mp3'),
         '-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','128k',str(w/'voix-hpb-v12.mp3')])
    delta=span-(end-start)
    words=[x for x in t['words'] if x['start']<start]
    words.extend(dict(w=x['w'],start=x['start']+start,end=x['end']+start) for x in display_words(fix['words']))
    words.extend(dict(w=x['w'],start=x['start']+delta,end=x['end']+delta) for x in t['words'] if x['start']>=end)
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(w/'voix-hpb-v12.mp3')]).strip())
    durations=t['scene_durations'][:];durations[5]=span;durations[-1]+=duration-sum(durations)
    t=dict(duration=duration,scene_durations=durations,words=words)
    d['scenes'][5]['narration_voix']='Quatre moteurs électriques, plus de trois mille chevaux, et Marc Basseng au volant. À plus de cinq cents kilomètres heure, la route défile à une vitesse folle. Elle bat ainsi son précédent record, qui était de quatre cent quatre-vingt-seize virgule vingt-deux kilomètres heure.'
    d['scenes'][5]['narration']='4 moteurs électriques, plus de 3 000 chevaux, et Marc Basseng au volant. À plus de 500 kilomètres heure, la route défile à une vitesse folle. Elle bat ainsi son précédent record, qui était de 496,22 kilomètres heure.'
    assert not any('compteur' in s['narration'].lower() for s in d['scenes'])
    save(w/'timings-hpb-v12.json',t);save(w/'histoire-hpb-v12.json',d)
    return w,d,t


def blocks():
    # Liste finie : aucune boucle de plans et aucun intervalle source réutilisé.
    return [
      [('ssc-dash',118,2.5,.5),('ssc-road',1,3,.5),('ssc-road',10,3,.5),('ssc-road',14,3,.5),
       ('ssc-speed',15,3,.5),('ssc-road',18,2.8,.5),('ssc-road',22,2.8,.5),('ssc-speed',39,2,.5),
       ('ssc-tuatara',6,2.5,.5),('ssc-road',4.05,2.5,.5)],
      [('bugatti-dash',140,2.5,.5),('bugatti-record',89,1.8,.5),('bugatti-record',79,3.5,.5),
       ('bugatti-record',83,2.5,.5),('bugatti-record',86,2.8,.5),('bugatti-record',154,2.5,.5),
       ('bugatti-record',157,3.5,.5),('bugatti-record',161,2.5,.5),('bugatti-record',40,3,.5)],
      [('byd-native-meter',115,2.5,.5),('yangwang-u9-xtreme-2025',26,3,.55),
       ('yangwang-u9-xtreme-2025',30,3,.55),('yangwang-u9-xtreme-2025',34,1.4,.16),
       ('yangwang-u9-xtreme-2025',38,3,.42),('yangwang-u9-xtreme-2025',42,3,.5),
       ('yangwang-u9-xtreme-2025',46,3,.5),('yangwang-u9-xtreme-2025',64,3,.55),
       ('yangwang-u9-xtreme-2025',68,3,.55),('yangwang-u9-xtreme-2025',72,2,.16),
       ('yangwang-u9-xtreme-2025',76,3,.58),('yangwang-u9-xtreme-2025',80,3,.5),
       ('yangwang-u9-xtreme-2025',84,3,.5)]]


def shot(w,i,name,start,frames,cx):
    if name in ('ssc-dash','bugatti-dash','byd-native-meter'):
        return native_shot(w,i,name,start,frames,cx)
    key=hashlib.sha1(f'{name}/{start}/{frames}/{cx}/exterieur12'.encode()).hexdigest()[:10]
    p=w/f'v12-plan{i:02d}-{key}.mp4'
    if not p.exists():
        vf=('crop=iw:trunc(ih*0.74/2)*2:0:(ih-oh)/2,'
            f'crop=trunc(ih*9/16/2)*2:ih:max(0\\,min(iw-ow\\,iw*{cx}-ow/2)):0,'
            'scale=1080:1920,fps=30,setsar=1')
        run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(SOURCES/(name+'.mp4')),'-vf',vf,
             '-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','3',
             '-pix_fmt','yuv420p','-r','30','-video_track_timescale','15360',str(p)])
    return p


def build_car(w,t):
    limits=[sum(t['scene_durations'][:2]),sum(t['scene_durations'][:4]),t['duration']]
    files=[];edits=[];cursor=0;used={};counters=[]
    for rank,group,end in zip([3,2,1],blocks(),limits):
        for name,start,limit,cx in group:
            if cursor>=round(end*30):break
            frames=min(round(limit*30),round(end*30)-cursor);duration=frames/30
            source={'ssc-dash':'ssc-tuatara','bugatti-dash':'bugatti-record','byd-native-meter':'yangwang-u9-xtreme-2026'}.get(name,name)
            assert not any(max(start,a)<min(start+duration,b)-.001 for a,b in used.get(source,[])),f'Plan répété {source}'
            used.setdefault(source,[]).append((start,start+duration))
            p=shot(w,len(files),name,start,frames,cx)
            standard=w/('v12-couleur-'+p.name)
            if not standard.exists():
                run(['ffmpeg','-v','error','-y','-i',str(p),'-c','copy','-bsf:v',
                     'h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1',
                     '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(standard)])
            counter=name in ('ssc-dash','bugatti-dash','byd-native-meter')
            if counter:counters.append(dict(rang=rank,start=cursor/30,duration=duration))
            edits.append(dict(rang=rank,source=source,start_source=start,start=cursor/30,duration=duration,compteur=counter,fichier=standard.name))
            files.append(standard.name);cursor+=frames
        assert cursor==round(end*30),'Pas assez de plans uniques pour cette entrée'
        print('Voitures - rang',rank,'monté',flush=True)
    assert len(counters)==3 and all(2<=x['duration']<=3 for x in counters)
    (w/'concat-v12.txt').write_text(''.join(f"file '{p}'\n" for p in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat-v12.txt','-c','copy','base-hpb-v12.mp4'],w)
    save(w/'montage-hpb-v12.json',edits)
    return counters


def music(slug,w,duration):
    kind={CAR:'voitures',ASTRO:'espace',TRAFFIC:'bouchons'}[slug]
    folder=ROOT/'assets/musique/mixkit'
    track=next(x for x in read(folder/'sources.json') if x['slug']==kind)
    bed=w/'musique-hpb-v12.wav'
    run(['ffmpeg','-v','error','-y','-ss',str(track['start']),'-i',str(folder/(kind+'.mp3')),
         '-af',f'atrim=duration={duration},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2:LRA=9,afade=t=in:d=0.8,afade=t=out:st={duration-2}:d=2',
         '-ar','44100','-ac','2','-c:a','pcm_s16le',str(bed)])
    voice=w/('voix-hpb-v12.mp3' if slug==CAR else 'voix-hpb-v11.mp3')
    mix_voice(voice,bed,w/'mix-hpb-v12.wav',duration,run)
    return track


def unchanged_video(slug,w,t):
    run(['ffmpeg','-v','error','-y','-i','final-hpb-v11.mp4','-i','mix-hpb-v12.wav',
         '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(t['duration']),
         '-movflags','+faststart','final-hpb-v12.mp4'],w)
    duration=validate_duration(w/'final-hpb-v12.mp4')
    run(['ffmpeg','-v','error','-y','-i','comparaison-hpb-v11.mp4','-i','final-hpb-v12.mp4',
         '-map','0:v:0','-map','0:a:0','-map','1:a:0','-c','copy','-metadata:s:a:0','title=Original',
         '-metadata:s:a:1','title=Histoires pas banales','-disposition:a:0','0','-disposition:a:1','default',
         '-movflags','+faststart','comparaison-hpb-v12.mp4'],w)
    for a,b in [('final-hpb-v12.mp4','final.mp4'),('comparaison-hpb-v12.mp4','comparaison.mp4')]:shutil.copy2(w/a,w/b)
    save(w/'controle-hpb-v12.json',dict(duration_mp4=duration,images='Reprises de la v11 validée',musique='Nouvelle piste Mixkit'))


def main(slug):
    if slug==CAR:
        w,d,t=prepare_car();counters=build_car(w,t)
    else:
        w=ROOT/'out'/slug;d=read(w/'histoire.json');t=read(w/'timings-hpb-v11.json');counters=None
    track=music(slug,w,t['duration'])
    if slug==CAR:
        starts=[sum(t['scene_durations'][:i]) for i in range(len(t['scene_durations']))]
        item=item_for(CAR,t,starts);item['facts']=[(a,b,s.replace('490,484','490,48')) for a,b,s in item['facts']]
        export(slug,w,t,item,'mix-hpb-v12.wav','base-hpb-v12.mp4',version=12)
        for a,b in [('voix-hpb-v12.mp3','voix.mp3'),('timings-hpb-v12.json','timings.json')]:shutil.copy2(w/a,w/b)
    else:unchanged_video(slug,w,t)
    control=read(w/'controle-hpb-v12.json');control.update(musique=track,compteurs=counters,plans_sans_boucle=True)
    save(w/'controle-hpb-v12.json',control)
    d.update(statut='Version v12 - musiques de bibliothèque',musique=track)
    save(w/'histoire.json',d);save(w/'histoire-hpb-v12.json',d)
    print(slug,'V12 vidéo et comparaison prêtes',flush=True)


if __name__=='__main__':
    for slug in sys.argv[1:] or (CAR,ASTRO,TRAFFIC):main(slug)
