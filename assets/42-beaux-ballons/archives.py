"""Dossier 42 : extraits officiels en 1080x1920, image entière sur fond flou (procédé des dossiers 27 et 40).

Chaque extrait est recadré (zone x, y, w, h dans la source 1920x1080) pour exclure logos FIFA TV / FIFA+ / UEFA,
tableaux de score et bandes floues des archives 4:3, réduit à 1080 de large et posé à y = TOP sur un fond
flou assombri du même plan. Lancer depuis ce dossier : python archives.py [clé ...]
Les photos de ballons (fichiers .jpg) passent par le même procédé : ballon entier, net, sur fond flou.
"""
import subprocess
import sys

TOP = 610  # sous le bandeau de rang (y 380-600), au-dessus des sous-titres

# clé : (source, début, durée, (x, y, w, h))
SEGMENTS = {
    'fra26': ('yt/n3JDGlOwMJ4.mp4', 12.5, 7, (240, 160, 1440, 810)),      # France - Sénégal 2026, score haut gauche exclu
    'por-but': ('yt/1ykn3lx-I0w.mp4', 50.5, 7.5, (240, 150, 1400, 788)),   # Portugal - Uruguay 2022 : Ronaldo célèbre, ralenti du centre
    'jab-tete': ('yt/lo8_Ox0YkWI.mp4', 303, 4, (240, 90, 1440, 810)),     # finale 2010, ballon en l'air, tête de Puyol
    'jab-sol': ('yt/lo8_Ox0YkWI.mp4', 471, 4, (240, 90, 1440, 810)),      # finale 2010, ballon au sol
    'jab-but': ('yt/lo8_Ox0YkWI.mp4', 544, 4, (240, 90, 1440, 810)),      # finale 2010, Iniesta face au gardien
    'etr': ('yt/5MLZbUZJDTQ.mp4', 22, 8, (240, 90, 1440, 810)),           # Italie 1990, ballon au sol
    'uefa': ('yt/Qn1PJgdLlaI.mp4', 0.8, 16, (100, 130, 1500, 844)),       # UEFA, gros plans du Beau Jeu, logo UEFA exclu
    'azt': ('yt/eTbAZMvz1us.mp4', 145.5, 3.5, (300, 40, 1320, 742)),      # 1986, Maradona (bandes floues 4:3 exclues)
    'tg-avant': ('yt/jb16JvUCVQs.mp4', 41.5, 2.5, (160, 190, 1320, 742)), # finale 2006, Zidane et le ballon doré, logo FIFA TV exclu
    'tg-coup': ('yt/jb16JvUCVQs.mp4', 164.5, 4, (160, 190, 1320, 742)),   # finale 2006, coup de tête
    'tango': ('yt/g4v4GlEA2yQ.mp4', 223.2, 2.6, (300, 40, 1320, 742)),    # finale 1978, Kempes et le Tango
    'telstar': ('yt/v7NlB2xlijQ.mp4', 502.8, 3.5, (240, 120, 1440, 810)), # finale 1970, Pelé et le Telstar
    'telstar2': ('yt/v7NlB2xlijQ.mp4', 18, 3.5, (240, 120, 1440, 810)),   # finale 1970, duel avec le ballon
    'z98-0': ('yt/fE8AEnbvn9s.mp4', 226.3, 2.8, (240, 120, 1440, 810)),   # finale 1998, corner de la première tête
    'z98-1': ('yt/fE8AEnbvn9s.mp4', 222.8, 2.4, (240, 100, 1440, 810)),   # finale 1998, Zidane de près
    'z98-2': ('yt/fE8AEnbvn9s.mp4', 233.8, 4.2, (240, 120, 1440, 810)),   # première tête, ralenti
    'z98-3': ('yt/fE8AEnbvn9s.mp4', 357.8, 4.4, (240, 120, 1440, 810)),   # Zidane embrasse son maillot
    'z98-4': ('yt/fE8AEnbvn9s.mp4', 606, 6, (240, 90, 1440, 810)),        # les Bleus soulèvent la Coupe
}


