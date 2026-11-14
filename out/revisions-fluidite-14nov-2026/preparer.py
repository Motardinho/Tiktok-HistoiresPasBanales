from pathlib import Path
import json,subprocess,shutil
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def ff(a):subprocess.run(['ffmpeg','-v','error','-y',*map(str,a)],check=True)
def build(n):
 d=OUT/str(n);rows=json.loads((d/'plans.json').read_text(encoding='utf-8'))
 for i,p in enumerate(rows):
  f=d/f'plan-{i:02}.mp4'
  if not p['reconstruire']:shutil.copy2(ROOT/f'out/revisions-archives-14nov-2026/{n}/plan-{p["ancien_plan"]:02}.mp4',f)
  else:
   frames=round((p['start']+p['duration'])*30)-round(p['start']*30)
   ff(['-ss',p['ss'],'-i',p['source'],'-an','-vf',p['crop']+',fps=30,format=yuv420p','-frames:v',frames,'-c:v','libx264','-preset','fast','-crf','20','-threads','3',f])
 (d/'concat.txt').write_text('\n'.join(f"file 'plan-{i:02}.mp4'" for i in range(len(rows))),encoding='utf-8')
 ff(['-f','concat','-safe','0','-i',d/'concat.txt','-c','copy',d/'base.mp4'])
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(d/'base.mp4'),'-vf','freezedetect=n=-45dB:d=0.6','-an','-f','null','-'],capture_output=True,text=True)
 log='\n'.join(l for l in r.stderr.splitlines() if 'freeze' in l);(d/'controle-gels.txt').write_text(log);print(n,log or 'Aucun gel >= 0.6 seconde',flush=True)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(build,[27,28]))
