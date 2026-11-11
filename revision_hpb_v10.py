"""Voix validée, ordre strict 3/2/1, sport spatial et musique adaptée."""
import copy
import hashlib
import json
import math
import re
import shutil
import sys
import unicodedata

from montage_reel import ROOT, SOURCES, run
from narrateur.musique import create_bed, mix_voice
from revision_hpb_v9 import ASTRO, CAR, TRAFFIC, export, read, save


def norm(value):
    return unicodedata.normalize('NFKC',value).lower().replace('’',"'").strip('.,;:!?«»')


NUMBERS={
 'quatre cent soixante-quatorze virgule huit':'474,8',
 'quatre cent quatre-vingt-dix virgule quatre huit':'490,48',
 'cinq cent trois virgule dix-sept':'503,17',
 'quatre cent quatre-vingt-seize virgule vingt-deux':'496,22',
 'deux mille vingt-quatre':'2024','deux mille vingt-six':'2026','deux mille dix-neuf':'2019',
 'mille six cents':'1\u202f600','trois mille':'3\u202f000','deux cent quarante':'240',
 'cent trente-deux':'132','cent une':'101','cent deux':'102','quatre-vingt-dix-sept':'97',
 'trois cents plus':'300+','trois cents':'300','cinq cents':'500',
 'vé huit':'V8','double vé seize':'W16',
 'numéro trois':'N°3','numéro deux':'N°2','numéro un':'N°1',
 'deux':'2','trois':'3','quatre':'4','cinq':'5',
}


def dedupe_overlapping_words(words):
    """Retirer les doublons d'alignement, sans supprimer une répétition orale."""
    result=[]
    for word in words:
        previous=result[-1] if result else None
        if (previous and norm(previous['w'])==norm(word['w'])
                and min(previous['end'],word['end'])>max(previous['start'],word['start'])):
            previous['start']=min(previous['start'],word['start'])
            previous['end']=max(previous['end'],word['end'])
        else:
            result.append(copy.deepcopy(word))
    return result


def display_words(words):
    result=[];i=0
    patterns=sorted(NUMBERS,key=lambda p:-len(p.split()))
    while i<len(words):
        for pattern in patterns:
            n=len(pattern.split());group=words[i:i+n]
            if ' '.join(norm(x['w']) for x in group)==pattern:
                suffix=re.search(r'[.,;:!?]+$',group[-1]['w'])
                result.append(dict(w=NUMBERS[pattern]+(suffix.group() if suffix else ''),
                                   start=group[0]['start'],end=group[-1]['end']))
                i+=n;break
        else:
            word=copy.deepcopy(words[i])
            if norm(word['w'])=='une' and i+1<len(words) and norm(words[i+1]['w']) in ('heure','seconde'):
                word['w']='1'
            result.append(word);i+=1
    return dedupe_overlapping_words(result)


def prepare(slug):
    w=ROOT/'out'/slug
    story=read(w/('histoire-top3-hpb-v10.json' if slug==CAR else 'histoire-hpb-v10.json'))
    oral=read(w/'timings-oraux-hpb-v10.json')
    duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(w/'voix-hpb-v10.mp3')]).strip())
    tokens=[(i,norm(word['w'])) for i,word in enumerate(oral['words']) if norm(word['w'])]
    starts=[0.0];cursor=0
    # Délimiter les scènes par leurs vrais premiers mots, pas par une estimation
    # au prorata des caractères (qui se décale lorsque les nombres changent).
    for scene in story['scenes'][1:]:
        prefix=[norm(x) for x in scene['narration_voix'].split() if norm(x)][:4]
        found=next((j for j in range(cursor+1,len(tokens)-len(prefix)+1)
                    if [x[1] for x in tokens[j:j+len(prefix)]]==prefix),None)
        if found is None:raise ValueError(f'Début de scène introuvable : {prefix}')
        starts.append(oral['words'][tokens[found][0]]['start']);cursor=found
    durations=[b-a for a,b in zip(starts,starts[1:]+[duration])]
    timing=dict(duration=duration,scene_durations=durations,words=display_words(oral['words']))
    assert duration>60
    if slug in (CAR,TRAFFIC):
        assert [x['rang'] for x in story['scenes'] if x['rang'] is not None]==[3,2,1]
        assert norm(story['scenes'][0]['narration_voix']).startswith('numéro trois')
    text=' '.join(x['w'] for x in timing['words'])
    assert not re.search(r'\b(cents|cent|horsepower)\b',text,re.I),text
    save(w/'timings-hpb-v10.json',timing)
    print(slug,'scènes alignées',list(map(lambda d:round(d,2),durations)),flush=True)
    return w,story,timing,starts


