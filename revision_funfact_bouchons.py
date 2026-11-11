"""Complément du fun fact Londres ; conserve les images Paris/New York et la musique validée."""
import copy,hashlib,json,re,shutil
import yaml
from montage_reel import ROOT,SOURCES,run
from produire_lot_16_18 import read,save
from revision_hpb_v10 import NUMBERS,display_words
from revision_hpb_v9 import captions
from revision_hpb_v12 import music
from habillage_reference import layers
from narrateur.validation import validate_duration
from comparer_lot_16_18 import compare

w=ROOT/'out/15-villes-plus-lentes-tomtom-2024'
stage=w/'_montage/revision-funfact-v13';m=stage/'_montage';d=read(stage/'histoire.json');t=read(m/'timings-oraux.json')
NUMBERS.update({'mille huit cent soixante-huit':'1868','deux mille vingt-quatre':'2024','kilomètres heure':'KM/H'})
t=copy.deepcopy(t);t['words']=display_words(t['words']);save(m/'timings.json',t)
starts=[sum(t['scene_durations'][:i]) for i in range(len(d['scenes']))]
assert t['duration']>60
old=read(w/'_montage/timings.json');oldbase=w/'_montage/base-hpb-v11.mp4'
ends=[starts[2],starts[4],t['duration']];cursor=0;files=[];edits=[]
for i,(source,offset,end) in enumerate([(oldbase,0,ends[0]),(SOURCES/'londres.mp4',2,ends[1]),(oldbase,sum(old['scene_durations'][:4]),ends[2])]):
    frames=round(end*30)-cursor;f=m/f'pays-{i}.mp4'
    vf='fps=30,setpts=PTS-STARTPTS'
    if i==1:vf+=',scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1'
    run(['ffmpeg','-v','error','-y','-ss',str(offset),'-i',str(source),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(f)])
    files.append(f.name);edits.append(dict(rang=3-i,start=cursor/30,duration=frames/30,source=str(source.relative_to(ROOT)),start_source=offset));cursor+=frames
(m/'concat.txt').write_text(''.join(f"file '{f}'\\n" for f in files),encoding='utf-8')
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','base.mp4'],m);save(m/'montage.json',edits)
item=dict(title=['TOP 3','JUSQU’À 102 H','DANS LES BOUCHONS'],series='3 VILLES - BOUCHONS',credits='Pexels - INRIX 2024',facts=[(0,4,'3 - PARIS'),(4,starts[2],'3 - PARIS - 2024\\N97 H DANS LES BOUCHONS'),(starts[2],starts[4],'2 - LONDRES - 2024\\N101 H DANS LES BOUCHONS'),(starts[4],t['duration'],'1 - NEW YORK - 2024\\N102 H DANS LES BOUCHONS')])
layers(m,item);cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=88,words_per_caption=5,subtitle_wrap=19)
captions(m,t,item,cfg,cta_start=starts[6]);shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
# Le récit historique reste sur des images actuelles de Londres, sans les dater de 1868.
a=next(x['start'] for x in t['words'] if x['w'].strip('.,:;!?')=='1868');p=m/'sous-titres-reference.ass';s=p.read_text(encoding='utf-8');from narrateur.assemble import _ass_time
s+=f'Dialogue: 1,{_ass_time(a)},{_ass_time(min(starts[4],a+4))},Fact,,0,0,0,,{{\\an8\\pos(540,400)\\fs38}}LE PREMIER FEU AU GAZ - 1868\\n';p.write_text(s,encoding='utf-8')
shutil.copy2(m/'voix.mp3',m/'voix-hpb-v11.mp3');track=music('villes-plus-lentes-tomtom-2024',m,t['duration'])
graph=('[0:v]fps=30,setpts=PTS-STARTPTS,ass=sous-titres-reference.ass:fontsdir=.[cap];[3:v]format=rgba,fade=t=out:st=3.8:d=0.2:alpha=1[hook];[cap][hook]overlay=0:0:enable=lt(t\\,4):shortest=1[h];[h][2:v]overlay=0:0:shortest=1[v]')
run(['ffmpeg','-v','error','-y','-i','base.mp4','-i','mix-hpb-v12.wav','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(stage/'final.mp4')],m)
actual=validate_duration(stage/'final.mp4');assert abs(actual-t['duration'])<.1
run(['ffmpeg','-v','error','-i',str(stage/'final.mp4'),'-f','null','-'])
archive=w/'_montage/avant-funfact';archive.mkdir(exist_ok=True)
for name in ['final.mp4','comparaison.mp4','histoire.json','publication.txt']:
    if not (archive/name).exists():shutil.copy2(w/name,archive/name)
d.update(statut='Fun fact ajouté - rendu vérifié',musique=track);save(stage/'histoire.json',d)
for name in ['final.mp4','histoire.json','script.txt']:shutil.copy2(stage/name,w/name)
for name in ['timings.json','timings-oraux.json','voix.mp3','montage.json']:shutil.copy2(m/name,w/'_montage'/name)
compare(w)
save(w/'_montage/controle.json',dict(duration_mp4=actual,decodage_integral=True,funfact='Premier feu de circulation installé à Londres en 1868, au gaz, puis retiré après une explosion',source_funfact='https://www.ciht.org.uk/news/traffic-light-anniversary-reached-in-london/',sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest(),deux_points_lies=True,revision='funfact-v13',verification_visuelle='en cours'))
(w/'voix-texte.txt').write_text('\\n\\n'.join(s['narration_voix'] for s in d['scenes']),encoding='utf-8')
p=w/'verification.md';oldtext=p.read_text(encoding='utf-8');addition='\\n\\nFun fact - Londres : premier feu de circulation installé en décembre 1868, alimenté au gaz et retiré environ un mois plus tard après une explosion. Source CIHT, citant Transport for London : https://www.ciht.org.uk/news/traffic-light-anniversary-reached-in-london/ . Les images sont des vues actuelles de Londres, pas des archives de 1868.\\n';p.write_text(oldtext+addition,encoding='utf-8')
(w/'CREDITS.md').write_text((ROOT/'assets/sources-reelles/CREDITS.md').read_text(encoding='utf-8')+'\\n\\nMontage actuel : Paris-soir et New-York-bouchons (versions recadrées existantes), Londres (nouvel extrait continu). Aucun visuel historique présenté comme une archive de 1868.\\n\\nMusique : '+track['title']+' - '+track['artist']+' - '+track['page']+' - '+track['license_url']+'\\nVoix : Hugo ElevenLabs '+t['model']+' .\\n',encoding='utf-8')
run(['ffmpeg','-v','error','-y','-ss','1','-i',str(w/'final.mp4'),'-frames:v','1',str(w/'apercu.png')])
print('15 FUN FACT ET COMPARAISON',actual,flush=True)
