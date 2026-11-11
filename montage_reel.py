"""Montage des séquences réelles et comparaisons originales/nouvelles versions."""
import json
import subprocess
import sys
from pathlib import Path
import yaml
from narrateur import assemble

ROOT=Path(__file__).resolve().parent
SOURCES=ROOT/'assets'/'sources-reelles'

def run(cmd,cwd=ROOT):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if r.returncode:raise RuntimeError(r.stderr[-3500:])
 return r.stdout

def montage(slug,only=None):
 work=ROOT/'out'/slug
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
 data=json.loads((work/'histoire.json').read_text(encoding='utf-8'))
 timing=json.loads((work/'timings.json').read_text(encoding='utf-8'))
 shots=json.loads((work/'sources-visuelles.json').read_text(encoding='utf-8'))
 overlays=[(0,2.5,f"DOSSIER N°{data['numero']}")]
 cursor=0
 for scene,dur in zip(data['scenes'],timing['scene_durations']):
  if scene.get('bandeau'):overlays.append((cursor,cursor+dur,scene['bandeau'],'Bandeau'))
  cursor+=dur
 overlays.append((0,cursor,data['titre_fixe'],'Titre'))
 assemble.write_subtitles(cfg,timing['words'],work/'sous-titres.ass',overlays)
 files=[]
 for i,(shot,dur) in enumerate(zip(shots,timing['scene_durations'])):
  target=work/f'reel-scene{i:02d}.mp4'
  if only is not None and i not in only and target.exists():
   files.append(target)
   continue
  src=SOURCES/shot['fichier']
  info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height','-of','json',str(src)]))
  vs=next(s for s in info['streams'] if s['codec_type']=='video')
  portrait=vs['height']>vs['width']
  if portrait:
   filt='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
   opts=['-vf',filt]
  else:
   # Le plan entier reste visible ; le fond est une copie floue de la vraie vidéo.
   filt=('split=2[bg][fg];[bg]scale=270:480:force_original_aspect_ratio=increase,'
         'crop=270:480,gblur=sigma=12,scale=1080:1920,eq=brightness=-0.18[back];'
         '[fg]scale=1080:1000:force_original_aspect_ratio=decrease[front];'
         '[back][front]overlay=(W-w)/2:420:shortest=1,fps=30,setsar=1[v]')
   opts=['-filter_complex',filt,'-map','[v]']
  run(['ffmpeg','-v','error','-y','-ss',str(shot['debut_s']),'-stream_loop','-1','-i',str(src),'-t',str(dur+(0.5 if i==len(shots)-1 else 0)),*opts,'-an','-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p',str(target)])
  files.append(target)
  print(slug,'plan',i+1,'/',len(shots),flush=True)
 assemble.assemble(cfg,work,files,work/'voix.mp3',work/'sous-titres.ass',work/'final.mp4',assemble.stamp_time(timing['words']))
 (work/'publication.txt').write_text(data['legende']+'\n\n'+' '.join(data['hashtags'])+'\n\nVoix synthétique : activer le label IA. Images réelles, séquences proches ou identiques à la référence.\nSources factuelles : verification.md. Crédits visuels : assets/sources-reelles/CREDITS.md.\n',encoding='utf-8')
 print(slug,'monté',flush=True)
 compare(slug)

def compare(slug):
 work=ROOT/'out'/slug
 original=ROOT/'assets'/'references-faiseemoc84'/(slug+'.mp4')
 target=work/'comparaison.mp4'
 # Deux vidéos côte à côte, départ simultané ; fin figée si une version est plus courte.
 font=str((ROOT/'assets/fonts/Poppins-ExtraBold.ttf').resolve()).replace('\\','/').replace(':','\\:')
 graph=("[0:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[l];"
        "[1:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[r];"
        "[l][r]hstack=inputs=2,pad=1080:1040:0:80:color=0x111827,"+
        f"drawtext=fontfile='{font}':text='ORIGINAL':fontcolor=white:fontsize=28:x=180:y=24,"+
        f"drawtext=fontfile='{font}':text='NOTRE VERSION':fontcolor=white:fontsize=28:x=670:y=24[v]")
 durations=[float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(p)]))['format']['duration']) for p in [original,work/'final.mp4']]
 # Pistes audio séparées pour pouvoir écouter chacune sans mélanger les narrations.
 run(['ffmpeg','-v','error','-y','-i',str(original),'-i',str(work/'final.mp4'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-map','1:a:0','-t',str(max(durations)),'-c:v','libx264','-preset','fast','-crf','21','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-metadata:s:a:0','title=Original','-metadata:s:a:1','title=Notre version','-disposition:a:0','0','-disposition:a:1','default','-movflags','+faststart',str(target)])
 print(slug,'comparaison prête',flush=True)

if __name__=='__main__':
 for slug in sys.argv[1:]:montage(slug)
