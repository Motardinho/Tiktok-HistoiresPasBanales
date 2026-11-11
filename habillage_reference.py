"""Habillage de la présentation retenue : header/footer permanents, titre de hook seul."""
import copy,json,shutil,sys,re,unicodedata
from PIL import Image,ImageDraw,ImageChops
import yaml
from construire_identite import video_mark_image,font,INK,CREAM,YELLOW
from montage_reel import ROOT,run
from narrateur import assemble

ITEMS={
 'astronautes-sport-en-orbite':dict(count=23,title=['SE PESER','DANS','L’ESPACE ?'],series='COMMENT C’EST POSSIBLE ?',credits='ASC / NASA',facts=[(33.6,38.08,'AVEC UNE PERSONNE'),(38.08,42.24,'SANS PERSONNE')]),
 'trois-records-voitures-vitesse':dict(count=19,title=['3 HYPERCARS.','LE PIÈGE DES','CHIFFRES.'],series='LE CHIFFRE QUI SURPREND',credits='Hennessey / Bugatti',facts=[(21.08,28.64,'CHIRON • 2019 • UN SEUL SENS'),(33.24,38.04,'BOLIDE CLIENT • 380 KM/H')]),
 'villes-plus-lentes-tomtom-2024':dict(count=24,title=['DES JOURS','DANS LES','BOUCHONS.'],series='LE CHIFFRE QUI SURPREND',credits='Pexels • INRIX 2024',facts=[(17.88,25.24,'LONDRES • 101 H'),(25.24,33.96,'NEW YORK • 102 H'),(33.96,41.44,'PARIS • 97 H')])}


def label_text(text):
 return re.sub(r'\s*[•·–—]\s*',' - ',text).replace(' / ',' - ')

def layers(w,item):
 header=Image.new('RGBA',(1080,1920))
 if item.get('tiktok_safe'):
  header.alpha_composite(video_mark_image(110),(90,265))
  d=ImageDraw.Draw(header);label=label_text(item['series']);sz=42
  while d.textlength(label,font=font(sz))>600:sz-=1
  # Centrer le corps des capitales ; les accents débordent dans la marge haute.
  tile=Image.new('RGBA',(750,140));ImageDraw.Draw(tile).text((10,10),label,font=font(sz),fill=YELLOW);ink=tile.getbbox()
  plain=''.join(c for c in unicodedata.normalize('NFD',label) if not unicodedata.combining(c))
  body=Image.new('RGBA',tile.size);ImageDraw.Draw(body).text((10,10),plain,font=font(sz),fill=YELLOW);body_box=body.getbbox()
  pad=22;height=body_box[3]-body_box[1]+2*pad;top=277;width=ink[2]-ink[0]
  d.rectangle((225,top,225+width+38,top+height),fill=INK)
  text_y=top+pad-(body_box[1]-ink[1]);header.alpha_composite(tile.crop(ink),(244,text_y))
  (w/'bandeau-layout.json').write_text(json.dumps(dict(texte=label,taille=sz,rectangle=[225,top,225+width+38,top+height],marge_corps_haut=pad,marge_corps_bas=pad,accents_en_debord=True),ensure_ascii=False,indent=2),encoding='utf-8')
  header.save(w/'header-footer-reference.png');hook_layer(w,item);return
 shade=Image.new('RGBA',header.size);sd=ImageDraw.Draw(shade)
 for y in range(1650,1920):sd.line((0,y,1080,y),fill=(18,21,28,int(190*(y-1650)/270)))
 header.alpha_composite(shade)
 header.alpha_composite(video_mark_image(170),(32,35))
 d=ImageDraw.Draw(header)
 label=label_text(item['series']);sz=42
 while d.textlength(label,font=font(sz))>740:sz-=1
 width=d.textlength(label,font=font(sz))
 d.rectangle((225,79,225+width+60,150),fill=INK)
 box=d.textbbox((0,0),label,font=font(sz))
 text_y=79+(71-(box[3]-box[1]))/2-box[1]
 d.text((255,text_y),label,font=font(sz),fill=YELLOW)
 header.save(w/'header-footer-reference.png')
 hook_layer(w,item)


