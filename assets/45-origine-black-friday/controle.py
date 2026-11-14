import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'out/45-origine-black-friday'
plans=json.loads((P/'plans.json').read_text(encoding='utf8'))
font=ROOT/'assets/fonts/Poppins-ExtraBold.ttf'
def ff(args):subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],check=True,capture_output=True)
def snap(src,t,path,width=360):ff(['-ss',t,'-i',src,'-frames:v',1,'-vf',f'scale={width}:-1',path])
def qa(v):
 w=P/v;q=w/'controle';q.mkdir(exist_ok=True)
 for start in range(0,len(plans),5):
  sheet=Image.new('RGB',(1080,5*665),'#141414');draw=ImageDraw.Draw(sheet)
  for j,p in enumerate(plans[start:start+5]):
   for c,t in enumerate([p['start']+.01,p['start']+p['duration']/2,p['start']+p['duration']-.07]):
    dst=q/f"plan-{p['numero']:02}-{c}.jpg";snap(w/'final.mp4',t,dst);sheet.paste(Image.open(dst),(360*c,665*j));draw.text((360*c+5,665*j+642),f"plan {p['numero']} / {t:.2f}s",fill='white')
  sheet.save(q/f'planche-{start//5}.jpg')
 for t in [0,1,2,3,4,5,65,66]:snap(w/'final.mp4',t,q/f'image-{t}.jpg')
 sim=Image.new('RGB',(1080,690),'#121212');draw=ImageDraw.Draw(sim)
 for j,t in enumerate([0,38,65]):
  tmp=q/f'tiktok-{j}.jpg';snap(w/'final.mp4',t,tmp,1080);im=Image.open(tmp).convert('RGBA');ui=Image.new('RGBA',im.size);a=ImageDraw.Draw(ui)
  a.rounded_rectangle((90,65,990,170),radius=24,fill=(20,20,20,185));a.text((125,90),'Rechercher',font=ImageFont.truetype(str(font),46),fill='white')
  a.rectangle((0,1420,1080,1920),fill=(0,0,0,145))
  for k,s in enumerate(['@histoirespasbanales','Le Black Friday, un nom de policiers.','Bonnes affaires ou piège à achats ?','#BlackFriday #HistoireVraie']):a.text((55,1440+k*80),s,font=ImageFont.truetype(str(font),35),fill='white')
  for y in [850,1040,1220,1390]:a.ellipse((965,y,1035,y+70),fill='white')
  im=Image.alpha_composite(im,ui).convert('RGB').resize((360,640));sim.paste(im,(j*360,45));draw.text((j*360+8,12),f'SIMULATION TIKTOK / {t}s',fill='white')
 sim.save(w/'apercu-tiktok.jpg')
 if (w/'comparaison.mp4').exists():snap(w/'comparaison.mp4',5,q/'comparaison.jpg',1080)
 print(v,'captures prêtes',flush=True)
if __name__=='__main__':qa(sys.argv[1])
