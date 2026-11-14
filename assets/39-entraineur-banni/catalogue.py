"""Catalogue de repérage : 5 images par clip (vertical), libellé id, résolution, durée.

python catalogue.py sortie.jpg fichier1.mp4 fichier2.mp4 ...
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype('C:/Projets/Tiktok - MrBallen/assets/fonts/Poppins-ExtraBold.ttf', 18)
W, H, N = 162, 288, 5
files = [Path(f) for f in sys.argv[2:]]
sheet = Image.new('RGB', (W * N + 260, H * len(files)), 'black')
draw = ImageDraw.Draw(sheet)
tmp = Path('tmp')
tmp.mkdir(exist_ok=True)
for row, f in enumerate(files):
    info = json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
         '-of', 'json', str(f)]))
    d = float(info['format']['duration'])
    w, h = info['streams'][0]['width'], info['streams'][0]['height']
    for k in range(N):
        t = d * (0.08 + 0.84 * k / (N - 1))
        out = tmp / f'{f.stem}-{k}.jpg'
        vf = (f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale={W}:{H}")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(f), '-frames:v', '1', '-vf', vf, str(out)],
                       check=True)
        sheet.paste(Image.open(out), (260 + k * W, row * H))
        draw.text((260 + k * W + 4, row * H + 4), f'{t:.1f}s', font=font, fill='yellow')
    draw.text((6, row * H + 10), f.stem.replace('pexels-', 'P '), font=font, fill='white')
    draw.text((6, row * H + 40), f'{w}x{h}', font=font, fill='white')
    draw.text((6, row * H + 70), f'{d:.1f}s', font=font, fill='white')
sheet.save(sys.argv[1], quality=82)
print(sys.argv[1], len(files))
