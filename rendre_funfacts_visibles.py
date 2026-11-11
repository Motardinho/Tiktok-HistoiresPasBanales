"""Rend les anecdotes existantes identifiables sans son, sans changer la narration."""
import json, shutil, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import unicodedata
from montage_reel import ROOT, run
from comparer_lot_16_18 import compare

FACTS = {
14: (42.68,47.60,['300+ : LA BARRE DES','300 MILES/H FRANCHIE']),
15: (35.40,45.60,['LE PREMIER FEU AU GAZ','A EXPLOSÉ']),
16: (70.40,75.95,['UNE BOULANGERIE','SUR UN PORTE-AVIONS']),
17: (32.48,38.80,['LES FEMELLES ÉTUDIÉES','PESAIENT 11 À 12 G']),
18: (30.20,38.80,['LE PLUS LONG LITTORAL','DU MONDE EST AU CANADA']),
}

def make_card(n):
    w=next((ROOT/'out').glob(f'{n}-*'));m=w/'_montage';lines=FACTS[n][2]
    im=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(im)
    font=lambda size:ImageFont.truetype(str(ROOT/'assets/fonts/Poppins-ExtraBold.ttf'),size)
    size=58
    while max(d.textbbox((0,0),line,font=font(size))[2] for line in lines)>880:size-=1
    f=font(size);header=font(48)
    body=d.textbbox((0,0),'H',font=f);cap_height=body[3]-body[1]
    hbox=d.textbbox((0,0),'FUN FACT',font=header);hh=hbox[3]-hbox[1]
    top=430 if n==17 else 530;first=top+22+hh+24;bottom=first+len(lines)*cap_height+(len(lines)-1)*8+22
    d.rounded_rectangle((65,top,1015,bottom),radius=10,fill=(18,21,28,230))
    d.text(((1080-hbox[2])/2,top+22-hbox[1]),'FUN FACT',font=header,fill='#FFE24A')
    layout=[]
    for i,line in enumerate(lines):
        plain=''.join(c for c in unicodedata.normalize('NFD',line) if not unicodedata.combining(c))
        box=d.textbbox((0,0),line,font=f);bodybox=d.textbbox((0,0),plain,font=f);y=first+i*(cap_height+8)
        d.text(((1080-(box[2]-box[0]))/2,y-bodybox[1]),line,font=f,fill='#F7F3E9')
        layout.append(dict(texte=line,taille=size,haut_corps=y,bas_corps=y+cap_height,interligne=8,accents_en_superposition=True))
    im.save(m/'funfact-visible.png')
    (m/'funfact-layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2),encoding='utf-8')

def render(n):
    w=next((ROOT/'out').glob(f'{n}-*')); m=w/'_montage'
    archive=m/'avant-funfact-visible'; archive.mkdir(exist_ok=True)
    for name in ['final.mp4','comparaison.mp4','histoire.json']:
        if not (archive/name).exists(): shutil.copy2(w/name,archive/name)
    start,end,lines=FACTS[n];make_card(n)
    target=m/'final-funfact-visible.mp4'
    run(['ffmpeg','-v','error','-y','-i',str(archive/'final.mp4'),'-loop','1','-framerate','30','-i','funfact-visible.png',
         '-filter_complex_threads','1','-filter_complex',f'[0:v][1:v]overlay=0:0:enable=between(t\\,{start}\\,{end}):shortest=1[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    info=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height','-of','json',str(target)]))
    assert float(info['format']['duration'])>60
    video=next(s for s in info['streams'] if s['codec_type']=='video');assert (video['width'],video['height'])==(1080,1920)
    target.replace(w/'final.mp4');compare(w)
    story=json.loads((w/'histoire.json').read_text(encoding='utf-8'))
    story['fun_fact_affichage']={'debut':start,'fin':end,'texte':lines,'mention':'FUN FACT'}
    (w/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
    report=dict(numero=n,debut=start,fin=end,texte=lines,sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest(),comparaison_a_jour=(w/'comparaison.mp4').stat().st_mtime>=(w/'final.mp4').stat().st_mtime)
    (m/'controle-funfact-visible.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(n,'fun fact visible et comparaison actualisée',flush=True)

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,FACTS))
