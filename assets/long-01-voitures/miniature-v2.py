# Miniature YouTube 16:9 de la vidéo longue « TOP 3 — Jusqu'à 503 km/h », version 2 (15 novembre 2026).
# Fond : film officiel BYD Global PWWamnhY9pE « YANGWANG U9X | 503.17km/h », image de 204,35 s : la U9 Xtreme n° 01
# lancée sur la piste d'Abu Dhabi, celle de la tentative à 503 km/h. Titre en style « course » de miniatures_hpb.py
# (maquette 07), logo validé en haut à droite. Rien n'est généré par IA : recadrage, réglages et texte seulement.
# Usage, depuis la racine du dépôt : python assets/long-01-voitures/miniature-v2.py
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import miniatures_hpb as mh  # noqa: E402

SRC = ROOT / 'assets/long-01-voitures/PWWamnhY9pE.mp4'
INSTANT = 204.35
OUT = ROOT / 'out/long-01-voitures-vitesse'
WORK = OUT / '_montage'
L, H = 1920, 1080
CADRE = (0, 0, 3840, 2160)  # image entière : la source est douce, la voiture reste nette à cette taille ; ciel libre en haut à gauche pour le titre
REGLAGES = dict(luminosite=1.03, contraste=1.16, couleurs=1.18, nettete=dict(rayon=1.0, pourcent=70, seuil=3))
LIGNES = [mh.N('TOP 3'), mh.N('JUSQU’À'), mh.N('503 KM/H', 128)]
HAUT_TITRE = 500  # hauteur du bloc titre (plaques comprises) sur 1080


def main():
    raw = WORK / 'miniature-v2-source.png'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(INSTANT), '-i', str(SRC),
                    '-frames:v', '1', str(raw)], check=True)
    im = Image.open(raw).convert('RGB').crop(CADRE).resize((L, H), Image.Resampling.LANCZOS)
    im.save(WORK / 'miniature-v2-avant.jpg', quality=95)
    r = REGLAGES
    im = ImageEnhance.Brightness(im).enhance(r['luminosite'])
    im = ImageEnhance.Contrast(im).enhance(r['contraste'])
    im = ImageEnhance.Color(im).enhance(r['couleurs'])
    n = r['nettete']
    im = im.filter(ImageFilter.UnsharpMask(n['rayon'], n['pourcent'], n['seuil']))
    im.save(WORK / 'miniature-v2-apres.jpg', quality=95)

    out = im.convert('RGBA')
    # Voile marine en haut à gauche, derrière le titre : le ciel est pâle, le blanc de « JUSQU'À » doit ressortir.
    voile = Image.new('L', (L, H), 0)
    d = ImageDraw.Draw(voile)
    for x in range(L):
        for_x = max(0.0, 1 - x / 1250)
        d.line((x, 0, x, H), fill=round(255 * for_x))
    vert = Image.linear_gradient('L').resize((L, H)).point(lambda v: 255 - v)  # fort en haut, nul en bas
    masque = Image.fromarray(((mh.np.asarray(voile, float) / 255) * (mh.np.asarray(vert, float) / 255) * 150).astype('uint8'))
    sombre = Image.new('RGBA', (L, H), (5, 10, 38, 255))
    sombre.putalpha(masque)
    out.alpha_composite(sombre)

    bloc, _ = mh.bloc_cale(LIGNES, 'course')
    bloc = bloc.crop(bloc.getbbox())
    k = HAUT_TITRE / bloc.height
    bloc = bloc.resize((round(bloc.width * k), HAUT_TITRE), Image.Resampling.LANCZOS)
    pos = (58, 60)
    out.alpha_composite(bloc, pos)
    logo = mh.logo_valide().resize((220, 220), Image.Resampling.LANCZOS)
    out.alpha_composite(logo, (L - 220 - 40, 30))

    fin = out.convert('RGB')
    fin.save(OUT / 'miniature-youtube-v2.jpg', quality=92)
    # Taille téléphone : vignette de la page d'accueil YouTube (environ 360 px de large) et petite suggestion (168 px).
    tel = Image.new('RGB', (360 + 16 + 168, 202), (18, 21, 28))
    tel.paste(fin.resize((360, 202), Image.Resampling.LANCZOS), (0, 0))
    tel.paste(fin.resize((168, 94), Image.Resampling.LANCZOS), (376, 0))
    tel.save(WORK / 'miniature-v2-mobile.png')
    av = Image.new('RGB', (960, 270))
    av.paste(Image.open(WORK / 'miniature-v2-avant.jpg').resize((480, 270)), (0, 0))
    av.paste(Image.open(WORK / 'miniature-v2-apres.jpg').resize((480, 270)), (480, 0))
    av.save(WORK / 'miniature-v2-reglages.jpg', quality=92)
    (WORK / 'miniature-v2-manifeste.json').write_text(json.dumps(dict(
        source='BYD Global, YouTube PWWamnhY9pE « YANGWANG U9X | 503.17km/h, Pursuit beyond the Ultimate », 3840x2160',
        instant_s=INSTANT, sujet='Yangwang U9 Xtreme n° 01, piste d’Abu Dhabi (tentative à 503 km/h)',
        cadre_source=CADRE, reglages=REGLAGES, voile='marine #050A26, 150/255 max en haut à gauche',
        style='course (maquette 07) de miniatures_hpb.py, bloc mis à 500 px de haut ; « 503 KM/H » agrandi (cap 128 au lieu de 86)',
        texte=[l['texte'] for l in LIGNES], titre_youtube='TOP 3 — Jusqu’à 503 km/h : la course aux limites',
        logo='hpb-reference-propre-v1.png, 220x220 en haut à droite',
        remplace='miniature-youtube.jpg (gros plan de phare, titre « À LA LIMITE DE LA VITESSE »), conservée'),
        ensure_ascii=False, indent=1), encoding='utf-8')
    print(OUT / 'miniature-youtube-v2.jpg', (OUT / 'miniature-youtube-v2.jpg').stat().st_size, 'octets ; bloc', bloc.size)


if __name__ == '__main__':
    main()