def render_shot(w,index,name,start,frames,cx=.5,window=1):
    key=hashlib.sha1(f'{name}/{start}/{frames}/{cx}/{window}/v10'.encode()).hexdigest()[:10]
    target=w/f'v10-plan{index:02d}-{key}.mp4'
    if target.exists():return target
    if name.startswith('byd-'):
        source=SOURCES/'yangwang-u9-xtreme-2026.mp4'
        graph=('[0:v]split=2[a][b];[a]crop=1920:582:0:84,crop=328:582:796:0,scale=1080:1920[road];')
        if name=='byd-meter':
            graph+='[b]crop=388:326:1510:709,scale=800:672[detail];[road][detail]overlay=140:400,fps=30,setsar=1[v]'
        elif name=='byd-driver':
            graph+='[b]crop=440:326:22:709,scale=800:592[detail];[road][detail]overlay=140:475,fps=30,setsar=1[v]'
        else:
            graph='[0:v]crop=1920:582:0:84,crop=328:582:796:0,scale=1080:1920,fps=30,setsar=1[v]'
        opts=['-filter_complex',graph,'-map','[v]']
    elif name=='ssc-meter':
        source=SOURCES/'ssc-tuatara.mp4'
        graph=('[0:v]split=2[a][b];[a]crop=1920:700:0:0,crop=394:700:763:0,scale=1080:1920[road];'
               '[b]crop=880:370:0:700,scale=940:395[detail];[road][detail]overlay=70:620,fps=30,setsar=1[v]')
        opts=['-filter_complex',graph,'-map','[v]']
    else:
        source=SOURCES/('bugatti-record.mp4' if name=='bugatti-emb' else 'astronautes-sport-machines.mp4' if name=='ared-rotation' else name+'.mp4')
        if name=='bugatti-emb':
            vf='crop=1920:550:0:400,crop=310:550:805:0,scale=1080:1920,fps=30,setsar=1'
        elif name=='ared-rotation':
            # La prise est couchée : la rotation remet le corps et le mécanisme
            # dans le format portrait sans supprimer les pieds ou la barre.
            vf='transpose=clock,scale=1080:1920,fps=30,setsar=1'
        else:
            lead='crop=iw:trunc(ih*0.74/2)*2:0:(ih-oh)/2,' if name in ('bugatti-record','ssc-tuatara') else ''
            vf=lead+(f"crop=w='trunc(ih*{window}*9/16/2)*2':h='trunc(ih*{window}/2)*2':"
                     f"x='max(0,min(iw-ow,iw*{cx}-ow/2))':y=ih-oh,"
                     'scale=1080:1920:flags=lanczos,fps=30,setsar=1')
        opts=['-vf',vf]
    run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(source),*opts,
         '-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19',
         '-threads','3','-pix_fmt','yuv420p','-r','30','-video_track_timescale','15360',str(target)])
    actual=int(run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(target)]).strip())
    if actual!=frames:raise ValueError(f'Plan trop court : {name}, {actual}/{frames} images')
    return target


