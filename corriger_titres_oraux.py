"""Titre prononcé avant le classement ; seuls les débuts de voix sont remplacés."""
import copy,shutil,re
from pathlib import Path
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
from revision_hpb_v10 import display_words
from monter_lot_16_18 import music
for n,span in [(13,2.107),(14,4.8),(18,4.007)]:
 w=next((ROOT/'out').glob(f'{n}-*'));root=w/'_montage';m=root/'ouverture-titre-puis-rang';m.mkdir(exist_ok=True)
 if (m/'termine.json').exists():continue
 it=read(m/'phrase/_montage/timings-oraux.json');t=read(root/'timings.json');d=read(w/'histoire.json');voice=m/'phrase/_montage/voix.mp3';natural=max(it['duration'],it['words'][-1]['end']+.05);ratio=max(1,natural/span);assert ratio<1.3
 if not (m/'voix-avant.mp3').exists():
  shutil.copy2(root/'voix.mp3',m/'voix-avant.mp3');save(m/'histoire-avant.json',d);save(m/'timings-avant.json',t)
 t=read(m/'timings-avant.json');d=read(m/'histoire-avant.json')
 run(['ffmpeg','-v','error','-y','-i',str(voice),'-af',f'atempo={ratio},apad,atrim=duration={span}',str(m/'phrase.wav')])
 graph=f'[0:a]asetpts=PTS-STARTPTS[a];[1:a]atrim=start={span},asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1[out]'
 run(['ffmpeg','-v','error','-y','-i',str(m/'phrase.wav'),'-i',str(m/'voix-avant.mp3'),'-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')])
 t['words']=[dict(w=x['w'],start=x['start']/ratio,end=x['end']/ratio) for x in display_words(it['words'])]+[x for x in t['words'] if x['start']>=span-.005]
 words=it['words'];intro=next((x['start']/ratio for x in words if x['w'].lower()=='numéro'),span)
 if n==18:
  delta=intro-t['scene_durations'][0];t['scene_durations'][0]=intro;t['scene_durations'][1]-=delta
 save(m/'timings.json',t);music(w,m,t,{13:16,14:17,18:18}[n]);run(['ffmpeg','-v','error','-y','-i',str(m/'mix.wav'),'-c:a','aac','-b:a','192k',str(m/'audio-corrige.m4a')])
 phrase=' '.join(s['narration_voix'] for s in read(m/'phrase/histoire.json')['scenes'])
 if n==13:
  for key in ['narration','narration_voix']:d['scenes'][0][key]=re.sub(r'^C[’\x27]est la pesée en apesanteur\s*:',phrase,d['scenes'][0][key])
 elif n==14:
  for key in ['narration','narration_voix']:
   s=d['scenes'][0][key];d['scenes'][0][key]=phrase+' '+s.split('Tuatara.',1)[1].strip()
 else:
  for key in ['narration','narration_voix']:
   d['scenes'][0][key]='Top trois des plus grands pays du monde.';d['scenes'][1][key]=re.sub(r'^(?:Numéro (?:trois|3)|N°3) des plus grands pays du monde\s*:', 'Numéro trois :',d['scenes'][1][key],flags=re.I)
 d.setdefault('correction_locale',{}).update(audio=str((m/'audio-corrige.m4a').relative_to(w)),fin_annonce_titre=intro)
 d['hook']=d['scenes'][0]['narration'];d['script']=' '.join(s['narration'] for s in d['scenes']);save(w/'histoire.json',d);(w/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']),encoding='utf-8')
 for file in ['timings.json','voix.mp3']:shutil.copy2(m/file,root/file)
 old=read(root/'timings-oraux.json') if (root/'timings-oraux.json').exists() else copy.deepcopy(t);old.update(words=t['words'],duration=t['duration'],scene_durations=t['scene_durations']);save(root/'timings-oraux.json',old)
 save(m/'termine.json',dict(texte=phrase,titre_termine=intro,ratio=ratio,fin_remplacement=span));print(n,'titre à l’oral corrigé',flush=True)
