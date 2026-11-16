"""Voix ElevenLabs du dossier 52 : lit narration_voix de histoire.json, écrit voix.mp3 et timings.json."""
import base64
import json
import sys
from pathlib import Path

import requests
import yaml

work = Path(__file__).resolve().parent
root = work.parent.parent
sys.path.insert(0, str(root))
from narrateur.voice import _api_key

config = yaml.safe_load((root / 'config.yaml').read_text(encoding='utf-8'))['voice']
histoire = json.loads((work / 'histoire.json').read_text(encoding='utf-8'))
spoken = ' '.join(' '.join(s['narration_voix'] for s in histoire['scenes']).split())
(work / 'histoire.txt').write_text(
    '\n\n'.join(s['narration'] for s in histoire['scenes']) + '\n', encoding='utf-8')
(work / 'voix.txt').write_text(spoken + '\n', encoding='utf-8')

response = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{config['voice_id']}/with-timestamps",
    params={'output_format': config['output_format']},
    headers={'xi-api-key': _api_key()},
    json={'text': spoken, 'model_id': config['model_id'], 'seed': 16112026,
          'voice_settings': {'stability': config['stability'], 'similarity_boost': 0.75}},
    timeout=180,
)
if not response.ok:
    print(response.status_code, response.text[:500])
response.raise_for_status()
data = response.json()
assert ''.join(data['alignment']['characters']) == spoken
(work / 'voix.mp3').write_bytes(base64.b64decode(data['audio_base64']))
(work / 'timings.json').write_text(json.dumps(data['alignment'], ensure_ascii=False), encoding='utf-8')
fin = data['alignment']['character_end_times_seconds'][-1]
print(f'{len(spoken.split())} mots, fin de voix à {fin:.2f} s')
