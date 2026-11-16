from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
from plans import PLANS, FIN, ENTREE, FINAL

qa = Path('controle')
qa.mkdir(exist_ok=True)
def sheet(name, frames, cols, width, video='final.mp4', simulate=False):
    dest = qa / name
    dest.mkdir(exist_ok=True)
    filt = '+'.join(f'eq(n,{f})' for f in frames)
    subprocess.run(['ffmpeg','-v','error','-y','-i',video,'-an','-vf',f"select='{filt}',scale={width}:{width*16//9}",'-fps_mode','vfr',str(dest/'%03d.jpg')],check=True)
    height = width * 16 // 9
    board = Image.new('RGB',(cols*width,((len(frames)+cols-1)//cols)*(height+20)), '#16191e')
    draw = ImageDraw.Draw(board)
    for i, (f, file) in enumerate(zip(frames, sorted(dest.glob('[0-9]*.jpg')),strict=True)):
        im = Image.open(file).convert('RGBA')
        if simulate:
            ui = Image.new('RGBA',im.size)
            d = ImageDraw.Draw(ui)
            d.rounded_rectangle((25,22,330,60),radius=9,fill=(24,24,24,175))
            d.text((44,36),'Rechercher',fill='white')
            for y,label in [(280,'Profil'),(345,"J’aime"),(406,'Com.'),(457,'Partager')]:
                d.ellipse((324,y,348,y+24),fill=(255,255,255,220))
                d.text((307,y+25),label,fill='white')
            d.rectangle((0,476,360,640),fill=(0,0,0,150))
            for y,label in [(482,'@histoirespasbanales'),(506,'Kevin Mayer, de zéro au record du monde'),(529,'#Décathlon #Athlétisme'),(610,'Accueil       Amis       +       Messages')]:
                d.text((14,y),label,fill='white')
            im = Image.alpha_composite(im,ui)
        x, y = i%cols*width, i//cols*(height+20)
        board.paste(im.convert('RGB'),(x,y+20))
        draw.text((x+5,y+3),f'{f/30:05.2f} s',fill='white')
    board.save(qa/f'{name}.jpg',quality=92)

cuts = [round(p[0]*30) for p in PLANS]+[round(FIN*30)]
frames = [[a,(a+b)//2,b-1] for a,b in zip(cuts,cuts[1:])]
for i in range(0,len(frames),3):
    sheet(f'plans-{i//3}',[f for group in frames[i:i+3] for f in group],9,180)
sheet('ouverture',list(range(0,150,5)),10,144)
sheet('tiktok',[14,305,round(ENTREE*30)+10,round(FIN*30)-12],4,360,simulate=True)
