"""Plans du dossier 26, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère
précédent. Sources : Pexels (licence Pexels) en vertical natif >= 1080x1920 ou 4K,
et passages 4K CC BY de la vidéo YouTube K_blduG9eiU (Marathon des Sables, Massi Milani),
sans les passages portant un repère kilométrique incrusté.
"""
import json
import re
from pathlib import Path

m = Path('out/26-perdu-9-jours-dans-le-sahara/_montage')
S = '26-perdu-sahara/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('parti', P(17230362), 2.0, .5, 'Hook : sable arraché par le vent contre le ciel'),
 ('il', P(29481814), 1.0, .5, 'Coureur seul au loin dans le désert (illustration, pas Prosperi)'),
 ('et', P(20636703), 2.0, .5, 'Montagnes arides : « retrouvé en Algérie »'),
 ('avril', P(33766127), 2.0, .5, 'Silhouette minuscule sur l’horizon : le doute'),
 ('mauro', 'mds-326', 0.0, .5, 'Désert du Marathon des Sables, caméra en course'),
 ('quarante-six', 'mds-800', 14.4, .45, 'Coureur du MDS vu d’en haut dans le sable'),
 ('puis', 'mds-8', 0.0, .5, '46 degrés : soleil écrasant sur le désert'),
 ('huit', P(27740324), 12.0, .5, 'La tempête se lève : sable soufflé'),
 ('quand', P(31448827), 0.5, .5, 'Huit heures sans rien voir : sable en mouvement'),
 ('plus', P(18897114), 1.0, .5, 'Le vent tombe : dunes dans la brume'),
 ('plus', P(8865368), 1.0, .5, 'Plus de piste : sable lisse'),
 ('sa', P(36259626), 8.0, .5, 'Plus personne : Sahara vide'),
 ('alors', P(7624037), 1.0, .5, 'La gourde se vide : sable qui coule des mains'),
 ('un', P(8865213), 2.0, .5, 'Il boit à la bouteille (illustration), route masquée', 'crop=iw*0.75:ih*0.75:0:0'),
 ('il', P(39872733), 3.0, .5, 'Un hélicoptère passe'),
 ('personne', P(39926234), 2.0, .5, 'Signal de détresse fumigène, sol masqué', 'crop=iw*0.5:ih*0.5:iw*0.25:0'),
 ('il', P(39535967), 3.0, .5, 'L’hélicoptère s’éloigne, minuscule'),
 (('abandonné', 'dans'), P(35626497), 0.3, .5, 'Bâtiment abandonné (illustration générique du sanctuaire)'),
 ("d'après", P(27787008), 0.5, .5, 'Chauves-souris suspendues'),
 (('sang', 'il'), P(27787008), 4.0, .5, 'Chauve-souris en gros plan'),
 ('pourtant', P(29182492), 4.0, .5, 'Message d’adieu : main dans le sable'),
 ('le', P(19688516), 0.5, .5, 'Il repart vers le soleil'),
 ('le', P(32177425), 0.5, .5, 'Huitième jour : de l’eau'),
 ('elle', P(14257968), 4.0, .5, 'Neuvième jour : des chèvres'),
 ('dans', P(27740324), 20.0, .5, 'Crête de dune vide balayée par le vent : elle a disparu'),
 (('os', 'il'), P(5103847), 5.0, .5, 'Reflet dans un miroir posé sur le sable'),
 ('et', P(36259626), 1.0, .5, 'Algérie, près de 300 km : immensité du Sahara'),
 ('il', 'mds-326', 2.5, .5, 'Fun fact : caméra en course dans les dunes du MDS'),
 ('mais', 'mds-240', 10.3, .5, 'Fun fact : coureurs du Marathon des Sables au lever du soleil, avant l’arche MDS Ultra'),
 ('fondateur', P(17230362), 9.0, .5, 'Sable lâché dans le vent'),
 ('toi', P(8865368), 3.0, .5, 'Dunes vides'),
 (None, P(33766127), 9.0, .5, 'Fin : silhouette seule sur l’horizon'),
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
    plan = dict(fin=end, source=S + s + '.mp4', entree=t, cadrage=c, note=n)
    if zone:
        plan['zone'] = zone[0]
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
