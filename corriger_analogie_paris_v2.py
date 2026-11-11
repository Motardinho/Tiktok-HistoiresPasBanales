"""Remplacements locaux de narration, sans décaler les autres passages."""
import copy,math,shutil,json
from pathlib import Path
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save,speech
from revision_hpb_v10 import display_words,NUMBERS
from monter_lot_16_18 import music
from narrateur.assemble import _ass_time
NUMBERS.update({'cent kilotonnes':'100 kilotonnes'})
for n,phrase in [(16,'Une seule ogive pourrait dévaster le cœur de Paris, avec des conséquences bien au-delà.')]:
 w=next((ROOT/'out').glob(f'{n}-*'));root=w/'_montage';m=root/'corrections-locales-v2';m.mkdir(exist_ok=True)
 if (m/'termine.json').exists():continue
 stage=m/'phrase';stage.mkdir(exist_ok=True);save(stage/'histoire.json',dict(scenes=[dict(narration_voix=phrase)]));speech(stage)
 it=read(stage/'_montage/timings-oraux.json');t=read(root/'timings.json');d=read(w/'histoire.json')
 a,b=(d['repere_nucleaire']['debut'],d['repere_nucleaire']['fin']) if n==16 else (9.52,12.267)
 span=b-a;natural=max(it['duration'],it['words'][-1]['end']+.05);ratio=max(1,natural/span)
 assert ratio<1.3,(n,ratio)
 run(['ffmpeg','-v','error','-y','-i',str(stage/'_montage/voix.mp3'),'-af',f'atempo={ratio},apad,atrim=duration={span}',str(m/'phrase.wav')])
 shutil.copy2(root/'voix.mp3',m/'voix-avant.mp3');shutil.copy2(root/'timings.json',m/'timings-avant.json');save(m/'histoire-avant.json',d)
 graph=f'[0:a]atrim=end={a},asetpts=PTS-STARTPTS[a];[1:a]asetpts=PTS-STARTPTS[b];[0:a]atrim=start={b},asetpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=0:a=1[out]'
 run(['ffmpeg','-v','error','-y','-i',str(m/'voix-avant.mp3'),'-i',str(m/'phrase.wav'),'-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')])
 t['words']=[x for x in t['words'] if x['end']<=a+.001 or x['start']>=b-.001]+[dict(w=x['w'],start=a+x['start']/ratio,end=min(b,a+x['end']/ratio)) for x in display_words(it['words'])];t['words'].sort(key=lambda x:x['start'])
 save(m/'timings.json',t);music(w,m,t,n)
 run(['ffmpeg','-v','error','-y','-i',str(m/'mix.wav'),'-c:a','aac','-b:a','192k',str(m/'audio-corrige.m4a')])
 d['correction_locale']=dict(audio=str((m/'audio-corrige.m4a').relative_to(w)),debut=a,fin=b,texte=phrase)
 if n==16:
  old=d['repere_nucleaire']['texte'];d['repere_nucleaire'].update(texte=phrase,source='https://remm.hhs.gov/zones_nucleardetonation.htm',precision='Ordre de grandeur pour une ogive de 100 kt, pas une puissance attribuée à toutes les ogives chinoises. Les effets varient selon les conditions ; aucune région entière annoncée détruite.')
  base=root/'revision-impact-v10/_montage/base.mp4';image=ROOT/'assets/sources-reelles/paris.jpg'
  run(['ffmpeg','-v','error','-y','-loop','1','-i',str(image),'-t',str(span),'-vf',"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.02+0.0004*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p",'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2',str(m/'paris.mp4')])
  graph=f'[0:v]trim=end={a},setpts=PTS-STARTPTS,fps=30[a];[1:v]setpts=PTS-STARTPTS,fps=30[b];[0:v]trim=start={b},setpts=PTS-STARTPTS,fps=30[c];[a][b][c]concat=n=3:v=1:a=0[v]'
  run(['ffmpeg','-v','error','-y','-i',str(base),'-i',str(m/'paris.mp4'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'base.mp4')]);d['correction_locale']['base']=str((m/'base.mp4').relative_to(w))
  ass=root/'sous-titres-ponctuation-liee.ass';s=ass.read_text(encoding='utf-8').replace('HIROSHIMA - 1945','100 KT - REPÈRE : PARIS');ass.write_text(s,encoding='utf-8')
 else:old='Une voiture lancée sur l’autoroute resterait derrière !'
 for sc in d['scenes']:
  for key in ['narration','narration_voix']:
   if key in sc:sc[key]=sc[key].replace(old,phrase)
 d['script']=' '.join(s['narration'] for s in d['scenes']);save(w/'histoire.json',d);(w/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']),encoding='utf-8')
 for name in ['timings.json','voix.mp3']:shutil.copy2(m/name,root/name)
 save(m/'termine.json',dict(debut=a,fin=b,texte=phrase,ratio=ratio));print(n,'phrase et audio corrigés',flush=True)