def hook_layer(w,item):
 hook=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(hook)
 for y in range(850,1920):d.line((0,y,1080,y),fill=(18,21,28,int(155*(y-850)/1070)))
 y=item.get('title_top',1138);left=item.get('title_left',75);max_width=item.get('title_width',930);stroke=item.get('title_stroke',5)
 gap=item.get('title_line_gap',8)
 layout=[]
 letters=Image.new('RGBA',(1080,1920));bodies=Image.new('RGBA',(1080,1920))
 if len(item['title'])>4:raise ValueError('Titre limité à quatre lignes : revoir le découpage.')
 for i,label in enumerate(item['title']):
  label=label_text(label).replace("'",'’')
  sz=82 if label=='2026' else item.get('title_size',112)
  while d.textlength(label,font=font(sz))>max_width:sz-=2
  line=Image.new('RGBA',(1080,300));ld=ImageDraw.Draw(line)
  yellow=i==len(item['title'])-1 or (item['title'][-1]=='2026' and i==len(item['title'])-2)
  ld.text((left,0),label,font=font(sz),fill=YELLOW if yellow else CREAM,stroke_width=stroke,stroke_fill=INK)
  bounds=line.getbbox()
  plain=''.join(c for c in unicodedata.normalize('NFD',label) if not unicodedata.combining(c))
  body=Image.new('RGBA',(1080,300));ImageDraw.Draw(body).text((left,0),plain,font=font(sz),fill='white',stroke_width=stroke,stroke_fill='black')
  body_bounds=body.getbbox();body_height=body_bounds[3]-body_bounds[1]
  line=line.crop((0,bounds[1],1080,bounds[3]))
  ink_y=y+bounds[1]-body_bounds[1]
  placed=Image.new('RGBA',(1080,1920));placed.alpha_composite(line,(0,ink_y))
  # Les accents débordent sur la ligne du dessus, détachés par le contour sombre (règle de Marc) :
  # seule une collision entre corps de lettres, accents exclus, bloque le titre.
  placed_body=Image.new('RGBA',(1080,1920));placed_body.alpha_composite(body,(0,y-body_bounds[1]))
  if ImageChops.multiply(bodies.getchannel('A'),placed_body.getchannel('A')).getbbox():raise ValueError(f'Collision de lettres dans le titre : {label}')
  bodies.alpha_composite(placed_body)
  letters.alpha_composite(placed)
  layout.append(dict(texte=label,taille=sz,haut=y,bas_exclusif=y+body_height,haut_encre=ink_y,bas_encre=ink_y+line.height,accents_en_superposition=True,espace_apres=gap))
  y+=body_height+gap
 if 'title_bottom' in item:
  bottom=item['title_bottom'];bounds=letters.getbbox();dy=bottom-bounds[3]
  shifted=Image.new('RGBA',letters.size);shifted.alpha_composite(letters,(0,dy));letters=shifted
  for row in layout:
   for key in ['haut','bas_exclusif','haut_encre','bas_encre']:row[key]+=dy
  assert letters.getbbox()[3]==bottom
 hook.alpha_composite(letters)
 hook.save(w/'titre-hook-reference.png')
 (w/'titre-hook-layout.json').write_text(json.dumps(dict(methode='Corps des capitales espacés régulièrement ; accents en superposition, sans modifier interligne',espace_pixels=gap,collision=False,ancrage_bas=item.get('title_bottom'),lignes=layout),ensure_ascii=False,indent=2),encoding='utf-8')

def subs(w,t,item,cfg):
 assemble.YELLOW='&H4AE2FF&';assemble.RED='&H4E62FF&'
 p=w/'sous-titres-reference.ass';assemble.write_subtitles(cfg,t['words'],p)
 s=p.read_text(encoding='utf-8').replace('&H00FFFFFF','&H00E9F3F7').replace('8,50,50,1090,1','8,65,65,1190,1')
 st='Style: Fact,Poppins ExtraBold,53,&H004AE2FF,&H004AE2FF,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,3,14,0,8,75,75,230,1\n'
 s=s.replace('\n[Events]','\n'+st+'\n[Events]')
 lines=[]
 group_starts={}
 for line in s.splitlines():
  if line.startswith('Dialogue:'):
   parts=line.split(',',9)
   if parts[3]=='Default':
    h,m,x=parts[1].split(':');at=int(h)*3600+int(m)*60+float(x)
    key=re.sub(r'\{[^}]*\}','',parts[9]);group_starts.setdefault(key,at)
 for line in s.splitlines():
  if line.startswith('Dialogue:'):
   parts=line.split(',',9)
   def seconds(value):
    h,m,x=value.split(':');return int(h)*3600+int(m)*60+float(x)
   start,end=seconds(parts[1]),seconds(parts[2])
   if parts[3]=='Default':
    if end<=1.5:continue
    if start<1.5:parts[1]=assemble._ass_time(1.5)
   hook_seconds=item.get('hook_seconds',1.5 if item['title'][0].startswith('TOP 3') else 4)
   key=re.sub(r'\{[^}]*\}','',parts[9])
   if group_starts.get(key,start)<hook_seconds:parts[9]='{\\an8\\pos(540,620)}'+parts[9]
   if item is ITEMS['astronautes-sport-en-orbite'] and start<7.92:parts[9]='{\\an8\\pos(540,620)}'+parts[9]
   line=','.join(parts)
  lines.append(line)
 s='\n'.join(lines)+'\n'
 for a,b,label in item['facts']:
  if b>1.5:s+=f'Dialogue: 1,{assemble._ass_time(max(a,1.5))},{assemble._ass_time(b)},Fact,,0,0,0,,{label_text(label)}\n'
 p.write_text(s,encoding='utf-8')

