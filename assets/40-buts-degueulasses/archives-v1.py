"""Dossier 40 : extraits des buts en 1080x1920, image entière sur fond flou (procédé du dossier 27).

Chaque extrait est recadré (zone x, y, w, h dans la source) pour exclure logos de diffuseur,
tableaux de score et filigranes, réduit à 1080 de large et posé à y = TOP sur un fond flou
assombri du même plan. Lancer depuis ce dossier : python archives.py [clé ...]
"""
import subprocess
import sys

TOP = 610  # sous le bandeau de rang (y 380-600), au-dessus des sous-titres

# clé : (source, début, durée, (x, y, w, h))
SEGMENTS = {
    'collymore': ('8DShcsZSVQg.mp4', 17, 19, (246, 128, 1430, 824)),   # 4:3 SD agrandi, sans bandes noires
    'inzaghi': ('HB3JnHb_IG4.mp4', 14, 13, (480, 120, 1440, 830)),     # logo UEFA en haut à droite exclu
    'green': ('8ahf8b7ex8U.mp4', 86, 10, (40, 75, 703, 405)),          # 854x480, logo FIFA TV exclu
    'origi': ('0iXX_xN05Cg.mp4', 50, 20, (240, 200, 1440, 830)),       # score LIV-EVE et LFCTV exclus
    'lloris0': ('GrsEAvRerTg.mp4', 0.2, 3.6, (640, 330, 860, 470)),    # le trophée avant la finale : coupe seule, sans visages ni incrustation
    'lloris': ('GrsEAvRerTg.mp4', 94, 6, (480, 220, 1440, 830)),       # score FRA-CRO et FIFA TV exclus
    'karius': ('rtFGpfrdlMI.mp4', 16, 13, (480, 130, 1440, 830)),      # logo UEFA exclu
    'chicharito': ('CYJGpH5n-KM.mp4', 7, 11, (240, 190, 1440, 830)),   # écusson Man United exclu
    'kiessling': ('d8LDD9AJcmI.mp4', 1, 25, (240, 120, 1440, 830)),    # score et logo Bundesliga exclus
    'bent': ('PPHy9M2daTc.mp4', 268, 30, (240, 120, 1440, 830)),       # logo Premier League exclu
    'kane0': ('Bnsc-7TJDUI.mp4', 18, 6, (240, 120, 1440, 830)),        # plan large du même match, avant le coup franc
    'kane': ('Bnsc-7TJDUI.mp4', 50, 15, (480, 120, 1440, 830)),        # logo Spurs TV exclu
    'interview': ('pehSmaHn5Tk.mp4', 7, 27, (200, 110, 1440, 830)),    # logo Sky exclu
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
