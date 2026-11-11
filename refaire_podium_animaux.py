"""Podium de pointes en piqué : gerfaut, aigle royal, pèlerin ; sources et conditions documentées."""
import copy,json,math,shutil,hashlib
from pathlib import Path
import yaml
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save,speech
from revision_hpb_v10 import NUMBERS,display_words
from habillage_reference import layers,subs
from monter_lot_16_18 import music
from narrateur.assemble import _ass_time
from comparer_lot_16_18 import compare
from rendre_funfacts_visibles import make_card,FACTS

w=next((ROOT/'out').glob('17-*'));stage=w/'_montage/podium-mondial-v6';stage.mkdir(exist_ok=True);m=stage/'_montage';m.mkdir(exist_ok=True);assets=ROOT/'assets/lot-16-18/nouveaux-rapaces'
texts=[
'Top trois des animaux les plus rapides du monde.',
'Numéro trois : le faucon gerfaut. En piqué, il a été mesuré à près de deux cent neuf kilomètres heure. Une voiture lancée sur l’autoroute resterait derrière !',
'Et voici son détail fou : c’est le plus grand faucon du monde. Son envergure dépasse un mètre. Un véritable géant parmi les faucons, qui vit dans les grands espaces de l’Arctique.',
'Numéro deux : l’aigle royal. Lorsqu’il plonge depuis une grande hauteur, il peut approcher trois cent vingt kilomètres heure. Imagine ce rapace immense lancé dans une descente pareille.',
'Son envergure peut dépasser deux mètres. Il repère sa proie, puis utilise ses puissantes serres pour la saisir. Mais attends le premier : sa pointe expérimentale va encore beaucoup plus loin.',
'Numéro un : le faucon pèlerin. Un record expérimental rapporte environ trois cent quatre-vingt-neuf kilomètres heure en piqué. Plus de cent mètres parcourus en une seconde !',
'Ce chiffre vient d’un essai mené en altitude avec des appareils de mesure. Les ailes repliées réduisent la résistance de l’air. C’est une pointe en descente, pas sa vitesse de vol habituelle.',
'Trois rapaces sur le podium. Tu avais pensé à eux, ou au guépard ? Donne ton pronostic en commentaire. Pas banal, hein ?'
]
if not (stage/'histoire.json').exists():
    d=copy.deepcopy(read(w/'histoire.json'));d.update(titre='TOP 3 ANIMAUX LES PLUS RAPIDES DU MONDE - 2026',titre_fixe='TOP 3 ANIMAUX LES PLUS RAPIDES DU MONDE - 2026',hook=texts[0],revision='podium-mondial-v6',critere='Pointes maximales publiées en piqué : gerfaut ~209, aigle royal ~320, pèlerin ~389 km/h (ce dernier en essai expérimental). Édition vérifiée en 2026 ; mesures historiques.',scenes=[dict(narration=s,narration_voix=s,rang=[None,3,3,2,2,1,1,None][i]) for i,s in enumerate(texts)])
    d['script']=' '.join(texts);d['fun_fact']=dict(texte='Le gerfaut est le plus grand faucon du monde.',source='https://www.adfg.alaska.gov/index.cfm?adfg=birdviewing.birdersbirds&species=gyrfalcon');save(stage/'histoire.json',d)
