"""Livraison du dossier 39 : légende, crédits, contrôle daté, index."""
import importlib.util
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

p = Path('out/39-l-entraineur-boycotte-dans-tout-le-pays')
m = p / '_montage'
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat()

plans = json.loads((m / 'plans.json').read_text(encoding='utf8'))
used = []
for x in plans:
    k = Path(x['source']).stem
    if k not in used:
        used.append(k)
photos_used = {k[len('photo-'):] for k in used if k.startswith('photo-')}

legend = """Juin 2026 : la Corée du Sud sort au 1er tour du Mondial. Son sélectionneur, capitaine légendaire de 2002, se retrouve interdit d'entrée dans des bars, des restos et des supérettes de son propre pays. Hong Myung-bo : bouc émissaire ou vrai coupable ? Réponds en un mot.

#histoirevraie #football #coupedumonde2026 #coreedusud #scandale #HistoiresPasBanales

Sources : Korea JoongAng Daily (28 juin au 1er juillet 2026 : défaite contre l'Afrique du Sud, démission, panneaux « interdit d'entrée », menaces, retour à Incheon, réaction du président), The Telegraph (30 juin 2026), RMC Sport (29 juin 2026), CBS News (Mexique-Corée du Sud, 18 juin 2026), ministère sud-coréen des Sports sur le recrutement de 2024. Caramels lancés en 2014 : Associated Press, juillet 2014.

Images : FIFA (YouTube) - résumés Corée du Sud-Tchéquie, Mexique-Corée du Sud et Afrique du Sud-Corée du Sud du Mondial 2026, séance de tirs au but Espagne-Corée du Sud 2002 ; KBS WORLD News, « Hong Myung-bo resigns as head coach », 29 juin 2026 ; Arirang News, « Hong Myung-bo resigns as S. Korea national team manager », 10 juillet 2014 ; Yonhap News TV, direct du retour de la sélection à l'aéroport d'Incheon, 30 juin 2026. Extraits courts recadrés, son d'origine coupé.
Photos (Wikimedia Commons, recadrées) : Lee Kang-in - Werner100359, CC BY-SA 4.0 ; président Lee Jae-myung - Republic of Korea, CC BY-SA 2.0 ; aéroport d'Incheon - Arne Müseler, CC BY-SA 3.0 DE ; yeot - Institut national de la langue coréenne, CC BY-SA 2.0 KR ; vendeur de yeot - Korea.net (KOCIS), CC BY-SA 2.0. Commerces et vue de Séoul : vidéos Pexels (licence Pexels), illustrations.
Musique : Greed - Arulo / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.
"""
for name in ['legende.txt', 'publication.txt']:
    (p / name).write_text(legend, encoding='utf8')

d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
credits = ['# Sources et crédits', '', '## Faits']
for x in d['sources_a_verifier']:
    credits.append(f"- {x['fait']} : {x['url']}" + (f" ({x['note']})" if x.get('note') else ''))
credits += ['', '## Vraies séquences (extraits recadrés, son coupé, découpés par assets/39-entraineur-banni/archives.py)']
_spec = importlib.util.spec_from_file_location('archives', 'assets/39-entraineur-banni/archives.py')
archives = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(archives)
for k in used:
    if k.startswith('arch-'):
        src, debut, duree, zone, desc, *_ = archives.SEGMENTS[k[5:]]
        info = json.loads(Path('assets/39-entraineur-banni/sources/' + src.replace('.mp4', '.info.json')).read_text(encoding='utf8'))
        u = info['upload_date']
        credits.append(f"- {desc} : {info['channel']}, « {info['title']} », mis en ligne le {u[6:]}/{u[4:6]}/{u[:4]}, {info['webpage_url']} "
                       f"({info.get('license') or 'licence YouTube standard'}), extrait {debut:.1f}-{debut + duree:.1f} s, source {info['width']}x{info['height']}")
credits += ['', '## Vidéos Pexels (illustrations, sans séquence réelle disponible)']
for k in used:
    if k.startswith('pexels-'):
        credits.append(f"- {k}.mp4 : Pexels, licence Pexels, https://www.pexels.com/video/{k.split('pexels-')[1]}/")
