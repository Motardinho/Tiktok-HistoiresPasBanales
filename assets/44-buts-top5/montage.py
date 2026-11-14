"""Plans du dossier 44 : chaque rang enchaîne ses extraits sans trou, du direct au ralenti.

Les extraits `arch-*.mp4` (archives.py) sont des plans entiers du réalisateur d'origine. Dans un rang, ils se
suivent à leur durée réelle ; le dernier dure jusqu'au mot « numéro » suivant, où tombe le volet jaune.
Seule l'accroche (Pexels, sans révélation) est découpée sur des mots repères.
Lancer depuis la racine : python assets/44-buts-top5/montage.py
"""
import json
import re
import subprocess
from pathlib import Path

m = Path('out/44-top-5-buts-les-plus-degueulasses/_montage')
A = Path('assets/44-buts-top5')
S, P = '44-buts-top5/', '40-buts-degueulasses/'
timing = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))
words = timing['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower()) for w in words]


def find(word, start=0):
    i = next(i for i in range(start, len(tokens)) if tokens[i] == word)
    return i, round(words[i]['start'], 3)


def duree(key):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                          str(A / f'arch-{key}.mp4')], text=True))


# Débuts des rangs : les cinq « numéro » qui ouvrent une scène (le premier « numéro » est dans l'accroche).
numeros = [i for i, t in enumerate(tokens) if t == 'numéro']
direct = json.loads((m.parent / 'histoire.json').read_text(encoding='utf8')).get('depart_direct_classement', False)
assert len(numeros) == (5 if direct else 6), numeros
rangs = [round(words[i]['start'], 3) for i in (numeros if direct else numeros[1:])]
fin_n1 = find('kayne', find("l'a", numeros[-1])[0] - 2)[1]  # « Kane l'a touché : oui ou non ? »

plans = []
# Accroche : mêmes plans Pexels que le dossier 40, aucun nom ni but révélé.
if not direct:
    i1, t1 = find('le', 3)
    i2, t2 = find('réclamé', i1)
else:
    t1 = t2 = 0
for fin, src, entree, note in [(t1, P + 'pexels-6084018.mp4', 5.0, 'Accroche : gardien qui plonge (Pexels)'),
                               (t2, P + 'pexels-40867851.mp4', 3.0, 'Accroche : stade de nuit vu du ciel (Pexels)'),
                               (rangs[0], P + 'pexels-6077715.mp4', 11.0, 'Accroche : penalty tiré (Pexels)')]:
    if direct:
        continue
    row = dict(fin=fin, source=src, entree=entree, cadrage=.5, note=note)
    if 'pexels-6084018' in src:
        row['zone'] = 'crop=1215:2160:900:1100'
    plans.append(row)

# (début du bloc, fin du bloc, [(extrait, note), ...]) : le dernier extrait prend le temps restant.
blocs = [
 (rangs[0], rangs[1], [('green-direct', 'N°5 : Angleterre - États-Unis 2010, la frappe de Dempsey en direct, ballon au fond'),
                       ('green-ralenti', 'N°5 : ralenti au ras du sol d’un seul tenant, de la frappe au ballon qui glisse sous Rob Green et entre')]),
 (rangs[1], rangs[2], [('chicha-centre', 'N°4 : Community Shield 2010, Valencia déborde et centre'),
                       ('chicha-direct', 'N°4 : l’action en direct, plan large, jusqu’au but'),
                       ('chicha-ralenti', 'N°4 : ralenti, la reprise ratée, le ballon sur le visage, le but'),
                       ('chicha-joie', 'N°4 : Chicharito célèbre')]),
 (rangs[2], rangs[3], [('kiess-corner', 'N°3 : Hoffenheim - Leverkusen 2013, le corner'),
                       ('kiess-direct', 'N°3 : l’action en direct, la tête de Kießling, le ballon dans le but'),
                       ('kiess-ralenti', 'N°3 : ralenti derrière le but, le ballon passe à côté du poteau et entre par le filet')]),
 (rangs[3], rangs[4], [('bent-direct', 'N°2 : Sunderland - Liverpool 2009, l’action en direct, ballon de plage sur la pelouse'),
                       ('bent-ralenti', 'N°2 : ralenti, la frappe de Bent dévie sur le ballon de plage, but ; fun fact sur la fin')]),
 (rangs[4], fin_n1, [('kane-eriksen', 'N°1 : Stoke - Tottenham 2018, Eriksen tire le coup franc'),
                     ('kane-direct', 'N°1 : l’action en direct, le ballon au fond'),
                     ('kane-ralenti', 'N°1 : ralenti, le ballon passe devant Kane puis entre')]),
 (fin_n1, None, [('kane-reclame', 'Fin : Kane derrière le but réclame le but, puis célèbre')]),
]
MARGE = .07  # on quitte chaque extrait un peu avant sa dernière image
for debut, fin, rows in blocs:
    t = debut
    for k, (key, note) in enumerate(rows):
        last = k == len(rows) - 1
        d = duree(key) - MARGE
        end = fin if last else round(t + d, 3)
        if last and fin is not None:
            assert fin - t <= d + .001, (key, 'extrait trop court pour finir le rang', round(fin - t, 2), round(d, 2))
        if last and fin is None:
            assert timing['duration'] - t <= d + .001, (key, 'extrait trop court pour la fin', round(timing['duration'] - t, 2), round(d, 2))
        plans.append(dict(fin=end, source=S + f'arch-{key}.mp4', entree=0, cadrage=.5, note=note))
        t = end
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
print('rangs', rangs, 'fin n°1', fin_n1)
