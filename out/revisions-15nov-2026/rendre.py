from pathlib import Path
import json,subprocess,shutil,sys,math,re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageFont
import yaml
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;S=OUT/'sources'
sys.path.insert(0,str(ROOT))
from narrateur.assemble import write_subtitles
from monter_lot_21_23 import caption_words
from securiser_habillage_tiktok import wrap_caption
def ff(a,cwd=None):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,a)],cwd=cwd,check=True)
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def dur(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))
def tm(s):
 h,m,t=s.split(':');return int(h)*3600+int(m)*60+float(t)
def ast(t):
 c=round(max(t,0)*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'

def docs():
 # Extraits photographiques limités des pages réellement consultées ; pas de faux document.
 gu=Image.open(S/'guinness-record.png');ga=Image.open(S/'guardian-sanctions.png');head=Image.open(S/'guinness-page.png')
 font=ImageFont.truetype(str(ROOT/'assets/fonts/Poppins-ExtraBold.ttf'),28)
 for name in ['record','date','sanctions']:
  im=Image.new('RGB',(1080,1920),'#eeece6');d=ImageDraw.Draw(im)
  if name in ['record','date']:
   logo=head.crop((4,10,90,87));im.paste(logo.resize((240,216)),(75,265))
   # Citation exacte, recomposée en grands caractères pour la lecture téléphone.
   # Ce sont des extraits documentaires attribués, pas une fausse capture intégrale.
   serif=ImageFont.truetype('C:/Windows/Fonts/times.ttf',76)
   rows=['The most own goals','scored by a team','in a single football','match is']
   for j,row in enumerate(rows):d.text((80,550+j*78),row,font=serif,fill='#102d48')
   d.text((75,850),'149',font=ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf',180),fill='#102d48')
   d.text((340,360),'31 OCTOBER 2002',font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',37),fill='#102d48')
   d.text((85,1530),'Extrait — Guinness World Records',font=font,fill='#173954')
   if name=='date':
    # Une autre échelle du même document, sans information supplémentaire.
    im=im.resize((1134,2016)).crop((20,35,1100,1955))
  else:
   logo=ga.crop((1160,75,1502,179));logo=logo.resize((650,198));im.paste(logo,(80,300))
   serif=ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf',100)
   for j,row in enumerate(['Team punished','for 149-0','own-goal farce']):d.text((75,650+j*125),row,font=serif,fill='#102d48')
   date=ga.crop((317,390,530,414)).resize((780,88));im.paste(date,(80,530))
   d.text((85,1530),'Extrait — The Guardian',font=font,fill='#173954')
  im.save(S/f'document-{name}.png')

def render(n):
 d=OUT/str(n);src=next((ROOT/'out').glob(f'{n}-*'));story=json.loads((d/'histoire.json').read_text(encoding='utf-8'))
 if n==31:
  cut=5.36;length=dur(src/'_montage/mix.wav')-cut
  ff(['-ss',cut,'-i',src/'_montage/mix.wav','-t',length,'-c:a','pcm_s16le',d/'mix.wav'])
  lines=[]
  for l in (src/'_montage/sous-titres.ass').read_text(encoding='utf-8-sig').splitlines():
   if l.startswith('Dialogue:'):
    a=l.split(',',9)
    if a[3]!='Default' or tm(a[2])<=cut:continue
    a[1]=ast(tm(a[1])-cut);a[2]=ast(tm(a[2])-cut);l=','.join(a)
   lines.append(l)
  (d/'sous-titres.ass').write_text('\n'.join(lines),encoding='utf-8')
  seq=[
   (2.4,'VFuZMU9rGA8',354,'paul'),(2.8,'VFuZMU9rGA8',394,'paul'),
   (3.2,'VFuZMU9rGA8',414,'paul'),(3.96,'VFuZMU9rGA8',435.3,'paul'),
   (3.72,'VFuZMU9rGA8',484,'paul'),(3.2,'VFuZMU9rGA8',494,'paul'),
   (3.24,'VFuZMU9rGA8',514,'paul'),(3.5,'KCLUsiKZP1s',38,'courtwide'),
   (3.1,'VFuZMU9rGA8',395,'paul'),(2.84,'KCLUsiKZP1s',32,'courtlawyer'),
   (4.5,'hoJtxb9Enyw',19,'mathias'),(4.46,'hoJtxb9Enyw',79,'mathias'),
   (3.5,'KCLUsiKZP1s',11.5,'court'),(3.54,'KCLUsiKZP1s',54,'courtwide'),
   (3.2,'KCLUsiKZP1s',8.3,'court'),(3.36,'KCLUsiKZP1s',44,'courtlawyer'),
   (2.1,'VFuZMU9rGA8',485,'paul'),(5.38,'freres-pogba.jpg',0,'photo'),
   (3.3,'freres-pogba.jpg',0,'photo'),(length-65.3,'VFuZMU9rGA8',515,'paul')]
 else:
  tim=json.loads((d/'_montage/timings-oraux.json').read_text(encoding='utf-8'));length=tim['duration']
  ff(['-i',d/'_montage/voix.mp3','-stream_loop','-1','-i',src/'_montage/musique.wav','-filter_complex','[1:a]volume=0.13[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.96[a]','-map','[a]','-t',length,d/'mix.wav'])
  cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'));words=caption_words(tim['words'],story['affichage']);words[0]['start']=0
  write_subtitles(cfg,words,d/'sous-titres.ass')
  lines=[]
  for l in (d/'sous-titres.ass').read_text(encoding='utf-8').splitlines():
   if l.startswith('Dialogue:'):
    a=l.split(',',9);txt=wrap_caption(a[9],90);size=90
    if txt.count(r'\N')>2:size=80;txt=wrap_caption(a[9],size)
    a[9]=r'{\an2\pos(540,1370)\fs'+str(size)+r'\fsp0}'+txt;l=','.join(a)
   lines.append(l)
  (d/'sous-titres.ass').write_text('\n'.join(lines),encoding='utf-8')
  seq=[(2.5,'document-record.png',0,'doc'),(3.18,'document-date.png',0,'doc'),
   (4.2,'document-date.png',0,'doc'),(4.28,'document-record.png',0,'doc'),
   (3.2,'2G3xDfxozwQ',33,'club'),(3.24,'2G3xDfxozwQ',55,'club'),
   (4.8,'document-record.png',0,'doc'),(4.84,'document-date.png',0,'doc'),
   (3.2,'2G3xDfxozwQ',65,'club'),(3.2,'document-record.png',0,'doc'),(3.2,'document-record.png',0,'doc'),
   (3.6,'2G3xDfxozwQ',84,'club'),(3.6,'2G3xDfxozwQ',94,'club'),
   (4.04,'document-sanctions.png',0,'doc'),(4,'document-sanctions.png',0,'doc'),
   (2.9,'document-record.png',0,'doc'),(2.9,'document-date.png',0,'doc'),
   (3.5,'2G3xDfxozwQ',40,'club'),(3.78,'2G3xDfxozwQ',73,'club')]
 # Arrondir chaque frontière à l'image, jamais allonger un extrait gelé.
 assert abs(sum(x[0] for x in seq)-length)<.08,(n,sum(x[0] for x in seq),length)
 plans=[];start=0
 for i,(seconds,source,ss,kind) in enumerate(seq):
  path=S/(source if '.' in source else source+'.mp4');frames=round((start+seconds)*30)-round(start*30)
  f=d/f'plan-{i:02}.mp4'
  crops={'paul':'crop=608:1080:1120:0','mathias':'crop=236:420:118:290','court':'crop=404:720:680-15*t:0','arrival':'crop=404:720:740:0','courtside':'crop=404:720:650:0','courtwide':'crop=404:720:530:0','courtlawyer':'crop=404:720:540:0'}
  if kind=='paul' and 480<=ss<500:crops['paul']='crop=608:1080:950:0'
  if kind=='paul' and ss>=510:crops['paul']='crop=608:1080:1050:0'
  inp=['-loop','1','-i',path] if kind in ['photo','doc'] else ['-ss',ss,'-i',path]
  if kind in crops:
   graph=crops[kind]+',scale=1080:1920:flags=lanczos,fps=30,setsar=1,format=yuv420p'
   args=['-vf',graph]
  elif kind=='club':
   graph='[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.12[bg];[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:470,fps=30,setsar=1,format=yuv420p[v]';args=['-filter_complex_threads','1','-filter_complex',graph,'-map','[v]']
  elif kind=='photo':
   graph='[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:520,zoompan=z=1+0.00015*on:x=iw/2-iw/zoom/2:y=ih/2-ih/zoom/2:d=1:s=1080x1920:fps=30,format=yuv420p[v]';args=['-filter_complex_threads','1','-filter_complex',graph,'-map','[v]']
  else:
   graph="scale=2160:3840,zoompan=z='1+0.00018*on':x=iw/2-iw/zoom/2:y=ih/2-ih/zoom/2:d=1:s=1080x1920:fps=30,format=yuv420p";args=['-vf',graph]
  if n!=31 or i in [4,5,6,14,16,19] or not f.exists():ff([*inp,*args,'-an','-frames:v',frames,'-c:v','libx264','-preset','fast','-crf','20','-threads','3',f])
  plans.append(dict(start=start,duration=seconds,source=str(path),ss=ss,kind=kind,filter=graph));start+=seconds
 save(d/'plans.json',plans)
 (d/'concat.txt').write_text('\n'.join(f"file 'plan-{i:02}.mp4'" for i in range(len(plans))),encoding='utf-8')
 ff(['-f','concat','-safe','0','-i',d/'concat.txt','-c','copy',d/'base.mp4'])
 ff(['-i','base.mp4','-i','mix.wav','-loop','1','-i','logo.png','-filter_complex_threads','1','-filter_complex','[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v]','-map','[v]','-map','1:a','-t',length,'-c:v','libx264','-preset','fast','-crf','19','-threads','3','-c:a','aac','-b:a','192k','-movflags','+faststart','final.mp4'],d)
 ref=src/'version-validee/final.mp4';total=max(dur(ref),dur(d/'final.mp4'))
 graph=f'[0:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[l];[1:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[r];[l][r]hstack[v];[0:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a0];[1:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a1]'
 ff(['-i',ref,'-i',d/'final.mp4','-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','[a1]','-map','[a0]','-c:v','libx264','-preset','fast','-crf','21','-threads','3','-c:a','aac','-b:a','128k','-metadata:s:a:0','title=Nouvelle version HPB','-metadata:s:a:1','title=Ancienne version validee','-disposition:a:0','default','-disposition:a:1','0','-movflags','+faststart',d/'comparaison.mp4'])
 print('RENDU',n,dur(d/'final.mp4'),flush=True)

if __name__=='__main__':
 docs()
 with ThreadPoolExecutor(max_workers=2) as p:list(p.map(render,[31,33]))
