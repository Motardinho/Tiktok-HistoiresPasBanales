"""Livraison du dossier 29 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/29-le-faux-ministre-au-masque')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Un masque en silicone, un faux bureau de ministre… et des milliardaires qui virent des millions. Chikli : génie ou simple voyou ? Réponds en un mot.

#histoirevraie #arnaque #escroquerie #ledrian #faitsdivers #HistoiresPasBanales

Sources : escroquerie au « faux Le Drian » (2015-2017) - Public Sénat, 2 février 2020 ; AFP via Times of Israël, 9 septembre 2020 ; The Telegraph via NZ Herald, 4 février 2020 ; Wikipédia « Gilbert Chikli ». Condamnés en appel le 9 septembre 2020 : Gilbert Chikli (10 ans) et Anthony Lasarevitsch (7 ans), qui nient les faits.

Aucune image ne montre Gilbert Chikli ni son complice (pas de photo libre), ni le vrai masque de l'affaire. Les autres plans sont des illustrations ; seules les photos nommées ci-dessous montrent les personnes citées.
Photos des personnes citées (Wikimedia Commons) : Jean-Yves Le Drian - Remi Jouan, CC BY-SA 3.0 et Pymouss, CC BY 3.0 ; François Hollande - COP Paris, CC0 ; Mohammed VI - UN Climate Change, CC BY 2.0 ; Ali Bongo Ondimba - Foreign and Commonwealth Office, OGL v1.0 ; André Vingt-Trois - Marie-Lan Nguyen, CC BY 2.5 ; Aga Khan IV - DFID, CC BY 2.0 ; Macky Sall - Chief, National Guard Bureau, CC BY 2.0 ; Albert II - UN Climate Change, CC BY 2.0. Photos recadrées. Liens dans CREDITS.md. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine.
Masques en silicone hyperréalistes : « Disturbingly Realistic Masks Made Possible by 3D Printing », LulzBot, YouTube, licence Creative Commons Attribution (CC BY-SA 4.0 indiquée en fin de vidéo), https://www.youtube.com/watch?v=P4bEWl0w-dw - masques de l'atelier Hyperflesh, sans lien avec l'affaire, recadrés et montés sans le son d'origine.
Musique : Masking the Masters - Eugenio Mininni / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
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
    'Aucune image ne montre Jean-Yves Le Drian, Gilbert Chikli, son complice, les victimes ni le faux bureau : plans génériques Pexels. Les masques sont de vrais masques en silicone hyperréalistes de l’atelier Hyperflesh, pas le masque de l’affaire (aucune image publique libre de ce masque).',
    '- Masques en silicone hyperréalistes : « Disturbingly Realistic Masks Made Possible by 3D Printing », LulzBot, YouTube, licence Creative Commons Attribution (CC BY-SA 4.0 indiquée en fin de vidéo), https://www.youtube.com/watch?v=P4bEWl0w-dw - masques de l’atelier Hyperflesh, sans lien avec l’affaire, recadrés et montés sans le son d’origine.',
    'Vues réelles mais génériques : Paris de nuit (19006219), Kiev, place de l’Indépendance (14615718), Monaco (11957604).',
    'Écartés au repérage : bureau avec calligraphie arabe au mur, SMS en vietnamien, visages d’hommes qui pouvaient passer pour l’escroc (téléphone, bureau, prison de face, masque levé), masque Anonymous devant un drapeau américain, compteuse de billets floue.',
    '', '## Photos des personnes citées (Wikimedia Commons, recadrées)',
] + [f"- {r['titre'][5:]} - {r['auteur']} - {r['licence']} - {r['url']}" for r in json.loads(Path('assets/29-faux-le-drian/photos/selection.json').read_text(encoding='utf8')) if r['fichier'] != 'agakhan-03.jpg'] + [
    '', '## Son',
    '- Masking the Masters - Eugenio Mininni, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
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
        'Catalogues de repérage : assets/29-faux-le-drian/cat-*.jpg',
        '87 captures du MP4 habillé (début, milieu, fin de chaque plan) : _montage/controle/final-page-*.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=['Hook : titre « IL S’EST FAIT PASSER POUR UN MINISTRE » sur le gros plan d’un vrai masque en silicone hyperréaliste à 0:00, « masque en silicone » prononcé à 2,6-3,0 s, 3 plans avant 5 s', 'Ton gossip : faux bureau, otages, milliardaires piégés, trahi par un vouvoiement, « eux jurent toujours que ce n’était pas eux », question finale « génie ou simple voyou ? »', 'Fun fact « trahi par un vouvoiement » 40,8-48,2 s, encart en haut sur des plans au haut du cadre libre, sous-titres maintenus', 'Photos réelles (Commons) calées sur chaque nom prononcé : Le Drian (2 photos), Hollande, Mohammed VI, Ali Bongo, André Vingt-Trois, Aga Khan, Macky Sall (fun fact, recadrée sous l’encart), Albert II ; bandeau « PARIS - 2015 » raccourci pour ne pas passer sur la photo de 2014 ; Chikli sans photo (aucune photo libre), silhouette conservée',
        'Corrections après contrôle : 7 plans remplacés (calligraphie arabe, SMS étrangers, quatre visages pouvant passer pour Chikli, compteuse floue) ; masques de carnaval remplacés par de vrais masques en silicone (demande de Marc), têtes de célébrités (Walter White, Tyrion) et enseigne Hyperflesh laissées hors cadre', 'Sources Pexels 4K ou vertical natif ≥ 1080×1920, BT.709 ; aucune source HDR'],
    limites=['Aucune écoute possible : prononciations (Skaïpe, Aga Khan, Chikli, Le Drian) et mix non validés à l’oreille.', 'Contrôle par captures, pas de visionnage continu.', 'Durée 73,4 s, au-dessus de la cible 61-70 s (plafond 75 s respecté).', 'Photos de personnes : dates 2011 à 2022, pas forcément de l’époque des faits (Le Drian 2014 et 2011, Sall 2022, Albert II 2016) ; l’archevêque de Paris de 2005 à 2017 était André Vingt-Trois, la cible exacte n’est pas nommée par les sources.',
        'Photos fixes avec léger zoom (aucune vidéo libre de ces personnes trouvée en 4K).',
        'Masques en silicone : source YouTube 1080p, environ 600 px de large une fois recadrée, image plus douce que le reste (choix de Marc : vrais masques plutôt que vidéo IA).',
        'Licence du reportage LulzBot : CC BY sur YouTube, CC BY-SA 4.0 sur le carton final ; la clause SA peut imposer de partager la vidéo sous la même licence.'],
    a_revoir_avant_de_poster=['FUN FACT à source unique lue : Macky Sall repère le vouvoiement (The Telegraph, repris par le NZ Herald ; Asharq Al-Awsat le reprend de la BBC). À recouper si possible avant de poster.', 'Montants : 20 M€ (Aga Khan) et 47 M$ (Inan Kiraç) concordants Public Sénat / Telegraph.', 'Label IA TikTok non requis (vrais plans, voix de narrateur qui n’imite personne).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 29]
data.append(dict(numero=29, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, ton gossip (escroquerie au faux Le Drian)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

print('ok', used)