def compare(slug,w,dur,version=6):
 original=ROOT/'assets/references-faiseemoc84'/(slug+'.mp4')
 od=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(original)]))['format']['duration'])
 graph=("[0:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[l];"
        "[1:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[r];"
        "[l][r]hstack=inputs=2,pad=1080:1040:0:80:color=0x12151C,"
        "drawtext=fontfile=police.ttf:text='ORIGINAL':fontcolor=0xF7F3E9:fontsize=27:x=180:y=23,"
        "drawtext=fontfile=police.ttf:text='HISTOIRES PAS BANALES':fontcolor=0xFFE24A:fontsize=24:x=632:y=25[v]")
 run(['ffmpeg','-v','error','-y','-i',str(original),'-i',f'final-hpb-v{version}.mp4','-filter_complex',graph,'-map','[v]','-map','0:a:0','-map','1:a:0','-t',str(max(dur,od)),'-c:v','libx264','-preset','fast','-crf','21','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-metadata:s:a:0','title=Original','-metadata:s:a:1','title=Histoires pas banales','-disposition:a:0','0','-disposition:a:1','default','-movflags','+faststart',f'comparaison-hpb-v{version}.mp4'],w)

def main(slug):
 w=ROOT/'out'/slug;item=ITEMS[slug]
 cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
 cfg['render'].update(subtitle_size=88,words_per_caption=5,subtitle_wrap=19)
 t=json.loads((w/'timings.json').read_text(encoding='utf-8'))
 dur=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'voix.mp3')]))['format']['duration'])
 layers(w,item);subs(w,t,item,cfg)
 # Sources plein écran seules, y compris le premier plan : aucun miroir ni dédoublement.
 files=[f'dynamique{i:02d}.mp4' for i in range(item['count'])]
 (w/'concat-reference.txt').write_text(''.join(f"file '{p}'\n" for p in files),encoding='utf-8')
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat-reference.txt','-c','copy','base-reference.mp4'],w)
 shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',w/'police.ttf')
 # Export d'un aperçu fidèle avant le rendu complet.
 run(['ffmpeg','-v','error','-y','-ss','0.8','-i','base-reference.mp4','-frames:v','1','frame-reference.png'],w)
 im=Image.open(w/'frame-reference.png').convert('RGBA');im.alpha_composite(Image.open(w/'titre-hook-reference.png'));im.alpha_composite(Image.open(w/'header-footer-reference.png'));im.convert('RGB').save(w/'apercu-hpb-v6.png')
 graph=('[0:v]ass=sous-titres-reference.ass:fontsdir=.[cap];'
        '[3:v]format=rgba,fade=t=out:st=3.8:d=0.2:alpha=1[hook];'
        '[cap][hook]overlay=0:0:enable=lt(t\\,4):shortest=1[h];'
        '[h][2:v]overlay=0:0:shortest=1[v]')
 run(['ffmpeg','-v','error','-y','-i','base-reference.mp4','-i','voix.mp3','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(dur),'-c:v','libx264','-preset','fast','-crf','19','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','final-hpb-v6.mp4'],w)
 run(['ffmpeg','-v','error','-i',str(w/'final-hpb-v6.mp4'),'-f','null','-'])
 print(slug,'nouvel habillage rendu',flush=True)
 compare(slug,w,dur)
 shutil.copy2(w/'final-hpb-v6.mp4',w/'final.mp4');shutil.copy2(w/'comparaison-hpb-v6.mp4',w/'comparaison.mp4')
 (w/'controle-hpb-v6.json').write_text(json.dumps(dict(version='HPB v6 présentation de référence',miroir=False,dedoublement=False,header='logo gauche et bandeau de série permanents',footer='nom du compte permanent',titre='blanc et jaune, bas gauche, premières 4 secondes',logo='version validée',audio='voix et timings conservés ensemble',validation='Décodage intégral réussi ; contrôle visuel à compléter.'),ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug,'comparaison v6 prête',flush=True)

if __name__=='__main__':
 for slug in sys.argv[1:] or ITEMS:main(slug)
