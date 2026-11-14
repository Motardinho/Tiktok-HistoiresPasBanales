"""Livraison du dossier 37 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/37-la-fifa-a-paye-pour-la-main-d-henry')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()
photos = {r['fichier']: r for r in json.loads(Path('assets/37-main-henry/photos/selection.json').read_text(encoding='utf8'))}

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).name
    if k not in used:
        used.append(k)
used_photos = [photos[k] for k in used if k in photos]

legend = """18 novembre 2009 : la main d'Henry envoie la France au Mondial. 5 ans plus tard, on apprend que la FIFA a versé 5 millions à l'Irlande pour qu'elle renonce au procès. Et sept mois après la main, le karma : Knysna. Triche ou réflexe ? Réponds en un mot.

#histoirevraie #football #thierryhenry #equipedefrance #triche #HistoiresPasBanales

Sources : France-Irlande du 18 novembre 2009 (ESPN, CBC, Irish Times) ; demande irlandaise d'être la 33e équipe (Al Jazeera, 30 novembre 2009) ; révélation de John Delaney sur RTÉ le 4 juin 2015 (CBS Sports) ; version de la FIFA, prêt effacé fin 2014 (Inside World Football) ; Mondial 2010 et Knysna (Eurosport). Montant : 5 millions d'euros selon la fédération irlandaise, 5 millions de dollars selon la FIFA.

Images d'archives (extraits courts) : 20 heures de France 2 du 19/11/2009, images TF1 (INA Actu, youtube.com/watch?v=z8StDPaxo88) ; L'Équipe, « Main de Thierry Henry contre l'Irlande : pourquoi la France entière était-elle devenue folle ? » (19/11/2025, youtube.com/watch?v=Q52Vd0EEIE0) ; Téléfoot - TF1, « Thierry Henry revient sur sa main contre l'Irlande » (youtube.com/watch?v=CkWyDnvqBkc) ; FRANCE 24, « La FIFA a acheté le silence de l'Irlande pour la main d'Henry » (05/06/2015, youtube.com/watch?v=QxXpTNm6iSk) ; AFP, « France mutiny over Anelka expulsion » (21/06/2010, youtube.com/watch?v=Wa_f47OPj_g).

Photos (Wikimedia Commons, recadrées) : but de Gallas le 18/11/2009 - Nicolas Richoffer, CC BY-SA 4.0 ; Stade de France après le match - Julien Menichini, CC BY 2.0 ; Thierry Henry - wonker, CC BY 2.0 / Ronnie Macdonald, CC BY 2.0 / miguelangelnunez, CC BY 2.0 ; Robbie Keane - Michael Kranewitter, CC BY-SA 3.0 AT ; siège de la FIFA - Juerg.hug, CC BY-SA 3.0 / Bic, CC BY-SA 4.0. Vol FPV dans le Stade de France - Kevin Lomprez, CC BY 3.0. Autres vidéos : Pexels (licence Pexels), illustrations. Auteurs et liens dans CREDITS.md.
Musique : Greed - Arulo / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vidéos',
            '- stade-de-france-fpv.webm : « Stade de France FPV », Kevin Lomprez, CC BY 3.0, https://commons.wikimedia.org/wiki/File:Stade_de_France_FPV.webm (vue réelle du stade, 2021, pas le match de 2009)']
for k in used:
    if k.startswith('pexels-'):
        i = k[len('pexels-'):-4]
        credits.append(f'- {k} : Pexels, licence Pexels, https://www.pexels.com/video/{i}/')
