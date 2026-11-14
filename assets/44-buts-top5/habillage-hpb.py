"""Demande de Marc : titre réservé à la couverture, logo HPB en haut à droite, sans bandeau de série."""
import json
import shutil
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, '.')
from miniatures_hpb import logo_hpb

p = Path('out/44-top-5-buts-les-plus-degueulasses')
a = Path('assets/44-buts-top5')
backup = p / '_montage/avant-logo-hpb'
backup.mkdir(exist_ok=True)
for name in ['histoire.json', 'final.mp4', 'controle-livraison.json']:
    if not (backup/name).exists():
        shutil.copy2(p/name, backup/name)
canvas = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
logo = logo_hpb(hauteur=130)
xy = (1080 - 64 - logo.width, 240)
canvas.alpha_composite(logo, xy)
dest = a / 'entete-hpb.png'
canvas.save(dest)
d = json.loads((p/'histoire.json').read_text(encoding='utf8'))
d['titre_ouverture_visible'] = False
d['habillage_entete_fichier'] = dest.as_posix()
d['logo_hpb_position'] = {'x': xy[0], 'y': xy[1], 'largeur': logo.width, 'hauteur': logo.height}
d['bandeau_serie_visible'] = False
d['choix_editoriaux'].append('13 novembre 2026 : demande explicite de Marc, titre d’ouverture retiré, nouveau logo HPB jaune en haut à droite, bandeau permanent de série retiré. Les repères de classement et le fun fact restent distincts.')
(p/'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
print('Habillage prêt', xy, logo.size)
