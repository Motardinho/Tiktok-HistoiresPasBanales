"""Plans du dossier 37, accrochés aux mots de timings-oraux.json (méthode des dossiers 25 et 30).

Archives officielles (archives.py) : 20 heures de France 2 (INA), L’Équipe, Téléfoot (TF1), FRANCE 24, AFP.
Vidéos : Pexels (licence Pexels) et vol FPV dans le Stade de France (Kevin Lomprez, Commons, CC BY 3.0).
Photos : Wikimedia Commons, dont deux photos réelles du match du 18 novembre 2009.
"""
import json
import re
from pathlib import Path

m = Path('out/37-la-fifa-a-paye-pour-la-main-d-henry/_montage')
S = '37-main-henry/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}.mp4'
F = 'stade-de-france-fpv.webm'
A = lambda k: f'arch-{k}.mp4'  # extraits officiels préparés par archives.py
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('main', A('leq-hook'), 0, .5, 'ARCHIVE : Henry, le ballon contre la main devant le but (L’Équipe, 19/11/2025)'),
 ('cinq', 'photos/photo-henry12b.jpg', 0, .71, 'PHOTO : Thierry Henry lève la main, Arsenal, 4 février 2012 (Commons, CC BY 2.0)'),
 ('personne', P(855388), 1.0, .5, 'Billets en euros : cinq millions (illustration ; la FIFA parle de dollars)'),
 ('novembre', 'photos/photo-fifa10.jpg', 0, .3, 'PHOTO : siège de la FIFA à Zurich, 2011 (Commons, CC BY-SA 3.0)'),
 ('barrage', F, 10.0, .5, 'Stade de France réel : tribunes vues du toit (vol FPV 2021)'),
 ('france', F, 32.6, .5, 'Stade de France réel : pelouse et tribunes (vol FPV 2021)'),
 ('irlande', A('ina-france'), 0, .5, 'ARCHIVE : France-Irlande en direct, plan large (images TF1 dans le 20 heures de France 2 du 19/11/2009, INA)'),
 ('les', P(38817231), 0.5, .57, 'Drapeau irlandais dans une rue de Dublin'),
 ('mais', P(4003023), 2.0, .5, 'Dublin vu du ciel : le match aller'),
 ('robi', A('leq-keane'), 0, .5, 'ARCHIVE : but de Robbie Keane (L’Équipe), score exclu'),
 ('prolongation', 'photos/photo-keane13b.jpg', 0, .52, 'PHOTO : Robbie Keane (n°10) avec l’Irlande, 10 septembre 2013 (Michael Kranewitter, Commons, CC BY-SA 3.0 AT)'),
 ('cent', A('ina-large'), 0, .5, 'ARCHIVE : le match en direct, plan large (20 heures, INA)'),
 ('un', P(40867851), 0.5, .5, 'Stade éclairé vu du ciel : 103e minute (illustration)'),
 ('thierry', A('ina-arrive'), 0, .5, 'ARCHIVE : ralenti, le ballon arrive sur Henry (20 heures, INA)'),
 ('contrôle', A('ina-henry'), 0, .5, 'ARCHIVE : ralenti, Henry (n°12) contrôle de la main (20 heures, INA)'),
 ('deux', A('leq-main'), 0, .5, 'ARCHIVE : gros plan, la main d’Henry sur le ballon (L’Équipe)'),
 ('il', A('leq-main2'), 0, .5, 'ARCHIVE : deuxième touche, devant le gardien Shay Given (L’Équipe)'),
 ('william', A('ina-centre'), 0, .5, 'ARCHIVE : le centre vers Gallas (20 heures, INA)'),
 ('la', 'photos/photo-gallas-but.jpg', 0, [[0, .42], [3.2, .8]], 'PHOTO RÉELLE du match : Gallas fête son but, Kevin Kilbane réclame la main, 18 novembre 2009 (Nicolas Richoffer, CC BY-SA 4.0)'),
 ('le', A('leq-joie'), 0, .5, 'ARCHIVE : Henry exulte après l’égalisation (L’Équipe), texte incrusté exclu'),
 ('henri', A('tf1-fin'), 0, .5, 'ARCHIVE : après le match, Henry et Domenech sur la pelouse (Téléfoot, TF1)'),
 ("l'irlande", A('ina-interview'), 0, .5, 'ARCHIVE : Henry au micro le soir du match (20 heures de France 2, INA)'),
 ('refusé', P(38817231), 2.0, .57, 'Drapeau irlandais à Dublin : l’Irlande exige de rejouer'),
 ('alors', 'photos/photo-fifa10.jpg', 50, .3, 'PHOTO : siège de la FIFA (autre passage) : refusé'),
 ('trente-troisième', P(4003023), 12.0, .5, 'Dublin vu du ciel : la demande irlandaise'),
 ('mais', P(27561584), 1.0, .5, 'Stade éclairé vu du dessus : 33e équipe'),
 ('le', A('f24-unes'), 0, .5, 'ARCHIVE : unes des journaux irlandais, « Le Cheat » (FRANCE 24, 2015)'),
 ('la', A('f24-delaney'), 0, .5, 'ARCHIVE : John Delaney, patron de la fédération irlandaise (FRANCE 24, 2015), bandeau exclu'),
 ('cinq', A('f24-fifa'), 0, .5, 'ARCHIVE : siège de la FIFA (FRANCE 24, 2015)'),
 ('pour', P(855388), 7.0, .5, 'Billets en euros : cinq millions (illustration)'),
 ('la', P(6101337), 0.5, .5, 'Marteau de juge et contrat : renoncer au procès (illustration)'),
 ('construire', A('f24-fifa2'), 0, .5, 'ARCHIVE : siège de la FIFA (FRANCE 24, 2015) : la version de la FIFA'),
 (('stade', 'un'), P(5629558), 8.0, .5, 'Aviva Stadium de Dublin vu du ciel : un stade (la FAI dit que l’argent a financé ce stade)'),
 ('et', P(6101337), 4.5, .5, 'Document signé : un prêt effacé (illustration)'),
 ('qualifiés', P(2249402), 9.0, .5, 'Stade vide de nuit : le karma frappe (illustration)'),
 ('les', A('ina-angle2'), 0, .5, 'ARCHIVE : la main, deuxième angle derrière le but (20 heures, INA) : qualifiés grâce à une main'),
 ('dernière', A('afp-bus'), 0, .5, 'ARCHIVE : Knysna, les Bleus quittent l’entraînement et regagnent leur bus (AFP, 21/06/2010)'),
 ('la', A('afp-domenech'), 0, .5, 'ARCHIVE : Knysna, Domenech seul face à la presse (AFP, 21/06/2010)'),
 ('réponds', 'photos/photo-henry07.jpg', 100, .42, 'PHOTO : Thierry Henry qui applaudit, 2007 (Commons, CC BY 2.0) : triche ou réflexe ?'),
 ('pas', F, 4.6, .5, 'Stade de France réel (vol FPV 2021) : réponds en un mot'),
 (None, P(40867851), 9.0, .5, 'Fin : stade éclairé vu du ciel'),
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
    plan = dict(fin=end, source=S + s, entree=t, cadrage=c, note=n)
    if zone:
        plan['zone'] = zone[0]
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
