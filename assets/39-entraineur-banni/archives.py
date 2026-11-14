"""Dossier 39 : vraies séquences en 1080x1920, image entière sur fond flou (procédé des dossiers 27 et 40).

Chaque extrait est recadré (x, y, w, h dans la source) pour exclure scores, logos de chaîne, incrustations
et sous-titres, réduit à 1080 de large et posé à y = TOP sur un fond flou assombri du même plan, son coupé.
Lancer depuis ce dossier : python archives.py [clé ...]
"""
import subprocess
import sys

TOP = 600

# clé : (source, début, durée, (x, y, w, h), description[, top propre au plan])
SEGMENTS = {
    'hong2002': ('TTuHlPD6eaY.mp4', 327.8, 3.5, (240, 60, 1440, 810), 'FIFA : Hong Myung-bo (n°20, brassard) célèbre son tir au but, Corée-Espagne 2002'),
    'stade2026': ('6k18EJY8zIc.mp4', 1.0, 3.0, (240, 135, 1440, 810), 'FIFA : Corée du Sud-Tchéquie, Mondial 2026, vue du stade'),
    'victoire': ('6k18EJY8zIc.mp4', 69.6, 2.8, (240, 135, 1440, 810), 'FIFA : joie des Coréens après l’égalisation contre la Tchéquie (victoire 2-1)'),
    'mexique': ('o_AAtfdVp3Y.mp4', 46.7, 2.2, (240, 135, 1440, 810), 'FIFA : but du Mexique, Mexique 1-0 Corée du Sud, ralenti dans le but'),
    'afsud': ('cZoaEEYtKhE.mp4', 87.0, 2.3, (240, 135, 1440, 810), 'FIFA : but de l’Afrique du Sud, Afrique du Sud 1-0 Corée du Sud'),
    'elimines': ('cZoaEEYtKhE.mp4', 107.85, 2.42, (0, 140, 1600, 900), 'FIFA : coup de sifflet final, le banc sud-africain fête la qualification'),
    'hong2026': ('zPkAhQe55kg.mp4', 50.0, 2.7, (200, 0, 1350, 760), 'KBS WORLD : Hong Myung-bo à la conférence de démission, 28 juin 2026, remonté au-dessus du titre', 420),
    'hong2014': ('ES8xyOVrGpY.mp4', 41.0, 2.6, (160, 20, 900, 506), 'Arirang News : Hong Myung-bo démissionne, 10 juillet 2014'),
    'salut': ('zPkAhQe55kg.mp4', 41.85, 3.1, (240, 40, 1440, 810), 'KBS WORLD : Hong Myung-bo s’incline devant la presse, Korea House, 28 juin 2026'),
    'supporters': ('D2YPWNSoPNA.mp4', 1200.0, 3.4, (0, 140, 1230, 692), 'Yonhap TV : supporters et policiers attendent la sélection, Incheon, 30 juin 2026'),
    'profil': ('zPkAhQe55kg.mp4', 64.0, 2.3, (240, 0, 1440, 810), 'KBS WORLD : Hong Myung-bo de profil pendant la conférence, 28 juin 2026'),
    'aeroport': ('D2YPWNSoPNA.mp4', 600.0, 3.8, (0, 140, 1230, 692), 'Yonhap TV : policiers déployés dans le hall des arrivées A d’Incheon, 30 juin 2026 vers 3 h 30'),
    'gwangju': ('TTuHlPD6eaY.mp4', 54.0, 4.3, (240, 100, 1440, 810), 'FIFA : stade de Gwangju en rouge pendant la séance de tirs au but, 22 juin 2002'),
    'tir': ('TTuHlPD6eaY.mp4', 325.0, 2.6, (0, 150, 1600, 900), 'FIFA : dernier tir au but de Hong Myung-bo, Corée-Espagne 2002'),
    'hong2026b': ('zPkAhQe55kg.mp4', 52.6, 1.1, (200, 0, 1350, 760), 'KBS WORLD : Hong Myung-bo lève les yeux, conférence de démission, 28 juin 2026'),
    'hong2026c': ('zPkAhQe55kg.mp4', 72.0, 2.4, (380, 110, 1100, 619), 'KBS WORLD : Hong Myung-bo lit sa déclaration de démission, 28 juin 2026, visage au-dessus des sous-titres'),
    'police': ('D2YPWNSoPNA.mp4', 2303.8, 2.0, (0, 175, 1600, 900), 'Yonhap TV : policier en gilet « POLICE » autour de la sélection, Incheon, 30 juin 2026'),
    'fin2002': ('TTuHlPD6eaY.mp4', 341.9, 4.2, (240, 100, 1440, 810), 'FIFA : les supporters et les joueurs coréens fêtent la demi-finale, 2002'),
}


def render(key):
    src, start, dur, (x, y, w, h), _, *top = SEGMENTS[key]
    top = top[0] if top else TOP
    graph = (f'[0:v]crop={w}:{h}:{x}:{y},split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85[bg];'
             '[a]scale=1080:-2:flags=lanczos[fg];'
             f'[bg][fg]overlay=0:{top},setsar=1,fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-i', 'sources/' + src, '-t', str(dur),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    f'arch-{key}.mp4'], check=True)
    print(key, 'ok', flush=True)


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(render, sys.argv[1:] or SEGMENTS))
