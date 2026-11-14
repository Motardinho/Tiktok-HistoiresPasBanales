"""Livraison des dossiers 35 et 36 : aperçu simulé du lecteur, légende, crédits, contrôle daté, index.
python livraison.py 35|36"""
import json, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

n = int(sys.argv[1])
root = Path.cwd()
p = next((root / 'out').glob(f'{n}-*')); m = p / '_montage'
A = root / 'assets'
d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
plans = json.loads((m / 'plans.json').read_text(encoding='utf8'))
stamp = datetime.now(timezone(timedelta(hours=1))).isoformat(timespec='seconds')
font = lambda s: ImageFont.truetype(str(A / 'fonts/Poppins-ExtraBold.ttf'), s)

# --- Aperçu simulé du lecteur TikTok (distinct du final)
duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p / 'final.mp4')]))
fact = d['fun_fact_affichage']
sheet = Image.new('RGB', (1080, 694), '#11151c'); draw = ImageDraw.Draw(sheet)
for i, t in enumerate([.6, (fact['debut'] + fact['fin']) / 2, duration - 1.2]):
    shot = m / f'controle-lecteur-{i}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(p / 'final.mp4'), '-frames:v', '1', str(shot)], check=True)
    im = Image.open(shot).convert('RGBA'); ui = Image.new('RGBA', im.size); x = ImageDraw.Draw(ui)
    x.rounded_rectangle((90, 65, 990, 170), radius=24, fill=(20, 20, 20, 185)); x.text((125, 90), 'Rechercher', font=font(46), fill='white')
    x.rectangle((0, 1410, 1080, 1920), fill=(0, 0, 0, 150)); x.text((55, 1430), '@histoirespasbanales', font=font(42), fill='white')
    for j, s in enumerate([d['legende'][:38] + '...', d['scenes'][-1]['narration'].split('?')[0] + '?', ' '.join(d['hashtags'][:3])]):
        x.text((55, 1500 + j * 60), s, font=font(35), fill='white')
    x.text((55, 1740), 'Son original', font=font(35), fill='white'); x.line((0, 1810, 1080, 1810), fill='gray', width=2)
    for y, label in [(850, 'Profil'), (1040, 'J’aime'), (1220, 'Com.'), (1390, 'Partager')]:
        x.ellipse((965, y, 1035, y + 70), fill=(255, 255, 255, 220)); x.text((945, y + 80), label, font=font(22), fill='white')
    im = Image.alpha_composite(im, ui).convert('RGB').resize((360, 640), Image.Resampling.LANCZOS)
    sheet.paste(im, (i * 360, 54)); draw.text((i * 360 + 10, 14), f'{n} - {t:.1f}s - SIMULATION', font=font(16), fill='white')
sheet.save(p / 'apercu-tiktok.jpg')

# --- Crédits
photos = {}
for folder in ('35-crashgate', '36-spygate'):
    f = A / folder / 'photos/selection.json'
    if f.exists():
        for r in json.loads(f.read_text(encoding='utf8')):
            photos[f"{folder}/photos/{r['fichier']}"] = r
sources = list(dict.fromkeys(x['source'] for x in plans))
video_lines, photo_lines, compact_videos, by_licence = [], [], [], {}
archives = {}
for folder in ('35-crashgate', '36-spygate'):
    af = A / folder / 'archives.json'
    if af.exists():
        archives.update({f'{folder}/{k}': v for k, v in json.loads(af.read_text(encoding='utf8')).items()})
