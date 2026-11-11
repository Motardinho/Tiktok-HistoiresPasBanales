"""Voix du gag Nokia (angélique + troll) avec timings ElevenLabs. Idempotent."""
import sys, json, base64, requests
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from narrateur.voice import _api_key
D = ROOT/'assets/refonte-14-20/telephone/troll'
JOBS = {
 'ange-eva': ('D6VK2PsbVdaFL5aALfRc', "Numéro un… le légendaire… Nokia trente-trois dix.", 0.45),
 'ange-victoria': ('WeAAwKYcS06VmXw086yZ', "Numéro un… le légendaire… Nokia trente-trois dix.", 0.45),
 'troll-callum': ('N2lVS1w4EtoT3dr4eOWO', "Hé hé hé hé ! T'as cru ?", 0.3),
 'troll-laura': ('FGY2WhTYpPnrIDTdsKH5', "Hé hé hé hé ! T'as cru ?", 0.3),
}
for nom, (vid, txt, stab) in JOBS.items():
    f = D/f'{nom}.mp3'
    if f.exists(): continue
    r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps',
        headers={'xi-api-key': _api_key()}, params={'output_format': 'mp3_44100_128'}, timeout=120,
        json={'text': txt, 'model_id': 'eleven_v4', 'seed': 3310, 'language_code': 'fr',
              'voice_settings': {'stability': stab, 'similarity_boost': 0.75}})
    if r.status_code != 200:
        r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps',
            headers={'xi-api-key': _api_key()}, params={'output_format': 'mp3_44100_128'}, timeout=120,
            json={'text': txt, 'model_id': 'eleven_v4', 'seed': 3310,
                  'voice_settings': {'stability': stab, 'similarity_boost': 0.75}})
    r.raise_for_status(); d = r.json()
    f.write_bytes(base64.b64decode(d['audio_base64']))
    al = d.get('alignment')
    (D/f'{nom}.json').write_text(json.dumps(al, ensure_ascii=False), encoding='utf-8')
    print(nom, round(al['character_end_times_seconds'][-1], 2))
