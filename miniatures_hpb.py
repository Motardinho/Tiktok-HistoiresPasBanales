# Miniatures HPB v4 : fichiers séparés de la vidéo. Bulle « HPB » (lettres découpées) seule en haut à droite,
# titre dans un des cinq styles de STYLES, choisi par dossier.
# Usage, depuis la racine du dépôt :
#   python miniatures_hpb.py            -> toutes les miniatures + planche
#   python miniatures_hpb.py 31 43      -> seulement ces dossiers
# Les fonds sont de vraies images (plans d'ouverture sans titre), rangées dans assets/miniatures-v2/fonds/.
# Rien n'est généré par IA : recadrage, étalonnage et texte seulement.
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parent
FONDS = ROOT / 'assets/miniatures-v2/fonds'
SORTIE = ROOT / 'out/miniatures-v4'  # v2 (contour) et v3 (plaques bleues partout) restent dans leurs dossiers
LOGO = ROOT / 'identite/histoires-pas-banales/logos/symbole-couleur.png'
POPPINS = ROOT / 'assets/fonts/Poppins-ExtraBold.ttf'
IMPACT = Path('C:/Windows/Fonts/impact.ttf')
BEBAS = ROOT / 'assets/fonts/BebasNeue-Regular.ttf'
ARIAL_BLACK = Path('C:/Windows/Fonts/ariblk.ttf')
FRANKLIN = Path('C:/Windows/Fonts/framd.ttf')
SEGOE_BLACK = Path('C:/Windows/Fonts/seguibl.ttf')
# Polices libres (Google Fonts, licence OFL dans assets/fonts/licences), choisies le 14 novembre 2026 parce qu'elles
# collent le mieux aux lettres des maquettes, qui ont été dessinées par ImageGen et ne sortent d'aucune vraie police.
GOLDMAN = ROOT / 'assets/fonts/Goldman-Bold.ttf'
RUSSO = ROOT / 'assets/fonts/RussoOne-Regular.ttf'
SQUADA = ROOT / 'assets/fonts/SquadaOne-Regular.ttf'
EPAULES_900 = (ROOT / 'assets/fonts/BigShouldersDisplay-Variable.ttf', 900)
EPAULES_800 = (ROOT / 'assets/fonts/BigShouldersDisplay-Variable.ttf', 800)
MONTSERRAT_900 = (ROOT / 'assets/fonts/Montserrat-Variable.ttf', 900)

L, H = 1080, 1920
ENCRE, JAUNE, PAPIER, CORAIL = '#12151C', '#FFE24A', '#F7F3E9', '#FF624E'
BLANC = '#FFFFFF'
PENTE = 0.20          # inclinaison des plaques et de l'italique
MARGE_G = 64          # bord gauche du bloc titre (au pied de la dernière ligne)
LARGEUR_MAX = 955     # largeur maximale d'une ligne, plaque comprise
# TikTok recadre la grille du profil en 3:4 : seules les lignes 240 à 1680 restent visibles.
HAUT_BANDEAU = 262
BAS_TITRE = 1440


def rgb(c, a=255):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def police(chemin, taille):
    if isinstance(chemin, tuple):  # police variable : (fichier, graisse)
        f = ImageFont.truetype(str(chemin[0]), taille)
        f.set_variation_by_axes([chemin[1]])
        return f
    return ImageFont.truetype(str(chemin), taille)


# ---------------------------------------------------------------- fond
def fond_portrait(photo, echelle, haut, cx=0.5):
    """Portrait posé sous le bandeau : la photo nette à l'échelle voulue, sur elle-même floutée et assombrie."""
    e = max(L / photo.width, H / photo.height)
    flou = photo.resize((round(photo.width * e), round(photo.height * e)), Image.Resampling.LANCZOS)
    flou = flou.crop(((flou.width - L) // 2, 0, (flou.width - L) // 2 + L, H))
    flou = ImageEnhance.Brightness(flou.filter(ImageFilter.GaussianBlur(45))).enhance(0.55)
    net = photo.resize((round(photo.width * echelle), round(photo.height * echelle)), Image.Resampling.LANCZOS)
    masque = Image.new('L', net.size, 255)
    d = ImageDraw.Draw(masque)
    for i in range(90):  # fondu en haut et en bas
        d.line((0, i, net.width, i), fill=round(255 * i / 90))
        d.line((0, net.height - 1 - i, net.width, net.height - 1 - i), fill=round(255 * i / 90))
    flou.paste(net, (round(L / 2 - net.width * cx), haut), masque)
    return flou


def preparer_fond(src, zoom=1.0, centre=(0.5, 0.5), miroir=False, contraste=1.14, saturation=1.28,
                  luminosite=1.0, voile_bas=0.78, voile_haut=0.45, portrait=None, vignette=True):
    im = Image.open(src).convert('RGB')
    if portrait:
        im = fond_portrait(im, **portrait)
    if miroir:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    # Remplir 1080x1920 puis zoomer autour du point d'intérêt.
    e = max(L / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * e), round(im.height * e)), Image.Resampling.LANCZOS)
    x = min(max(round(im.width * centre[0] - L / 2), 0), im.width - L)
    y = min(max(round(im.height * centre[1] - H / 2), 0), im.height - H)
    im = im.crop((x, y, x + L, y + H))
    im = ImageEnhance.Contrast(im).enhance(contraste)
    im = ImageEnhance.Color(im).enhance(saturation)
    im = ImageEnhance.Brightness(im).enhance(luminosite)
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    # Voiles encre : en haut pour le bandeau, en bas pour le titre. Le sujet reste clair au milieu.
    masque = Image.new('L', (1, H))
    for yy in range(H):
        haut = max(0.0, 1 - yy / 520) ** 1.6 * voile_haut
        bas = max(0.0, (yy - 820) / (H - 820)) ** 1.25 * voile_bas
        masque.putpixel((0, yy), round(255 * min(1.0, haut + bas)))
    masque = masque.resize((L, H))
    im.paste(Image.new('RGB', (L, H), ENCRE), (0, 0), masque)
    # Vignette légère.
    v = Image.new('L', (L, H), 0)
    ImageDraw.Draw(v).ellipse((-260, -200, L + 260, H + 200), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    sombre = ImageEnhance.Brightness(im).enhance(0.62)
    return (Image.composite(im, sombre, v) if vignette else im).convert('RGBA')


MAQUETTES = ROOT / 'out/miniatures-10-variantes-2026-11-12'


def etalonner(im, maquette, titre):
    """Donne au fond les réglages photo de la maquette (luminosité, contraste, couleurs) : pour chaque canal, la
    courbe qui fait coïncider les histogrammes des deux images, mesurés hors du bandeau du haut et hors des rangées
    du titre (titre = première et dernière rangée du titre sur la maquette). Même méthode que fond_31_cagoule.py."""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    ref = np.asarray(Image.open(MAQUETTES / maquette).convert('RGB').resize((L, H)))
    rangs = np.r_[375:titre[0] - 10, titre[1] + 10:H - 20]
    sortie = np.empty_like(a)
    for c in range(3):
        src = np.clip(a[rangs, :, c], 0, 255).astype(np.uint8)
        cs = np.cumsum(np.bincount(src.ravel(), minlength=256)) / src.size
        cr = np.cumsum(np.bincount(ref[rangs, :, c].ravel(), minlength=256)) / src.size
        courbe = np.interp(cs, cr, np.arange(256))
        courbe = np.convolve(np.pad(courbe, 8, mode='edge'), np.ones(17) / 17, mode='valid')  # courbe lissée
        sortie[..., c] = np.interp(a[..., c], np.arange(256), np.maximum.accumulate(courbe))
    out = Image.fromarray(np.clip(sortie, 0, 255).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=2.0, percent=60, threshold=2)).convert('RGBA')


