"""Retire la précision de protocole automobile sans changer le montage approuvé."""
import json,hashlib,shutil
from montage_reel import ROOT,run
from alleger_ouvertures_top import seconds
from narrateur.assemble import _ass_time
from comparer_lot_16_18 import compare

w=next((ROOT/'out').glob('14-*'));m=w/'_montage';a=m/'avant-retrait-mention-pointes';a.mkdir(exist_ok=True)
for name in ['final.mp4','comparaison.mp4','histoire.json']:
    if not (a/name).exists():shutil.copy2(w/name,a/name)
p=m/'sous-titres-reference.ass';text=p.read_text(encoding='utf-8');header=[];events=[]
for line in text.splitlines():
    if 'POINTES EN UN SEUL SENS' in line:continue
    if not line.startswith('Dialogue:'):header.append(line);continue
    v=line.split(',',9)
    if seconds(v[2])<=4:continue
    if seconds(v[1])<4:v[1]=_ass_time(4)
    events.append(','.join(v))
events=[x for x in (m/'ouverture-allegee.ass').read_text(encoding='utf-8').splitlines() if x.startswith('Dialogue:') and 'POINTES EN UN SEUL SENS' not in x]+events
(m/'voitures-sans-mention-pointes.ass').write_text('\n'.join(header+events)+'\n',encoding='utf-8')
p.write_text('\n'.join(x for x in text.splitlines() if 'POINTES EN UN SEUL SENS' not in x)+'\n',encoding='utf-8')
graph=('[0:v]trim=end=4,setpts=PTS-STARTPTS,fps=30[a];[1:v]trim=start=4,setpts=PTS-STARTPTS,fps=30[b];'
       '[a][b]concat=n=2:v=1:a=0,ass=voitures-sans-mention-pointes.ass:fontsdir=.[s];'
       '[s][3:v]overlay=0:0:enable=lt(t\\,1.5):shortest=1[t];[t][4:v]overlay=0:0:shortest=1[h];'
       '[h][5:v]overlay=0:0:enable=between(t\\,42.68\\,47.60):shortest=1[v]')
target=m/'final-sans-mention-pointes.mp4'
duration=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(a/'final.mp4')]))['format']['duration'])
run(['ffmpeg','-v','error','-y','-i','intro-ssc-kmh-original.mp4','-i','base-hpb-v13.mp4','-i',str(a/'final.mp4'),'-loop','1','-framerate','30','-i','titre-hook-reference.png','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','funfact-visible.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','2:a:0','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
run(['ffmpeg','-v','error','-i',str(target),'-f','null','-']);target.replace(w/'final.mp4');compare(w)
story=json.loads((w/'histoire.json').read_text(encoding='utf-8'));story['mention_protocole_ecran']=False;(w/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
p=m/'controle-funfact-visible.json';d=json.loads(p.read_text(encoding='utf-8'));d['sha256']=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest();p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('14 : mention retirée, comparaison actualisée')
