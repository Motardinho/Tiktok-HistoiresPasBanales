"""Planches horodatees d'une archive : python planches.py fichier.mp4 pas_en_secondes [debut] [fin]"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
f = Path(sys.argv[1]); step = float(sys.argv[2])
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)]))
a = float(sys.argv[3]) if len(sys.argv) > 3 else 0; b = min(dur, float(sys.argv[4])) if len(sys.argv) > 4 else dur
times = [a + i * step for i in range(int((b - a) / step) + 1)][:48]
font = ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf', 15)
W, H, C = 320, 180, 6
sheet = Image.new('RGB', (W * C, H * ((len(times) + C - 1) // C)), 'black'); d = ImageDraw.Draw(sheet)
tmp = Path('tmp/planche.jpg')
for n, t in enumerate(times):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(f), '-frames:v', '1', '-vf', f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2', str(tmp)], check=True)
    sheet.paste(Image.open(tmp), ((n % C) * W, (n // C) * H)); d.text(((n % C) * W + 4, (n // C) * H + 2), f'{t:.1f}s', font=font, fill='yellow')
out = f.with_name(f.stem + f'-planche-{int(a)}.jpg'); sheet.save(out, quality=80); print(out)
