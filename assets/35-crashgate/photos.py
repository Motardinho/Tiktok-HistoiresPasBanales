"""Photos Commons en vignettes de taille standard (demande de Wikimedia), avec auteur, licence, date.
Peu d'appels : un pour les metadonnees, un par taille de vignette. python photos.py <dossier assets> cle=Titre ..."""
import json, re, sys, time
from pathlib import Path
import requests

UA = {'User-Agent': 'media-research-script/1.0'}
API = 'https://commons.wikimedia.org/w/api.php'
p = Path(sys.argv[1]) / 'photos'
p.mkdir(parents=True, exist_ok=True)
pairs = dict(a.split('=', 1) for a in sys.argv[2:])
pairs = {k: t for k, t in pairs.items() if not (p / f'photo-{k}.jpg').exists()}
if not pairs:
    sys.exit('rien a telecharger')
clean = lambda e, k: re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', e.get(k, {}).get('value', ''))).strip()


def call(titles, **extra):
    for attempt in range(5):
        time.sleep(10 + 60 * attempt)
        r = requests.get(API, headers=UA, timeout=60, params=dict(action='query', format='json', prop='imageinfo',
                         titles='|'.join('File:' + t for t in titles), **extra))
        if r.ok and r.text.startswith('{'):
            q = r.json()['query']
            norm = {n['to']: n['from'] for n in q.get('normalized', [])}
            return {norm.get(x['title'], x['title'])[5:]: x for x in q['pages'].values()}
    raise RuntimeError(r.status_code)


meta = call(pairs.values(), iiprop='size|extmetadata', iiextmetadatafilter='LicenseShortName|LicenseUrl|Artist|DateTimeOriginal|ImageDescription')
sizes = {}
for key, title in pairs.items():
    if 'imageinfo' not in meta[title]:
        print('ABSENT', key, title); continue
    w = meta[title]['imageinfo'][0]['width']
    sizes.setdefault(next((s for s in (3840, 1920, 1280, 960) if s <= w), 960), []).append(key)
sel_file = p / 'selection.json'
sel = json.loads(sel_file.read_text(encoding='utf8')) if sel_file.exists() else []
for size, keys in sizes.items():
    thumbs = call([pairs[k] for k in keys], iiprop='url', iiurlwidth=size)
    for key in keys:
        title = pairs[key]; i = meta[title]['imageinfo'][0]; e = i['extmetadata']
        time.sleep(5)
        d = requests.get(thumbs[title]['imageinfo'][0]['thumburl'], headers=UA, timeout=180)
        if d.status_code != 200:
            print('ECHEC', key, d.status_code, size, flush=True); continue
        (p / f'photo-{key}.jpg').write_bytes(d.content)
        row = dict(cle=key, fichier=f'photo-{key}.jpg', titre='File:' + title, licence=clean(e, 'LicenseShortName'), licence_url=clean(e, 'LicenseUrl'),
                   auteur=clean(e, 'Artist'), date=clean(e, 'DateTimeOriginal'), taille_originale=f"{i['width']}x{i['height']}", largeur_telechargee=size,
                   url='https://commons.wikimedia.org/wiki/File:' + title.replace(' ', '_'), description=clean(e, 'ImageDescription')[:300])
        sel = [s for s in sel if s['cle'] != key] + [row]
        sel_file.write_text(json.dumps(sel, ensure_ascii=False, indent=1), encoding='utf8')
        print(key, row['taille_originale'], size, row['licence'], '|', row['auteur'][:30], '|', row['date'][:20], '|', row['description'][:70], flush=True)
