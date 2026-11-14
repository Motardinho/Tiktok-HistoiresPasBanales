"""Visuel carré du sondage YouTube « main d'Henry » (post du 18 novembre).

Photo réelle du match : but de Gallas, Kilbane réclame la main.
Nicolas Richoffer, CC BY-SA 4.0, Wikimedia Commons.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).parent
RACINE = ICI.parents[2]
PHOTO = ICI.parent / "photos" / "photo-gallas-but.jpg"
BEBAS = RACINE / "assets" / "fonts" / "BebasNeue-Regular.ttf"
POPPINS = RACINE / "assets" / "fonts" / "Poppins-ExtraBold.ttf"
TAILLE = 1080
JAUNE = (255, 214, 0)

img = Image.open(PHOTO).convert("RGB")
w, h = img.size
# carré calé à droite : Gallas (5), Henry (9) et Kilbane bras levés
img = img.crop((w - h, 0, w, h)).resize((TAILLE, TAILLE), Image.LANCZOS)

# dégradés sombres en haut et en bas pour la lisibilité
voile = Image.new("L", (1, TAILLE))
for y in range(TAILLE):
    haut = max(0, 1 - y / 330)
    bas = max(0, (y - 640) / 440)
    voile.putpixel((0, y), int(225 * max(haut, bas) ** 1.2))
voile = voile.resize((TAILLE, TAILLE))
img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, voile)

d = ImageDraw.Draw(img)


def centre(texte, y, police, couleur):
    largeur = d.textlength(texte, font=police)
    d.text(((TAILLE - largeur) / 2, y), texte, font=police, fill=couleur,
           stroke_width=3, stroke_fill=(0, 0, 0))


centre("18 NOVEMBRE 2009", 40, ImageFont.truetype(str(BEBAS), 92), JAUNE)
centre("FRANCE 1-1 IRLANDE · STADE DE FRANCE", 140,
       ImageFont.truetype(str(BEBAS), 50), (255, 255, 255))
centre("LA MAIN D'HENRY", 800, ImageFont.truetype(str(BEBAS), 130), (255, 255, 255))
centre("TU EN PENSES QUOI ?", 930, ImageFont.truetype(str(POPPINS), 54), JAUNE)

credit = "Photo : Nicolas Richoffer, CC BY-SA 4.0, Wikimedia Commons (recadrée)"
pc = ImageFont.truetype(str(POPPINS), 17)
d.text((TAILLE - d.textlength(credit, font=pc) - 18, TAILLE - 30), credit,
       font=pc, fill=(200, 200, 200))

img.save(ICI / "sondage-henry.jpg", quality=92)
print("ok", ICI / "sondage-henry.jpg")
