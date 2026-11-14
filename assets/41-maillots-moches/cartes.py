"""Dossier 41 : plans verticaux 1080x1920 des maillots.

- Photos (consigne de Marc du 12 nov. 2026 : photos des maillots, séquences intercalées) :
  'carte' = photo entière posée sur un fond flou assombri de la même photo ;
  'plein' = recadrage 9:16 plein écran autour d'un point (cx, cy), pour les photos en portrait.
- Extraits vidéo (procédé des dossiers 27 et 40) : zone (x, y, w, h) qui exclut logos de chaîne,
  score et sous-titres incrustés, réduite à 1080 de large et posée à y = TOP sur un fond flou du même plan.
Lancer depuis ce dossier : python cartes.py [clé ...]
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

TOP = 610  # sous le bandeau de rang (y 380-600), comme le dossier 40
OUT = Path('plans')

# clé : (fichier, mode, recadrage source (x0, y0, x1, y1) ou None, centre (cx, cy) pour 'plein')
PHOTOS = {
    'aux-photo': ('auxerre/photos/S10AHCIJDt1CaqU.jpg', 'plein', None, (.5, .45)),
    'bdx-detail': ('bordeaux/photos/uksoccershop-bordeaux-16-17-kit-shirt-detail.jpg', 'carte', None, None),
    'omj-face': ('om-jean/photos/footyheadlines-om-away-1314.jpg', 'carte', (150, 150, 1900, 1950), None),
    'olo-aouar': ('ol-orange/photos/footballfashion-ol-third-8.jpg', 'carte', None, None),
    'omr-face': ('om-reversible/photos/cfs-third-1213.jpg', 'carte', None, None),
    'akhenaton': ('om-reversible/photos/photo-akhenaton-charrues-2018.jpg', 'carte', None, None),
    'psg-face': ('psg-lv/photos/cfs-away-0607-a.jpg', 'carte', None, None),
    'psg-motif': ('psg-lv/photos/cfs-away-0607-a.jpg', 'carte', (1150, 250, 1950, 1050), None),
    'lumiere': ('photos/photo-lumiere.jpg', 'carte', None, None),
    'ol3d-face': ('ol-3d/photos/cfs-third-1213-3d.jpg', 'carte', None, None),
    'ol3d-motif': ('ol-3d/photos/cfs-third-1213-3d.jpg', 'carte', (850, 120, 2050, 820), None),
}

# clé : (source, début, durée, (x, y, w, h))
SEGMENTS = {
    'aux60': ('auxerre/U-SoroHDbwo.mkv', 58.0, 5, (0, 75, 960, 645)),     # Canal+ en haut à droite exclu
    'aux140': ('auxerre/U-SoroHDbwo.mkv', 138.5, 4, (0, 75, 960, 645)),
    'aux160': ('auxerre/U-SoroHDbwo.mkv', 158.5, 4, (0, 75, 960, 645)),
    'bdx92': ('bordeaux/_GGWWMSebXg.mkv', 90.5, 4, (160, 0, 960, 720)),
    'bdx141': ('bordeaux/MmLHQIuT7JY.mkv', 140.0, 4, (240, 0, 960, 720)),
    'omj171': ('om-jean/6cejUILWtoA.mkv', 170.0, 4, (160, 0, 960, 720)),
    'omj173': ('om-jean/6cejUILWtoA.mkv', 172.4, 4, (200, 0, 960, 720)),
    'olo61': ('ol-orange/FF6BxnNzftM.webm', 60.2, 4, (240, 0, 1440, 1080)),   # logo UEFA exclu
    'olo24': ('ol-orange/FF6BxnNzftM.webm', 22.8, 4, (120, 0, 1440, 1080)),
    'evi178': ('evian/SFApSf1PsK4.mp4', 176.0, 4, (240, 0, 960, 720)),
    'evi116': ('evian/Nj6Om1Ei_wE.mp4', 114.8, 4, (160, 0, 960, 720)),
    'evi95': ('evian/Nj6Om1Ei_wE.mp4', 93.5, 4, (160, 0, 960, 720)),
    'omr63': ('om-reversible/ftjrCj0NsAU.mp4', 63.4, 2.2, (160, 0, 960, 600)),  # sous-titres anglais exclus
    'psg73': ('psg-lv/xnFCp6jePFk-850.mp4', 71.5, 4, (210, 130, 680, 590)),   # score, logo et horloge exclus
    'bas100': ('bastia/tC9bSNIqJAQ.mp4', 98.5, 4, (160, 0, 960, 720)),
    'bas60': ('bastia/tC9bSNIqJAQ.mp4', 58.5, 4, (160, 0, 960, 720)),
    'bas105': ('bastia/r6XiH_vsVUw.mp4', 103.5, 4, (160, 0, 960, 720)),
    'ol3d27': ('ol-3d/lWqsp24_PfU.mp4', 26.0, 4, (240, 0, 1440, 1080)),
    'ol3d78': ('ol-3d/lWqsp24_PfU.mp4', 77.0, 4, (240, 0, 1440, 1080)),
    'ol3d70': ('ol-3d/lWqsp24_PfU.mp4', 68.0, 4, (240, 0, 1440, 1080)),
}


def photo(key):
    path, mode, box, centre = PHOTOS[key]
    im = Image.open(path).convert('RGB')
    if box:
        im = im.crop(box)
    if mode == 'plein':
        s = max(1080 / im.width, 1920 / im.height)
        big = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        cx, cy = centre
        x = min(max(round(big.width * cx - 540), 0), big.width - 1080)
        y = min(max(round(big.height * cy - 960), 0), big.height - 1920)
        out = big.crop((x, y, x + 1080, y + 1920))
    else:
        s = max(1080 / im.width, 1920 / im.height)
        bg = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        x, y = (bg.width - 1080) // 2, (bg.height - 1920) // 2
        bg = bg.crop((x, y, x + 1080, y + 1920)).filter(ImageFilter.GaussianBlur(40))
        out = ImageEnhance.Brightness(bg).enhance(.6)
        f = min(1040 / im.width, 860 / im.height)
        fg = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
        out.paste(fg, ((1080 - fg.width) // 2, 1020 - fg.height // 2))
    out.save(OUT / f'{key}.png')
    print(key, 'ok', flush=True)


def segment(key):
    src, start, dur, (x, y, w, h) = SEGMENTS[key]
    graph = (f'[0:v]crop={w}:{h}:{x}:{y},split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85[bg];'
             '[a]scale=1080:-2:flags=lanczos[fg];'
             f'[bg][fg]overlay=0:{TOP},setsar=1,fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-i', src, '-t', str(dur),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    str(OUT / f'arch-{key}.mp4')], check=True)
    print(key, 'ok', flush=True)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for k in sys.argv[1:] or [*PHOTOS, *SEGMENTS]:
        photo(k) if k in PHOTOS else segment(k)
