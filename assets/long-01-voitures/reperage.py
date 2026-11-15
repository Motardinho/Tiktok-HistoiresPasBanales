from pathlib import Path
import sys,subprocess,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'out/long-01-voitures-vitesse/_montage/reperage';O.mkdir(parents=True,exist_ok=True)
for arg in sys.argv[1:]:
 p=ROOT/arg
 d=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(p)]))['format']['duration'])
 step=10 if d>100 else 4
 folder=O/p.stem;folder.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(p),'-vf',f'fps=1/{step},scale=320:180','-q:v','3',str(folder/'%03d.jpg')],check=True)
 frames=sorted(folder.glob('*.jpg'))
 for page in range((len(frames)+15)//16):
  im=Image.new('RGB',(1280,816),'#15151a');draw=ImageDraw.Draw(im)
  for j,f in enumerate(frames[page*16:page*16+16]):
   x=j%4*320;y=j//4*204;im.paste(Image.open(f),(x,y))
   draw.text((x+6,y+182),f'{p.stem} ~{(page*16+j+.5)*step:.0f}s',fill='white')
  im.save(O/f'{p.stem}-{page}.jpg',quality=88)
 print(p.stem,len(frames),'frames',flush=True)
