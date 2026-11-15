from production import *
from PIL import Image,ImageDraw
from concurrent.futures import ThreadPoolExecutor

video=OUT/'essai-long-v5.mp4'
folder=WORK/'v5/controle-export';folder.mkdir(exist_ok=True)
times=[0,.3,.7,1,1.3,1.6,2,2.4,2.8,2.9,3.05,3.2,4.5,50,137,481.9]
def grab(t):
 p=folder/f'{t:06.2f}.jpg'
 subprocess.run(['ffmpeg','-y','-v','error','-threads','1','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(p)],check=True)
 return p
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(grab,times))
for page in range((len(times)+7)//8):
 board=Image.new('RGB',(960,4*294),'#171717');d=ImageDraw.Draw(board)
 for i,t in enumerate(times[page*8:page*8+8]):
  x=(i%2)*480;y=(i//2)*294
  board.paste(Image.open(folder/f'{t:06.2f}.jpg').resize((480,270)),(x,y));d.text((x+5,y+273),f'{t:.2f} s',fill='white')
 board.save(folder/f'final-{page}.jpg',quality=92)
mobile=Image.new('RGB',(360,4*224),'#171717');d=ImageDraw.Draw(mobile)
for i,t in enumerate([.3,1.3,2.4,3.2]):
 mobile.paste(Image.open(folder/f'{t:06.2f}.jpg').resize((360,202)),(0,i*224));d.text((5,i*224+205),f'{t} s — 360 px',fill='white')
mobile.save(folder/'mobile.jpg',quality=95)
meta=probe(video);writej(folder/'probe.json',meta)
with (folder/'decodage.txt').open('w') as f:
 r=subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(video),'-f','null','-'],stdout=f,stderr=f)
writej(folder/'resultat-technique.json',{'decodage_exit':r.returncode,'video':str(video),'duree':meta['format']['duration'],'captures':times,'ecoute_effectuee':False,'visionnage_continu_effectue':False})
with (folder/'niveaux.txt').open('w') as f:
 subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=8:print_format=json','-f','null','-'],stdout=f,stderr=f)
print('Contrôle technique et captures terminés',flush=True)
