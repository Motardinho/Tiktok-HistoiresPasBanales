"""Livraison du dossier 38 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/38-top-10-corruptions-du-foot')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

plans = json.loads((m / 'plans.json').read_text(encoding='utf8'))
used = []
for x in plans:
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Notre top 10 des plus grosses corruptions du foot : d'un arbitre payé avec une télé à un raid de la police dans un palace de Zurich. L'OM en 6e : trop haut ou trop bas ? Réponds en un mot.

#histoirevraie #foot #corruption #top #record #HistoiresPasBanales

Sources : scandale des paris truqués en Allemagne (2005) ; Nîmes Olympique, tribunal correctionnel de Paris (septembre 2018) ; affaire Osasuna, Audience provinciale de Navarre et Tribunal suprême ; scandale de la Bundesliga (1971) ; affaire VA-OM (1993) ; Totonero (1980) ; Calciopoli (2006) ; condamnations de l'ex-président de la fédération chinoise (26 mars 2024) et de l'ex-sélectionneur chinois (13 décembre 2024) ; affaire ISL (Zoug, 2008, documents publiés en 2012 ; rapport d'éthique de la FIFA, 2013) ; FIFAgate (arrestations de Zurich, 27 mai 2015 ; acte d'accusation du ministère américain de la Justice, décembre 2015). Classement établi par la rédaction, selon l'ampleur du scandale.

Photos (Wikimedia Commons, recadrées) : Bernard Tapie 1994 - © Union européenne 1994, Parlement européen ; Paolo Rossi - domaine public ; João Havelange 1997 - Leo Medvedev, CC BY-SA 4.0 ; stade Reyno de Navarra - Stuart MacDonald, CC BY 3.0 ; siège de la FIFA - Juerg.hug, CC BY-SA 3.0, et Bic, CC BY-SA 4.0.
Vidéos YouTube sous licence Creative Commons BY, recadrées : Stade des Costières - Oziak, https://www.youtube.com/watch?v=7GXJor7D2NM ; Benito Villamarín - En el Gol Sur del Villamarín, https://www.youtube.com/watch?v=wkMCHKErJyg ; Baur au Lac - reisememo.ch, https://www.youtube.com/watch?v=QfWTXzqS4xM . Liens dans CREDITS.md. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine : illustrations, elles ne montrent pas les faits.
Musique : Greed - Arulo / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
(p / 'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']) + '\n', encoding='utf8')
rows = json.loads(Path('assets/38-top10-corruption/photos/selection.json').read_text(encoding='utf8'))
rows += [r for r in json.loads(Path('assets/37-main-henry/photos/selection.json').read_text(encoding='utf8')) if r['cle'] in ('fifa10', 'fifahall')]
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vidéos réelles des lieux (YouTube, Creative Commons BY, recadrées, sans le son d’origine)',
    '- Stade des Costières, Nîmes - Ajaccio, mai 2018 : Oziak, https://www.youtube.com/watch?v=7GXJor7D2NM (passage 76-79 s filmé en tribune ; la vidéo contient ailleurs des images marquées « Nîmes TV », non utilisées)',
    '- Benito Villamarín, Betis - Valence, octobre 2017 : En el Gol Sur del Villamarín, https://www.youtube.com/watch?v=wkMCHKErJyg',
    '- Hôtel Baur au Lac, Zurich, novembre 2017 : reisememo.ch, https://www.youtube.com/watch?v=QfWTXzqS4xM (filigrane hors du cadre vertical)',
    '', '## Vidéos utilisées (illustrations, licence Pexels)']
for k in used:
    if 'pexels-' in k:
        credits.append(f"- {k}.mp4 : https://www.pexels.com/video/{k.split('pexels-')[1]}/")
credits += [
    '',
    'Aucune vidéo ne montre les matchs, les personnes ni les lieux des affaires, sauf mention : vues actuelles de Marseille, Milan, Turin, Berlin, Zurich, Pékin (place Tian’anmen) et Séville.',
    'Photos restantes et pistes vidéo examinées : Tapie, Rossi, Havelange (règle photo à chaque nom cité, aucune vidéo libre de ces personnes) ; stade Reyno de Navarra / El Sadar (YouTube CC : arrivée du Real Madrid avec visages de joueurs sans rapport, entrée des équipes en 720p, supporters de Saragosse devant le stade sans vue du stade ; Pexels « pamplona » sans le stade) ; siège de la FIFA, deux photos (YouTube CC : visite du musée de la FIFA, pas du siège ; supporters devant le siège en 1080x1080 ; Pexels sans le siège).',
    'Écartés au contrôle : vidéo de Zurich en HDR, penalty filmé depuis la tribune (têtes au premier plan), stade plein aux sièges jaunes (pays non identifiable, possiblement turc) pendant « Allemagne », juge en perruque à l’anglaise pendant « justice américaine », photo Italie-Brésil 1982 (Rossi non identifiable), vue du parc du Baur au Lac (hôtel invisible).',
    '', '## Photos (Wikimedia Commons, recadrées)',
    '- Bernard Tapie 1994 - European Parliament Multimedia Centre, © Union européenne 1994 - PE - https://commons.wikimedia.org/wiki/File:Bernard_Tapie_1994.jpg',
] + [f"- {r['titre'][5:]} - {r['auteur']} - {r['licence']} - {r['url']}" for r in rows] + [
    '', '## Son',
    '- Greed - Arulo, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
    '- Whoosh des volets : synthèse maison, aucun son tiers.',
    '- Narration synthétique ElevenLabs.', '',
    'Comparaison de travail uniquement : vidéo HPB des montagnes russes validée (top), à gauche.', '',
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
        'Planches de repérage : assets/38-top10-corruption/planche-*.jpg et photos/planche.jpg',
        '120 captures du MP4 habillé (début, milieu, fin de chaque plan) : _montage/controle/final-page-*.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Hook : titre « TOP 10 DES PLUS GROSSES CORRUPTIONS DU FOOT » sur un stade vu du ciel à 0:00 ; phrase-hameçon « Le numéro un a fini à l’aube, dans un palace, avec la police » de 2,9 à 7,3 s ; 3 plans avant 5 s',
        'Volet jaune et whoosh à chaque rang (10 volets), coupe de plan sous le panneau',
        'Photos réelles sur chaque nom prononcé : Tapie (41,9 s), Rossi (46,1 s), Havelange (68,8 s) ; vidéos réelles des lieux : Costières (14,5 s), Benito Villamarín (25,3 s), façade du Baur au Lac (76,1 s) ; photos réelles : Reyno de Navarra, siège de la FIFA',
        'Fun fact « SUSPENDU 2 ANS - PUIS BALLON D’OR 1982 » de 46,1 à 50,9 s sur la photo de Rossi, encart descendu à y = 770 pour dégager le visage',
        'Bandeaux de rang 10 à 1 avec lieu, année et chiffre clé ; fin sur la question OM puis l’appel à s’abonner et la signature'],
    limites=[
        'Durée 86,9 s : au-dessus de la cible 61-70 s, format top 10 d’environ 80 s choisi par Marc.',
        'Photos Commons en vignettes de 1280 px (960 px pour Rossi) : originaux bloqués par Wikimedia (erreur 429), image un peu douce sur Rossi.',
        'Vidéos réelles des Costières, du Villamarín et du Baur au Lac en source 1080p : environ 600 px utiles après recadrage vertical, sous le seuil de 1 000 px ; gardées car plus nettes que les photos qu’elles remplacent (405 et 960 px) et seules vues réelles trouvées.',
        'Licence de la vidéo des Costières : CC BY déclarée par un particulier sur un montage qui contient ailleurs des images « Nîmes TV » ; seul le passage filmé en tribune est utilisé, mais la licence reste à confirmer par Marc.',
        'L’encart du fun fact frôle le menton de Rossi : impossible de descendre plus bas sans toucher les sous-titres.',
        'Aucune écoute possible : prononciations (Ossassouna, Bétis, Boundesliga, Caltchopoli, I S L, Avelange, Fifa guéte) et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Quota ElevenLabs quasiment épuisé : toute retouche du texte demandera de relever la limite de la clé.'],
    a_revoir_avant_de_poster=[
        'Classement éditorial (ampleur) : assumé dans la légende, à défendre en commentaire si contesté.',
        'FIFAgate : 200 millions = chiffre de l’accusation américaine, dit « selon la justice américaine ».',
        'Personnes vivantes citées par leur fonction seulement, toutes condamnées : arbitre allemand, président de Nîmes, ex-patron du foot chinois.',
        'Label IA TikTok non requis (vrais plans, voix de narrateur qui n’imite personne).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 38]
data.append(dict(numero=38, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : v2, photos des Costières, du Villamarín et du Baur au Lac remplacées par de vraies vidéos (YouTube CC BY)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print('ok', len(used), 'sources')
