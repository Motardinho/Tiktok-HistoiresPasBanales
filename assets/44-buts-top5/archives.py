"""Dossier 44 : chaque but en entier, en 1080x1920, cadrage serré qui suit l'action.

Même procédé que assets/40-buts-degueulasses/archives.py (fenêtre carrée centrée sur l'action par images
clés, posée sur un fond flou du même plan, sans logo de diffuseur ni tableau de score), mais chaque extrait
couvre un plan entier du réalisateur d'origine : l'action en direct jusqu'au ballon au fond, puis le ralenti.
Les sources restent dans assets/40-buts-degueulasses/.
Lancer depuis ce dossier : python archives.py [clé ...]
"""
import subprocess
import sys

SRC = '../40-buts-degueulasses/'
CY = 960
W, H = 1920, 1080

INTERDIT = {
    'm7Ra_FafbEQ.mp4': [(1020, 0, 1200, 58)],                                # SBS HD (source 1280x720)
    'CYJGpH5n-KM.mp4': [(1730, 30, 1870, 165)],                              # écusson Man United
    'd8LDD9AJcmI.mp4': [(1040, 45, 1840, 115), (1590, 870, 1730, 1010)],     # score, logo Bundesliga
    'PPHy9M2daTc.mp4': [(10, 10, 160, 170)],                                 # Premier League
    'Bnsc-7TJDUI.mp4': [(1570, 25, 1840, 150)],                              # Spurs TV
}

# clé : (source, début, durée source, côté de la fenêtre, [(seconde source, x centre, y centre), ...], ralentissement)
SEGMENTS = {
    # N°5 Rob Green : fin de l'action en direct (plan large), puis le ralenti au ras du sol d'un seul tenant
    'green-direct': ('m7Ra_FafbEQ.mp4', 21.1, 2.7, 660, [(21.0, 720, 390), (21.4, 640, 390), (22.0, 400, 390), (22.5, 380, 390), (23.0, 330, 390), (23.8, 330, 390)], 1),
    'green-ralenti': ('m7Ra_FafbEQ.mp4', 23.85, 7.9, 660, [(23.9, 790, 420), (24.5, 820, 400), (25.0, 600, 400), (25.5, 330, 400), (26.0, 380, 420),
                                                            (26.5, 800, 400), (27.0, 600, 420), (27.5, 640, 420), (28.0, 950, 400), (28.5, 950, 400),
                                                            (29.0, 800, 400), (29.5, 640, 400), (30.0, 520, 400), (30.5, 450, 400), (31.0, 400, 400), (31.8, 400, 400)], 1),
    # N°4 Chicharito : le centre de Valencia, l'action en direct, le ralenti (ballon sur le visage), la célébration
    'chicha-centre': ('CYJGpH5n-KM.mp4', 6.25, 1.95, 900, [(6.3, 800, 540), (7.0, 930, 540), (8.0, 850, 540)], 1),
    'chicha-direct': ('CYJGpH5n-KM.mp4', 8.28, 3.56, 900, [(8.3, 750, 540), (9.0, 950, 520), (9.5, 1050, 500), (11.9, 1100, 500)], 1),
    'chicha-ralenti': ('CYJGpH5n-KM.mp4', 12.02, 3.38, 900, [(12.1, 750, 600), (12.8, 800, 600), (13.4, 750, 600), (13.9, 850, 600), (14.5, 1250, 600), (15.4, 1250, 600)], 1.36),
    'chicha-joie': ('CYJGpH5n-KM.mp4', 15.65, 2.55, 900, [(15.7, 850, 480)], 1),
    # N°3 Kießling : le corner, l'action en direct, le ralenti derrière le but (le ballon entre par le côté du filet)
    'kiess-corner': ('d8LDD9AJcmI.mp4', 0.5, 1.86, 900, [(0.6, 860, 630)], 1),
    'kiess-direct': ('d8LDD9AJcmI.mp4', 2.4, 3.5, 740, [(2.4, 1350, 492), (2.85, 1350, 492), (3.33, 1100, 500), (3.84, 950, 500), (4.36, 900, 500),
                                                        (4.87, 950, 500), (5.9, 900, 500)], 1),
    'kiess-ralenti': ('d8LDD9AJcmI.mp4', 18.9, 6.3, 900, [(18.9, 850, 600), (19.6, 850, 600), (20.1, 1000, 600), (20.5, 900, 600), (21.0, 950, 600),
                                                          (21.5, 950, 600), (22.0, 800, 600), (22.5, 700, 600), (23.0, 750, 620), (25.3, 800, 620)], 1),
    # N°2 Darren Bent : l'action en direct (le ballon de plage est sur la pelouse), puis le ralenti de la frappe et du but
    'bent-direct': ('PPHy9M2daTc.mp4', 266.45, 5.25, 900, [(266.4, 800, 480), (267.0, 750, 480), (267.5, 700, 480), (268.0, 1000, 480),
                                                           (268.5, 1050, 480), (269.0, 1100, 480), (271.7, 1100, 480)], 1),
    'bent-ralenti': ('PPHy9M2daTc.mp4', 280.0, 6.55, 1000, [(280.0, 1420, 540), (280.5, 900, 540), (281.0, 660, 540), (281.5, 900, 540), (282.0, 900, 540),
                                                            (282.5, 900, 560), (282.8, 760, 580), (283.3, 900, 580), (283.7, 1000, 580), (284.0, 1150, 580),
                                                            (284.3, 900, 580), (284.9, 700, 580), (285.4, 950, 580), (285.9, 1150, 580)], 1),
    # N°1 Kane : Eriksen tire le coup franc, l'action en direct, le ralenti, Kane qui réclame le but
    'kane-eriksen': ('Bnsc-7TJDUI.mp4', 52.7, 2.2, 1000, [(52.8, 950, 580)], 1),
    'kane-direct': ('Bnsc-7TJDUI.mp4', 54.98, 3.82, 800, [(55.0, 1400, 550), (56.0, 1450, 550), (56.5, 1250, 550), (57.0, 1150, 550), (57.5, 950, 550),
                                                          (58.0, 1150, 550), (58.8, 1050, 550)], 1),
    'kane-ralenti': ('Bnsc-7TJDUI.mp4', 67.8, 5.5, 900, [(67.8, 1050, 620), (70.0, 1000, 620), (70.5, 1050, 630), (71.0, 1150, 630), (71.5, 1400, 630),
                                                         (72.05, 1450, 630), (72.12, 1000, 620), (73.3, 1000, 620)], 1),
    'kane-reclame': ('Bnsc-7TJDUI.mp4', 58.9, 6.05, 900, [(58.9, 870, 602), (60.0, 900, 602), (60.5, 1150, 602), (61.0, 1350, 602), (62.0, 1250, 602),
                                                          (62.5, 1400, 602), (63.0, 1150, 602), (64.9, 1250, 602)], 1),
}


