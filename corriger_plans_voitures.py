"""Remplace les plans parasites à la source, sans recouvrir l'ancien montage."""
import shutil,json
from montage_reel import ROOT,SOURCES,run
from produire_lot_16_18 import read,save

w=next((ROOT/'out').glob('14-*'));m=w/'_montage';archive=m/'avant-controle-plans';archive.mkdir(exist_ok=True);base=m/'base-hpb-v13.mp4'
if not (archive/base.name).exists():shutil.copy2(base,archive/base.name)
old=archive/base.name
replacements=[
 (5.5,3.0,'ssc-tuatara',9,'0.68'),
 (8.5,3.0,'ssc-road',14,'0.4-0.05*t'),
 (45.7333333333333,2.43333333333333,'bugatti-record',170,'0.57'),
 (56.6666666666667,1.4,'yangwang-u9-xtreme-2025',52,'0.5'),
 (78.0666666666667,3.0,'yangwang-u9-xtreme-2025',53.5,'0.5'),
]
files=[]
for i,(at,dur,slug,start,cx) in enumerate(replacements):
 p=m/f'plan-corrige-v2-{i}.mp4';vf=f"crop=trunc(ih*9/16/2)*2:ih:max(0\\,min(iw-ow\\,iw*({cx})-ow/2)):0,scale=1080:1920,fps=30,setsar=1"
 if not p.exists():run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(SOURCES/(slug+'.mp4')),'-vf',vf,'-frames:v',str(round(dur*30)),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(p)])
 files.append(p)
duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(old)]).strip());inputs=['-i',str(old)]
for p in files:inputs+=['-i',str(p)]
parts=[];labels=[];cursor=0
for i,(at,dur,*_) in enumerate(replacements):
 if at>cursor:
  label=f'a{i}';parts.append(f'[0:v]trim=start={cursor}:end={at},setpts=PTS-STARTPTS,fps=30[{label}]');labels.append(f'[{label}]')
 parts.append(f'[{i+1}:v]setpts=PTS-STARTPTS[r{i}]');labels.append(f'[r{i}]');cursor=at+dur
parts.append(f'[0:v]trim=start={cursor},setpts=PTS-STARTPTS,fps=30[last]');labels.append('[last]');parts.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=0[v]')
target=m/'base-plans-corriges.mp4';run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex_threads','2','-filter_complex',';'.join(parts),'-map','[v]','-an','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',str(target)])
target.replace(base);save(m/'corrections-plans.json',[dict(debut=at,duree=dur,source=slug,debut_source=start,centre_x=cx) for at,dur,slug,start,cx in replacements]);print('5 passages automobiles recadrés ou remplacés',flush=True)
