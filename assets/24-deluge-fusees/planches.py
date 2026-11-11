from pathlib import Path
import subprocess,json
p=Path('assets/24-deluge-fusees')
for f in p.glob('*.mp4'):
 d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)]))
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f'fps=1/{d/20},scale=320:180,tile=5x4','-frames:v','1',str(f.with_suffix('.jpg'))],check=True)
 print(f.name,d)
