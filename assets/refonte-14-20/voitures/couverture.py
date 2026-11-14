# Couverture du dossier 14 (TOP 3 des voitures les plus rapides), à partir des vraies images des trois voitures.
# Usage : python assets/refonte-14-20/voitures/couverture.py [photos|illustration]  (depuis la racine du dépôt)
# photos : bandes de vraies images ; illustration : visuel IA fourni par Marc, rhabillé (texte d'origine masqué).
# Sources : vidéos officielles SSC North America, Bugatti et BYD (assets/sources-reelles), voir CREDITS.md du dossier.
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

root = Path.cwd()
src = root / 'assets/sources-reelles'
dossier = root / 'out/14-trois-records-voitures-vitesse'
tmp = dossier / 'couvertures'
tmp.mkdir(exist_ok=True)
POLICE = str(root / 'assets/fonts/Poppins-ExtraBold.ttf')
LOGO = root / 'identite/histoires-pas-banales/gabarits/symbole-video-contraste.png'
ENCRE, JAUNE, CREME, CORAIL = (18, 21, 28), (255, 226, 74), (247, 243, 233), (255, 60, 48)
W, H = 1080, 1920
PENTE = 0.07  # inclinaison commune des bandes et des cartouches

# nom : (vidéo, instant en s, découpe x0 y0 x1 y1 dans l'image 1920x1080)
PLANS = {
    'ssc': ('ssc-road.mp4', 22.5, (40, 150, 1440, 575)),             # SSC Tuatara, de face
    'bugatti': ('bugatti-record.mp4', 80.0, (230, 400, 1920, 941)),  # Chiron Super Sport 300+, vue plongeante
    'yangwang': ('yangwang-u9-xtreme-2025.mp4', 30.0, (330, 330, 1500, 1080)),  # Yangwang U9 Xtreme
}


def f(n):
    return ImageFont.truetype(POLICE, n)


def plan(nom, largeur, hauteur, ancre=0.5):
    video, t, boite = PLANS[nom]
    png = tmp / f'_source-{nom}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(src / video), '-frames:v', '1', str(png)], check=True)
    im = Image.open(png).convert('RGB').crop(boite)
    k = max(largeur / im.width, hauteur / im.height)
    im = im.resize((round(im.width * k) + 1, round(im.height * k) + 1), Image.Resampling.LANCZOS)
    x, y = (im.width - largeur) // 2, round((im.height - hauteur) * ancre)
    im = im.crop((x, y, x + largeur, y + hauteur))
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Color(im).enhance(1.25)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))


def penche(calque, k=0.16):
    # Faux italique : cisaillement horizontal du calque de texte.
    w, h = calque.size
    return calque.transform((w, h), Image.Transform.AFFINE, (1, k, -k * h / 2, 0, 1, 0), Image.Resampling.BICUBIC)


def texte(im, morceaux, taille, y, contour=0, ombre=True, lueur=None):
    # morceaux : [(texte, couleur)], centrés ensemble sur la largeur.
    police = f(taille)
    d = ImageDraw.Draw(im)
    total = sum(d.textlength(t, font=police) for t, _ in morceaux)
    calque = Image.new('RGBA', (W, taille * 2), (0, 0, 0, 0))
    c = ImageDraw.Draw(calque)
    x = (W - total) / 2
    for t, couleur in morceaux:
        c.text((x, taille * 0.3), t, font=police, fill=couleur, stroke_width=contour, stroke_fill=ENCRE)
        x += d.textlength(t, font=police)
    calque = penche(calque)
    pos = (0, y - round(taille * 0.3))
    if lueur:
        halo = Image.new('RGBA', calque.size, lueur + (0,))
        halo.putalpha(calque.getchannel('A').filter(ImageFilter.GaussianBlur(22)))
        im.alpha_composite(halo, pos)
    if ombre:
        noir = Image.new('RGBA', calque.size, (0, 0, 0, 0))
        noir.putalpha(calque.getchannel('A').filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .8)))
        im.alpha_composite(noir, (pos[0] + 6, pos[1] + 8))
    im.alpha_composite(calque, pos)


def cartouche(im, boite, couleur, k=0.16):
    x0, y0, x1, y1 = boite
    dx = (y1 - y0) * k / 2
    ombre = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ombre).polygon([(x0 + dx + 8, y0 + 10), (x1 + dx + 8, y0 + 10), (x1 - dx + 8, y1 + 10), (x0 - dx + 8, y1 + 10)], fill=(0, 0, 0, 150))
    im.alpha_composite(ombre.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).polygon([(x0 + dx, y0), (x1 + dx, y0), (x1 - dx, y1), (x0 - dx, y1)], fill=couleur)


def marque(im):
    by0 = 96
    ImageDraw.Draw(im).rounded_rectangle((80, by0, 1000, 200), radius=14, fill=ENCRE)
    logo = Image.open(LOGO).convert('RGBA').resize((118, 118), Image.Resampling.LANCZOS)
    pm = f(48)
    d = ImageDraw.Draw(im)
    l1, l2 = d.textlength('HISTOIRES ', font=pm), d.textlength('PAS BANALES', font=pm)
    x = (W - (100 + l1 + l2)) / 2
    im.alpha_composite(logo, (round(x) - 12, by0 - 6))
    d.text((x + 100, by0 + 18), 'HISTOIRES ', font=pm, fill=CREME)
    d.text((x + 100 + l1, by0 + 18), 'PAS BANALES', font=pm, fill=JAUNE)


