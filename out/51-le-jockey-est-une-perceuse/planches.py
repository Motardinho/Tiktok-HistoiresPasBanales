"""Planches de repérage horodatées : python planches.py <fichier source> [pas en s] [debut] [fin]."""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

work = Path(__file__).resolve().parent
source = work / 'sources' / sys.argv[1]
step = float(sys.argv[2]) if len(sys.argv) > 2 else 4
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=width,height,color_transfer',
                                   '-select_streams', 'v:0', '-of', 'json', str(source)],
                                  capture_output=True, text=True, check=True).stdout)
duration = float(probe['format']['duration'])
start = float(sys.argv[3]) if len(sys.argv) > 3 else 0
end = float(sys.argv[4]) if len(sys.argv) > 4 else duration
out = work / 'reperage'
out.mkdir(exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 22)
times = [start + i * step for i in range(int((end - start) / step) + 1)]
cells = []
for t in times:
    data = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', str(source), '-frames:v', '1',
                           '-vf', 'scale=480:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                          capture_output=True, check=True).stdout
    if data:
        from io import BytesIO
        cells.append((t, Image.open(BytesIO(data)).convert('RGB')))
cols = 5
w, h = cells[0][1].size
for page in range(0, len(cells), 30):
    chunk = cells[page:page + 30]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h), '#111')
    draw = ImageDraw.Draw(sheet)
    for i, (t, im) in enumerate(chunk):
        x, y = (i % cols) * w, (i // cols) * h
        sheet.paste(im, (x, y))
        draw.rectangle((x, y, x + 92, y + 30), fill='black')
        draw.text((x + 6, y + 3), f'{t:.1f}', font=font, fill='#FFE24A')
    name = f'{source.stem}-{page // 30 + 1}.jpg'
    sheet.save(out / name, quality=85)
    print(name)
stream = probe['streams'][0]
print(source.name, stream['width'], 'x', stream['height'], stream.get('color_transfer'), round(duration, 1), 's')
