import json,subprocess,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];P=R/'out/47-dortmund-attentat-en-bourse';Q=P/'controle';Q.mkdir(exist_ok=True)
plans=json.loads((P/'plans.json').read_text(encoding='utf8'))
def snap(t,f,width=360):
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(P/'final.mp4'),'-vf',f'scale={width}:-1','-frames:v','1',str(f)],check=True,capture_output=True)
for start in range(0,len(plans),4):
 rows=plans[start:start+4];im=Image.new('RGB',(1080,len(rows)*666),'#151515');dr=ImageDraw.Draw(im)
 for j,p in enumerate(rows):
  for k,t in enumerate([p['start']+.01,p['start']+p['duration']/2,p['start']+p['duration']-.07]):
   f=Q/f"plan-{p['numero']:02}-{k}.jpg";snap(t,f);im.paste(Image.open(f),(k*360,j*666));dr.text((k*360+8,j*666+642),f"{p['numero']} - {t:.2f}s",fill='white')
 im.save(Q/f'planche-{start//4}.jpg')
snap(0,Q/'premiere-image.jpg',1080)
sim=Image.new('RGB',(1080,680),'#151515')
font=ImageFont.truetype(str(R/'assets/fonts/Poppins-ExtraBold.ttf'),32)
for k,t in enumerate([0,37,49]):
 f=Q/f'tiktok-{k}.jpg';snap(t,f,1080);im=Image.open(f).convert('RGBA');ui=Image.new('RGBA',im.size);dr=ImageDraw.Draw(ui)
 dr.rounded_rectangle((90,65,990,170),radius=22,fill=(20,20,20,180));dr.text((120,98),'Rechercher',font=font,fill='white')
 dr.rectangle((0,1450,1080,1920),fill=(0,0,0,165))
 for j,s in enumerate(['@histoirespasbanales','Dortmund : un attentat pour la Bourse.','14 ans, suffisant ou trop peu ?','#Football #FaitsDivers']):dr.text((50,1470+70*j),s,font=font,fill='white')
 for y in [850,1040,1220,1390]:dr.ellipse((970,y,1030,y+60),fill='white')
 im=Image.alpha_composite(im,ui).convert('RGB');sim.paste(im.resize((360,640)),(k*360,35))
ImageDraw.Draw(sim).text((10,8),'SIMULATION DU LECTEUR TIKTOK',fill='white');sim.save(P/'apercu-tiktok.jpg')
print('Captures de contrôle prêtes',flush=True)