def bas_sombre(im, debut=1700, force=170):
    voile = Image.new('L', (W, H), 0)
    dv = ImageDraw.Draw(voile)
    for y in range(debut, H):
        dv.line((0, y, W, y), fill=int(force * (y - debut) / (H - debut)))
    return Image.composite(Image.new('RGBA', im.size, ENCRE + (255,)), im, voile)


def couverture_photos():
    im = Image.new('RGBA', (W, H), ENCRE + (255,))
    # Fond du haut : la route du record, floutée et assombrie, pour porter le titre.
    fond = plan('bugatti', W, 1000).filter(ImageFilter.GaussianBlur(26))
    fond = ImageEnhance.Brightness(fond).enhance(.38)
    fond = ImageChops.multiply(fond, Image.new('RGB', fond.size, (150, 185, 255)))
    im.paste(fond, (0, 0))
    # Trois bandes inclinées, une vraie image par voiture.
    Y0, PAS = 985, 245
    d = round(W * PENTE / 2)
    bandes = [('ssc', Y0, Y0 + PAS, .5), ('bugatti', Y0 + PAS, Y0 + 2 * PAS, 1.), ('yangwang', Y0 + 2 * PAS, H + 60, .0)]
    for nom, y0, y1, ancre in bandes:
        photo = plan(nom, W, y1 - y0 + 2 * d, ancre)
        masque = Image.new('L', photo.size, 0)
        ImageDraw.Draw(masque).polygon([(0, 2 * d), (W, 0), (W, y1 - y0), (0, y1 - y0 + 2 * d)], fill=255)
        im.paste(photo, (0, y0 - d), masque)
    trait = ImageDraw.Draw(im)
    for i in range(3):
        y = Y0 + i * PAS
        trait.polygon([(0, y + d - 5), (W, y - d - 5), (W, y - d + 5), (0, y + d + 5)], fill=JAUNE)
    im = bas_sombre(im)
    marque(im)
    cartouche(im, (215, 262, 865, 440), CORAIL)
    texte(im, [('TOP 3', CREME)], 158, 262)
    texte(im, [('VOITURES', CREME)], 152, 440, contour=8)
    cartouche(im, (70, 622, 1010, 738), CREME)
    texte(im, [('LES PLUS RAPIDES', ENCRE)], 86, 624, ombre=False)
    # Chiffre choc : 503,17 km/h le 1er novembre 2026 (FIA, BYD, Guinness), cf. verification.md.
    texte(im, [('500+ ', CREME), ('KM/H', CORAIL)], 138, 742, contour=6, lueur=(90, 190, 255))
    texte(im, [('NOUVEAU RECORD 2026', JAUNE)], 44, 880, contour=4)
    return im


def couverture_illustration():
    # Visuel IA d'origine (572x1024) : on garde la scène des trois voitures, on masque tout le texte incrusté.
    origine = Image.open(root / 'assets/refonte-14-20/voitures/couverture-illustration-source.webp').convert('RGB')
    scene = origine.resize((W, round(origine.height * W / origine.width)), Image.Resampling.LANCZOS)
    scene = scene.crop((0, scene.height - H, W, scene.height)) if scene.height >= H else scene.resize((W, H), Image.Resampling.LANCZOS)
    scene = scene.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    # Fond du haut : le ciel de la scène, étiré, flouté et assombri (aucun texte d'origine lisible).
    haut = origine.crop((0, 600, origine.width, 680)).resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    haut = ImageEnhance.Brightness(haut).enhance(.45)
    FIN_TEXTE, FONDU = 1165, 90  # le texte incrusté s'arrête vers y=615/1024
    masque = Image.new('L', (W, H), 0)
    dm = ImageDraw.Draw(masque)
    for y in range(FIN_TEXTE, H):
        dm.line((0, y, W, y), fill=min(255, int(255 * (y - FIN_TEXTE) / FONDU)))
    im = Image.composite(scene, haut, masque).convert('RGBA')
    im = bas_sombre(im, 1760, 150)
    marque(im)
    cartouche(im, (190, 268, 890, 470), CORAIL)
    texte(im, [('TOP 3', CREME)], 180, 268)
    texte(im, [('VOITURES', CREME)], 166, 478, contour=8)
    cartouche(im, (55, 680, 1025, 808), CREME)
    texte(im, [('LES PLUS RAPIDES', ENCRE)], 94, 683, ombre=False)
    texte(im, [('500+ ', CREME), ('KM/H', CORAIL)], 150, 822, contour=6, lueur=(90, 190, 255))
    texte(im, [('NOUVEAU RECORD 2026', JAUNE)], 50, 978, contour=4)
    return im


mode = sys.argv[1] if len(sys.argv) > 1 else 'photos'
im = (couverture_illustration if mode == 'illustration' else couverture_photos)()
sortie = dossier / ('couverture-tiktok-illustration.jpg' if mode == 'illustration' else 'couverture-tiktok.jpg')
im.convert('RGB').save(sortie, quality=93)
print('Couverture :', sortie)
