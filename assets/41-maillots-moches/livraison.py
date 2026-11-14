"""Livraison du dossier 41 : légende, crédits, contrôle daté. Lancer depuis la racine du dépôt."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/41-top-10-maillots-les-plus-moches')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

VIDEOS = [
    ('Montpellier domicile 2025-26', 'MHSC TV, « Nouveau maillot domicile 25-26 », 15/07/2025, Creative Commons BY', 'https://www.youtube.com/watch?v=-sFSl6s4_cM'),
    ('Auxerre - OM, 22/09/2007 (images Canal+)', 'mise en ligne JojoNice070, 13/10/2018', 'https://www.youtube.com/watch?v=U-SoroHDbwo'),
    ('OL - Bordeaux 1-3, 2016-17', 'Ligue 1, 11/09/2016', 'https://www.youtube.com/watch?v=_GGWWMSebXg'),
    ('Nancy - Bordeaux 0-2, 2016-17', 'Ligue 1, 29/01/2017', 'https://www.youtube.com/watch?v=MmLHQIuT7JY'),
    ('Ajaccio - OM 1-3, 2013-14', 'Ligue 1, 24/11/2013', 'https://www.youtube.com/watch?v=6cejUILWtoA'),
    ('Man City - Lyon 1-2, Ligue des champions 2018-19', 'UEFA, 23/09/2018', 'https://www.youtube.com/watch?v=FF6BxnNzftM'),
    ('Évian TG - PSG 0-1, 2012-13', 'Ligue 1, 28/04/2013', 'https://www.youtube.com/watch?v=SFApSf1PsK4'),
    ('Évian TG - Rennes 4-2, 2012-13', 'Ligue 1, 14/04/2013', 'https://www.youtube.com/watch?v=Nj6Om1Ei_wE'),
    ('Film de présentation du third OM 2012-13 (adidas)', 'mise en ligne Adidas Addict, 26/02/2014', 'https://www.youtube.com/watch?v=ftjrCj0NsAU'),
    ('Auxerre - PSG 0-0, 22/10/2006 (rediffusion polonaise, VHS)', 'mise en ligne VHS Retro Sport, 27/01/2024', 'https://www.youtube.com/watch?v=xnFCp6jePFk'),
    ('PSG - Bastia 4-0, 2013-14', 'Ligue 1, 20/10/2013', 'https://www.youtube.com/watch?v=tC9bSNIqJAQ'),
    ('Toulouse - Bastia 1-3, 2013-14', 'Ligue 1, 12/02/2014', 'https://www.youtube.com/watch?v=r6XiH_vsVUw'),
    ('Finale de la Coupe de France 2012, Lyon - Quevilly 1-0', 'FFF, 23/04/2018', 'https://www.youtube.com/watch?v=lWqsp24_PfU'),
]
PHOTOS = [
    ('Auxerre third 2007-08', 'Football Kit Archive', 'https://www.footballkitarchive.com/aj-auxerre-2007-08-third-kit/'),
    ('Bordeaux third 2016-17, détail', 'visuel officiel repris par UK Soccer Shop', 'https://blog.uksoccershop.com/girondins-de-bordeaux-release-striking-2016-17-third-kit/'),
    ('OM extérieur 2013-14', 'visuel produit adidas repris par Footy Headlines', 'https://www.footyheadlines.com/2013/05/marseille-om-1314-201314-denim-away-kit.html'),
    ('OL third 2018-19', 'visuel officiel adidas/OL repris par Football Fashion', 'https://footballfashion.org/wordpress/2018/08/24/olympique-lyon-201819-adidas-third-kit/'),
    ('OM third 2012-13', 'Classic Football Shirts', 'https://www.classicfootballshirts.co.uk/2012-13-olympique-marseille-third-shirt-910-m-mart12249573.html'),
    ('PSG extérieur 2006-07', 'Classic Football Shirts', 'https://www.classicfootballshirts.co.uk/2006-07-paris-saint-germain-away-shirt-810-xl-psga06697677.html'),
    ('OL européen 2012-13', 'Classic Football Shirts', 'https://www.classicfootballshirts.com/2012-13-lyon-third-shirt-810-xl-lynt12366394.html'),
]
COMMONS = [
    ('Akhenaton, Festival des Vieilles Charrues 2018', 'Thesupermat, CC BY-SA 4.0', 'https://commons.wikimedia.org/wiki/File:Festival_des_Vieilles_Charrues_2018_-_IAM_-_030.jpg'),
    ('Auguste et Louis Lumière, vers 1895', 'auteur inconnu, domaine public', 'https://commons.wikimedia.org/wiki/File:Lumi%C3%A8re_brothers.jpg'),
]
PEXELS = ['31343045', '35117249', '7988641', '8261604', '7985885']

legend = """Notre top 10 des maillots les plus moches du foot français : du faux jean, du camouflage, du marron-rose que l'OM a dû porter… et un maillot qu'il fallait regarder avec des lunettes 3D. C'est lequel le pire pour toi ? Donne son numéro.

#foot #football #maillot #ligue1 #top #record #HistoiresPasBanales

