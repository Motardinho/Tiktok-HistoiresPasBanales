import json, subprocess, sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path('out/39-l-entraineur-boycotte-dans-tout-le-pays');m=p/'_montage';qa=m/'controle';qa.mkdir(exist_ok=True)
plans=json.loads((m/'montage.json').read_text(encoding='utf8'))
final='final' in sys.argv
font=ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf',17)
evidence=[]
for page in range((len(plans)+3)//4):
 sheet=Image.new('RGB',(1080,4*680),'#15181d');dr=ImageDraw.Draw(sheet)
 for j,row in enumerate(plans[page*4:page*4+4]):
  i=page*4+j;dur=row['fin']-row['debut']
  for k,rel in enumerate([.04,dur/2,max(.04,dur-.06)]):
   at=row['debut']+rel if final else rel
   src=p/'final.mp4' if final else m/f'plan-{i:02}.mp4'
   dest=qa/f'{"final" if final else "plan"}-{i:02}-{k}.jpg'
   subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(src),'-frames:v','1','-vf','scale=360:640',str(dest)],check=True)
   sheet.paste(Image.open(dest),(k*360,j*680+40))
   dr.text((k*360+6,j*680+8),f'Plan {i:02} - {row["debut"]+rel:.2f}s',font=font,fill='white')
   evidence.append(dict(fichier=str(dest),timeline=row['debut']+rel,source=row['source']))
 sheet.save(qa/f'{"final" if final else "plans"}-page-{page}.jpg')
(qa/f'{"final" if final else "plans"}-captures.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
print('Captures',len(evidence),flush=True)
