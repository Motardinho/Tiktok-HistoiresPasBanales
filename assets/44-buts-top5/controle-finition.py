"""Preuves du dernier export ; ne certifie pas à lui seul un visionnage ou une écoute."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p = Path('out/44-top-5-buts-les-plus-degueulasses')
story = json.loads((p/'histoire.json').read_text(encoding='utf8'))
offset = story.get('intro_supprimee_secondes', 0)
q = p / ('_montage/controle-depart-direct' if offset else '_montage/controle-2026-11-13')
q.mkdir(exist_ok=True)
font = ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf', 16)
times = [0, 1, 2.3, 2.8, 2.9, 4.8, 5.8, 27.6, 28.2, 29.1, 29.55, 50.4, 51.3, 63.3, 64.8, 68.3]
times += [x / 10 for a, b in [(150, 171), (238, 272), (350, 375), (493, 517), (618, 636)] for x in range(a, b, 3)]
times = sorted(set(times))
if offset:
    times = sorted(set([0, .3, 1.2, 2.5, 4.8] + [round(t-offset, 3) for t in times if t>=offset]))
for page in range((len(times) + 11) // 12):
    sheet = Image.new('RGB', (1440, 2010), '#15181d')
    draw = ImageDraw.Draw(sheet)
    for i, t in enumerate(times[page*12:page*12+12]):
        dest = q / f'{t:05.1f}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(p/'final.mp4'), '-frames:v', '1', '-vf', 'scale=360:640', str(dest)], check=True)
        x, y = i%4*360, i//4*670
        sheet.paste(Image.open(dest), (x, y+30))
        draw.text((x+5,y+4), f'{t:.1f} s', fill='white', font=font)
    sheet.save(q / f'page-{page}.jpg')
(q/'captures.json').write_text(json.dumps(times), encoding='utf8')
print('Preuves générées :', len(times), 'captures du dernier final.')
