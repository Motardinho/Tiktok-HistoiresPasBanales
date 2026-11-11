"""Plans du dossier 30, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Sources Pexels (licence Pexels), 4K ou vertical natif ; illustrations génériques.
"""
import json
import re
from pathlib import Path

m = Path('out/30-la-juve-envoyee-en-serie-b/_montage')
S = '30-calciopoli/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
O = lambda i: '../28-om-va/pexels-%d' % i
rows = [
 ('cinq', O(39593839), 3.0, .5, 'Hook : action de football de nuit (illustration, pas la Juventus)'),
 ('coupe', P(18999864), 1.0, .5, 'Olympiastadion de Berlin, lieu de la finale 2006 (prise récente)'),
 ('mai', O(37622460), 4.0, .35, 'Feu d’artifice sur un stade : Coupe du monde'),
 ('on', P(38826405), 0.5, .5, 'Rotative de journaux : les écoutes fuitent dans la presse'),
 ('au', P(8382685), 2.0, .5, 'Magnétophone à bandes : écoutes (pas Moggi)'),
 ('arbitres', P(10397452), 2.0, .5, 'Cadran de téléphone : au bout du fil'),
 ('selon', P(40551621), 2.5, .5, 'Arbitre sur un terrain (match amateur, pas la Serie A)'),
 ('pour', P(6754816), 1.5, .5, 'Intérieur de téléphone : cartes SIM (aucune séquence de carte SIM en 4K trouvée)'),
 ('et', P(7948198), 2.0, .5, 'Homme avec écouteur dans la nuit : ne pas être écouté'),
 ('enfermé', P(4761712), 1.0, .5, 'Porte « LOCKER ROOM » : vestiaire'),
 ('pendant', P(8053942), 1.5, .5, 'Clé tournée dans un casier : enfermé'),
 ('finale', P(34640566), 0.5, .5, 'Berlin vu du ciel : à Berlin'),
 ('sur', P(39799276), 1.0, .5, 'Façade de l’Olympiastadion de Berlin : finale'),
 ('buffon', 'photos/photo-cannavaro-04.jpg', 0, .2, 'PHOTO : la finale du 9 juillet 2006 à Berlin, Cannavaro (Juventus) au premier plan, Henry, Gattuso - David Ruddell, Commons, CC BY 2.0'),
 ('et', 'photos/photo-buffon-06.jpg', 0, .5, 'PHOTO : Gianluigi Buffon, 2016 (Commons, CC BY 2.0), recadrée pour garder le visage sous l’encart', 'crop=iw:ih*0.62:0:0'),
 ('qui', 'photos/photo-trezeguet-08.jpg', 0, .5, 'PHOTO : David Trezeguet, 2017 (Commons, CC BY 2.0)'),
 ("l'italie", P(14234085), 1.0, .5, 'Tir au but manqué à l’entraînement (illustration, pas Trezeguet)'),
 ('cinq', 'photos/photo-celebration-01.jpg', 0, .55, 'PHOTO : supporters italiens à Little Italy (New York) après la victoire en Coupe du monde 2006 (Commons, CC BY-SA 2.5)'),
 ('perd', P(29808342), 1.0, .5, 'Turin vu du ciel : le verdict tombe sur la Juve'),
 ('cannavaro', P(2249402), 1.0, .5, 'Stade vide sous les projecteurs : Série B'),
 ('thuram', 'photos/photo-cannavaro-01.jpg', 0, .5, 'PHOTO : Fabio Cannavaro, 2011 (Commons, CC BY 2.0)'),
 ('ibrahimovitch', 'photos/photo-thuram-01.jpg', 0, .5, 'PHOTO : Lilian Thuram, 2013 (Commons, CC BY 3.0)'),
 ('mais', 'photos/photo-ibra-06.jpg', 0, .5, 'PHOTO : Zlatan Ibrahimović, 2013 (Commons, CC BY-SA 3.0)'),
 ('del', 'photos/photo-buffon-07.jpg', 0, .5, 'PHOTO : Gianluigi Buffon, 2016 (Commons, CC BY 2.0)'),
 ('trézéguet', 'photos/photo-delpiero-01.jpg', 0, .5, 'PHOTO : Alessandro Del Piero sous le maillot de la Juventus, 2008 (Commons, CC BY 2.0)'),
 ('et', 'photos/photo-trezeguet-01.jpg', 0, .5, 'PHOTO : David Trezeguet, 2017 (Commons, CC BY 2.0)'),
 ('le', P(30099008), 5.0, .5, 'Stade vu du ciel : la Juve remonte'),
 ('sauf', P(6532230), 2.0, .5, 'Main qui prend un trophée doré : le titre file à l’Inter'),
 ('trop', P(38826405), 5.0, .5, 'Rotative : un procureur accuse aussi l’Inter (stade de Beşiktaş 37342407 écarté)'),
 ('et', P(39740462), 1.0, .5, 'Stade vide : prescrit'),
 ('au', O(40867851), 15.0, .5, 'Stade éclairé vu du ciel : Moggi radié à vie'),
 ('alors', P(2249402), 10.0, .5, 'Stade vide sous les projecteurs : prescription'),
 ('réponds', P(30099008), 20.0, .5, 'Stade vu du ciel : tricheuse ou bouc émissaire ?'),
 (None, O(40867851), 25.0, .5, 'Fin : stade éclairé vu du ciel'),
]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], -1
for anchor, s, t, c, n, *zone in rows:
    end = None
    if anchor:
        for w in (anchor if isinstance(anchor, tuple) else (anchor,)):
            cursor = find(w, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plan = dict(fin=end, source=S + s + ('' if s.endswith(('.jpg', '.png')) else '.mp4'), entree=t, cadrage=c, note=n)
    if zone:
        plan['zone'] = zone[0]
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
