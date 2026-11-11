"""Révision demandée : photos et scènes plein écran, aucun panneau scolaire."""
import argparse
import copy
import hashlib
import html
import re
import shutil
from pathlib import Path

import yaml
from montage_reel import ROOT,run
from produire_lot_16_18 import FOLDERS,read,save,speech
from monter_lot_16_18 import numeric_words,render_clip,music
from habillage_reference import layers,subs
from narrateur import assemble
from narrateur.validation import validate_duration
from comparer_lot_16_18 import compare

PHOTOS=ROOT/'assets/lot-16-18/photos-v2'
INTROS={16:'Trois armées gigantesques. Et la première ne joue pas dans la même dimension.',17:'Trois animaux aux vitesses folles. Tu les aurais classés dans le bon ordre ?',18:'Trois pays immenses. Le premier est encore beaucoup plus grand que tu l’imagines.'}
TEXTS={
16:[
 (3,'Numéro 3 : la Chine. Plus de deux millions de militaires actifs. Et trois cent trente-six milliards de dollars de dépenses militaires en deux mille vingt-cinq. Une armée qui se transforme à toute vitesse.'),
 (3,'Sa montée en puissance se voit aussi en mer. Porte-avions, chasseurs embarqués : Pékin voit grand. Et elle possède aussi un arsenal nucléaire estimé à six cent vingt ogives. Derrière les défilés, il y a une puissance bien réelle.'),
 (2,'Numéro 2 : la Russie. Son atout le plus redoutable ne se voit pas dans un simple défilé. Son stock nucléaire militaire est estimé à quatre mille quatre cents ogives. Le plus important au monde.'),
 (2,'Ses dépenses militaires atteignaient cent quatre-vingt-dix milliards de dollars en deux mille vingt-cinq. Derrière les missiles, il y a aussi les blindés, les hélicoptères et les avions de combat. Un arsenal massif.'),
 (1,'Numéro 1 : les États-Unis. En deux mille vingt-cinq, leurs dépenses militaires atteignaient neuf cent cinquante-quatre milliards de dollars. À eux seuls, environ un tiers du total mondial.'),
 (1,'Et ces porte-avions sont de vraies villes flottantes. Sur le Ronald Reagan, il faut nourrir des milliers de marins chaque jour. Oui, ce géant possède même sa propre boulangerie à bord !'),
 (1,'Et le nucléaire compte aussi : leur stock militaire est estimé à trois mille sept cents ogives. Ajoute le ravitaillement en vol et les transports : ils peuvent soutenir des opérations à grande distance.'),
 (None,'Et toi, quelle armée pensais-tu voir à la première place ? Dis-le en commentaire. Pas banal, hein ?'),
],
17:[
 (3,'Numéro 3 de ces vitesses animales : le guépard. Autour de 100 kilomètres heure en pointe. Imagine une voiture lancée sur la route, mais avec des pattes.'),
 (3,'Ce félin est le mammifère terrestre le plus rapide sur courte distance. Sa force, c’est le sprint : une course fulgurante, pas des kilomètres à cette allure.'),
 (2,'Numéro 2 de notre sélection : le molosse du Brésil. Une chauve-souris dont des pointes autour de 160 kilomètres heure ont été mesurées par rapport au sol.'),
 (2,'Les femelles étudiées ne pesaient que 11 à 12 grammes. Oui, un animal aussi léger, lancé à cette vitesse. Le vent peut influencer cette mesure, mais le chiffre reste saisissant.'),
 (1,'Numéro 1 de cette sélection : le faucon pèlerin. En piqué, il peut atteindre environ 320 kilomètres heure. Là, on passe encore dans une autre dimension.'),
 (1,'Pour atteindre cette pointe, il plonge vers sa proie. C’est bien une vitesse en descente. Il ne traverse pas le ciel à cette allure en permanence.'),
 (1,'Un guépard qui sprinte, une chauve-souris minuscule, puis ce rapace qui plonge. Trois animaux, trois performances. Le plus impressionnant n’est peut-être pas celui que tu imaginais.'),
 (None,'Lequel t’a le plus surpris ? Le guépard, la chauve-souris ou le faucon ? Donne ton choix en commentaire. Pas banal, hein ?'),
],
18:[
 (3,'Numéro 3 des plus grands pays du monde : les États-Unis. Environ 9,8 millions de kilomètres carrés, en comptant les terres et les eaux.'),
 (3,'Des grandes villes aux montagnes de l’Alaska, le changement de décor est immense. L’Alaska fait bien partie du total. Et pourtant, les États-Unis ne sont que troisièmes.'),
 (2,'Numéro 2 : le Canada. Presque 10 millions de kilomètres carrés. Imagine les montagnes, les forêts et ces lacs qui s’étendent dans des paysages gigantesques.'),
 (2,'Et le Canada cache un autre record : il possède le plus long littoral du monde. Ses côtes touchent trois océans : l’Atlantique, le Pacifique et l’Arctique.'),
 (1,'Numéro 1 : la Russie. Environ 17,1 millions de kilomètres carrés. On ne monte plus d’un petit cran : on change complètement de dimension.'),
 (1,'De l’Europe jusqu’au nord de l’Asie, son territoire s’étire sur une étendue immense. Même le Canada, pourtant gigantesque, reste très loin derrière en superficie totale.'),
 (1,'Le chiffre donne le vertige : la Russie représente environ 1,7 fois la superficie du Canada. Un seul pays, et une place énorme sur la planète.'),
 (None,'États-Unis, Canada, Russie. Tu avais trouvé les 3 dans le bon ordre ? Donne ton score en commentaire. Pas banal, hein ?'),
]}
ORAL={'2026':'deux mille vingt-six','13 000':'treize mille','5 000':'cinq mille','4 000':'quatre mille','320':'trois cent vingt','160':'cent soixante','100':'cent','17,1':'dix-sept virgule un','9,8':'neuf virgule huit','1,7':'un virgule sept','12':'douze','11':'onze','10':'dix','3':'trois','2':'deux','1':'un'}
TITLES={16:['TOP 3','DES ARMÉES','LES PLUS PUISSANTES','2026'],17:['TOP 3','RECORDS DE','VITESSE ANIMALE','2026'],18:['TOP 3','DES PLUS GRANDS','PAYS DU MONDE','2026']}