arch_lines, arch_sources = [], {}
for s in sources:
    stem = Path(s).stem
    if stem.startswith('arch-'):
        r = archives[s]
        arch_lines.append(f"- {r['description']} : {r['chaine']}, « {r['titre']} », mis en ligne le {r['mise_en_ligne']}, {r['url']} - source {r['resolution']}, extrait de {r['duree']} s à partir de {r['debut']} s, recadré sans logo, posé sur fond flou, son coupé.")
        arch_sources[r['url']] = f"{r['chaine']}, « {r['titre']} » ({r['mise_en_ligne'][:4]}) {r['url']}"
    elif stem.startswith('pexels-'):
        info = json.loads((A / Path(s).with_suffix('.json')).read_text(encoding='utf8'))
        video_lines.append(f"- {info['auteur']} : {info['source']} - licence Pexels https://www.pexels.com/license/ - {info['width']}x{info['height']}, extrait recadré, sans son original.")
        compact_videos.append(f"{info['auteur']} https://www.pexels.com/video/{stem[7:]}/")
    else:
        r = photos[s]
        author = r['auteur'] or 'auteur non renseigné'
        photo_lines.append(f"- {r['titre'][5:]} : {author}, {r['date'] or 'date non renseignée'} - {r['licence']} {r.get('licence_url', '')} - {r['url']} - original {r.get('taille_originale', r.get('taille'))}, vignette {r.get('largeur_telechargee', 'originale')} px, recadrée, léger zoom.")
        by_licence.setdefault(r['licence'], []).append(author.split(' from ')[0])
track = next(x for x in json.loads((A / 'musique/mixkit/sources.json').read_text(encoding='utf8')) if x['slug'] == d['musique'])
music = f"Musique : {track['title']} - {track['artist']} / Mixkit, {track['license_url']}"
notes = [x['note'] for x in plans]
DISCLOSURE = {
 35: "Les séquences de course sont de vraies images du Grand Prix de Singapour du 28 septembre 2008 (diffusion d'origine, vidéo de spectateur) et du Grand Prix du Brésil 2008 (chaîne officielle Formula 1) : extraits courts, recadrés, son d'origine coupé, droits de leurs diffuseurs. Photos d'archives identifiées de 2006 à 2024. Seuls le panorama de Singapour et le marteau de juge sont des illustrations.",
 36: "Les séquences de course et d'audience sont de vraies images de 2007 : Grand Prix du Brésil (chaîne officielle Formula 1), qualifications de Hongrie (diffusion d'origine), audience de la FIA du 13 septembre 2007 à Paris (AP Archive). Extraits courts, recadrés, son d'origine coupé, droits de leurs diffuseurs. Photocopieur, documents, disque, téléphone, clavier et billets sont des illustrations : personne à l'écran n'est l'employé, l'ingénieur ou son épouse. Le portrait d'Alonso date de 2008.",
}[n]
intro = d['legende'] + '\n\n' + ' '.join(d['hashtags'])
urls = '\n'.join(dict.fromkeys(x['url'] for x in d['sources_a_verifier']))
licences = {'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/', 'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/',
            'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/', 'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/',
            'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/', 'CC BY 2.5': 'https://creativecommons.org/licenses/by/2.5/'}
photo_compact = ' ; '.join(f"{', '.join(dict.fromkeys(v))} ({k}{' ' + licences[k] if k in licences else ''})" for k, v in by_licence.items())
publication = (intro + '\n\n' + DISCLOSURE + '\n\nSources :\n' + urls + '\n\nPhotos Wikimedia Commons, recadrées : ' + photo_compact +
               '. Adaptations sous la même licence.\nSéquences réelles, extraits courts recadrés, son coupé : ' + ' ; '.join(arch_sources.values()) +
               '\nVidéos Pexels, recadrées, licence https://www.pexels.com/license/ : ' + ' ; '.join(compact_videos) +
               '\n' + music + ' . Voix synthétique ElevenLabs.\n')
if len(publication) >= 4000:
    publication = publication.replace(' ; '.join(compact_videos), ', '.join(dict.fromkeys(v.rsplit(' ', 1)[0] for v in compact_videos)))
