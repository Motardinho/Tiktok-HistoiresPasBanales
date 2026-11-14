"""Planche des photos : image entiere + recadrage 9:16 centre. python planche_photos.py <dossier assets>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
p = Path(sys.argv[1]) / 'photos'
files = sorted(p.glob('photo-*.jpg'))
font = ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf', 16)
W = 6; cell = (360, 300)
sheet = Image.new('RGB', (W * cell[0], ((len(files) + W - 1) // W) * cell[1]), 'black'); d = ImageDraw.Draw(sheet)
for n, f in enumerate(files):
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
    x, y = (n % W) * cell[0], (n // W) * cell[1]
    full = im.copy(); full.thumbnail((200, 270)); sheet.paste(full, (x, y + 24))
    w = min(im.width, im.height * 9 // 16); crop = im.crop(((im.width - w) // 2, 0, (im.width + w) // 2, im.height)).resize((152, 270)); sheet.paste(crop, (x + 204, y + 24))
    d.text((x + 4, y + 2), f"{f.stem[6:]} {im.width}x{im.height}", font=font, fill='yellow')
sheet.save(p / 'planche.jpg', quality=85); print(len(files))