def plans(slug):
    # Durées maximales par plan ; boucler les points d'entrée, jamais figer ou
    # ralentir artificiellement pour atteindre la durée de narration.
    if slug==CAR:
        return [
          [('ssc-meter',151,2.6),('ssc-tuatara',119,2.8),('ssc-tuatara',6,2.5),('ssc-meter',152,3)],
          [('ssc-tuatara',103,3.2),('ssc-tuatara',10,2.5),('ssc-tuatara',120,3),('ssc-meter',151,3)],
          [('bugatti-record',80,3),('bugatti-record',160,3),('bugatti-emb',128,3),('bugatti-emb',146,3)],
          [('bugatti-emb',120,3),('bugatti-record',80,3),('bugatti-emb',146,3),('bugatti-record',160,3)],
          [('byd-meter',115,3),('byd-road',108,3),('byd-driver',104,3),('byd-meter',114,3)],
          [('byd-driver',104,3),('byd-road',108,2.5),('byd-meter',115,3.5),('byd-road',115,3)],
          [('byd-road',115,3),('byd-driver',110,3),('byd-meter',116,3)]]
    if slug==TRAFFIC:
        paris=[('paris-soir',4,3,.48),('paris-soir',14,3,.5),('paris-soir',20,3,.53)]
        london=[('londres',8,3,.4),('londres',16,3,.5),('londres',21,3,.55)]
        ny=[('new-york-bouchons',0,3,.5,.7),('new-york-bouchons',4,3,.5,.8),('new-york-bouchons',1,3,.5)]
        return [paris,paris,london,london,ny,ny,ny]
    return [
      [('astronautes-masse',24,2.8,.53,.84),('astronautes-masse',32,2.8,.53,.78),('astronautes-masse',38,3,.53,.84)],
      [('astronautes-masse',54,3,.53),('astronautes-masse',24,3,.53),('astronautes-masse',34,3,.53)],
      [('nyberg-cheveux',128,2.5,.51),('ared-rotation',81,2.8),('williams-visite',247,3,.68)],
      [('astronautes-sport-machines',42,3,.55),('astronautes-sport-machines',94,3,.56),('astronautes-sport-machines',102,3,.54)],
      [('astronautes-sport-machines',52,3,.56),('astronautes-sport-machines',113,3,.53),('astronautes-sport-machines',55,3,.58)],
      [('williams-visite',247,3,.68),('williams-visite',263,3,.43),('williams-visite',272,3,.46),('ared-rotation',81,2.5)],
      [('astronautes-sport-machines',94,2.5,.56),('astronautes-sport-machines',113,2.5,.53),('williams-visite',263,2.5,.43)],
      [('williams-visite',289,2.5,.52),('nyberg-cheveux',125,2.5,.51),('williams-visite',310,2.5,.52)]]


def item_for(slug,t,starts):
    end=t['duration']
    if slug==CAR:
        return dict(title=['TOP 3','DES VOITURES','LES PLUS RAPIDES'],series='TOP 3 • VITESSE',
                    credits='SSC / Bugatti / BYD',facts=[
                    (0,starts[2],'3 • SSC TUATARA\\N474,8 KM/H'),
                    (starts[2],starts[4],'2 • CHIRON SUPER SPORT 300+\\N490,484 KM/H'),
                    (starts[4],end,'1 • YANGWANG U9 XTREME\\N503,17 KM/H')])
    if slug==TRAFFIC:
        return dict(title=['97 H','DANS LES','BOUCHONS'],series='3 VILLES • BOUCHONS',credits='Pexels • INRIX 2024',facts=[
                    (0,starts[2],'3 • PARIS • 2024\\N97 H DANS LES BOUCHONS'),
                    (starts[2],starts[4],'2 • LONDRES • 2024\\N101 H DANS LES BOUCHONS'),
                    (starts[4],starts[6],'1 • NEW YORK • 2024\\N102 H DANS LES BOUCHONS')])
    return dict(title=['CES MACHINES','DANS','L’ESPACE'],series='COMMENT C’EST POSSIBLE ?',credits='ASC / NASA',facts=[
                (starts[1],starts[2],'MESURER LA MASSE'),
                (starts[2],starts[3],'ENVIRON 2 H D’EXERCICE PAR JOUR'),
                (starts[3],starts[4],'VÉLO • SANS SELLE'),
                (starts[4],starts[5],'TAPIS • AVEC HARNAIS'),
                (starts[5],starts[6],'MUSCULATION • ARED')])


