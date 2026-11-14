"""Livraison du dossier 43 : aperçu, légende, crédits, contrôle daté, index.
Lancer depuis la racine du projet : python assets/43-motos-serie/livraison.py
"""
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/43-top-3-motos-plus-rapides')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

# Aperçu simulé du lecteur : script du dossier 25, lignes de légende adaptées.
apercu = Path('assets/25-montagnes-russes/apercu.py').read_text(encoding='utf8')
old = "['Top 3 des montagnes russes les plus rapides.', 'Tu monterais dans laquelle ?', '#histoirevraie #montagnesrusses #record']"
new = "['Top 3 des motos de série les plus rapides.', '58 000 euros, interdite sur la route :', 'tu signes ? #histoirevraie #moto #record']"
assert old in apercu
Path('assets/43-motos-serie/apercu.py').write_text(apercu.replace(old, new), encoding='utf8')
subprocess.run([sys.executable, 'assets/43-motos-serie/apercu.py', '43'], check=True)

SRC = {
    'vVN9zcxxNhk': ('BMW Motorrad', 'The new BMW M 1000 RR and BMW S 1000 RR | #NeverStopChallenging', '2024', '4K'),
    '1p2Q2eJtIbQ': ('BMW Motorrad', 'CLOSE LOOK - The new M 1000 RR', '2024', '4K'),
    'w_1lcMyWqMU': ('Ducati', 'New Panigale V4 R | Racing is just the beginning', '2025', '4K'),
    'j8VJXb2LoMM': ('Kawasaki', '2015 Ninja H2R Promotion Video', '2014', '1080p'),
    '6_n7ru1e-rg': ('Den ProHD', 'Kawasaki H2R - World Record 400 km/h in 26 sec. HD', '2016', '1080p'),
    'ALFEZNDyWZs': ('Türkiye Motosiklet Federasyonu', 'Kenan Sofuoğlu 400 km’lik Hız - Kawasaki H2R World Speed Record', '2019', '1080p'),
}
plans = json.loads((m / 'plans.json').read_text(encoding='utf8'))
used = []
for x in plans:
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)
assert set(used) <= set(SRC), set(used) - set(SRC)
videos = ' ; '.join(f'{SRC[k][0]}, « {SRC[k][1]} » ({SRC[k][2]}) https://www.youtube.com/watch?v={k}' for k in used)

legend = f"""Top 3 des motos de série les plus rapides. 58 000 euros pour une moto interdite sur la route : tu signes ? Réponds oui ou non.

#histoirevraie #moto #record #kawasaki #ducati #bmw #HistoiresPasBanales

Sources (motos de série en vente, relevé du 12 novembre 2026) :
BMW M 1000 RR : 314 km/h, plus haute vitesse homologuée d’une moto de série 2026 (Bennetts BikeSocial, 5 mai 2026), à partir de 37 000 € en France
Ducati Panigale V4 R : 330,6 km/h avec le kit course, 318,4 km/h de série, chiffres annoncés par Ducati ; 43 990 €
Kawasaki Ninja H2R : 400 km/h en 26 s lus au compteur, Kenan Sofuoglu, pont Osman Gazi (Turquie), 30 juin 2016, vitesse non officielle ; 310 ch, réservée au circuit, 58 000 € en France
Accord des 300 km/h entre constructeurs depuis les modèles 2000 : Wikipedia, « List of fastest production motorcycles » ; Bennetts BikeSocial

Séquences réelles, extraits courts recadrés, son d’origine coupé, droits de leurs auteurs : {videos}
Musique : Sports Highlights - Ahjay Stelino / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits', *[f'- {x}' for x in d['sources_a_verifier']], '',
           '## Vidéos utilisées (licence YouTube standard, sans autorisation)']
for k in used:
    au, ti, an, res = SRC[k]
    credits.append(f'- {k}.mp4 : {au}, « {ti} » ({an}), {res}, https://www.youtube.com/watch?v={k}')
credits += ['', '## Plans (source, entrée en secondes, sujet)']
credits += [f"- {Path(x['source']).stem} à {x['entree']} s : {x['note']}" for x in plans]
credits += [
    '',
    'Toutes sources admises, citées en légende (règle de Marc du 12 novembre 2026). Risque droits d’auteur : vidéos officielles BMW, Ducati et Kawasaki.',
    'Sources 1080p (record de 2016 et film Kawasaki de 2014) recadrées en plein écran : environ 607 px utiles, image plus douce que les plans 4K.',
    'Le film BMW montre aussi la S 1000 RR : seuls les plans des M 1000 RR n°54 (noire) et n°60 (blanche) sont utilisés.',
    '', '## Son',
    '- Sports Highlights - Ahjay Stelino, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
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
        'Planches de repérage des sources : assets/43-motos-serie/reperage-*.jpg et fin-*.jpg',
        '69 captures du MP4 habillé (début, milieu, fin des 23 plans) : _montage/controle/final-page-0..5.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Image 0:00 : M 1000 RR sur l’angle, titre seul, aucun nom ni rang ; deux plans avant 5 s ; phrase-hameçon finie à 4,9 s',
        'Déroulé 3 - 2 - 1 avec bandeaux de rang et volets jaunes ; relance « 70 KM/H de plus » avant le N°1',
        'Fun fact 15,25-24,08 s, encart en haut, sans contact avec les sous-titres',
        'Visage de Kenan Sofuoglu (interview sur le pont, jour du record) sur son nom',
        'Compteur du record : « 400 » lisible, « km/h » en bord de cadre ; les sous-titres mordent sur le bas des chiffres',
        'Logo et bandeau de série présents sur toutes les captures'],
    limites=[
        'Aucune écoute possible : prononciation des noms (BMW M 1000 RR, Ducati Panigale V4 R, H2R, Sofuoglu), mix et rythme non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Plans Kawasaki en 1080p recadrés : plus doux que les plans BMW et Ducati en 4K.',
        'Sous-titres sur 4 lignes par moments (noms longs).'],
    a_revoir_avant_de_poster=[
        'Prix : BMW 37 000 €, Ducati 43 990 € (« près de 44 000 »), H2R 58 000 € (fiches de concession, pas de grille officielle Kawasaki France trouvée).',
        '400 km/h : lu au compteur, non officiel ; Kawasaki annonce 380 km/h. Commentaire probable.',
        'Ducati : 330,6 km/h avec kit course (non homologué route), 299 km/h à l’homologation.',
        'Lightning LS-218 électrique (environ 350 km/h, moto modifiée) : écartée, commentaire probable.',
        'Droits d’auteur : vidéos officielles BMW, Ducati, Kawasaki et films du record, licence YouTube standard.'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 43]
data.append(dict(numero=43, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, top 3 des motos de série',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

md = Path('out/INDEX.md')
t = md.read_text(encoding='utf8')
row = '| 43 | [Top 3 des motos de série les plus rapides](43-top-3-motos-plus-rapides/) | Export de travail, à valider |'
if '| 43 |' not in t:
    anchor = next(line for line in t.splitlines() if line.startswith('| 42 |'))
    md.write_text(t.replace(anchor, anchor + '\n' + row), encoding='utf8')
print('ok', used, export['duree_video'])
