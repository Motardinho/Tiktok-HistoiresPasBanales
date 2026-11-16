"""Plans de l'essai « intense » du dossier 53 (environ 50 s) : la version de 35 s, plus les larmes du vestiaire,
l'enjeu des 4 minutes 49 et la dernière ligne droite entière.

Chaque plan : (début dans la sortie, source, début dans la source, style, noir et blanc, recadrage x y l h[, vitesse]).
"""
from calage import B, D, F, FIN, T, mot, reel

PLEIN, CADRE = 'plein', 'cadre'
PLANS = [
    # vrai son d'ouverture : Mayer à Berlin après son zéro, au fond du trou
    (0.0, B, 53.1, PLEIN, 0, (480, 0, 607, 1080)),                          # accroupi, tête dans les mains
    (reel('r0', 2.14), B, 51.3, PLEIN, 0, (640, 120, 540, 960), 0.5),       # mains sur la tête, ralenti
    # le narrateur relie : qui, la joie, le drapeau rouge
    (mot('Aux championnats'), B, 7.3, CADRE, 0, (510, 0, 897, 1080)),       # stade olympique de Berlin
    (mot('Kévin Maillère'), B, 15.0, PLEIN, 0, (850, 0, 607, 1080), 0.75),  # visage de Mayer, sur son nom
    (mot('hurle de joie', -0.35), B, 41.0, PLEIN, 0, (672, 50, 432, 768)),  # envol bras levés
    (mot('après son saut', 0.1), D, 18.60, CADRE, 0, (40, 215, 860, 725), 0.35),  # il se relève, bras ouverts (ralenti)
    (mot('mais le juge'), B, 45.75, CADRE, 0, (320, 0, 1000, 1080)),        # le juge lève le drapeau rouge
    (mot('saut annulé'), B, 46.5, PLEIN, 0, (680, 0, 607, 1080)),           # le drapeau rouge de près
    # vrai son : « je suis devenu rien du tout »
    (reel('r1'), B, 60.5, PLEIN, 0, (290, 0, 607, 1080), 0.6),              # il quitte le sautoir, seul
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
    # vrai son final : toute la dernière ligne droite, image et commentaire synchrones, puis le record
    (reel('r2'), T, 149.96, CADRE, 0, (500, 0, 897, 1080)),                 # dernière ligne droite
    (reel('r2', 3.0), T, 152.96, CADRE, 0, (500, 0, 897, 1080)),            # il franchit la ligne
    (reel('r2', 6.1), F, 1940.0, CADRE, 0, (420, 130, 950, 850)),           # il s'effondre, front sur la piste
    (reel('r2', 8.0), F, 1934.5, CADRE, 0, (600, 0, 897, 1080)),            # accolade des autres décathloniens
    (reel('r2', 9.6), F, 1953.9, CADRE, 0, (510, 0, 897, 1080)),            # tribune debout
    (reel('r2', 11.1), F, 1981.5, CADRE, 0, (560, 0, 897, 1080), 0.8),      # dans les bras de sa compagne, léger ralenti
    (reel('r2', 13.0), F, 2011.9, CADRE, 0, (330, 40, 1500, 1000)),         # tribune, bras levés
    (reel('r2', 14.4), F, 2069.0, CADRE, 0, (624, 0, 1296, 1080)),          # panneau WR 9126 et décathloniens
    (reel('r2', 16.0), F, 1959.4, CADRE, 0, (600, 185, 1100, 760)),         # Mayer hurle à côté du panneau
]
# éclairs blancs : drapeau rouge, quarante jours plus tard, dernière ligne droite
ECLAIRS = [mot('mais le juge'), mot('Mais quarante'), reel('r2')]
# musique : l'orchestre entre sur « Mais quarante jours plus tard », s'efface un peu sous le vestiaire, puis grandit jusqu'à la fin
ENTREE = mot('Mais quarante')
FINAL = reel('r2')
DOUX = (reel('r3'), reel('r3', 4.9))

if __name__ == '__main__':
    for i, p in enumerate(PLANS):
        suivant = PLANS[i + 1][0] if i + 1 < len(PLANS) else FIN
        print(f'{i:02d} {p[0]:7.3f} {suivant - p[0]:5.2f} s  {p[1][:4]} {p[2]}')
    print('FIN', round(FIN, 3))
