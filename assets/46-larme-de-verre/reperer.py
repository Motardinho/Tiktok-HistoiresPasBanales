import sys, subprocess, math
from pathlib import Path
from PIL import Image, ImageDraw
A=Path(__file__).resolve().parent
def sheet(name, step=5, start=0, end=None):
    src=A/(name+'.mp4'); folder=A/('reperage-'+name);folder.mkdir(exist_ok=True)
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(src)]))
    end=min(end or duration,duration)
    times=list(range(int(start),int(end),int(step)))
    for k in range(0,len(times),24):
        ts=times[k:k+24]; im=Image.new('RGB',(1280,math.ceil(len(ts)/4)*205),'#151515');d=ImageDraw.Draw(im)
        for j,t in enumerate(ts):
            target=folder/f'{t:04}.jpg'
            if not target.exists():subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(src),'-vf','scale=320:180','-frames:v','1',str(target)],check=True,capture_output=True)
            x=j%4*320;y=j//4*205;im.paste(Image.open(target),(x,y));d.text((x+5,y+182),str(t)+' s',fill='white')
        dest=folder/f'sheet-{start:03}-{step}-{k//24:02}.jpg';im.save(dest);print(dest,flush=True)
if __name__=='__main__':sheet(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 5,int(sys.argv[3]) if len(sys.argv)>3 else 0,int(sys.argv[4]) if len(sys.argv)>4 else None)

