"""Habillage reconstruit dans les marges du lecteur, sans ajouter de surcouche aux anciens textes."""
import copy,json,re,shutil,hashlib,unicodedata,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import yaml
from montage_reel import ROOT,run
from habillage_reference import layers
from narrateur import assemble
from comparer_lot_16_18 import compare

SAFE=(90,250,880,1380)
INCLUDE_APPROVED=False
STAGES={15:'revision-accroche-claire-v16',16:'revision-impact-v10',17:'podium-mondial-v6',18:'revision-spectaculaire-v5'}
TITLES={13:['SE PESER','DANS L’ESPACE'],14:['TOP 3','DES VOITURES','LES PLUS RAPIDES','2026'],15:['TOP 3 DES VILLES','LES PLUS','EMBOUTEILLÉES','2026'],16:['TOP 3 DES ARMÉES','LES PLUS','PUISSANTES','2026'],17:['TOP 3 DES','ANIMAUX LES PLUS','RAPIDES DU MONDE','2026'],18:['TOP 3','DES PLUS GRANDS','PAYS DU MONDE','2026']}
SERIES={13:'SE PESER DANS L’ESPACE',14:'TOP 3 - VOITURES RAPIDES',15:'TOP 3 - VILLES EMBOUTEILLÉES',16:'TOP 3 - ARMÉES PUISSANTES',17:'TOP 3 - ANIMAUX RAPIDES',18:'TOP 3 - PLUS GRANDS PAYS'}
CARD={14:['300+ : SON NOM VIENT','DES 300 MILES/H'],15:['1868 : PREMIER FEU','AU GAZ','IL A EXPLOSÉ'],16:['UNE BOULANGERIE','À BORD DU','RONALD REAGAN'],17:['DES LUNETTES NATURELLES'],18:['LE PLUS LONG LITTORAL','EST AU CANADA']}

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def seconds(s):
 h,m,x=s.split(':');return int(h)*3600+int(m)*60+float(x)
def font(size):return ImageFont.truetype(str(ROOT/'assets/fonts/Poppins-ExtraBold.ttf'),size)
def plain(s):return re.sub(r'\{[^}]*\}','',s).replace(r'\h','\u00a0')

def wrap_caption(text,size=80):
 text=text.replace(r'\N',' ')
 text=re.sub(r'(?<=\d) (?=\d{3}\b)',lambda _:r'\h',text)
 lines=[];line=[];measure=ImageDraw.Draw(Image.new('RGB',(1,1)))
 for word in text.split(' '):
  if not word:continue
  candidate=' '.join(line+[word])
  if line and measure.textlength(plain(candidate),font=font(size))>730:lines.append(' '.join(line));line=[]
  line.append(word)
 if line:lines.append(' '.join(line))
 return r'\N'.join(lines)

def card(m,n,*,top=None,padding=None):
 im=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(im);lines=CARD[n];size=54
 while max(d.textlength(x,font=font(size)) for x in lines)>700:size-=1
 f=font(size);h=font(40);stroke=3;cap=d.textbbox((0,0),'H',font=f,stroke_width=stroke);height=cap[3]-cap[1]
 hb=d.textbbox((0,0),'FUN FACT',font=h,stroke_width=stroke);hh=hb[3]-hb[1]
 if top is None:top=415 if n==17 else 650
 pad_top=20 if padding is None else padding
 pad_bottom=22 if padding is None else padding
 first=top+pad_top+hh+22
 d.text(((960-d.textlength('FUN FACT',font=h))/2,top+pad_top-hb[1]),'FUN FACT',font=h,fill='#FFE24A',stroke_width=3,stroke_fill='#080B10')
 layout=[]
 for i,line in enumerate(lines):
  base=''.join(c for c in unicodedata.normalize('NFD',line) if not unicodedata.combining(c));box=d.textbbox((0,0),base,font=f,stroke_width=stroke);y=first+i*(height+8)
  x=480-d.textlength(line,font=f)/2;d.text((x,y-box[1]),line,font=f,fill='#F7F3E9',stroke_width=stroke,stroke_fill='#080B10');layout.append(dict(texte=line,haut=y,bas=y+height,taille=size,contour=stroke,accents_en_superposition=True))
 # Le slash et certains glyphes dépassent le corps des capitales : mesurer
 # l'encre réellement rendue, sans modifier l'interligne compact.
 ink=im.getbbox();bottom=ink[3]+pad_bottom
 assert bottom<1000
 bg=Image.new('RGBA',im.size);ImageDraw.Draw(bg).rounded_rectangle((100,top,860,bottom),radius=9,fill=(18,21,28,235));im=Image.alpha_composite(bg,im)
 im.save(m/'funfact-safe.png');save(m/'funfact-layout.json',layout)
 save(m/'funfact-marges.json',dict(rectangle=[100,top,860,bottom],encre=list(ink),marge_haute=ink[1]-top,marge_basse=bottom-ink[3],mesure='Encre réelle, contour et dépassement du slash inclus'))
 return (top,bottom)