speech(stage)
d=read(stage/'histoire.json');t=read(m/'timings-oraux.json')
NUMBERS.update({'deux cent neuf':'209','trois cent vingt':'320','trois cent quatre-vingt-neuf':'389','cent mètres':'100 mètres','un mètre':'1 mètre'})
t=copy.deepcopy(t);t['words']=display_words(t['words']);save(m/'timings.json',t)
if t['duration']<=60:raise ValueError('Durée utile insuffisante')
starts=[sum(t['scene_durations'][:i]) for i in range(len(texts))];ends=[sum(t['scene_durations'][:i+1]) for i in range(len(texts))]
item=dict(title=['TOP 3','ANIMAUX LES PLUS','RAPIDES DU MONDE','2026'],series='TOP 3 - ANIMAUX',credits='Guinness - Cornell - Photos et archives',facts=[])
layers(m,item);cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=83,words_per_caption=5,subtitle_wrap=20);subs(m,t,item,cfg)
shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
ass=m/'sous-titres-reference.ass';s=ass.read_text(encoding='utf-8')
adjusted=[]
for line in s.splitlines():
    if line.startswith('Dialogue:'):
        p=line.split(',',9)
        if p[3]=='Default':
            hh,mm,ss=p[1].split(':');at=int(hh)*3600+int(mm)*60+float(ss)
            if starts[1]<=at<starts[3]:p[9]=r'{\an8\pos(540,1450)}'+p[9];line=','.join(p)
    adjusted.append(line)
s='\n'.join(adjusted)+'\n'
for i,label in [(1,'3 - FAUCON GERFAUT\\NENVIRON 209 KM/H - EN PIQUÉ'),(3,'2 - AIGLE ROYAL\\NENVIRON 320 KM/H - EN PIQUÉ'),(5,'1 - FAUCON PÈLERIN\\N389 KM/H - ESSAI EN PIQUÉ')]:
    s+=f'Dialogue: 1,{_ass_time(starts[i])},{_ass_time(min(ends[i],starts[i]+6))},Fact,,0,0,0,,{{\\an8\\pos(540,250)\\fs50}}{label}\n'
ass.write_text(s,encoding='utf-8')

# Aucun hybride, pygargue ou séquence présentée comme la mesure du record.
# La photographie USFWS montre bien le pèlerin ailes repliées, en piqué.
plans=[
 [('photo',ROOT/'assets/lot-16-18/photos-v2/earth-hero.jpg',0,30)],
 [('video',assets/'gyrfalcon-olivier.mp4',.5,3),('photo',assets/'gyrfalcon-flight.jpg',0,30)],
 [('photo',assets/'gyrfalcon-flight.jpg',0,4),('video',assets/'gyrfalcon-olivier.mp4',6,3.5),('photo',assets/'gyrfalcon-flight.jpg',0,30)],
 [('video',assets/'golden-rrp.mp4',1,3),('photo',assets/'golden-dive-dvids.jpg',0,30)],
 [('photo',assets/'golden-dive-dvids.jpg',0,7.5),('video',assets/'golden-rrp.mp4',61,4),('photo',assets/'golden-dive-dvids.jpg',0,30)],
 [('photo',assets/'peregrine-stoop.jpg',0,30)],
 [('video',assets/'peregrine-ryan.mp4',42,4),('photo',assets/'peregrine-stoop.jpg',0,30)],
 [('photo',assets/'gyrfalcon-flight.jpg',0,3),('photo',assets/'golden-dive-dvids.jpg',0,3),('photo',assets/'peregrine-stoop.jpg',0,30)],
]
# Accroche générique : aucune espèce du podium dévoilée avant le n°3.
if not plans[0][0][1].exists():plans[0]=[('video',ROOT/'assets/sources-reelles/terre.mp4',0,30)]
files=[];edits=[];cursor=0
for scene,group in enumerate(plans):
    stop=round(ends[scene]*30)
    for kind,source,start,limit in group:
        if cursor>=stop:break
        frames=min(round(limit*30),stop-cursor);duration=frames/30
        key=hashlib.sha1(f'{kind}/{source}/{start}/{frames}/action-v3'.encode()).hexdigest()[:8];target=m/f'plan-{len(files):02d}-{key}.mp4'
        if not source.exists():raise FileNotFoundError(source)
        if not target.exists():
            if kind=='photo':
                # Prolonger uniquement le ciel ou l'eau : aucun second oiseau fantôme dans le fond.
                plate=m/('photo-portrait-v3-'+source.stem+'.png')
                if not plate.exists():
                    if source.name=='gyrfalcon-flight.jpg':
                        imagegraph="[0:v]split[a][b];[a]crop=iw:trunc(ih*0.12/2)*2:0:0,scale=1080:1920,gblur=sigma=12[bg];[b]scale=1700:-2,crop=1080:ih:(iw-ow)/2:0,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/100,(H-Y-1)/100))'[fg];[bg][fg]overlay=0:(H-h)/2[v]"
                    elif source.name=='golden-dive-dvids.jpg':
                        imagegraph="[0:v]split[a][b];[a]crop=iw:trunc(ih*0.18/2)*2:0:trunc(ih*0.82/2)*2,scale=1080:1920,gblur=sigma=16[bg];[b]scale=1080:-2,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/80,(H-Y-1)/80))'[fg];[bg][fg]overlay=0:(H-h)/2[v]"
                    else:imagegraph='[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v]'
                    run(['ffmpeg','-v','error','-y','-i',str(source),'-filter_complex_threads','1','-filter_complex',imagegraph,'-map','[v]','-frames:v','1',str(plate)])
                z=f'1.025+0.035*on/{max(1,frames-1)}' if len(files)%2==0 else f'1.06-0.035*on/{max(1,frames-1)}'
                graph=f"[0:v]zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1[v]"
                inputs=['-loop','1','-i',str(plate)]
            else:
                graph='[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v]';inputs=['-ss',str(start),'-i',str(source)]
            run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v',str(frames),'-r','30','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2',str(target)])
        files.append(target.name);edits.append(dict(scene=scene,source=str(source.relative_to(ROOT)),source_start=start,start=cursor/30,duration=duration));cursor+=frames
    assert cursor==stop
