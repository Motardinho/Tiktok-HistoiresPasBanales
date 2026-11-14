"""Livraison du dossier 42 : légende avec sources, crédits, contrôle daté, index. Lancer depuis la racine du projet."""
import importlib.util
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/42-top-10-plus-beaux-ballons-de-foot')
m = p / '_montage'
A = Path('assets/42-beaux-ballons')
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

spec = importlib.util.spec_from_file_location('archives', A / 'archives.py')
archives = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archives)

plans = json.loads((m / 'plans.json').read_text(encoding='utf8'))
videos, photos = [], []
add = lambda lst, x: lst.append(x) if x not in lst else None
for x in plans:
    src = Path(x['source'])
    stem = src.stem
    if stem.startswith('arch-p-'):
        add(photos, Path({**archives.PHOTOS, **archives.BALLONS}[stem[5:]][0]).stem)
    elif stem.startswith('arch-'):
        add(videos, Path(archives.SEGMENTS[stem[5:]][0]).stem)
    elif src.parent.name == 'yt':
        add(videos, stem)
    elif src.parent.name == 'photos':
        add(photos, stem)

info = {y: json.loads((A / f'yt/{y}.info.json').read_text(encoding='utf8')) for y in videos}
sel = {s['fichier'][:-4]: s for s in json.loads((A / 'photos/selection.json').read_text(encoding='utf8'))}

lines_src = [f"{info[y]['channel']} : « {info[y]['title']} », https://youtu.be/{y}" for y in videos]
lines_photo = [f"{sel[k]['titre'].replace('File:', '')} : {sel[k]['auteur']}, {sel[k]['licence']}, {sel[k]['url']}" for k in photos]
d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
legend = '\n'.join([
    d['legende'],
    '',
    ' '.join(d['hashtags']),
    '',
    'Images des matchs et des ballons (extraits recadrés et montés, sans le son d’origine) :',
    *lines_src,
    '',
    'Photos (Wikimedia Commons) :',
    *lines_photo,
    '',
    'Faits : FIFA, UEFA, NASA, adidas via Sky Sports et FourFourTwo, Reuters, MercoPress, CBS Sports, Wikipédia.',
    'Musique : Sports Highlights - Ahjay Stelino / Mixkit. Voix synthétique ElevenLabs.',
    '',
])
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

credits = ['# Sources et crédits', '', '## Faits']
credits += [f"- {x['fait']} - {x['url']}" + (f" ({x['note']})" if x.get('note') else '') for x in d['sources_a_verifier']]
credits += ['', '## Vidéos (NASA : domaine public ; FIFA et UEFA : licence YouTube standard, extraits courts, choix de Marc pour montrer l’action réelle)']
for y in videos:
    segs = [f"{k} : {s[1]}-{s[1] + s[2]} s, zone {s[3]}" for k, s in archives.SEGMENTS.items() if s[0] == f'yt/{y}.mp4']
    direct = [f"plein cadre à {x['entree']} s" for x in plans if Path(x['source']).stem == y]
    credits.append(f"- {y} : {info[y]['channel']}, « {info[y]['title']} », {info[y]['height']}p, "
                   f"https://www.youtube.com/watch?v={y} ; {' ; '.join(segs + direct)}")
credits += ['', '## Photos Wikimedia Commons']
credits += [f"- {sel[k]['fichier']} : {sel[k]['titre']}, {sel[k]['auteur']}, {sel[k]['licence']} {sel[k].get('licence_url', '')}, {sel[k]['url']}" for k in photos]
credits += ['', '## Son', '- Sports Highlights - Ahjay Stelino, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
            '- Narration synthétique ElevenLabs.', '',
            'Comparaison de travail uniquement : vidéo HPB des montagnes russes validée, à gauche.', '']
(p / 'CREDITS.md').write_text('\n'.join(credits), encoding='utf8')

export = json.loads((m / 'controle-export.json').read_text(encoding='utf8'))
tracks = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream_tags=handler_name',
                                  '-of', 'csv=p=0', str(p / 'comparaison.mp4')], encoding='utf8').strip().splitlines()
assert len(tracks) == 2, tracks
assert (p / 'comparaison.mp4').stat().st_mtime >= (p / 'final.mp4').stat().st_mtime, 'comparaison antérieure au final'
report = json.loads((A / 'controle-notes.json').read_text(encoding='utf8'))
report.update(date=stamp, technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False,
              sources_video=videos, photos=photos)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 42]
data.append(dict(numero=42, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : v2, chaque ballon montré en entier (demande de Marc), nouvelle photo du Jabulani',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

md = Path('out/INDEX.md')
t = md.read_text(encoding='utf8')
if '| 42 |' not in t:
    lines = t.splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith('| 3') or l.startswith('| 4'))
    lines.insert(last + 1, '| 42 | [Top 10 des plus beaux ballons de foot](42-top-10-plus-beaux-ballons-de-foot/) | Export de travail, à valider |')
    md.write_text('\n'.join(lines) + '\n', encoding='utf8')
print('ok', videos, photos)
