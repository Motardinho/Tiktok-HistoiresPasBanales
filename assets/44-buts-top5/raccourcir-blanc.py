"""Retire 1,4 s du blanc de narration laissé après Chicharito."""
import json
import shutil
import subprocess
from pathlib import Path

p = Path('out/44-top-5-buts-les-plus-degueulasses')
m = p / '_montage'
b = m / 'avant-correction-blanc'
b.mkdir(exist_ok=True)
for f in [p/'histoire.json', p/'final.mp4', m/'voix.mp3', m/'timings-oraux.json', m/'plans.json', m/'montage.json', m/'base.mp4']:
    if not (b/f.name).exists(): shutil.copy2(f,b/f.name)
read = lambda f: json.loads(f.read_text(encoding='utf8'))
write = lambda f,d: f.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
start, end = 21.05, 22.45
delta = round(end-start,3)
def shift(t):
    return round(t-delta,6) if t>=end else t
t = read(b/'timings-oraux.json')
assert not any(w['start']<end and w['end']>start for w in t['words']), 'La coupe toucherait une parole'
t['duration'] = round(t['duration']-delta,3)
t['scene_durations'][1] = round(t['scene_durations'][1]-delta,3)
for w in t['words']:
    for k in ['start','end']: w[k]=shift(w[k])
write(m/'timings-oraux.json',t)
d = read(b/'histoire.json')
d['coupe_blanc'] = {'debut_avant':start,'fin_avant':end,'duree_retiree':delta}
for k in ['debut','fin']: d['fun_fact_affichage'][k]=shift(d['fun_fact_affichage'][k])
d['volets_jaunes'] = [shift(x) for x in d['volets_jaunes']]
d['choix_editoriaux'].append('Blanc après Chicharito raccourci de 1,4 s après retour de Marc : coupe 21,05–22,45 s dans la célébration, aucun mot ni geste du but supprimé. Pause résiduelle environ 0,6 s.')
write(p/'histoire.json',d)
plans=read(b/'plans.json')
for row in plans:
    if row['fin'] is not None: row['fin']=shift(row['fin'])
write(m/'plans.json',plans)
rows=read(b/'montage.json')
for row in rows:
    for k in ['debut','fin']: row[k]=shift(row[k])
write(m/'montage.json',rows)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(b/'voix.mp3'),'-filter_complex',f'[0:a]asplit[a][b];[a]atrim=end={start},asetpts=PTS-STARTPTS[a0];[b]atrim=start={end},asetpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=0:a=1[out]','-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')],check=True)
# Coupe sur les images entières : 21,0667 à 22,4667 s = 42 images.
subprocess.run(['ffmpeg','-v','error','-y','-i',str(b/'base.mp4'),'-filter_complex','[0:v]split[a][b];[a]trim=end_frame=632,setpts=PTS-STARTPTS[a0];[b]trim=start_frame=674,setpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=1:a=0[out]','-map','[out]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(m/'base.mp4')],check=True)
print('Blanc raccourci, durée narration',t['duration'],flush=True)
