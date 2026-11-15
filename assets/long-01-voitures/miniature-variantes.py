# Trois variantes de la miniature YouTube v4 de la vidéo longue (Marc, 15 novembre 2026 : « 3 variantes dans ce
# genre ») : même titre « TOP 3 / DES VOITURES / LES PLUS RAPIDES / 2026 », même style course et même logo que
# miniature-v4.py ; une vraie photo de chacune des trois voitures du top, en roulage.
# Rien n'est généré par IA : recadrage, réglages et texte seulement.
# Usage, depuis la racine du dépôt : python assets/long-01-voitures/miniature-variantes.py
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import miniatures_hpb as mh  # noqa: E402

OUT = ROOT / 'out/long-01-voitures-vitesse'
WORK = OUT / '_montage'
L, H = 1920, 1080
LIGNES = [mh.N('TOP 3'), mh.N('DES VOITURES'), mh.N('LES PLUS RAPIDES'), mh.N('2026')]

VARIANTES = [
    # Bugatti, « Chiron Super Sport 300+, record 2019 » (bugatti-record.mp4, 1920x1080 avec bandes noires de
    # 132 px) : la voiture du record sur la piste d'Ehra-Lessien. Cadre 16:9 pris dans l'image utile, voiture à droite.
    dict(nom='bugatti', src='assets/sources-reelles/bugatti-record.mp4', t=26.5, cadre=(469, 132, 1920, 948),
         credit='Bugatti, film du record 2019 (bugatti-record.mp4)', haut=470, voile=0.62,
         reglages=dict(luminosite=1.02, contraste=1.10, couleurs=1.12, nettete=dict(rayon=1.6, pourcent=70, seuil=2))),
    # SSC North America, film « SSC Tuatara » (ssc-road.mp4) : la Tuatara blanche de face dans les virages.
    dict(nom='ssc-face', src='assets/sources-reelles/ssc-road.mp4', t=19.5, cadre=(0, 0, 1920, 1080),
         credit='SSC North America, film « SSC Tuatara » (ssc-road.mp4)', haut=480,
         reglages=dict(luminosite=1.06, contraste=1.12, couleurs=1.15, nettete=dict(rayon=1.4, pourcent=60, seuil=2))),
    # BYD Global PWWamnhY9pE (3840x2160) : la Yangwang U9 Xtreme n° 01 sur la piste d'Abu Dhabi, tentative à 503 km/h.
    dict(nom='yangwang', src='assets/long-01-voitures/PWWamnhY9pE.mp4', t=204.35, cadre=(0, 0, 3840, 2160),
         credit='BYD Global, « YANGWANG U9X | 503.17km/h » (YouTube PWWamnhY9pE)', haut=500, voile=0.40,
         reglages=dict(luminosite=1.02, contraste=1.16, couleurs=1.18, nettete=dict(rayon=1.0, pourcent=60, seuil=3))),
]


def composer(v):
    raw = WORK / f'miniature-variante-{v["nom"]}-source.png'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(v['t']), '-i', str(ROOT / v['src']),
                    '-frames:v', '1', str(raw)], check=True)
    im = Image.open(raw).convert('RGB').crop(v['cadre']).resize((L, H), Image.Resampling.LANCZOS)
    avant = im.copy()
    r = v['reglages']
    im = ImageEnhance.Brightness(im).enhance(r['luminosite'])
    im = ImageEnhance.Contrast(im).enhance(r['contraste'])
    im = ImageEnhance.Color(im).enhance(r['couleurs'])
    n = r['nettete']
    im = im.filter(ImageFilter.UnsharpMask(n['rayon'], n['pourcent'], n['seuil']))
    av = Image.new('RGB', (960, 270))
    av.paste(avant.resize((480, 270)), (0, 0))
    av.paste(im.resize((480, 270)), (480, 0))
    av.save(WORK / f'miniature-variante-{v["nom"]}-reglages.jpg', quality=92)
    out = im.convert('RGBA')
    if v.get('voile'):  # voile marine en haut, nul à la rangée 640 : le blanc du titre ressort sur un ciel clair
        masque = Image.new('L', (1, H))
        for y in range(H):
            masque.putpixel((0, y), round(255 * v['voile'] * max(0.0, 1 - y / 640) ** 1.3))
        sombre = Image.new('RGBA', (L, H), (5, 10, 38, 255))
        sombre.putalpha(masque.resize((L, H)))
        out.alpha_composite(sombre)
    bloc, _ = mh.bloc_cale(LIGNES, 'course')
    bloc = bloc.crop(bloc.getbbox())
    bloc = bloc.resize((round(bloc.width * v['haut'] / bloc.height), v['haut']), Image.Resampling.LANCZOS)
    out.alpha_composite(bloc, (52, 52))
    out.alpha_composite(mh.logo_valide().resize((220, 220), Image.Resampling.LANCZOS), (L - 220 - 40, 30))
    fin = out.convert('RGB')
    chemin = OUT / f'miniature-youtube-variante-{v["nom"]}.jpg'
    fin.save(chemin, quality=92)
    print(chemin, chemin.stat().st_size, 'octets')
    return fin


def main():
    vues = [Image.open(OUT / 'miniature-youtube-v4.jpg').convert('RGB')] + [composer(v) for v in VARIANTES]
    # Planche à taille téléphone (vignettes de 360 px, comme l'accueil YouTube mobile) : v4 puis les trois variantes.
    planche = Image.new('RGB', (2 * 360 + 3 * 16, 2 * 202 + 3 * 16), (18, 21, 28))
    for i, v in enumerate(vues):
        planche.paste(v.resize((360, 202), Image.Resampling.LANCZOS), (16 + (i % 2) * 376, 16 + (i // 2) * 218))
    planche.save(WORK / 'miniature-variantes-mobile.png')
    (WORK / 'miniature-variantes-manifeste.json').write_text(json.dumps(dict(
        demande='Marc, 15 novembre 2026 : « 3 variantes dans ce genre » (après la v4 sur le modèle du Short kdbAWhNzqpI)',
        style='course (maquette 07) de miniatures_hpb.py, quatre lignes, logo hpb-reference-propre-v1.png 220x220 en haut à droite',
        texte=[l['texte'] for l in LIGNES],
        variantes=[{k: v.get(k) for k in ('nom', 'src', 't', 'cadre', 'credit', 'haut', 'voile', 'reglages')} for v in VARIANTES]),
        ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
