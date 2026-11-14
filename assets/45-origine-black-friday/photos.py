import requests,json,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
p=Path('assets/45-origine-black-friday'); rows=json.loads((p/'recherche-photos.json').read_text(encoding='utf8'))
sel=[2,3,4,28,32,35]
for i in sel:
 r=rows[i];f=p/f'photo-{i}.jpg'
 if not f.exists():
  b=requests.get(r['url'].split('?')[0],headers={'User-Agent':'HPB editorial research/1.0'},timeout=90);b.raise_for_status()
  tmp=p/f'photo-{i}.raw';tmp.write_bytes(b.content)
  Image.open(tmp).convert('RGB').save(f,quality=95)
sheet=Image.new('RGB',(1200,800),'#202020');d=ImageDraw.Draw(sheet)
for j,i in enumerate(sel):
 im=ImageOps.contain(Image.open(p/f'photo-{i}.jpg'),(390,360));x=(j%3)*400;y=(j//3)*400;sheet.paste(im,(x,y+30));d.text((x+10,y+8),str(i),fill='white')
sheet.save(p/'photos.jpg')
(p/'photos-retenues.json').write_text(json.dumps([dict(index=i,**rows[i]) for i in sel],ensure_ascii=False,indent=2),encoding='utf8')

