import base64
import json
import subprocess
import sys
from pathlib import Path

import requests
import yaml

work = Path(__file__).resolve().parent
root = work.parent.parent
sys.path.insert(0, str(root))
from narrateur.voice import _api_key

config = yaml.safe_load((root / 'config.yaml').read_text(encoding='utf-8'))['voice']
script = (work / 'histoire.txt').read_text(encoding='utf-8').strip()
script = ' '.join(script.split())
spoken = script.replace('Rice', 'Raïs').replace('Faye Yap', 'Faïe Yap')
tail_only = '--chute' in sys.argv
if tail_only:
    old = json.loads((work / 'timings.json').read_text(encoding='utf-8'))
    split = spoken.index('Un an plus tard')
    assert ''.join(old['characters'][:split]) == spoken[:split]
    cut = old['character_start_times_seconds'][split]
    spoken = spoken[split:]
response = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{config['voice_id']}/with-timestamps",
    params={'output_format': config['output_format']},
    headers={'xi-api-key': _api_key()},
    json={'text': spoken, 'model_id': config['model_id'], 'seed': 7112026,
          'voice_settings': {'stability': config['stability'], 'similarity_boost': 0.75}},
    timeout=120,
)
if not response.ok:
    print(response.status_code, response.json().get('detail', {}))
response.raise_for_status()
data = response.json()
if tail_only:
    updated = data['alignment']
    assert ''.join(updated['characters']) == spoken
    (work / 'voix-chute.mp3').write_bytes(base64.b64decode(data['audio_base64']))
    # Le début audible de la phrase peut précéder le repère fourni par ElevenLabs.
    # Couper dans la pause, puis combler jusqu'au départ prévu de la nouvelle prise.
    quiet_cut = cut - 0.24
    prefix = (f'[0:a]atrim=end={quiet_cut},afade=t=out:st={quiet_cut - 0.02}:d=0.02,'
              f'apad=whole_dur={cut},atrim=end={cut},asetpts=PTS-STARTPTS[p]')
    subprocess.run(
        ['ffmpeg', '-y', '-v', 'error', '-i', 'voix.mp3', '-i', 'voix-chute.mp3',
         '-filter_complex', f'{prefix};[p][1:a]concat=n=2:v=0:a=1',
         '-c:a', 'libmp3lame', '-b:a', '192k', 'voix-revisee.mp3'],
        cwd=work, check=True,
    )
    for key, values in updated.items():
        old[key] = old[key][:split] + (values if key == 'characters' else [cut + value for value in values])
    (work / 'voix-revisee.mp3').replace(work / 'voix.mp3')
    data['alignment'] = old
else:
    (work / 'voix.mp3').write_bytes(base64.b64decode(data['audio_base64']))
(work / 'timings.json').write_text(json.dumps(data['alignment'], ensure_ascii=False), encoding='utf-8')
