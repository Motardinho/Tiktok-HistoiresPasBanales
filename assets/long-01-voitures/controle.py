from production import *
from PIL import Image,ImageDraw
import math
def boards():
 ps=json.loads((WORK/'plans.json').read_text(encoding='utf8'));folder=WORK/'controle';folder.mkdir(exist_ok=True)
 for page in range(math.ceil(len(ps)/6)):
  board=Image.new('RGB',(960,6*204),'#13141b');draw=ImageDraw.Draw(board)
  for row,p in enumerate(ps[page*6:page*6+6]):
   src=WORK/f'plan-{p["i"]:03}.mp4';dur=p['end']-p['start']
   for j,at in enumerate([.05,dur/2,max(.05,dur-.1)]):
    out=folder/f'p{p["i"]:03}-{j}.jpg'
    if not out.exists():subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(at),'-i',str(src),'-frames:v','1','-vf','scale=320:180',str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    board.paste(Image.open(out),(j*320,row*204))
   draw.text((6,row*204+182),f'Plan {p["i"]:03} | {p["start"]:.1f}-{p["end"]:.1f}s | {Path(p["source"]).stem} @{p["entree"]}',fill='white')
  board.save(folder/f'plans-{page:02}.jpg',quality=88)
  print('Planche',page,flush=True)
if __name__=='__main__':boards()
