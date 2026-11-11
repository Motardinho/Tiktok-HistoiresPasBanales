"""Plans du dossier 27, accrochés aux mots de timings-oraux.json (méthode des dossiers 25 et 26).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère
précédent. Sources : Pexels (licence Pexels) en vertical natif >= 1080x1920 ou 4K, et
archive INA « Les naufragés du Vendée Globe » (k791y4C_aGs, licence YouTube standard,
choix de Marc du 11 nov. 2026) pour les seuls plans authentiques de 1996 : épave
d'Algimouss et Dinelli sur le pont vus de l'avion, Pete Goss et Aqua Quorum.
Recadrage choisi pour exclure le filigrane « ina.fr » (bas droite). Les plans INA d'autres
marins (Poupon 1989, Bullimore, Dubois, Roufs) sont écartés.
"""
import json
import re
from pathlib import Path

m = Path('out/27-demi-tour-dans-la-tempete/_montage')
S = '27-demi-tour-tempete/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
INA = 'arch-k791y4C_aGs'
# Plans authentiques de 1996 : archive entière sur fond flou (1280x860 sans filigrane, agrandie x0,84),
# pré-rendue de 95 à 111 s par l'ffmpeg noté dans reperage.md ; entrée = seconde INA - 95.
CADRE = 'arch-cadre-95'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note) ; None = dernier plan
rows = [
 ('en', P(35371501), 9.6, .45, 'Hook : vague qui déferle en pleine mer'),
 ('un', INA, 12.2, .5, 'Archive non datée du Vendée Globe : houle énorme vue du pont'),
 (('français', 'un'), P(5417206), 8.0, .5, 'Un Anglais : marin en ciré rouge à la proue (illustration, pas Goss)'),
 ('droit', P(34646250), 1.0, .5, 'Étrave dans les embruns'),
 ('le', P(17786067), 1.0, .5, 'Ciel de tempête : « pas le droit d’être là »'),
 ('le', INA, 16.6, .5, 'Archive non datée du Vendée Globe : voilier gîté dans la tempête'),
 ('raphaël', P(4936487), 3.0, .5, 'Tour du monde en solitaire : voilier seul vu du ciel'),
 ('il', P(5417209), 2.0, .5, 'Proue d’un voilier par mer grise'),
 ('son', P(4936486), 10.0, .5, 'Il part quand même'),
 (('pirate', 'le'), P(11415810), 4.0, .5, 'Le pirate : ciel noir sur la mer'),
 ('le', INA, 20.0, .63, 'Mers du Sud : iceberg (archive non datée du Vendée Globe)'),
 ('son', P(35371501), 0.5, .5, 'Vent à plus de 130 km/h : crêtes arrachées'),
 ('le', P(9806390), 2.0, .5, 'Son bateau se retourne : mer déchaînée vue d’en haut'),
 ('trois', INA, 46.4, .5, 'Le mât sous l’eau : gréement couché sur la mer (archive non datée)'),
 ('et', P(39321062), 1.0, .5, 'Trois heures plus tard : houle sombre'),
 ('un', CADRE, 100.3 - 95, .5, 'AUTHENTIQUE 1996 : Dinelli debout sur le pont submergé d’Algimouss, vu de l’avion'),
 ('celui', P(19528653), 1.0, .5, 'Un seul bateau peut l’atteindre'),
 ('à', CADRE, 104.3 - 95, .5, 'AUTHENTIQUE : Aqua Quorum, le voilier jaune de Pete Goss, à quai'),
 ('goss', P(4936486), 20.0, .5, 'À près de 300 km : voilier minuscule'),
 ('droit', P(5417209), 9.0, .5, 'Goss fait demi-tour : proue dans la mer'),
 ('juste', P(34646250), 4.5, .5, 'Droit dans la tempête : embruns'),
 ('ne', P(9806390), 12.0, .5, 'Mer vue d’en haut'),
 ('goss', CADRE, 96.6 - 95, .5, 'AUTHENTIQUE 1996 : l’épave d’Algimouss vue de l’avion australien'),
 ('dinelli', P(39009187), 0.5, .5, 'Goss le retrouve : voilier dans les vagues'),
 ('une', P(5417074), 2.0, .5, 'Monte à bord : équipage sur le pont (illustration)'),
 ('il', P(8808262), 1.0, .5, 'Bouteille de champagne'),
 ('repart', P(4936487), 10.0, .5, 'Il le dépose en Australie'),
 ('et', P(5417206), 15.0, .5, 'Repart, finit cinquième'),
 ('et', CADRE, 107.0 - 95, .5, 'AUTHENTIQUE : Pete Goss accueilli, poignées de main'),
 ('goss', P(18924025), 2.0, .5, 'Fun fact : alliances, mariés flous à l’arrière-plan'),
 ('dinelli', P(18924025), 8.0, .5, 'Fun fact : témoin du mariage'),
 ('par', P(18924025), 14.0, .5, 'Fun fact : la demande'),
 (('sauveteur', 'le'), P(6100897), 8.0, .5, 'Fun fact : feuilles de papier (le fax)'),
 ("c'est", P(31945455), 3.0, .5, 'Le vrai vainqueur : voilier au coucher du soleil'),
 ('toi', CADRE, 108.9 - 95, .5, 'AUTHENTIQUE : Pete Goss en gros plan, « c’est lui »'),
 ('réponds', P(31945455), 6.0, .5, 'Voilier au coucher du soleil'),
 ('pas', P(4936486), 28.0, .5, 'Voilier seul en mer'),
 (None, P(31945455), 12.0, .5, 'Fin : voilier au coucher du soleil'),
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
    plan = dict(fin=end, source=S + s + ('.mkv' if s == INA else '.mp4'), entree=t, cadrage=c, note=n)
    if zone:
        plan['zone'] = zone[0]
    elif s == INA:
        # Archive en 16:9 avec bandes noires : zone utile, filigrane ina.fr hors du recadrage vertical.
        plan['zone'] = 'crop=1520:860:200:110'
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
