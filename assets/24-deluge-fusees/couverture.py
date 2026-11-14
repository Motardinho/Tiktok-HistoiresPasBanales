# Couvertures « décalées » du post 24 (TikTok et YouTube), à partir d'images NASA réelles.
# Usage : python assets/24-deluge-fusees/couverture.py  (depuis la racine du dépôt)
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

root = Path.cwd()
a = root / 'assets/24-deluge-fusees'
out = root / 'out/24-deluge-fusees/couvertures'
out.mkdir(exist_ok=True)
font = str(root / 'assets/fonts/Poppins-ExtraBold.ttf')
JAUNE, BLANC = (255, 222, 47), (250, 248, 240)

# source, instant (s), x de la découpe, hauteur utile (évite le chrono NASA en bas)
SOURCES = {
    'fusee': ('lancement-plateforme.mp4', 30.5, 440, 1040),  # Artemis I, 16 nov. 2022, T-5,8 s
    'drone': ('deluge-drone-2023.mp4', 28.0, 656, 1080),      # essai sans fusée, 24 oct. 2023
}
COUVERTURES = [
    ('A-ils-noient-leur-fusee', 'fusee', [('ILS NOIENT', BLANC), ('LEUR FUSÉE ?!', JAUNE)]),
    ('B-robinet', 'fusee', [('QUI A OUBLIÉ', BLANC), ('DE FERMER', BLANC), ('LE ROBINET ?', JAUNE)]),
    ('C-douche-1500-tonnes', 'drone', [('UNE DOUCHE', BLANC), ('DE 1 500', JAUNE), ('TONNES ?!', JAUNE)]),
]


def image_source(nom):
    f, t, x, h = SOURCES[nom]
    png = out / f'_source-{nom}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(a / f), '-frames:v', '1', str(png)], check=True)
    im = Image.open(png).convert('RGB')
    w = round(h * 9 / 16)
    return im.crop((x, 0, x + w, h)).resize((1080, 1920), Image.Resampling.LANCZOS)


def image_large(nom):
    # Plan large (fusée + torrent) en bas, même plan flouté et assombri en fond pour le texte.
    f, t, x, h = SOURCES[nom]
    im = Image.open(out / f'_source-{nom}.png').convert('RGB')
    net = im.crop((380, 0, 1460, 1040))
    fond = im.crop((560, 0, 1145, 1040)).resize((1080, 1920), Image.Resampling.LANCZOS)
    fond = fond.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * .45))
    fond.paste(net, (0, 760))
    return fond


def composer(nom, src, lignes):
    if src == 'fusee':
        image_source(src)
        im = image_large(src)
        centre = 470
    else:
        im = image_source(src)
        centre = 760
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    # Voile sombre derrière le texte pour la lisibilité (zone 3:4 centrale, visible dans la grille du profil).
    voile = Image.new('L', im.size, 0)
    d = ImageDraw.Draw(voile)
    for y in range(centre - 380, centre + 420):
        d.line((0, y, 1080, y), fill=int(150 * max(0, 1 - abs(y - centre) / 420)))
    im = Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, voile)
    d = ImageDraw.Draw(im)
    taille = 118
    f = ImageFont.truetype(font, taille)
    while max(d.textlength(t, font=f) for t, _ in lignes) > 960:
        taille -= 4
        f = ImageFont.truetype(font, taille)
    pas = int(taille * 1.12)
    y = centre - pas * len(lignes) // 2
    for texte, couleur in lignes:
        d.text((60, y), texte, font=f, fill=couleur, stroke_width=9, stroke_fill=(10, 10, 10))
        y += pas
    im.save(out / f'{nom}.jpg', quality=93)


for nom, src, lignes in COUVERTURES:
    composer(nom, src, lignes)
print('Couvertures :', out)
