"""Plans du dossier 43, accrochés aux mots de timings-oraux.json (procédé du dossier 25).

Chaque fin de plan est le début d'un mot repère, cherché dans l'ordre à partir du repère
précédent : le découpage suit la voix même après une nouvelle synthèse.
Lancer depuis la racine du projet : python assets/43-motos-serie/montage.py
"""
import json
import re
from pathlib import Path

m = Path('out/43-top-3-motos-plus-rapides/_montage')
S = '43-motos-serie/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?]+$", '', w['w'].lower()) for w in words]

BMW = 'vVN9zcxxNhk'      # BMW Motorrad, « The new BMW M 1000 RR and BMW S 1000 RR » (4K, bandes noires jusqu'à 145 s)
BMW2 = '1p2Q2eJtIbQ'     # BMW Motorrad, « CLOSE LOOK - The new M 1000 RR » (4K)
DUC = 'w_1lcMyWqMU'      # Ducati, « New Panigale V4 R | Racing is just the beginning » (4K)
KAW = 'j8VJXb2LoMM'      # Kawasaki, « 2015 Ninja H2R Promotion Video » (1080p)
REC = '6_n7ru1e-rg'      # film du record du 30 juin 2016 (1080p)
FED = 'ALFEZNDyWZs'      # Fédération turque de motocyclisme, record du 30 juin 2016 (1080p)
BARRES = 'crop=3840:1550:0:304'  # retire les bandes noires du film BMW

# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, zone, note) ; None = dernier plan
rows = [
 ('la', BMW, 98.7, .26, BARRES, 'Accroche : M 1000 RR n°54 sur l’angle, vue de drone (aucun nom à l’écran)'),
 (('route', 'numéro'), BMW, 9.7, .5, BARRES, 'Accroche : ligne droite vue de drone'),
 (('erre', 'erre', 'trois'), BMW, 146.0, [[0, .42], [4.1, .6]], None, 'N°3 : la M 1000 RR entière, de profil'),
 ('trente-sept', BMW, 101.6, .26, BARRES, 'N°3 : M 1000 RR n°54 en courbe'),
 ('pourtant', BMW2, 22.2, .58, None, 'N°3 : face avant et ailerons'),
 ('à', BMW, 93.5, .5, BARRES, 'Fun fact : les deux M 1000 RR (n°60 et n°54) en piste'),
 ('bmw', BMW, 151.0, [[0, .6], [3.4, .45]], None, 'Fun fact : la M 1000 RR de profil'),
 ('numéro', BMW2, 14.3, .5, None, 'Fun fact : logo BMW et aileron en carbone'),
 ('trois', DUC, 17.6, .6, None, 'N°2 : la Panigale V4 R sort du stand'),
 ('c’est', DUC, 23.4, .47, None, 'N°2 : sur l’angle, de près'),
 ('près', DUC, 61.9, .46, None, 'N°2 : la Ducati officielle du championnat du monde Superbike'),
 ('mais', DUC, 96.2, .5, None, 'N°2 : la moto de série à l’arrêt'),
 (('plus', 'numéro'), DUC, 47.8, .47, None, 'Relance : roue avant levée en sortie de virage'),
 ('kilomètres-heure', KAW, 86.3, [[0, .45], [4.0, .6]], None, 'N°1 : la Ninja H2R devant le hangar'),
 ('trois', FED, 82.05, [[0, .49], [.95, .41], [1.45, .41]], None, 'N°1 : le compteur du record affiche 400 km/h'),
 ('en', KAW, 23.92, [[0, .25], [.68, .25], [.76, .55], [2.4, .55]], None, 'N°1 : carter « supercharged » puis roue du compresseur'),
 ('kénane', REC, 5.4, .5, None, 'N°1 : le pont Osman Gazi au lever du soleil'),
 ('atteint', FED, 130.0, .5, None, 'N°1 : Kenan Sofuoglu sur le pont, le jour du record'),
 ('sur', FED, 61.0, .5, None, 'N°1 : la H2R lancée sur le pont'),
 ('prix', FED, 39.2, .5, None, 'N°1 : le pont fermé, vide'),
 ('alors', REC, 47.8, .62, None, 'N°1 : Sofuoglu monte sur la H2R'),
 ('réponds', REC, 7.3, .6, None, 'Fin : caméra arrière embarquée sur le pont'),
 (None, REC, 17.5, .5, None, 'Fin : départ vu du dessus'),
]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], 0
for anchor, s, t, c, z, n in rows:
    end = None
    if anchor:
        for w in (anchor if isinstance(anchor, tuple) else (anchor,)):
            cursor = find(w, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plans.append(dict(fin=end, source=S + s + '.mp4', entree=t, cadrage=c, note=n, **({'zone': z} if z else {})))
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