credits += [
    '',
    'Panneaux « interdit d’entrée » (reportages KNN LaRYHh_qw4I et MmkQ8xOWAa0, YTN wqXcKjFjGho) et jets de yeot à l’aéroport en 2014 (MBC qmj55kBy7Zw, sirTFgNWYYU) : YouTube a bloqué le téléchargement (contrôle anti-robot), passages illustrés par Pexels et une photo Commons.',
    'Plan écarté : arrivée à Incheon avec un homme aux cheveux gris en chemise blanche au premier plan (non identifié, risque de le prendre pour Hong).',
    'Écartés au repérage : stades et supporters identifiables (Fenerbahçe 35053395, 35002181, 35002164, 34514079 ; Beşiktaş 37342408 ; Brighton 39711248, 39239777 ; Galatasaray 32337290 ; tribune jaune 34605094), football australien 37636010, atterrissage trop sombre 10961750, parking 20331106, barbecue 2560 px 19810469.',
    'Photos écartées : portrait 2013 de Hong et photo recadrée de Lee Kang-in (visage sous le bandeau de série), photos Special Olympics 2013 (contexte sans rapport).',
    '', '## Photos (Wikimedia Commons, recadrées)',
] + [f"- {r['titre'][5:]} - {r['auteur']} - {r['licence']} - {r['url']}"
     for r in json.loads(Path('assets/39-entraineur-banni/photos/selection.json').read_text(encoding='utf8'))
     if r['cle'] in photos_used] + [
    '', '## Son',
    '- Greed - Arulo, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/',
    '- Narration synthétique ElevenLabs.', '',
    'Comparaison de travail uniquement : vidéo franceinfo du 2 juillet 2026 (https://www.youtube.com/shorts/k5omLtD4ddA), à gauche.', '',
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
        'Grilles de repérage horodatées des vraies séquences : assets/39-entraineur-banni/reperage/*.jpg ; contrôle des extraits recadrés : reperage/arch-controle.jpg',
        '81 captures du MP4 habillé (début, milieu, fin de chaque plan) : _montage/controle/final-page-*.jpg ; corrections : revue-corrections.jpg',
        'Aperçu simulé du lecteur TikTok : apercu-tiktok.jpg'],
    observations=[
        'Hook : titre « L’ENTRAÎNEUR BOYCOTTÉ DANS TOUT LE PAYS » sur Hong Myung-bo à sa conférence de démission (KBS WORLD, 28 juin 2026), visage remonté au-dessus du titre ; Hong en 2002 célébrant son tir au but sur « héros national » dès 2,5 s ; 2 plans avant 5 s',
        'Vraies séquences sourcées : 3 matchs du Mondial 2026 (FIFA), démission de Hong et salut à la presse (KBS WORLD), démission de 2014 (Arirang), aéroport d’Incheon le 30 juin 2026 avec policiers et supporters (Yonhap TV), tir au but de Hong et liesse de 2002 (FIFA)',
        'Scores, logos de chaîne, incrustations et sous-titres anglais exclus du recadrage ; image entière sur fond flou, son d’origine coupé',
        'Bandeaux « CORÉE DU SUD - MONDIAL 2026 », « PHASE DE GROUPES », « ÉLIMINÉE » sur le coup de sifflet final, « CORÉE - ESPAGNE, MONDIAL 2002 » sur le stade de Gwangju',
        'Fun fact « MANGE DU CARAMEL » = UNE INSULTE 26,0-30,5 s sur des photos de yeot',
        'Corrections après contrôle : restes du score FIFA en haut du cadre supprimés, logo Yonhap retiré du plan des policiers, plan KBS avec flash blanc remplacé, bandeau nominatif KBS sorti du cadre'],
    limites=[
        'Aucune écoute possible : prononciations (Hong Myong-bo, Li Kang-inne) et mix non validés à l’oreille.',
        'Contrôle par captures, pas de visionnage continu.',
        'Sources 1080p (720p pour Arirang 2014) : posées sur fond flou, pas recadrées en plein écran ; le plan de 2014 reste un peu doux.',
        'Panneaux « interdit d’entrée » et jets de yeot de 2014 : séquences non téléchargeables, illustrés par Pexels (bar, resto, supérette) et une photo du hall d’Incheon.',
        'Ministère et fédération : vue de Séoul (Pexels), aucune séquence de l’audit.'],
    a_revoir_avant_de_poster=[
        'Droits : extraits FIFA, KBS, Arirang et Yonhap sous licence YouTube standard, courts extraits commentés, sources citées ; risque de réclamation ou de blocage (Content ID) sur TikTok ou YouTube accepté par Marc le 12 novembre 2026.',
        'Titre « boycotté dans tout le pays » choisi par Marc : formule d’ampleur ; les panneaux documentés concernent quelques commerces dans plusieurs villes, et la colère est nationale.',
        'Hong est vivant et n’est accusé d’aucune infraction : la vidéo rapporte les réactions (panneaux, supporters, menaces) et la conclusion attribuée au ministère sur la fédération.',
        'Label IA TikTok non requis (vraies séquences et photos, voix de narrateur qui n’imite personne).'],
    technique=dict(export, pistes_comparaison=tracks), validation_utilisateur=False)
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export à visionner'
d['legende'] = legend.split('\n')[0]
d['hashtags'] = legend.split('\n')[2].split()
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')

idx = Path('out/versions-actuelles.json')
data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != 39]
data.append(dict(numero=39, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True,
                 statut='a_visionner', revision=stamp + ' : vraies séquences sourcées (FIFA, KBS, Arirang, Yonhap) à la place des plans génériques',
                 apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print('ok', used)