def _window(src, size, cx, cy):
    """Coin haut gauche de la fenêtre, borné à l'image, en vérifiant qu'elle évite les zones interdites."""
    w, h = size if isinstance(size, tuple) else (size, size)
    sw, sh = (1280, 720) if src.startswith('m7Ra') else (W, H)
    x = min(max(cx - w / 2, 0), sw - w)
    y = min(max(cy - h / 2, 0), sh - h)
    for (a, b, c, d) in INTERDIT.get(src, []):
        assert x >= c or x + w <= a or y >= d or y + h <= b, f'{src} : fenêtre {x:.0f},{y:.0f} {w}x{h} sur la zone {a},{b},{c},{d}'
    return round(x), round(y)


def _expr(points):
    """Interpolation linéaire par morceaux en fonction de t (secondes depuis le début du segment)."""
    if len(points) == 1:
        return str(points[0][1])
    e = str(points[-1][1])
    for (t0, v0), (t1, v1) in reversed(list(zip(points, points[1:]))):
        e = f'if(lt(t,{t1:.3f}),{v0}+({v1}-{v0})*(t-{t0:.3f})/{t1 - t0:.3f},{e})'
    return f'if(lt(t,{points[0][0]:.3f}),{points[0][1]},{e})'


def render(key):
    src, start, dur, size, track, lent = SEGMENTS[key]
    w, h = size if isinstance(size, tuple) else (size, size)
    pts = [(t - start, *_window(src, size, cx, cy)) for t, cx, cy in track]
    xs, ys = _expr([(t, x) for t, x, _ in pts]), _expr([(t, y) for t, _, y in pts])
    out_h = round(1080 * h / w / 2) * 2
    slow = f'setpts={lent}*PTS,' if lent != 1 else ''
    graph = ('[0:v]split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85[bg];'
             f"[a]crop={w}:{h}:'{xs}':'{ys}',scale=1080:{out_h}:flags=lanczos[fg];"
             f'[bg][fg]overlay=0:{CY - out_h // 2},setsar=1,{slow}fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', SRC + src,
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    f'arch-{key}.mp4'], check=True)
    print(key, 'ok', f'{w}x{h} px source -> {1080 / w:.2f}x', flush=True)


if __name__ == '__main__':
    for k in sys.argv[1:] or SEGMENTS:
        render(k)
