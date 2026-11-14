"""Liste Commons : python commons.py cat "Catégorie" ... | python commons.py search "termes" ... (images >= 1000 px)."""
import sys, time, re, json
import requests
UA = {'User-Agent': 'media-research-script/1.0'}
mode = sys.argv[1]
for q in sys.argv[2:]:
    gen = dict(generator='categorymembers', gcmtitle='Category:' + q, gcmtype='file|subcat', gcmlimit=200) if mode == 'cat' else \
        dict(generator='search', gsrsearch=q + ' filetype:bitmap', gsrnamespace=6, gsrlimit=40)
    r = requests.get('https://commons.wikimedia.org/w/api.php', headers=UA, timeout=40, params=dict(
        action='query', format='json', prop='imageinfo', iiprop='size|extmetadata',
        iiextmetadatafilter='LicenseShortName|DateTimeOriginal|Artist|ImageDescription', **gen))
    print('===', q, r.status_code)
    if r.ok:
        for p in r.json().get('query', {}).get('pages', {}).values():
            ii = p.get('imageinfo')
            if not ii:
                print(' ', p['title']); continue
            i = ii[0]; e = i['extmetadata']; g = lambda k: re.sub('<[^>]+>', '', e.get(k, {}).get('value', ''))[:70]
            if i['width'] >= 1000:
                print(' ', p['title'], '|', f"{i['width']}x{i['height']}", '|', g('LicenseShortName'), '|', g('DateTimeOriginal'), '|', g('ImageDescription'))
    time.sleep(6)
