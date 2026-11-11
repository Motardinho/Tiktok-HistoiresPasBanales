from pathlib import Path
import subprocess,json,sys
from PIL import Image,ImageDraw,ImageFont
root=Path.cwd();font=root/'assets/fonts/Poppins-ExtraBold.ttf'
def f(n):return ImageFont.truetype(str(font),n)
for n in (map(int,sys.argv[1:]) if len(sys.argv)>1 else range(13,19)):
 w=next((root/'out').glob(str(n)+'-*'));m=w/'_montage/tiktok-safe'
 if not m.exists():m=w/'_montage'
 d=json.loads((w/'histoire.json').read_text(encoding='utf-8'));duration=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'final.mp4')]))['format']['duration'])
 at=(d['fun_fact_affichage']['debut']+d['fun_fact_affichage']['fin'])/2 if n>=14 else 6.4
 sheet=Image.new('RGB',(1080,694),'#11151c');draw=ImageDraw.Draw(sheet)
 for i,t in enumerate([.6,at,duration-1.2]):
  p=m/f'controle-lecteur-{i}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(w/'final.mp4'),'-frames:v','1',str(p)],check=True)
  im=Image.open(p).convert('RGBA');ui=Image.new('RGBA',im.size);x=ImageDraw.Draw(ui)
  x.rounded_rectangle((90,65,990,170),radius=24,fill=(20,20,20,185));x.text((125,90),'Rechercher',font=f(46),fill='white')
  x.rectangle((0,1410,1080,1920),fill=(0,0,0,150));x.text((55,1430),'@histoirespasbanales',font=f(42),fill='white')
  for j,s in enumerate(["L'OM a acheté un match en 1993...", 'Glassmann : héros ou balance ?', '#histoirevraie #om #vaom']):x.text((55,1500+j*60),s,font=f(35),fill='white')
  x.text((55,1740),'Son original',font=f(35),fill='white');x.line((0,1810,1080,1810),fill='gray',width=2);x.text((100,1840),'Accueil     Amis      +      Messages',font=f(32),fill='white')
  for y,label in [(850,'Profil'),(1040,'J’aime'),(1220,'Com.'),(1390,'Partager')]:
   x.ellipse((965,y,1035,y+70),fill=(255,255,255,220));x.text((945,y+80),label,font=f(22),fill='white')
  im=Image.alpha_composite(im,ui).convert('RGB');im.resize((360,640),Image.Resampling.LANCZOS).save(m/f'apercu-simule-{i}.png');sheet.paste(im.resize((360,640),Image.Resampling.LANCZOS),(i*360,54));draw.text((i*360+10,14),f'{n} - {t:.1f}s - SIMULATION',font=f(16),fill='white')
 sheet.save(w/'apercu-tiktok.jpg')
print('Aperçus simulés prêts')

