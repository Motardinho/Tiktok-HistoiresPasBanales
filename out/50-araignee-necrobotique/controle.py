import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

work = Path(__file__).resolve().parent
root = work.parent.parent
plans = json.loads((work / 'plans.json').read_text())
proof = work / 'controle'
proof.mkdir(exist_ok=True)

def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-nostdin', '-hide_banner', '-loglevel', 'error',
                    *map(str, args)], cwd=work, check=True)

frames = []
for plan in plans:
    first = round(plan['debut'] * 25)
    last = round(plan['fin'] * 25) - 1
    frames.extend([first, (first + last) // 2, last])
select = '+'.join(f'eq(n\\,{number})' for number in frames)
ffmpeg('-i', 'final.mp4', '-vf', f'select={select},scale=360:640', '-fps_mode', 'passthrough',
       'controle/image-%02d.jpg')
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
for group in range(7):
    sheet = Image.new('RGB', (675, 1230), '#14171e')
    draw = ImageDraw.Draw(sheet)
    for cell in range(9):
        index = group * 9 + cell
        x, y = (cell % 3) * 225, (cell // 3) * 410
        shot = Image.open(proof / f'image-{index + 1:02}.jpg')
        sheet.paste(shot.resize((225, 400)), (x, y + 10))
        draw.text((x + 5, y), f'{frames[index] / 25:.2f} s', font=font, fill='white')
    sheet.save(proof / f'plans-{group + 1}.jpg', quality=93)

preview = Image.new('RGB', (1080, 640))
for panel, index in enumerate([0, 33, 49]):
    shot = Image.open(proof / f'image-{index + 1:02}.jpg').convert('RGBA')
    ui = Image.new('RGBA', shot.size)
    draw = ImageDraw.Draw(ui)
    draw.rounded_rectangle((24, 23, 330, 56), radius=12, fill=(14, 14, 17, 191))
    draw.text((38, 31), 'Rechercher', font=font, fill='white')
    draw.rectangle((0, 482, 360, 640), fill=(14, 14, 17, 172))
    draw.text((17, 496), '@histoirespasbanales', font=font, fill='white')
    draw.text((17, 524), 'Une araignée morte qui attrape encore.', font=font, fill='white')
    for y, label in [(287, 'Profil'), (352, 'J’aime'), (418, 'Com.'), (478, 'Partager')]:
        draw.ellipse((324, y, 348, y + 24), fill=(255, 255, 255, 225))
        draw.text((303, y + 26), label, font=font, fill='white')
    preview.paste(Image.alpha_composite(shot, ui).convert('RGB'), (panel * 360, 0))
preview.save(work / 'apercu-tiktok.jpg', quality=94)
for number, name in enumerate(['photo-avant.png', 'photo-apres.jpg', 'miniature.jpg']):
    if number == 0:
        covers = Image.new('RGB', (1080, 640))
    shot = Image.open(work / name).convert('RGB')
    covers.paste(shot.resize((360, 640), Image.Resampling.LANCZOS), (360 * number, 0))
covers.save(proof / 'miniature-avant-apres.jpg', quality=94)
ffmpeg('-i', 'final.mp4', '-vf', 'scale=360:640', '-c:v', 'libx264', '-preset', 'veryfast',
       '-crf', 20, '-c:a', 'copy', 'controle/lecture-360.mp4')
ffmpeg('-i', 'final.mp4', '-map', '0:v', '-map', '0:a', '-f', 'null', '-')
