"""Montage des trois nouvelles vidéos, sources réelles et graphiques originaux."""
import argparse
import copy
import html
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageDraw

from construire_identite import font, INK, CREAM, YELLOW
from habillage_reference import layers, subs
from montage_reel import ROOT, run
from narrateur import assemble
from narrateur.musique import mix_voice
from narrateur.validation import validate_duration
from produire_lot_16_18 import FOLDERS, read, save, norm

ASSETS=ROOT/'assets/lot-16-18'

def numeric_words(words):
    replacements={'deux mille vingt-six':'2026','cent quarante-cinq':'145','treize mille':'13 000',
                  'trois cent vingt':'320','cent soixante':'160','dix-sept virgule un':'17,1',
                  'neuf virgule huit':'9,8','un virgule sept':'1,7','soixante':'60',
                  'cent':'100','dix':'10','numéro trois':'N°3','numéro deux':'N°2','numéro un':'N°1',
                  'deux millions':'2 millions','trois':'3','kilomètres heure':'KM/H','kilomètres carrés':'km²'}
    out=[];i=0
    for_unused=None
    patterns=sorted(replacements,key=lambda x:-len(x.split()))
    while i<len(words):
        for phrase in patterns:
            n=len(phrase.split());group=words[i:i+n]
            if len(group)==n and ' '.join(norm(x['w']) for x in group)==phrase:
                suffix=re.search(r'[.,;:!?]+$',group[-1]['w'])
                out.append(dict(w=replacements[phrase]+(suffix.group() if suffix else ''),start=group[0]['start'],end=group[-1]['end']))
                i+=n;break
        else:out.append(copy.deepcopy(words[i]));i+=1
    return out

def title(draw,text,y,size=64,fill=CREAM):
    while draw.textlength(text,font=font(size))>930:size-=2
    draw.text((75,y),text,font=font(size),fill=fill)

def background():
    im=Image.new('RGB',(1080,1920),INK);d=ImageDraw.Draw(im)
    for x in range(0,1080,60):d.line((x,0,x,1920),fill='#1b2430',width=1)
    for y in range(0,1920,60):d.line((0,y,1080,y),fill='#1b2430',width=1)
    return im

def rings(geometry):
    if geometry['type']=='Polygon':return [geometry['coordinates'][0]]
    return [p[0] for p in geometry['coordinates']]

GEO=None
def country_points(code):
    global GEO
    if GEO is None:GEO=read(ASSETS/'countries.geojson')['features']
    feature=next(f for f in GEO if f['properties']['ADM0_A3']==code)
    polygons=[]
    for ring in rings(feature['geometry']):
        # Natural Earth utilise des frontières de fait ; la Crimée reste
        # ukrainienne dans notre carte des territoires internationalement reconnus.
        if code=='RUS' and all(32<lon<37 and 44<lat<46.5 for lon,lat in ring):
            continue
        points=[]
        for lon,lat in ring:
            if code=='RUS' and lon<0:lon+=360
            points.append((math.radians(lon)*math.cos(math.radians(45)),-math.sin(math.radians(lat))/math.cos(math.radians(45))))
        polygons.append(points)
    return polygons

def map_shape(d,code,box,color=YELLOW,scale=None):
    polygons=country_points(code);allp=[p for ring in polygons for p in ring]
    minx,maxx=min(x for x,y in allp),max(x for x,y in allp)
    miny,maxy=min(y for x,y in allp),max(y for x,y in allp)
    x,y,width,height=box
    factor=scale or min(width/(maxx-minx),height/(maxy-miny))
    offsetx=x+(width-(maxx-minx)*factor)/2;offsety=y+(height-(maxy-miny)*factor)/2
    for ring in polygons:
        p=[(offsetx+(a-minx)*factor,offsety+(b-miny)*factor) for a,b in ring]
        if len(p)>=3:d.polygon(p,fill=color,outline=CREAM,width=2)
    return factor

