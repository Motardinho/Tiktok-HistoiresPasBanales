"""Livraison du dossier 30 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/30-la-juve-envoyee-en-serie-b')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Cinq jours après la Coupe du monde, la Juve envoyée en Série B. Et l'Inter, qui récupère le titre ? Accusée à son tour en 2011… prescrit. La Juve : tricheuse ou bouc émissaire ? Réponds en un mot.

#histoirevraie #juventus #calciopoli #football #seriea #scandale #HistoiresPasBanales

Sources : affaire Calciopoli (2006) - Wikipédia italien « Calciopoli », « Luciano Moggi », « Gianluca Paparesta » ; Wikipédia anglais « Calciopoli », « 2006 FIFA World Cup final ». Sanction sportive de Luciano Moggi (radiation FIGC, 2011) ; condamnation pénale annulée pour prescription (Cassation, 24 mars 2015).

Images d'illustration : aucune ne montre la Juventus, ses joueurs, Luciano Moggi ni la finale 2006. Vues actuelles de l'Olympiastadion de Berlin et de Turin. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine.
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
    if 'pexels-' in k:
        credits.append(f'- {k}.mp4 : Pexels, licence Pexels, https://www.pexels.com/video/{k.split('pexels-')[1]}/')
credits += [
    '',
    'Aucune image ne montre la Juventus, ses joueurs, Luciano Moggi, les arbitres ni la finale 2006 : plans génériques Pexels.',
    'Vues réelles actuelles : Olympiastadion de Berlin (18999864, 39799276), Berlin (34640566), Turin (29808342).',
    'Le tir au but manqué est une prise d’entraînement amateur, pas le tir de Trezeguet ; l’intérieur de téléphone illustre les cartes SIM (aucune séquence 4K de carte SIM trouvée).',
    'Écartés au repérage : stades turcs identifiables (écusson de Beşiktaş, stade de Fenerbahçe), supporters avec banderoles de clubs, statuette de type Oscar, sablier en 720p, sources 2732×1440 trop étroites, une source HDR.',
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
        'Catalogues de repérage : assets/30-calciopoli/cat-*.jpg',
        '87 captures du MP4 habillé (début, milieu, fin de chaque plan) : _montage/controle/final-page-*.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=['Hook : titre « LA JUVE ENVOYÉE EN SÉRIE B » sur une frappe de nuit à 0:00, « cinq jours après… la Coupe du monde » prononcé à 2,3-4,6 s, 3 plans avant 5 s', 'Titre : interligne d’origine, accent du É qui déborde sur la ligne du dessus avec contour sombre (le contrôle de collision ignore désormais les accents)', 'Ton gossip : écoutes, cartes SIM suisses, vantardise du vestiaire, l’Inter accusée à son tour, question finale « tricheuse ou bouc émissaire ? »', 'Fun fact « 8 joueurs de la Juve en finale » 30,6-34,6 s, encart retiré avant le tir au but pour laisser voir la barre', 'Corrections après contrôle : stades de Beşiktaş et de Fenerbahçe remplacés, tir au but réel ajouté, drapeau du feu d’artifice sorti du cadre, trophée pris après sa pose'],
    limites=['Aucune écoute possible : prononciations (Juve corrigé le 11/11, Modji, Trézéguet, Ibrahimovitch, Del Piéro, Buffon) et mix non validés à l’oreille.', 'Contrôle par captures, pas de visionnage continu.', 'Durée 74,4 s, au-dessus de la cible 61-70 s (plafond 75 s respecté).', 'Cartes SIM illustrées par un intérieur de téléphone, sans carte visible.'],
    a_revoir_avant_de_poster=['Tir de Trezeguet sur la barre : lu dans un résumé de la page Wikipédia de la finale, à revérifier mot à mot.', 'Moggi est vivant : la vidéo s’en tient à la radiation sportive, aux écoutes rapportées (« se vante ») et à « selon les enquêteurs » pour les cartes SIM.', 'Label IA TikTok non requis (vrais plans, voix de narrateur qui n’imite personne).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 30]
data.append(dict(numero=30, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, niche sport, ton gossip (Calciopoli 2006)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

print('ok', used)
