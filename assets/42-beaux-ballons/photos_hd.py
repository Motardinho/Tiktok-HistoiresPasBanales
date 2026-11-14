"""Remplace les photos de photos/selection.json par l'original (ou la vignette standard 3840 px si plus large)."""
import json, sys, time
from pathlib import Path
import requests
UA = {'User-Agent': 'hpb-photo-fetch/1.1 (one-off personal download; low rate)'}
p = Path('photos'); sel = json.loads((p / 'selection.json').read_text(encoding='utf8'))
keys = sys.argv[1:] or [s['cle'] for s in sel]
for s in sel:
    if s['cle'] not in keys:
        continue
    r = requests.get('https://commons.wikimedia.org/w/api.php', headers=UA, timeout=60, params=dict(
        action='query', format='json', prop='imageinfo', titles=s['titre'], iiprop='url|size', iiurlwidth=3840 if s['taille'].split('x')[0] and int(s['taille'].split('x')[0]) > 3840 else 1920))
    i = next(iter(r.json()['query']['pages'].values()))['imageinfo'][0]
    src = i['thumburl'] if i['width'] > 1920 else i['url']
    for attempt in range(6):
        time.sleep(10 + 60 * attempt)
        d = requests.get(src, headers=UA, timeout=300)
        if d.status_code != 429:
            break
    d.raise_for_status()
    (p / s['fichier']).write_bytes(d.content)
    print(s['cle'], i['width'], 'x', i['height'], len(d.content) // 1000, 'ko', flush=True)
