"""Couverture du dossier 28 (L'OM a acheté un match), v4 : la v3 validée, remontée pour la grille 3:4 de TikTok.

Le 14 novembre 2026, Marc a vu « UN MATCH » coupé dans la grille du profil : TikTok n'y garde que les rangées 240 à
1680, et le titre de la v3 (incrusté dans le PNG par image_gen) descendait jusqu'à la rangée 1825. On remonte toute
l'image de DECALAGE rangées : le titre passe au-dessus de 1680 et l'ancien logo, trop haut, sort par le haut. Le bas
libéré est comblé par la veste (rangées sous le titre, étirées et assombries). Le logo validé est reposé ensuite.

Usage : python couverture_28_v4.py [variante]   (variantes : voir LOGOS)
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from miniatures_hpb import BOITE_LOGO, logo_valide  # noqa: E402

DOSSIER = ROOT / 'out/miniatures-programmees-14nov-2026'
SOURCE = DOSSIER / 'version-validee/28-om-v3.png'
DECALAGE = 230    # titre 1146-1825 -> 916-1595 ; ancien logo (rangées 54-222) -> hors cadre
SOUS_TITRE = 1840  # première rangée sans lettre sous « UN MATCH »

# Logo : (x, y, côté). À BOITE_LOGO (en haut à droite, y = 234), il couvrirait l'œil gauche de Tapie une fois l'image
# remontée. Marc veut le voir dans la grille 3:4 (rangées 240 à 1680), d'où ces placements.
LOGOS = {
    'haut': (BOITE_LOGO[0], 0, 240),     # sur les cheveux, hors grille : refusé par Marc (« on ne voit pas le logo »)
    'bas-droite': (806, 1356, 240),      # sur la veste, à droite de « UN MATCH », dans la grille
    'haut-gauche': (14, 252, 170),       # sur le stade, à gauche de la ligne jaune, dans la grille
}


def fond():
    src = Image.open(SOURCE).convert('RGB')
    W, H = src.size
    im = Image.new('RGB', (W, H))
    im.paste(src.crop((0, DECALAGE, W, H)), (0, 0))
    # Comblement du bas : la veste sous le titre, étirée, floutée et fondue vers le noir.
    bas = src.crop((0, SOUS_TITRE, W, H)).resize((W, DECALAGE + 40), Image.Resampling.LANCZOS)
    bas = bas.filter(ImageFilter.GaussianBlur(6))
    noir = Image.new('RGB', bas.size, (4, 6, 16))
    degrade = Image.linear_gradient('L').resize(bas.size).point(lambda v: round(v * 0.55))
    bas = Image.composite(noir, bas, degrade)
    fondu = Image.linear_gradient('L').resize((W, 40))  # raccord doux sur 40 rangées
    raccord = Image.composite(bas.crop((0, 0, W, 40)), im.crop((0, H - DECALAGE - 40, W, H - DECALAGE)), fondu)
    im.paste(bas.crop((0, 40, W, bas.height)), (0, H - DECALAGE))
    im.paste(raccord, (0, H - DECALAGE - 40))
    return im.convert('RGBA')


def composer(variante):
    x, y, cote = LOGOS[variante]
    im = fond()
    logo = logo_valide()
    if cote != logo.width:
        logo = logo.resize((cote, cote), Image.Resampling.LANCZOS)
    im.alpha_composite(logo, (x, y))
    return im.convert('RGB')


def main():
    variantes = sys.argv[1:] or list(LOGOS)
    for v in variantes:
        sortie = DOSSIER / f'28-om-v4-{v}.png'
        composer(v).save(sortie)
        print(sortie)


if __name__ == '__main__':
    main()
