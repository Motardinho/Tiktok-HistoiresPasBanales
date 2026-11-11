"""Plans du dossier 31, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère
précédent. Sources : Pexels uniquement (licence Pexels), vertical natif >= 1080x1920.
Illustrations génériques : aucun plan ne montre Paul ou Mathias Pogba, les prévenus, Mbappé,
le tribunal de Paris ni l'appartement de Montévrain. Aucun visage identifiable qui pourrait
passer pour une personne de l'affaire.
"""
import json
import re
from pathlib import Path

m = Path('out/31-pogba-braque-pour-13-millions/_montage')
S = '31-pogba/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('et', P(6091316), 3.0, .5, 'Hook : arme braquée vers la caméra dans la pénombre (illustration ; groupe cagoulé avec casque et gilet tactique écarté, pouvait passer pour la police)'),
 ('son', P(29992749), 1.0, .5, 'Billets en euros qui tombent : 13 millions'),
 ('mars', P(39917292), 7.0, .5, 'Silhouette encapuchonnée, visage dans l’ombre : son propre frère'),
 ('retrouve', P(35970585), 5.0, .5, 'Terrain éclairé vu du ciel : champion du monde'),
 ('et', P(6016323), 0.3, .5, 'Immeuble de nuit, fenêtres éclairées : la soirée entre potes'),
 ('deux', P(4547598), 1.0, .5, 'Porte ouverte sur une pièce sombre : accroche-toi'),
 ('armes', P(6670907), 18.0, .5, 'Gros plan d’une cagoule : deux hommes cagoulés'),
 ('le', P(6091316), 8.0, .5, 'Arme braquée vers la caméra : armes pointées sur lui'),
 ('pogba', P(31402662), 2.0, .5, 'Liasse d’euros comptée : le prix'),
 ('les', P(8860241), 3.0, .5, 'Silhouette assise, tête dans les mains : « tu dis oui à tout »'),
 ('mais', P(29992746), 1.0, .5, 'Billets en euros : les 13 millions jamais payés'),
 ('près', P(4836403), 4.0, .5, 'Billets de 50 euros qui tombent : selon l’enquête (zlotys polonais de 34812223 écartés)'),
 ('le', P(31402662), 14.0, .5, 'Liasse d’euros : 250 000 euros'),
 ('six', P(8308012), 2.0, .5, 'Portants de vêtements en boutique : la virée shopping (enseigne SK LAND de 40723961 écartée pendant « Adidas »)'),
 ('plus', P(6565836), 0.5, .5, 'Sacs de boutique à la main (sans visage) : 633 articles'),
 ('pogba', P(9595330), 2.5, .5, 'Sacs tendus au comptoir (mains seules) : 57 000 euros'),
 ('et', P(6170608), 0.3, .5, 'Cartons chargés dans un utilitaire : Pogba paie la différence'),
 ('en', P(39917302), 5.0, .5, 'Silhouette encapuchonnée de dos : le frère, Mathias'),
 (('il', 'il'), P(38410499), 12.0, .5, 'Main qui fait défiler des vidéos sur un téléphone : il balance des vidéos'),
 ('marabouter', P(31777302), 1.0, .5, 'Rangées de bougies rouges : l’accusation'),
 ('paul', P(33997119), 2.0, .5, 'Bougies dans la pénombre : marabouter Mbappé'),
 ('décembre', P(8860241), 12.0, .5, 'Silhouette assise : Paul dément'),
 ('les', P(10475367), 3.0, .5, 'Menottes retirées dans une cellule : le verdict'),
 ('mathias', P(6904057), 0.5, .5, 'Cagoule sur fond neutre : jamais identifiés'),
 ('il', P(19436637), 1.0, .5, 'Chemin de nuit, lampe lointaine : absent ce soir-là'),
 ('et', P(7646797), 0.2, .5, 'Clé tournée dans une porte : peine à domicile, appel annoncé puis abandonné'),
 ('mais', P(7984191), 2.0, .5, 'Rangées de sièges vides : même pas venu au procès'),
 ('longue', P(10374888), 0.5, .5, 'Galerie de photos de paysages sur un téléphone : il poste une photo avec ses frères (fil 38410501 écarté : femme et vignette fitness à l’écran)'),
 ('alors', '28-om-va/pexels-40867851', 18.0, .5, 'Stade éclairé vu du ciel : longue vie à mes frères (stade de Fenerbahçe 34514063 écarté)'),
 ('réponds', P(40867848), 28.0, .5, 'Stade vu du ciel : tu aurais pardonné ?'),
 (None, P(35970584), 0.5, .5, 'Fin : terrains éclairés vus du ciel'),
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
    plan = dict(fin=end, source=(s if '/' in s else S + s) + '.mp4', entree=t, cadrage=c, note=n)
    if zone:
        plan['zone'] = zone[0]
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
