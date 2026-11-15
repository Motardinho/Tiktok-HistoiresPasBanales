import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter,ImageFont
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
import miniatures_hpb as m
A=R/'assets/46-larme-de-verre';P=R/'out/46-larme-de-verre/variantes-miniatures';P.mkdir(exist_ok=True)
# Coordonnées des photogrammes source, sans transformation du sujet.
rows=[
 ('01-verre-transparent','lt-zvsGvtqg',0.8,(510,400,892,1080)),
 ('02-verre-polarise','lt-zvsGvtqg',70.3,(640,170,1152,1080)),
 ('03-verre-en-fusion','A6NUNroyUys',15.1,(1530,440,2498,2160)),
 ('04-rupture-au-ralenti','xe-f4gokRBs',162.1,(480,120,1020,1080)),
]
overlay=Image.new('RGBA',(1080,1920));overlay.alpha_composite(m.logo_valide(),m.BOITE_LOGO[:2])
block,anchor=m.bloc_cale([m.N('CE VERRE CACHE'),m.P('UN POINT FAIBLE')],'jaune');x,y=m.STYLES['jaune']['ancre'];overlay.alpha_composite(block,(x-anchor[0],1410-anchor[1]))
overlay.save(P/'habillage-identique.png')
manifest=[];sheet=Image.new('RGB',(1440,700),'#141414');dr=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(m.POPPINS),18)
for i,(name,source,at,box) in enumerate(rows):
 f=P/(name+'-source.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(A/(source+'.mp4')),'-frames:v','1',str(f)],check=True,capture_output=True)
 im=Image.open(f).convert('RGB').crop(box).resize((1080,1920),Image.Resampling.LANCZOS)
 im.save(P/(name+'-avant.jpg'),quality=95)
 im=ImageEnhance.Contrast(im).enhance(1.14);im=ImageEnhance.Color(im).enhance(1.28);im=ImageEnhance.Brightness(im).enhance(1.03);im=im.filter(ImageFilter.UnsharpMask(radius=2.2,percent=70,threshold=2))
 bg=im.convert('RGBA');veil=Image.new('RGBA',bg.size);vd=ImageDraw.Draw(veil)
 for yy in range(850,1920):vd.line((0,yy,1080,yy),fill=(23,19,15,round(160*min(1,(yy-850)/800))))
 bg=Image.alpha_composite(bg,veil);bg.convert('RGB').save(P/(name+'-photo-reglee.jpg'),quality=95)
 bg=Image.alpha_composite(bg,overlay).convert('RGB');bg.save(P/(name+'.png'));bg.resize((360,640)).save(P/(name+'-apercu.jpg'),quality=95)
 sheet.paste(bg.resize((360,640)),(i*360,45));dr.text((i*360+12,12),name.replace('-',' '),font=font,fill='white')
 manifest.append(dict(variante=name,source=source+'.mp4',seconde=at,recadrage=box,contraste=1.14,saturation=1.28,luminosite=1.03,netteté=dict(rayon=2.2,intensite=70,seuil=2),voile='identique à la miniature initiale',habillage='même calque RGBA pour toutes les variantes',note='Couleurs de la variante polarisée issues des filtres de laboratoire, non couleur naturelle du verre.'))
sheet.save(P/'planche.jpg',quality=96)
(P/'reglages-et-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(P/'planche.jpg')
