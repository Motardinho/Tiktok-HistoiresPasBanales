"""Livraison du dossier 26 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/26-perdu-9-jours-dans-le-sahara')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

src = json.loads(Path('assets/musique/mixkit/sources.json').read_text(encoding='utf8'))
for x in src:
    if x['slug'] == 'survie':
        x['artist'] = 'Eugenio Mininni'
Path('assets/musique/mixkit/sources.json').write_text(json.dumps(src, ensure_ascii=False, indent=2), encoding='utf8')

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Perdu 9 jours dans le Sahara en pleine course, retrouvé en Algérie… Toi, tu crois à son histoire ?

#histoirevraie #survie #sahara #marathondessables #ultratrail #sport #HistoiresPasBanales

Sources : Mauro Prosperi, Marathon des Sables 1994 (Wikipedia « Mauro Prosperi », qui cite BBC News 2014 et Men's Journal 1998). Les détails de survie viennent de son récit ; en 1998, le fondateur de la course, Patrick Bauer, l'a qualifié d'inventé.

Images d'illustration, pas de Mauro Prosperi ni de l'édition 1994 : vidéos Pexels (licence Pexels) et extraits de « 161 km nel deserto: Cosimo all'Ultra Marathon des Sables » de Massi Milani (YouTube, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/legalcode), recadrés et montés sans le son d'origine.
Musique : Silent Descent - Eugenio Mininni / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vidéos utilisées (illustrations)']
for k in used:
    if k.startswith('pexels-'):
        credits.append(f'- {k}.mp4 : Pexels, licence Pexels, https://www.pexels.com/video/{k[7:]}/')
    else:
        credits.append(f'- {k}.mp4 : Massi Milani, « 161 km nel deserto: Cosimo all’Ultra Marathon des Sables », '
                       'CC BY 3.0, https://www.youtube.com/watch?v=K_blduG9eiU (passages 4K sans repère kilométrique incrusté)')
credits += [
    '',
    'Aucune image ne montre Mauro Prosperi ni l’édition 1994. Les plans du Marathon des Sables viennent de l’Ultra Marathon des Sables récent (Maroc).',
    'Le sanctuaire est illustré par un bâtiment abandonné générique : aucune vidéo nette d’un marabout du désert trouvée.',
    '', '## Son',
    '- Silent Descent - Eugenio Mininni, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
    '- Narration synthétique ElevenLabs.', '',
    'Comparaison de travail uniquement : vidéo HPB des téléphones validée, à gauche.', '',
]
(p / 'CREDITS.md').write_text('\n'.join(credits), encoding='utf8')

export = json.loads((m / 'controle-export.json').read_text(encoding='utf8'))
tracks = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream_tags=handler_name',
                                  '-of', 'csv=p=0', str(p / 'comparaison.mp4')], encoding='utf8').strip().splitlines()
assert len(tracks) == 2, tracks
assert (p / 'comparaison.mp4').stat().st_mtime >= (p / 'final.mp4').stat().st_mtime, 'comparaison antérieure au final'
report = dict(
    date=stamp, statut='export à visionner - écoute requise',
    preuves_visuelles=[
        'Catalogues de repérage : assets/26-perdu-sahara/cat-1..4.jpg, reperage-mds-*.jpg',
        '96 captures du MP4 habillé (début, milieu, fin des 32 plans) : _montage/controle/final-page-0..7.jpg',
        'Logo et bandeau vérifiés image par image sur les 2 138 images',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Hook : titre « PERDU 9 JOURS DANS LE SAHARA », puis « retrouvé en Algérie » prononcé avant 5,0 s (fin 5,0 s), 3 plans avant 5 s',
        'Doute de l’organisateur posé dès 5,4 s et repris en question finale (contenu clivant)',
        'Fun fact « revenu courir la course 6 fois » 60,12-63,92 s, encart en haut, sous-titres maintenus',
        'Toutes les sources en 4K ou vertical natif ≥ 1080×1920, BT.709 ; source HDR écartée',
        'Corrections après contrôle : hook terne remplacé, selfie et dossard « COSIMO » retirés, routes masquées ou plans remplacés, arche « MDS ULTRA » évitée, plan d’un homme pour « elle » remplacé',
        'Pipeline : couleurs normalisées par plan (des paramètres hétérogènes faisaient disparaître l’habillage aux coupes)'],
    limites=[
        'Aucune écoute possible : voix (Prospéri), musique Silent Descent et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Durée 71,3 s, un peu au-dessus de la cible 61-70 s (maximum 75 s).',
        'Sanctuaire illustré par un bâtiment abandonné générique ; chauves-souris filmées dans un arbre, pas dans une tour.'],
    a_revoir_avant_de_poster=[
        'Fun fact « revenu 6 fois, 13e en 2001 » : confirmer par une seconde source.',
        'Consulter l’interview BBC 2014 citée par Wikipedia.',
        'Label IA TikTok (voix synthétique).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 26]
data.append(dict(numero=26, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, niche sport (Prosperi)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

md = Path('out/INDEX.md')
t = md.read_text(encoding='utf8')
if '| 26 |' not in t:
    row25 = next(l for l in t.splitlines() if l.startswith('| 25 |'))
    t = t.replace(row25, row25 + '\n| 26 | [Perdu 9 jours dans le Sahara](26-perdu-9-jours-dans-le-sahara/) | Export de travail, à valider |')
    md.write_text(t, encoding='utf8')
print('ok', used)
