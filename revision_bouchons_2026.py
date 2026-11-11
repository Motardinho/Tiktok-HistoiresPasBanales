"""Édition 2026, dernières données INRIX 2025, départ rapide et image fournie par Marc."""
import copy,hashlib,shutil
import yaml
from montage_reel import ROOT,SOURCES,run
from produire_lot_16_18 import read,save
from revision_hpb_v10 import NUMBERS,display_words
from revision_hpb_v9 import captions
from revision_hpb_v12 import music
from habillage_reference import layers
from narrateur.validation import validate_duration
from comparer_lot_16_18 import compare

w=next((ROOT/'out').glob('15-*'));stage=w/'_montage/revision-donnees-2025-rapide-v15';m=stage/'_montage';d=read(stage/'histoire.json');t=read(m/'timings-oraux.json')
NUMBERS.update({'quatre-vingt-dix':'90','quatre-vingt-onze':'91','mille huit cent soixante-huit':'1868','deux mille vingt-cinq':'2025','onze':'11','douze':'12'})
t=copy.deepcopy(t);t['words']=display_words(t['words']);save(m/'timings.json',t)
starts=[sum(t['scene_durations'][:i]) for i in range(len(d['scenes']))]
oldm=w/'_montage/revision-funfact-v13/_montage';old=read(oldm/'timings.json');oldbase=oldm/'base.mp4'
ends=[starts[1],starts[3],starts[5],t['duration']];cursor=0;files=[];edits=[]
for i,end in enumerate(ends):
    frames=round(end*30)-cursor;f=m/f'chapitre-{i}.mp4'
    if i==0:
        source=SOURCES/'bouchons-hero-marc-nuit.png';offset=0
        vf="scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.02+0.0007*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1"
        input_args=['-loop','1','-i',str(source)]
    else:
        source=SOURCES/'londres.mp4' if i==2 else oldbase
        offset=2 if i==2 else 0 if i==1 else sum(old['scene_durations'][:4])
        vf='fps=30,setpts=PTS-STARTPTS'
        if i==2:vf+=',scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1'
        vf+=',tpad=stop_mode=clone:stop_duration=2'
        input_args=['-ss',str(offset),'-i',str(source)]
    run(['ffmpeg','-v','error','-y',*input_args,'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(f)])
    files.append(f.name);edits.append(dict(rang=None if i==0 else 4-i,start=cursor/30,duration=frames/30,source=str(source.relative_to(ROOT)),start_source=offset));cursor+=frames
(m/'concat.txt').write_text(''.join(f"file '{x}'\n" for x in files),encoding='utf-8')
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','base.mp4'],m);save(m/'montage.json',edits)
item=dict(title=['TOP 3','JUSQU’À 102 H','DANS LES BOUCHONS','2026'],series='3 VILLES - BOUCHONS',credits='Données INRIX 2025 - Images d’illustration',facts=[(starts[1],starts[3],'3 - PARIS - 2025\\N90 H DANS LES BOUCHONS'),(starts[3],starts[5],'2 - LONDRES - 2025\\N91 H DANS LES BOUCHONS'),(starts[5],t['duration'],'1 - NEW YORK - 2025\\N102 H DANS LES BOUCHONS')])
layers(m,item);cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=88,words_per_caption=5,subtitle_wrap=19)
captions(m,t,item,cfg,cta_start=starts[7]);shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
from narrateur.assemble import _ass_time
a=next(x['start'] for x in t['words'] if x['w'].strip('.,:;!?')=='1868');p=m/'sous-titres-reference.ass';s=p.read_text(encoding='utf-8')
s+=f'Dialogue: 1,{_ass_time(a)},{_ass_time(min(starts[5],a+4))},Fact,,0,0,0,,{{\\an8\\pos(540,440)\\fs46}}PREMIER FEU AU GAZ - 1868\n';p.write_text(s,encoding='utf-8')
shutil.copy2(m/'voix.mp3',m/'voix-hpb-v11.mp3');track=music('villes-plus-lentes-tomtom-2024',m,t['duration'])
graph=('[0:v]fps=30,setpts=PTS-STARTPTS,ass=sous-titres-reference.ass:fontsdir=.[cap];[3:v]format=rgba,fade=t=out:st=1.3:d=0.2:alpha=1[hook];[cap][hook]overlay=0:0:enable=lt(t\\,1.5):shortest=1[h];[h][2:v]overlay=0:0:shortest=1[v]')
run(['ffmpeg','-v','error','-y','-i','base.mp4','-i','mix-hpb-v12.wav','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(stage/'final.mp4')],m)
actual=validate_duration(stage/'final.mp4');assert abs(actual-t['duration'])<.1;run(['ffmpeg','-v','error','-i',str(stage/'final.mp4'),'-f','null','-'])
archive=w/'_montage/avant-donnees-2025';archive.mkdir(exist_ok=True)
for name in ['final.mp4','comparaison.mp4','histoire.json','publication.txt','verification.md']:
    if not (archive/name).exists():shutil.copy2(w/name,archive/name)
d.update(statut='Édition 2026 rendue - dernières données INRIX 2025',edition_video=2026,annee_donnees=2025,musique=track,critere='Comparaison de Paris, Londres et New York selon les heures annuelles perdues par conducteur, INRIX 2025. Pas le podium mondial.')
save(stage/'histoire.json',d)
for name in ['final.mp4','histoire.json','script.txt']:shutil.copy2(stage/name,w/name)
for name in ['timings.json','timings-oraux.json','voix.mp3','montage.json']:shutil.copy2(m/name,w/'_montage'/name)
compare(w)
save(w/'_montage/controle.json',dict(duration_mp4=actual,decodage_integral=True,annee_video=2026,annee_donnees=2025,source_donnees='https://inrix.com/scorecard/',classement='Paris 90 H, Londres 91 H, New York 102 H ; sélection de trois villes',source_hero='Image fournie par Marc, illustration générique sans attribution de ville',entree_3_secondes=starts[1],sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest(),revision=d['revision']))
(w/'voix-texte.txt').write_text('\n\n'.join(x['narration_voix'] for x in d['scenes']),encoding='utf-8')
(w/'verification.md').write_text('# Édition vidéo 2026 - données INRIX 2025\n\nDernière édition disponible vérifiée le 8 novembre 2026. Paris : 90 H ; Londres : 91 H ; New York : 102 H. Classement interne à ces trois villes, pas podium mondial.\n\nSources : https://inrix.com/scorecard/ et https://www.sipotra.it/wp-content/uploads/2026/04/2025-INRIX-Global-Traffic-Scorecard.pdf (rapport original INRIX, pages 10-12).\n\nFun fact : premier feu au gaz à Londres en 1868 puis retrait après une explosion. https://www.ciht.org.uk/news/traffic-light-anniversary-reached-in-london/\n\nAccroche : photo fournie par Marc utilisée comme illustration générique, avant le nom des villes. Paris et New York : séquences validées ; Londres : Pexels George Morina. Les images ne sont pas présentées comme des prises des mesures 2025.\n',encoding='utf-8')
(w/'publication.txt').write_text(d['legende']+'\n\n'+' '.join(d['hashtags'])+'\n\nÉdition vidéo 2026 - données INRIX 2025. Activer le label IA pour la voix. Sources : verification.md ; attributions : CREDITS.md.\n',encoding='utf-8')
run(['ffmpeg','-v','error','-y','-ss','0.5','-i',str(w/'final.mp4'),'-frames:v','1',str(w/'apercu.png')])
print('15 ÉDITION 2026 ET COMPARAISON',actual,flush=True)
