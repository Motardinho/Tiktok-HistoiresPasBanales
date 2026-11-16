"""Plans du dossier 53, version au rythme du Short de Bolt « He Was Disqualified… » (environ 41 s).

Chaque plan : (début dans la sortie, source, début dans la source, style, noir et blanc, recadrage x y l h[, vitesse]).
Style « plein » = plein écran 9:16 ; « cadre » = fenêtre entre deux filets lumineux sur fond flou (code Bolt).
Vitesse inférieure à 1 = ralenti. Les débuts sont accrochés aux mots et aux vrais sons par calage.py.
"""
from calage import B, D, F, FIN, T, mot, reel

PLEIN, CADRE = 'plein', 'cadre'
ARCHIVE_BERLIN = 'berlin-francetv'
PLANS = [
    # France TV Sport : la réaction à chaud, caméra au niveau de Mayer.
    (0.0, ARCHIVE_BERLIN, 93.40, PLEIN, 0, (560, 90, 288, 512), 0.70),
    (reel('r0', 2.9), ARCHIVE_BERLIN, 95.43, CADRE, 0, (427, 80, 524, 520), 0.77),
    # Berlin : visage, élan, saut, puis preuve de la faute.
    (mot('À Berlin'), B, 15.0, PLEIN, 0, (850, 0, 607, 1080), 0.72),
    (mot('croit avoir'), B, 40.2, CADRE, 0, (450, 0, 825, 1080), 0.75),
    (mot('drapeau rouge', -0.14), B, 45.75, CADRE, 0, (320, 0, 1000, 1080)),
    (mot('saut annulé'), B, 46.5, PLEIN, 0, (680, 0, 607, 1080)),
    # vrai son : « je suis devenu rien du tout »
    (reel('r1'), B, 60.5, PLEIN, 0, (290, 0, 607, 1080), 0.6),              # il quitte le sautoir, seul
    (reel('r1', 2.0), ARCHIVE_BERLIN, 87.10, CADRE, 0, (440, 110, 510, 460), 0.72),
    # Le même geste réussit à Talence ; pause au vestiaire avant la course.
    (mot('Mais le mois'), F, 500.0, CADRE, 0, (510, 0, 897, 1080)),
    (mot('à Talence'), F, 322.7, CADRE, 0, (840, 165, 540, 650)),
    (mot('sept mètres'), F, 325.8, CADRE, 0, (750, 110, 706, 850)),
    (reel('r3'), F, 1714.0, CADRE, 0, (560, 0, 897, 1080)),
    (reel('r3', 2.4), F, 1717.6, PLEIN, 0, (700, 0, 607, 1080), 0.85),
    (mot('Pour le record'), F, 1831.5, CADRE, 0, (760, 110, 706, 850)),
    (mot('mille cinq cents'), T, 150.40, CADRE, 0, (500, 0, 897, 1080), 0.52),
    # vrai son final : l'arrivée et le record, commentaire original sur le vrai franchissement
    (reel('r2'), T, 153.75, CADRE, 0, (670, 0, 897, 1080)),                 # il franchit la ligne
    (reel('r2', 2.1), F, 1940.0, CADRE, 0, (420, 130, 950, 850)),           # il s'effondre, front sur la piste
    (reel('r2', 3.7), F, 1934.5, CADRE, 0, (600, 0, 897, 1080)),            # accolade des autres décathloniens
    (reel('r2', 5.0), F, 1981.5, CADRE, 0, (560, 0, 897, 1080)),            # dans les bras de sa compagne
    (reel('r2', 6.5), F, 1959.4, CADRE, 0, (600, 185, 1100, 760)),           # Mayer devant le panneau
    (reel('r2', 7.75), F, 2069.0, CADRE, 0, (624, 0, 1296, 1080), 0.6),     # WR 9126 en dernière image
]
# éclairs blancs : drapeau rouge, quarante jours plus tard, ligne d'arrivée
ECLAIRS = [mot('drapeau rouge', -0.14), mot('Mais le mois'), reel('r2')]
# musique : l'orchestre entre sur « Et quarante jours plus tard » et grandit jusqu'à l'arrivée
ENTREE = mot('Mais le mois')
FINAL = reel('r2')

if __name__ == '__main__':
    for i, p in enumerate(PLANS):
        suivant = PLANS[i + 1][0] if i + 1 < len(PLANS) else FIN
        print(f'{i:02d} {p[0]:7.3f} {suivant - p[0]:5.2f} s  {p[1][:4]} {p[2]}')
    print('FIN', round(FIN, 3))