def stage_for(w):return w/{16:'_montage/revision-spectaculaire-v9',17:'_montage/revision-spectaculaire-v5',18:'_montage/revision-spectaculaire-v5'}.get(int(w.name[:2]),'_montage/revision-spectaculaire-v3')

def prepare(w):
    n=int(w.name[:2]);stage=stage_for(w);stage.mkdir(parents=True,exist_ok=True)
    archive=w/'_montage/avant-revision-spectaculaire';archive.mkdir(exist_ok=True)
    for name in ['histoire.json','script.txt','voix-texte.txt','publication.txt','CREDITS.md','final.mp4','comparaison.mp4']:
        f=w/name
        if f.exists() and not (archive/name).exists():shutil.copy2(f,archive/name)
    d=copy.deepcopy(read(archive/'histoire.json'))
    d['titre']={16:'TOP 3 DES ARMÉES LES PLUS PUISSANTES',17:'TOP 3 DES VITESSES ANIMALES',18:'TOP 3 DES PLUS GRANDS PAYS DU MONDE'}[n]
    d['titre_fixe']=d['titre'].upper();d['statut']='Révision spectaculaire en production'
    d['scenes']=[]
    content=[(None,INTROS[n])]+copy.deepcopy(TEXTS[n])
    rank_one=next(i for i,(rank,_) in enumerate(content) if rank==1)
    rank,text=content[rank_one-1]
    content[rank_one-1]=(rank,text+' '+{16:'Mais le numéro un change encore de dimension.',17:'Mais le numéro un va encore beaucoup plus vite.',18:'Mais le numéro un est encore beaucoup plus vaste.'}[n])
    for rank,text in content:
        oral=text
        for number,spelling in ORAL.items():oral=oral.replace(number,spelling)
        d['scenes'].append(dict(narration=text,narration_voix=oral,rang=rank))
    d['script']=' '.join(s['narration'] for s in d['scenes']);d['hook']=INTROS[n]
    d['direction_visuelle']='Spectaculaire, proche de la référence : photos et archives plein écran, mentions courtes superposées, aucune grille, carte, infographie ou récapitulatif sur fond uni.'
    d['revision']={16:'spectaculaire-v8-budgets-trois-pays',17:'spectaculaire-v4-accroche-corrigee',18:'spectaculaire-v4-funfact'}.get(n,'spectaculaire-v3-teasing')
    if n==16:
        d['legende']='Trois armées colossales. Laquelle attendais-tu en première place ?'
        d['sources_a_verifier'] += ['Fun fact - boulangerie sur le USS Ronald Reagan : photo US Navy du 6 février 2007, spécialiste culinaire préparant de la pâte dans la boulangerie du navire. Source et crédits de la photo dans CREDITS.md. Milliers de marins et préparation de pains : reportage du service de communication du USS Ronald Reagan, 21 juin 2020 : https://www.dvidshub.net/news/386054/serving-sailors-reagans-kitchen']
        d['sources_a_verifier'] += ['Dépenses militaires 2025 : Chine 336 milliards USD ; Russie 190 milliards USD ; États-Unis 954 milliards USD, 33 % du total mondial. SIPRI Yearbook 2026 : https://www.sipri.org/yearbook/2026/05', 'Stocks nucléaires militaires estimés début 2026, même catégorie pour les trois pays : Chine 620, Russie 4 400, États-Unis 3 700 ogives ; comprend réserves et non-déployées, exclut les ogives retirées en attente de démantèlement. FAS : https://fas.org/initiative/status-world-nuclear-forces/']
        d['sources_a_verifier'] += ['Chine : stock estimé 5 870 chars ; Russie : stock estimé 5 630 chars ; États-Unis : 11 porte-avions, Global Firepower 2026, pages pays vérifiées le 8 novembre 2026.']
    if n==18:d['sources_a_verifier'] += ['Fun fact - Canada : plus long littoral du monde, côtes sur Atlantique, Pacifique et Arctique. Gouvernement du Canada : https://www.canada.ca/en/services/environment/our-environment/nature-based-climate-solutions/coastlines.html']
    if n==17:d['sources_a_verifier'] += ['Max Planck, novembre 2016 : femelles étudiées de 11 à 12 g, pointes à plus de 160 km/h. https://www.mpg.de/10820289/freischwanz-fledermaus-ist-der-schnellste-flieger-im-tierreich?c=987944']
    save(stage/'histoire.json',d)
    (stage/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']),encoding='utf-8')
    print(n,len(d['script'].split()),'mots',flush=True)

def photo(m,index,slug,frames,cx=.5,cy=.45):
    source=PHOTOS/(slug+'.jpg');target=m/f'photo-{index:02d}-{slug}-{frames}-{cx}-{cy}-zoom-v2.mp4'
    if target.exists():return target
    # Alternance de rapprochements et reculs fluides, sans inventer de mouvement du sujet.
    progress=f"(1-cos(PI*on/{max(1,frames-1)}))/2"
    zoom=f"1.025+0.065*{progress}" if index%2==0 else f"1.09-0.065*{progress}"
    vf=("scale=2160:3840:force_original_aspect_ratio=increase,"
        f"crop=2160:3840:max(0\\,min(iw-2160\\,iw*{cx}-1080)):max(0\\,min(ih-3840\\,ih*{cy}-1920)),"
        f"zoompan=z='{zoom}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1")
    run(['ffmpeg','-v','error','-y','-loop','1','-i',str(source),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p',str(target)])
    return target

def body_groups(n):
    if n==16:return [
      [('clip:china-parade',25,3,.5),('clip:china-parade',29,3,.5),('clip:china-parade',34,3,.5),('photo:china-tank',0,10,.5)],
      [('photo:china-carrier',0,7,.55),('clip:china-parade',46,13,.5)],
      [('photo:russia-soldiers-real',0,3,.5),('photo:russia-missile-real',0,7,.5),('photo:russia-jets',0,12,.5)],
      [('clip:russia-air',28,3,.5),('clip:russia-air',36,3,.5),('photo:russia-tank',0,18,.5)],
      [('photo:usa-airborne',0,3.5,.47),('photo:usa-jets',0,3.5,.5),('photo:usa-parachutes',0,12,.5)],
      [('photo:usa-carrier',0,4,.5),('photo:usa-bakery',0,16,.48)],
      [('photo:usa-airborne',0,3,.45),('photo:usa-jets',0,3.5,.5),('photo:usa-pararescue',0,12,.6)],
      [('photo:usa-parachutes',0,3,.5),('photo:usa-pararescue',0,12,.6)]]
    if n==17:return [
      [('clip:cheetah',.8,2.5,.5),('clip:cheetah',3.4,2.5,.5),('clip:cheetah',6,3,.55),('clip:cheetah',34,4,.5)],
      [('clip:cheetah',36,3,.5),('photo:cheetah-one',0,4,.55),('clip:cheetah',42,6,.5)],
      [('clip:bats',0,3,.5),('photo:bat-two',0,4,.5),('clip:bats',5,8,.5)],
      [('photo:bat-one',0,4,.5),('clip:bats',13,3,.5),('photo:bat-two',0,4,.55),('clip:bats',20,8,.5)],
      [('photo:falcon-stoop',0,4,.5),('photo:falcon-one',0,3.5,.5),('photo:falcon-two',0,7,.5)],
      [('photo:falcon-stoop',0,4,.5),('photo:falcon-one',0,4,.55),('photo:falcon-two',0,8,.5)],
      [('photo:cheetah-one',0,3,.55),('photo:bat-two',0,3,.5),('photo:falcon-two',0,8,.5)],
      [('clip:cheetah',49,2.5,.55),('clip:bats',28,2.5,.5),('photo:falcon-one',0,9,.5)]]
    return [
      [('photo:usa-city',0,3.5,.5),('photo:usa-canyon',0,3.5,.5),('photo:denali',0,8,.5)],
      [('clip:alaska',0,3,.5),('photo:denali',0,4,.6),('clip:alaska',12,8,.5)],
      [('photo:canada-lake',0,4,.55),('clip:canada',0,3.5,.5),('photo:canada-forest',0,8,.5)],
      [('photo:canada-coast',0,18,.5)],
      [('photo:kamchatka-one',0,4,.5),('photo:russia-volcano',0,4,.5),('photo:kamchatka-two',0,8,.5)],
      [('photo:russia-volcano',0,4,.5),('photo:kamchatka-two',0,4,.55),('photo:kamchatka-one',0,9,.5)],
      [('photo:kamchatka-two',0,4,.45),('photo:russia-volcano',0,4,.6),('photo:kamchatka-one',0,8,.5)],
      [('photo:usa-city',0,2.5,.55),('photo:canada-lake',0,2.5,.5),('photo:russia-volcano',0,10,.5)]]

def groups(n):
    hero={16:('photo:russia-tank',0,15,.52),17:('photo:canada-forest',0,15,.45),18:('photo:earth-hero',0,15,.5)}[n]
    body=body_groups(n)
    return [[hero]]+body

def numeric_v2(words):
    from revision_hpb_v10 import display_words,NUMBERS
    NUMBERS.update({'trois cent trente-six':'336','cent quatre-vingt-dix':'190','six cent vingt':'620','quatre mille quatre cents':'4 400','trois mille sept cents':'3 700','neuf cent cinquante-quatre':'954','deux mille vingt-cinq':'2025','deux millions':'2 millions','un tiers':'1/3','cinq mille':'5 000','quatre mille':'4 000','treize mille':'13 000','trois cent vingt':'320','cent soixante':'160','cent':'100','onze':'11','douze':'12','dix':'10','dix-sept virgule un':'17,1','neuf virgule huit':'9,8','un virgule sept':'1,7','kilomètres heure':'KM/H','kilomètres carrés':'km²'})
    return display_words(words)

def overlay_labels(n,starts,ends):
    if n==17:
        return [(starts[1],starts[3],'3 - GUÉPARD\\N100 KM/H - EN SPRINT'),
                (starts[3],starts[5],'2 - MOLOSSE DU BRÉSIL\\N160 KM/H - EN VOL'),
                (starts[5],starts[8],'1 - FAUCON PÈLERIN\\N320 KM/H - EN PIQUÉ')]
    labels={16:[(0,'3 - CHINE'),(1,'UNE ARMÉE EN TRANSFORMATION'),(2,'2 - RUSSIE'),(3,'BLINDÉS - AVIATION - MISSILES'),(4,'1 - ÉTATS-UNIS'),(5,'UNE BOULANGERIE À BORD')],
            17:[(0,'GUÉPARD - ENVIRON 100 KM/H'),(2,'MOLOSSE DU BRÉSIL - ENVIRON 160 KM/H'),(4,'FAUCON - ENVIRON 320 KM/H')],
            18:[(0,'ÉTATS-UNIS - 9,8 MILLIONS KM²'),(2,'CANADA - PRESQUE 10 MILLIONS KM²'),(4,'RUSSIE - 17,1 MILLIONS KM²'),(6,'ENVIRON 1,7 FOIS LE CANADA')]}[n]
    result=[]
    for i,label in labels:
        i+=1
        result.append((starts[i],min(ends[i],starts[i]+4),label))
    return result

def render(w):
    stage=stage_for(w);m=stage/'_montage';d=read(stage/'histoire.json');n=d['numero'];oral=read(m/'timings-oraux.json')
    if oral['duration']<=60:raise ValueError('Narration trop courte : enrichir avant export.')
    t=copy.deepcopy(oral);t['words']=numeric_v2(t['words']);save(m/'timings.json',t)
    starts=[sum(t['scene_durations'][:i]) for i in range(len(d['scenes']))];ends=[sum(t['scene_durations'][:i+1]) for i in range(len(d['scenes']))]
    item=dict(series=d['serie'],title=TITLES[n],credits={16:'Photos et archives - crédits dans le dossier',17:'Guinness - Max Planck - Photos et archives',18:'Nations unies - Photos et archives'}[n],facts=[])
    layers(m,item);cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=83,words_per_caption=5,subtitle_wrap=20)
    subs(m,t,item,cfg);p=m/'sous-titres-reference.ass';s=p.read_text(encoding='utf-8')
    s=s.replace('Style: Fact,Poppins ExtraBold,53','Style: Fact,Poppins ExtraBold,57')
    # Mentions directement sur l’image, sans tableau ni panneau de présentation.
    for a,b,label in overlay_labels(n,starts,ends):
        s+=f'Dialogue: 1,{assemble._ass_time(a)},{assemble._ass_time(b)},Fact,,0,0,0,,{{\\an8\\pos(540,250)\\fs52}}{label}\n'
    if n==16:
        for i,value in [(1,'336'),(4,'190'),(5,'954')]:
            a=next(x['start'] for x in t['words'] if x['w'].strip('.,:;!?')==value and starts[i]<=x['start']<ends[i]);b=min(ends[i],a+4)
            s+=f'Dialogue: 1,{assemble._ass_time(a)},{assemble._ass_time(b)},Fact,,0,0,0,,{{\\an8\\pos(540,370)\\fs58}}{value} MILLIARDS $\\N{{\\fs42}}DÉPENSES MILITAIRES - 2025\n'
        for i,value in [(2,'620'),(3,'4 400'),(7,'3 700')]:
            a=next(x['start'] for x in t['words'] if x['w'].strip('.,:;!?')==value and starts[i]<=x['start']<ends[i]);b=min(ends[i],a+4)
            s+=f'Dialogue: 1,{assemble._ass_time(a)},{assemble._ass_time(b)},Fact,,0,0,0,,{{\\an8\\pos(540,370)\\fs52}}ENVIRON {value} OGIVES\\N{{\\fs42}}STOCK MILITAIRE - ESTIMATION 2026\n'
    if n==17:
        s+=f'Dialogue: 1,{assemble._ass_time(starts[3])},{assemble._ass_time(starts[5])},Fact,,0,0,0,,{{\\an8\\pos(540,440)\\fs44}}MESURE PAR RAPPORT AU SOL\n'
    if n==18:
        a=next(x['start'] for x in t['words'] if x['w'].strip('.,:;!?').lower()=='terres')
        s+=f'Dialogue: 1,{assemble._ass_time(max(starts[1],a-.6))},{assemble._ass_time(a+2.4)},Fact,,0,0,0,,{{\\an8\\pos(540,350)\\fs52}}TERRES + EAUX\n'
    p.write_text(s,encoding='utf-8');shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
    edits=[];files=[];cursor=0;used={}
    for scene,group in enumerate(groups(n)):
        end=round(ends[scene]*30)
        for source,start,limit,cx in group:
            if cursor>=end:break
            frames=min(round(limit*30),end-cursor);kind,slug=source.split(':')
            if kind=='photo':path=photo(m,len(files),slug,frames,cx)
            else:
                interval=(start,start+frames/30)
                assert not any(max(start,a)<min(interval[1],b)-.001 for a,b in used.get(slug,[])),source
                used.setdefault(slug,[]).append(interval);path=render_clip(m,len(files),slug,start,frames,cx)
            uniform=m/('uniform-'+path.name)
            if not uniform.exists():run(['ffmpeg','-v','error','-y','-i',str(path),'-c','copy','-bsf:v','h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(uniform)])
            edits.append(dict(scene=scene,source=source,start_source=start,start=cursor/30,duration=frames/30,crop_x=cx));files.append(uniform.name);cursor+=frames
        assert cursor==end,(n,scene,cursor/30,end/30)
        print(n,'scène',scene+1,'photos et séquences',flush=True)
    save(m/'montage.json',edits);(m/'concat.txt').write_text(''.join(f"file '{f}'\n" for f in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','base.mp4'],m)
    track=music(w,m,t,n)
    accents=[]
    if n==16:
        accents=[next(x['start'] for x in t['words'] if x['w'].strip('.,:;!?')==value)+.2 for value in ['336','190','954']]
    zoom_expression='1'+''.join(f'+0.035*exp(-pow((on/30-{at:.3f})/0.28,2))' for at in accents)
    motion=(f"scale=2160:3840,zoompan=z='{zoom_expression}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30," if accents else '')
    save(m/'effets-zoom.json',dict(photos='Alternance zoom avant/arrière fluide 2,5 à 9 %',accents_budget_secondes=accents,amplitude_accent=.035,textes_stables=True))
    graph=('[0:v]fps=30,setpts=PTS-STARTPTS,'+motion+'ass=sous-titres-reference.ass:fontsdir=.[cap];[3:v]format=rgba,fade=t=out:st=1.3:d=0.2:alpha=1[hook];[cap][hook]overlay=0:0:enable=lt(t\\,1.5):shortest=1[h];[h][2:v]overlay=0:0:shortest=1[v]')
    target=stage/'final.mp4'
    run(['ffmpeg','-v','error','-y','-i','base.mp4','-i','mix.wav','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(target)],m)
    actual=validate_duration(target);run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    assert abs(actual-t['duration'])<.2
    d.update(statut='Révision spectaculaire rendue - contrôle visuel en cours',musique=track)
    save(stage/'histoire.json',d)
    # Les documents et les MP4 précédents restent dans avant-revision-spectaculaire.
    for name in ['final.mp4','histoire.json','script.txt']:shutil.copy2(stage/name,w/name)
    for name in ['timings.json','timings-oraux.json','voix.mp3','montage.json']:
        shutil.copy2(m/name,w/'_montage'/name)
    save(w/'_montage/controle.json',dict(duration_mp4=actual,voice_model=t['model'],voix='Hugo ElevenLabs',decodage_integral=True,plans_sans_boucle=True,habillage='HPB - photos et archives plein écran',verification_visuelle='en cours',revision=d['revision']))
    compare(w)
    print(n,'RÉVISION ET COMPARAISON',actual,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('step',choices=['prepare','speech','render']);parser.add_argument('--numero',type=int);args=parser.parse_args()
    for w in FOLDERS:
        if args.numero is not None and int(w.name[:2])!=args.numero:continue
        if args.step=='prepare':prepare(w)
        elif args.step=='speech':speech(stage_for(w))
        else:render(w)
