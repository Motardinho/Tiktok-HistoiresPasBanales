"""Retire l'amorce résiduelle de l'ancienne prise juste avant « Numéro un » (48,02-48,14 s)."""
import shutil, wave
from pathlib import Path
import numpy as np
from montage_reel import ROOT, run
from narrateur.musique import mix_voice

m = next((ROOT / 'out').glob('14-*')) / '_montage'
r = m / 'raccord-yangwang'
for name in ('voix.wav', 'mix.wav', 'audio-corrige.m4a'):
    backup = r / ('avant-correction-n1-' + name)
    if not backup.exists():
        shutil.copy2(r / name, backup)
with wave.open(str(r / 'avant-correction-n1-voix.wav')) as f:
    params = f.getparams(); x = np.frombuffer(f.readframes(f.getnframes()), dtype='<i2').copy()
sr = params.framerate
a, b = round(48.015 * sr), round(48.138 * sr)
x[a:b] = 0
with wave.open(str(r / 'voix.wav'), 'wb') as f:
    f.setparams(params); f.writeframes(x.tobytes())
duration = len(x) / sr
mix_voice(r / 'voix.wav', m / 'musique-hpb-v13.wav', r / 'mix.wav', duration, run)
run(['ffmpeg', '-v', 'error', '-y', '-i', str(r / 'mix.wav'), '-t', '81.58', '-c:a', 'aac', '-b:a', '204k', str(r / 'audio-corrige.m4a')])
print('voix corrigée', a / sr, b / sr)