def wrap_fact(text,size=46):
 text=re.sub(r'\{[^}]*\}','',text);out=[]
 for paragraph in text.split(r'\N'):
  words=paragraph.split();line=''
  for word in words:
   candidate=(line+' '+word).strip()
   if line and ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(candidate,font=font(size))>730:out.append(line);line=word
   else:line=candidate
  if line:out.append(line)
 return r'\N'.join(out)

def check_collisions(lines,m):
 # Précontrôle conservateur des textes ASS : positions, intervalles et hauteur des lignes.
 boxes=[]
 for line in lines:
  p=line.split(',',9);pos=re.search(r'\\pos\((\d+),(\d+)\)',p[9]);fs=re.search(r'\\fs(\d+)',p[9])
  if not pos or not fs:continue
  y=int(pos[2]);size=int(fs[1]);pad=18 if p[3]!='Default' else 8
  height=size*1.55*(plain(p[9]).count(r'\N')+1)
  top,bottom=(y-height-pad,y+pad) if r'\an2' in p[9] else (y-pad,y+height+pad)
  boxes.append(dict(debut=seconds(p[1]),fin=seconds(p[2]),haut=top,bas=bottom,style=p[3],texte=plain(p[9])))
 risks=[]
 for a in boxes:
  if a['style']!='Default':continue
  for b in boxes:
   if b['style']=='Default':continue
   if max(a['debut'],b['debut'])<min(a['fin'],b['fin']) and max(a['haut'],b['haut'])<min(a['bas'],b['bas']):risks.append(dict(sous_titre=a,bandeau=b))
 save(m/'controle-collisions.json',dict(methode='Précontrôle conservateur ASS ; contrôle visuel du MP4 requis.',risques=risks))
 assert not risks,risks[:2]

