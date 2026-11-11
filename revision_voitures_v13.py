"""Retire la relance sur les marques de piste, devenue sans raccord visuel."""
import copy
import shutil
from montage_reel import ROOT,run
from narrateur.musique import mix_voice
from revision_hpb_v11 import CAR,read,save,item_for,export


def main():
    w=ROOT/'out'/CAR
    t=copy.deepcopy(read(w/'timings-hpb-v12.json'))
    story=read(w/'histoire.json')
    begin=24.12;end=sum(t['scene_durations'][:2]);removed=end-begin
    assert any(x['w']=='Regarde' and begin<=x['start']<end for x in t['words'])
    source_duration=t['duration']
    t['words']=[dict(w=x['w'],start=x['start']-(removed if x['start']>=end else 0),
                     end=x['end']-(removed if x['start']>=end else 0))
                for x in t['words'] if x['start']<begin or x['start']>=end]
    t['scene_durations'][1]-=removed;t['duration']-=removed
    graph=(f'[0:a]atrim=0:{begin},asetpts=PTS-STARTPTS[a];'
           f'[0:a]atrim=start={end}:end={source_duration},asetpts=PTS-STARTPTS[b];'
           '[a][b]concat=n=2:v=0:a=1[out]')
    run(['ffmpeg','-v','error','-y','-i','voix-hpb-v12.mp3','-filter_complex',graph,
         '-map','[out]','-c:a','libmp3lame','-b:a','128k','voix-hpb-v13.mp3'],w)
    # Le plan 22,1-24,12 s montrait un avion dans le film source : le remplacer
    # par deux intervalles inédits de la voiture en mouvement.
    crop=('crop=iw:trunc(ih*0.74/2)*2:0:(ih-oh)/2,'
          'crop=trunc(ih*9/16/2)*2:ih:(iw-ow)/2:0,scale=1080:1920,fps=30,setsar=1')
    graph=(f'[0:v]split=2[x][y];[x]trim=end=22.1,setpts=PTS-STARTPTS[a];'
           f'[1:v]trim=end=1,setpts=PTS-STARTPTS,{crop}[c];'
           f'[2:v]trim=start=4.05:end=5.07,setpts=PTS-STARTPTS,{crop}[d];'
           f'[y]trim=start={end},setpts=PTS-STARTPTS[b];'
           '[a][c][d][b]concat=n=4:v=1:a=0,fps=30,setsar=1[out]')
    road=ROOT/'assets/sources-reelles/ssc-road.mp4'
    run(['ffmpeg','-v','error','-y','-i','base-hpb-v12.mp4','-i',str(road),'-i',str(road),'-filter_complex',graph,
         '-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','3',
         '-pix_fmt','yuv420p','-video_track_timescale','15360','base-hpb-v13.mp4'],w)
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','voix-hpb-v13.mp3'],w).strip())
    t['scene_durations'][-1]+=duration-t['duration'];t['duration']=duration
    save(w/'timings-hpb-v13.json',t)
    track=read(w/'controle-hpb-v12.json')['musique']
    run(['ffmpeg','-v','error','-y','-ss',str(track['start']),'-i',str(ROOT/'assets/musique/mixkit/voitures.mp3'),
         '-af',f'atrim=duration={duration},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2:LRA=9,afade=t=in:d=0.8,afade=t=out:st={duration-2}:d=2',
         '-ar','44100','-ac','2','-c:a','pcm_s16le','musique-hpb-v13.wav'],w)
    mix_voice(w/'voix-hpb-v13.mp3',w/'musique-hpb-v13.wav',w/'mix-hpb-v13.wav',duration,run)
    starts=[sum(t['scene_durations'][:i]) for i in range(len(t['scene_durations']))]
    item=item_for(CAR,t,starts);item['facts']=[(a,b,s.replace('490,484','490,48')) for a,b,s in item['facts']]
    export(CAR,w,t,item,'mix-hpb-v13.wav','base-hpb-v13.mp4',version=13)
    for key in ['narration','narration_voix']:
        story['scenes'][1][key]=story['scenes'][1][key].replace(' Regarde les marques de la piste défiler.','')
    story['statut']='Version v13 - relance hors raccord retirée'
    save(w/'histoire-hpb-v13.json',story);save(w/'histoire.json',story)
    for source,target in [('voix-hpb-v13.mp3','voix.mp3'),('timings-hpb-v13.json','timings.json')]:shutil.copy2(w/source,w/target)
    edits=[]
    for old in read(w/'montage-hpb-v12.json'):
        clip=copy.deepcopy(old);a=clip['start'];b=a+clip['duration']
        if a>=begin and b<=end+.04:continue
        if a<begin<b:clip['duration']=begin-a
        if a>=end-.001:clip['start']-=removed
        if clip['source']=='ssc-tuatara' and clip['start_source']==6:
            for source_start,at,span in [(0,22.1,1),(4.05,23.1,begin-23.1)]:
                replacement=copy.deepcopy(clip)
                replacement.update(source='ssc-road',start_source=source_start,start=at,duration=span,fichier='Coupe v13 - plan extérieur')
                edits.append(replacement)
            continue
        edits.append(clip)
    save(w/'montage-hpb-v13.json',edits)
    counters=[dict(rang=e['rang'],start=e['start'],duration=e['duration']) for e in edits if e['compteur']]
    assert len(counters)==3 and all(abs(x['duration']-2.5)<.001 for x in counters)
    control=read(w/'controle-hpb-v13.json');control.update(musique=track,compteurs=counters,
           correction='Phrase sur les marques de piste retirée de la voix et des sous-titres, coupe vidéo correspondante',ordre=[3,2,1])
    save(w/'controle-hpb-v13.json',control)
    print('Voitures v13 corrigées',duration,'s',flush=True)


if __name__=='__main__':main()
