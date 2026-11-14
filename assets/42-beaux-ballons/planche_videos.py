"""Planche de repérage : python planche_videos.py sortie.jpg fichier1 fichier2 ... (6 instants par vidéo, horodatés)."""
import subprocess, sys, tempfile
from pathlib import Path
out, files = sys.argv[1], sys.argv[2:]
tmp = Path(tempfile.mkdtemp())
rows = []
for k, f in enumerate(files):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
    cells = []
    for j in range(6):
        t = d * (j + .5) / 6
        c = tmp / f'{k}-{j}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', f, '-frames:v', '1', '-vf',
                        f"scale=-2:200,drawtext=fontfile=police.ttf:text='{Path(f).stem} {t:.1f}s':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black", str(c)], check=True)
        cells.append(c)
    r = tmp / f'row{k}.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *sum([['-i', str(c)] for c in cells], []), '-filter_complex',
                    ''.join(f'[{i}]scale=-2:200[c{i}];' for i in range(6)) + ''.join(f'[c{i}]' for i in range(6)) + 'hstack=6', str(r)], check=True)
    rows.append(r)
subprocess.run(['ffmpeg', '-v', 'error', '-y', *sum([['-i', str(r)] for r in rows], []), '-filter_complex',
                ''.join(f'[{i}]scale=2100:-2[r{i}];' for i in range(len(rows))) + ''.join(f'[r{i}]' for i in range(len(rows))) + f'vstack={len(rows)}', out], check=True)
print(out)