# ---------------------------------------------------------------- bandeau de chaîne
def bandeau_chaine():
    """Bandeau encre sur toute la largeur : le symbole de la photo de profil, puis le nom de la chaîne sur une ligne."""
    h, filet, marge, ecart, h_logo = 156, 0, 36, 28, 116
    bord = 44  # marge laissée de chaque côté : le bandeau ne touche pas les bords
    larg_bande = L - 2 * bord
    logo = Image.open(LOGO).convert('RGBA')
    logo = logo.crop(logo.getbbox())
    logo = logo.resize((round(logo.width * h_logo / logo.height), h_logo), Image.Resampling.LANCZOS)
    m1, m2 = 'HISTOIRES ', 'PAS BANALES'
    dispo = larg_bande - 2 * marge - logo.width - ecart
    taille = 90
    while police(POPPINS, taille).getlength(m1 + m2) > dispo:
        taille -= 1
    f = police(POPPINS, taille)
    bande = Image.new('RGBA', (larg_bande, h), rgb(ENCRE, 245))
    d = ImageDraw.Draw(bande)
    # Logo et nom centrés ensemble dans la largeur.
    larg = logo.width + ecart + round(f.getlength(m1 + m2))
    x = (larg_bande - larg) // 2
    bande.alpha_composite(logo, (x, (h - filet - h_logo) // 2 + 3))
    x += logo.width + ecart
    bb = f.getbbox('H')
    y = (h - filet - (bb[3] - bb[1])) // 2 - bb[1]
    d.text((x, y), m1, font=f, fill=PAPIER)
    d.text((x + f.getlength(m1), y), m2, font=f, fill=JAUNE)
    return bande


def ombre_portee(calque, decalage=(0, 10), flou=16, force=150):
    a = calque.getchannel('A').point(lambda v: v * force // 255)
    o = Image.new('RGBA', calque.size, rgb(ENCRE, 0))
    o.putalpha(a)
    grand = Image.new('RGBA', (calque.width + 80, calque.height + 80), (0, 0, 0, 0))
    grand.alpha_composite(o, (40 + decalage[0], 40 + decalage[1]))
    return grand.filter(ImageFilter.GaussianBlur(flou))


def halo_sombre(calque, serre=(7, 9, 250), large=(40, 90, 150), couleur='#05060E'):
    """Fond noirci derrière le titre, comme sur la maquette 09 : une bande presque noire derrière chaque ligne (elle
    bouche l'intérieur des lettres et l'espace entre elles, sans dessiner un contour), plus un voile large et léger
    qui assombrit la photo autour. Chaque couche : (dilatation, flou, opacité sur 255).
    L'image rendue déborde de 260 px de chaque côté."""
    marge = 260
    a = calque.getchannel('A').point(lambda v: 255 if v > 128 else 0)
    plein = Image.new('L', a.size, 0)
    d = ImageDraw.Draw(plein)
    for y in range(a.height):  # chaque rangée : remplie du premier au dernier pixel d'encre
        bb = a.crop((0, y, a.width, y + 1)).getbbox()
        if bb:
            d.line((bb[0], y, bb[2] - 1, y), fill=255)
    base = Image.new('L', (calque.width + 2 * marge, calque.height + 2 * marge), 0)
    base.paste(plein, (marge, marge))
    total = Image.new('L', base.size, 0)
    for dilat, flou, force in (serre, large):
        c = base.filter(ImageFilter.MaxFilter(2 * dilat + 1)).filter(ImageFilter.GaussianBlur(flou))
        total = ImageChops.lighter(total, c.point(lambda v: v * force // 255))
    o = Image.new('RGBA', base.size, rgb(couleur, 0))
    o.putalpha(total)
    return o


# ---------------------------------------------------------------- titre
# Cinq styles de titre retenus par Marc le 13 novembre 2026 (pop, course, autocollant, magazine, jaune), repris des maquettes de out/miniatures-10-variantes-2026-11-12 (typographie refaite ici,
# sans génération d'image). Chaque style donne (encre, fond) pour la première ligne, les lignes du milieu et la
# dernière ; fond None = texte nu avec ombre dure.
BLEU, ROSE, ROUGE, VIOLET = '#1A1FD8', '#FF1F8E', '#E8141C', '#7A2BFF'
STYLES = {
    # Les quatre styles « calés » reprennent au pixel les maquettes 06, 07, 08 et 10 (1080x1920). Tout est en
    # proportion de la hauteur des capitales (cap) : etire = largeur des lettres, gras = épaississement,
    # pente_texte = italique, pente = biais de la plaque, pad_* = marges de la plaque, espace = blanc entre les mots.
    # dx, avant, dx_texte, ombres et socles sont en pixels, pour la taille de la maquette.
    # Maquette 06 : plaques bleues #0014BF puis jaune #FCEF02, biais 0,39, ombre rose #FA0170 décalée de (-32, 28),
    # « TOP 10 » en italique large, les deux autres lignes droites, barre jaune au pied de la première plaque.
    'pop': dict(cale=True, ancre=(88, 1454), pente=0.39, ombre=('#FA0170', -32, 28), accent='#FCEF02',
                debut=dict(fonte=GOLDMAN, cap=91, etire=1.10, gras=0.018, pente_texte=0.24, espace=0.46, encre='#FAFAFC',
                           fond='#0014BF', pad_x=0.62, pad_haut=0.235, pad_bas=0.175, dx=12, dx_texte=4),
                milieu=dict(fonte=RUSSO, cap=73, etire=1.225, gras=0.018, pente_texte=0.0, espace=0.445, encre='#FAFAFC',
                            fond='#0014BF', pad_x=0.67, pad_haut=0.23, pad_bas=0.30, dx=14, dx_texte=6),
                fin=dict(fonte=RUSSO, cap=67, etire=0.975, gras=0.018, pente_texte=0.03, espace=0.375, encre='#04070E',
                         fond='#FCEF02', pad_x=0.68, pad_haut=0.28, pad_bas=0.31, avant=2, dx_texte=-1)),
    # Maquette 07 : Squada One et Big Shoulders Display en italique 0,44 ; plaques rouges #E61B02 au biais 0,49, ombre marine décalée de
    # (24, 24) ; ligne du milieu sans plaque, avec la même ombre marine.
    'course': dict(cale=True, ancre=(56, 1302), fonte=SQUADA, gras=0, pente_texte=0.44, pente=0.49, encre='#FCFCFC',
                   ombre=('#050A26', 24, 24), ombre_texte=('#050A26', 11, 8),
                   debut=dict(cap=91, etire=1.46, espace=0.47, fond='#E61B02', pad_x=0.74, pad_haut=0.17, pad_bas=0.20, dx=12,
                              dx_texte=6),
                   milieu=dict(fonte=EPAULES_900, cap=87, etire=1.173, espace=0.37, fond=None, avant=10, dx=42),
                   fin=dict(cap=86, etire=1.0, espace=0.38, fond='#E61B02', pad_x=0.40, pad_haut=0.21, pad_bas=0.21, avant=14,
                            dx_texte=0)),
    # Maquette 08 : lettres blanches à gros contour noir et relief vers le bas à droite, penchées de 0,85° ; plaque
    # jaune #FCDB18 penchée de 2,3° sur un socle violet puis noir.
    'autocollant': dict(cale=True, ancre=(84, 1413), rotation=0.85, pente_texte=0.14, contour=0.068, relief=(0.12, 0.12),
                        debut=dict(fonte=MONTSERRAT_900, cap=127, etire=0.857, gras=0, espace=0.25, encre='#FDFDFD', fond=None, dx=128),
                        milieu=dict(fonte=MONTSERRAT_900, cap=72, etire=0.896, gras=0, espace=0.43, encre='#FDFDFD', fond=None,
                                    avant=14, dx=53),
                        fin=dict(fonte=SEGOE_BLACK, cap=84, etire=0.925, gras=0.013, pente_texte=0.19, pente=0.2, encre='#050505',
                                 fond='#FCDB18', pad_x=0.38, pad_haut=0.25, pad_bas=0.345, avant=22, rot=1.45, dx_texte=6,
                                 socle=[('#000000', 4, 20, 0), ('#9904E7', 0, 13, 0.5)], contour=0, relief=None)),
    # Maquette 10 : Impact resserré en italique 0,21 sur deux plaques jaunes #FBD400 au biais 0,22, le tout penché
    # de 5,94° ; la seconde plaque a un bord droit plus couché ; ombre noire floue sous chaque plaque.
    'jaune': dict(cale=True, ancre=(68, 1334), rotation=5.94, fonte=IMPACT, gras=0, etire=0.82, pente_texte=0.21, pente=0.22,
                  encre='#0A0A0A', ombre_floue=('#000000', 5, 13, 5, 235),
                  debut=dict(cap=95, espace=0.30, fond='#FBD400', pad_x=0.285, pad_haut=0.20, pad_bas=0.22, dx=31, dx_texte=-12),
                  milieu=dict(cap=95, espace=0.30, fond='#FBD400', pad_x=0.285, pad_haut=0.20, pad_bas=0.22, avant=17, dx=31, dx_texte=-12),
                  fin=dict(cap=141, etire=0.80, espace=0.245, dx_texte=6, fond='#FBD400', pad_x=0.34, pad_haut=0.16, pad_bas=0.19, avant=17, pente_d=0.375)),
    # Maquette 09, mesurée au pixel (1080x1920) : POGBA capitales de 220 px, fûts de 43 ; plaque rouge #FA3332 de
    # 147 px qui dépasse de 16 à gauche, mot en Arial Black ; dernière ligne jaune #FBF94E de 159 px, fûts de 25,
    # amorce blanche de 107 px posée 12 px plus bas, à 24 px du corps ; 11 à 14 px entre les lignes ; aucune ombre dure.
    'magazine': dict(fonte=IMPACT, echelle=1.0, sans_ombre=True, halo=True, debord=16, dx_fin=-10, ecart=10,
                     debut=dict(encre='#FCFCFC', fond=None, haut=1.25, etire=1.03),
                     milieu=dict(encre='#FDFCFC', fond='#FA3332', fonte=ARIAL_BLACK, etire=0.889, pad_x=0.135, pad_haut=0.013, pad_y=0.02,
                                 accent_h=0.104, queue=0.08),
                     fin=dict(encre='#FBF94E', fond=None, haut=1.51, etire=1.05, espace=0.16, amorce=0.66, amorce_bas=0.05,
                              amorce_ecart=0.14)),
}


def incliner(calque, pente):
    if not pente:
        return calque
    dx = round(pente * calque.height)
    return calque.transform((calque.width + dx, calque.height), Image.Transform.AFFINE,
                            (1, pente, -dx, 0, 1, 0), resample=Image.Resampling.BICUBIC)


def ligne(texte, taille, st, pos):
    """Une ligne du titre : sur plaque de couleur si « fond », sinon texte nu.
    « AMORCE|CORPS » : l'amorce est écrite en blanc et en plus petit devant le corps."""
    g = {**st, **pos}
    encre, fond, fonte = g['encre'], g['fond'], g['fonte']
    etire, pente, etire_haut = g.get('etire', 1.0), g.get('pente', 0.0), g.get('haut', 1.0)
    taille = round(taille * g['echelle'])
    amorce, _, corps = texte.rpartition('|')

    def morceaux(t):
        """(mot, police, couleur, blanc avant le mot, descente) pour chaque mot de la ligne."""
        f, petit = police(fonte, t), police(fonte, round(t * g.get('amorce', 0.70)))
        esp = lambda pf: g['espace'] * pf.size if 'espace' in g else pf.getlength(' ')
        out = []
        for m in amorce.split():
            out.append((m, petit, encre if fond else BLANC, esp(petit) if out else 0, round(t * g.get('amorce_bas', 0))))
        for i, m in enumerate(corps.split()):
            avant = esp(f) if i else round(t * g.get('amorce_ecart', 0.18)) if out else 0
            out.append((m, f, encre, avant, 0))
        return out

    def largeur(t):
        return sum(av + pf.getlength(m) for m, pf, _, av, _ in morceaux(t)) * etire + 2 * round(t * 0.20) + pente * t * 1.1

    if largeur(taille) > LARGEUR_MAX:  # réduire pour tenir dans la largeur
        taille = int(taille * LARGEUR_MAX / largeur(taille))
    trait = round(taille * 0.07) if g.get('contour') and not fond else 0
    f = police(fonte, taille)
    pad_x, pad_y = ((round(taille * g.get('pad_x', 0.20)), round(taille * g.get('pad_y', 0.11))) if fond
                    else (trait + 4, trait + round(taille * 0.04)))
    haut, bas = f.getbbox('É')[1], f.getbbox('H')[3]
    parts = morceaux(taille)
    queue = round(taille * g.get('queue', 0))  # place sous la ligne de base, pour la queue du Q
    mot = Image.new('RGBA', (round(sum(av + pf.getlength(m) for m, pf, _, av, _ in parts)) + 8, bas - haut + 8 + queue), (0, 0, 0, 0))
    d, x, aigus = ImageDraw.Draw(mot), 4, []
    for m, pf, couleur, avant, descente in parts:  # haut des capitales aligné sur celui du corps
        x += avant
        d.text((x, 4 - haut + f.getbbox('H')[1] - pf.getbbox('H')[1] + descente), m, font=pf, fill=couleur,
               stroke_width=g.get('graisse', 0), stroke_fill=couleur)  # graisse : lettres épaissies
        for i, c in enumerate(m):  # É et È : bords de la lettre, pour redessiner l'accent
            if c in 'ÉÈ':
                x0 = x + pf.getlength(m[:i])
                aigus.append((x0 + pf.getbbox('E')[0], x0 + pf.getbbox('E')[2], c == 'È', couleur))
        x += pf.getlength(m)
    if 'accent_h' in g:  # accents aplatis et collés aux capitales, pour une plaque serrée sur les lettres
        sommet, h_acc = 4 - haut + f.getbbox('H')[1], round(taille * g['accent_h'])
        zone = mot.crop((0, 0, mot.width, sommet))
        serre = Image.new('RGBA', (mot.width, h_acc + mot.height - sommet), (0, 0, 0, 0))
        serre.paste(mot.crop((0, sommet, mot.width, mot.height)), (0, h_acc))
        zd = ImageDraw.Draw(zone)
        for g0, g1, grave, couleur in aigus:  # accent dessiné : parallélogramme épais posé au-dessus de la lettre
            zd.rectangle((g0 - 2, 0, g1 + 2, sommet), fill=(0, 0, 0, 0))
            bas_acc, lg = h_acc - round(h_acc * 0.25), g1 - g0
            pts = [(0.33, bas_acc), (0.65, bas_acc), (0.84, 0), (0.455, 0)]
            pts = [(1 - u if grave else u, v) for u, v in pts]
            masque = Image.new('L', (mot.width * 4, h_acc * 4), 0)
            ImageDraw.Draw(masque).polygon([((g0 + u * lg) * 4, v * 4) for u, v in pts], fill=255)
            masque = masque.resize((mot.width, h_acc), Image.Resampling.LANCZOS)
            dessin = Image.new('RGBA', masque.size, rgb(couleur, 0))
            dessin.putalpha(masque)
            serre.alpha_composite(dessin, (0, 0))
        # Le haut arrondi des lettres rondes (O, Q, C) dépasse un peu la ligne des capitales : il reste tel quel.
        rond = min(round(taille * 0.03), h_acc - 4)
        serre.alpha_composite(zone.crop((0, sommet - rond, mot.width, sommet)), (0, h_acc - rond))
        zone = zone.crop((0, 0, mot.width, sommet - rond))
        if zone.getbbox():  # autres accents (Ê, À, Ô…) : ceux de la police, aplatis au-dessus de la lettre
            x0, y0a, x1, y1a = zone.getbbox()
            acc = zone.crop((0, y0a, mot.width, y1a)).resize((mot.width, h_acc - rond - 2), Image.Resampling.LANCZOS)
            serre.alpha_composite(acc, (0, 0))
        mot = serre
    mot = mot.resize((round(mot.width * etire), round(mot.height * etire_haut)), Image.Resampling.LANCZOS)
    pad_h = round(taille * g['pad_haut']) if fond and 'pad_haut' in g else pad_y  # marge du haut, si elle diffère
    calque = Image.new('RGBA', (mot.width + 2 * pad_x, mot.height + pad_h + pad_y), rgb(fond) if fond else (0, 0, 0, 0))
    if trait:  # contour encre : le mot dilaté, sous le mot
        dessous = Image.new('RGBA', calque.size, (0, 0, 0, 0))
        dessous.alpha_composite(mot, (pad_x, pad_h))
        gras = dessous.getchannel('A').filter(ImageFilter.MaxFilter(2 * trait + 1))
        calque = Image.new('RGBA', calque.size, rgb(ENCRE, 0))
        calque.putalpha(gras)
    calque.alpha_composite(mot, (pad_x, pad_h))
    return incliner(calque, pente)


def hauteur_capitales(fonte):
    bb = police(fonte, 1000).getbbox('H')
    return (bb[3] - bb[1]) / 1000


BORD = 0.36  # place gardée au-dessus des capitales (accents), en proportion de leur hauteur


def ligne_calee(texte, g, cap=None):
    """Une ligne d'un style calé sur sa maquette. Rend (calque, boîte de référence, échelle) : la boîte est celle de
    la plaque, ou celle des capitales pour un texte nu ; c'est elle que bloc_cale aligne. L'échelle vaut 1 quand la
    ligne a la taille de la maquette."""
    cap = demande = cap or g['cap']
    fonte, etire, pente_t = g['fonte'], g.get('etire', 1.0), g.get('pente_texte', 0.0)
    ratio, gr = hauteur_capitales(fonte), g.get('gras', 0)
    cap = round(cap)
    t = round(3 * cap / (ratio + 2 * gr))  # dessiné trois fois plus grand puis réduit : hauteur exacte, bords nets
    f, gras = police(fonte, t), round(t * gr)
    cap_g = round(ratio * t) + 2 * gras
    red = cap / cap_g
    mots, esp = texte.replace('|', ' ').split(), cap * g.get('espace', 0.4) / (etire * red)
    m, bb_h = t, f.getbbox('H')
    morceaux = []
    for w in mots:  # mot par mot, haut des capitales à y = m, chaque mot rogné sur son encre
        bb = f.getbbox(w)
        tmp = Image.new('L', (bb[2] - bb[0] + 4 * gras + 40, cap_g + 2 * m), 0)
        ImageDraw.Draw(tmp).text((20 - bb[0] + gras, m - bb_h[1] + gras), w, font=f, fill=255, stroke_width=gras, stroke_fill=255)
        xs = tmp.getbbox()
        morceaux.append(tmp.crop((xs[0], 0, xs[2], tmp.height)))
    im = Image.new('L', (round(sum(c.width for c in morceaux) + esp * (len(mots) - 1)) + 4, cap_g + 2 * m), 0)
    x = 2.0  # (la toile est un peu trop large quand une ponctuation est rapprochée : rognée plus bas)
    for c, suivant in zip(morceaux, mots[1:] + ['']):
        im.paste(c, (round(x), 0))
        x += c.width + esp * (0.8 if suivant in ('?', '!') else 1)  # ponctuation plus près du mot
    haut, bas = round(cap * BORD), round(cap * 0.30)  # place gardée pour les accents et la queue du Q
    im = im.crop((0, m - round(haut / red), im.width, m + cap_g + round(bas / red)))
    im = im.resize((round(im.width * etire * red), haut + cap + bas), Image.Resampling.LANCZOS)
    if pente_t:  # italique
        dx = round(pente_t * im.height)
        im = im.transform((im.width + dx, im.height), Image.Transform.AFFINE, (1, pente_t, -dx, 0, 1, 0),
                          resample=Image.Resampling.BICUBIC)
    xs = im.crop((0, haut, im.width, haut + cap)).getbbox()  # étendue des capitales, hors accents
    tx0, tx1 = xs[0], xs[2]
    contour = round(cap * g.get('contour', 0))
    relief = g.get('relief') or (0, 0)
    rx, ry = round(cap * relief[0]), round(cap * relief[1])
    mg = contour + max(rx, ry) + 6
    alpha = Image.new('L', (im.width + 2 * mg, im.height + 2 * mg), 0)
    alpha.paste(im, (mg, mg))
    mot = Image.new('RGBA', alpha.size, rgb(g['encre'], 0))
    mot.putalpha(alpha)
    if contour or rx or ry:  # contour noir, puis relief : le contour répété le long de la diagonale
        gros = alpha.filter(ImageFilter.MaxFilter(2 * contour + 1)) if contour else alpha
        dessous = gros.copy()
        n = max(rx, ry)
        for k in range(1, n + 1):
            dessous = ImageChops.lighter(dessous, ImageChops.offset(gros, round(rx * k / n), round(ry * k / n)))
        fond_noir = Image.new('RGBA', alpha.size, rgb(g.get('contour_couleur', '#000000'), 0))
        fond_noir.putalpha(dessous)
        fond_noir.alpha_composite(mot)
        mot = fond_noir
    tx0, tx1, y_cap = tx0 + mg, tx1 + mg, mg + haut
    ech = cap / g['cap']
    if not g.get('fond'):
        boite = (tx0, y_cap, tx1, y_cap + cap)
        if boite[2] - boite[0] > LARGEUR_MAX:
            return ligne_calee(texte, g, min(demande - 1, demande * LARGEUR_MAX / (boite[2] - boite[0])))
        return mot, boite, ech
    pente = g.get('pente', 0.0)
    pad_haut, pad_bas, pad_x = round(cap * g['pad_haut']), round(cap * g['pad_bas']), round(cap * g['pad_x'])
    h, larg = pad_haut + cap + pad_bas, tx1 - tx0 + 2 * pad_x
    if larg > LARGEUR_MAX:
        return ligne_calee(texte, g, min(demande - 1, demande * LARGEUR_MAX / larg))
    bord = 8 + haut
    k = 4  # plaque : parallélogramme dessiné 4 fois plus grand puis réduit, pour des bords nets
    masque = Image.new('L', ((larg + 2 * bord) * k, (h + 2 * bord) * k), 0)
    pts = [(pente * h, 0), (larg, 0), (larg - g.get('pente_d', pente) * h, h), (0, h)]
    ImageDraw.Draw(masque).polygon([((bord + u) * k, (bord + v) * k) for u, v in pts], fill=255)
    masque = masque.resize((larg + 2 * bord, h + 2 * bord), Image.Resampling.LANCZOS)
    calque = Image.new('RGBA', masque.size, rgb(g['fond'], 0))
    calque.putalpha(masque)
    x_mot = bord + round((larg - (tx1 - tx0)) / 2) + round(g.get('dx_texte', 0) * ech) - tx0
    tmp = Image.new('RGBA', calque.size, (0, 0, 0, 0))
    tmp.paste(mot, (x_mot, bord + pad_haut - y_cap))
    calque.alpha_composite(tmp)
    return calque, (bord, bord, bord + larg, bord + h), ech


def tourner(calque, boite, angle):
    """Tourne le calque autour de son centre ; la boîte de référence suit (son centre reste à sa place)."""
    if not angle:
        return calque, boite
    r = calque.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    ox, oy = (r.width - calque.width) // 2, (r.height - calque.height) // 2
    return r, (boite[0] + ox, boite[1] + oy, boite[2] + ox, boite[3] + oy)


def bloc_cale(lignes, style):
    """Bloc titre d'un style calé. Rend (bloc, ancre) : l'ancre est le coin bas gauche de la dernière ligne."""
    st = STYLES[style]
    commun = {k: v for k, v in st.items() if k not in ('debut', 'milieu', 'fin')}
    n, marge, y, places = len(lignes), 160, 0, []
    for i, l in enumerate(lignes):
        g = {**commun, **st['debut' if i == 0 and n > 1 else 'fin' if i == n - 1 else 'milieu']}
        r, boite, ech = ligne_calee(l['texte'], g, l.get('taille'))
        socles = []
        for couleur, sx, sy, rot in g.get('socle', []):  # socle : la plaque d'une autre couleur, glissée dessous
            sr, sb = tourner(teinte(r, couleur), boite, rot)
            socles.append((sr, sb, round(sx * ech), round(sy * ech)))
        nue = boite
        r, boite = tourner(r, boite, g.get('rot', 0))
        y += round(g.get('avant', 0) * ech) if i else 0
        x0 = round(g.get('dx', 0) * ech)
        places.append((r, marge + x0 - boite[0], marge + y - boite[1], g, ech, boite,
                       [(sr, marge + x0 - sb[0] + sx, marge + y - sb[1] + sy) for sr, sb, sx, sy in socles]))
        y += boite[3] - boite[1]
    larg = max(x + r.width for r, x, *_ in places) + marge
    bloc = Image.new('RGBA', (larg, y + 2 * marge), (0, 0, 0, 0))

    def poser(calque, x, yy):
        tmp = Image.new('RGBA', bloc.size, (0, 0, 0, 0))
        tmp.paste(calque, (x, yy))
        bloc.alpha_composite(tmp)

    for r, x, yy, g, ech, boite, socles in places:  # ombres et socles, sous toutes les lignes
        if g.get('ombre_floue'):
            couleur, ox, oy, flou, force = g['ombre_floue']
            o = teinte(r, couleur)
            o.putalpha(o.getchannel('A').point(lambda v: v * force // 255))
            tmp = Image.new('RGBA', bloc.size, (0, 0, 0, 0))
            tmp.paste(o, (x + round(ox * ech), yy + round(oy * ech)))
            bloc.alpha_composite(tmp.filter(ImageFilter.GaussianBlur(flou * ech)))
        dure = g.get('ombre') if g.get('fond') else g.get('ombre_texte')
        if dure:
            poser(teinte(r, dure[0]), x + round(dure[1] * ech), yy + round(dure[2] * ech))
        for sr, sx, sy in socles:
            poser(sr, sx, sy)
    for i, (r, x, yy, g, ech, boite, _) in enumerate(places):
        poser(r, x, yy)
        if i == 0 and n > 1 and g.get('accent') and g.get('fond'):  # barre jaune au pied droit de la première plaque
            h = boite[3] - boite[1]
            bh, bl, biais, k = round(h * 0.50), round(h * 0.325), 0.5, 4
            m = Image.new('L', ((bl + round(biais * bh)) * k, bh * k), 0)
            ImageDraw.Draw(m).polygon([(biais * bh * k, 0), ((bl + biais * bh) * k, 0), (bl * k, bh * k), (0, bh * k)], fill=255)
            m = m.resize((bl + round(biais * bh), bh), Image.Resampling.LANCZOS)
            barre = Image.new('RGBA', m.size, rgb(g['accent'], 0))
            barre.putalpha(m)
            pied = x + boite[2] - g['pente'] * h  # pied droit de la plaque
            poser(barre, round(pied + 0.02 * h), yy + boite[3] - bh - round(0.03 * h))
    ancre = (marge, marge + y)
    angle = st.get('rotation', 0)
    if angle:
        a = math.radians(angle)
        cx, cy = bloc.width / 2, bloc.height / 2
        bloc = bloc.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        dx, dy = ancre[0] - cx, ancre[1] - cy
        ancre = (round(bloc.width / 2 + dx * math.cos(a) + dy * math.sin(a)),
                 round(bloc.height / 2 - dx * math.sin(a) + dy * math.cos(a)))
    return bloc, ancre


def teinte(calque, couleur):
    o = Image.new('RGBA', calque.size, rgb(couleur, 0))
    o.putalpha(calque.getchannel('A'))
    return o


def bloc_titre(lignes, style):
    """Empile les lignes le long de la pente, pose l'ombre dure, puis penche le bloc. Rend (bloc, hauteur utile)."""
    st = STYLES[style]
    pente, n = st.get('pente', 0.0), len(lignes)
    rendus = []
    for i, l in enumerate(lignes):
        pos = st['debut'] if i == 0 and n > 1 else st['fin'] if i == n - 1 else st['milieu']
        pos = pos if isinstance(pos, dict) else dict(encre=pos[0], fond=pos[1])
        rendus.append((ligne(l['texte'], l['taille'], st, pos), pos['fond']))
    marge = 60
    y, places = marge, []
    for i, (r, fond) in enumerate(rendus):
        dessous = sum(round(pente * s.height) for s, _ in rendus[i + 1:])
        if 'ecart' in st:  # calage sur l'encre visible : même écart entre les lignes, bords gauches alignés
            bb = r.getbbox()
            dx = -st.get('debord', 0) if fond else st.get('dx_fin', 0) if i == n - 1 else 0
            places.append((r, marge + 30 + dx - bb[0], y - bb[1], fond))
            y += bb[3] - bb[1] + st['ecart']
            continue
        debord = st.get('debord', 0) if fond else 0  # la plaque dépasse à gauche de la colonne de texte
        places.append((r, marge + dessous - debord + (14 * (n - 1 - i) if st.get('accent') else 0), y, fond))
        y += r.height + (-3 if fond else 2)
    larg = max(x + r.width for r, x, _, _ in places) + marge + 40
    bloc = Image.new('RGBA', (larg, y + marge), (0, 0, 0, 0))
    for r, x, yy, fond in places:  # ombre dure : couleur du style sur les plaques, encre sous le texte nu
        if fond and st.get('ombre'):
            bloc.alpha_composite(teinte(r, st['ombre']), (x - 22, yy + 18))
        elif not st.get('sans_ombre'):
            bloc.alpha_composite(teinte(r, ENCRE), (x + (9 if fond else 6), yy + (10 if fond else 7)))
    for r, x, yy, _ in places:
        bloc.alpha_composite(r, (x, yy))
    if st.get('accent'):  # barre jaune au pied droit de la première ligne
        r0, x0, y0, _ = places[0]
        accent = incliner(Image.new('RGBA', (round(r0.height * 0.20), round(r0.height * 0.42)), rgb(JAUNE)), pente)
        bloc.alpha_composite(accent, (x0 + r0.width - round(pente * r0.height) + 12, y0 + r0.height - accent.height))
    if st.get('rotation'):
        bloc = bloc.rotate(st['rotation'], resample=Image.Resampling.BICUBIC, expand=True)
    return bloc, bloc.height - 2 * marge


# ---------------------------------------------------------------- dossiers
def N(t, taille=None):  # une ligne du titre ; couleurs, plaques et taille viennent du style du dossier.
    # taille : corps de la police pour le style magazine, hauteur des capitales en pixels pour les styles calés.
    return dict(texte=t, taille=taille)


P = N  # ancien nom de la dernière ligne (plaque jaune de la v3)

KANE = dict(fond='../sources/kane-2018-07-03.jpg', portrait=dict(echelle=0.74, haut=392, cx=0.53), saturation=1.12, voile_haut=0.2,
            yeux=(478, 880, 470, 104, -2))

DOSSIERS = {
    13: dict(fond='13.png', style='pop', centre=(0.5, 0.42), zoom=1.12, lignes=[N('SE PESER'), P("DANS L'ESPACE ?")]),
    14: dict(fond='14.png', style='magazine', voile_bas=0.25, bas=1230, lignes=[N('TOP 3', 216), N('VOITURES', 154), P('LES PLUS|RAPIDES', 129)]),
    17: dict(fond='17.png', style='autocollant', centre=(0.5, 0.40), zoom=1.18, lignes=[N('TOP 3'), N('ANIMAUX'), P('LES PLUS RAPIDES')]),
    20: dict(fond='20.png', style='pop', lignes=[N('TOP 3'), N('TÉLÉPHONES'), P('LES PLUS CHERS')]),
    24: dict(fond='24.png', style='jaune', etalon=('10-fusee-yellow.png', (880, 1360)), lignes=[N('POURQUOI INONDER'), P('UNE FUSÉE ?')]),
    25: dict(fond='25.png', style='course', lignes=[N('TOP 3'), N('MONTAGNES RUSSES'), P('LES PLUS RAPIDES')]),
    # fond déjà étalonné sur la maquette par assets/miniatures-v2/fond_31_cagoule.py : aucun réglage ici
    31: dict(fond='31-cagoule.png', style='magazine', contraste=1.0, saturation=1.0, voile_bas=0, voile_haut=0,
             vignette=False, bas=1514, dx=24, lignes=[N('POGBA', 216), N('BRAQUÉ', 154), P('POUR|13 MILLIONS', 129)]),
    40: dict(KANE, style='autocollant', bas=1650, lignes=[N('TOP 10'), N('BUTS LES PLUS'), P('DÉGUEULASSES')]),
    42: dict(fond='42.png', style='pop', etalon=('06-ballons-pop.png', (1080, 1500)), lignes=[N('TOP 10'), N('PLUS BEAUX'), P('BALLONS DE FOOT')]),
    43: dict(fond='43.png', style='course', etalon=('07-motos-racing.png', (920, 1450)), lignes=[N('TOP 3'), N('MOTOS DE SÉRIE'), P('LES PLUS RAPIDES')]),
    44: dict(KANE, style='autocollant', bas=1650, lignes=[N('TOP 5'), N('BUTS LES PLUS'), P('DÉGUEULASSES')]),
}


def logo_hpb(hauteur=190, decoupe=True):
    """La bulle jaune du logo, pleine, avec « HPB » à la place du « ?! » : découpé (par défaut) ou en noir plein."""
    logo = Image.open(LOGO).convert('RGBA')
    alpha = logo.getchannel('A').point(lambda v: 255 if v > 40 else 0)
    cadre = Image.new('L', (logo.width + 2, logo.height + 2), 0)
    cadre.paste(alpha, (1, 1))
    ImageDraw.floodfill(cadre, (0, 0), 128)  # 128 = extérieur de la bulle
    trous = cadre.crop((1, 1, logo.width + 1, logo.height + 1)).point(lambda v: 255 if v == 0 else 0)
    plein = ImageChops.lighter(logo.getchannel('A'), trous.filter(ImageFilter.MaxFilter(5)))
    bulle = Image.new('RGBA', logo.size, rgb(JAUNE, 0))
    bulle.putalpha(plein)
    f = police(POPPINS, 300)
    bb = f.getbbox('HPB')
    mot = Image.new('RGBA', (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(mot).text((4 - bb[0], 4 - bb[1]), 'HPB', font=f, fill=rgb('#000000'))
    mot = mot.resize((520, round(mot.height * 520 / mot.width * 1.12)), Image.Resampling.LANCZOS)
    # Lettres pleines : l'intérieur du P et du B est bouché (tout ce que l'extérieur n'atteint pas est lettre).
    ext = Image.new('L', (mot.width + 2, mot.height + 2), 0)
    ext.paste(mot.getchannel('A').point(lambda v: 255 if v > 128 else 0), (1, 1))
    ImageDraw.floodfill(ext, (0, 0), 128)
    creux = ext.crop((1, 1, mot.width + 1, mot.height + 1)).point(lambda v: 255 if v == 0 else 0)
    mot.putalpha(ImageChops.lighter(mot.getchannel('A'), creux.filter(ImageFilter.MaxFilter(5))))
    mot = mot.rotate(11.5, resample=Image.Resampling.BICUBIC, expand=True)  # la pente de la bulle
    place = (476 - mot.width // 2, 436 - mot.height // 2)  # centre du corps de la bulle
    if decoupe:  # lettres découpées dans la bulle : on voit l'image au travers
        trou = Image.new('L', bulle.size, 0)
        trou.paste(mot.getchannel('A'), place)
        bulle.putalpha(ImageChops.subtract(bulle.getchannel('A'), trou))
    else:  # lettres noires pleines
        bulle.alpha_composite(mot, place)
    bulle = bulle.crop(bulle.getbbox())
    return bulle.resize((round(bulle.width * hauteur / bulle.height), hauteur), Image.Resampling.LANCZOS)


def composer(n):
    c = dict(DOSSIERS[n])
    lignes = c.pop('lignes')
    style = c.pop('style')
    bas_dossier = c.pop('bas', None)
    bas = bas_dossier or BAS_TITRE
    yeux = c.pop('yeux', None)
    dx = c.pop('dx', 0)  # décalage du bloc titre vers la droite
    etalon = c.pop('etalon', None)  # (maquette, rangées du titre) : le fond prend les réglages photo de la maquette
    if etalon:
        c = {**dict(contraste=1.0, saturation=1.0, voile_bas=0, voile_haut=0, vignette=False), **c}
    im = preparer_fond(FONDS / c.pop('fond'), **c)
    if etalon:
        im = etalonner(im, *etalon)
    if yeux:  # bandeau noir sur les yeux (cx, cy, largeur, hauteur, angle), pour l'accroche
        cx, cy, w, h, angle = yeux
        barre = Image.new('RGBA', (w, h), (0, 0, 0, 255)).rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        im.alpha_composite(barre, (cx - barre.width // 2, cy - barre.height // 2))
    # En haut : le logo seul, à droite, dans la zone gardée par la grille 3:4 de TikTok.
    logo = logo_hpb()
    im.alpha_composite(logo, (L - MARGE_G - logo.width, HAUT_BANDEAU))
    if STYLES[style].get('cale'):  # style calé : le coin bas gauche de la dernière ligne va sur l'ancre de la maquette
        bloc, ancre = bloc_cale(lignes, style)
        ax, ay = STYLES[style]['ancre']
        calque = Image.new('RGBA', im.size, (0, 0, 0, 0))
        calque.paste(bloc, (ax + dx - ancre[0], (bas_dossier or ay) - ancre[1]))
        im.alpha_composite(calque)
        return im.convert('RGB')
    bloc, total = bloc_titre(lignes, style)
    if STYLES[style].get('halo'):  # fond noirci derrière le titre
        h = halo_sombre(bloc)
        calque = Image.new('RGBA', im.size, (0, 0, 0, 0))
        calque.paste(h, (MARGE_G - 60 - 260 + dx, bas - total - 60 - 260))
        im.alpha_composite(calque)
    else:
        im.alpha_composite(ombre_portee(bloc, flou=22, force=120), (MARGE_G - 60 - 40 + dx, bas - total - 60 - 40))
    im.alpha_composite(bloc, (MARGE_G - 60 + dx, bas - total - 60))
    return im.convert('RGB')


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    nums = [int(a) for a in sys.argv[1:]] or sorted(DOSSIERS)
    for n in nums:
        composer(n).save(SORTIE / f'{n}.jpg', quality=93)
        print('miniature', n)
    tous = sorted(int(p.stem) for p in SORTIE.glob('[0-9]*.jpg'))
    col = 6
    rangs = -(-len(tous) // col)
    planche = Image.new('RGB', (col * 432 + (col + 1) * 16, rangs * 768 + (rangs + 1) * 16), ENCRE)
    for i, n in enumerate(tous):
        v = Image.open(SORTIE / f'{n}.jpg').resize((432, 768), Image.Resampling.LANCZOS)
        planche.paste(v, (16 + (i % col) * 448, 16 + (i // col) * 784))
    planche.save(SORTIE / 'planche.jpg', quality=90)
    print('planche :', SORTIE / 'planche.jpg')


if __name__ == '__main__':
    main()
