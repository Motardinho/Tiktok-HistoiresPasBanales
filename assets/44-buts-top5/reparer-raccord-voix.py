"""Reconstruit le raccord depuis la source, sans amorce de la phrase supprimée."""
import json
import shutil
import subprocess
from pathlib import Path

p = Path('out/44-top-5-buts-les-plus-degueulasses')
m = p / '_montage'
b = m / 'avant-raccord-v8'
b.mkdir(exist_ok=True)
for f in [p/'final.mp4', p/'histoire.json', m/'voix.mp3', m/'timings-oraux.json']:
    if not (b/f.name).exists(): shutil.copy2(f,b/f.name)
source = m/'avant-finition-2026-11-13/voix.mp3'
# Source : silence observé à 27,311–27,552 ; reprise suivante vers 29,531.
# L'ancien mute à 27,700 conservait le début audible de « Son ».
cut, resume, begin = 27.43, 29.50, 17.28
target = 10.82
tempo = (cut-begin)/target
graph = (f'[0:a]asplit=3[a][b][c];'
         f'[a]atrim=start=6.8:end={begin},asetpts=PTS-STARTPTS[a0];'
         f'[b]atrim=start={begin}:end={cut},asetpts=PTS-STARTPTS,atempo={tempo},'
         f'apad,atrim=duration={target},afade=t=out:st={target-.008}:d=0.008[a1];'
         f'[c]atrim=start={resume},asetpts=PTS-STARTPTS,afade=t=in:d=0.008[a2];'
         '[a0][a1][a2]concat=n=3:v=0:a=1[out]')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-filter_complex',graph,
                '-map','[out]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')],check=True)
t = json.loads((b/'timings-oraux.json').read_text(encoding='utf8'))
for word in t['words']:
    if 10.48 <= word['start'] < 21.3:
        for key in ['start','end']:
            word[key] = round(min(21.3,10.48+(word[key]-10.48)/tempo),6)
t['raccord_v8'] = dict(source=str(source), coupe_source=[cut,resume], atempo_chicharito=tempo,
                       note='Source non mutée ; fin de rentre conservée, amorce de Son retirée ; n°3 et suite inchangés.')
(m/'timings-oraux.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
d=json.loads((b/'histoire.json').read_text(encoding='utf8'))
d['raccord_audio_v8']=t['raccord_v8']
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('Raccord reconstruit, tempo',tempo)
