"""Ne montrer TERRES + EAUX qu'au passage où cette précision est racontée."""
import json,hashlib,shutil
from montage_reel import ROOT,run
from alleger_ouvertures_top import seconds
from narrateur.assemble import _ass_time
from comparer_lot_16_18 import compare

w=next((ROOT/'out').glob('18-*'));m=w/'_montage';src=m/'revision-spectaculaire-v5/_montage';archive=m/'avant-mention-superficie-breve';archive.mkdir(exist_ok=True)
for name in ['final.mp4','comparaison.mp4','histoire.json']:
    if not (archive/name).exists():shutil.copy2(w/name,archive/name)
text=(src/'sous-titres-reference.ass').read_text(encoding='utf-8');header=[];events=[]
for line in text.splitlines():
    if not line.startswith('Dialogue:'):header.append(line);continue
    if 'TERRES + EAUX' in line:continue
    p=line.split(',',9)
    if seconds(p[2])<=4:continue
    if seconds(p[1])<4:p[1]=_ass_time(4)
    events.append(','.join(p))
events=[x for x in (m/'ouverture-allegee.ass').read_text(encoding='utf-8').splitlines() if x.startswith('Dialogue:')]+events
events.append(r'Dialogue: 1,0:00:08.18,0:00:11.18,Fact,,0,0,0,,{\an8\pos(540,350)\fs52}TERRES + EAUX')
(m/'superficie-mention-breve.ass').write_text('\n'.join(header+events)+'\n',encoding='utf-8')
graph=('[0:v]fps=30,setpts=PTS-STARTPTS,ass=superficie-mention-breve.ass:fontsdir=.[s];'
       '[s][2:v]overlay=0:0:enable=lt(t\\,1.5):shortest=1[t];[t][3:v]overlay=0:0:shortest=1[h];'
       '[h][4:v]overlay=0:0:enable=between(t\\,30.2\\,38.8):shortest=1[v]')
target=m/'final-superficie-mention-breve.mp4'
run(['ffmpeg','-v','error','-y','-i',str(src/'base.mp4'),'-i',str(archive/'final.mp4'),'-loop','1','-framerate','30','-i','titre-hook-reference.png','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','funfact-visible.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t','79.34','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
run(['ffmpeg','-v','error','-i',str(target),'-f','null','-']);target.replace(w/'final.mp4');compare(w)
d=json.loads((w/'histoire.json').read_text(encoding='utf-8'));d['mention_superficie']={'texte':'TERRES + EAUX','debut':8.18,'fin':11.18,'permanente':False};(w/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=m/'controle-funfact-visible.json';d=json.loads(p.read_text(encoding='utf-8'));d['sha256']=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest();p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('18 : mention limitée à 3 secondes, comparaison actualisée')
