"""Couverture du dossier 28 (L'OM a acheté un match), v5 : titre remonté dans la grille, logo en haut à droite.

14 novembre 2026. Dans la grille 3:4 du profil TikTok (rangées 240 à 1680), la v3 coupait « UN MATCH » (titre
jusqu'à la rangée 1825) et son logo (rangées 54 à 222). La v4 remontait toute l'image : le titre rentrait, mais le
logo à BOITE_LOGO tombait sur l'œil de Tapie, et Marc a refusé tout autre emplacement (« le logo est TOUJOURS en haut
à droite »). Ici l'image reste en place (le logo à BOITE_LOGO tombe sur les cheveux et le haut du front) et seul le
titre, incrusté dans le PNG par image_gen, est détouré par ses couleurs puis remonté de MONTEE rangées. L'ancien
titre et l'ancien logo sont effacés par reconstruction du fond (cv2.inpaint), sur la veste et les cheveux sombres.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from miniatures_hpb import BOITE_LOGO, logo_valide  # noqa: E402

DOSSIER = ROOT / 'out/miniatures-programmees-14nov-2026'
SOURCE = DOSSIER / 'version-validee/28-om-v3.png'
SORTIE = DOSSIER / '28-om-v5.png'
ZONE_TITRE = (0, 1100, 820, 1900)   # x0, y0, x1, y1 : tout le bloc titre de la v3
ZONE_LOGO = (780, 20, 1060, 260)    # ancien logo de la v3
MONTEE = 290                        # titre 1146-1825 -> 856-1535 : au-dessus de la bande des compteurs (rangée 1540)


def masque_titre(a):
    """Lettres blanches, plaque rouge, lettres jaunes, dans la zone du titre (élargi de quelques pixels)."""
    r, g, b = (a[..., i].astype(int) for i in range(3))
    blanc = (r > 200) & (g > 200) & (b > 200)
    rouge = (r > 170) & (g < 90) & (b < 90)
    jaune = (r > 200) & (g > 190) & (b < 110)
    m = blanc | rouge | jaune
    x0, y0, x1, y1 = ZONE_TITRE
    zone = np.zeros_like(m)
    zone[y0:y1, x0:x1] = True
    m &= zone
    m = cv2.morphologyEx(m.astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return m


def masque_logo(a):
    r, g, b = (a[..., i].astype(int) for i in range(3))
    jaune = (r > 200) & (g > 180) & (b < 120)
    x0, y0, x1, y1 = ZONE_LOGO
    m = np.zeros(jaune.shape, np.uint8)
    m[y0:y1, x0:x1] = jaune[y0:y1, x0:x1].astype(np.uint8) * 255
    return m


def plume(h, w, bord):
    """Masque 0..1 qui monte sur `bord` pixels depuis chaque côté."""
    yy = np.minimum(np.arange(h), np.arange(h)[::-1])[:, None]
    xx = np.minimum(np.arange(w), np.arange(w)[::-1])[None, :]
    return np.clip(np.minimum(yy, xx) / bord, 0, 1)


def reprendre_cheveux(a, fond, ml):
    """Ancien logo : on recopie les cheveux voisins (DECALE_CHEVEUX px à gauche), fondus sur les bords."""
    ys, xs = np.nonzero(ml)
    y0, y1, x0, x1 = ys.min() - 30, ys.max() + 30, xs.min() - 30, xs.max() + 30
    y0 = max(y0, 0)
    pris = a[y0:y1, x0 - DECALE_CHEVEUX:x1 - DECALE_CHEVEUX].astype(float)
    m = plume(y1 - y0, x1 - x0, 30)[..., None]
    out = fond.copy()
    out[y0:y1, x0:x1] = (pris * m + fond[y0:y1, x0:x1] * (1 - m)).round().astype(np.uint8)
    return out


def fondre_bas(fond):
    """Sous le titre remonté : ombres de l'ancien titre fondues dans un dégradé de veste floue et sombre."""
    x1, y0 = 900, 1470
    zone = fond[y0:, :x1].astype(float)
    flou = cv2.GaussianBlur(fond, (0, 0), 45)[y0:, :x1].astype(float)
    h, w = zone.shape[:2]
    haut = np.clip(np.arange(h) / 80, 0, 1)[:, None]               # entrée progressive sur 80 rangées
    droite = np.clip((w - np.arange(w)) / 120, 0, 1)[None, :]       # sortie progressive à droite
    m = (haut * droite)[..., None]
    sombre = np.linspace(0.85, 0.55, h)[:, None, None]              # plus sombre vers le bas, comme la v3
    out = fond.copy()
    out[y0:, :x1] = (flou * sombre * m + zone * (1 - m)).round().astype(np.uint8)
    return out


DECALE_CHEVEUX = 300


def main():
    a = np.asarray(Image.open(SOURCE).convert('RGB'))
    mt = masque_titre(a)
    ml = masque_logo(a)
    # Le titre détouré avec un liseré doux (garde l'ombre et l'anticrénelage du bord des lettres).
    alpha = cv2.GaussianBlur(cv2.dilate(mt, np.ones((5, 5), np.uint8)), (5, 5), 0)
    titre = np.dstack([a, alpha])
    # Fond sans titre ni logo : masques élargis pour emporter les ombres portées.
    efface = cv2.dilate(mt, np.ones((23, 23), np.uint8)) | cv2.dilate(ml, np.ones((25, 25), np.uint8))
    bgr = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    fond = cv2.cvtColor(cv2.inpaint(bgr, efface, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
    fond = reprendre_cheveux(a, fond, ml)
    fond = fondre_bas(fond)
    fond = Image.fromarray(fond).convert('RGBA')
    calque = Image.new('RGBA', fond.size, (0, 0, 0, 0))
    calque.paste(Image.fromarray(titre, 'RGBA'), (0, -MONTEE))
    # Ombre douce sous le titre remonté, comme une ombre portée de maquette.
    ombre = Image.fromarray(cv2.GaussianBlur(cv2.dilate(alpha, np.ones((15, 15), np.uint8)), (41, 41), 0))
    noir = Image.new('RGBA', fond.size, (2, 4, 12, 0))
    noir.putalpha(ombre.point(lambda v: round(v * 0.55)))
    ombre_dec = Image.new('RGBA', fond.size, (0, 0, 0, 0))
    ombre_dec.paste(noir, (0, -MONTEE + 8))
    fond.alpha_composite(ombre_dec)
    fond.alpha_composite(calque)
    fond.alpha_composite(logo_valide(), BOITE_LOGO[:2])
    fond.convert('RGB').save(SORTIE)
    print(SORTIE)


if __name__ == '__main__':
    main()
