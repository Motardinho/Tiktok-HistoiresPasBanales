"""Plans de l'essai « intense » du dossier 53 (environ 50 s) : la version de 35 s, plus les larmes du vestiaire,
l'enjeu des 4 minutes 49 et la dernière ligne droite entière.

Chaque plan : (début dans la sortie, source, début dans la source, style, noir et blanc, recadrage x y l h[, vitesse]).
"""
from calage import B, D, F, FIN, T, mot, reel

PLEIN, CADRE = 'plein', 'cadre'
ARCHIVE_BERLIN = 'berlin-francetv'
PLANS = [
    # France TV Sport : le visage de Mayer et la même réaction en plan plus large.
    (0.0, ARCHIVE_BERLIN, 93.40, PLEIN, 0, (560, 90, 288, 512), 0.70),
    (reel('r0', 2.9), ARCHIVE_BERLIN, 95.43, CADRE, 0, (427, 80, 524, 520), 0.77),
    # le narrateur relie : qui, la joie, le drapeau rouge
    (mot('Aux championnats'), B, 7.3, CADRE, 0, (510, 0, 897, 1080)),       # stade olympique de Berlin
    (mot('Kévin Maillère'), B, 15.0, PLEIN, 0, (850, 0, 607, 1080), 0.75),  # visage de Mayer, sur son nom
    (mot('hurle de joie', -0.35), B, 41.0, PLEIN, 0, (672, 50, 432, 768)),  # envol bras levés
    (mot('après son saut', 0.1), D, 18.60, CADRE, 0, (40, 215, 860, 725), 0.35),  # il se relève, bras ouverts (ralenti)
    (mot('mais le juge'), B, 45.75, CADRE, 0, (320, 0, 1000, 1080)),        # le juge lève le drapeau rouge
    (mot('saut annulé'), B, 46.5, PLEIN, 0, (680, 0, 607, 1080)),           # le drapeau rouge de près
    # vrai son : « je suis devenu rien du tout »
    (reel('r1'), B, 60.5, PLEIN, 0, (290, 0, 607, 1080), 0.6),              # il quitte le sautoir, seul
    (reel('r1', 2.0), ARCHIVE_BERLIN, 87.10, CADRE, 0, (440, 110, 510, 460), 0.72),
    # le revirement : quarante jours plus tard, tout près du record
    (mot('Mais quarante'), F, 500.0, CADRE, 0, (510, 0, 897, 1080)),        # stade de Talence plein
    (mot('à Talence'), F, 325.8, CADRE, 0, (750, 110, 706, 850)),           # bras écartés après son saut à 7,80 m
    (mot('il ne lui reste'), F, 1598.5, CADRE, 0, (780, 105, 706, 850)),    # cri après le javelot
    (mot('pour battre'), F, 1823.0, CADRE, 0, (400, 0, 897, 1080)),         # ligne de départ du 1 500 m
    # vrai son : les larmes du vestiaire, plans tenus plus longtemps
    (reel('r3'), F, 1714.0, CADRE, 0, (560, 0, 897, 1080)),                 # vestiaire, silence
    (reel('r3', 1.6), F, 1717.6, PLEIN, 0, (700, 0, 607, 1080), 0.7),       # tête basse, ralenti
    (reel('r3', 3.5), F, 1728.0, PLEIN, 0, (800, 0, 607, 1080), 0.8),       # avec son kiné
    # l'enjeu
    (mot('Il doit courir'), F, 1831.5, CADRE, 0, (760, 110, 706, 850)),     # regard avant le départ
    (mot('quatre minutes'), F, 1849.6, CADRE, 0, (400, 0, 897, 1080)),      # dans la course
    # Les images du reportage suivent ses propres commentaires jusqu'à l'arrivée.
    (reel('r2'), T, 149.90, CADRE, 0, (450, 0, 980, 1080)),
    (reel('r2', 2.65), T, 152.55, CADRE, 0, (605, 125, 955, 800)),
    (reel('r2', 6.0), T, 155.90, CADRE, 0, (520, 80, 820, 900)),
    (reel('r2', 7.8), F, 1940.0, CADRE, 0, (420, 130, 950, 850)),
    (reel('r2', 9.4), F, 1934.5, CADRE, 0, (600, 0, 897, 1080)),
    (reel('r2', 11.2), F, 2011.9, CADRE, 0, (330, 40, 1500, 1000)),
    (reel('r2', 13.1), F, 1981.5, CADRE, 0, (560, 0, 897, 1080)),
    (reel('r2', 15.2), F, 1959.4, CADRE, 0, (600, 185, 1100, 760)),
    (reel('r2', 16.55), F, 2069.0, CADRE, 0, (624, 0, 1296, 1080), 0.60),
]
ENTREE = mot('Mais quarante')
FINAL = reel('r2')
ECLAIRS = [mot('mais le juge'), reel('r2', 5.6)]

if __name__ == '__main__':
    for i, p in enumerate(PLANS):
        suivant = PLANS[i + 1][0] if i + 1 < len(PLANS) else FIN
        print(f'{i:02d} {p[0]:7.3f} {suivant - p[0]:5.2f} s  {p[1][:4]} {p[2]}')
    print('FIN', round(FIN, 3))
