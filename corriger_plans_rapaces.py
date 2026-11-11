from pathlib import Path
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
w=next((ROOT/'out').glob('17-*'));root=w/'_montage';m=root/'corrections-locales-v1';old=root/'podium-mondial-v6/_montage';assets=ROOT/'assets/lot-16-18/nouveaux-rapaces'
# Durée en images conservée : seuls les plans rejetés sont remplacés.
segments=[('base',0,91),('gyr',.5,56),('photo',0,34),('base',181/30,104),('avion',0,83),('base',368/30,120),('photo',0,105),('base',593/30,877),('stoop',75.7,63),('base',1533/30,88),('base',1621/30,120),('base',1741/30,383)]
paths={'avion':assets/'avion-tourisme-pexels-31662106.mp4','base':old/'base-uniforme.mp4','gyr':assets/'gyrfalcon-olivier.mp4','photo':old/'photo-portrait-v3-gyrfalcon-flight.png','stoop':assets/'natgeo-attaque-faucon.mp4','natgeo':assets/'natgeo-attaque-faucon.mp4'}
args=[];parts=[];edit=[];cursor=0
for i,(kind,start,frames) in enumerate(segments):
 args+=['-threads','1']+(['-loop','1','-framerate','30'] if kind=='photo' else ['-ss',str(start)])+['-i',str(paths[kind])]
 crop='crop=405:720:675:0,scale=1080:1920,' if kind=='gyr' else "scale=1280:720,crop=405:720:x='500-20*t':y=0,scale=1080:1920," if kind=='stoop' else 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,' if kind=='natgeo' else ''
 parts.append(f'[{i}:v]{crop}fps=30,trim=end_frame={frames},settb=1/30,setpts=N,format=yuv420p,setsar=1[v{i}]');edit.append(dict(debut=cursor/30,fin=(cursor+frames)/30,source=str(paths[kind].relative_to(ROOT)),source_start=start,remplacement=kind));cursor+=frames
assert cursor==2124
parts.append(''.join(f'[v{i}]' for i in range(len(segments)))+f'concat=n={len(segments)}:v=1:a=0[v]')
run(['ffmpeg','-v','error','-y']+args+['-filter_complex_threads','1','-filter_complex',';'.join(parts),'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'base.mp4')])
d=read(w/'histoire.json');d['correction_locale']['base']=str((m/'base.mp4').relative_to(w));save(w/'histoire.json',d);save(m/'plans-corriges.json',edit)
print('17 : cadrage gerfaut et piqué vidéo pèlerin remplacés',flush=True)
