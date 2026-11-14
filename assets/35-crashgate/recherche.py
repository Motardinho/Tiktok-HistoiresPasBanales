"""Recherche Pexels : python recherche.py <dossier assets> "terme 1" "terme 2" ... -> <terme>-search.json + résumé."""
import json, sys, time
from pathlib import Path
from curl_cffi import requests
from bs4 import BeautifulSoup
p = Path(sys.argv[1])
for term in sys.argv[2:]:
    r = requests.get('https://www.pexels.com/search/videos/' + term.replace(' ', '%20') + '/', impersonate='chrome', timeout=40)
    h = BeautifulSoup(r.text, 'html.parser')
    tag = h.find('script', id='__NEXT_DATA__')
    if not tag:
        print(term, 'ECHEC', r.status_code); continue
    d = json.loads(tag.string)['props']['pageProps']['initialData']['data']
    (p / (term.replace(' ', '-') + '-search.json')).write_text(json.dumps(d, ensure_ascii=False), encoding='utf8')
    print('==', term)
    for x in d:
        a = x['attributes']
        print(' ', x['id'], f"{a['width']}x{a['height']}", (a.get('description') or a.get('title') or '')[:90])
    time.sleep(2)
