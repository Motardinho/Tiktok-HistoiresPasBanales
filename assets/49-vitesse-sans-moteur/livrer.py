"""Livraison du dossier 49 : légendes, crédits, miniature, contrôle daté et index."""
import json, hashlib, subprocess, shutil, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image

R = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R))
import miniatures_hpb as mh
P = R / 'out/49-top-3-records-vitesse-sans-moteur'; A = R / 'assets/49-vitesse-sans-moteur'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
save = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

d = read(P / 'histoire.json'); plans = read(P / 'plans.json')
sources = []
for sid in dict.fromkeys(Path(p['source']).stem for p in plans):
    x = read(A / (sid + '.info.json'))
    sources.append(dict(id=sid, chaine=x.get('channel'), titre=x.get('title'), date=x.get('upload_date'),
                        url=x.get('webpage_url'), largeur=x['width'], hauteur=x['height']))
for p in plans:
    s = next(s for s in sources if s['id'] == Path(p['source']).stem)
    p['provenance'] = s
    p['largeur_utile'] = 2 * round(p['hauteur'] * 9 / 16 / 2)
save(P / 'sources-visuelles.json', plans)

images = ' ; '.join(f"{s['chaine']}, « {s['titre']} » ({s['date'][:4]}) {s['url']}" for s in sources)
faits = """Simon Billy, 255,5 km/h à ski, 22 mars 2023, Vars (Hautes-Alpes), record du monde : Eurosport ; vars.com
Philippe Billy, son père, record du monde en 1997 à Vars (243,902 km/h) : Eurosport ; vars.com
0 à 200 km/h en moins de 6 s sur la piste de Chabrières : station de Vars
Denise Mueller-Korenek, 296,009 km/h à vélo dans l’abri d’un dragster, 16 septembre 2018, Bonneville (Utah) : Guinness World Records ; NPR ; Wall Street Journal
Felix Baumgartner, 1 357,6 km/h en chute libre, mur du son franchi, 14 octobre 2012, saut depuis environ 39 km (Red Bull Stratos) : Guinness World Records
8 millions de flux simultanés en direct sur YouTube, record de la plateforme à l’époque : The Drum ; Tubefilter (chiffre de YouTube)
Sélection d’un record par discipline, pas un podium absolu : le wingsuit (396,88 km/h) va plus vite que le vélo."""
musique = 'Musique : Sports Highlights - Ahjay Stelino / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.'
legende = ('255 km/h à ski, 296 à vélo, 1 357 en chute libre. Aucun moteur. Pour toi, c’est qui le vrai numéro 1 ?\n\n'
           '#HistoiresPasBanales #record #vitesse #ski #velo #chutelibre\n\nSources des faits :\n' + faits +
           '\n\nSéquences réelles, extraits courts recadrés, son d’origine coupé, droits de leurs auteurs : ' + images +
           '\n' + musique + '\n')
for name in ['legende.txt', 'publication.txt']:
    (P / name).write_text(legende, encoding='utf8')
(P / 'CREDITS.md').write_text('# Top 3 des records de vitesse les plus fous sans moteur\n\n## Faits\n\n' + faits +
    '\n\n## Images\n\n' + '\n'.join(f"- {s['chaine']} - {s['titre']} - {s['date']} - {s['url']} ({s['largeur']}x{s['hauteur']})" for s in sources) +
    '\n- Miniature : Red Bull, FHtvDA0W34I à 51,5 s (Felix Baumgartner sur la marche de la capsule Stratos).\n\n## Musique et voix\n\n' + musique +
    '\n\nLa citation des sources ne vaut pas acquisition des droits. Les ayants droit peuvent revendiquer les extraits (son coupé ou diffusion limitée sur TikTok et YouTube).\n',
    encoding='utf8')

# Miniature : copie, preuve avant/après des réglages photo, aperçu 360 px.
shutil.copy2(R / 'out/miniatures-v4/49.jpg', P / 'miniature.jpg')
c = dict(mh.DOSSIERS[49]); c.pop('lignes'); c.pop('style'); fond = c.pop('fond')
avant = mh.preparer_fond(mh.FONDS / fond, centre=c['centre'], contraste=1.0, saturation=1.0, luminosite=1.0,
                         voile_bas=0, voile_haut=0, vignette=False).convert('RGB')
