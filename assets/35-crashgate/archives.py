"""Dossiers 35 et 36 : vraies séquences (diffusion d'origine, F1 officiel, AP Archive) en 1080x1920,
image entière sur fond flou du même plan (procédé des dossiers 27 et 40).

Chaque extrait est recadré (zone x, y, w, h dans la source) pour exclure logos de diffuseur, habillage
et filigranes, mis à 1080 de large et posé à y = top. `vitesse` < 1 = ralenti. Son d'origine coupé.
python archives.py 35|36 [clé ...]  ->  assets/<dossier>/arch-<clé>.mp4 + archives.json
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = {35: '35-crashgate', 36: '36-spygate'}
TV = (480, 60, 2880, 1650)      # ulQpaIS-iZQ 3840x2160 : logo F1 en bas à gauche et pastille en haut à droite exclus
CRASH = (1000, 150, 2000, 1500)  # même source, cadre serré sur le mur
AP = (80, 54, 480, 300)          # AP Archive 640x360, image 4:3 : logo AP en haut à droite exclu
F1 = (240, 60, 1440, 830)        # F1 officiel 1920x1080 : logo F1 et mention de course du bas exclus

# clé : (source, début, durée source, zone, top, vitesse, description)
SEGMENTS = {35: {
    'crash-hook': ('ulQpaIS-iZQ', 7.55, 2.5, CRASH, 440, 1, "L'accident de Nelson Piquet Jr, virage 17, Singapour, 28 septembre 2008"),
    'muret': ('ulQpaIS-iZQ', 2.0, 2.8, TV, 610, 1, "Le muret des stands Renault pendant la course"),
    'piste': ('ulQpaIS-iZQ', 5.0, 2.4, TV, 610, 1, "Le circuit de Marina Bay de nuit"),
    'stand': ('ulQpaIS-iZQ', 0.0, 0.95, TV, 610, .42, "Arrêt au stand de la Renault d'Alonso, ralenti"),
    'ralenti': ('ulQpaIS-iZQ', 7.85, 0.8, CRASH, 610, .5, "L'accident de Piquet Jr, ralenti"),
    'sc': ('ulQpaIS-iZQ', 11.0, 1.7, TV, 610, 1, "Panneau lumineux SC : voiture de sécurité"),
    'ravitaillement': ('ulQpaIS-iZQ', 15.0, 2.5, TV, 610, 1, "La voie des stands sous voiture de sécurité"),
    'apres': ('ulQpaIS-iZQ', 9.3, 1.2, CRASH, 610, 1, "La Renault de Piquet Jr contre le mur"),
    'grue': ('IMbx-wLwwHY', 3.0, 4.0, (80, 60, 480, 360), 610, 1, "La Renault accidentée de Piquet Jr soulevée par une grue (vidéo de spectateur)"),
    'grue2': ('IMbx-wLwwHY', 20.0, 3.5, (80, 60, 480, 360), 610, 1, "La Renault accidentée de Piquet Jr évacuée (vidéo de spectateur)"),
    'alonso-gagne': ('VVAbwLGuQ_M', 34.0, 1.3, (100, 95, 420, 315), 610, 1, "Alonso vainqueur dans sa Renault (écran de télévision filmé)"),
    'massa-podium': ('3pKsxtzfVbQ', 487.2, 2.5, F1, 610, 1, "Felipe Massa sur le podium du Brésil 2008, titre perdu d'un point"),
}, 36: {
    'depart1': ('dCmT9A7mCwM', 12.0, 2.7, F1, 610, 1, "Départ du Grand Prix du Brésil 2007, Ferrari et McLaren en tête"),
    'depart2': ('dCmT9A7mCwM', 14.8, 3.3, F1, 610, 1, "Premiers virages du Grand Prix du Brésil 2007"),
    'kimi-cockpit': ('dCmT9A7mCwM', 59.6, 1.7, F1, 610, 1, "Kimi Räikkönen dans sa Ferrari, Brésil 2007"),
    'ferrari-fete': ('dCmT9A7mCwM', 107.6, 1.8, F1, 610, 1, "L'équipe Ferrari fête le titre 2007"),
    'kimi-damier': ('dCmT9A7mCwM', 80.2, 3.2, F1, 610, 1, "Räikkönen passe le drapeau à damier, Brésil 2007"),
    'kimi-podium': ('dCmT9A7mCwM', 100.8, 3.3, F1, 610, 1, "Räikkönen champion du monde sur le podium, Brésil 2007"),
    'kimi-champagne': ('dCmT9A7mCwM', 104.4, 1.3, F1, 610, 1, "Räikkönen champion du monde, Brésil 2007"),
    'cartons': ('p-oZ-SPL794', 127.3, 3.6, AP, 610, 1, "Cartons de documents apportés à l'audience de la FIA, Paris, 13 septembre 2007"),
    'fia-plaque': ('p-oZ-SPL794', 11.2, 1.7, AP, 610, 1, "Siège de la FIA, place de la Concorde, 13 septembre 2007"),
    'dennis-foule': ('p-oZ-SPL794', 74.6, 4.0, AP, 610, 1, "Ron Dennis, patron de McLaren, arrive à l'audience, 13 septembre 2007"),
    'dennis-conf': ('pnr2O2uUqIg', 61.0, 1.5, AP, 610, 1, "Ron Dennis en conférence de presse après le verdict"),
    'dennis-conf2': ('pnr2O2uUqIg', 118.0, 3.3, AP, 610, 1, "Ron Dennis lit sa déclaration après le verdict"),
    'hongrie-stand': ('T1m2_yDndrs', 0.2, 2.8, (340, 60, 900, 500), 610, 1, "Voie des stands, qualifications du Grand Prix de Hongrie 2007"),
    'hongrie': ('T1m2_yDndrs', 9.0, 2.1, (340, 60, 900, 500), 610, 1, "La McLaren d'Alonso immobile dans son stand, Hongrie 2007"),
}}


def render(n, key):
    src, start, dur, (x, y, w, h), top, speed, note = SEGMENTS[n][key]
    d = ROOT / FOLDER[n]
    graph = (f'[0:v]setpts=PTS/{speed},crop={w}:{h}:{x}:{y},split[a][b];'
             '[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             'boxblur=28:2,eq=brightness=-0.16:saturation=0.85[bg];'
             '[a]scale=1080:-2:flags=lanczos[fg];'
             f'[bg][fg]overlay=0:{top},setsar=1,fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', str(d / 'archives' / (src + '.mp4')),
                    '-filter_complex', graph, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    str(d / f'arch-{key}.mp4')], check=True)
    out = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(d / f'arch-{key}.mp4')]))
    print(n, key, round(out, 2), 's', flush=True)


if __name__ == '__main__':
    n = int(sys.argv[1])
    for k in sys.argv[2:] or SEGMENTS[n]:
        render(n, k)
    manifest = {}
    for k, (src, start, dur, zone, top, speed, note) in SEGMENTS[n].items():
        info = json.loads((ROOT / FOLDER[n] / 'archives' / (src + '.info.json')).read_text(encoding='utf8'))
        manifest[f'arch-{k}.mp4'] = dict(source=src, url=info['webpage_url'], chaine=info.get('channel'), titre=info['title'],
                                         mise_en_ligne=info.get('upload_date'), resolution=f"{info.get('width')}x{info.get('height')}",
                                         debut=start, duree=dur, zone=zone, vitesse=speed, description=note)
    (ROOT / FOLDER[n] / 'archives.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf8')
