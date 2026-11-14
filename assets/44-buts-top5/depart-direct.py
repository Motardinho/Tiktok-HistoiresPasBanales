"""Supprime les 6,8 s d'introduction et recale toutes les données du montage."""
import json
import shutil
import subprocess
from pathlib import Path

p = Path('out/44-top-5-buts-les-plus-degueulasses')
m = p / '_montage'
b = m / 'avant-depart-direct'
b.mkdir(exist_ok=True)
for f in [p/'histoire.json', p/'final.mp4', m/'voix.mp3', m/'timings-oraux.json', m/'plans.json', m/'montage.json', m/'base.mp4']:
    if not (b/f.name).exists():
        shutil.copy2(f, b/f.name)
read = lambda f: json.loads(f.read_text(encoding='utf8'))
write = lambda f,d: f.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
d = read(b/'histoire.json')
t = read(b/'timings-oraux.json')
cut = t['scene_durations'][0]
assert abs(cut - 6.8) < .001
d['scenes'] = d['scenes'][1:]
d['hook'] = d['scenes'][0]['narration']
d['depart_direct_classement'] = True
d['bandeaux_debut_min'] = 0
d['fin_annonce_titre'] = 0
d['fin_annonce_titre_mesuree'] = 0
d['intro_supprimee_secondes'] = cut
for tag in d['bandeaux']:
    tag['scene'] -= 1
d['fun_fact']['scene'] -= 1
for key in ['debut', 'fin']:
    d['fun_fact_affichage'][key] = round(d['fun_fact_affichage'][key]-cut,3)
d['volets_jaunes'] = [round(x-cut,3) for x in d['volets_jaunes'] if x>cut+.1]
d['choix_editoriaux'].append('13 novembre 2026 : démarrage direct sur Numéro 5 demandé par Marc. Introduction orale et trois plans génériques supprimés (6,8 s) ; aucun volet à 0:00.')
t['duration'] = round(t['duration']-cut,3)
t['scene_durations'] = t['scene_durations'][1:]
t['words'] = [dict(w, start=round(w['start']-cut,3), end=round(w['end']-cut,3)) for w in t['words'] if w['start']>=cut-.001]
write(p/'histoire.json',d)
write(m/'timings-oraux.json',t)
(p/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes'])+'\n',encoding='utf8')
plans = read(b/'plans.json')[3:]
for row in plans:
    if row['fin'] is not None: row['fin'] = round(row['fin']-cut,3)
write(m/'plans.json', plans)
rows = read(b/'montage.json')[3:]
for row in rows:
    for key in ['debut','fin']: row[key] = round(row[key]-cut,6)
write(m/'montage.json', rows)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(b/'voix.mp3'),'-af',f'atrim=start={cut},asetpts=PTS-STARTPTS','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(cut),'-i',str(b/'base.mp4'),'-an','-c:v','libx264','-preset','veryfast','-crf','18',str(m/'base.mp4')],check=True)
print('Départ direct prêt :',t['duration'],'s',t['words'][:2],flush=True)
