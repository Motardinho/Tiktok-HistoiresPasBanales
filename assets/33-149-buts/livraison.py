"""Livraison du dossier 33 : légende, crédits, contrôle daté, index."""
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/33-149-buts-contre-leur-camp')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

used = []
for x in json.loads((m / 'plans.json').read_text(encoding='utf8')):
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)

legend = """Championnat de Madagascar, 31 octobre 2002 : 149 buts contre leur camp, exprès, pour protester contre l'arbitre. Ce coach : génie ou honte du football ? Réponds en un mot.

#histoirevraie #football #record #madagascar #insolite #HistoiresPasBanales

Sources : Guinness World Records, « Most own goals in a domestic league football match » ; dépêche AP du 3 novembre 2002 (Seattle Times, d'après Midi Madagasikara) ; Wikipédia, « AS Adema 149-0 SO l'Emyrne » ; These Football Times, 11 décembre 2018.

Images d'illustration : aucune ne montre le match de 2002, les deux clubs ni les personnes citées. Vidéos Pexels (licence Pexels), recadrées et montées sans le son d'origine.
Musique : Sports Highlights - Ahjay Stelino / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
(p / 'script.txt').write_text('\n'.join(s['narration'] for s in d['scenes']) + '\n', encoding='utf8')
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vidéos utilisées (illustrations)']
for k in used:
    credits.append(f'- {k}.mp4 : Pexels, licence Pexels, https://www.pexels.com/video/{k[7:]}/')
credits += [
    '',
    'Aucune image ne montre le match AS Adema - SO de l’Emyrne du 31 octobre 2002, les deux clubs, l’entraîneur ni l’arbitre : plans génériques Pexels.',
    'Écartés au contrôle : 2 sources en 720p, 2 sources horizontales 1080p, 1 source HDR, tir devant des panneaux publicitaires (12689679), supporters aux maillots et drapeau du Maroc avec nom de joueur lisible (34452575, 34452568), ballon à marque lisible (37568235), plans de joueuses.',
    '', '## Son',
    '- Sports Highlights - Ahjay Stelino, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
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
        'Catalogues de repérage : assets/33-149-buts/cat-00..03.jpg, strips-0..1.jpg, s-arbitre.jpg, s-5.jpg',
        '132 captures du MP4 habillé (début, milieu, fin des 44 plans) : _montage/controle/final-page-0..10.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Sujet choisi par Marc le 11/11/2026 ; script non relu par lui avant la voix',
        'Hook : titre « ILS ONT MARQUÉ 149 BUTS CONTRE LEUR CAMP » sur une frappe face au gardien à 0:00 ; « Exprès. » prononcé à 2,96 s, « Et en face, personne n’a bougé » fini vers 5,8 s ; 4 plans avant 5 s',
        'Fun fact « 1 BUT TOUTES LES 36 SECONDES » 34,2-38,5 s, encart en haut, sous-titres maintenus',
        'Corrections après contrôle : hook redécoupé (but vide trop long), tir devant des panneaux publicitaires remplacé, cadre presque vide remplacé par le gardien immobile, supporters marocains remplacés, bandeau Madagascar raccourci',
        'Révision demandée par Marc le 11/11/2026 (« on ne sait pas quelle est la compétition ») : « octobre 2002, phase finale du championnat national » et « dernière journée » dits à l’oral, bandeaux « CHAMPIONNAT NATIONAL » et « DERNIÈRE JOURNÉE », bandeau de série « FOOT - MADAGASCAR 2002 » ; phrase sur le record de 1885, « Et encore » et « Pendant tout le match » retirés pour tenir la durée',
        'Sources en vertical natif ≥ 1080×1920 ou 4K horizontal, BT.709'],
    limites=[
        'Aucune écoute possible : voix, musique et mix non validés à l’oreille (prononciation de « L’Émirne » et « l’Adéma » à écouter).',
        'Contrôle par captures, pas de visionnage continu.',
        'Plans d’arbitre (pexels-40551621) : banderole publicitaire avec « 1978 » et un logo visibles en arrière-plan ; même source que la vidéo 30.',
        'Beaucoup de plans tournés dans la même salle couverte européenne : aucun plan libre de football à Madagascar.',
        'Lémurs catta pour situer Madagascar : lieu de tournage non précisé par Pexels (peut-être un parc).',
        'Aucun plan libre de guichet de stade : « foncent aux guichets » illustré par une tribune debout puis un stade.',
        'Entraîneur et joueurs identifiables dans le plan du coach (figurants Pexels), marque de l’équipementier visible sur les maillots.',
        'Trophée avec un « 20 » décoratif.'],
    a_revoir_avant_de_poster=[
        'Ville du match non dite (Toamasina ou Antananarivo selon les sources).',
        '« Dernière journée » : déduit du déroulé de la poule finale (six journées, l’Adema sacré à une journée de la fin) d’après Wikipédia.',
        'Rôle du coach : attribué à la presse locale à l’oral. Trois ans de suspension : Wikipédia et These Football Times, article du Guardian non consulté.'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 33]
data.append(dict(numero=33, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : compétition située (championnat national, dernière journée)',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

print('ok', used)