apres = mh.preparer_fond(mh.FONDS / fond, **c).convert('RGB')
avant.save(P / 'miniature-photo-avant.jpg', quality=92); apres.save(P / 'miniature-photo-apres.jpg', quality=92)
Image.open(P / 'miniature.jpg').resize((360, 640), Image.Resampling.LANCZOS).save(P / 'miniature-apercu.jpg', quality=92)
save(P / 'miniature-manifeste.json', dict(style='course (modèle 07, vitesse)', fond=fond, reglages={k: v for k, v in c.items()},
     titre=['TOP 3', 'RECORDS DE VITESSE', 'LES PLUS FOUS', 'SANS MOTEUR'], generateur='miniatures_hpb.py 49',
     controle_zones='out/miniatures-v4/zones-49.jpg', limite='Source 1080p agrandie 1,78 fois : image un peu douce.',
     fichiers_examines=['out/miniatures-v4/49.jpg', 'miniature-photo-avant.jpg', 'miniature-photo-apres.jpg', 'miniature-apercu.jpg']))

final = P / 'final.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(final), '-f', 'null', '-'], check=True, capture_output=True)
info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
       'format=duration:stream=codec_type,duration,width,height', '-of', 'json', str(final)]))
v = next(s for s in info['streams'] if s['codec_type'] == 'video'); a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
assert float(v['duration']) > 60 and abs(float(v['duration']) - float(a['duration'])) < .15
now = datetime.now(ZoneInfo('Europe/Paris')).isoformat()
save(P / 'controle-livraison.json', dict(date=now, statut='montage à visionner et écouter', validation_utilisateur=False,
    technique=dict(info=info, decodage_integral=True, sha256=hashlib.sha256(final.read_bytes()).hexdigest()),
    preuves_examinees=['Planches de repérage horodatées assets/49-vitesse-sans-moteur/reperage-*',
                       'Aperçus portrait des plans avant montage (portrait-0 à 6.jpg)',
                       'Détection automatique des changements de plan des sources dans chaque plan (coupes.py) : aucune coupe restante',
                       'Captures début/milieu/fin des 38 plans, controle/planche-0.jpg à planche-9.jpg',
                       'Première image à 0:00 (controle/premiere-image.jpg) et simulation du lecteur TikTok (apercu-tiktok.jpg)',
                       'Miniature, zones sûres et avant/après des réglages photo'],
    corrections=['Plans d’un autre dragster (violet) écartés : seul le dragster rouge de Shea Holbrook apparaît',
                 'Spectateur au premier plan, incrustations km/h et icônes de lecteur des sources recadrées ou écartées',
                 'Logo HPB déplacé hors des visages (cycliste, Simon Billy) par recadrage',
                 'Avion de ligne remplacé par un A380 qui reste dans le cadre',
                 'Coupes de source en milieu de plan supprimées (17 plans recalés)',
                 'Archive 1997 scindée pour ne pas montrer un autre skieur sur « son père »'],
    limites=['Écoute et visionnage continu non réalisés dans cet environnement : contrôle par captures.',
             'Sources ski et Stratos en 1080p (608 px utiles après recadrage vertical) : image plus douce que la vidéo WSJ en 4K.',
             'Archive 1997 en 480p, très douce. Identité du skieur de 1997 donnée par le titre de la source, non certifiée.',
             'Plan de fondu sur le visage de Baumgartner en fin de plan (fondu présent dans la source).',
             'Extraits sous licence YouTube standard : revendications possibles des ayants droit.'],
    comparaison_requise=False))
d.update(statut='à visionner et écouter', duree=float(v['duration']), comparaison_requise=False); save(P / 'histoire.json', d)
index = R / 'out/versions-actuelles.json'; items = [x for x in read(index) if x.get('numero') != 49]
items.append(dict(numero=49, dossier=P.name, statut='a_visionner_et_ecouter', duree=float(v['duration']), revision=now,
                  miniature='miniature.jpg', comparaison_requise=False)); save(index, items)
print('Livraison préparée', v['duration'])
