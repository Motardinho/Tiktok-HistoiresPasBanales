import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[1]
sys.path.insert(0, str(ROOT))
from narrateur.assemble import write_subtitles
import miniatures_hpb as cover


# Fin dans le montage, source, départ source, fenêtre (x, y, largeur, hauteur).
# Les fenêtres des archives restent larges et gardent les visages hors du cadre.
PLANS = [
    (1.68, 'afp.mp4', 55.72, (274, 62, 846, 650)),
    (3.68, 'onu.webm', 598.8, (22, 10, 596, 334)),
    (6.08, 'onu.webm', 530.9, (18, 24, 475, 286)),
    (9.48, 'course.webm', 106.9, (1420, 0, 1214, 2160)),
    (12.96, 'afp.mp4', 53.0, (480, 18, 766, 636)),
    (15.36, 'onu.webm', 537.2, (15, 24, 470, 286)),
    (18.28, 'course.webm', 139.8, (1430, 0, 1214, 2160)),
    (21.60, 'onu.webm', 96.5, (0, 6, 640, 344)),
    (24.36, 'onu.webm', 425.2, (6, 12, 628, 306)),
    (27.52, 'onu.webm', 103.0, (0, 8, 640, 344)),
    (30.20, 'onu.webm', 100.0, (0, 8, 640, 344)),
    (32.60, 'course.webm', 130.4, (1040, 0, 1214, 2160)),
    (35.88, 'onu.webm', 448.9, (12, 124, 612, 218)),
    (38.36, 'onu.webm', 451.6, (18, 145, 602, 205)),
    (41.60, 'onu.webm', 454.05, (24, 188, 586, 160)),
    (44.84, '2009.jpg', 0.0, (18, 15, 930, 558)),
    (47.72, 'onu.webm', 104.1, (0, 18, 638, 320)),
    (50.48, 'course.webm', 189.3, (1420, 0, 1214, 2160)),
    (53.40, 'onu.webm', 609.1, (0, 8, 640, 344)),
    (55.12, 'course.webm', 144.1, (1320, 0, 1214, 2160)),
    (57.20, 'afp.mp4', 56.4, (385, 22, 860, 650)),
    (59.52, 'course.webm', 164.0, (1220, 80, 1350, 1500)),
    (61.56, 'afp.mp4', 92.8, (85, 62, 1050, 560)),
    (63.44, 'onu.webm', 594.8, (0, 5, 640, 342)),
]


def run(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)], cwd=WORK, check=True)


def subtitles():
    timing = json.loads((WORK / 'timings.json').read_text(encoding='utf-8'))
    words = timing['words']
    numbers = {'deux mille cinq,': '2005,', 'vingt-trois mille': '23\u00a0000',
               'mille soixante-treize': '1\u00a0073', 'quatre-quatre.': '4x4.', 'Al Chahaniya,': 'Al\u00a0Shahaniya,'}
    for phrase, display in numbers.items():
        tokens = phrase.split()
        for i in range(len(words) - len(tokens) + 1):
            if [word['w'] for word in words[i:i+len(tokens)]] == tokens:
                words[i:i+len(tokens)] = [{**words[i], 'w': display, 'end': words[i+len(tokens)-1]['end']}]
                break
    path = WORK / 'sous-titres.ass'
    write_subtitles({'render': {'width': 1080, 'height': 1920, 'subtitle_font': 'Arial',
                     'subtitle_size': 83, 'words_per_caption': 4, 'subtitle_wrap': 20}}, words, path)
    ass = path.read_text(encoding='utf-8').replace('0,0,0,0,100,100,1,0,1,8,4,8,50,50,1090,1',
                                                    '-1,0,0,0,100,100,0,0,1,7,3,2,100,200,550,1')
    path.write_text(ass.replace('&H3C3CFF&', '&H00E6FF&'), encoding='utf-8')


