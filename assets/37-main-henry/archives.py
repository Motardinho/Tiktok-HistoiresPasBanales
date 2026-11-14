"""Dossier 37 : extraits officiels en 1080x1920, image entière sur fond flou (procédé des dossiers 27 et 40).

Chaque extrait est recadré (zone x, y, w, h dans la source) pour exclure logos de chaîne, bandeaux de nom,
scores et textes incrustés, réduit à 1080 de large et posé à y = TOP sur un fond flou assombri du même plan.
Lancer depuis ce dossier : python archives.py [clé ...]
"""
import subprocess
import sys

TOP = 610  # sous le bandeau de série et les bandeaux (y 380-600), au-dessus des sous-titres
LEQ = 'officiel/yt-Q52Vd0EEIE0.mp4'   # L'Équipe, « Main de Thierry Henry contre l'Irlande… », 19/11/2025, 1080p
INA = 'officiel/yt-z8StDPaxo88.mp4'   # INA Actu, 20 heures de France 2 du 19/11/2009, 512x288
F24 = 'officiel/yt-QxXpTNm6iSk.mp4'   # FRANCE 24, « La FIFA a acheté le silence de l'Irlande… », 05/06/2015, 720p
TF1 = 'officiel/yt-CkWyDnvqBkc.mp4'   # Téléfoot (TF1), « Thierry Henry revient sur sa main… », 23/07/2015, 1080p
AFP = 'officiel/yt-Wa_f47OPj_g.mp4'   # AFP, « France mutiny over Anelka expulsion », 21/06/2010, 640x480

L = (280, 160, 1480, 680)   # intérieur du cadre L'Équipe, sans étiquette rose, logo, autocollant ni sous-titre
I = (16, 30, 480, 200)      # 20 heures : sans score TF1 en haut, logo France 2 / ina.fr, mention IMAGES TF1 ni bandeau de nom

# clé : (source, début, durée, (x, y, w, h))
SEGMENTS = {
    'leq-hook': (LEQ, 105.5, 1.9, L),                    # Henry, le ballon contre la main, devant le but
    'ina-france': (INA, 123.0, 1.0, (16, 52, 480, 176)),                  # le match en direct, plan large (images TF1)
    'leq-keane': (LEQ, 90.0, 1.1, (280, 160, 1480, 600)),  # but de Keane, score 0-1 exclu
    'ina-large': (INA, 124.1, 1.7, (16, 52, 480, 176)),                   # plan large, prolongation
    'ina-arrive': (INA, 111.1, 1.4, I),                  # ralenti : le ballon arrive sur Henry
    'ina-henry': (INA, 112.5, 1.85, I),                   # ralenti : Henry contrôle de la main
    'leq-main': (LEQ, 102.3, 1.7, L),                    # gros plan : la main sur le ballon
    'leq-main2': (LEQ, 107.6, 1.2, L),                   # deuxième touche, devant Given
    'ina-centre': (INA, 114.6, 1.2, I),                  # le centre vers Gallas
    'leq-joie': (LEQ, 117.0, 2.3, (780, 160, 980, 470)),  # Henry exulte, texte « main de Dieu » exclu
    'tf1-fin': (TF1, 44.95, 1.95, (0, 150, 1700, 850)),    # après le match, Henry et Domenech (logo TF1 exclu)
    'ina-interview': (INA, 139.5, 4.6, (16, 8, 480, 215)),  # Henry au micro le soir du match
    'f24-unes': (F24, 4.0, 2.4, (0, 0, 1280, 600)),      # unes des journaux irlandais, logo FRANCE 24 exclu
    'f24-delaney': (F24, 25.0, 2.8, (0, 0, 1280, 520)),  # John Delaney, bandeau de nom exclu
    'f24-fifa': (F24, 16.0, 1.6, (0, 0, 1280, 600)),     # siège de la FIFA, drapeaux
    'f24-fifa2': (F24, 19.0, 2.4, (0, 0, 1280, 600)),    # siège de la FIFA
    'ina-angle2': (INA, 134.5, 2.6, (16, 52, 480, 176)),  # deuxième angle, derrière le but
    'afp-bus': (AFP, 47.25, 3.7, (0, 0, 640, 420)),       # Knysna : les Bleus regagnent leur bus
    'afp-domenech': (AFP, 100.0, 2.8, (0, 0, 640, 420)),  # Knysna : Domenech seul face à la presse
}


def render(key):
    src, start, dur, (x, y, w, h) = SEGMENTS[key]
    graph = (f'[0:v]crop={w}:{h}:{x}:{y},split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85[bg];'
             '[a]scale=1080:-2:flags=lanczos[fg];'
             f'[bg][fg]overlay=0:{TOP},setsar=1,fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-i', src, '-t', str(dur),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    f'arch-{key}.mp4'], check=True)
    print(key, 'ok', flush=True)


if __name__ == '__main__':
    for k in sys.argv[1:] or SEGMENTS:
        render(k)
