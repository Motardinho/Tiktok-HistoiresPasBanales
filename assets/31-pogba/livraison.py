"""Livraison du dossier 31 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/31-pogba-braque-pour-13-millions')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Braqué pour 13 millions par des potes d'enfance… et son propre frère condamné. Toi, tu aurais pardonné ? Réponds oui ou non.

#histoirevraie #pogba #football #equipedefrance #scandale #HistoiresPasBanales

Sources : jugement du tribunal correctionnel de Paris du 19 décembre 2024 (AFP, reprise par DH et Blick) ; récit d'audience AFP du 28 novembre 2024 ; ordonnance de renvoi (AFP, 10 septembre 2024) ; interview de Paul Pogba à Sept à huit, juin 2025 (DH) ; désistement d'appel de Mathias Pogba (Paris Match, février 2025), condamnation définitive ; photo « Longue vie à mes frères », août 2025 (DH).

Images d'illustration : aucune ne montre les personnes citées, les lieux réels ni le procès. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine.
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
    'Aucune image ne montre Paul ou Mathias Pogba, les prévenus, Kylian Mbappé, Montévrain ni le tribunal de Paris : plans génériques Pexels, sans visage qui puisse passer pour une personne de l’affaire.',
    'Écartés au contrôle : groupe cagoulé avec casque et gilet tactique (pouvait passer pour la police), billets en zlotys polonais, boutique à enseigne SK LAND pendant « Adidas », stade de Fenerbahçe reconnaissable, téléphone affichant des footballeurs réels, chaussures à logo Nike, 2 sources HDR et 2 sources trop petites.',
    'Bandeau « MARS 2022 » sans lieu : la vue aérienne n’est pas Montévrain.',
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
        'Catalogues de repérage : assets/31-pogba/cat-00..03.jpg et remplacements.jpg',
        '93 captures du MP4 habillé (début, milieu, fin des 31 plans) : _montage/controle/final-page-0..7.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Révision du 11/11/2026 avant programmation : « Il fait appel » était dépassé (désistement) ; fin réécrite, voix régénérée, plans de fin recalés',
        'Hook : titre « POGBA BRAQUÉ POUR 13 MILLIONS » sur une arme braquée vers la caméra à 0:00, « son propre frère » prononcé à 3,9-4,9 s, 3 plans avant 5 s',
        'Ton gossip (consigne de Marc du 11/11/2026) : potes d’enfance, 13 millions, virée Adidas, maraboutage de Mbappé, photo « Longue vie à mes frères », question finale « tu aurais pardonné ? »',
        'Fun fact « 633 articles Adidas en 3 jours » 27,8-37,2 s, encart en haut, sous-titres maintenus',
        'Corrections après contrôle : hook (casque tactique type police), zlotys, enseigne SK LAND, stade de Fenerbahçe, footballeurs réels sur le téléphone remplacés ; bandeau MONTÉVRAIN ramené à MARS 2022',
        'Toutes les sources en vertical natif ≥ 1080×1920, BT.709 ; 2 sources HDR et 2 sources trop petites écartées'],
    limites=[
        'Aucune écoute possible : voix, musique et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Le téléphone du plan 18 fait défiler un fil générique avec de petites vignettes de personnes inconnues.',
        'Les bougies (plans 19-20) sont des cierges d’église : illustration générique, sans représentation du maraboutage.',
        'Plan 29 (stade vu du ciel) très sombre.'],
    a_revoir_avant_de_poster=[
        'Virée Adidas (fun fact) : 633 articles et 57 227 € selon l’AFP (Blick, 90min) ; Foot01 parle de 47 000 € (écart de détail signalé à Marc).',
        'Citation « quand tu te fais braquer, tu dis oui à tout » : raccourci de « tu n’as pas le temps de penser, tu dis oui à tout » (DH, juin 2025).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 31]
data.append(dict(numero=31, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : fin corrigée (désistement d’appel, photo avec ses frères), voix régénérée',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

print('ok', used)