assert len(publication) < 4000, len(publication)
(p / 'legende.txt').write_text(publication, encoding='utf8'); (p / 'publication.txt').write_text(publication, encoding='utf8')
(p / 'CREDITS.md').write_text(
    f'# Sources et crédits - dossier {n}\n\n{DISCLOSURE}\n\n## Faits\n\n' +
    '\n'.join(f"- {x['fait']} : {x['url']} ({x.get('note', '')})" for x in d['sources_a_verifier']) +
    '\n\n## Photos Wikimedia Commons\n\n' + '\n'.join(photo_lines) + '\n\n## Séquences réelles (droits des diffuseurs)\n\n' + '\n'.join(arch_lines) + '\n\n## Vidéos Pexels\n\n' + '\n'.join(video_lines) +
    f"\n\n## Son\n\n- {music} ; page {track['page']}\n- Voix synthétique ElevenLabs.\n\n## Plans\n\n" +
    '\n'.join(f"- {x['source']} : {x['note']}" for x in plans) + '\n', encoding='utf8')
(p / 'script.txt').write_text('\n\n'.join(x['narration'] for x in d['scenes']) + '\n', encoding='utf8')

# --- Contrôle daté
export = json.loads((m / 'controle-export.json').read_text(encoding='utf8'))
assert (p / 'comparaison.mp4').stat().st_mtime >= (p / 'final.mp4').stat().st_mtime
timing = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))
first = d['scenes'][0]['narration_voix'].split()
hook_end = timing['words'][len(first) - 1]['end']
cuts = [x['fin'] for x in plans if x['fin'] is not None and x['fin'] < 5]
report = dict(
    date=stamp, statut='export de travail - écoute et visionnage continu par Marc requis', validation_utilisateur=False,
    technique=export, duree_cible='61 à 70 s, 75 au plus', fin_du_hook_oral=round(hook_end, 2), plans_avant_5s=len(cuts) + 1,
    fun_fact=dict(texte=fact['texte'], debut=fact['debut'], fin=fact['fin'], source=d['fun_fact']['source']),
    captures=dict(dossier=str((m / 'controle').relative_to(root)), nombre=len(plans) * 3, methode='début, milieu et fin de chaque plan dans final.mp4, planches final-page-N.jpg regardées'),
    apercu_simule='apercu-tiktok.jpg',
    observations=json.loads((m / 'observations.json').read_text(encoding='utf8')) if (m / 'observations.json').exists() else [],
    limites=["Aucune écoute par l'agent : prononciation des noms (phonétique française), raccords et balance voix/musique restent à écouter.",
             'Contrôle visuel par captures (trois par plan), pas de visionnage continu.',
             'Photos Commons téléchargées en vignettes standard de 960 à 3840 px (limitation de débit de Wikimedia sur les originaux) : largeur utile après recadrage souvent inférieure à 1 000 px.',
             "Archives de diffusion en 360p à 720p (sauf Formula 1 officiel en 1080p) : image entière sur fond flou, plans doux. Droits d'auteur des diffuseurs : risque de son coupé, de diffusion limitée ou de retrait par TikTok ou YouTube."],
    comparaison=json.loads((m / 'controle-comparaison.json').read_text(encoding='utf8')) if (m / 'controle-comparaison.json').exists() else 'générée par le moteur après final.mp4')
(p / 'controle-livraison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
d['statut'] = 'export de travail - écoute et visionnage continu requis'
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
idx = root / 'out/versions-actuelles.json'; data = [x for x in json.loads(idx.read_text(encoding='utf8')) if x.get('numero') != n]
data.append(dict(numero=n, dossier=p.name, duree=export['duree_video'], sha256=export['sha256'], comparaison_a_jour=True, statut='a_visionner',
                 revision=stamp + ' : nouvelle vidéo automobile insolite', apercu_simule='apercu-tiktok.jpg'))
idx.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print(n, 'livraison enregistrée', stamp, '| légende', len(publication), 'caractères | hook oral fini à', round(hook_end, 2), 's | plans avant 5 s :', len(cuts) + 1)
