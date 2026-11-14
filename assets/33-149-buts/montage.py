"""Plans du dossier 33, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Sources : Pexels uniquement (licence Pexels), vertical natif >= 1080x1920 ou 4K, BT.709.
Illustrations génériques : aucun plan ne montre le match AS Adema - SO de l'Emyrne de 2002,
les deux clubs, l'entraîneur ni l'arbitre. Écartés : 2 sources en 720p, 2 horizontales 1080p,
1 HDR, plans de joueuses pour des équipes masculines, ballon à marque lisible (37568235).
"""
import json
import re
from pathlib import Path

m = Path('out/33-149-buts-contre-leur-camp/_montage')
S = '33-149-buts/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
A = lambda d, i: f'../{d}/pexels-{i}'
ARBITRE = A('30-calciopoli', 40551621)
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('cent', P(6077714), 6.3, .5, 'Hook : frappe face au gardien, en action à 0:00'),
 ('contre', P(6084018), 6.4, .5, 'Tir et plongeon du gardien : 149 buts'),
 ('exprès', P(6077696), 0.4, .5, 'Frappe en gros plan : contre leur camp'),
 ('et', P(6077705), 1.6, .5, 'Joueur de dos qui frappe : exprès'),
 ('madagascar', P(12460620), 0.8, .5, 'Joueurs à l’arrêt sur un terrain : personne n’a bougé'),
 ('phase', P(38870678), 4.0, .5, 'Lémurs catta, emblème de Madagascar (lieu de tournage non précisé)'),
 ("l'émirne", P(34841978), 1.0, .5, 'Équipes alignées avant un match (stade générique) : championnat national'),
 ('joue', A('28-om-va', 7005912), 1.0, .5, 'Trophée de foot : champion en titre'),
 ('en', P(36296347), 4.0, .5, 'Équipes qui entrent sur le terrain : joue le titre'),
 ("l'arbitre", P(29724548), 1.0, .5, 'Match vu de loin : en fin de match'),
 ('penalty', ARBITRE, 3.2, .5, 'Arbitre sur un terrain (match amateur, pas celui de 2002)'),
 ('égalisation', P(6084017), 2.8, .5, 'Tireur de dos face au but : penalty'),
 ('titre', P(11271465), 6.0, .5, 'Jeu vu à travers les filets : égalisation'),
 ('le', P(10349018), 0.3, .5, 'Joueur assis sur un ballon, tête basse : titre perdu'),
 ('et', P(6078635), 1.5, .5, 'Entraîneur debout devant ses joueurs (illustration, pas le coach de l’Emyrne)'),
 ('pour', A('30-calciopoli', 38826405), 0.5, .5, 'Rotative : selon la presse locale'),
 ('dernière', P(6078635), 9.0, .5, 'Entraîneur et joueurs : il a un plan'),
 ('ses', P(6079620), 0.5, .5, 'Rond central vu de haut : dernière journée, coup d’envoi'),
 ('se', P(6077720), 0.4, .5, 'Joueurs en mouvement : ils récupèrent le ballon'),
 ('et', P(6084019), 2.5, .5, 'Joueur de dos, balle au pied : ils se retournent'),
 ('engagement', P(6077715), 11.9, .5, 'Frappe et ballon au fond des filets : dans leur propre but (12689679 écarté : panneaux publicitaires)'),
 ('rebelote', P(12788730), 0.6, .5, 'Pied posé sur le ballon : engagement'),
 ('encore', P(6078257), 16.0, .5, 'Frappe : rebelote'),
 ('et', P(6077696), 3.0, .5, 'Frappe en gros plan : encore'),
 ('un', P(31430984), 0.3, .5, 'Ballon derrière les filets : accroche-toi'),
 ('en', P(6077714), 0.5, .5, 'Fun fact : gardien face au ballon, sous l’encart'),
 ('regarde', P(12460620), 4.5, .5, 'Joueurs à l’arrêt : l’Adema regarde'),
 ("l'arbitre", P(6077715), 7.0, .5, 'Gardien immobile face au ballon : planté là'),
 ('personne', ARBITRE, 4.2, .5, 'Arbitre : l’arbitre aussi'),
 (('le', 'le'), P(29724548), 8.0, .5, 'Match vu de loin : personne n’arrête le massacre'),
 (('les', 'les'), P(9374370), 0.3, .5, 'Stade et tribunes : dans les tribunes'),
 ('pour', P(16472277), 0.2, .5, 'Tribune debout : les spectateurs foncent (34452575 et 34452568 écartés : maillots et drapeau du Maroc, nom d’un joueur lisible)'),
 ('score', P(9374370), 2.2, .5, 'Stade et tribunes : se faire rembourser (aucun plan libre de guichet de stade)'),
 ('la', P(31430984), 2.05, .5, 'Ballon au fond des filets : score final, 149 à 0'),
 ('le', A('32-festina', 6101349), 1.0, .5, 'Marteau de juge : la fédération'),
 ('interdit', P(6078635), 14.0, .5, 'Entraîneur : trois ans de suspension (illustration)'),
 ('des', A('30-calciopoli', 2249402), 1.0, .5, 'Stade vide : interdit de stade'),
 ('et', P(10349018), 2.0, .5, 'Joueur assis sur un ballon : joueurs suspendus'),
 ('alors', ARBITRE, 11.0, .5, 'Arbitre : rien'),
 ('génie', P(6078635), 5.5, .5, 'Entraîneur : ce coach'),
 ('ou', P(6084019), 6.4, .5, 'Joueur bras écartés : génie de la protestation'),
 ('réponds', A('30-calciopoli', 39740462), 1.0, .5, 'Stade vide : honte du football ?'),
 ('pas', A('28-om-va', 40867849), 40.0, .5, 'Stade vu du ciel : réponds en un mot'),
 (None, P(6077714), 9.0, .5, 'Fin : but vide'),
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
    plan = dict(fin=end, source=(s[3:] if s.startswith('../') else S + s) + '.mp4', entree=t, cadrage=c, note=n)
    if zone:
        plan['zone'] = zone[0]
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
