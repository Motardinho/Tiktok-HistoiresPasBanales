# Miniature YouTube 16:9 de la vidéo longue, version 3 (15 novembre 2026) : reprise du short 14
# (out/miniatures-v4/14.jpg) à la demande de Marc, « s'inspirer du short, pour le titre et la photo ».
# Même titre, même style magazine (maquette 09, fond noirci derrière le titre), même source photo : la vue embarquée
# officielle VBOX Motorsport IgXuBBe017Q de la SSC Tuatara, prise ici au moment de la pointe (295 mph / 474 km/h).
# Rien n'est généré par IA : recadrage, réglages et texte seulement.
# Usage, depuis la racine du dépôt : python assets/long-01-voitures/miniature-v3.py
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import miniatures_hpb as mh  # noqa: E402

SRC = ROOT / 'assets/sources-reelles/ssc-vbox-2022.mp4'
INSTANT = 51.0  # compteur VBOX à 295 mph / 474 km/h
OUT = ROOT / 'out/long-01-voitures-vitesse'
WORK = OUT / '_montage'
L, H = 1920, 1080
# Réglages du dossier 14 dans miniatures_hpb.py (défauts de preparer_fond), netteté réduite : source 1080p.
REGLAGES = dict(contraste=1.14, couleurs=1.28, luminosite=1.0, nettete=dict(rayon=1.6, pourcent=60, seuil=2))
LIGNES = [mh.N('TOP 3', 216), mh.N('VOITURES', 154), mh.P('LES PLUS|RAPIDES', 129)]  # identiques au dossier 14
HAUT_TITRE = 560  # hauteur des lettres du bloc sur 1080
POS_TITRE = (70, 56)  # coin haut gauche des lettres


def main():
    raw = WORK / 'miniature-v3-source.png'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(INSTANT), '-i', str(SRC),
                    '-frames:v', '1', str(raw)], check=True)
    im = Image.open(raw).convert('RGB').resize((L, H), Image.Resampling.LANCZOS)
    im.save(WORK / 'miniature-v3-avant.jpg', quality=95)
    r = REGLAGES
    im = ImageEnhance.Contrast(im).enhance(r['contraste'])
    im = ImageEnhance.Color(im).enhance(r['couleurs'])
    im = ImageEnhance.Brightness(im).enhance(r['luminosite'])
    n = r['nettete']
    im = im.filter(ImageFilter.UnsharpMask(n['rayon'], n['pourcent'], n['seuil']))
    im.save(WORK / 'miniature-v3-apres.jpg', quality=95)
    out = im.convert('RGBA')

    bloc, _ = mh.bloc_titre(LIGNES, 'magazine')
    bb = bloc.getbbox()
    k = HAUT_TITRE / (bb[3] - bb[1])
    bloc = bloc.resize((round(bloc.width * k), round(bloc.height * k)), Image.Resampling.LANCZOS)
    bb = bloc.getbbox()
    x0, y0 = POS_TITRE[0] - bb[0], POS_TITRE[1] - bb[1]
    halo = mh.halo_sombre(bloc)  # déborde de 260 px de chaque côté
    calque = Image.new('RGBA', (L, H), (0, 0, 0, 0))
    calque.paste(halo, (x0 - 260, y0 - 260), halo)
    out.alpha_composite(calque)
    calque = Image.new('RGBA', (L, H), (0, 0, 0, 0))
    calque.paste(bloc, (x0, y0), bloc)
    out.alpha_composite(calque)
    titre = mh.boite_opaque(calque)
    logo = mh.logo_valide().resize((220, 220), Image.Resampling.LANCZOS)
    out.alpha_composite(logo, (L - 220 - 40, 30))

    fin = out.convert('RGB')
    fin.save(OUT / 'miniature-youtube-v3.jpg', quality=92)
    tel = Image.new('RGB', (360 + 16 + 168, 202), (18, 21, 28))
    tel.paste(fin.resize((360, 202), Image.Resampling.LANCZOS), (0, 0))
    tel.paste(fin.resize((168, 94), Image.Resampling.LANCZOS), (376, 0))
    tel.save(WORK / 'miniature-v3-mobile.png')
    av = Image.new('RGB', (960, 270))
    av.paste(Image.open(WORK / 'miniature-v3-avant.jpg').resize((480, 270)), (0, 0))
    av.paste(Image.open(WORK / 'miniature-v3-apres.jpg').resize((480, 270)), (480, 0))
    av.save(WORK / 'miniature-v3-reglages.jpg', quality=92)
    (WORK / 'miniature-v3-manifeste.json').write_text(json.dumps(dict(
        demande='Marc, 15 novembre 2026 : « s’inspirer du short, pour le titre et la photo » (short 14, out/miniatures-v4/14.jpg)',
        source='VBOX Motorsport, YouTube IgXuBBe017Q « Go onboard the SSC Tuatara as it hits a staggering 295mph! », 1920x1080',
        instant_s=INSTANT, compteur='295 mph / 474 km/h (pointe du 14 mai 2022)', reglages=REGLAGES,
        style='magazine (maquette 09) de miniatures_hpb.py, fond noirci halo_sombre, tailles du dossier 14',
        texte=[l['texte'] for l in LIGNES], boite_titre=titre, logo='hpb-reference-propre-v1.png, 220x220 en haut à droite'),
        ensure_ascii=False, indent=1), encoding='utf-8')
    print(OUT / 'miniature-youtube-v3.jpg', (OUT / 'miniature-youtube-v3.jpg').stat().st_size, 'octets ; titre', titre)


if __name__ == '__main__':
    main()