def graphic(path,kind,phase=0):
    im=background();d=ImageDraw.Draw(im)
    if kind in ('USA','CAN','RUS'):
        names={'USA':'ÉTATS-UNIS','CAN':'CANADA','RUS':'RUSSIE'}
        values={'USA':'9,8 MILLIONS KM²','CAN':'PRESQUE 10 MILLIONS KM²','RUS':'17,1 MILLIONS KM²'}
        title(d,names[kind],340,76,YELLOW);title(d,values[kind],450,58)
        map_shape(d,kind,(65,620,950,480))
        title(d,'SUPERFICIE TOTALE - EAUX INCLUSES',1580,33)
        title(d,'CARTE - PROJECTION ÉQUIVALENTE',1635,26,'#9caabc')
    elif kind=='compare':
        title(d,'LA DIFFÉRENCE EST LÀ',330,58)
        # Lambert cylindrical equal-area coordinates and identical scale.
        scale=210
        map_shape(d,'CAN',(70,465,940,330),scale=scale)
        map_shape(d,'RUS',(70,900,940,330),scale=scale)
        title(d,'CANADA',810,45);title(d,'RUSSIE',1245,45,YELLOW)
        title(d,'ENVIRON 1,7 FOIS LE CANADA',1360,48,YELLOW)
        title(d,'MÊME ÉCHELLE - SUPERFICIES TOTALES',1690,29)
    elif kind=='geo-recap':
        title(d,'TU AVAIS TROUVÉ ?',335,65)
        for code,name,rank,y in [('USA','ÉTATS-UNIS',3,475),('CAN','CANADA',2,810),('RUS','RUSSIE',1,1145)]:
            map_shape(d,code,(650,y,330,225));title(d,f'{rank} - {name}',y+80,50,YELLOW)
    elif kind=='factors':
        title(d,'LA PUISSANCE SE COMBINE',350,59)
        for label,y in [('ÉQUIPEMENTS',510),('FINANCES',710),('LOGISTIQUE',910),('GÉOGRAPHIE',1110)]:
            d.rounded_rectangle((75,y,1005,y+130),radius=15,fill='#263241',outline=YELLOW,width=3)
            title(d,label,y+33,57,YELLOW)
        title(d,'GFP 2026 - 145 PAYS',1650,35)
    elif kind=='aircraft':
        title(d,'PARC AÉRIEN MILITAIRE',350,58)
        title(d,'ÉTATS-UNIS',520,65,YELLOW)
        title(d,'13 032',680,170,YELLOW)
        title(d,'AVIONS ET HÉLICOPTÈRES',930,48)
        title(d,'STOCK ESTIMÉ - GLOBAL FIREPOWER 2026',1530,30)
    elif kind=='army-recap':
        title(d,'GLOBAL FIREPOWER 2026',350,55)
        for rank,name,value,y in [(3,'CHINE','EFFECTIFS ACTIFS : N°1',560),(2,'RUSSIE','PARC AÉRIEN : N°2',850),(1,'ÉTATS-UNIS','CLASSEMENT GLOBAL : N°1',1140)]:
            title(d,f'{rank} - {name}',y,74,YELLOW);title(d,value,y+110,32)
        title(d,'QUEL CRITÈRE CHOISIRAIS-TU ?',1550,39)
    elif kind=='tracking':
        title(d,'SUIVIE PAR ÉMETTEUR',360,60)
        # Diagramme original, explicitement marqué : aucune fausse mesure filmée.
        pts=[(130,1010),(265,860),(430,970),(610,760),(815,830),(945,590)]
        d.line(pts,fill=YELLOW,width=9)
        for x,y in pts:d.ellipse((x-14,y-14,x+14,y+14),fill=CREAM)
        x,y=pts[min(5,int(phase*5))];d.ellipse((x-30,y-30,x+30,y+30),outline=YELLOW,width=4)
        title(d,'ENVIRON 160 KM/H',1080,74,YELLOW)
        title(d,'VITESSE PAR RAPPORT AU SOL',1190,34)
        title(d,'SCHÉMA EXPLICATIF - PAS UNE MESURE FILMÉE',1660,25,'#9caabc')
    elif kind=='wind':
        title(d,'LE VENT CHANGE LA MESURE',360,52)
        for y,label,color in [(650,'AIR',CREAM),(980,'SOL',YELLOW)]:
            d.line((120,y,900,y),fill=color,width=12);d.polygon([(900,y),(850,y-30),(850,y+30)],fill=color)
            title(d,label,y-100,55,color)
        title(d,'UNE POINTE - PAS LA CROISIÈRE',1110,45,YELLOW)
        title(d,'SCHÉMA EXPLICATIF',1660,32,'#9caabc')
    elif kind=='dive':
        title(d,'LE PIQUÉ DU FAUCON',355,64)
        p=phase
        # Trajectoire descendante, aucune accélération d’une archive réelle.
        x=200+650*p;y=590+570*p
        d.line((180,550,880,1200),fill='#526278',width=4)
        d.polygon([(x,y+45),(x-45,y-35),(x,y-10),(x+45,y-35)],fill=YELLOW)
        title(d,'ENVIRON 320 KM/H',1040,76,YELLOW)
        title(d,'EN PIQUÉ',1160,52)
        title(d,'SCHÉMA EXPLICATIF - VITESSE NON À L’ÉCHELLE',1660,25,'#9caabc')
    elif kind=='animal-recap':
        title(d,'3 FAÇONS D’ALLER VITE',355,59)
        for name,value,mode,y in [('GUÉPARD','100 KM/H','COURSE',440),('MOLOSSE DU BRÉSIL','160 KM/H','VITESSE AU SOL',710),('FAUCON PÈLERIN','320 KM/H','PIQUÉ',980)]:
            title(d,name,y,45);title(d,'ENVIRON '+value,y+70,64,YELLOW);title(d,mode,y+165,30,'#9caabc')
    else:raise ValueError(kind)
    im.save(path)

