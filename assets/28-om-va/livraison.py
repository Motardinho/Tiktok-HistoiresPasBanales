"""Livraison du dossier 28 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/28-om-a-achete-un-match')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """L'OM a acheté un match en 1993… et celui qui a tout balancé a fini sifflé dans les stades. Glassmann : héros ou balance ? Réponds en un mot.

#histoirevraie #om #vaom #football #tapie #scandale #HistoiresPasBanales

Sources : affaire VA-OM, match du 20 mai 1993 (Wikipédia « Affaire VA-OM » et « Jacques Glassmann » ; franceinfo, « Ça s'est passé le 20 mai 1993 », 2020 ; Journal de l'année Larousse 1996). Condamnés en 1995 : Bernard Tapie, Jean-Pierre Bernès, Jean-Jacques Eydelie, Christophe Robert, Jorge Burruchaga.

Photo de Bernard Tapie : portrait de député européen, 1994 - © Union européenne 1994, Parlement européen (via Wikimedia Commons). Aucune photo libre de Jacques Glassmann ni de Christophe Robert : les autres images sont des illustrations et ne montrent ni le match, ni les joueurs. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine.
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
    'Photo de Bernard Tapie sur ses deux mentions : « Bernard Tapie 1994.jpg », European Parliament Multimedia Centre, © Union européenne 1994 - PE, https://commons.wikimedia.org/wiki/File:Bernard_Tapie_1994.jpg',
    'Aucune photo libre de Jacques Glassmann ni de Christophe Robert sur Wikimedia Commons : plans génériques (joueur de dos, enveloppe) à leurs noms.',
    'Aucune image ne montre le match VA-OM, les joueurs ni les lieux réels : plans génériques Pexels.',
    'La Réunion n’est pas montrée : aucune vidéo identifiable trouvée, le passage reste sur un plan d’entraînement générique.',
    'Écartés au repérage : billets en dollars (l’enveloppe contenait des francs), supporters reconnaissables (Fenerbahçe, club vert), stade de la fédération marocaine, homme qui aurait pu passer pour Glassmann, police et tribunaux étrangers (uniformes américains, perruques, marteau de juge).',
    '', '## Son',
    '- Greed - Arulo, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
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
        'Catalogues de repérage : assets/28-om-va/cat-00..03.jpg',
        '96 captures du MP4 habillé (début, milieu, fin des 32 plans) : _montage/controle/final-page-0..7.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Retouche du 11/11 (Marc) : photo réelle de Bernard Tapie (1994) sur « L’OM de Bernard Tapie » et « Et Tapie ? Il nie tout » ; Glassmann et Christophe Robert sans photo libre',
        'Hook : titre « L’OM A ACHETÉ UN MATCH » sur une frappe de nuit à 0:00, « enterrée dans un jardin » prononcé à 4,4-5,0 s, 3 plans avant 5 s',
        'Ton gossip (consigne de Marc du 11/11/2026) : enveloppe sur un parking, jardin de la tante, « j’ai menti de bonne foi », « la balance », question finale « héros ou balance ? »',
        'Fun fact « son indemnisation : 1 franc » 58,6-62,0 s, encart en haut, sous-titres maintenus',
        'Corrections après contrôle : supporters de Fenerbahçe, stade de la fédération marocaine et homme assis sur un ballon (pouvait passer pour Glassmann) remplacés ; clavier recadré sur l’enveloppe ; feu d’artifice recadré pour sortir un drapeau',
        'Toutes les sources en 4K ou vertical natif ≥ 1080×1920, BT.709 ; 3 sources HDR et 3 sources trop petites écartées'],
    limites=[
        'Aucune écoute possible : prononciation de « Glassmanne », musique Greed et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Une fine bande de clavier reste en haut des deux plans d’enveloppe, sous la barre de recherche TikTok.',
        'Petits panneaux de stade (« nova », sponsors de piste) visibles sur les vues aériennes 40867849, hors des 5 premières secondes.',
        'La Réunion n’est pas montrée (aucune vidéo trouvée).'],
    a_revoir_avant_de_poster=[
        'Cachette de l’enveloppe : tante (Wikipédia FR, fanafoot) ou belle-mère (franceinfo) de Christophe Robert ; la vidéo dit « la tante ».',
        'Phrase de Tapie : « J’ai menti de bonne foi » (Larousse) ; Wikipédia FR donne « J’ai menti, mais c’était de bonne foi ».',
        'Label IA TikTok (voix synthétique).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 28]
data.append(dict(numero=28, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : retouche demandée par Marc, photo de Bernard Tapie sur ses deux mentions (version validée v1 conservée dans version-validee/)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

print('ok', used)
