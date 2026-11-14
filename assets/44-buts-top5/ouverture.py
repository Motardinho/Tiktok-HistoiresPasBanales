"""Dossier 44 : la vidéo s'ouvre sur la nouvelle miniature (demande de Marc, 12 novembre 2026).

La miniature v2 (out/miniatures-v2/44.jpg) couvre l'image pendant l'annonce du titre, à la place de l'ancien
carton de titre : l'image à 0:00 est donc la miniature. Le reste du film et le son ne changent pas.
Part de _montage/final.mp4 (export habillé), écrit final.mp4, régénère la comparaison et le contrôle d'export.
Lancer depuis la racine : python assets/44-buts-top5/ouverture.py
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, '.')
from comparer_lot_16_18 import compare  # noqa: E402

p = Path('out/44-top-5-buts-les-plus-degueulasses')
m = p / '_montage'
DUREE = 2.0  # durée de l'ancien carton de titre, entièrement recouvert

shutil.copy2('out/miniatures-v2/44.jpg', m / 'miniature-ouverture.jpg')
target = m / 'final-miniature.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'final.mp4', '-loop', '1', '-framerate', '30', '-i', 'miniature-ouverture.jpg',
                '-filter_complex', f"[1:v]scale=1080:1920,format=yuv420p[mi];[0:v][mi]overlay=0:0:enable='lt(t,{DUREE})':shortest=1[v]",
                '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'copy', '-movflags', '+faststart', target.name], cwd=m, check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-map', '0:v', '-map', '0:a', '-f', 'null', '-'], check=True)
probe = lambda kind: float(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', f'{kind}:0', '-show_entries',
                                                    'stream=duration', '-of', 'csv=p=0', str(target)], text=True).strip())
video, audio = probe('v'), probe('a')
assert video > 60 and abs(video - audio) < .3, (video, audio)
shutil.copy2(target, p / 'final.mp4')
compare(p)
(m / 'controle-export.json').write_text(json.dumps(dict(
    duree_video=video, duree_audio=audio, sha256=hashlib.sha256((p / 'final.mp4').read_bytes()).hexdigest(),
    decodage_integral=True, comparaison_a_jour=True, ouverture_miniature=DUREE), ensure_ascii=False, indent=2), encoding='utf8')
print('final avec miniature en ouverture', round(video, 2), 's')
