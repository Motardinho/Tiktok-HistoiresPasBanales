"""Plans du dossier 41, accrochés aux mots de timings-oraux.json (méthode des dossiers 25 et 40).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère précédent.
Photos des maillots + séquences intercalées (consigne de Marc du 12 novembre 2026).
Les `plans/arch-*.mp4` et `plans/*.png` sont produits par cartes.py, déjà en 1080x1920.
Lancer depuis la racine du dépôt : python assets/41-maillots-moches/montage.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cartes import SEGMENTS  # noqa: E402

m = Path('out/41-top-10-maillots-les-plus-moches/_montage')
S = '41-maillots-moches/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?]+$", '', w['w'].lower()) for w in words]


def arch(key, offset=0.3):
    assert offset < SEGMENTS[key][2]
    return S + f'plans/arch-{key}.mp4', offset, .5


def card(key):
    return S + f'plans/{key}.png', 0, .5


MTP = S + 'montpellier/-sFSl6s4_cM.webm'
# (mot repère qui ouvre le plan suivant, (source, entrée, cadrage), note) ; None = dernier plan
rows = [
 ('le', (S + 'pexels-31343045.mp4', 5.5, .5), 'Accroche : tribunes pleines et pelouse (Pexels, 4K vertical), aucun maillot du classement'),
 ('lunettes', (S + 'pexels-35117249.mp4', 2.0, .5), 'Accroche : supporters qui chantent (Pexels)'),
 ('numéro', (S + 'pexels-7988641.mp4', 1.0, .5), 'Accroche : spectatrice en lunettes 3D sur « lunettes 3D » (Pexels), sans révéler le n°1'),
 ('montpellier', (MTP, 19.0, .55), 'N°10 : le maillot domicile 2025-26 accroché à une grille (MHSC TV, CC BY, 4K)'),
 ('chevron', (MTP, 24.6, .45), 'N°10 : écusson puis gros plan sur le chevron orange, FAUN et le blason'),
 ('torse', (MTP, 37.4, [[0, .28], [.6, .42], [1.44, .45]]), 'N°10 : joueur près du but, le maillot de face, sur « en travers du torse »'),
 ('numéro', (MTP, 39.4, .52), 'N°10 : joueur ballon sous le bras, avant le carton de fin'),
 ('marron…', card('aux-photo'), 'N°9 : photo du third Auxerre 2007-08 Airness, marron et rose (Football Kit Archive)'),
 ('le', arch('aux60', 1.6), 'N°9 : joueur de l\'OM en gros plan avec le maillot marron et rose de l\'AJA, Auxerre - OM 2007 (Canal+)'),
 ('qui', arch('aux140', 1.3), 'Fun fact : autre joueur de l\'OM en maillot de l\'AJA, sur « l\'OM a dû le porter »'),
 ('numéro', arch('aux160'), 'Fun fact : joueur de l\'OM interviewé en maillot de l\'AJA'),
 ('les', arch('bdx92'), 'N°8 : Bordeaux third 2016-17 en match, OL - Bordeaux 2016 (Ligue 1)'),
 ('imprimés', card('bdx-detail'), 'N°8 : détail des photos de monuments imprimées (visuel officiel)'),
 ('numéro', arch('bdx141', 1.2), 'N°8 : motif lisible de trois quarts, Nancy - Bordeaux 2017'),
 ('un', arch('omj171'), 'N°7 : OM extérieur 2013-14 en match, Ajaccio - OM 2013 (Ligue 1)'),
 ('avec', card('omj-face'), 'N°7 : maillot effet jean, de face (visuel produit adidas)'),
 ('numéro', arch('omj173'), 'N°7 : la poche en jean visible en gros plan'),
 ('tout', arch('olo61'), 'N°6 : OL third 2018-19 orange, Man City - Lyon 2018 (UEFA, logo exclu)'),
 ('les', card('olo-aouar'), 'N°6 : maillot orange porté, visuel officiel adidas/OL'),
 ('et', arch('olo24'), 'N°6 : autre joueur lyonnais en orange, même match'),
 ('numéro', (S + 'pexels-8261604.mp4', 3.0, .5), 'Relance : spectatrice en lunettes 3D roses et pop-corn sur « pique les yeux » (Pexels), sans révélation'),
 ('tout', arch('evi178'), 'N°5 : Évian TG domicile 2012-13 rose, Évian - PSG 2013 (Ligue 1)'),
 ('numéro', arch('evi116'), 'N°5 : deux joueurs d\'Évian en rose, Évian - Rennes 2013'),
 ('encore', arch('omr63', 0.05), 'N°4 : le third réversible 2012-13 suspendu au vestiaire (film adidas, sous-titres exclus)'),
 ('akhénaton', card('omr-face'), 'N°4 : maillot bleu nuit et orange, intérieur orange au col (photo produit)'),
 ('numéro', card('akhenaton'), 'N°4 : photo d\'Akhenaton sur son nom (Commons, CC BY-SA 4.0)'),
 ('marron', arch('psg73'), 'N°3 : PSG extérieur 2006-07 marron, Auxerre - PSG 2006 (VHS, score et logo exclus)'),
 ('qui', card('psg-face'), 'N°3 : maillot marron de face, motif monogramme (photo produit)'),
 ('numéro', card('psg-motif'), 'N°3 : gros plan sur le motif façon Louis Vuitton'),
 ('camouflage', arch('bas100'), 'N°2 : Bastia third camouflage 2013-14, PSG - Bastia 2013 (Ligue 1)'),
 ('lui', arch('bas60'), 'N°2 : Bastiais en camouflage devant le but'),
 ('numéro', arch('bas105'), 'N°2 : Bastiais en camouflage, Toulouse - Bastia 2014'),
 ('aux', arch('ol3d27'), 'N°1 : OL 2012-13 « 3D » porté en finale de Coupe de France 2012 (FFF)'),
 ('en', card('lumiere'), 'N°1 : photo des frères Lumière sur leur nom (Commons, domaine public)'),
 ('pour', card('ol3d-face'), 'N°1 : le maillot 3D de face (photo produit)'),
 ('lunettes', card('ol3d-motif'), 'N°1 : gros plan sur le graphisme 3D rouge et cyan'),
 ('et', (S + 'pexels-7985885.mp4', 2.0, .5), 'N°1 : spectatrice en lunettes 3D sur « lunettes » (Pexels)'),
 ('abonne-toi', arch('ol3d70'), 'Fin : Lyonnais en maillot 3D avec leurs médailles'),
 (None, arch('ol3d78', 0.2), 'Fin : les Lyonnais en maillot 3D soulèvent la Coupe de France 2012'),
]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], 0
for anchor, (src, t, c), note in rows:
    end = None
    if anchor:
        cursor = find(anchor, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plans.append(dict(fin=end, source=src, entree=t, cadrage=c, note=note))
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
prev = 0
for p in plans:
    f = p['fin'] or json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['duration']
    seg = re.search(r'arch-(\w+)\.mp4', p['source'])
    if seg:
        assert p['entree'] + f - prev <= SEGMENTS[seg.group(1)][2] + .01, ('extrait trop court', p['source'], round(f - prev, 2))
    prev = f
print(len(plans), 'plans :', [p['fin'] for p in plans])