def render_graphic(m,index,kind,frames):
    target=m/f'plan-{index:02d}-{kind}-{frames}-v3.mp4'
    if target.exists():return target
    if kind in ('dive','tracking'):
        # Produire un cycle unique de trajectoire, pas une boucle de prise réelle.
        proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','540x960','-framerate','30','-i','pipe:0','-an','-vf','scale=1080:1920','-c:v','libx264','-preset','veryfast','-crf','20','-threads','3','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
        tmp=m/f'graph-{index:02d}.png'
        try:
            for f in range(frames):
                graphic(tmp,kind,f/max(frames-1,1));im=Image.open(tmp).resize((540,960));proc.stdin.write(im.tobytes())
        finally:proc.stdin.close()
        if proc.wait():raise RuntimeError('Animation échouée')
    else:
        picture=m/f'graph-{index:02d}.png';graphic(picture,kind)
        run(['ffmpeg','-v','error','-y','-loop','1','-i',str(picture),'-vf',"scale=2160:3840,zoompan=z='min(zoom+0.00008,1.03)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1",'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','3','-pix_fmt','yuv420p',str(target)])
    return target

def render_clip(m,index,slug,start,frames,cx=.5):
    entry=next(x for x in read(ASSETS/'sources-visuelles.json') if x['slug']==slug)
    src=ASSETS/entry['file']
    target=m/f'plan-{index:02d}-{slug}-{start}-{frames}-{cx}-{src.stat().st_size}.mp4'
    if target.exists():return target
    info=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height','-of','json',str(src)]))
    duration=float(info['format']['duration']);assert start+frames/30<=duration+.05,(slug,start,frames/30,duration)
    vf=f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:max(0\\,min(iw-1080\\,iw*{cx}-540)):0,fps=30,setsar=1"
    run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(src),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','3','-pix_fmt','yuv420p',str(target)])
    return target

def music(w,m,t,number):
    profiles={16:'espace',17:'voitures',18:'bouchons'}
    directory=ROOT/'assets/musique/mixkit';track=next(x for x in read(directory/'sources.json') if x['slug']==profiles[number])
    bed=m/'musique.wav';duration=t['duration']
    run(['ffmpeg','-v','error','-y','-ss',str(track['start']),'-i',str(directory/(track['slug']+'.mp3')),'-af',f'atrim=duration={duration},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2:LRA=9,afade=t=in:d=0.8,afade=t=out:st={duration-2}:d=2','-ar','44100','-ac','2',str(bed)])
    mix_voice(m/'voix.mp3',bed,m/'mix.wav',duration,run)
    return track

