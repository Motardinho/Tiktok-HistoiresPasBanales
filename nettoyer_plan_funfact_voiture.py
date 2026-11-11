from pathlib import Path
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
w=next((ROOT/'out').glob('14-*'));m=w/'_montage/ouverture-titre-puis-rang';a=1280/30;b=1372/30;span=b-a
source=ROOT/'assets/sources-reelles/bugatti-record.mp4'
g="[0:v]split[a][b];[a]crop=iw:trunc(ih*0.12/2)*2:0:trunc(ih*0.12/2)*2,scale=1080:1920,gblur=sigma=15[bg];[b]crop=iw:trunc(ih*0.74/2)*2:0:(ih-oh)/2,scale=1080:-2,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/45,(H-Y-1)/45))'[fg];[bg][fg]overlay=0:900,fps=30,setsar=1,format=yuv420p[v]"
run(['ffmpeg','-v','error','-y','-ss','25.8','-i',str(source),'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-frames:v','92','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2',str(m/'bugatti-funfact.mp4')])
g=f'[0:v]trim=end={a},setpts=PTS-STARTPTS,fps=30[a];[1:v]setpts=PTS-STARTPTS,fps=30[b];[0:v]trim=start={b},setpts=PTS-STARTPTS,fps=30[c];[a][b][c]concat=n=3:v=1:a=0[v]'
run(['ffmpeg','-v','error','-y','-i',str(w/'_montage/base-hpb-v13.mp4'),'-i',str(m/'bugatti-funfact.mp4'),'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'base-voiture.mp4')])
d=read(w/'histoire.json');d['correction_locale']['base']=str((m/'base-voiture.mp4').relative_to(w));save(w/'histoire.json',d);save(m/'correction-plan-funfact.json',dict(debut=a,fin=b,source=str(source.relative_to(ROOT)),entree_source=25.8,raison='Retirer les intervenants tronqués et montrer la voiture pendant le fun fact.'))
print('14 : fun fact illustré par la voiture en mouvement',flush=True)
