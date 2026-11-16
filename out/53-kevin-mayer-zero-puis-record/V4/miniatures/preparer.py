"""Déclinaisons du gabarit magazine HPB, à partir des archives référencées."""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

V4 = Path(__file__).resolve().parent.parent
ROOT = V4.parents[2]
sys.path.insert(0, str(ROOT))
import miniatures_hpb as hpb

OUT = V4 / 'miniatures'
RAW = OUT / 'sources'
QA = OUT / 'controle'
L, H = 1080, 1920
QA.mkdir(parents=True, exist_ok=True)

# Une direction pour chacune, avec un traitement photo indépendant.
VUES = [
    ('01-le-regard', hpb.FONDS / '53-mayer-berlin-van-leeuwen.jpg', None,
     {'echelle': 1.68, 'haut': 183, 'cx': .50}, (1.075, 1.01, 1.05, 1.4, 44)),
    ('02-le-desarroi', RAW / '02-berlin.jpg', (572, 12, 904, 602),
     None, (1.09, .94, 1.21, 1.5, 36)),
    ('03-le-portrait', RAW / '03-stade.jpg', (704, 0, 1311, 1080),
     None, (1.045, .94, 1.01, 1.5, 45)),
    ('04-l-accolade', RAW / '06-accolade.jpg', (665, 130, 1195, 1072),
     None, (1.075, 1.10, 1.045, 1.45, 42)),
    ('05-le-record', RAW / '05-panneau.jpg', (560, 85, 1920, 1080),
     {'echelle': .81, 'haut': 231, 'cx': .50}, (1.10, 1.05, 1.02, 1.45, 49)),
]

def composer_planche(noms, sortie, dossiers=OUT):
    planche = Image.new('RGB', (5*360+6*14, 688), '#10131A')
    d = ImageDraw.Draw(planche)
    for i, nom in enumerate(noms):
        x = 14 + i*374
        image = Image.open(dossiers / f'{nom}.jpg').resize((360, 640), Image.Resampling.LANCZOS)
        planche.paste(image, (x, 14))
        d.text((x+7, 664), nom.replace('-', ' ').upper(), fill='#FFFFFF')
    planche.save(sortie, quality=94)

manifeste = QA / 'reglages-photos.json'
fiche = {x['fichier']: x for x in json.loads(manifeste.read_text(encoding='utf-8'))} if manifeste.exists() else {}
choix = set(sys.argv[1:])
for nom, source, crop, portrait, parametres in VUES:
    if choix and nom[:2] not in choix:
        continue
    im = Image.open(source).convert('RGB')
    if crop:
        im = im.crop(crop)
    if portrait:
        im = hpb.fond_portrait(im, **portrait)
    im = ImageOps.fit(im, (L, H), method=Image.Resampling.LANCZOS)
    im.save(QA / f'{nom}-avant.jpg', quality=94)
    contraste, couleur, lum, rayon, montant = parametres
    im = ImageEnhance.Contrast(im).enhance(contraste)
    im = ImageEnhance.Color(im).enhance(couleur)
    im = ImageEnhance.Brightness(im).enhance(lum)
    im = im.filter(ImageFilter.UnsharpMask(radius=rayon, percent=montant, threshold=3))
    fond = QA / f'{nom}-apres.jpg'
    im.save(fond, quality=95)
    config = dict(hpb.DOSSIERS[53])
    config.pop('portrait', None)
    config.update(fond=fond, contraste=1, saturation=1, luminosite=1, voile_haut=.04, voile_bas=.52)
    hpb.DOSSIERS[5300] = config
    couverture = hpb.composer(5300)
    erreurs = hpb.hors_zone(5300)
    if erreurs:
        raise RuntimeError((nom, erreurs))
    couverture.save(OUT / f'{nom}.jpg', quality=95, subsampling=0)

    bas = couverture.crop((0, 240, L, 1680))
    bas.resize((360,480), Image.Resampling.LANCZOS).save(QA / f'{nom}-grille.jpg', quality=93)
    compare = Image.new('RGB', (720, 640))
    for x, stade in [(0, 'avant'), (360, 'apres')]:
        compare.paste(Image.open(QA / f'{nom}-{stade}.jpg').resize((360,640), Image.Resampling.LANCZOS), (x, 0))
    compare.save(QA / f'{nom}-traitement.jpg', quality=93)
    fiche[f'{nom}.jpg'] = dict(fichier=f'{nom}.jpg', image_source=str(source), recadrage=crop,
                      contraste=contraste, saturation=couleur, luminosite=lum, rayon_nettete=rayon,
                      nettete=montant, titre_et_logo=hpb.ZONES[5300])

composer_planche([v[0] for v in VUES], OUT / 'planche.jpg')
manifeste.write_text(json.dumps([fiche[k] for k in sorted(fiche)], ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
