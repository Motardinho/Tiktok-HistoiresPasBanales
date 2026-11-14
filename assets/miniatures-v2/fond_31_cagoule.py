# Fond de la miniature 31 : Pogba (finale 2018) à gauche, braqueur cagoulé (illustration) à droite, ligne jaune en
# diagonale. Sans texte ni logo : le titre et la bulle HPB sont posés par miniatures_hpb.py.
# Les deux photos sont de vraies photos (crédits dans sources/CREDITS.md), recadrées, assombries, la cagoule désaturée.
# Le cadrage est recalé sur l'ancienne miniature d'essai E1, que Marc avait choisie.
# Usage, depuis la racine du dépôt : python assets/miniatures-v2/fond_31_cagoule.py
from pathlib import Path

import cv2
import numpy as np

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent
POGBA = ICI / 'sources/pogba-2018/Paul_Pogba_in_2018.jpg'
CAGOULE = ICI / 'sources/cagoule-marquize/thomas-marquize-NUnaOLFFVEw.jpg'
E1 = RACINE / 'out/31-pogba-braque-pour-13-millions/miniature-essai/E1-diagonale-bleus-cagoule.jpg'
MAQUETTE = RACINE / 'out/miniatures-10-variantes-2026-11-12/09-pogba-magazine.png'  # étalonnage de référence
SORTIE = ICI / 'fonds/31-cagoule.png'
L, H = 1080, 1920
ENCRE = np.array([28, 21, 18], np.float32)      # #12151C en BGR
JAUNE = np.array([74, 226, 255], np.float32)    # #FFE24A en BGR
X0, PENTE = 639.5, -0.1032                      # la diagonale : x = X0 + PENTE * y (mesurée sur E1)


def lire(chemin):
    return cv2.imdecode(np.fromfile(str(chemin), np.uint8), cv2.IMREAD_COLOR)


def recaler(photo, repere, zone, echelles):
    """Échelle et position de la photo dans le cadre 1080x1920, par corrélation avec une zone sans texte de E1."""
    xa, ya, xb, yb = zone
    motif = cv2.cvtColor(repere[ya:yb, xa:xb], cv2.COLOR_BGR2GRAY)
    gris = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    meilleur = (-1, None, None)
    for e in echelles:
        g = cv2.resize(gris, None, fx=e, fy=e, interpolation=cv2.INTER_AREA if e < 1 else cv2.INTER_CUBIC)
        if g.shape[0] < motif.shape[0] or g.shape[1] < motif.shape[1]:
            continue
        r = cv2.matchTemplate(g, motif, cv2.TM_CCOEFF_NORMED)
        _, score, _, (px, py) = cv2.minMaxLoc(r)
        if score > meilleur[0]:
            meilleur = (score, e, (xa - px, ya - py))
    return meilleur


