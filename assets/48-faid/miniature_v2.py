"""Miniature v2 du dossier 48 : vidéosurveillance de l'hélicoptère posé dans la cour de Réau (TF1 INFO, 24 s)
+ photo de l'avis de recherche de Faïd (BFMTV, 11 s). Style magazine (maquette 09), logo validé en haut à droite.
Usage : python assets/48-faid/miniature_v2.py [A|B]"""
import sys, json, subprocess
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
R = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R))
import miniatures_hpb as m

A = R / 'assets/48-faid'; P = R / 'out/48-faid-evasion-helicoptere'
TITRES = {'A': 'FILMÉE|PAR UN DÉTENU', 'B': 'SOUS LES|CAMÉRAS'}
v = (sys.argv[1] if len(sys.argv) > 1 else 'A').upper()


def cadre(video, t, nom):
    f = A / nom
    if not f.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(A / video), '-frames:v', '1', str(f)], check=True)
    return Image.open(f).convert('RGB')


# Fond : vidéosurveillance, hélicoptère au centre, murs de la prison autour.
cctv = cadre('rz7MsZ4KK54.mp4', 24, 'miniature-v2-cctv.jpg')
S = 1.6
x0, y0 = 745, 275
haut = cctv.crop((x0, y0, x0 + round(1080 / S), y0 + round(1140 / S))).resize((1080, 1140), Image.Resampling.LANCZOS)
haut = haut.filter(ImageFilter.MedianFilter(3))
haut = ImageOps.autocontrast(haut.convert('L'), cutoff=1).convert('RGB')
haut = ImageEnhance.Contrast(haut).enhance(1.15)
haut = haut.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))
bg = Image.new('RGBA', (1080, 1920), (5, 6, 14, 255))
bg.paste(haut, (0, 0))
fondu = Image.new('RGBA', bg.size); d = ImageDraw.Draw(fondu)
for y in range(900, 1140):
    d.line((0, y, 1080, y), fill=(5, 6, 14, round(255 * ((y - 900) / 240) ** 1.4)))
bg.alpha_composite(fondu)

# Photo de l'avis de recherche, en fiche penchée en haut à gauche.
avis = cadre('99EQ3yqL8Pg.mp4', 11, 'miniature-v2-avis.jpg')
photo = avis.crop((297, 155, 637, 405)).resize((270, 199), Image.Resampling.LANCZOS)
photo = photo.filter(ImageFilter.UnsharpMask(radius=1.5, percent=50, threshold=2))
f_police = m.police(m.IMPACT, 40)
while ImageDraw.Draw(Image.new('L', (1, 1))).textlength('AVIS DE RECHERCHE', font=f_police) > 250:
    f_police = m.police(m.IMPACT, f_police.size - 1)
fiche = Image.new('RGBA', (300, 290), (250, 250, 247, 255))
fiche.paste(photo, (15, 15))
df = ImageDraw.Draw(fiche)
df.rectangle((15, 222, 285, 275), fill=m.rgb('#FA3332'))

df.text((150, 248), 'AVIS DE RECHERCHE', font=f_police, fill='#FFFFFF', anchor='mm')
fiche = fiche.rotate(-5, resample=Image.Resampling.BICUBIC, expand=True)
bg.alpha_composite(m.ombre_portee(fiche, decalage=(8, 14), flou=14, force=170), (44 - 40, 250 - 40))
bg.alpha_composite(fiche, (44, 250))

bg.alpha_composite(m.logo_valide(), m.BOITE_LOGO[:2])

block, total = m.bloc_titre([m.N('ÉVASION', 160), m.N('EN HÉLICO', 135), m.N(TITRES[v], 112)], 'magazine')
bas = 1530
halo = m.halo_sombre(block); layer = Image.new('RGBA', bg.size)
layer.paste(halo, (m.MARGE_G - 60 - 260, bas - total - 60 - 260)); bg.alpha_composite(layer)
layer = Image.new('RGBA', bg.size); layer.paste(block, (m.MARGE_G - 60, bas - total - 60))
titre = m.boite_opaque(layer); bg.alpha_composite(layer)

im = bg.convert('RGB')
lb = m.boite_opaque(m.logo_valide()); lx, ly = m.BOITE_LOGO[:2]
m.ZONES[48] = {'logo': (lx + lb[0], ly + lb[1], lx + lb[2], ly + lb[3]), 'titre': titre}
defauts = m.hors_zone(48)
m.controle_zones(im).save(P / f'miniature-v2{v}-zones.jpg', quality=88)
print('titre', titre, 'défauts', defauts or 'aucun')
im.save(P / f'miniature-v2{v}.png')
ref = Image.open(P / 'miniature.png').convert('RGB')
cmp = Image.new('RGB', (720, 640)); cmp.paste(ref.resize((360, 640))); cmp.paste(im.resize((360, 640)), (360, 0))
cmp.save(P / f'miniature-v2{v}-comparaison.jpg', quality=95)
