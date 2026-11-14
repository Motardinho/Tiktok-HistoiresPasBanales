from pathlib import Path
import subprocess,json,math
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent
def ff(a):subprocess.run(['ffmpeg','-v','error','-y',*map(str,a)],check=True)
def check(n):
 d=OUT/str(n);plans=json.loads((d/'plans.json').read_text(encoding='utf-8'));font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
 for page in range(0,len(plans),5):
  sheet=Image.new('RGB',(720,5*450),'#171717');draw=ImageDraw.Draw(sheet)
  for row,p in enumerate(plans[page:page+5]):
   for col,t in enumerate([p['start']+.04,p['start']+p['duration']/2,p['start']+p['duration']-.1]):
    f=d/'qa-frame.png';ff(['-ss',t,'-i',d/'final.mp4','-frames:v','1','-vf','scale=240:426',f]);sheet.paste(Image.open(f),(col*240,row*450));draw.text((col*240,row*450+427),f'Plan {page+row} / {t:.2f}s',font=font,fill='yellow')
  sheet.save(d/f'controle-{page//5}.jpg')
 for t in [0,3,15,35,60,67]:ff(['-ss',t,'-i',d/'final.mp4','-frames:v','1','-vf','scale=360:640',d/f'frame-{t}.jpg'])
 im=Image.open(d/'frame-3.jpg').convert('RGBA');draw=ImageDraw.Draw(im)
 draw.rounded_rectangle((20,25,340,55),8,fill=(40,40,40,180));draw.text((30,31),'Recherche TikTok',font=font,fill='white')
 draw.text((310,330),'♡\n\n○\n\n↗',font=font,fill='white');draw.rectangle((0,520,360,640),fill=(10,10,10,90));draw.text((15,530),'@histoirespasbanales\nHistoire vraie…\n♫ Son original',font=font,fill='white');im.convert('RGB').save(d/'simulation-tiktok.jpg')
 ff(['-ss',3,'-i',d/'comparaison.mp4','-frames:v','1',d/'comparaison.jpg'])
 for f in ['final.mp4','comparaison.mp4']:
  r=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(d/f),'-f','null','-'],capture_output=True,text=True);(d/(f+'.decode.txt')).write_text(r.stderr or 'Décodage complet sans erreur.',encoding='utf-8');assert r.returncode==0
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(d/'base.mp4'),'-vf','freezedetect=n=-45dB:d=0.6','-an','-f','null','-'],capture_output=True,text=True)
 (d/'controle-gels.txt').write_text('\n'.join(l for l in r.stderr.splitlines() if 'freeze' in l) or 'Aucun gel détecté >= 0,6 s',encoding='utf-8')
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(d/'final.mp4'),'-af','volumedetect,silencedetect=n=-45dB:d=0.8','-vn','-f','null','-'],capture_output=True,text=True)
 (d/'controle-audio-technique.txt').write_text('\n'.join(l for l in r.stderr.splitlines() if any(k in l for k in ['volume','silence_'])),encoding='utf-8')
 print('CONTROLE TECHNIQUE',n,flush=True)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as p:list(p.map(check,[31,33]))
