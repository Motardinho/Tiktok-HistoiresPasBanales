"""Plans du dossier 38 (top 10 corruptions du foot), accrochés aux mots de timings-oraux.json.

Vidéos : Pexels (licence Pexels), certaines déjà téléchargées pour les dossiers 30, 35, 36 et 37.
Photos : Wikimedia Commons (personnes nommées : Tapie, Rossi, Havelange ; lieux réels : Costières,
Reyno de Navarra, Benito Villamarín, FIFA, Baur au Lac).
Toutes les vidéos sont des illustrations : aucune ne montre les faits racontés.
"""
import json
import re
from pathlib import Path

m = Path('out/38-top-10-corruptions-du-foot/_montage')
S = '38-top10-corruption/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}.mp4'
H = '../37-main-henry/'
C = '../30-calciopoli/'
F1 = '../35-crashgate/'
SP = '../36-spygate/'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note)
rows = [
 # Hook
 ('le', H + P(27561584), 2.0, .5, 'Hook : stade éclairé vu du ciel, de nuit (illustration)'),
 ('dans', H + P(29992746), 0.5, .5, 'Billets en euros qui volent (illustration)'),
 ('avec', P(33857285), 6.0, .5, 'Hôtel de luxe de nuit (illustration, pas le Baur au Lac)'),
 ('numéro', P(7714378), 3.0, .55, 'Gyrophare de police (illustration)'),
 # 10 - Hoyzer
 ('un', H + P(2249402), 2.0, .5, 'Stade vide éclairé de nuit, sans signe distinctif (illustration ; le stade plein du dossier 37 écarté : pays non identifiable)'),
 ('soixante-sept', H + P(3192198), 1.5, .5, 'Joueur qui frappe un ballon de nuit (illustration, pas un match truqué)'),
 ('et', H + P(855388), 2.0, .5, 'Billets en euros comptés (illustration)'),
 ('numéro', P(11999587), 6.5, .5, 'Vieille télé (illustration : la télé offerte à l’arbitre)'),
 # 9 - Nîmes
 ('le', 'yt/7GXJor7D2NM.mp4', 76.0, .5, 'VIDÉO RÉELLE : Stade des Costières plein, Nîmes - Ajaccio, mai 2018 (YouTube Oziak, CC BY ; passage filmé en tribune, sans logo ; source 1080p)'),
 ('dix-huit', P(11321634), 9.0, .5, 'Billets glissés dans une enveloppe (illustration)'),
 ('numéro', P(10472893), 2.0, .5, 'Cellule de prison (illustration)'),
 # 8 - Osasuna
 ('paie', 'photos/photo-sadar.jpg', 0, .5, 'PHOTO : stade Reyno de Navarra (El Sadar) d’Osasuna, 2008 (Commons, CC BY 3.0)'),
 ('deux', P(6700265), 1.0, .5, 'Billets comptés à la main (illustration)'),
 ('numéro', 'yt/wkMCHKErJyg.mp4', 18.5, .5, 'VIDÉO RÉELLE : Benito Villamarín de nuit depuis le Gol Sur, Betis - Valence, octobre 2017 (YouTube « En el Gol Sur del Villamarín », CC BY ; source 1080p)'),
 # 7 - Bundesliga 1971
 ('la', P(34459925), 1.0, .5, 'Berlin vu du ciel (illustration de l’Allemagne)'),
 ('à', C + P(8382685), 2.0, .5, 'Magnétophone à bandes (illustration de l’enregistrement)'),
 ('numéro', P(7826147), 0.5, .5, 'Gâteau « 50 » (Canellas fêtait ses 50 ans ; illustration)'),
 # 6 - OM-VA
 ('deux', P(35241817), 2.0, .55, 'Marseille, Vieux-Port et Notre-Dame-de-la-Garde'),
 ('tapie', P(36906606), 0.5, .5, 'On creuse dans un jardin (illustration)'),
 ('numéro', '../28-om-va/photos/photo-tapie-1994.jpg', 0, .5, 'PHOTO : Bernard Tapie, député européen, 1994 (Parlement européen, Commons)'),
 # 5 - Totonero
 ('paolo', P(12498404), 2.0, .5, 'Milan, le Duomo (illustration de l’Italie et du Milan)'),
 ('numéro', 'photos/photo-rossi.jpg', 0, .5, 'PHOTO : Paolo Rossi au Lanerossi Vicenza (Commons, domaine public) : suspendu puis champion du monde 1982'),
 # 4 - Calciopoli
 ('la', C + P(39349754), 1.0, .5, 'Turin vu du ciel au coucher du soleil'),
 ('numéro', C + P(29808342), 3.0, .5, 'Turin vu du ciel'),
 # 3 - Chine
 ("l'ex-patron", P(36926174), 3.0, .45, 'Drapeau chinois de nuit devant des tours'),
 ('des', P(6266659), 1.0, .5, 'Menottes sur des liasses de billets (illustration)'),
 ('la', P(6266920), 1.0, .4, 'Sac rempli de billets (illustration)'),
 ('accroche-toi', P(40144527), 4.0, .55, 'Place Tian’anmen et drapeau chinois, Pékin'),
 # 2 - ISL
 ('i', H + P(40867851), 1.0, .5, 'Stade éclairé vu du ciel (relance)'),
 ("jusqu'à", H + 'photos/photo-fifa10.jpg', 0, .5, 'PHOTO : siège de la FIFA à Zurich, 2011 (Commons, CC BY-SA 3.0)'),
 ('même', SP + P(5909916), 2.0, .5, 'Compteuse de billets (illustration)'),
 ('numéro', 'photos/photo-havelange.jpg', 0, .5, 'PHOTO : João Havelange, président de la FIFA, 1997 (Commons, CC BY-SA 4.0)'),
 # 1 - FIFAgate
 ('à', H + 'photos/photo-fifahall.jpg', 0, .5, 'PHOTO : hall du siège de la FIFA, 2014 (Commons, CC BY-SA 4.0)'),
 ('police', P(3717997), 5.0, .5, 'Zurich vu du ciel, lumière d’aube (illustration du raid)'),
 ('palace', P(7714378), 12.0, .55, 'Gyrophare de police (illustration, autre passage)'),
 ('plus', 'yt/QfWTXzqS4xM.mp4', 2.72, .27, 'VIDÉO RÉELLE : façade et enseigne du Baur au Lac de nuit, novembre 2017 (YouTube reisememo.ch, CC BY ; filigrane hors cadre ; source 1080p)'),
 ('selon', P(4275306), 8.0, .5, 'Billets de 100 dollars (illustration)'),
 ("l'om", F1 + P(6101348), 3.0, .5, 'Marteau de juge posé sur un bureau, sans personne (illustration)'),
 # Fin
 ('abonne-toi', P(38161894), 2.0, .5, 'Marseille, Vieux-Port vu d’en haut'),
 (None, '../39-entraineur-banni/' + P(37342408), 5.0, .5, 'Fin : stade éclairé de nuit, vue en hauteur (illustration)'),
]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], -1
for anchor, s, t, c, n in rows:
    end = None
    if anchor:
        cursor = find(anchor, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plans.append(dict(fin=end, source=S + s, entree=t, cadrage=c, note=n))
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
