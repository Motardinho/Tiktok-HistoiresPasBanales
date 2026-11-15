# Miniature YouTube 16:9 de la vidéo longue, version 4 (15 novembre 2026), sur le modèle du Short publié
# « Trois voitures de série qui ont dépassé les 450 km/h » (youtube.com/shorts/kdbAWhNzqpI, 4,6 k vues le 15 nov.) :
# même photo (SSC Tuatara blanche sur la route de montagne, film SSC North America ssc-road.mp4) et même titre
# « TOP 3 / DES VOITURES / LES PLUS RAPIDES / 2026 », en style course (maquette 07, quatre lignes comme les motos).
# Rien n'est généré par IA : recadrage, réglages et texte seulement.
# Usage, depuis la racine du dépôt : python assets/long-01-voitures/miniature-v4.py
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import miniatures_hpb as mh  # noqa: E402

SRC = ROOT / 'assets/sources-reelles/ssc-road.mp4'
INSTANT = 13.0
OUT = ROOT / 'out/long-01-voitures-vitesse'
WORK = OUT / '_montage'
L, H = 1920, 1080
CADRE = (0, 0, 1920, 1080)  # image entière : source 1080p, pas d'agrandissement
REGLAGES = dict(luminosite=1.0, contraste=1.12, couleurs=1.15, nettete=dict(rayon=1.4, pourcent=60, seuil=2))
LIGNES = [mh.N('TOP 3'), mh.N('DES VOITURES'), mh.N('LES PLUS RAPIDES'), mh.N('2026')]
HAUT_TITRE = 540  # hauteur du bloc titre (plaques comprises) sur 1080
POS_TITRE = (52, 52)


def main():
    raw = WORK / 'miniature-v4-source.png'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(INSTANT), '-i', str(SRC),
                    '-frames:v', '1', str(raw)], check=True)
    im = Image.open(raw).convert('RGB').crop(CADRE).resize((L, H), Image.Resampling.LANCZOS)
    im.save(WORK / 'miniature-v4-avant.jpg', quality=95)
    r = REGLAGES
    im = ImageEnhance.Brightness(im).enhance(r['luminosite'])
    im = ImageEnhance.Contrast(im).enhance(r['contraste'])
    im = ImageEnhance.Color(im).enhance(r['couleurs'])
    n = r['nettete']
    im = im.filter(ImageFilter.UnsharpMask(n['rayon'], n['pourcent'], n['seuil']))
    im.save(WORK / 'miniature-v4-apres.jpg', quality=95)
    out = im.convert('RGBA')

    bloc, _ = mh.bloc_cale(LIGNES, 'course')
    bloc = bloc.crop(bloc.getbbox())
    k = HAUT_TITRE / bloc.height
    bloc = bloc.resize((round(bloc.width * k), HAUT_TITRE), Image.Resampling.LANCZOS)
    out.alpha_composite(bloc, POS_TITRE)
    logo = mh.logo_valide().resize((220, 220), Image.Resampling.LANCZOS)
    out.alpha_composite(logo, (L - 220 - 40, 30))

    fin = out.convert('RGB')
    fin.save(OUT / 'miniature-youtube-v4.jpg', quality=92)
    tel = Image.new('RGB', (360 + 16 + 168, 202), (18, 21, 28))
    tel.paste(fin.resize((360, 202), Image.Resampling.LANCZOS), (0, 0))
    tel.paste(fin.resize((168, 94), Image.Resampling.LANCZOS), (376, 0))
    tel.save(WORK / 'miniature-v4-mobile.png')
    av = Image.new('RGB', (960, 270))
    av.paste(Image.open(WORK / 'miniature-v4-avant.jpg').resize((480, 270)), (0, 0))
    av.paste(Image.open(WORK / 'miniature-v4-apres.jpg').resize((480, 270)), (480, 0))
    av.save(WORK / 'miniature-v4-reglages.jpg', quality=92)
    (WORK / 'miniature-v4-manifeste.json').write_text(json.dumps(dict(
        demande='Marc, 15 novembre 2026 : « s’inspirer du short, pour le titre et la photo », « regarde sur le compte youtube »',
        modele='Short YouTube kdbAWhNzqpI « Trois voitures de série qui ont dépassé les 450 km/h », image affichée sur la chaîne',
        source='SSC North America, film « SSC Tuatara » (assets/sources-reelles/ssc-road.mp4, 1920x1080), plan déjà crédité au dossier 14',
        instant_s=INSTANT, reglages=REGLAGES, style='course (maquette 07) de miniatures_hpb.py, quatre lignes, bloc à 540 px de haut',
        texte=[l['texte'] for l in LIGNES], logo='hpb-reference-propre-v1.png, 220x220 en haut à droite'),
        ensure_ascii=False, indent=1), encoding='utf-8')
    print(OUT / 'miniature-youtube-v4.jpg', (OUT / 'miniature-youtube-v4.jpg').stat().st_size, 'octets ; bloc', bloc.size)


if __name__ == '__main__':
    main()
