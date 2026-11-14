"""Dossier 40 : extraits des buts en 1080x1920, cadrage serré qui suit l'action (révision du 12 novembre 2026).

Première version : image entière 16:9 sur fond flou, l'action restait trop petite (retour de Marc :
« y'en a qu'on ne voit pas assez bien »). Chaque plan a maintenant sa propre fenêtre, carrée de
côté `cote` pixels source (4:3 pour l'interview à deux), centrée sur l'action par images clés (seconde de la source, x, y)
interpolées linéairement, réduite ou agrandie à 1080x1080 et posée au centre de l'écran
(y 420-1500) sur un fond flou assombri du même plan. Les fenêtres excluent logos de diffuseur,
tableaux de score et filigranes (bornes notées par source).
Lancer depuis ce dossier : python archives.py [clé ...] ; python archives.py photos
"""
import subprocess
import sys

CY = 960  # centre vertical de l'extrait à l'écran : sous le bandeau de série, au-dessus des sous-titres
W, H = 1920, 1080

# Zones interdites par source (x0, y0, x1, y1) : logos, scores, filigranes
INTERDIT = {
    '8DShcsZSVQg.mp4': [(0, 0, 250, 1080), (1670, 0, 1920, 1080)],          # bandes noires du 4:3
    'HB3JnHb_IG4.mp4': [(1640, 20, 1860, 130)],                              # UEFA
    'm7Ra_FafbEQ.mp4': [(1020, 0, 1200, 58)],                                # SBS HD (source 1280x720)
    '0iXX_xN05Cg.mp4': [(0, 20, 700, 200), (1640, 20, 1890, 110)],           # score LIV-EVE, LFCTV
    'GrsEAvRerTg.mp4': [(0, 0, 620, 100), (1480, 40, 1730, 195)],            # score FRA-CRO, FIFA TV
    'rtFGpfrdlMI.mp4': [(1650, 30, 1840, 125)],                              # UEFA
    'CYJGpH5n-KM.mp4': [(1730, 30, 1870, 165)],                              # écusson Man United
    'd8LDD9AJcmI.mp4': [(1040, 45, 1840, 115), (1590, 870, 1730, 1010)],     # score, logo Bundesliga
    'PPHy9M2daTc.mp4': [(10, 10, 160, 170)],                                 # Premier League
    'Bnsc-7TJDUI.mp4': [(1570, 25, 1840, 150)],                              # Spurs TV
    'pehSmaHn5Tk.mp4': [(0, 0, 230, 70)],                                    # Sky Sports
}

