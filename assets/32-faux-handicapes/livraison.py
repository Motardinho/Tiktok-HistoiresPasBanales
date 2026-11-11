"""Livraison du dossier 32 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/32-espagne-a-vole-or-paralympique')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """10 joueurs sur 12 sans handicap, et l'or paralympique au cou. Le journaliste infiltré : héros ou complice ? Réponds en un mot.

#histoirevraie #basket #jeuxparalympiques #espagne #scandale #HistoiresPasBanales

Sources : Comité international paralympique, retrait de la médaille en décembre 2000 ; récit de Carlos Ribagorda (magazine Capital, novembre 2000 ; NBC Sports/AFP, Vice, El Español) ; jugement de Madrid du 7 octobre 2013 (Irish Times, Público, Vozpopuli) ; eldiario.es ; Wikipédia, « Basketball ID at the 2000 Summer Paralympics ».

Images d'illustration : aucune ne montre l'équipe, le match ni les personnes citées. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine.
Musique : Greed - Arulo / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
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
credits += [
    '',
    'Aucune image ne montre l’équipe d’Espagne de 2000, le match réel, Carlos Ribagorda ni les dirigeants : plans génériques Pexels.',
    'Écartés au contrôle : arénas à logos (NBA), journaux à titres lisibles, portrait barbe et casquette d’un inconnu, pompes avec visage en gros plan, ballon à marque lisible, plans de joueuses, sources horizontales 1080p, 2 sources HDR et 2 sources en 720p.',
    'Bandeau « SYDNEY - OCTOBRE 2000 » limité au plan de l’opéra de Sydney ; bandeau « MADRID - OCTOBRE 2013 » retiré (il tombait sur la restitution de la médaille, qui date de décembre 2000).',
    '', '## Son',
    '- Greed - Arulo, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
    '- Narration synthétique ElevenLabs.', '',
    'Comparaison de travail uniquement : vidéo HPB OM-VA validée (étalon du ton gossip), à gauche.', '',
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
        'Catalogues de repérage : assets/32-faux-handicapes/cat-00..04.jpg et cat-pompes.jpg',
        '114 captures du MP4 habillé (début, milieu, fin des 38 plans) : _montage/controle/final-page-0..9.jpg, retouches.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Sujet et script validés par Marc le 11/11/2026 avant la voix',
        'Hook : titre « L’ESPAGNE A VOLÉ L’OR PARALYMPIQUE » sur un ballon qui traverse le filet à 0:00 ; « 10 joueurs sur 12 n’avaient aucun handicap » prononcé de 2,5 à 4,97 s (silencedetect) ; 3 plans avant 5 s',
        'Ton gossip : journaliste infiltré, six pompes, lever le pied à +30, barbe et casquette à l’aéroport, 5 400 euros d’amende, question finale « héros ou complice ? »',
        'Fun fact « SEUL EXAMEN : 6 POMPES » 21,3-27,8 s, encart en haut, sous-titres maintenus',
        'Corrections après contrôle : pompes avec visage en gros plan remplacées, médailles déplacées hors des sous-titres, ballon à marque lisible remplacé, bandeau Sydney raccourci, bandeau Madrid retiré',
        'Toutes les sources en vertical natif ≥ 1080×1920, BT.709'],
    limites=[
        'Aucune écoute possible : voix, musique et mix non validés à l’oreille (prononciation de « Ribagorda » et de « Q.I. » à écouter).',
        'Contrôle par captures, pas de visionnage continu.',
        'Durée 74,97 s : dans la limite de 75 s, au-dessus de la cible 61-70 s.',
        'Matchs illustrés par du basket de rue en extérieur : aucun plan libre de match masculin en salle sans logo.',
        'Le tableau de score affiche un score générique, pas 87-63.',
        'Plan 12 (pompes) : visage d’un inconnu visible de loin à la première image, puis tourné vers le sol.',
        'Plan 33 : dés formant le mot WINNER à côté de la médaille.',
        'Aéroport générique, pas Madrid-Barajas ; voyageurs masqués visibles (images récentes pour un récit de 2000).'],
    a_revoir_avant_de_poster=[
        'Question finale « héros ou complice ? » : Carlos Ribagorda est vivant et non condamné ; formulée comme une question, validée par Marc avec le script.',
        'Six pompes, lever le pied, barbe et casquette : récit du seul Ribagorda, attribué à l’oral.'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 32]
data.append(dict(numero=32, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : première livraison',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

print('ok', used)
