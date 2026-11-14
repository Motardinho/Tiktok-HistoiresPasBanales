"""Verrouille la version validée par Marc du dossier 44 (même format que le dossier 33)."""
import hashlib
import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/44-top-5-buts-les-plus-degueulasses')
v = p / 'version-validee'
v.mkdir(exist_ok=True)
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
d['statut'] = 'validée'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
c = json.loads((p / 'controle-livraison.json').read_text(encoding='utf8'))
c.update(statut='validée par Marc', validation_utilisateur=True, validation=stamp)
(p / 'controle-livraison.json').write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding='utf8')

names = ['final.mp4', 'comparaison.mp4', 'histoire.json', 'script.txt', 'legende.txt', 'publication.txt',
         'CREDITS.md', 'controle-livraison.json', 'apercu-tiktok.jpg', 'miniature-v2.jpg']
for n in names:
    shutil.copy2(p / n, v / n)
record = dict(statut='validee', validation_par='utilisateur', message='ok pour top 5', date=stamp[:10], horodatage=stamp,
              fuseau='Europe/Paris', sha256=sha(p / 'final.mp4'), version_conservee='version-validee/final.mp4',
              fichiers_sha256={n: sha(v / n) for n in names})
for target in (p, v):
    (target / 'validation-utilisateur.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = json.loads(idx.read_text(encoding='utf8'))
row = next(x for x in data if x.get('numero') == 44)
assert row['sha256'] == record['sha256'], 'final.mp4 a changé depuis la livraison'
row.update(statut='validee', validation=stamp, version_validee='version-validee/final.mp4')
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print('validée', record['sha256'][:12])
