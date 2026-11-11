"""Plans du dossier 25, accrochés aux mots de timings-oraux.json.

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère
précédent : le découpage suit la voix même après une nouvelle synthèse.
"""
import json
import re
from pathlib import Path

m = Path('out/25-montagnes-russes-plus-rapides/_montage')
S = '25-montagnes-russes/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?]+$", '', w['w'].lower()) for w in words]

# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note) ; None = dernier plan
rows = [
 ('attache', 'ZSrHdILQkpc', 92.6, .5, 'Accroche : sommet de Top Thrill 2, vue plongeante sur le parc (aucun nom)'),
 ('numéro', 'ZSrHdILQkpc', 74.0, .5, 'Accroche : montée arrière, vue verticale sur la gare'),
 ('à', 'gW19l3OMbbE', 147.4, .55, 'N°3 : entrée « Top Thrill 2 » à Cedar Point'),
 ('cent', 'gW19l3OMbbE', 175.1, .55, 'N°3 : la tour de 130 m'),
 ('puis', 'ZSrHdILQkpc', 46.0, .5, 'N°3 : lancement vers l’avant, bras levés'),
 ('puis', 'ZSrHdILQkpc', 64.0, .5, 'N°3 : retour en arrière'),
 ('et', 'ZSrHdILQkpc', 82.0, .5, 'N°3 : nouveau départ vers l’avant, tour en face'),
 ('mètres', 'ZSrHdILQkpc', 86.0, .5, 'N°3 : montée verticale'),
 ('numéro', 'gW19l3OMbbE', 118.6, .52, 'N°3 : le train au sommet de la tour, vue extérieure'),
 ('ferrari', 'PED5EcH6mRU', 30.0, .55, 'N°2 : le train Formula Rossa en gare, derrière la vitre'),
 ('kilomètres-heure', 'Bg7GV5m8cd0', 58.0, [[0, .75], [1.0, .6], [2.72, .45]], 'N°2 : le train rouge sous le toit de Ferrari World'),
 ('elle', 'Bg7GV5m8cd0', 73.4, .3, 'N°2 : départ de la gare, lancement à 76 s source'),
 ('ici', 'K2AiJrgOp_k', 66.0, [[0, .55], [2.88, .66]], 'N°2 : le train passe de près'),
 ('désert', 'ijuQwnfBBZw', 48.4, .66, 'Fun fact : passager avec lunettes de protection, visage haut dans le cadre'),
 ('mais', 'ijuQwnfBBZw', 35.0, [[0, .3], [5.88, .68]], 'Fun fact : les deux pilotes Ferrari à bord, panoramique de gauche à droite'),
 (('vite', 'numéro'), 'Q7Atm5C15zg', 126.5, .5, 'Relance : vue de nuit très haut au-dessus de la ville (sans nom)'),
 ('deux', 'cUURkqyn4Zs', 56.8, .5, 'N°1 : Falcons Flight, tour et falaises du désert'),
 ('ouverte', 'cUURkqyn4Zs', 143.6, .5, 'N°1 : passage rapide au-dessus du parc'),
 ('plus', 'cUURkqyn4Zs', 64.0, .5, 'N°1 : virage dans la structure'),
 (('monde', 'plus'), 'cUURkqyn4Zs', 73.0, .5, 'N°1 : très haut au-dessus du parking'),
 ('elle', 'cUURkqyn4Zs', 100.0, .5, 'N°1 : rails le long de la falaise'),
 ('puis', 'cUURkqyn4Zs', 81.0, .5, 'N°1 : montée vers la falaise'),
 (('vide', 'le'), 'cUURkqyn4Zs', 119.0, .5, 'N°1 : au bord de la falaise'),
 ('toi', 'cUURkqyn4Zs', 123.9, .5, 'N°1 : plongée verticale dans le tunnel (tunnel visible à 126,4 s source, sur le mot « tunnel »)'),
 (None, 'cUURkqyn4Zs', 131.0, .5, 'Fin : sortie du tunnel'),
]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], 0
for anchor, s, t, c, n in rows:
    end = None
    if anchor:
        for w in (anchor if isinstance(anchor, tuple) else (anchor,)):
            cursor = find(w, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plans.append(dict(fin=end, source=S + s + '.mp4', entree=t, cadrage=c, note=n))
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
