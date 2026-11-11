"""Planches de contrôle du final : début, milieu et fin de chaque plan, habillage inclus.

Usage : python planches_controle.py 21 [largeur_vignette]
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
n = sys.argv[1]
width = int(sys.argv[2]) if len(sys.argv) > 2 else 240
height = round(width * 16 / 9)
w = next((ROOT / 'out').glob(f'{n}-*'))
m = w / '_montage'
plans = json.loads((m / 'montage.json').read_text(encoding='utf8'))
font = ImageFont.truetype(str(ROOT / 'assets/fonts/Poppins-ExtraBold.ttf'), 15)
frames = []
for i, p in enumerate(plans):
    for t in (p['debut'] + .1, (p['debut'] + p['fin']) / 2, p['fin'] - .35):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(w / 'final.mp4'), '-frames:v', '1',
                              '-vf', f'scale={width}:{height}', '-f', 'image2pipe', '-c:v', 'png', '-'],
                             capture_output=True, check=True).stdout
        import io
        frames.append((i, t, Image.open(io.BytesIO(raw)).convert('RGB')))
per_sheet = 18
for s in range(0, len(frames), per_sheet):
    chunk = frames[s:s + per_sheet]
    rows = (len(chunk) + 5) // 6
    sheet = Image.new('RGB', (6 * width, rows * (height + 22)), '#11151c')
    d = ImageDraw.Draw(sheet)
    for k, (i, t, im) in enumerate(chunk):
        x, y = (k % 6) * width, (k // 6) * (height + 22)
        sheet.paste(im, (x, y + 22))
        d.text((x + 4, y + 2), f'plan {i:02} - {t:.1f}s', font=font, fill='white')
    target = m / f'controle-plans-{s // per_sheet + 1}.jpg'
    sheet.save(target, quality=88)
    print(target)