def main(slug):
    w,story,t,starts=prepare(slug)
    files=[];edits=[];cursor=0
    for scene,(group,duration) in enumerate(zip(plans(slug),t['scene_durations'])):
        end=round(sum(t['scene_durations'][:scene+1])*30);j=0
        while cursor<end:
            name,start,limit,*framing=group[j%len(group)]
            frames=min(round(limit*30),end-cursor)
            cx=framing[0] if framing else .5;window=framing[1] if len(framing)>1 else 1
            target=render_shot(w,len(files),name,start,frames,cx,window)
            files.append(target.name)
            edits.append(dict(scene=scene,source=name,source_start=start,start=cursor/30,duration=frames/30))
            cursor+=frames;j+=1
        print(slug,'scène',scene+1,'prête',flush=True)
    if slug==ASTRO:
        # Les archives ASC et NASA portent des métadonnées couleur différentes.
        # Les uniformiser dans les en-têtes H264 avant concaténation empêche une
        # réinitialisation du filtre fps au milieu de la vidéo.
        uniform=[]
        for file in files:
            target=w/('couleur-'+file)
            if not target.exists():
                run(['ffmpeg','-v','error','-y','-i',str(w/file),'-c','copy',
                     '-bsf:v','h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1',
                     '-color_range','tv','-colorspace','bt709','-color_primaries','bt709',
                     '-color_trc','bt709',str(target)])
            uniform.append(target.name)
        files=uniform
    (w/'concat-v10.txt').write_text(''.join(f"file '{p}'\n" for p in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat-v10.txt','-c','copy','base-hpb-v10.mp4'],w)
    save(w/'montage-hpb-v10.json',edits)
    kind={ASTRO:'espace',CAR:'voitures',TRAFFIC:'bouchons'}[slug]
    music=ROOT/'assets/musique'/f'{kind}-hpb-v10.wav'
    create_bed(music,t['duration'],kind)
    mix_voice(w/'voix-hpb-v10.mp3',music,w/'mix-hpb-v10.wav',t['duration'],run)
    item=item_for(slug,t,starts)
    export(slug,w,t,item,'mix-hpb-v10.wav','base-hpb-v10.mp4',
           cta_start=starts[6] if slug==TRAFFIC else None,version=10)
    for src,dst in [('voix-hpb-v10.mp3','voix.mp3'),('timings-hpb-v10.json','timings.json')]:shutil.copy2(w/src,w/dst)
    story.update(statut='Rendu v10 terminé : voix ElevenLabs validée et musique originale discrète',
                 musique=dict(fichier=str(music.relative_to(ROOT)),origine='Composition instrumentale originale, synthèse locale',mix='niveau bas, atténuation pendant la parole'),
                 ordre=[3,2,1] if slug in (CAR,TRAFFIC) else None)
    save(w/'histoire.json',story)
    save(w/('histoire-top3-hpb-v10.json' if slug==CAR else 'histoire-hpb-v10.json'),story)
    control=read(w/'controle-hpb-v10.json')
    control.update(ordre=story['ordre'],musique=story['musique'],voix='ElevenLabs Hugo validée',
                   chiffres='Voix en français, transcription en chiffres, timings recalculés')
    save(w/'controle-hpb-v10.json',control)
    print(slug,'FINAL v10 + comparaison terminés',flush=True)


if __name__=='__main__':
    for slug in sys.argv[1:] or (CAR,ASTRO,TRAFFIC):main(slug)
