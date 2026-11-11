"""Livraison du dossier 25 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/25-montagnes-russes-plus-rapides')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()
SRC = {
    'ZSrHdILQkpc': ("Keg's Coasters", 'Top Thrill 2 (TT2) at Cedar Point 2026-07-07', 'CC BY 3.0'),
    'gW19l3OMbbE': ('Canobie Coaster', 'Top Thrill 2 Off-Ride Footage (60FPS, 2025)', 'CC BY 3.0'),
    'Bg7GV5m8cd0': ('Canobie Coaster', 'Formula Rossa Off-Ride Footage (60FPS)', 'CC BY 3.0'),
    'PED5EcH6mRU': ('Coaster Wave', 'Riding The FASTEST Roller Coaster In The World!', 'CC BY 3.0'),
    'K2AiJrgOp_k': ('Shamu Express Hearts Club Band', 'Formula Rossa at Ferrari World 2011', 'CC BY 3.0'),
    'ijuQwnfBBZw': ('Motor1', "Ferrari's Alonso and Massa ride world's fastest rollercoaster at Ferrari World (2010)", 'CC BY 3.0'),
    'cUURkqyn4Zs': ('CoasterForce (filmé par Upstop Media)', "Falcon's Flight front seat on-ride 4K POV", 'Licence YouTube standard'),
    'Q7Atm5C15zg': ('CoasterForce (filmé par Upstop Media)', 'Falcons Flight nighttime front seat on-ride 4K POV', 'Licence YouTube standard'),
}
used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)
assert set(used) <= set(SRC), set(used) - set(SRC)

legend = """Top 3 des montagnes russes les plus rapides. Tu monterais dans laquelle ?

#histoirevraie #montagnesrusses #parcdattractions #top3 #HistoiresPasBanales #record

Sources (vitesses maximales, relevées le 11 novembre 2026) :
Falcons Flight, Six Flags Qiddiya City : 250 km/h, ouverte le 31 décembre 2025 (Wikipedia, RCDB)
Formula Rossa, Ferrari World Abu Dhabi : 240 km/h, record du monde de 2010 à 2025, lunettes de protection obligatoires (Wikipedia)
Top Thrill 2, Cedar Point : 193 km/h (120 mph), 130 m (Wikipedia)

Crédits vidéo :
CC BY 3.0 (YouTube) : Keg's Coasters, Canobie Coaster, Coaster Wave, Shamu Express Hearts Club Band, Motor1
Images : CoasterForce / Upstop Media (YouTube)
Extraits recadrés et montés, sans le son d’origine. Licence : https://creativecommons.org/licenses/by/3.0/legalcode .
Musique : Sports Highlights - Ahjay Stelino / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits', *[f'- {x}' for x in d['sources_a_verifier']], '', '## Vidéos utilisées']
for k in used:
    au, ti, li = SRC[k]
    credits.append(f'- {k}.mp4 : {au}, « {ti} », {li}, https://www.youtube.com/watch?v={k}')
credits += [
    '',
    'Falcons Flight : vues CoasterForce en licence YouTube standard, sans autorisation, choisies par Marc le 11 novembre 2026 '
    '(« 4K de passionné ») plutôt que la vue officielle du parc republiée en 480p sous un CC BY douteux (ArLcFx6ws7k, Coaster Actus). '
    'Le filigrane CF sort du cadre au recadrage vertical ; il n’a pas été effacé.',
    'Les deux pilotes Ferrari ne sont pas désignés individuellement à l’image.',
    '', '## Son',
    '- Sports Highlights - Ahjay Stelino, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
    '- Narration synthétique ElevenLabs (modèle eleven_v4).', '',
    'Comparaison de travail uniquement : vidéo HPB des téléphones validée, à gauche. Repérage : assets/25-montagnes-russes/reperage.md.', '',
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
        'Planches de repérage des sources : assets/25-montagnes-russes/reperage-*.jpg et fin/',
        '75 captures du MP4 habillé (début, milieu, fin des 25 plans) : _montage/controle/final-page-0..6.jpg',
        'Image 0:00 et plan 09 corrigé : _montage/controle/image-0.jpg, plan09-verif.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Titre seul pendant l’annonce orale, puis sous-titres ; aucun nom ni rang sur l’image 0:00 (vue plongeante depuis Top Thrill 2)',
        'Déroulé 3 - 2 - 1 avec bandeaux de rang ; relance « 10 KM/H plus vite » avant le N°1',
        'Fun fact Formula Rossa 29,68-39,32 s : encart descendu à y = 760-980 pour ne pas cacher les visages (lunettes visibles) ; sous-titres de 3 lignes au plus, sans contact',
        'Plongée verticale dans le tunnel visible sur le mot « tunnel » (61 s)',
        'Corrections après contrôle : enseigne Formula Rossa coupée remplacée par le train en gare ; plans du fun fact rechoisis (visages auparavant sous l’encart)',
        'Logo et bandeau de série présents sur toutes les captures'],
    limites=[
        'Aucune écoute possible : noms étrangers écrits en phonétique française pour la voix (Top Trile, Cédar Poïnte, Ferrari Weurld, Félipé, Falkonz Flaïte, demande de Marc du 11 nov.), rendu de l’accent, mix et rythme non validés à l’oreille. Voix précédente (accent anglais) : _montage/voix-accent-anglais/.',
        'Contrôle par captures, pas de visionnage continu.',
        'Encart de fun fact plus bas que la règle « encart en haut » : exception pour cette vidéo, à valider par Marc.'],
    a_revoir_avant_de_poster=[
        'Formula Rossa fermée « pour maintenance » depuis le 12 mai 2026 selon Wikipedia : le classement porte sur la vitesse, commentaire probable.',
        'Falcons Flight : 250 km/h (fiche) ou 249 km/h (texte), 155 mph dans les deux cas.',
        'Kingda Ka (206 km/h) démolie : non classée. Si un commentaire la cite, répondre qu’elle n’existe plus.',
        'Images Falcons Flight en licence YouTube standard (CoasterForce), sans autorisation.'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 25]
data.append(dict(numero=25, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : nouvelle vidéo, référence qualité téléphones validée',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

md = Path('out/INDEX.md')
t = md.read_text(encoding='utf8')
row23 = '| 23 | [Gratte-ciel les plus hauts](23-gratte-ciel-plus-hauts/) | Export de travail, à valider |'
add = ''
if '| 24 |' not in t:
    add += '\n| 24 | [Pourquoi inonder une fusée ?](24-deluge-fusees/) | Validée le 11 nov. (`version-validee/`) |'
if '| 25 |' not in t:
    add += '\n| 25 | [Montagnes russes les plus rapides](25-montagnes-russes-plus-rapides/) | Export de travail, à valider |'
md.write_text(t.replace(row23, row23 + add), encoding='utf8')
print('ok', used)
