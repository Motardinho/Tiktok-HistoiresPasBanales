"""Captures ciblées après retrait des cinq bandeaux de match."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p = Path('out/44-top-5-buts-les-plus-degueulasses')
q = p / '_montage/controle-sans-bandeaux'
q.mkdir(exist_ok=True)
times = [0, 1.5, 3.4, 10.9, 12.2, 13.8, 23.2, 24.6, 26.2, 34.5, 35.8, 37.4, 46.1, 47.4, 49, 44.4, 58, 61.4]
story = json.loads((p/'histoire.json').read_text(encoding='utf8'))
if story.get('coupe_blanc'):
    cut = story['coupe_blanc']
    times = [round(t-cut['duree_retiree'],3) if t>=cut['fin_avant'] else t for t in times]
font = ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf',16)
for page in range(2):
    sheet = Image.new('RGB',(1080,2010),'#15181d')
    draw = ImageDraw.Draw(sheet)
    for i,t in enumerate(times[page*9:page*9+9]):
        dest = q/f'{t:05.1f}.jpg'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(p/'final.mp4'),'-frames:v','1','-vf','scale=360:640',str(dest)],check=True)
        x,y=i%3*360,i//3*670
        sheet.paste(Image.open(dest),(x,y+30))
        draw.text((x+6,y+5),f'{t:.1f} s',font=font,fill='white')
    sheet.save(q/f'page-{page}.jpg')
(q/'captures.json').write_text(json.dumps(times),encoding='utf8')
print('18 captures générées')
