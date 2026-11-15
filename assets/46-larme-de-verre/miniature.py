import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
import miniatures_hpb as m
A=R/'assets/46-larme-de-verre';P=R/'out/46-larme-de-verre'
# Photogramme du vrai essai au marteau ; aucune image générée.
src=A/'miniature-source.jpg'
subprocess.run(['ffmpeg','-v','error','-y','-ss','69.6','-i',str(A/'xe-f4gokRBs.mp4'),'-frames:v','1',str(src)],check=True,capture_output=True)
im=Image.open(src).convert('RGB')
# L'action et la larme occupent la moitié supérieure, le bas porte le titre.
im=im.crop((880,480,1218,1080)).resize((1080,1920),Image.Resampling.LANCZOS)
im.save(P/'miniature-photo-avant.jpg',quality=96)
im=ImageEnhance.Contrast(im).enhance(1.14)
im=ImageEnhance.Color(im).enhance(1.28)
im=ImageEnhance.Brightness(im).enhance(1.03)
im=im.filter(ImageFilter.UnsharpMask(radius=2.2,percent=70,threshold=2))
im.save(P/'miniature-photo-apres.jpg',quality=96)
bg=im
over=Image.new('RGBA',(1080,1920));dr=ImageDraw.Draw(over)
for y in range(850,1920):dr.line((0,y,1080,y),fill=(23,19,15,round(160*min(1,(y-850)/800))))
bg=Image.alpha_composite(bg.convert('RGBA'),over)
bg.alpha_composite(m.logo_valide(),m.BOITE_LOGO[:2])
block,anchor=m.bloc_cale([m.N('CE VERRE CACHE'),m.P('UN POINT FAIBLE')],'jaune')
x,y=m.STYLES['jaune']['ancre'];bg.alpha_composite(block,(x-anchor[0],1410-anchor[1]))
bg.convert('RGB').save(P/'miniature.png')
bg.convert('RGB').resize((360,640)).save(P/'miniature-apercu.jpg',quality=96)
ref=Image.open(R/'identite/histoires-pas-banales/modeles-miniatures/10-fusee-yellow.png').convert('RGB')
compare=Image.new('RGB',(720,640));compare.paste(ref.resize((360,640)),(0,0));compare.paste(bg.convert('RGB').resize((360,640)),(360,0));compare.save(P/'miniature-comparaison.jpg',quality=96)
(P/'miniature-manifeste.json').write_text(json.dumps(dict(modele='10-fusee-yellow.png',moteur='miniatures_hpb.py, style jaune Impact',source='xe-f4gokRBs.mp4, 69.6 s',logo='hpb-reference-propre-v1.png issu du SVG validé',titre='CE VERRE CACHE UN POINT FAIBLE',statut='à examiner'),ensure_ascii=False,indent=2),encoding='utf8')
