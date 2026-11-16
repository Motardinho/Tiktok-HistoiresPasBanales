"""Captures début, milieu et fin de chaque plan du final, planches de 12, aperçu lecteur TikTok."""
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

work = Path(__file__).resolve().parent
plans = json.loads((work / 'plans.json').read_text(encoding='utf-8'))
proof = work / 'controle'
proof.mkdir(exist_ok=True)
for old in proof.glob('image-*.jpg'):
    old.unlink()


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-nostdin', '-hide_banner', '-loglevel', 'error', *map(str, args)], cwd=work, check=True)


frames = []
for plan in plans:
    first, last = round(plan['debut'] * 25), round(plan['fin'] * 25) - 1
    frames.extend([first, (first + last) // 2, last])
from concurrent.futures import ThreadPoolExecutor


def grab(pair):
    i, n = pair
    ffmpeg('-ss', f'{min(n / 25 + 0.001, plans[-1]["fin"] - 0.12):.3f}', '-i', 'final.mp4', '-frames:v', 1, '-vf', 'scale=360:640',
           f'controle/image-{i + 1:03}.jpg')


with ThreadPoolExecutor(6) as pool:
    list(pool.map(grab, enumerate(frames)))
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 16)
per = 12
for group in range(0, len(frames), per):
    sheet = Image.new('RGB', (6 * 225, 2 * 410), '#14171e')
    draw = ImageDraw.Draw(sheet)
    for cell, index in enumerate(range(group, min(group + per, len(frames)))):
        x, y = (cell % 6) * 225, (cell // 6) * 410
        shot = Image.open(proof / f'image-{index + 1:03}.jpg')
        sheet.paste(shot.resize((225, 400)), (x, y + 10))
        draw.text((x + 4, y - 2), f'P{index // 3} {frames[index] / 25:.2f} s', font=font, fill='#FFE24A')
    sheet.save(proof / f'plans-{group // per + 1}.jpg', quality=90)

preview = Image.new('RGB', (1080, 640))
for panel, t in enumerate([0.4, 33.0, 64.0]):
    out = proof / f'apercu-{panel}.jpg'
    ffmpeg('-ss', t, '-i', 'final.mp4', '-frames:v', 1, '-vf', 'scale=360:640', str(out))
    shot = Image.open(out).convert('RGBA')
    ui = Image.new('RGBA', shot.size)
    d = ImageDraw.Draw(ui)
    d.rounded_rectangle((24, 23, 330, 56), radius=12, fill=(14, 14, 17, 191))
    d.text((38, 31), 'Rechercher', font=font, fill='white')
    d.rectangle((0, 482, 360, 640), fill=(14, 14, 17, 172))
    d.text((17, 496), '@histoirespasbanales', font=font, fill='white')
    d.text((17, 524), 'Le jockey est une perceuse.', font=font, fill='white')
    for y, label in [(287, 'Profil'), (352, 'J’aime'), (418, 'Com.'), (478, 'Partager')]:
        d.ellipse((324, y, 348, y + 24), fill=(255, 255, 255, 225))
        d.text((300, y + 26), label, font=font, fill='white')
    preview.paste(Image.alpha_composite(shot, ui).convert('RGB'), (panel * 360, 0))
preview.save(work / 'apercu-tiktok.jpg', quality=94)
ffmpeg('-i', 'final.mp4', '-map', '0:v', '-map', '0:a', '-f', 'null', '-')
print(len(frames), 'captures')
