"""Plans du dossier 32, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Sources : Pexels uniquement (licence Pexels), vertical natif >= 1080x1920, BT.709.
Illustrations génériques : aucun plan ne montre l'équipe d'Espagne de 2000, le match réel,
Carlos Ribagorda ni les dirigeants. Écartés : arénas à logos (26626901, 34359956), journaux à
titres lisibles (38071228, 10449873), portrait barbe et casquette (9723909, inconnu identifiable),
plans de joueuses pour une équipe masculine, sources horizontales 1080p, 2 HDR, 2 en 720p.
"""
import json
import re
from pathlib import Path

m = Path('out/32-espagne-a-vole-or-paralympique/_montage')
S = '32-faux-handicapes/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('dix', P(6777262), 0.3, .5, 'Hook : ballon qui traverse le filet, en action à 0:00'),
 ('aucun', P(10341422), 9.5, .5, 'Joueur qui dribble dans la pénombre (silhouette) : 10 joueurs sur 12'),
 ('sydney', P(6265092), 1.0, .5, 'Médaille d’or tenue en main, au-dessus des sous-titres : aucun handicap, et l’or'),
 ('basket', P(36427881), 5.0, .5, 'Opéra de Sydney'),
 ("l'espagne", P(5586530), 4.5, .5, 'Match sur terrain extérieur, tir : basket'),
 ('quatre-vingt-sept', P(32067896), 12.8, .5, 'Dunk : l’Espagne écrase tout'),
 ('sauf', P(6536350), 12.0, .5, 'Tableau de score en salle (score générique, pas celui de la finale)'),
 ('journaliste', P(5275554), 13.0, .5, 'Groupe de joueurs sur un terrain : dans l’équipe'),
 ('carlos', P(12894347), 2.0, .5, 'Mains sur un clavier : journaliste infiltré'),
 ('et', P(6143906), 1.0, .5, 'Machine à écrire'),
 ('le', P(39134702), 1.0, .5, 'Rotative : il va tout balancer'),
 ('il', P(8814707), 3.0, .5, 'Dossier ouvert sur un bureau : le test'),
 ('une', P(10483840), 9.5, .5, 'Pompes en extérieur, visage tourné vers le sol : six pompes (6455340 écarté : visage en gros plan)'),
 ('aucun', P(5722110), 27.0, .5, 'Brassard de tensiomètre : prise de tension'),
 ('et', P(7659130), 7.0, .5, 'Prise de tension vue de dessus : aucun test de QI'),
 ('selon', P(5275544), 0.3, .5, 'Action de jeu : accroche-toi'),
 ("l'équipe", P(5275561), 2.5, .5, 'Action de jeu : en plein match'),
 ('le', P(6536350), 19.0, .5, 'Tableau de score : plus de 30 points'),
 ('pour', P(5275549), 9.5, .5, 'Joueurs à l’arrêt : lever le pied'),
 ('le', P(10341422), 1.0, .5, 'Dribble lent dans la pénombre : ne pas éveiller les soupçons'),
 ('consigne', P(37651037), 9.5, .5, 'Avion à l’approche : au retour'),
 ('barbe', P(13790665), 5.0, .5, 'Hall d’aéroport, voyageurs : consigne des dirigeants'),
 ('pour', P(32473991), 0.5, .5, 'Aérogare vue de haut : barbe, casquette, lunettes (aéroport générique, pas Barajas)'),
 ('raté', P(13790665), 8.9, .5, 'Hall d’aéroport : à l’aéroport'),
 ('la', P(39134701), 1.0, .5, 'Rotative : un journal publie'),
 ('et', P(39134702), 5.0, .5, 'Pages imprimées : la photo de l’équipe'),
 ("l'espagne", P(39134701), 6.0, .5, 'Rotative : des lecteurs reconnaissent'),
 ('et', P(6120372), 0.3, .5, 'Médaille d’or et main : rendre l’or'),
 ('treize', P(8814707), 5.2, .5, 'Signature d’un document : le patron de la fédération'),
 ('sa', '32-festina/pexels-6101349', 1.0, .5, 'Marteau de juge : il avoue'),
 ('les', '31-pogba/pexels-29992749', 3.0, .5, 'Billets en euros : 5 400 euros d’amende'),
 ('bannis', P(9145019), 2.0, .5, 'Vestiaire vide : les vraies victimes'),
 ('et', P(10397706), 0.3, .5, 'Panier seul : bannis des Jeux'),
 ('alors', P(6120372), 5.0, .5, 'Médaille d’or sur fond noir : ils perdent leur titre (7005888 écarté : marque lisible sur le ballon)'),
 ('héros', P(6143906), 6.0, .5, 'Machine à écrire : le journaliste'),
 ('réponds', P(6265085), 1.0, .5, 'Médaille d’or au bout de son ruban : héros ou complice ?'),
 ('pas', P(6777262), 8.0, .5, 'Ballon dans le filet : réponds en un mot'),
 (None, P(5586712), 0.5, .5, 'Fin : terrain vu de haut'),
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