def prepare(m,w,n):
 d=read(w/'histoire.json');t=read(w/'_montage/timings.json');src=w/'_montage' if n in (13,14) else w/'_montage'/STAGES[n]/'_montage'
 active=w/'_montage'/('sous-titres-reference.ass' if n==17 else 'sous-titres-ponctuation-liee.ass')
 old=active.read_text(encoding='utf-8');events=[line.split(',',9) for line in old.splitlines() if line.startswith('Dialogue:')]
 item=dict(title=TITLES[n],series=SERIES[n],credits='',title_bottom=1370,title_left=100,title_width=750,title_size=100,title_stroke=6,tiktok_safe=True)
 layers(m,item);shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
 cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')));cfg['render'].update(subtitle_size=80,words_per_caption=5,subtitle_wrap=17)
 caption_start={13:2.107,14:2.96,15:t['scene_durations'][0],16:t['scene_durations'][0],17:t['scene_durations'][0],18:4.007}[n]
 caption_start=d.get('correction_locale',{}).get('fin_annonce_titre',caption_start)
 reveal_start=caption_start
 if n==14:caption_start=max(4.8,caption_start) # titre, puis compteur ; le cartouche nomme déjà la SSC pendant l'annonce du rang
 # Filtrer les mots avant leur groupement : couper seulement l'horaire laisserait
 # réapparaître la fin du titre dans un bloc chevauchant le début du classement.
 caption_words=[x for x in t['words'] if x['start']>=caption_start-.005]
 assemble.YELLOW='&H4AE2FF&';assemble.RED='&H4E62FF&';assemble.write_subtitles(cfg,caption_words,m/'captions.ass')
 if n==16 and d.get('triptyque_equipements'):
  cuts=[0,52.380333,53.113333,54.073333,54.633333,55.393333,t['duration']+1];dialogues=[];cap_header=None
  for i,(lo,hi) in enumerate(zip(cuts,cuts[1:])):
   words=[x for x in caption_words if lo-.001<=x['start']<hi-.001];part=m/f'captions-partie-{i}.ass';assemble.write_subtitles(cfg,words,part)
   content=part.read_text(encoding='utf-8');cap_header=content.split('[Events]')[0]+'[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
   for line in content.splitlines():
    if not line.startswith('Dialogue:'):continue
    q=line.split(',',9);q[1]=assemble._ass_time(max(lo,seconds(q[1])));q[2]=assemble._ass_time(min(hi,seconds(q[2])));dialogues.append(','.join(q))
  (m/'captions.ass').write_text(cap_header+'\n'.join(dialogues)+'\n',encoding='utf-8')
 header=old.split('[Events]')[0]+'[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
 fact=d.get('fun_fact_affichage');blocked=[]
 if fact:
  card(m,n)  # la transcription continue pendant le fun fact (demande de Marc)
 if n==17:
  for p in events:
   if p[3]!='Default' and 'KM/H' in p[9]:blocked.append((seconds(p[1]),seconds(p[2])))
 new=[]
 # Ne pas transcrire de nouveau le titre déjà lu pendant son annonce orale.
 for line in (m/'captions.ass').read_text(encoding='utf-8').splitlines():
  if not line.startswith('Dialogue:'):continue
  p=line.split(',',9);a,b=seconds(p[1]),seconds(p[2]);segments=[(max(caption_start,a),b)] if b>caption_start else []
  for lo,hi in blocked:
   segments=[part for x,y in segments for part in ([(x,min(y,lo))] if x<lo else [])+([(max(x,hi),y)] if y>hi else []) if part[1]-part[0]>.001]
  size=90
  if n==16 and d.get('triptyque_equipements') and 52.38<=a<55.39:
   p[9]=p[9].replace(r'\N',' ')
   while ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(plain(p[9]),font=font(size))>730:size-=2
  # Taille 90 par défaut ; revenir vers 80 si le bloc dépasserait trois lignes.
  while size>80 and wrap_caption(p[9],size).count(r'\N')>2:size-=2
  p[9]=wrap_caption(p[9],size);text=plain(p[9]);count=text.count(r'\N')+1
  y=1370
  for x,z in segments:
   q=p[:];q[1]=assemble._ass_time(x);q[2]=assemble._ass_time(z);q[9]=f'{{\\an2\\pos(540,{y})\\fs{size}\\fsp0}}'+p[9];new.append(','.join(q))
 for p in events:
  if p[3]=='Default' or any(x in p[9].upper() for x in ['POINTES EN UN SEUL SENS','TA PIRE EXPÉRIENCE','PAS BANAL, HEIN','PREMIER FEU AU GAZ']):continue
  if n==13 and 'MESURER LA MASSE' in plain(p[9]):continue
  raw=plain(p[9]);stat=any(x in raw for x in ['MILLIARDS','OGIVES','STOCK MILITAIRE','DÉPENSES MILITAIRES'])
  y,size=(650,50) if stat else (650,48) if 'TERRES + EAUX' in raw else (420,46)
  q=p[:];q[9]=f'{{\\an8\\pos(540,{y})\\fs{size}}}'+wrap_fact(p[9],size)
  if n in (14,18) and seconds(q[1])<reveal_start and seconds(q[2])>reveal_start:q[1]=assemble._ass_time(reveal_start)
  if n==17 and 'FAUCON GERFAUT' in raw:
   # Sur le portrait filmé, réserver le haut à la tête de l'oiseau.
   first=q[:];first[2]=assemble._ass_time(min(4.9,seconds(q[2])));first[9]=r'{\an8\pos(540,1130)\fs60}3 - FAUCON GERFAUT';new.append(','.join(first));q[1]=assemble._ass_time(4.9)
  q[1]=assemble._ass_time(max(1.5,seconds(q[1])));new.append(','.join(q))
 ass=m/'sous-titres-safe.ass';ass.write_text(header+'\n'.join(new)+'\n',encoding='utf-8')
 check_collisions(new,m)
 # Contrôle déterministe des bords : le texte ne doit pas déborder sur les commandes.
 for line in new:
  p=line.split(',',9);body=plain(p[9]);fs=int(re.search(r'\\fs(\d+)',p[9]).group(1))
  for segment in body.split(r'\N'):
   assert ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(segment,font=font(fs))<780,(n,segment)
 save(m/'zones-reservees.json',dict(zone_texte=SAFE,haut_reserve=250,bas_reserve=540,droite_reservee=200,usage='Marge de travail conservatrice, aperçu simulé du lecteur avec légende repliée ; interface variable selon appareil et longueur de légende.',contour_titres=6,contour_funfacts=3,sources='https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads'))
 return src,t,d