# clé : (source, début, durée, côté de la fenêtre, [(seconde source, x centre, y centre), ...])
SEGMENTS = {
    'collymore': ('8DShcsZSVQg.mp4', 20.2, 4.2, 720, [(20.3, 760, 580), (20.5, 760, 580), (21.1, 860, 600), (21.6, 1050, 560),
                                                       (22.2, 1050, 530), (22.8, 1150, 480), (23.4, 1250, 470), (23.8, 1310, 460), (24.3, 1310, 460)]),  # jusqu'au ballon au fond (23,9 s)
    'collymore2': ('8DShcsZSVQg.mp4', 26.4, 3.0, 720, [(26.6, 860, 480)]),
    'inzaghi': ('HB3JnHb_IG4.mp4', 15.3, 3.6, 900, [(15.4, 930, 600)]),
    'inzaghi2': ('HB3JnHb_IG4.mp4', 18.3, 3.5, 900, [(18.4, 750, 600), (19.4, 700, 600), (19.9, 1000, 600), (20.3, 1250, 600),
                                                      (20.6, 1300, 600), (21.0, 1150, 600), (21.7, 1100, 600)]),  # le but entier dans le cadre (ballon au fond vers 20,9 s)
    # Rob Green : caméra au ras du sol (720p) au lieu du plan large FIFA en 480p
    'green': ('m7Ra_FafbEQ.mp4', 23.8, 2.9, 660, [(23.9, 790, 420), (24.5, 820, 400), (25.0, 600, 400), (25.5, 330, 400),
                                                   (26.0, 380, 420), (26.5, 800, 400)]),
    'green2': ('m7Ra_FafbEQ.mp4', 29.2, 2.2, 640, [(29.3, 600, 400), (29.7, 450, 400), (30.1, 340, 400), (30.5, 320, 400), (31.4, 320, 400)]),  # le ballon glisse jusqu'au poteau et entre (31 s)
    'origi': ('0iXX_xN05Cg.mp4', 59.4, 4.2, 860, [(59.5, 870, 630), (60.6, 900, 630), (61.1, 850, 630), (61.7, 750, 630),
                                                   (62.2, 1000, 630), (62.8, 1150, 630), (63.2, 1150, 630), (63.25, 1400, 630)]),
    'origi2': ('0iXX_xN05Cg.mp4', 63.8, 1.5, 880, [(63.9, 1000, 640)]),
    'origi3': ('0iXX_xN05Cg.mp4', 65.6, 1.8, 880, [(65.7, 1170, 440)]),  # tête d'Origi et ballon au fond (66,6 s), sans le score ni LFCTV
    'lloris0': ('GrsEAvRerTg.mp4', 0.2, 3.6, (860, 470), [(0.4, 1070, 565)]),  # le trophée seul, sans visages ni incrustation
    'mandzukic': ('GrsEAvRerTg.mp4', 98.8, 1.1, 900, [(98.9, 800, 630)]),
    'lloris': ('GrsEAvRerTg.mp4', 99.7, 4.3, 760, [(99.8, 650, 575), (101.6, 650, 575), (102.0, 850, 650), (102.4, 1000, 700), (103.9, 1000, 700)]),  # ralenti depuis le but : contre de Mandžukić puis le ballon roule au fond
    'lloris2': ('GrsEAvRerTg.mp4', 94.9, 2.2, 560, [(95.0, 1580, 480), (96.0, 1580, 480), (97.0, 1540, 480)]),  # plan large serré sur le but : contre de Mandžukić (95,5 s), le ballon roule au fond (vers 96,5 s)
    'karius': ('rtFGpfrdlMI.mp4', 17.5, 2.9, 640, [(17.6, 950, 420), (18.1, 1050, 420), (18.6, 1300, 440), (19.1, 1200, 460),
                                                    (19.6, 1050, 460), (20.1, 1050, 440)]),
    'karius2': ('rtFGpfrdlMI.mp4', 20.2, 3.1, 760, [(20.3, 1050, 510), (20.8, 1100, 510), (21.2, 1300, 510), (21.6, 1400, 510), (22.2, 1400, 510),
                                                    (23.1, 1380, 510)]),  # relance contrée par Benzema, ballon au fond (22,9 s)
    'benzema': ('rtFGpfrdlMI.mp4', 23.9, 1.4, 900, [(24.0, 1450, 610), (24.4, 950, 610), (25.0, 1350, 610)]),
    'chicharito': ('CYJGpH5n-KM.mp4', 8.5, 1.4, 720, [(8.6, 950, 560)]),
    'chicharito2': ('CYJGpH5n-KM.mp4', 15.9, 1.2, 900, [(16.0, 800, 450)]),
    'chicharito3': ('CYJGpH5n-KM.mp4', 11.5, 4.5, 900, [(11.6, 1150, 540), (12.0, 1150, 540), (12.1, 750, 600), (12.8, 800, 600),
                                                         (13.4, 750, 600), (13.9, 850, 600), (14.5, 1250, 600), (15.6, 1250, 600),
                                                         (15.65, 900, 480)]),
    'kiessling': ('d8LDD9AJcmI.mp4', 2.2, 4.0, 740, [(2.3, 780, 640), (2.75, 780, 640), (2.85, 1350, 492), (3.33, 1100, 500),
                                                      (3.84, 950, 500), (4.36, 900, 500), (4.87, 950, 500), (5.9, 900, 500)]),
    'kiessling2': ('d8LDD9AJcmI.mp4', 11.9, 1.2, 960, [(12.0, 1000, 600)]),
    'kiessling3': ('d8LDD9AJcmI.mp4', 19.5, 3.3, 900, [(19.6, 850, 600), (20.1, 1000, 600), (20.5, 900, 600), (21.0, 950, 600),
                                                        (21.5, 950, 600), (22.0, 800, 600), (22.5, 700, 600)]),
    'bent': ('PPHy9M2daTc.mp4', 273.9, 3.6, 860, [(274.0, 900, 540), (274.5, 650, 540), (275.0, 600, 560), (275.6, 900, 560),
                                                   (276.1, 1150, 560), (276.6, 1250, 560)]),
    'bent2': ('PPHy9M2daTc.mp4', 271.9, 1.3, 1000, [(272.0, 1420, 540), (272.4, 1050, 540), (272.9, 1000, 560)]),
    'bent3': ('PPHy9M2daTc.mp4', 282.7, 3.6, 1000, [(282.8, 760, 580), (283.3, 900, 580), (283.7, 1000, 580), (284.0, 1150, 580),
                                                    (284.3, 900, 580), (284.9, 700, 580), (285.4, 950, 580), (285.9, 1150, 580)]),  # le ballon file au fond (283,9-284,1 s)
    'bent4': ('PPHy9M2daTc.mp4', 288.4, 2.3, 1000, [(288.5, 1350, 580), (289.0, 1400, 580), (289.4, 1100, 580), (289.85, 1200, 580),
                                                     (290.3, 1250, 580)]),
    'bent5': ('PPHy9M2daTc.mp4', 293.9, 2.6, 1000, [(294.0, 850, 500), (294.5, 950, 500), (295.0, 1150, 500), (295.5, 1400, 500),
                                                     (296.1, 1000, 500)]),
    'kane0': ('Bnsc-7TJDUI.mp4', 18.4, 3.7, 800, [(18.5, 900, 520), (19.0, 650, 560), (19.6, 750, 560), (20.1, 600, 520),
                                                   (21.7, 750, 540)]),
    'eriksen': ('Bnsc-7TJDUI.mp4', 53.5, 1.2, 1000, [(53.6, 950, 580)]),  # Eriksen prend son élan
    'kane': ('Bnsc-7TJDUI.mp4', 55.9, 1.2, 760, [(56.0, 1540, 540), (56.2, 1500, 540), (56.6, 1350, 540), (57.0, 1250, 540)]),  # le coup franc arrive au but
    'kane2': ('Bnsc-7TJDUI.mp4', 58.9, 1.3, 1000, [(59.0, 870, 580)]),
    'kane3': ('Bnsc-7TJDUI.mp4', 61.4, 2.6, 1000, [(61.5, 1060, 560)]),
    'interview': ('pehSmaHn5Tk.mp4', 9.9, 3.9, (1440, 1080), [(10.0, 980, 540)]),  # 4:3 : Kane et Eriksen ensemble
    'interview2': ('pehSmaHn5Tk.mp4', 19.9, 3.0, (1440, 1080), [(20.0, 980, 540)]),
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
    src, start, dur, size, track = SEGMENTS[key]
    w, h = size if isinstance(size, tuple) else (size, size)
    pts = [(t - start, *_window(src, size, cx, cy)) for t, cx, cy in track]
    xs, ys = _expr([(t, x) for t, x, _ in pts]), _expr([(t, y) for t, _, y in pts])
    out_h = round(1080 * h / w / 2) * 2
    graph = ('[0:v]split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85[bg];'
             f"[a]crop={w}:{h}:'{xs}':'{ys}',scale=1080:{out_h}:flags=lanczos[fg];"
             f'[bg][fg]overlay=0:{CY - out_h // 2},setsar=1,fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-i', src, '-t', str(dur),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    f'arch-{key}.mp4'], check=True)
    print(key, 'ok', f'{w}x{h} px source -> {1080 / w:.2f}x', flush=True)


