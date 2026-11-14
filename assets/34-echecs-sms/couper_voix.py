import json, subprocess
from pathlib import Path
m=Path('out/34-il-trichait-aux-echecs/_montage'); old=m/'voix-v1'
t=json.loads((old/'timings-oraux.json').read_text(encoding='utf8'))
# Coupes dans les silences entre les phrases, sans modifier le débit.
cuts=[(12.06,13.98),(34.12,36.34)]
spans=[(0,cuts[0][0]),(cuts[0][1],cuts[1][0]),(cuts[1][1],t['duration'])]
graph=';'.join(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]' for i,(a,b) in enumerate(spans))+';' + ''.join(f'[a{i}]' for i in range(len(spans)))+'concat=n=3:v=0:a=1[out]'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(old/'voix.mp3'),'-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')],check=True)
def mapped(x):return round(x-sum(b-a for a,b in cuts if x>=b),5)
words=[dict(w=w['w'],start=mapped(w['start']),end=mapped(w['end'])) for w in t['words'] if not any(a<=w['start']<b for a,b in cuts)]
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(m/'voix.mp3')]))
old_starts=[sum(t['scene_durations'][:i]) for i in range(len(t['scene_durations']))];starts=[mapped(x) for x in old_starts]
t.update(words=words,duration=duration,scene_durations=[b-a for a,b in zip(starts,starts[1:]+[duration])],montage_audio=dict(coupes=cuts,raison='Deux phrases de transition retirées ; quota TTS insuffisant pour une deuxième synthèse. Prise ElevenLabs originale conservée.'))
(m/'timings-oraux.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
print(duration,starts)
