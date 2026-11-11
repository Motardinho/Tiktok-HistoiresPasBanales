"""Livraison du dossier 27 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/27-demi-tour-dans-la-tempete')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Il fait demi-tour en pleine tempête pour sauver un rival… qui n'avait même pas le droit de courir. Toi, tu l'aurais fait ? Oui ou non 👇

#histoirevraie #vendeeglobe #voile #sauvetage #sport #HistoiresPasBanales

Sources : Vendée Globe 1996-1997, sauvetage de Raphaël Dinelli par Pete Goss (Wikipedia « Raphaël Dinelli », « Pete Goss », « 1996-1997 Vendée Globe » ; The Irish Times, 27 décembre 1996 ; petegoss.com).

Images : archives INA « Les naufragés du Vendée Globe » (épave d'Algimouss et Dinelli vus de l'avion australien, Pete Goss), archives non datées du Vendée Globe (INA) ; autres plans d'illustration Pexels (licence Pexels), qui ne montrent ni Dinelli ni Goss.
Musique : Silent Descent - Eugenio Mininni / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vidéos utilisées']
for k in used:
    if k.startswith('pexels-'):
        credits.append(f'- {k}.mp4 : Pexels, licence Pexels, https://www.pexels.com/video/{k[7:]}/ (illustration)')
    elif k == 'arch-k791y4C_aGs':
        credits.append('- arch-k791y4C_aGs.mkv : Ina Sport, « Les naufragés du Vendée Globe | Archive INA », '
                       'https://www.youtube.com/watch?v=k791y4C_aGs, licence YouTube standard (choix de Marc du 11 nov. 2026). '
                       'Plans « archives non datées » du Vendée Globe : houle vue du pont (12,2 s), voilier gîté (16,6 s), iceberg (20 s), gréement (46,4 s).')
    elif k == 'arch-cadre-95':
        credits.append('- arch-cadre-95.mp4 : même archive INA, 95-111 s, image entière sur fond flou, filigrane exclu du cadre. '
                       'Plans authentiques de 1996 : épave d’Algimouss vue de l’avion (96,6 s), Dinelli debout sur le pont submergé (100,3 s), '
                       'Aqua Quorum à quai et Pete Goss accueilli (104,3 à 109,8 s).')
credits += [
    '',
    'Écartés de l’archive INA car ils montrent d’autres marins : chavirage de Philippe Poupon (1989), sauvetages de Tony Bullimore et de François Dubois (radeaux orange), naufrage de Gerry Roufs.',
    'Aucune image du chavirage d’Algimouss ni du largage du radeau : passages illustrés par une mer déchaînée (Pexels) et le gréement couché d’une archive non datée.',
    'Le fax est illustré par des feuilles de papier (aucune vidéo nette d’un fax trouvée).',
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
        'Planches de repérage : assets/27-demi-tour-tempete/planche-pexels*.jpg, cat-1..3.jpg, reperage-ina*.jpg',
        '114 captures du MP4 habillé (début, milieu, fin des 38 plans) : _montage/controle/final-page-0..9.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Hook : vague qui déferle à 0:00, titre « DEMI-TOUR DANS LA TEMPÊTE », « un Anglais risque tout » prononcé de 3,4 à 4,6 s, 3 plans avant 5 s',
        'Angle clivant posé à 6,2-8,5 s (« pas le droit d’être là ») et repris en question finale « Toi, tu aurais fait demi-tour ? »',
        'Appels de fin à l’oral : « Réponds oui ou non, et abonne-toi pour le prochain dossier » (65,9-68,4 s), aucun panneau',
        'Fun fact « demande en mariage par le fax de son sauveteur » 54,5-62,0 s, encart en haut, sous-titres maintenus',
        'Bandeaux « MERS DU SUD - NOËL 1996 » (19,2 s) et « DEMI-TOUR FACE AU VENT » (37,2 s)',
        'Plans authentiques INA de 1996 en image entière sur fond flou, au-dessus des sous-titres, filigrane ina.fr hors cadre',
        'Pexels en 4K ou vertical natif, BT.709 ; deux sources HDR écartées (28915818, 34180226)'],
    limites=[
        'Aucune écoute possible : voix (« Pite Goss »), musique et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Archives INA en définition SD (années 1990), licence YouTube standard : exception choisie par Marc.',
        'Chavirage et largage du radeau sans image authentique ; fax illustré par des feuilles de papier.',
        'YouTube a bloqué le téléchargement du documentaire France TV et de la chaîne « Closer To The Wind » (contrôle anti-robot) : non consultés.'],
    a_revoir_avant_de_poster=[
        'Fax de la demande en mariage : seule source, le site de Pete Goss.',
        'Durée du sauvetage non dite (2 jours selon Wikipedia en, 24 h selon Wikipedia fr).',
        'Label IA TikTok selon la décision en vigueur, « Autoriser les importations de haute qualité » activé.'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 27]
data.append(dict(numero=27, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, niche sport (Goss et Dinelli, Vendée Globe 1996)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

md = Path('out/INDEX.md')
t = md.read_text(encoding='utf8')
if '| 27 |' not in t:
    row26 = next(l for l in t.splitlines() if l.startswith('| 26 |'))
    t = t.replace(row26, row26 + '\n| 27 | [Demi-tour dans la tempête](27-demi-tour-dans-la-tempete/) | Export de travail, à valider |')
    md.write_text(t, encoding='utf8')
print('ok', used)