def render(n):
 w=next((ROOT/'out').glob(f'{n}-*'))
 if (w/'validation-utilisateur.json').exists() and not INCLUDE_APPROVED:
  print(n,'version validée conservée : révision ignorée',flush=True);return
 root=w/'_montage';m=root/'tiktok-safe';m.mkdir(exist_ok=True);archive=m/'avant';archive.mkdir(exist_ok=True)
 for name in ['final.mp4','comparaison.mp4','histoire.json']:
  if not (archive/name).exists():shutil.copy2(w/name,archive/name)
 src,t,d=prepare(m,w,n);base=root/('base-hpb-v11.mp4' if n==13 else 'base-hpb-v13.mp4') if n in (13,14) else src/'base.mp4'
 if n==17:base=src/'base-uniforme.mp4'
 override=d.get('correction_locale',{})
 if override.get('base'):base=w/override['base']
 audio=w/override['audio'] if override.get('audio') else archive/'final.mp4'
 inputs=['-i',str(base),'-i',str(audio),'-loop','1','-framerate','30','-i','titre-hook-reference.png','-loop','1','-framerate','30','-i','header-footer-reference.png']
 if n>=14:inputs+=['-loop','1','-framerate','30','-i','funfact-safe.png']
 graph='';clean='[0:v]'
 if n in (13,14):
  idx=4 if n==13 else 5;cut=8 if n==13 else 4
  intro=root/('intro-pesee-demonstrative.mp4' if n==13 else 'intro-ssc-safe.mp4')
  if n==14 and (root/'intro-ssc-titre-bas.mp4').exists():intro=root/'intro-ssc-titre-bas.mp4'
  if not intro.exists():intro=root/'intro-ssc-kmh-original.mp4'
  inputs+=['-i',str(intro)]
  graph=f'[{idx}:v]trim=end={cut},setpts=PTS-STARTPTS,fps=30[a];[0:v]trim=start={cut},setpts=PTS-STARTPTS,fps=30[b];[a][b]concat=n=2:v=1:a=0[clean];';clean='[clean]'
 motion=''
 if n==16:
  accents=read(src/'effets-zoom.json')['accents_budget_secondes'];z='1'+''.join(f'+0.035*exp(-pow((on/30-{at:.3f})/0.28,2))' for at in accents);motion=f"scale=2160:3840,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,"
 graph+=clean+'fps=30,setpts=PTS-STARTPTS,'+motion+'ass=sous-titres-safe.ass:fontsdir=.[s];[s][2:v]overlay=0:0:enable=lt(t\\,1.5):shortest=1[h];[h][3:v]overlay=0:0:shortest=1[q]'
 if n>=14:
  fact=d['fun_fact_affichage'];graph+=f';[q][4:v]overlay=60:0:enable=between(t\\,{fact["debut"]}\\,{fact["fin"]}):shortest=1[v]'
 else:graph+=';[q]null[v]'
 target=m/'final.mp4';run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(t['duration']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(target)]))
 durations={s['codec_type']:float(s['duration']) for s in info['streams'] if s['codec_type'] in ('video','audio')}
 assert durations['video']>60 and abs(durations['video']-durations['audio'])<.3,durations
 run(['ffmpeg','-v','error','-i',str(target),'-f','null','-']);shutil.copy2(target,w/'final.mp4');compare(w)
 d['habillage_tiktok']=dict(dossier='_montage/tiktok-safe',zone_texte=SAFE,mention_nom_du_compte=False,contour_titres=6,contour_funfacts=3,transcription_sans_doublon_pendant_funfacts=True);save(w/'histoire.json',d)
 sha=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest();save(m/'controle.json',dict(sha256=sha,decodage_integral=True,comparaison_a_jour=True,controle_visuel='à effectuer avec aperçu simulé du lecteur'))
 print(n,'habillage sécurisé et comparaison prêts',flush=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('numeros',nargs='*',type=int);p.add_argument('--inclure-validees',action='store_true');args=p.parse_args();INCLUDE_APPROVED=args.inclure_validees
 with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,args.numeros or range(13,19)))