def cadrer_photos(target=.38):
    """Photos Commons recadrées en 1080x1920, visage centré en largeur et placé vers 38 % de la hauteur,
    sous le logo et le bandeau de série (le recadrage pleine hauteur le laissait collé en haut)."""
    import json
    from pathlib import Path
    from PIL import Image
    folder = Path('photos')
    for s in json.loads((folder / 'selection.json').read_text(encoding='utf8')):
        im = Image.open(folder / s['fichier']).convert('RGB')
        w, h = im.size
        cx, cy = s.get('centre_x', .5) * w, s.get('centre_y', .3) * h
        ch = min(h, w * 16 / 9)
        if cy < target * ch:  # zoom jusqu'à ce que le visage descende à la hauteur voulue, 2,2x au plus
            ch = max(cy / target, ch / 2.2)
        cw = ch * 9 / 16
        x0 = min(max(cx - cw / 2, 0), w - cw)
        y0 = min(max(cy - target * ch, 0), h - ch)
        out = folder / ('v-' + s['fichier'])
        im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((1080, 1920), Image.LANCZOS).save(out, quality=94)
        print(out.name, f'{cw:.0f}x{ch:.0f} px source, visage à {(cy - y0) / ch:.0%}')


if __name__ == '__main__':
    if sys.argv[1:] == ['photos']:
        cadrer_photos()
    else:
        for k in sys.argv[1:] or SEGMENTS:
            render(k)
