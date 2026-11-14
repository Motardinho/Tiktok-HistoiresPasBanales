import json,importlib.util,shutil,hashlib
from pathlib import Path
from datetime import datetime,timezone,timedelta
from PIL import Image,ImageOps,ImageDraw,ImageEnhance
import resvg_py
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/45-origine-black-friday';P=ROOT/'out/45-origine-black-friday';T=ROOT/'identite/histoires-pas-banales/gabarits-miniatures'
spec=importlib.util.spec_from_file_location('hpb_template',T/'render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
old=Image.open(A/'miniature-police-source.png').convert('RGB');old=old.crop((35,25,680,455));old=ImageOps.grayscale(old).convert('RGB');old=ImageEnhance.Contrast(old).enhance(1.12)
modern=Image.open(A/'1980s-1990s-americas-shopping-holiday-is-born.jpg').convert('RGB')
# Deux sources documentaires distinctes, séparation inclinée comme le modèle magazine.
left=ImageOps.fit(old,(660,1250),centering=(.34,.35));right=ImageOps.fit(modern,(660,1250),centering=(.48,.35))
bg=Image.new('RGB',(1080,1920),'#11151d');bg.paste(left,(0,100));bg.paste(right,(470,100))
mask=Image.new('L',(1080,1920));md=ImageDraw.Draw(mask);md.polygon([(0,0),(660,0),(525,1350),(470,1920),(0,1920)],fill=255)
leftfull=Image.new('RGB',(1080,1920),'#11151d');leftfull.paste(left,(0,100));bg=Image.composite(leftfull,bg,mask)
over=Image.new('RGBA',(1080,1920));dr=ImageDraw.Draw(over)
for y in range(1920):
 alpha=int(220*min(1,max(0,(y-820)/850)))
 if y<240:alpha=max(alpha,int(100*(240-y)/240))
 dr.line((0,y,1080,y),fill=(8,12,20,alpha))
dr.line([(645,150),(500,1640)],fill=(255,228,71,255),width=7)
bg=Image.alpha_composite(bg.convert('RGBA'),over).convert('RGB');bg.save(A/'miniature-fond.jpg',quality=96)
c=json.loads((T/'magazine.json').read_text(encoding='utf8'))
for row in c['rows']:row['alphabet']='lot';row['compose']=True
c['rows'][0].update(text='BLACK FRIDAY',x=100,y=968,w=880,h=215)
c['rows'][1].update(text='LE CAUCHEMAR',x=120,y=1216,w=830,h=106,polygon=[[100,1195],[970,1195],[970,1343],[100,1343]])
c['rows'][2].update(text='DES',x=104,y=1370,w=172,h=105)
c['rows'][3].update(text='FLICS',x=310,y=1358,w=400,h=155)
(A/'miniature-config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
s=r.svg(c,A/'miniature-fond.jpg').replace('x="800" y="24" width="240"','x="800" y="234" width="240"')
(P/'miniature.svg').write_text(s,encoding='utf8');(P/'miniature.png').write_bytes(resvg_py.svg_to_bytes(svg_string=s))
im=Image.open(P/'miniature.png').convert('RGB');im.resize((360,640)).save(P/'miniature-apercu.jpg',quality=95)
grid=im.crop((0,240,1080,1680));grid.resize((360,480)).save(P/'miniature-grille.jpg',quality=95)
ref=Image.open(ROOT/'identite/histoires-pas-banales/modeles-miniatures/09-pogba-magazine.png').convert('RGB');sheet=Image.new('RGB',(720,640));sheet.paste(ref.resize((360,640)),(0,0));sheet.paste(im.convert('RGB').resize((360,640)),(360,0));sheet.save(P/'miniature-comparaison.jpg',quality=95)
for v in ['videos','photos']:shutil.copy2(P/'miniature.png',P/v/'miniature.png')
manifest=dict(date='2026-11-14',titre=d['titre_fixe'] if (d:=json.loads((P/'histoire.json').read_text(encoding='utf8'))) else '',modele='09-pogba-magazine.png',lettres='tracés du modèle et compléments vectoriels du lot existants, sans nouvelle police',logo='hpb-reference-propre-v1.svg, x=800 y=234 taille=240',sources=['0Cs2xjzAJTU.mp4, 395 s, police Philadelphie donnée pour 1960 par le diffuseur, convertie en gris','Tasos Katopodis / Getty Images, photo de foule reproduite par HISTORY, Black Friday contemporain'],statut='créée, à contrôler visuellement',publication=False)
(P/'miniature-manifeste.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Miniature et aperçus créés')


