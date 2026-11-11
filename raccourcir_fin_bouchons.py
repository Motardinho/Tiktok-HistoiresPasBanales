"""Fin directe demandée : CTA puis signature existante, sans le paragraphe Selon l'heure."""
import sys,math,shutil,copy
sys.stdout.reconfigure(encoding='utf-8')
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save,speech
from monter_lot_16_18 import music
w=next((ROOT/'out').glob('15-*'));r=w/'_montage';m=r/'fin-directe-commentaire';m.mkdir(exist_ok=True)
if (m/'termine.json').exists():sys.exit(0)
p=m/'phrase';p.mkdir(exist_ok=True)
phrase='Raconte ta pire expérience de bouchon en commentaire.'
save(p/'histoire.json',dict(scenes=[dict(narration_voix=phrase)]));speech(p)
it=read(p/'_montage/timings-oraux.json');d=read(w/'histoire.json');t=read(r/'timings.json');save(m/'histoire-avant.json',d);save(m/'timings-avant.json',t)
for name in ['final.mp4','comparaison.mp4','publication.txt','legende.txt']:shutil.copy2(w/name,m/('avant-'+name))
shutil.copy2(r/'voix.mp3',m/'voix-avant.mp3')
cut=61.4;sig=75.64;ctadur=math.ceil(max(it['duration'],it['words'][-1]['end']+.08)*30)/30
tail=t['duration']-sig;duration=math.ceil((cut+ctadur+tail+.4)*30)/30
g=(f'[0:a]atrim=end={cut},asetpts=PTS-STARTPTS[x];'
 f'[1:a]apad,atrim=duration={ctadur},asetpts=PTS-STARTPTS[y];'
 f'[0:a]atrim=start={sig},asetpts=PTS-STARTPTS,apad,atrim=duration={duration-cut-ctadur}[z];'
 '[x][y][z]concat=n=3:v=0:a=1[o]')
run(['ffmpeg','-v','error','-y','-i',str(m/'voix-avant.mp3'),'-i',str(p/'_montage/voix.mp3'),'-filter_complex',g,'-map','[o]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')])
t['words']=[x for x in t['words'] if x['start']<cut]+[dict(w=x['w'],start=cut+x['start'],end=cut+x['end']) for x in it['words']]+[dict(w=x['w'],start=cut+ctadur+x['start']-sig,end=cut+ctadur+x['end']-sig) for x in t['words'] if x['start']>=sig]
t['duration']=duration;t['scene_durations'][-2]=cut-sum(t['scene_durations'][:-2]);t['scene_durations'][-1]=duration-cut
save(m/'timings.json',t);music(w,m,t,18)
run(['ffmpeg','-v','error','-y','-i',str(m/'mix.wav'),'-c:a','aac','-b:a','192k',str(m/'audio-corrige.m4a')])
for key in ['narration','narration_voix']:
 d['scenes'][-2][key]=d['scenes'][-2][key].split('Selon l’heure')[0].strip()
 d['scenes'][-1][key]=phrase+' Pas banal, hein ?'
d['script']=' '.join(s['narration'] for s in d['scenes']);d.setdefault('correction_locale',{})['audio']=str((m/'audio-corrige.m4a').relative_to(w))
d['revision_fin']=dict(coupe=cut,cta=phrase,signature_existante_conservee=True,duree=duration)
save(w/'histoire.json',d);(w/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']),encoding='utf-8')
for name in ['timings.json','voix.mp3']:shutil.copy2(m/name,r/name)
old=read(r/'timings-oraux.json');old.update(words=t['words'],duration=duration,scene_durations=t['scene_durations']);save(r/'timings-oraux.json',old)
save(m/'termine.json',d['revision_fin']);print('Fin raccourcie prête :',duration,'s',flush=True)
