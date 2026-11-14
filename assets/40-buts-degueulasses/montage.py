"""Plans du dossier 40, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère précédent.
Les extraits `arch-*.mp4` sont déjà en 1080x1920 (archives.py), un par plan, cadrés serré sur l'action :
`entree` y est compté depuis le début de l'extrait, soit la seconde de la source moins le début du segment.
Photos : vraies photos Commons au moment où le nom est prononcé (consigne de Marc), recadrées sur le visage.
"""
import json
import re
from pathlib import Path

from archives import SEGMENTS

m = Path('out/40-top-10-buts-les-plus-degueulasses/_montage')
S = '40-buts-degueulasses/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?]+$", '', w['w'].lower()) for w in words]
sel = {p['cle']: p for p in json.loads(Path('assets/40-buts-degueulasses/photos/selection.json').read_text(encoding='utf8'))}


def arch(key, src_second):
    """Plan d'un extrait vertical, entrée donnée en seconde de la source d'origine."""
    start = SEGMENTS[key][1]
    return S + f'arch-{key}.mp4', round(src_second - start, 2), .5


def photo(key):
    """Photo déjà recadrée en 9:16 sur le visage (archives.py photos)."""
    return S + 'photos/v-' + sel[key]['fichier'], 0, .5


# (mot repère qui ouvre le plan suivant, (source, entrée, cadrage), note) ; None = dernier plan
rows = [
 ('le', (S + 'pexels-6084018.mp4', 5.0, .5), 'Accroche : gardien qui plonge (Pexels, 4K vertical, zoom sur le but), aucun nom'),
 ('réclamé', (S + 'pexels-40867851.mp4', 3.0, .5), 'Accroche : stade de nuit vu du ciel (Pexels)'),
 ('numéro', (S + 'pexels-6077715.mp4', 11.0, .5), 'Accroche : penalty tiré (Pexels)'),
 ('colimor', arch('collymore', 20.3), 'N°10 : Blackburn - Liverpool 1996, la frappe et le ballon au fond'),
 ('une', photo('collymore'), 'N°10 : photo de Stan Collymore sur son nom'),
 ('numéro', arch('collymore2', 26.6), 'N°10 : autre angle, le ballon passe au-dessus du gardien'),
 ('inzagui', arch('inzaghi', 15.4), 'N°9 : finale de Ligue des champions 2007, coup franc'),
 ('le', photo('inzaghi'), 'N°9 : photo de Filippo Inzaghi sur son nom (le plan de célébration montrait surtout un coéquipier)'),
 ('numéro', arch('inzaghi2', 18.4), 'N°9 : coup franc de Pirlo dévié, but'),
 ('rob', arch('green', 23.9), 'N°8 : Angleterre - États-Unis 2010, frappe de Dempsey (caméra au ras du sol, 720p)'),
 ('filer', photo('green'), 'N°8 : photo de Robert Green sur son nom'),
 ('numéro', arch('green2', 29.3), 'N°8 : le ballon glisse sous Green, touche le poteau et entre'),
 ('pikford', arch('origi', 59.5), 'N°7 : derby de Liverpool 2018, dernière action'),
 ('rate', photo('pickford'), 'N°7 : photo de Jordan Pickford sur son nom'),
 ('origui', arch('origi2', 63.9), 'N°7 : Pickford remet le ballon en l’air'),
 ('numéro', arch('origi3', 65.7), 'N°7 : la tête d’Origi (n°27) et le ballon au fond, sur son nom'),
 ('lloris', arch('lloris0', 0.4), 'N°6 : finale du Mondial 2018, le trophée avant le match'),
 ('mandjoukitch', photo('lloris'), 'N°6 : photo de Hugo Lloris sur son nom'),
 ('devant', arch('mandzukic', 98.9), 'N°6 : Mandžukić de près dans le but, sur son nom (la photo Commons, 558x686, était trop floue en recadrage)'),
 ('croate…', arch('lloris', 99.8), 'N°6 : ralenti depuis le but, Lloris contré par Mandžukić, le ballon roule vers le but'),
 ('numéro', arch('lloris2', 95.0), 'N°6 : plan large sur « et rentre », le ballon entre dans le but'),
 ('dix-huit', arch('karius', 17.6), 'N°5 : finale de Ligue des champions 2018, Karius a le ballon'),
 ('karius', photo('karius'), 'N°5 : photo de Loris Karius, juste avant son nom'),
 ('numéro', arch('karius2', 20.3), 'N°5 : Karius a le ballon sur son nom, relance contrée par Benzema, ballon au fond avant le volet'),
 ('tchitcharito', arch('chicharito', 8.6), 'N°4 : Community Shield 2010, plan large'),
 ('rate', arch('chicharito2', 16.0), 'N°4 : Chicharito de face qui célèbre, sur son nom'),
 (('rentre', 'et'), arch('chicharito3', 11.6), 'N°4 : le centre, le ballon sur le visage, le but'),
 ('numéro', (S + 'pexels-40867851.mp4', 20.0, .5), 'Relance : stade de nuit (Pexels), sans révélation'),
 ('kisling', arch('kiessling', 2.3), 'N°3 : Hoffenheim - Leverkusen 2013, corner et tête'),
 ('à', arch('kiessling2', 12.0), 'N°3 : Kießling avec ses coéquipiers (nom au dos), sur son nom'),
 ('numéro', arch('kiessling3', 19.6), 'N°3 : derrière le but, le ballon entre par le côté du filet'),
 ('darène', arch('bent', 274.0), 'N°2 : Sunderland - Liverpool 2009, construction'),
 ('tape', arch('bent2', 272.0), 'N°2 : Darren Bent de près, sur son nom'),
 ('leur', arch('bent3', 282.8), 'N°2 : la frappe dévie sur le ballon de plage'),
 ('ce', arch('bent4', 288.5), 'N°2 : le gardien suit le mauvais ballon (ralenti)'),
 ('numéro', arch('bent5', 294.0), 'Fun fact : le ballon de plage rouge à l’image'),
 ("d'érikssène", arch('kane0', 18.5), 'N°1 : Stoke - Tottenham 2018, plan large du match'),
 ('direct', arch('eriksen', 53.6), 'N°1 : Eriksen prend son élan, sur son nom'),
 ('kéne', arch('kane', 56.0), 'N°1 : le coup franc arrive au but'),
 ("l'avoir", arch('kane2', 59.0), 'N°1 : Kane derrière le but (nom au dos), sur son nom'),
 ('kéne', arch('interview', 10.0), 'N°1 : Kane et Eriksen en interview après le match'),
 ('abonne-toi', arch('kane3', 61.5), 'Fin : Kane célèbre le but'),
 (None, arch('interview2', 20.0), 'Fin : Kane et Eriksen en interview'),
]
ZONES = {S + 'pexels-6084018.mp4': 'crop=1215:2160:900:1100'}


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], 0
for anchor, (src, t, c), note in rows:
    end = None
    if anchor:
        for w in (anchor if isinstance(anchor, tuple) else (anchor,)):
            cursor = find(w, cursor + 1)
        end = round(words[cursor]['start'], 3)
    row = dict(fin=end, source=src, entree=t, cadrage=c, note=note)
    if src in ZONES:
        row['zone'] = ZONES[src]
    plans.append(row)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