(m/'concat.txt').write_text(''.join(f"file '{name}'\n" for name in files),encoding='utf-8');run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','base.mp4'],m);save(m/'montage.json',edits);music(w,m,t,17)
d['fun_fact_affichage']=dict(debut=starts[2],fin=min(ends[2],starts[2]+7),texte=['LE PLUS GRAND FAUCON','DU MONDE'],mention='FUN FACT');save(stage/'histoire.json',d)
archive=w/'_montage/avant-podium-mondial';archive.mkdir(exist_ok=True)
for name in ['histoire.json','final.mp4','comparaison.mp4','script.txt']:
    if (w/name).exists() and not (archive/name).exists():shutil.copy2(w/name,archive/name)
FACTS[17]=(d['fun_fact_affichage']['debut'],d['fun_fact_affichage']['fin'],d['fun_fact_affichage']['texte']);make_card(17);shutil.copy2(w/'_montage/funfact-visible.png',m/'funfact-visible.png')
fact=d['fun_fact_affichage'];graph=('[0:v]fps=30,ass=sous-titres-reference.ass:fontsdir=.[s];[s][2:v]overlay=0:0:enable=lt(t\\,1.5):shortest=1[h];[h][3:v]overlay=0:0:shortest=1[q];'+f'[q][4:v]overlay=0:0:enable=between(t\\,{fact["debut"]}\\,{fact["fin"]}):shortest=1[v]')
run(['ffmpeg','-v','error','-y','-i','base.mp4','-i','mix.wav','-loop','1','-framerate','30','-i','titre-hook-reference.png','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','funfact-visible.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(stage/'final.mp4')],m)
run(['ffmpeg','-v','error','-i',str(stage/'final.mp4'),'-f','null','-'])
for name in ['final.mp4','histoire.json']:shutil.copy2(stage/name,w/name)
for name in ['timings.json','timings-oraux.json','voix.mp3','montage.json','sous-titres-reference.ass','titre-hook-reference.png','titre-hook-layout.json']:shutil.copy2(m/name,w/'_montage'/name)
(w/'script.txt').write_text('\n\n'.join(texts),encoding='utf-8');compare(w)
save(w/'_montage/controle-funfact-visible.json',dict(numero=17,debut=fact['debut'],fin=fact['fin'],texte=fact['texte'],sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest(),comparaison_a_jour=True))
print('17 : nouveau podium rendu',t['duration'],flush=True)
