from production import *
from narrateur.assemble import _ass_time
from PIL import ImageFont
import shutil
v=WORK/'v5';old=WORK/'v4';cut=2.9
words=json.loads((v/'hook-timings.json').read_text(encoding='utf8'))['words'];rate=3.6/cut
for w in words:w['start']/=rate;w['end']=min(cut,w['end']/rate)
font=ImageFont.truetype(str(ROOT/'assets/fonts/Poppins-ExtraBold.ttf'),92)
groups=[words[:3],words[3:7],words[7:]];events=[];srt=[]
def st(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
for gi,g in enumerate(groups):
 end=groups[gi+1][0]['start'] if gi+1<len(groups) else 3.081
 assert font.getlength(' '.join(w['w'] for w in g))<=1600
 for j,w in enumerate(g):
  stop=g[j+1]['start'] if j+1<len(g) else end
  txt=' '.join((r'{\c&H47E4FF&}'+x['w']+r'{\c&HFFFFFF&}') if j==k else x['w'] for k,x in enumerate(g))
  events.append(f'Dialogue: 0,{_ass_time(w["start"])},{_ass_time(stop)},Default,,0,0,0,,{txt}')
 srt.append(f'{gi+1}\n{st(g[0]["start"])} --> {st(end)}\n'+ ' '.join(w['w'] for w in g))
a=(old/'sous-titres.ass').read_text(encoding='utf8');header=a.split('Dialogue:')[0];rest=a[a.index('Dialogue: 0,0:00:03.08,'):]
(v/'sous-titres.ass').write_text(header+'\n'.join(events)+'\n'+rest,encoding='utf8')
blocks=(OUT/'sous-titres-v4.srt').read_text(encoding='utf8').strip().split('\n\n')[2:]
for b in blocks:
 lines=b.splitlines();lines[0]=str(int(lines[0])+1);srt.append('\n'.join(lines))
(OUT/'sous-titres-v5.srt').write_text('\n\n'.join(srt)+'\n',encoding='utf8')
for name in ['script','script-ssc']:
 (OUT/f'{name}-v5.txt').write_text((OUT/f'{name}-v4.txt').read_text(encoding='utf8').replace('À cette vitesse, une ligne droite devient trop courte.',"À cette vitesse, n'importe quelle ligne droite devient trop courte.",1),encoding='utf8')
for name in ['description-youtube','legende','publication']:shutil.copy2(OUT/f'{name}-v4.txt',OUT/f'{name}-v5.txt')
shutil.copy2(OUT/'CREDITS-v4.md',OUT/'CREDITS-v5.md')
run(['ffmpeg','-y','-v','error','-i',v/'hook.mp3','-i',ROOT/'assets/musique/mixkit/voitures.mp3','-i',OUT/'essai-long-v4.mp4','-filter_complex',f'[0:a]atempo={rate},apad,atrim=duration={cut},highpass=f=65,loudnorm=I=-16:TP=-1.5:LRA=8,aresample=48000[a];[1:a]atrim=duration={cut},volume=0.025,afade=t=in:d=0.3,aresample=48000[m];[a][m]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=2.88:d=0.02[h];[2:a]atrim=start={cut},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[t];[h][t]concat=n=2:v=0:a=1[out]','-map','[out]','-t','482','-ar','48000','-ac','2','-c:a','pcm_s16le',v/'mix.wav'])
writej(v/'correction.json',{'phrase':"À cette vitesse, n’importe quelle ligne droite devient trop courte.",'raccord_secondes':cut,'silence_v4_observe':[2.582479,3.020708],'tempo_hook':rate,'suite_voix':'mix V4 conservé après 2,92 s','images':'montage V4 inchangé','ecoute_effectuee':False})
subprocess.run(['ffmpeg','-y','-v','error','-threads','4','-i',str(old/'muet.mp4'),'-i','mix.wav','-i',str(WORK/'logo.png'),'-filter_complex_threads','2','-filter_complex',"[0:v]ass=sous-titres.ass:fontsdir='../../../../assets/fonts'[s];[s][2:v]overlay=0:0[v]",'-map','[v]','-map','1:a','-t','482','-c:v','libx264','-preset','fast','-crf','19','-threads','4','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'essai-long-v5.mp4')],cwd=v,check=True)
print('V5 exportée',flush=True)