credits += [
    '', '## Archives officielles (extraits courts, recadrés sans logo ni score, sources citées à la demande de Marc du 12/11/2026)',
    '- 20 heures de France 2 du 19/11/2009, images TF1 du match (INA Actu) : https://www.youtube.com/watch?v=z8StDPaxo88 - plan large en direct, ralentis de la main sous deux angles, centre, interview d’Henry',
    '- L’Équipe, « Main de Thierry Henry contre l’Irlande : pourquoi la France entière était-elle devenue folle ? », 19/11/2025 : https://www.youtube.com/watch?v=Q52Vd0EEIE0 - photos de presse animées de la main, du but de Keane et de la joie d’Henry',
    '- Téléfoot (TF1), « Thierry Henry revient sur sa main contre l’Irlande », 23/07/2015 : https://www.youtube.com/watch?v=CkWyDnvqBkc - Henry et Domenech sur la pelouse après le match',
    '- FRANCE 24, « La FIFA a acheté le silence de l’Irlande pour la main d’Henry », 05/06/2015 : https://www.youtube.com/watch?v=QxXpTNm6iSk - unes des journaux, John Delaney, siège de la FIFA',
    '- AFP, « France mutiny over Anelka expulsion », 21/06/2010 : https://www.youtube.com/watch?v=Wa_f47OPj_g - Knysna, les Bleus regagnent leur bus, Domenech',
    'Licence YouTube standard : utilisation sur choix explicite de Marc (12/11/2026), extraits courts, recadrés et montés avec narration. Risque de blocage ou de son coupé par les plateformes.',
    '',
    'Écartés au repérage : billets en euros flous (29992746), studio radio avec logo de station (12315775), match avec banderoles d’un autre pays (40718103), drapeau français trop lointain (20683467), photo Henry 2006 et portrait de Keane (tête sous le logo de série), Henry 2008 (minuscule entre des logos), logo FIFA11 (lettres coupées).',
    '', '## Photos (Wikimedia Commons, recadrées)',
] + [f"- {r['titre'][5:]} - {r['auteur']} - {r['licence']} - {r['url']}" for r in used_photos] + [
    '', '## Son',
    '- Greed - Arulo, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
    '- Narration synthétique ElevenLabs.', '',
    'Comparaison de travail uniquement : vidéo HPB 28 (OM-VA) validée, à gauche.', '',
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
        'Planches de repérage : assets/37-main-henry/planche-*.jpg',
        '120 captures du MP4 habillé (début, milieu, fin de chaque plan) : _montage/controle/final-page-*.jpg, puis verif-corrections*.jpg après retouches',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Hook : titre « LA FIFA A PAYÉ POUR LA MAIN D’HENRY » sur la vraie action (Henry, le ballon contre la main devant le but, L’Équipe), puis Henry main levée (1,7 s), billets (2,6 s), siège de la FIFA (4,2 s) ; « Cinq millions… » prononcé à 2,6 s.',
        'Action réelle à chaque temps fort : plan large en direct, ralenti de la main (INA, 20 h de France 2), gros plan de la main et deuxième touche (L’Équipe), centre (INA), but de Gallas (photo Commons), joie d’Henry, Henry et Domenech après le match (Téléfoot), Henry au micro le soir même (INA), unes irlandaises et John Delaney (FRANCE 24), bus de Knysna et Domenech (AFP).',
        'Chute karma demandée par Marc : « Et là, le karma frappe. Qualifiés grâce à une main, les Bleus sombrent au Mondial : grève dans le bus à Knysna… », deuxième angle de la main sur « qualifiés grâce à une main », bus de Knysna sur « grève dans le bus ».',
        'Deux photos réelles du match du 18 novembre 2009 : Gallas fête son but pendant que Kilbane réclame la main (recadrage qui glisse de Gallas à Kilbane sur « L’arbitre n’a rien vu »), puis le Stade de France en fête.',
        'Photo réelle à chaque nom prononcé : Henry (4 fois), Robbie Keane, William Gallas.',
        'Fun fact « L’Irlande veut être la 33e équipe » 38,0-44,8 s, encart en haut sans visage dessous ; bandeaux FRANCE - IRLANDE et BARRAGE RETOUR - MONDIAL 2010 sur la 2e scène, JUIN 2015 sur la révélation.',
        'Corrections après premier contrôle : ouverture qui partait dans le ciel, panneau HERVÉ x STADE DE FRANCE sorti du hook, encart et bandeaux décalés d’une scène, drapeau irlandais hors cadre, visage d’Henry 2006 et de Keane sous le logo, « Henri » écrit à l’écran, billets flous, tourbillon flou en fin de plan.'],
    limites=[
        'Archives du 20 heures en 512x288 et AFP en 640x480 : extraits nets mais doux une fois agrandis, posés en image entière sur fond flou (procédé des dossiers 27 et 40).',
        'Durée 74,97 s : sous le plafond de 75 s, au-dessus de la cible 61-70 s, à cause de la chute karma ajoutée.',
        'Photos d’Henry datées 2007, 2012 et 2014 (aucune photo libre exploitable de 2009) ; panneau Emirates visible derrière Henry main levée (publicité du stade, pas un filigrane).',
        'Photo de la fête au Stade de France en 1024 px : un peu douce une fois recadrée (2 s).',
        'Plans de match de nuit Pexels : stade étranger, présentés comme illustrations ; petits logos de sponsors dans les tribunes.',
        'Aucune écoute possible : prononciations (Henri, Robi Kine, Galasse) et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.'],
    a_revoir_avant_de_poster=[
        '« Cinq millions » sans devise à l’oral : la FAI parle d’euros, la FIFA de dollars ; préciser en commentaire épinglé si on vous corrige.',
        'Henry est vivant : la vidéo s’en tient à la main reconnue par lui et à des déclarations datées (FAI 2015, FIFA). Aucune accusation pénale.',
        'Label IA TikTok non requis (vrais plans et photos, voix de narrateur qui n’imite personne).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 37]
data.append(dict(numero=37, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, niche sport, sujet français (main d’Henry, 2009)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print('ok', len(used), 'sources', tracks)
