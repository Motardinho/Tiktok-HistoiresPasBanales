"""Livraison du dossier 40 : légende avec sources, crédits, contrôle daté, index. Lancer depuis la racine du projet."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/40-top-10-buts-les-plus-degueulasses')
m = p / '_montage'
A = Path('assets/40-buts-degueulasses')
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

import importlib.util  # noqa: E402 - archives.py n'est pas un paquet

# Segments des vidéos YouTube (source, début, durée, zone) : chaîne et titre lus dans <id>.info.json
spec = importlib.util.spec_from_file_location('archives', A / 'archives.py')
archives = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archives)

plans = json.loads((m / 'plans.json').read_text(encoding='utf8'))
videos, pexels, photos = [], [], []
for x in plans:
    stem = Path(x['source']).stem
    if stem.startswith('arch-'):
        yid = archives.SEGMENTS[stem[5:]][0][:-4]
        if yid not in videos:
            videos.append(yid)
    elif stem.startswith('pexels-'):
        if stem not in pexels:
            pexels.append(stem)
    elif stem.startswith('v-photo-') and stem[2:] not in photos:  # photo recadrée par archives.py
        photos.append(stem[2:])

info = {y: json.loads((A / f'{y}.info.json').read_text(encoding='utf8')) for y in videos}
sel = {s['fichier'][:-4]: s for s in json.loads((A / 'photos/selection.json').read_text(encoding='utf8'))}

lines_src = [f"{info[y]['channel']} : « {info[y]['title']} », https://youtu.be/{y}" for y in videos]
lines_photo = [f"{sel[k]['titre'].replace('File:', '')} : {sel[k]['auteur']}, {sel[k]['licence']}, {sel[k]['url']}" for k in photos]
legend = '\n'.join([
    "Notre top 10 des buts les plus dégueulasses : un ballon de plage, un nez, un trou dans le filet… et un but réclamé sur la vie d'une fille. Kane l'a touché, oui ou non ?",
    '',
    '#histoirevraie #foot #football #top #record #HistoiresPasBanales',
    '',
    'Images des matchs (extraits recadrés et montés, sans le son d’origine) :',
    *lines_src,
    '',
    'Photos (Wikimedia Commons) :',
    *lines_photo,
    '',
    'Faits : Sky Sports, Al Jazeera, Sports Illustrated, UPI, manutd.com, National Football Museum, 11v11.',
    'Plans d’accroche : Pexels. Musique : Sports Highlights - Ahjay Stelino / Mixkit. Voix synthétique ElevenLabs.',
    '',
])
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits']
credits += [f"- {x['fait']} - {x['url']}" + (f" ({x['note']})" if x.get('note') else '') for x in d['sources_a_verifier']]
credits += ['', '## Vidéos des matchs (licence YouTube standard, choix explicite de Marc du 11-12 novembre 2026)']
for y in videos:
    segs = [f"{k} : {s[1]}-{round(s[1] + s[2], 2)} s, fenêtre {s[3]} px suivant l'action" for k, s in archives.SEGMENTS.items() if s[0] == y + '.mp4']
    credits.append(f"- {y} : {info[y]['channel']}, « {info[y]['title']} », {info[y]['height']}p, https://www.youtube.com/watch?v={y} ; {' ; '.join(segs)}")
credits += ['', '## Pexels (licence Pexels)']
for k in pexels:
    j = json.loads((A / f'{k}.json').read_text(encoding='utf8'))
    credits.append(f"- {k} : {j.get('auteur', '')}, {j.get('source', '')}")
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
              sources_video=videos, photos=photos, pexels=pexels)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 40]
data.append(dict(numero=40, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : chaque but visible au moment où le ballon entre (retour de Marc), cadrage serré, Rob Green au ras du sol', apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

md = Path('out/INDEX.md')
t = md.read_text(encoding='utf8')
if '| 40 |' not in t:
    lines = t.splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith('| 3'))
    lines.insert(last + 1, '| 40 | [Top 10 des buts les plus dégueulasses](40-top-10-buts-les-plus-degueulasses/) | Export de travail, à valider |')
    md.write_text('\n'.join(lines) + '\n', encoding='utf8')
print('ok', videos, photos, pexels)
