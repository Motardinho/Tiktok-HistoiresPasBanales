import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
n = sys.argv[1]
p = next(Path('out').glob(n + '-*')); m = p / '_montage'; qa = m / 'controle'; qa.mkdir(exist_ok=True)
plans = json.loads((m / 'montage.json').read_text(encoding='utf8'))
font = ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf', 15)
evidence = []
PER = 6
for page in range((len(plans) + PER - 1) // PER):
    sheet = Image.new('RGB', (PER * 3 * 180 + (PER - 1) * 8, 344), '#15181d'); dr = ImageDraw.Draw(sheet)
    for j, row in enumerate(plans[page * PER:page * PER + PER]):
        i = page * PER + j; dur = row['fin'] - row['debut']
        for k, rel in enumerate([.04, dur / 2, max(.04, dur - .06)]):
            at = row['debut'] + rel
            dest = qa / f'final-{i:02}-{k}.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', str(p / 'final.mp4'), '-frames:v', '1', '-vf', 'scale=180:320', str(dest)], check=True)
            sheet.paste(Image.open(dest), (j * (548) + k * 180, 24))
            evidence.append(dict(fichier=str(dest), timeline=round(at, 2), source=row['source']))
        dr.text((j * 548 + 4, 3), f'Plan {i:02} - {row["debut"]:.2f}s', font=font, fill='white')
    sheet.save(qa / f'final-page-{page}.jpg', quality=88)
(qa / 'final-captures.json').write_text(json.dumps(evidence, indent=2), encoding='utf8')
print('Captures', len(evidence), 'pages', page + 1)
