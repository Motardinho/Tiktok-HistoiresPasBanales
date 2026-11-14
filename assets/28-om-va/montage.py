"""Plans du dossier 28, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère
précédent. Sources : Pexels uniquement (licence Pexels), vertical natif >= 1080x1920 ou 4K.
Illustrations génériques : aucun plan ne montre OM-VA, ses joueurs ni la Réunion.
"""
import json
import re
from pathlib import Path

m = Path('out/28-om-a-achete-un-match/_montage')
S = '28-om-va/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('et', P(39593839), 0.5, .5, 'Hook : frappe de balle de nuit sous les projecteurs (illustration, pas OM-VA)'),
 ('enterrée', P(40867851), 26.0, .5, 'Stade éclairé vu du ciel : « la preuve »'),
 ('mai', P(36906604), 1.0, .5, 'Pelle qui creuse : « enterrée dans un jardin »'),
 ("l'om", P(40867849), 4.0, .5, 'Mai 1993 : stade de nuit vu du ciel'),
 ('finale', 'photos/photo-tapie-1994.jpg', 0, .5, 'PHOTO : Bernard Tapie, député européen, 1994 (Parlement européen, Commons)'),
 ('dans', P(35970583), 10.0, .5, 'Terrain éclairé vu du ciel : la finale dans six jours'),
 ('mais', P(40867851), 3.0, .5, 'Stade lointain dans la nuit : finale dans six jours'),
 ('la', P(35970583), 2.0, .5, 'Terrain éclairé vu du ciel : un match à Valenciennes'),
 ('le', P(10397449), 0.3, .5, 'Vieux téléphone rouge décroché : le coup de fil'),
 ('levez', P(7119842), 4.0, .5, 'Main qui tortille le fil du téléphone : le message'),
 ('deux', P(6084023), 1.0, .5, 'Joueur qui marche balle au pied : lever le pied'),
 ('sur', P(7592161), 4.0, .5, 'Combiné raccroché : deux disent oui'),
 ("l'enveloppe", P(36248857), 3.0, .5, 'Voiture sur un parking de nuit'),
 ('le', P(11321634), 3.0, .5, 'Enveloppe noire entre deux mains (avant tout billet), clavier coupé', 'crop=iw:ih*0.82:0:ih*0.18'),
 ('et', P(39593839), 8.5, .5, 'Joueur de dos, seul sous les projecteurs : il refuse (pas de visage pour ne pas passer pour Glassmann)'),
 ("l'om", P(28186504), 0.5, .5, 'Photographes en rafale : il va tout balancer'),
 ('puis', P(40867849), 25.0, .62, 'L’OM gagne : match vu du ciel'),
 ('sauf', P(37622460), 1.0, .35, 'Feu d’artifice sur un stade : champion d’Europe'),
 ('les', P(30008290), 1.0, .5, 'Pluie de nuit sur des voitures : un mois après'),
 ('dans', P(36906606), 2.0, .5, 'Pelle qui creuse : les enquêteurs déterrent'),
 ('et', P(9323231), 1.0, .5, 'Homme qui creuse dans un jardin (illustration)'),
 ('puis', 'photos/photo-tapie-1994.jpg', 10, .5, 'PHOTO : Bernard Tapie, 1994 (Parlement européen, Commons) : Tapie nie tout'),
 (('il', 'il'), P(28186504), 3.5, .5, 'Flashs de la presse : la phrase au procès'),
 ("l'om", P(10475256), 1.0, .5, 'Barreaux de cellule, détenu de dos : la prison'),
 ('et', P(7005912), 1.0, .5, 'Trophée de foot : il perd son titre'),
 ('mais', P(40867851), 10.0, .5, 'Stade lointain dans la nuit : deuxième division (stade marocain identifiable écarté)'),
 ('et', P(13082848), 3.0, .5, 'Feu d’artifice au stade : la Ligue des champions, il la garde'),
 ('surnommé', P(9017833), 4.5, .5, 'Pouce vers le bas : sifflé'),
 ('il', P(35701014), 4.5, .5, 'Photographes : « la balance »'),
 (('la', 'la'), P(6084023), 7.0, .5, 'Fin de carrière : ballon et but, entraînement (pas la Réunion, aucune vidéo trouvée)'),
 ('alors', P(11321634), 17.8, .5, 'Fun fact : enveloppe refermée, 1 franc, clavier coupé', 'crop=iw:ih*0.82:0:ih*0.18'),
 ('réponds', P(40867849), 40.0, .5, 'Héros ou balance ? Stade vu du ciel'),
 (None, P(40867851), 30.0, .5, 'Fin : stade de nuit'),
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