def poser(photo, echelle, pos, fondu_haut, fondu_bas, gain, saturation=1.0):
    """La photo à l'échelle, sur fond encre, avec fondus vers l'encre en haut et en bas. Rend (image, alpha)."""
    p = cv2.resize(photo, None, fx=echelle, fy=echelle, interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    if saturation != 1.0:
        g = cv2.cvtColor(p.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)[..., None]
        p = g + (p - g) * saturation
    p = np.clip(p * gain, 0, 255)
    toile = np.tile(ENCRE, (H, L, 1)).astype(np.float32)
    alpha = np.zeros((H, L), np.float32)
    x, y = pos
    xa, ya, xb, yb = max(x, 0), max(y, 0), min(x + p.shape[1], L), min(y + p.shape[0], H)
    toile[ya:yb, xa:xb] = p[ya - y:yb - y, xa - x:xb - x]
    alpha[ya:yb, xa:xb] = 1
    rangs = np.arange(H, dtype=np.float32)
    h0, h1 = fondu_haut
    b0, b1 = fondu_bas
    a = np.clip((rangs - h0) / max(h1 - h0, 1), 0, 1) * np.clip((b1 - rangs) / max(b1 - b0, 1), 0, 1)
    alpha *= (a ** 1.3)[:, None]
    return toile, alpha


def etalonner(image, modele, zone, plafond=255, gris=False):
    """Donne à l'image les réglages de la maquette (luminosité, contraste, couleurs) : pour chaque canal, la courbe
    qui fait coïncider les histogrammes des deux images dans une zone sans texte, appliquée à toute l'image."""
    xa, ya, xb, yb = zone
    if gris:  # photo presque noire : un simple gain sur la luminance (une courbe d'histogramme y creuse des à-plats)
        lum = image.mean(2, keepdims=True)
        gain = np.percentile(modele[ya:yb, xa:xb].mean(2), 97) / max(np.percentile(lum[ya:yb, xa:xb], 97), 1)
        cible = lum * gain
        cible = np.where(cible > plafond - 40, plafond - 40 + 40 * np.tanh((cible - plafond + 40) / 40), cible)
        return np.clip(image * (cible / np.maximum(lum, 1)), 0, 255)
    sortie = np.empty_like(image)
    for c in range(3):
        src = np.clip(image[ya:yb, xa:xb, c], 0, 255).astype(np.uint8)
        ref = modele[ya:yb, xa:xb, c]
        cs = np.cumsum(np.bincount(src.ravel(), minlength=256)) / src.size
        cr = np.cumsum(np.bincount(ref.ravel(), minlength=256)) / ref.size
        courbe = np.interp(cs, cr, np.arange(256))
        courbe = np.convolve(np.pad(courbe, 8, mode='edge'), np.ones(17) / 17, mode='valid')  # courbe lissée
        courbe = np.maximum.accumulate(courbe)
        # au-delà des tons présents dans la zone, la courbe n'est pas connue : on la plafonne (reflets de l'arrière-plan)
        courbe = np.where(courbe > plafond - 40, plafond - 40 + 40 * np.tanh((courbe - plafond + 40) / 40), courbe)
        sortie[..., c] = np.interp(np.clip(image[..., c], 0, 255), np.arange(256), courbe)
    return sortie


def main():
    e1 = lire(E1)
    pogba, cagoule = lire(POGBA), lire(CAGOULE)
    s1, ep, pp = recaler(pogba, e1, (40, 420, 480, 900), np.arange(1.20, 1.80, 0.01))
    s2, ec, pc = recaler(cagoule, e1, (640, 430, 1040, 900), np.arange(0.24, 0.40, 0.002))
    print(f'Pogba : échelle {ep:.2f}, position {pp}, corrélation {s1:.2f}')
    print(f'Cagoule : échelle {ec:.3f}, position {pc}, corrélation {s2:.2f}')
    g, alpha_g = poser(pogba, ep, pp, (pp[1], pp[1] + 230), (1380, 1700), gain=0.78)
    d, alpha_d = poser(cagoule, ec, pc, (pc[1], pc[1] + 120), (930, 1130), gain=0.64, saturation=0.30)
    # Étalonnage sur la maquette, photo par photo, avant le fondu vers le fond sombre de la maquette.
    maquette = lire(MAQUETTE)
    g = etalonner(g, maquette, (30, 400, 480, 900))    # le visage de Pogba
    d = etalonner(d, maquette, (660, 430, 1050, 900), plafond=140, gris=True)  # la cagoule et son arrière-plan
    encre = np.tile(np.median(maquette[1750:1900, 620:1060].reshape(-1, 3), 0), (H, L, 1)).astype(np.float32)
    g = encre + (g - encre) * alpha_g[..., None]
    d = encre + (d - encre) * alpha_d[..., None]
    xs = np.arange(L, dtype=np.float32)[None, :].repeat(H, 0)
    ys = np.arange(H, dtype=np.float32)[:, None].repeat(L, 1)
    ecart = xs - (X0 + PENTE * ys)
    cote = np.clip(0.5 - ecart, 0, 1)[..., None]  # 1 à gauche de la diagonale
    im = d + (g - d) * cote
    # ligne jaune de 9 px, qui s'éteint vers le bas
    trait = np.clip(5.0 - np.abs(ecart), 0, 1) * np.clip(1 - (ys - 1350) / 700, 0.35, 1)
    im = im + (JAUNE - im) * trait[..., None]
    cv2.imencode('.png', np.clip(im, 0, 255).astype(np.uint8))[1].tofile(str(SORTIE))
    print('fond :', SORTIE)


if __name__ == '__main__':
    main()
