"""Plans du dossier 39, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Vraies séquences (FIFA, KBS WORLD, Arirang, Yonhap TV) découpées par archives.py ; Pexels seulement pour les commerces et le ministère, sans séquence réelle disponible.
Photos Wikimedia Commons pour les personnes citées et les lieux réels.
"""
import json
import re
from pathlib import Path

m = Path('out/39-l-entraineur-boycotte-dans-tout-le-pays/_montage')
S = '39-entraineur-banni/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…»«]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
O = lambda i: '../28-om-va/pexels-%d' % i
H = lambda i: '../37-main-henry/pexels-%d' % i
C = lambda i: '../30-calciopoli/pexels-%d' % i
A = lambda k: f'arch-{k}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('et', A('hong2026'), 0, .5, 'VRAIE SÉQUENCE : Hong Myung-bo à sa conférence de démission, 28 juin 2026 (KBS WORLD, image entière sur fond flou, sous-titres et logo exclus)'),
 ('mondial', A('hong2002'), 0, .5, 'VRAIE SÉQUENCE : Hong (n°20, brassard) célèbre le tir au but qualificatif, Corée-Espagne 2002 (FIFA) : héros national'),
 ('li', A('stade2026'), 0, .5, 'VRAIE SÉQUENCE : Corée du Sud-Tchéquie, Mondial 2026 (FIFA, score exclu)'),
 ('joue', 'photos/photo-lee-psg-large.jpg', 0, .64, 'PHOTO : Lee Kang-in sous le maillot du PSG, Salzbourg-PSG, 10 décembre 2024 (Commons, CC BY-SA 4.0) au moment où son nom est dit'),
 ('puis', A('victoire'), 0, .5, 'VRAIE SÉQUENCE : joie des Coréens contre la Tchéquie, victoire 2-1 (FIFA)'),
 ('contre', A('mexique'), 0, .5, 'VRAIE SÉQUENCE : le ballon au fond, Mexique 1-0 Corée du Sud (FIFA)'),
 ('éliminée', A('afsud'), 0, .5, 'VRAIE SÉQUENCE : but de l’Afrique du Sud, Afrique du Sud 1-0 Corée du Sud (FIFA)'),
 (('le', 'le'), A('elimines'), 0, .5, 'VRAIE SÉQUENCE : coup de sifflet final, les Sud-Africains fêtent, la Corée est éliminée (FIFA)'),
 ('déjà', A('profil'), 0, .5, 'VRAIE SÉQUENCE : Hong Myung-bo à la conférence de démission, 28 juin 2026 (KBS WORLD)'),
 ('cette', A('hong2014'), 0, .5, 'VRAIE SÉQUENCE : Hong Myung-bo démissionne après le Mondial 2014, 10 juillet 2014 (Arirang News, source 720p)'),
 ('caramels', 'photos/photo-incheon.jpg', 0, .5, 'PHOTO : hall des arrivées de l’aéroport d’Incheon (Commons) ; séquence MBC de 2014 non téléchargeable (YouTube bloque le téléchargement)'),
 ('en', 'photos/photo-yeot.jpg', 0, .5, 'PHOTO : yeot, caramel coréen (Commons, CC BY-SA 2.0 KR) - fun fact'),
 (('le',), 'photos/photo-yeot-vendeur.jpg', 0, .5, 'PHOTO : vendeur de yeot à Séoul (Commons, CC BY-SA 2.0) - fun fact'),
 ('trop', A('salut'), 0, .5, 'VRAIE SÉQUENCE : Hong s’incline devant la presse avant de démissionner, Korea House, 28 juin 2026 (KBS WORLD)'),
 ('le', A('hong2026b'), 0, .5, 'VRAIE SÉQUENCE : Hong lève les yeux, conférence de démission (KBS WORLD) : trop tard'),
 (('un', 'un'), P(40806778), 9.0, .5, 'Échoppe-bar de rue la nuit : un bar (illustration Pexels, pas le bar d’Anyang ; reportages KNN et YTN sur les panneaux non téléchargeables)'),
 ('une', P(39044463), 2.0, .5, 'Barbecue coréen : un resto (illustration Pexels, pas le restaurant de Gimje)'),
 ('ses', P(40101514), 0.0, .5, 'Supérette la nuit sous la pluie (illustration Pexels, pas la supérette de l’affaire)'),
 ('on', A('supporters'), 0, .5, 'VRAIE SÉQUENCE : supporters et policiers attendent la sélection à Incheon, 30 juin 2026 (Yonhap TV, incrustations exclues)'),
 ('retour', A('police'), 0, .5, 'VRAIE SÉQUENCE : policier en gilet « POLICE » autour de la sélection, Incheon, 30 juin 2026 (Yonhap TV)'),
 ('même', A('aeroport'), 0, .5, 'VRAIE SÉQUENCE : policiers déployés dans le hall des arrivées A d’Incheon vers 3 h 30, 30 juin 2026 (Yonhap TV)'),
 ('selon', 'photos/photo-president.jpg', 0, .5, 'PHOTO : le président Lee Jae-myung, investiture du 4 juin 2025 (Commons, CC BY-SA 2.0)'),
 (('le', 'le'), P(38734543), 1.0, .5, 'Séoul vu du ciel : ministère, fédération (illustration Pexels, aucune séquence de l’audit)'),
 ('sur', A('gwangju'), 0, .5, 'VRAIE SÉQUENCE : stade de Gwangju en rouge pendant la séance de tirs au but, 22 juin 2002 (FIFA)'),
 ('bouc', A('tir'), 0, .5, 'VRAIE SÉQUENCE : dernier tir au but de Hong Myung-bo, Corée-Espagne 2002 (FIFA)'),
 ('réponds', A('hong2026c'), 0, .5, 'VRAIE SÉQUENCE : Hong lit sa déclaration de démission, 28 juin 2026 (KBS WORLD) : bouc émissaire ou coupable ?'),
 (None, A('fin2002'), 0, .5, 'VRAIE SÉQUENCE : supporters et joueurs coréens fêtent la demi-finale, 2002 (FIFA)'),
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
