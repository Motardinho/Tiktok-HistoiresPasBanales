import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageEnhance,ImageFilter,ImageDraw
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
import miniatures_hpb as m
A=R/'assets/48-faid';P=R/'out/48-faid-evasion-helicoptere'
src=A/'miniature-source.jpg'
subprocess.run(['ffmpeg','-v','error','-y','-ss','28.5','-i',str(A/'rz7MsZ4KK54.mp4'),'-frames:v','1',str(src)],check=True,capture_output=True)
im=Image.open(src).convert('RGB').crop((720,45,1226,945)).resize((1080,1920),Image.Resampling.LANCZOS)
im.save(P/'miniature-photo-avant.jpg',quality=95)
im=ImageEnhance.Brightness(im).enhance(1.04)
im=ImageEnhance.Contrast(im).enhance(1.12)
im=ImageEnhance.Color(im).enhance(1.08)
im=im.filter(ImageFilter.UnsharpMask(radius=1.4,percent=45,threshold=3))
im.save(P/'miniature-photo-apres.jpg',quality=95)
bg=im.convert('RGBA');shade=Image.new('RGBA',bg.size);dr=ImageDraw.Draw(shade)
for y in range(850,1920):dr.line((0,y,1080,y),fill=(0,0,0,round(210*min(1,(y-850)/650))))
bg.alpha_composite(shade);bg.alpha_composite(m.logo_valide(),m.BOITE_LOGO[:2])
block,total=m.bloc_titre([m.N('ÉVASION',178),m.N('EN HÉLICO',150),m.N('FILMÉE|EN DIRECT',125)],'magazine')
halo=m.halo_sombre(block);layer=Image.new('RGBA',bg.size);layer.paste(halo,(m.MARGE_G-60-260,1530-total-60-260));bg.alpha_composite(layer)
layer=Image.new('RGBA',bg.size);layer.paste(block,(m.MARGE_G-60,1530-total-60));bg.alpha_composite(layer)
bg.convert('RGB').save(P/'miniature.png');bg.convert('RGB').resize((360,640)).save(P/'miniature-apercu.jpg',quality=95)
ref=Image.open(R/'identite/histoires-pas-banales/modeles-miniatures/09-pogba-magazine.png').convert('RGB')
cmp=Image.new('RGB',(720,640));cmp.paste(ref.resize((360,640)));cmp.paste(bg.convert('RGB').resize((360,640)),(360,0));cmp.save(P/'miniature-comparaison.jpg',quality=95)
cmp=Image.new('RGB',(720,640));cmp.paste(Image.open(P/'miniature-photo-avant.jpg').resize((360,640)));cmp.paste(im.resize((360,640)),(360,0));cmp.save(P/'miniature-reglages.jpg',quality=95)
(P/'miniature-manifeste.json').write_text(json.dumps(dict(modele='09-pogba-magazine.png',source='TF1 INFO rz7MsZ4KK54, 28.5 secondes, appareil dans la cour de Réau',recadrage=[720,45,1226,945],reglages=dict(luminosite=1.04,contraste=1.12,couleurs=1.08,netteté=dict(radius=1.4,percent=45,threshold=3)),logo='hpb-reference-propre-v1.png rendu du SVG validé',statut='à examiner'),ensure_ascii=False,indent=2),encoding='utf8')


