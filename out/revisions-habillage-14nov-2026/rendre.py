from pathlib import Path
import json,subprocess,shutil,importlib.util,sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
import resvg_py
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
REF=ROOT/'out/20-telephone-2899-dollars/version-validee/final.mp4'
def ff(args,cwd=None):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],cwd=cwd,check=True)
def dur(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))
def tm(s):
 h,m,v=s.split(':');return int(h)*3600+int(m)*60+float(v)
def ass(t):
 c=round(max(0,t)*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
def render(n):
 name='27-demi-tour-dans-la-tempete' if n==27 else '28-om-a-achete-un-match'
 src=ROOT/'out'/name;dst=OUT/str(n);old=ROOT/'out/revisions-ouverture-14nov-2026'/str(n);cut=(53 if n==27 else 182)/30
 plans=json.loads((dst/'plans.json').read_text(encoding='utf-8'))
 shutil.copy2(ROOT/'out/revisions-archives-14nov-2026'/str(n)/'base.mp4',dst/'base.mp4')
 lines=[]
 for l in (src/'_montage/sous-titres.ass').read_text(encoding='utf-8-sig').splitlines():
  if l.startswith('Dialogue:'):
   a=l.split(',',9)
   if a[3]=='Tag':
    assert any(k in a[9] for k in ['MERS DU SUD','DEMI-TOUR FACE AU VENT','VALENCIENNES']),a[9]
    continue
   t0,t1=tm(a[1]),tm(a[2])
   if t1<=cut or (n==28 and t0<6.07):continue
   a[1]=ass(t0-cut);a[2]=ass(t1-cut);l=','.join(a)
  lines.append(l)
 if n==28:
  for i,l in enumerate(lines):
   if l.startswith('Dialogue:'):a=l.split(',',9);a[1]='0:00:00.00';lines[i]=','.join(a);break
 (dst/'sous-titres.ass').write_text('\n'.join(lines),encoding='utf-8')
 shutil.copy2(src/'_montage/police.ttf',dst/'police.ttf')
 spec=importlib.util.spec_from_file_location('brand',ROOT/'identite/histoires-pas-banales/gabarits-miniatures/render.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">'+mod.logo()+'</svg>'
 (dst/'logo.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg))
 shutil.copy2(src/'_montage/funfact-safe.png',dst/'funfact.png')
 start,end=((54.52,62.04) if n==27 else (58.6,62))
 graph=f"[0:v]ass=sous-titres.ass:fontsdir=.[sub];[sub][2:v]overlay=0:0:shortest=1[logo];[logo][3:v]overlay=60:-131:enable='between(t,{start-cut},{end-cut})':shortest=1[v]"
 ff(['-i','base.mp4','-i',old/'final.mp4','-loop','1','-i','logo.png','-loop','1','-i','funfact.png','-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',dur(dst/'base.mp4'),'-c:v','libx264','-preset','fast','-crf','19','-threads','3','-c:a','copy','-movflags','+faststart','final.mp4'],dst)
 total=max(dur(dst/'final.mp4'),dur(REF))
 graph=f'[0:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[l];[1:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[r];[l][r]hstack=inputs=2[v];[0:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a0];[1:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a1]'
 ff(['-i',REF,'-i',dst/'final.mp4','-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','[a1]','-map','[a0]','-c:v','libx264','-preset','fast','-crf','21','-threads','3','-c:a','aac','-b:a','128k','-metadata:s:a:0','title=HPB archives 14 novembre','-metadata:s:a:1','title=Reference telephones','-disposition:a:0','default','-disposition:a:1','0','-movflags','+faststart',dst/'comparaison.mp4'])
 for page in range(0,len(plans),6):
  sheet=Image.new('RGB',(540,6*340),'#171717');d=ImageDraw.Draw(sheet)
  for row,p in enumerate(plans[page:page+6]):
   for col,t in enumerate([p['start'],p['start']+p['duration']/2,p['start']+p['duration']-.08]):
    f=dst/'qa.jpg';ff(['-ss',t,'-i',dst/'final.mp4','-frames:v','1','-vf','scale=180:320',f]);sheet.paste(Image.open(f),(col*180,row*340));d.text((col*180,row*340+320),f'{page+row} / {t:.2f}s',fill='yellow')
  sheet.save(dst/f'controle-final-{page//6}.jpg')
 for t in [0,3,8,55,60]:ff(['-ss',t,'-i',dst/'final.mp4','-frames:v','1','-vf','scale=360:640',dst/f'controle-{t}.jpg'])
 ff(['-ss',3,'-i',dst/'comparaison.mp4','-frames:v','1',dst/'comparaison.jpg'])
 for f in ['final.mp4','comparaison.mp4']:ff(['-i',dst/f,'-map','0:v','-map','0:a','-f','null','-'])
 for f in ['histoire.json','script.txt','timings-oraux.json','legende.txt','publication.txt','CREDITS.md']:shutil.copy2(ROOT/'out/revisions-archives-14nov-2026'/str(n)/f,dst/f)
 print(f'RENDU {n} {dur(dst/"final.mp4")}',flush=True)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,[27,28]))
