"""Fichiers de livraison des dossiers 21 à 23 : script, crédits, légende, contrôle daté, index."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOT = {
    21: dict(assets='langues',
             accroche='Top 3 des langues les plus parlées. Tu en parles combien ?',
             tags='#histoirevraie #langues #culturegenerale #top3 #HistoiresPasBanales #record',
             sources=['Ethnologue, 29e édition, 2026, total de locuteurs (langue maternelle et seconde langue) : https://www.ethnologue.com/insights/ethnologue200/',
                      'Anglais parlé dans 188 pays : https://www.ethnologue.com/insights/most-spoken-language/',
                      'Écriture devanagari : https://fr.wikipedia.org/wiki/Devanagari'],
             revoir=['Ethnologue 2026 : anglais 1,5 milliard, mandarin 1,2 milliard, hindi 611,2 millions.',
                     '« 3 locuteurs de l’anglais sur 4 non natifs » et « plus de 8 000 caractères » viennent de sources secondaires (Wikipédia citant Ethnologue et la liste officielle chinoise de 2013).',
                     'Les plans de foule de l’accroche et de la relance sont tournés à Tokyo (Shibuya) : ils n’illustrent aucune des trois langues.']),
    22: dict(assets='riches',
             accroche='Top 3 des pays les plus riches. Tu avais le numéro 1 ?',
             tags='#histoirevraie #pays #argent #top3 #HistoiresPasBanales #record',
             sources=['FMI, World Economic Outlook, octobre 2026, PIB par habitant en dollars courants, estimations 2026 : https://www.imf.org/external/datamapper/NGDPDPC@WEO/LIE/LUX/IRL/CHE',
                      'Irlande, PIB et revenu national corrigé (GNI*) : https://www.cso.ie',
                      'Luxembourg, transports publics gratuits depuis le 1er mars 2020 : https://gouvernement.lu',
                      'Liechtenstein, emplois et population : https://www.statistikportal.li'],
             revoir=['FMI, octobre 2026 : les valeurs 2026 sont des estimations. Irlande 127 837 $ et Suisse 124 478 $ : une révision peut inverser la 3e place.',
                     'Monaco n’est pas dans la base du FMI : le classement vaut « selon le FMI ». Commentaire probable.',
                     'Les pages sources des fun facts (gouvernement.lu, cso.ie, statistikportal.li) ont été lues par un agent de recherche : à rouvrir avant de poster.']),
    23: dict(assets='gratte-ciel',
             accroche='Top 3 des gratte-ciel les plus hauts. Tu monterais tout en haut ?',
             tags='#histoirevraie #gratteciel #architecture #top3 #HistoiresPasBanales #record',
             sources=['CTBUH, Skyscraper Center, bâtiments achevés, hauteur architecturale, lu le 9 novembre 2026 : https://www.skyscrapercenter.com/buildings',
                      'Ramadan au Burj Khalifa, The National, 8 août 2011 : https://www.thenationalnews.com/uae/fatwa-means-late-iftar-on-top-burj-khalifa-floors-1.432286'],
             revoir=['CTBUH : Burj Khalifa 828 m, Merdeka 118 678,9 m, Shanghai Tower 632 m. La Jeddah Tower est en chantier, non classée.',
                     'Merdeka 118 s’appelle officiellement Menara Merdeka Maybank depuis le 28 juillet 2026 ; la vidéo garde le nom courant.',
                     'L’ascenseur de la Shanghai Tower a eu le record en 2016 (20,5 m/s) ; il l’a perdu en 2019. La narration dit bien « en 2016 ».',
                     'Le dernier plan montre Dubaï de très haut ; la légende de la source ne confirme pas que la vue est prise du Burj Khalifa.']),
    15: dict(assets='../refonte-14-20/bouchons',
             accroche='Top 3 des villes les plus embouteillées. Raconte ta pire expérience de bouchon en commentaire.',
             tags='#histoirevraie #bouchons #trafic #top3 #HistoiresPasBanales #record',
             sources=['INRIX 2025 Global Traffic Scorecard (publié le 1er décembre 2025), heures perdues par conducteur en 2025 : https://inrix.com/scorecard/',
                      'Mexico, programme « Hoy No Circula » (depuis 1989) : L. Davis, Journal of Political Economy, 2008'],
             revoir=['INRIX 2025 : Istanbul 118 h, Chicago 112 h, Mexico 108 h, classés par heures perdues. Le rang officiel INRIX met Mexico 2e et Chicago 3e : la vidéo dit bien « le classement, ce sont les heures perdues ».',
                     'La prochaine édition INRIX sort probablement début décembre 2026 : revérifier avant de poster.',
                     'Chicago 14 km/h (9 mph) au centre-ville aux heures de pointe : rapport INRIX p. 15. « Hoy No Circula » : chiffres lus dans des résumés, pas dans l’étude Davis (2008).']),
    18: dict(assets='../refonte-14-20/pays',
             accroche='Top 3 des plus grands pays du monde. Ton score sur 3 en commentaire ?',
             tags='#histoirevraie #geographie #pays #top3 #HistoiresPasBanales #record',
             sources=['Nations unies, Demographic Yearbook 2024, tableau 3 (superficie totale) : https://unstats.un.org/unsd/demographic-social/products/dyb/',
                      'US Census Bureau, eaux côtières et territoriales : https://www.census.gov/geographies/reference-files/2010/geo/state-area.html',
                      'Gouvernement du Canada, littoral : https://www.canada.ca/en/services/environment/our-environment/nature-based-climate-solutions/coastlines.html',
                      'Lacs du Canada : Messager et al., Nature Communications, 2016'],
             revoir=['ONU DYB 2024 : Russie 17 098 246 km², Canada 9 984 670 km², États-Unis 9 833 517 km² (eaux côtières et territoriales comprises), Chine 9 600 000 km². Commentaire probable : « la Chine est plus grande que les États-Unis » ; la vidéo le dit elle-même en fun fact.',
                     '« Plus de la moitié des lacs de la planète » : 62 % des lacs de plus de 10 ha, lu via le communiqué de McGill, pas l’article.',
                     'Le Caucase et Moscou illustrent la Russie ; aucun plan de Sibérie.']),
    14: dict(assets='../sources-reelles', sources_fichiers='sources-voitures-officielles',
             accroche='Top 3 des voitures les plus rapides. Tu choisis laquelle ?',
             tags='#histoirevraie #voitures #byd #bugatti #top3 #HistoiresPasBanales #record',
             sources=['FIA, 6 novembre 2026, et communiqué BYD : Yangwang U9 Xtreme, 503,17 km/h le 1er novembre 2026',
                      'Bugatti : Chiron Super Sport 300+, 490,484 km/h, 2019',
                      'SSC North America : Tuatara, 295 mph (474,8 km/h), 14 mai 2022, Kennedy Space Center'],
             revoir=['Record Yangwang très récent (1er novembre 2026, publié par la FIA le 6) : revérifier le jour du post.',
                     'Les trois vitesses sont des pointes dans un seul sens ; si un commentaire parle de moyenne aller-retour, répondre en commentaire épinglé.',
                     'Images : vidéos officielles de Bugatti, SSC North America, VBOX Motorsport et BYD, sous licence YouTube standard (pas de licence de réutilisation), gardées sur décision de Marc du 10 novembre 2026.']),
    16: dict(assets='../refonte-14-20/armees',
             accroche='Top 3 des armées les plus puissantes. Tu aurais mis qui en premier ?',
             tags='#histoirevraie #armee #puissance #top3 #HistoiresPasBanales #record',
             sources=['Global Firepower 2026 : https://www.globalfirepower.com/countries-listing.php',
                      'SIPRI, dépenses militaires 2025 (avril 2026) et SIPRI Yearbook 2026 (ogives) : https://www.sipri.org',
                      'Énergie de la bombe d’Hiroshima, environ 15 kt : Los Alamos National Laboratory',
                      'Boulangerie du USS Ronald Reagan : U.S. Navy / DVIDS'],
             revoir=['GFP 2026 : 1 États-Unis, 2 Russie, 3 Chine. SIPRI 2025 : États-Unis 954 Md$, Chine 336 Md$ (estimation), Russie 190 Md$. Ogives (SIPRI 2026, estimations) : Russie 4 400, États-Unis 3 700, Chine 620.',
                     'Le repère « 300 kt, environ 20 fois Hiroshima » porte sur l’ogive américaine W87 du Minuteman III, et c’est bien dans l’entrée États-Unis qu’il est dit.',
                     'Photo d’Hiroshima 1945 (U.S. Navy, NARA 80-G-373265) : seule photo de la vidéo, à ta demande.',
                     'Les plans du Ford et du Spruance viennent d’une opération de combat réelle de 2026 ; le Ronald Reagan est en grand entretien depuis 2025.']),
    20: dict(assets='../refonte-14-20/telephone',
             accroche='Top 3 des téléphones les plus chers. Tu mettrais ce prix dans un téléphone ?',
             tags='#histoirevraie #iphone #samsung #smartphone #top3 #HistoiresPasBanales #record',
             sources=['Prix publics TTC en France, version la plus chère, relevés le 10 novembre 2026 : apple.com/fr (iPhone Duo, iPhone 18 Pro Max) ; Boulanger et LDLC (Galaxy Z Fold8 Ultra)',
                      'Fiches techniques : apple.com/fr et samsung.com/fr'],
             revoir=['Prix relevés le 10 novembre 2026 : iPhone Duo 2 To 3 839 €, iPhone 18 Pro Max 2 To 3 129 €, Galaxy Z Fold8 Ultra 1 To 2 799 €. Les revérifier le jour du post (promotions, Black Friday).',
                     'Le prix français du Fold8 Ultra vient de Boulanger, LDLC et la presse : samsung.com/fr n’a pas pu être lu. SMIC net (1 477,93 €) et épaisseur de la pièce de 2 € : extraits de recherche.',
                     'Règle du classement : un modèle par gamme. En comptant l’iPhone 18 Pro (2 979 €) à part, le podium serait 100 % Apple ; le Huawei Mate XT, non vendu officiellement en France, n’est pas classé. Commentaires probables.',
                     'Identification du 18 Pro Max et du Fold8 Ultra par le titre et la description des vidéos du testeur, pas par l’image.']),
    17: dict(assets='../refonte-14-20/animaux',
             accroche='Top 3 des animaux les plus rapides du monde. Tu aurais misé sur le guépard ?',
             tags='#histoirevraie #animaux #vitesse #faucon #top3 #HistoiresPasBanales #record',
             sources=['Gerfaut : Tucker, Cade & Tucker, Journal of Experimental Biology, 1998',
                      'Pèlerin : piqués de Frightful avec Ken Franklin (1999), National Geographic « Terminal Velocity » ; Guinness World Records',
                      'Guépard : Wilson et al., Nature, 2013'],
             revoir=['Critère : vitesse de pointe, piqué compris. L’aigle royal (320 km/h) est une estimation de 1968 jamais chronométrée ; en ne gardant que des mesures, le gerfaut passerait devant. La vidéo le dit (« une estimation »).',
                     'Les 389 km/h du pèlerin sont « rapportés » (altimètre de parachutiste, non publié) : la voix dit « elle aurait atteint ». Guinness retient 320 km/h.',
                     'Aucun piqué vertical n’est filmé sous licence libre : le pèlerin fond sur un drone (Australie), l’aigle royal plane. Les plans de gerfaut sont en 576p, oiseau au sol.']),
}
OFFICIELLES = [
    dict(fichier='ssc-tuatara.mp4', auteur='SSC North America', titre='SSC Tuatara, record 2022', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/@SSCNorthAmerica'),
    dict(fichier='ssc-road.mp4', auteur='SSC North America', titre='SSC Tuatara', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/@SSCNorthAmerica'),
    dict(fichier='ssc-speed.mp4', auteur='SSC North America', titre='SSC Tuatara', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/@SSCNorthAmerica'),
    dict(fichier='ssc-vbox-2022.mp4', auteur='VBOX Motorsport', titre='Télémétrie SSC Tuatara 2022', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/watch?v=IgXuBBe017Q'),
    dict(fichier='bugatti-record.mp4', auteur='Bugatti', titre='Chiron Super Sport 300+, record 2019', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/@bugatti'),
    dict(fichier='yangwang-u9-xtreme-2025.mp4', auteur='BYD', titre='Yangwang U9 Xtreme, record 2025', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/@BYDGlobal'),
    dict(fichier='yangwang-u9-xtreme-2026.mp4', auteur='BYD', titre='Yangwang U9 Xtreme, record Abou Dhabi 2026', licence='Licence YouTube standard', url_licence='', url_page='https://www.youtube.com/@BYDGlobal'),
]
import sys
if len(sys.argv) > 1:
    LOT = {n: LOT[n] for n in map(int, sys.argv[1:])}


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def probe(p, kind):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', f'{kind}:0', '-show_entries',
                                          'stream=duration', '-of', 'csv=p=0', str(p)]).strip())


rows = []
for n, lot in LOT.items():
    w = next((ROOT / 'out').glob(f'{n}-*'))
    m = w / '_montage'
    story = read(w / 'histoire.json')
    used = {Path(p['source']).name for p in read(m / 'plans.json')}
    pool = OFFICIELLES if lot.get('sources_fichiers') else read(ROOT / 'assets/lot-21-23' / lot['assets'] / 'sources.json')
    sources = [s for s in pool if Path(s['fichier']).name in used]
    missing = used - {Path(s['fichier']).name for s in sources}
    assert not missing, (n, missing)
    (w / 'script.txt').write_text('\n'.join(s['narration'] for s in story['scenes']) + '\n', encoding='utf-8')
    music = next(x for x in read(ROOT / 'assets/musique/mixkit/sources.json') if x['slug'] == story['musique'])
    # Un crédit par auteur et par plateforme (la liste détaillée avec les liens est dans CREDITS.md),
    # pour rester sous la limite de longueur des légendes TikTok.
    def platform(url):
        return ('Wikimedia Commons' if 'wikimedia' in url else 'Pexels' if 'pexels' in url else 'Mixkit' if 'mixkit' in url
                else 'YouTube' if 'youtu' in url else url.split('/')[2] if '//' in url else url)
    groups = {}
    for s in sources:
        author = s['auteur'].split(' (')[0].split(' - ')[0]
        key = (author, platform(s['url_page']))
        groups.setdefault(key, set()).add(s['licence'].split(' (')[0].replace(' - US Navy', '').replace(' - US Army', '')
                                          .replace(' - US Air Force', '').replace(' - US Space Force', ''))
    credits = []
    for (author, where), licences_set in groups.items():
        if licences_set == {'Licence YouTube standard'}:
            credits.append(f'Images : {author} ({where})')
        else:
            credits.append(f"{author} - {' / '.join(sorted(licences_set))} - {where}")
    licences = sorted({s['url_licence'] for s in sources if s.get('url_licence')})
    sound = f"Musique : {music['title']} - {music['artist']} / Mixkit, {music['license_url']} . Voix synthétique ElevenLabs."
    caption = '\n'.join([lot['accroche'], '', lot['tags'], '', 'Sources :', *lot['sources'], '', 'Crédits vidéo :', *credits,
                         'Extraits recadrés et montés, sans le son d’origine.' + (' Licences : ' + ' ; '.join(licences) + ' .' if licences else ''), sound, ''])
    (w / 'legende.txt').write_text(caption, encoding='utf-8')
    (w / 'publication.txt').write_text(caption, encoding='utf-8')
    (w / 'CREDITS.md').write_text('\n'.join(
        ['# Sources et crédits', '', '## Faits', *[f'- {x}' for x in story['sources_a_verifier']], '', '## Vidéos utilisées',
         *[f"- {Path(s['fichier']).name} : {s['auteur']}, « {s['titre']} », {s['licence']}, {s['url_page']}" for s in sources],
         '', '## Son', f"- {music['title']} - {music['artist']}, {music['license']}. {music['license_url']}",
         '- Narration synthétique ElevenLabs, voix Hugo.', '',
         'La référence TikTok apparaît seulement dans la comparaison locale de travail.', story['reference'], '']), encoding='utf-8')
    final, comparison = w / 'final.mp4', w / 'comparaison.mp4'
    assert comparison.stat().st_mtime >= final.stat().st_mtime, 'comparaison antérieure au final'
    video, audio = probe(final, 'v'), probe(final, 'a')
    assert video > 60
    tracks = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries',
                                      'stream_tags=handler_name', '-of', 'csv=p=0', str(comparison)], encoding='utf-8').split('\n')
    tracks = [t.strip() for t in tracks if t.strip()]
    assert len(tracks) == 2, tracks
    sheets = sorted(p.name for p in m.glob('controle-plans-*.jpg'))
    json.dump(dict(
        date=__import__('datetime').date.today().isoformat(), export=hashlib.sha256(final.read_bytes()).hexdigest(), duree_video=video, duree_audio=audio,
        decodage_integral=True, format='1080 x 1920, plans réels recadrés plein écran',
        verification_visuelle=[f'_montage/{s}' for s in sheets] + ['apercu-tiktok.jpg'],
        examine='Début, milieu et fin de chaque plan avec habillage (planches), première image à 0:00, fun fact, fin, aperçu simulé du lecteur à 360 px. Pas d’écoute : titre oral, rangs et chiffres contrôlés sur l’alignement des mots renvoyé par ElevenLabs.',
        comparaison_a_jour=True, pistes_comparaison=tracks, a_revoir_avant_de_poster=lot['revoir']),
        (m / 'controle-livraison.json').open('w', encoding='utf-8'), ensure_ascii=False, indent=2)
    rows.append((n, story['titre_fixe'], video, w))

refonte = all(n < 21 for n, *_ in rows)
if refonte:
    # Index cumulatif de la refonte : toutes les vidéos 14-20 déjà refaites.
    rows = [(n, read(w / 'histoire.json')['titre_fixe'], probe(w / 'final.mp4', 'v'), w)
            for n in range(14, 21) for w in [next((ROOT / 'out').glob(f'{n}-*'))]
            if (w / '_ancienne-version').is_dir() and (w / 'legende.txt').exists()]
title_md = '# Refonte des vidéos 14 à 20' if refonte else '# Vidéos 21 à 23'
intro = ('Script, voix, plans et montage refaits. Anciennes versions dans `_ancienne-version/` de chaque dossier. Exports de travail, non validés par Marc.'
         if refonte else 'Trois tops en portrait plein écran, plans réels, voix Hugo. Exports de travail, non validés par Marc.')
lines = [title_md, '', intro, '',
         '| N° | Sujet | Durée | Vidéo | Comparaison | Aperçu | Légende |', '|---|---|---:|---|---|---|---|']
for n, title, video, w in rows:
    base = '</' + w.as_posix()
    lines.append(f'| {n} | {title} | {video:.1f} s | [Vidéo]({base}/final.mp4>) | [Comparer]({base}/comparaison.mp4>) | '
                 f'[Voir]({base}/apercu-tiktok.jpg>) | [Texte]({base}/legende.txt>) |')
lines += ['', 'Comparaisons avec les tops correspondants de @faiseemoc84 (URL dans chaque `histoire.json`).',
          'Points à revérifier avant de poster : `_montage/controle-livraison.json` de chaque dossier.', '']
(ROOT / ('out/LIVRAISON-REFONTE-14-20.md' if refonte else 'out/LIVRAISON-21-23.md')).write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(f'{n} {video:.2f}s' for n, _, video, _ in rows))
