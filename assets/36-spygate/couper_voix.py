"""Raccourcit de 0,28 s le silence apres « l'addition » : le hook doit finir avant 5,0 s. Debit inchange."""
import json, shutil, subprocess
from pathlib import Path
m = Path('out/36-mclaren-trahie-par-une-photocopie/_montage'); old = m / 'voix-v1'
if not old.exists():
    old.mkdir(); shutil.copy2(m / 'voix.mp3', old / 'voix.mp3'); shutil.copy2(m / 'timings-oraux.json', old / 'timings-oraux.json')
t = json.loads((old / 'timings-oraux.json').read_text(encoding='utf8'))
a, b = 3.50, 3.78
graph = f'[0:a]atrim=end={a},asetpts=PTS-STARTPTS[x];[0:a]atrim=start={b},asetpts=PTS-STARTPTS[y];[x][y]concat=n=2:v=0:a=1[out]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(old / 'voix.mp3'), '-filter_complex', graph, '-map', '[out]', '-c:a', 'libmp3lame', '-b:a', '192k', str(m / 'voix.mp3')], check=True)
f = lambda x: round(x - (b - a), 5) if x >= b else x
words = [dict(w=w['w'], start=f(w['start']), end=f(w['end'])) for w in t['words']]
duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(m / 'voix.mp3')]))
starts = [f(sum(t['scene_durations'][:i])) for i in range(len(t['scene_durations']))]
t.update(words=words, duration=duration, scene_durations=[y - x for x, y in zip(starts, starts[1:] + [duration])],
         montage_audio=dict(coupes=[[a, b]], raison='Silence raccourci apres « l addition » pour finir le hook avant 5,0 s ; prise ElevenLabs conservee.'))
(m / 'timings-oraux.json').write_text(json.dumps(t, ensure_ascii=False, indent=2), encoding='utf8')
print(duration, [w for w in words if w['w'] == 'dollars.'][0])
