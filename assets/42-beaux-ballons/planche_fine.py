"""Planche fine : python planche_fine.py source.mp4 sortie.jpg debut fin pas (une vignette par pas, horodatée)."""
import subprocess, sys
src, out, a, b, step = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
n = int((b - a) / step) + 1
cols = 6
vf = (rf"fps=1/{step},scale=340:-2,drawtext=fontfile=police.ttf:text='%{{eif\:t+{a}\:d}}s':x=4:y=4:fontsize=22:fontcolor=yellow:box=1:boxcolor=black,"
      f"tile={cols}x{(n + cols - 1) // cols}")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(b - a), '-i', src, '-vf', vf, '-frames:v', '1', out], check=True)
print(out)
