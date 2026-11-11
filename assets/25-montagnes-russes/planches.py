"""Planches de repérage horodatées : python planches.py fichier.mp4 [pas_s] [debut] [fin]"""
import sys,subprocess,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
f=Path(sys.argv[1]);font=ImageFont.truetype('C:/Projets/Tiktok - MrBallen/assets/fonts/Poppins-ExtraBold.ttf',22)
d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)]))
step=float(sys.argv[2]) if len(sys.argv)>2 else max(2,d/40);a=float(sys.argv[3]) if len(sys.argv)>3 else 0;b=float(sys.argv[4]) if len(sys.argv)>4 else d
ts=[a+i*step for i in range(int((b-a)/step)+1) if a+i*step<d-.2]
W,H,C=384,216,5;tmp=Path('tmp');tmp.mkdir(exist_ok=True)
for page in range(0,len(ts),40):
    chunk=ts[page:page+40];rows=(len(chunk)+C-1)//C;sheet=Image.new('RGB',(W*C,H*rows),'black');dr=ImageDraw.Draw(sheet)
    for k,t in enumerate(chunk):
        o=tmp/f'{f.stem}-{t:.1f}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',str(f),'-frames:v','1','-vf',f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2',str(o)],check=True)
        x,y=(k%C)*W,(k//C)*H;sheet.paste(Image.open(o),(x,y));dr.rectangle((x,y,x+90,y+30),fill='black');dr.text((x+4,y+2),f'{t:.1f}s',font=font,fill='yellow')
    out=f'reperage-{f.stem}-{page//40+1:02}.jpg';sheet.save(out,quality=85);print(out,round(d,1),'s')
