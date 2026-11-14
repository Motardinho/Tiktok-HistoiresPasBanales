"""Grille de repérage horodatée : python grille.py source.mp4 pas sortie.jpg [debut] [fin] (une image tous les `pas` s)."""
import subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
src, step, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
a = float(sys.argv[4]) if len(sys.argv) > 4 else 0
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
b = min(float(sys.argv[5]) if len(sys.argv) > 5 else dur, dur - .2)
times = [a + i * step for i in range(int((b - a) / step) + 1)]
tmp = Path(tempfile.mkdtemp())
def grab(i):
    f = tmp / f'{i}.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{times[i]:.2f}', '-i', src, '-frames:v', '1', '-vf', 'scale=384:-2', str(f)])
    return f
with ThreadPoolExecutor(8) as ex:
    files = list(ex.map(grab, range(len(times))))
ims = [Image.open(f) if f.exists() else Image.new('RGB', (384, 216)) for f in files]
w, h = ims[0].size
cols = 6
sheet = Image.new('RGB', (cols * w, ((len(ims) + cols - 1) // cols) * h))
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
for i, (t, im) in enumerate(zip(times, ims)):
    d = ImageDraw.Draw(im)
    lab = f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:04.1f}' if dur > 3600 else f'{t:.1f}s'
    d.rectangle((0, 0, 12 * len(lab), 24), fill='black'); d.text((3, 1), lab, fill='yellow', font=font)
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=85)
print(out, len(ims), 'images')
