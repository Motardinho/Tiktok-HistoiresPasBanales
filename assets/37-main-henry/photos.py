"""Télécharge les originaux Commons et note auteur, licence, date : python photos.py <dossier assets> clé=Titre ..."""
import json, re, sys, time
from pathlib import Path
import requests

UA = {'User-Agent': 'media-research-script/1.0'}
p = Path(sys.argv[1]) / 'photos'
p.mkdir(parents=True, exist_ok=True)
pairs = dict(a.split('=', 1) for a in sys.argv[2:])
r = requests.get('https://commons.wikimedia.org/w/api.php', headers=UA, timeout=60, params=dict(
    action='query', format='json', prop='imageinfo', titles='|'.join('File:' + t for t in pairs.values()),
    iiprop='url|size|extmetadata', iiurlwidth=3840, iiextmetadatafilter='LicenseShortName|LicenseUrl|Artist|DateTimeOriginal|ImageDescription'))
r.raise_for_status()
q = r.json()['query']
norm = {n['to']: n['from'] for n in q.get('normalized', [])}
clean = lambda e, k: re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', e.get(k, {}).get('value', ''))).strip()
sel_file = p / 'selection.json'
sel = json.loads(sel_file.read_text(encoding='utf8')) if sel_file.exists() else []
for page in q['pages'].values():
    title = norm.get(page['title'], page['title'])
    key = next(k for k, t in pairs.items() if 'File:' + t == title)
    if 'imageinfo' not in page:
        print('ABSENT', key, title); continue
    i = page['imageinfo'][0]; e = i['extmetadata']
    src = i.get('thumburl') or i['url'].split('?')[0]  # vignette standard 3840 px, comme le demande Wikimedia
    out = p / f"photo-{key}.jpg"
    if not out.exists():
        for attempt in range(6):
            time.sleep(20 + 120 * attempt)
            d = requests.get(src, headers=UA, timeout=180)
            if d.status_code != 429:
                break
        d.raise_for_status(); out.write_bytes(d.content)
    row = dict(cle=key, fichier=out.name, titre=page['title'], licence=clean(e, 'LicenseShortName'), licence_url=clean(e, 'LicenseUrl'),
               auteur=clean(e, 'Artist'), date=clean(e, 'DateTimeOriginal'), taille=f"{i['width']}x{i['height']}",
               url='https://commons.wikimedia.org/wiki/' + page['title'].replace(' ', '_'), description=clean(e, 'ImageDescription')[:300])
    sel = [s for s in sel if s['cle'] != key] + [row]
    sel_file.write_text(json.dumps(sel, ensure_ascii=False, indent=1), encoding='utf8')
    print(key, row['taille'], row['licence'], '|', row['auteur'][:40], '|', row['date'], '|', row['description'][:90])
sel_file.write_text(json.dumps(sel, ensure_ascii=False, indent=1), encoding='utf8')