# Photos de ballons : clé : (photo, (centre x, centre y) relatifs, largeur du cadre / largeur de la photo).
# Cadre 1,2:1 réduit à 1080x900, léger zoom avant (6 % sur 6 s), sur fond flou de la même photo.
PHOTOS = {
    'p-trionda-iss': ('photos/photo-trionda-iss.jpg', (.50, .42), .58),
    'p-maradona': ('photos/photo-maradona.jpg', (.45, .36), 1.0),  # main de Dieu : main et ballon sous le logo
    'p-etrusco': ('photos/photo-etrusco3.jpg', (.38, .50), .70),   # gros plan voulu : les têtes de lion
}

# Ballon entier (demande de Marc du 12 nov. 2026 : « des photos où on le voit vraiment bien »).
# clé : (photo, centre du ballon (x, y) relatifs, diamètre du ballon / largeur de la photo).
# Carré autour du ballon avec 8 % de marge de chaque côté quand la photo le permet, affiché en 1080x1080.
BALLONS = {
    'p-trionda': ('photos/photo-trionda.jpg', (.42, .485), .455),
    'p-jabulani': ('photos/photo-jab-demi.jpg', (.512, .835), .225),  # vrai Jabulani, ballon officiel des demi-finales 2010
    'p-alrihla': ('photos/photo-alrihla.jpg', (.52, .49), .73),
    'p-beaujeu': ('photos/photo-beaujeu.jpg', (.50, .49), .42),
    'p-etrusco-entier': ('photos/photo-etrusco2.jpg', (.525, .34), .84),
    'p-azteca': ('photos/photo-azteca2.jpg', (.465, .35), .92),
    'p-teamgeist': ('photos/photo-teamgeist.jpg', (.49, .52), .645),
    'p-tango': ('photos/photo-tango2.jpg', (.515, .33), .92),
    'p-telstar': ('photos/photo-telstar2.jpg', (.52, .41), .79),
    'p-tricolore': ('photos/photo-tricolore2.jpg', (.50, .50), 1.0),
}


def render_ballon(key, dur=6.0):
    from PIL import Image
    src, (cx, cy), diam = BALLONS[key]
    W, H = Image.open(src).size
    d = diam * W
    side = round(min(d * 1.16, W, H)) // 2 * 2
    x = min(max(round(cx * W - side / 2), 0), W - side)
    y = min(max(round(cy * H - side / 2), 0), H - side)
    zoom = max(0.0, min(.05, side / d - 1.06))  # zoom avant seulement s'il reste de la marge autour du ballon
    n = round(dur * 30)
    graph = (f'[0:v]crop={side}:{side}:{x}:{y},split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85,fps=30[bg];'
             f"[a]scale=2160:2160:flags=lanczos,zoompan=z='1+{zoom:.3f}*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
             f":d=1:s=1080x1080:fps=30[fg];"
             f'[bg][fg]overlay=0:{TOP}:shortest=1,setsar=1,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '30', '-i', src, '-frames:v', str(n),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    f'arch-{key}.mp4'], check=True)
    print(key, 'ok', side, f'ballon {round(d * 1080 / side)} px', flush=True)


def render_photo(key, dur=6.0):
    src, (cx, cy), frac, *top = PHOTOS[key]
    top = top[0] if top else TOP
    from PIL import Image
    W, H = Image.open(src).size
    w = round(W * frac)
    h = min(round(w / 1.2), H)
    w = round(h * 1.2)
    x = min(max(round(cx * W - w / 2), 0), W - w)
    y = min(max(round(cy * H - h / 2), 0), H - h)
    n = round(dur * 30)
    graph = (f'[0:v]crop={w}:{h}:{x}:{y},split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85,fps=30[bg];'
             f"[a]scale=2160:1800:flags=lanczos,zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
             f":d=1:s=1080x900:fps=30[fg];"
             f'[bg][fg]overlay=0:{top}:shortest=1,setsar=1,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '30', '-i', src, '-frames:v', str(n),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    f'arch-{key}.mp4'], check=True)
    print(key, 'ok', w, h, flush=True)


def render(key):
    if key in BALLONS:
        return render_ballon(key)
    if key in PHOTOS:
        return render_photo(key)
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
    for k in sys.argv[1:] or [*SEGMENTS, *PHOTOS, *BALLONS]:
        render(k)
