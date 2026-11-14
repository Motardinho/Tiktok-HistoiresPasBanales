"""Dossier 31, révision v2 : hook « 13 millions d'euros » (Marc, 14 novembre 2026).

Seul le hook est resynthétisé (même voix, modèle, stabilité et graine que la voix validée).
La suite reprend voix.mp3 validée à partir de « Mars » (5,36 s), sans changer un mot.
Produit _montage/voix.wav, timings-oraux.json, musique.wav et mix.wav.
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from narrateur.voice import _api_key  # noqa: E402
import monter_lot_21_23 as lot  # noqa: E402

HOOK = "Pogba braqué pour treize millions d'euros. Et parmi les condamnés… son propre frère."
CUT = 5.36  # début de « Mars » dans la voix validée
GAP = 0.08  # respiration entre le hook et « Mars », comme dans l'original

src = ROOT / 'out/31-pogba-braque-pour-13-millions'
w = Path(__file__).resolve().parent
m = w / '_montage'
m.mkdir(exist_ok=True)


def ff(*a, cwd=None):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str, a)], cwd=cwd, check=True)


def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', str(p)]))


def words_from(al, offset=0.0):
    words, cur, start, last = [], '', None, 0
    for c, a, b in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if c.isspace():
            if cur:
                words.append(dict(w=cur, start=round(start + offset, 3), end=round(last + offset, 3)))
            cur, start = '', None
        else:
            if start is None:
                start = a
            cur += c
            last = b
    if cur:
        words.append(dict(w=cur, start=round(start + offset, 3), end=round(last + offset, 3)))
    return words


old = json.loads((src / '_montage/timings-oraux.json').read_text(encoding='utf-8'))
hook_mp3 = m / 'hook.mp3'
if not hook_mp3.exists():
    cfg = yaml.safe_load((ROOT / 'config.yaml').read_text(encoding='utf-8'))['voice']
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{old['voice_id']}/with-timestamps",
                      params={'output_format': cfg['output_format']}, headers={'xi-api-key': _api_key()},
                      json=dict(text=HOOK, model_id=old['model'], seed=7112026,
                                voice_settings=dict(stability=old['stability'], similarity_boost=.75)), timeout=300)
    r.raise_for_status()
    data = r.json()
    hook_mp3.write_bytes(base64.b64decode(data['audio_base64']))
    (m / 'hook-alignement.json').write_text(json.dumps(data.get('alignment') or data['normalized_alignment'],
                                                       ensure_ascii=False), encoding='utf-8')
al = json.loads((m / 'hook-alignement.json').read_text(encoding='utf-8'))
hook_words = words_from(al)
hook_end = hook_words[-1]['end'] + GAP
# Hook coupé juste après « frère. », puis voix validée à partir de « Mars ».
ff('-i', hook_mp3, '-ss', CUT, '-i', src / '_montage/voix.mp3', '-filter_complex',
   f'[0:a]aresample=44100,atrim=0:{hook_end},apad=whole_dur={hook_end}[h];[1:a]aresample=44100[r];[h][r]concat=n=2:v=0:a=1,aformat=channel_layouts=mono[a]',
   '-map', '[a]', '-c:a', 'pcm_s16le', m / 'voix.wav')
shift = hook_end - CUT
rest = [dict(w=x['w'], start=round(x['start'] + shift, 3), end=round(x['end'] + shift, 3))
        for x in old['words'] if x['start'] >= CUT - .01]
duration = dur(m / 'voix.wav')
timing = dict(duration=duration, words=hook_words + rest, model=old['model'], voice_id=old['voice_id'],
              stability=old['stability'], hook_fin=hook_end, decalage_suite=shift,
              note='Hook resynthétisé ; suite = voix validée à partir de 5,36 s')
(m / 'timings-oraux.json').write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding='utf-8')

# Musique « scandale » sur la nouvelle durée, même mixage que le lot.
story = json.loads((src / 'histoire.json').read_text(encoding='utf-8'))
ff('-i', m / 'voix.wav', '-c:a', 'libmp3lame', '-b:a', '192k', m / 'voix.mp3')
lot.music(story, m, duration)
print('hook', round(hook_end, 2), 's ; total', round(duration, 2), 's')
print(' '.join(f"{x['w']}@{x['start']}" for x in hook_words))