def plan(job):
    i, start, (end, source, at, (x, y, w, h)) = job
    if source.endswith('.jpg'):
        inputs = ['-loop', '1', '-framerate', '25', '-i', source]
    else:
        inputs = ['-ss', at, '-threads', '3', '-i', source]
    if source == 'onu.webm':
        w = min(w, 638 - x)
    crop = f'crop={w}:{h}:{x}:{y}'
    properties = 'setsar=1,fps=25,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709'
    if w == 1214 and h == 2160:
        filters = f'[0:v]{crop},scale=1080:1920,{properties}[v]'
    else:
        filters = (f'[0:v]{crop},split[rear][main];'
                   '[rear]scale=224:400:force_original_aspect_ratio=increase,crop=224:400,'
                   'gblur=sigma=13,eq=brightness=-0.15:saturation=0.82,scale=1080:1920[bg];'
                   f'[main]scale=1080:-2,setsar=1[fg];[bg][fg]overlay=0:430,{properties}[v]')
    run(*inputs, '-filter_complex_threads', 2, '-filter_complex', filters, '-map', '[v]',
        '-frames:v', round(end*25)-round(start*25), '-an', '-c:v', 'libx264', '-threads', 3,
        '-preset', 'ultrafast', '-crf', 16, '-pix_fmt', 'yuv420p', f'coupes/{i:02}.mp4')


def thumbnail():
    run('-ss', 144.68, '-i', 'course.webm', '-frames:v', 1,
        '-vf', 'crop=980:1742:1436:390,scale=1080:1920', 'miniature-brut.png')
    raw = Image.open(WORK / 'miniature-brut.png').convert('RGB')
    img = ImageEnhance.Brightness(raw).enhance(1.055)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    img = ImageEnhance.Color(img).enhance(1.12)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.35, percent=60, threshold=4))
    img.save(WORK / 'miniature-reglee.jpg', quality=96)
    cover.DOSSIERS['v2'] = {'fond': str(WORK / 'miniature-reglee.jpg'), 'style': 'magazine',
        'lignes': [cover.N('ENFANTS', 209), cover.N('REMPLACÉS', 131), cover.P('PAR|DES ROBOTS', 125)],
        'bas': 1528, 'contraste': 1, 'saturation': 1, 'voile_haut': 0, 'voile_bas': 0, 'vignette': False}
    cover.composer('v2').save(WORK / 'miniature.jpg', quality=96)
    print('Zones miniature', cover.ZONES['v2'])


def export():
    (WORK / 'coupes.txt').write_text(''.join(f"file 'coupes/{i:02}.mp4'\n" for i in range(len(PLANS))), encoding='utf-8')
    Image.open(cover.LOGO_VALIDE).convert('RGBA').resize((210,210), Image.Resampling.LANCZOS).save(WORK/'logo.png')
    music = ROOT / 'assets/musique/mixkit/espace.mp3'
    audio = ('[1:a]highpass=f=75,acompressor=threshold=0.13:ratio=2.2:attack=10:release=120,'
             'volume=1.22,apad=whole_dur=63.44[voice];'
             '[2:a]volume=0.092,afade=t=in:d=0.35,afade=t=out:st=62.1:d=1.34[music];'
             '[voice][music]amix=inputs=2:duration=first:normalize=0,volume=5.5dB,alimiter=limit=0.85:level=0:latency=1[a]')
    run('-f','concat','-safe',0,'-i','coupes.txt','-i','voix.mp3','-ss',12,'-i',music,
        '-loop',1,'-framerate',25,'-i','logo.png',
        '-filter_complex_threads',3,'-filter_complex',f'[0:v][3:v]overlay=817:182,ass=sous-titres.ass[v];{audio}',
        '-map','[v]','-map','[a]','-c:v','libx264','-threads',6,'-preset','fast','-crf',18,
        '-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
        '-c:a','aac','-b:a','192k','-ar','48000','-t','63.44','-movflags','+faststart','final.mp4')


def main():
    os.chdir(WORK)
    (WORK / 'coupes').mkdir(exist_ok=True)
    subtitles()
    jobs = [(i, PLANS[i-1][0] if i else 0, row) for i, row in enumerate(PLANS)]
    with ThreadPoolExecutor(3) as workers:
        list(workers.map(plan, jobs))
    export()
    thumbnail()


if __name__ == '__main__':
    main()