Classement établi par la rédaction. Sources : Footpack (Auxerre - OM, 2007) ; Topito (votes des internautes, saisons 2012-13 et 2013-14) ; Lyonmag (third orange de l'OL, 2018) ; Footy Headlines, Football Fashion, Football Kit Archive, nss magazine.
Images de match et de présentation : MHSC TV (CC BY), Ligue 1, UEFA, FFF, Canal+, film adidas, rediffusion +sport ; photos de maillots : Football Kit Archive, UK Soccer Shop, Footy Headlines, Football Fashion, Classic Football Shirts ; photos Wikimedia Commons : Akhenaton - Thesupermat, CC BY-SA 4.0 ; frères Lumière - domaine public. Liens dans CREDITS.md. Vidéos Pexels en ouverture et relance : illustrations.
Musique : Sports Highlights - Ahjay Stelino / Mixkit. Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
(p / 'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']) + '\n', encoding='utf8')
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vidéos réelles (YouTube, extraits courts recadrés sans logo de chaîne ni score, son d’origine coupé)',
            'Licence YouTube standard sauf mention, sur choix de Marc de montrer les vraies images en citant les sources.']
credits += [f'- {a} : {b}, {c}' for a, b, c in VIDEOS]
credits += ['', '## Photos des maillots (visuels produit ou officiels, non libres, sources citées ; consigne de Marc du 12 novembre 2026)']
credits += [f'- {a} : {b}, {c}' for a, b, c in PHOTOS]
credits += ['', '## Photos de personnes (Wikimedia Commons)']
credits += [f'- {a} : {b}, {c}' for a, b, c in COMMONS]
credits += ['', '## Illustrations (licence Pexels, sans le son d’origine, aucun maillot du classement)']
credits += [f'- pexels-{k}.mp4 : https://www.pexels.com/video/{k}/' for k in PEXELS]
credits += ['', '## Son',
            '- Sports Highlights - Ahjay Stelino, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
            '- Whoosh des volets : synthèse maison, aucun son tiers.', '- Narration synthétique ElevenLabs.', '',
            'Comparaison de travail uniquement : vidéo HPB des montagnes russes validée (top), à gauche.', '']
(p / 'CREDITS.md').write_text('\n'.join(credits), encoding='utf8')

export = json.loads((m / 'controle-export.json').read_text(encoding='utf8'))
tracks = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream_tags=handler_name',
                                  '-of', 'csv=p=0', str(p / 'comparaison.mp4')], encoding='utf8').strip().splitlines()
assert len(tracks) == 2, tracks
assert (p / 'comparaison.mp4').stat().st_mtime >= (p / 'final.mp4').stat().st_mtime, 'comparaison antérieure au final'
report = dict(
    date=stamp, statut='export à visionner - écoute requise',
    preuves_visuelles=[
        'Repérages : assets/41-maillots-moches/rep/*.jpg et planches par maillot (<clé>/planche.jpg)',
        '117 captures du MP4 habillé (début, milieu, fin de chaque plan) : _montage/controle/final-page-*.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Hook : titre « TOP 10 DES MAILLOTS LES PLUS MOCHES DU FOOT FRANÇAIS » sur un stade plein à 0:00 ; phrase-hameçon « Le numéro un, il fallait des lunettes 3D pour le regarder » de 3,4 à 6,9 s ; 3 plans avant 5 s, dont la spectatrice en lunettes 3D sur le mot « lunettes »',
        'Chaque maillot montré tel qu’il a été porté : vraie séquence de match ou de présentation, et photo du maillot exact, contrôlés à l’image (saison, équipementier, sponsor)',
        'Fun fact « L’OM A JOUÉ AVEC LE MAILLOT D’AUXERRE » de 19,2 à 22,4 s sur les images Canal+ du match où des joueurs de l’OM portent le maillot marron et rose de l’AJA',
        'Photos sur les noms cités : Akhenaton (55,4 s), frères Lumière (72,4 s)',
        'Volet jaune et whoosh à chaque rang ; fin sur la question « Donne son numéro », l’appel à s’abonner et la signature, sur les Lyonnais qui soulèvent la Coupe de France en maillot 3D',
        'Écartés au contrôle : supporters avec une écharpe de Krasnodar (relance), banderole d’un stade turc (fin), plans sombres du clip de Montpellier, entraîneur en costume au début du n°9, gros plan de Pastore (PSG) pendant Évian, homme non identifié dans le film adidas'],
    limites=[
        'Durée 82,6 s : au-dessus de la cible 61-70 s, format top 10 comme les dossiers 38 (86,9 s) et 40.',
        'Images de match en 720p ou en 480p (Auxerre - OM 2007, VHS d’Auxerre - PSG 2006) posées en image entière sur fond flou : plans doux, surtout le PSG en VHS.',
        'Licence YouTube standard pour toutes les vidéos sauf MHSC TV (CC BY) ; photos de maillots non libres (boutiques, archives, sites de maillots), sources citées : risque de son coupé ou de réclamation.',
        'Accroche et relance sur des vidéos Pexels de stades non français, non identifiables à l’écran.',
        'Aucune écoute possible : prononciations (O M, P S G, Akhénaton, Bad Gonnes) et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.'],
    a_revoir_avant_de_poster=[
        'Classement éditorial, assumé dans la légende.',
        'Lyonmag : maillot orange « banni du Virage Nord » par les Bad Gones, relire l’article si contesté.',
        'Maillot réversible de l’OM : source principale Football Fashion (site de passionnés) et film adidas.',
        'Label IA TikTok non requis : vraies images, voix de narrateur qui n’imite personne.'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
print('livraison 41 prête')
