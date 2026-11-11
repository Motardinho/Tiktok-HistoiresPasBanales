"""Trois vidéos russes entrent à chaque nom d’équipement, sur une seule phrase."""
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
w=next((ROOT/'out').glob('16-*'));root=w/'_montage';m=root/'triptyque-equipements';m.mkdir(exist_ok=True);d=read(w/'histoire.json');base=w/d['correction_locale']['base'];a=52.4;b=57.2;span=b-a
if base.resolve()==(m/'base.mp4').resolve():base=root/'corrections-locales-v3'/'base.mp4'
inputs=['-ss',str(a),'-i',str(base),'-ss','4','-i',str(ROOT/'assets/lot-16-18/russia-t90.mp4'),'-ss','8.5','-i',str(ROOT/'assets/lot-16-18/russia-air.webm'),'-ss','35.9','-i',str(ROOT/'assets/lot-16-18/russia-su35.mp4')]
starts=[52.5933333333-a,53.2333333333-a,54.3533333333-a]
def slide(start,direction):
 p=f'max(0,min(1,(t-{start})/0.24))';return f'{direction}*1080*pow(1-{p},3)'
g=("[0:v]fps=30,setsar=1[base];[1:v]scale=1138:640,crop=1080:640:(iw-ow)/2:0,fps=30,setsar=1[tk];"
"[2:v]scale=1080:-2,crop=1080:360:0:(ih-oh)/2,fps=30,setsar=1[he];"
"[3:v]scale=1080:-2,split[j1][j2];[j1]crop=400:80:340:0,scale=1080:920[bg];[j2]crop=1080:400:0:100[fg];[bg][fg]overlay=0:0,fps=30,setsar=1[je];"
+f"[base][tk]overlay=x='{slide(starts[0],1)}':y=0:enable='gte(t,{starts[0]})'[v1];"
+f"[v1][he]overlay=x='{slide(starts[1],-1)}':y=640:enable='gte(t,{starts[1]})'[v2];"
+f"[v2][je]overlay=x='{slide(starts[2],1)}':y=1000:enable='gte(t,{starts[2]})'[v]")
run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-t',str(span),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'sequence.mp4')])
g=f'[0:v]trim=end={a},setpts=PTS-STARTPTS,fps=30,setsar=1[a];[1:v]setpts=PTS-STARTPTS,fps=30,setsar=1[b];[0:v]trim=start={b},setpts=PTS-STARTPTS,fps=30,setsar=1[c];[a][b][c]concat=n=3:v=1:a=0[v]'
run(['ffmpeg','-v','error','-y','-i',str(base),'-i',str(m/'sequence.mp4'),'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'base.mp4')])
d['correction_locale']['base']=str((m/'base.mp4').relative_to(w));d['triptyque_equipements']=dict(debut=a,fin=b,entrees=[dict(mot=x,debut=a+s) for x,s in zip(['blindés','hélicoptères','avions de combat'],starts)],zones=[[0,0,1080,640],[0,640,1080,1000],[0,1000,1080,1920]],sous_titres_mots_separes=True)
save(w/'histoire.json',d);save(m/'montage.json',d['triptyque_equipements']);print('16 triptyque glissant synchronisé prêt',flush=True)
