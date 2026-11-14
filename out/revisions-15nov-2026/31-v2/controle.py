"""Planches de contrôle du MP4 final : début, milieu, fin de chaque plan (avec habillage)."""
import io
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = Path(__file__).resolve().parent
plans = json.loads((W / '_montage/plans.json').read_text(encoding='utf-8'))
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
out = W / 'controle'
out.mkdir(exist_ok=True)


def frame(t, w=240):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(W / 'final.mp4'), '-frames:v', '1',
                       '-vf', f'scale={w}:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    return Image.open(io.BytesIO(b)).convert('RGB')


per = 6
for page in range(0, len(plans), per):
    rows = plans[page:page + per]
    sheet = Image.new('RGB', (3 * 240, len(rows) * (427 + 26)), 'black')
    d = ImageDraw.Draw(sheet)
    for r, p in enumerate(rows):
        a, b = p['debut'], p['fin']
        for c, t in enumerate([a + .05, (a + b) / 2, b - .07]):
            sheet.paste(frame(t), (c * 240, r * 453 + 26))
        d.text((4, r * 453 + 2), f"{page + r:02} {a:.2f}-{b:.2f} {p['note'][:58]}", font=font, fill='yellow')
    sheet.save(out / f'plans-{page // per}.jpg', quality=85)
print(len(plans), 'plans')