def plans(number):
    # Par scène : source ou graphique, début source et durée limite. Tous les
    # intervalles d'une même source restent distincts ; aucun bouclage.
    if number==16:return [
        [('china-parade',25,3,.5),('china-parade',29,3,.42),('china-parade',34,5,.5)],
        [('china-parade',40,3,.6),('china-parade',46,8,.5)],
        [('graphic:factors',0,20,.5)],
        [('russia-air',5,3,.5),('russia-air',15,3,.5),('russia-air',25,4,.5)],
        [('russia-air',35,3,.5),('russia-air',45,3,.5),('graphic:factors',0,8,.5)],
        [('usa-f16',14,3,.6),('usa-f16',18,3,.5),('graphic:aircraft',0,7,.5)],
        [('usa-f16',28,3,.5),('usa-f16',34,3,.5),('graphic:army-recap',0,8,.5)],
        [('graphic:army-recap',0,20,.5)]]
    if number==17:return [
        [('cheetah',0.8,2.5,.5),('cheetah',3.4,2.5,.5),('cheetah',6,3,.55),('cheetah',34,2,.5)],
        [('cheetah',36,3,.5),('cheetah',39,3,.5),('cheetah',42,4,.5)],
        [('bats',0,3,.5),('bats',5,3,.5),('bats',10,5,.5)],
        [('graphic:tracking',0,20,.5)],
        [('graphic:wind',0,20,.5)],
        [('falcon',0,3,.5),('graphic:dive',0,15,.5)],
        [('graphic:dive',0,20,.5)],
        [('graphic:animal-recap',0,20,.5)]]
    return [
        [('graphic:USA',0,20,.5)],
        [('alaska',0,3,.5),('alaska',6,3,.5),('alaska',12,6,.5)],
        [('graphic:CAN',0,20,.5)],
        [('canada',0,3,.5),('canada',6,3,.5),('canada',12,8,.5)],
        [('graphic:RUS',0,20,.5)],
        [('graphic:compare',0,20,.5)],
        [('graphic:geo-recap',0,20,.5)],
        [('graphic:geo-recap',0,20,.5)]]

