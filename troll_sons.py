"""Sons du gag Nokia 3310 (V2 téléphones) : voix angélique + bruitages ElevenLabs. Idempotent."""
import sys, requests
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from narrateur.voice import _api_key
D = ROOT/'assets/refonte-14-20/telephone/troll'
H = {'xi-api-key': _api_key()}
TEXTE = "[softly] Numéro un… le légendaire… Nokia 3310."
VOIX = {}  # voix générées par troll_voix.py
SFX = {
 'choeur': ("Heavenly angelic choir singing a single sustained 'aaaah' chord, ethereal, with harp glissando, divine revelation", 4.0),
 'boom': ("Vine boom meme sound effect, deep bass impact thud", 1.0),
 'rire': ("Goofy cartoon troll laughing, mischievous high pitched 'hehehehe' cackle, meme sound", 2.0),
 'scratch': ("Record scratch, vinyl rewind stop sound effect, comedic", 1.0),
 'tampon': ("Heavy rubber stamp slamming down on a wooden desk, single loud thud", 0.6),
 'descente': ("Angelic heavenly choir singing a swelling 'aaaah', with a slow descending harp glissando, divine light coming down from the sky, magical and majestic", 4.0),
 'carillon': ("Magical sparkle chime, bright shimmering bell twinkle, heavenly ding, short", 1.5),
 'rembobinage': ("VHS tape fast rewind sound, rapid tape whirr, short", 1.0),
}
for nom, vid in VOIX.items():
    f = D/f'voix-{nom}.mp3'
    if f.exists(): continue
    r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}', headers=H,
        params={'output_format': 'mp3_44100_128'}, timeout=120,
        json={'text': TEXTE, 'model_id': 'eleven_v4', 'seed': 3310,
              'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}})
    if r.status_code != 200: print(nom, r.status_code, r.text[:300]); continue
    f.write_bytes(r.content); print('ok', f.name)
for nom, (prompt, d) in SFX.items():
    for k in (1, 2):
        f = D/f'sfx-{nom}-{k}.mp3'
        if f.exists(): continue
        r = requests.post('https://api.elevenlabs.io/v1/sound-generation', headers=H, timeout=120,
            json={'text': prompt, 'duration_seconds': d, 'prompt_influence': 0.6})
        if r.status_code != 200: print(nom, r.status_code, r.text[:300]); break
        f.write_bytes(r.content); print('ok', f.name)