def produce(w):
    if read(w/'histoire.json').get('revision','').startswith('spectaculaire'):
        from revision_spectaculaire import render
        return render(w)
    d=read(w/'histoire.json');number=d['numero'];m=w/'_montage';t=read(m/'timings-oraux.json')
    assert t['duration']>60
    display=copy.deepcopy(t);display['words']=numeric_words(t['words']);save(m/'timings.json',display)
    starts=[sum(t['scene_durations'][:i]) for i in range(len(d['scenes']))]
    item=dict(series=d['serie'],title={16:['TOP 3','DES ARMÉES','GFP 2026'],17:['3 ANIMAUX','AUX VITESSES','FOLLES'],18:['TOP 3','DES PLUS','GRANDS PAYS']}[number],
              credits={16:'GFP 2026 - CNS - Ministère russe de la Défense - USAF',17:'Guinness - Max Planck - Images Commons',18:'ONU - Statistique Canada - Natural Earth'}[number],facts=[])
    for i,s in enumerate(d['scenes']):
        if i==0 or s['rang']!=d['scenes'][i-1]['rang']:
            if s['rang']:
                a=max(4,starts[i]);b=starts[i]+t['scene_durations'][i]
                label=s['texte_ecran']
                # Le bandeau doit rester court : les valeurs sont dans les sous-titres.
                label=' - '.join(label.split(' - ')[:2])
                item['facts'].append((a,b,label))
    layers(m,item)
    cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
    cfg['render'].update(subtitle_size=83,words_per_caption=5,subtitle_wrap=20)
    subs(m,display,item,cfg)
    # Déplacer les faits sous le header et garder les sous-titres plus bas.
    p=m/'sous-titres-reference.ass';s=p.read_text(encoding='utf-8')
    s=s.replace('Style: Fact,Poppins ExtraBold,53','Style: Fact,Poppins ExtraBold,47')
    if number==16:
        s+=f'Dialogue: 2,0:00:00.00,{assemble._ass_time(t["duration"])},Fact,,0,0,0,,{{\\an8\\pos(540,310)\\fs27}}ARCHIVES - ILLUSTRATIONS DU CLASSEMENT\n'
    p.write_text(s,encoding='utf-8');shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
    edits=[];files=[];cursor=0;used={}
    for scene,group in enumerate(plans(number)):
        end=round(sum(t['scene_durations'][:scene+1])*30)
        for source,start,limit,cx in group:
            if cursor>=end:break
            frames=min(round(limit*30),end-cursor)
            if source.startswith('graphic:'):path=render_graphic(m,len(files),source.split(':')[1],frames)
            else:
                interval=(start,start+frames/30)
                assert not any(max(start,a)<min(interval[1],b)-.001 for a,b in used.get(source,[])),f'Répétition {source}'
                used.setdefault(source,[]).append(interval)
                path=render_clip(m,len(files),source,start,frames,cx)
            edits.append(dict(scene=scene,source=source,start_source=start,start=cursor/30,duration=frames/30,crop_x=cx))
            uniform=m/('uniform-'+path.name)
            if not uniform.exists():
                run(['ffmpeg','-v','error','-y','-i',str(path),'-c','copy','-bsf:v',
                     'h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1',
                     '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(uniform)])
            files.append(uniform.name);cursor+=frames
        assert cursor==end,f'Plans insuffisants scène {scene+1}: {cursor/30} / {end/30}'
        print(w.name,'scène',scene+1,'montée',flush=True)
    save(m/'montage.json',edits)
    # Les légendes des graphiques ne doivent jamais partager la zone des sous-titres.
    caption_lines=[]
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.startswith('Dialogue:'):
            cells=line.split(',',9)
            if cells[3]=='Default':
                h,minute,second=cells[1].split(':');at=int(h)*3600+int(minute)*60+float(second)
                edit=next((e for e in edits if e['start']<=at<e['start']+e['duration']),None)
                if edit and edit['source'].startswith('graphic:'):
                    kind=edit['source'].split(':')[1]
                    y=1480 if kind in ('geo-recap','compare') else 1330 if kind in ('factors','army-recap','tracking','wind','dive') else 1190
                    cells[9]=f'{{\\an8\\pos(540,{y})}}'+cells[9];line=','.join(cells)
        caption_lines.append(line)
    p.write_text('\n'.join(caption_lines)+'\n',encoding='utf-8')
    (m/'concat.txt').write_text(''.join(f"file '{f}'\n" for f in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','base.mp4'],m)
    track=music(w,m,t,number)
    graph=('[0:v]fps=30,setpts=PTS-STARTPTS,ass=sous-titres-reference.ass:fontsdir=.[cap];'
           '[3:v]format=rgba,fade=t=out:st=3.8:d=0.2:alpha=1[hook];'
           '[cap][hook]overlay=0:0:enable=lt(t\\,4):shortest=1[h];'
           '[h][2:v]overlay=0:0:shortest=1[v]')
    run(['ffmpeg','-v','error','-y','-i','base.mp4','-i','mix.wav','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png',
         '-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(w/'final.mp4')],m)
    actual=validate_duration(w/'final.mp4');run(['ffmpeg','-v','error','-i',str(w/'final.mp4'),'-f','null','-'])
    assert abs(actual-t['duration'])<.2
    d.update(statut='Vidéo rendue - contrôle visuel en cours',musique=track)
    save(w/'histoire.json',d);save(m/'controle.json',dict(duration_mp4=actual,voice_model=t['model'],voix='Hugo ElevenLabs',decodage_integral=True,plans_sans_boucle=True,habillage='HPB actuel',verification_visuelle='en cours'))
    print(w.name,'FINAL',actual,flush=True)
    from comparer_lot_16_18 import compare
    compare(w)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--numero',type=int);args=parser.parse_args()
    for w in FOLDERS:
        if args.numero is None or int(w.name[:2])==args.numero:produce(w)
