"""Plans du dossier 29, accrochés aux mots de timings-oraux.json (méthode du dossier 25).

Sources Pexels (licence Pexels), 4K ou vertical natif ; illustrations génériques.
"""
import json
import re
from pathlib import Path

m = Path('out/29-le-faux-ministre-au-masque/_montage')
S = '29-faux-le-drian/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower().replace('’', "'")) for w in words]

P = lambda i: f'pexels-{i}'
# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
rows = [
 ('avec', 'youtube-cc/P4bEWl0w-dw', 174.5, .3, 'Hook : gros plan d’un vrai masque en silicone hyperréaliste (Hyperflesh, LulzBot CC BY-SA, 1080p ; pas le masque de l’affaire ; tête de Walter White hors cadre)'),
 ('et', 'youtube-cc/P4bEWl0w-dw', 10.0, .5, 'Vrai masque en silicone retouché à la main : « masque en silicone » (visage de l’artisan hors cadre)'),
 ('deux', P(6266652), 0.5, .5, 'Mallette de billets : des millions'),
 ('jean-yves', P(19006219), 1.0, .5, 'Paris de nuit, drapeau français sur un toit : 2015'),
 ('et', 'photos/photo-ledrian-04.jpg', 0, .62, 'PHOTO : Jean-Yves Le Drian, ministre de la Défense, 11 novembre 2014 (Commons, CC BY-SA 3.0)'),
 ('il', P(12283288), 0.3, .5, 'Silhouette qui passe devant une fenêtre : un escroc'),
 ('drapeaux', P(36392511), 3.0, .5, 'Bureau sombre, écrans allumés : il reconstitue son bureau (32788087 écarté : calligraphie arabe ; 7448477 écarté : visage qui pouvait passer pour l’escroc)'),
 ('portrait', P(11329542), 1.0, .5, 'Drapeau français : drapeaux du faux bureau'),
 ('il', 'photos/photo-hollande-05.jpg', 0, .5, 'PHOTO : François Hollande, président, 30 novembre 2015 (Commons, CC0)'),
 ('baisse', 'youtube-cc/P4bEWl0w-dw', 11.8, .5, 'Vrai masque en silicone entre les mains de l’artisan : il enfile le masque'),
 ('appelle', P(36392511), 0.5, .5, 'Pièce sombre, écrans : il baisse la lumière'),
 ('son', P(6413828), 1.5, .5, 'Appel vidéo sur ordinateur portable : appelle sur Skype'),
 ('et', P(32829410), 12.0, .5, 'Silhouette encapuchonnée devant des écrans : le baratin (visage 5281602 écarté)'),
 ('plus', P(6266652), 5.0, .5, 'Mallette de billets : rançon'),
 ('le', P(8060394), 2.0, .5, 'Téléphone posé qui reçoit un appel : 150 cibles (SMS en vietnamien 10527947 écartés)'),
 ('le', 'photos/photo-maroc-01.jpg', 0, .5, 'PHOTO : le roi Mohammed VI, COP22, 15 novembre 2016 (Commons, CC BY 2.0)'),
 ("l'archevêque", 'photos/photo-gabon-01.jpg', 0, .5, 'PHOTO : Ali Bongo Ondimba, président du Gabon, 2012 (Commons, OGL v1.0)'),
 ('des', 'photos/photo-vingttrois-06.jpg', 0, .55, 'PHOTO : le cardinal André Vingt-Trois, archevêque de Paris de 2005 à 2017, en 2012 (Commons, CC BY 2.5)'),
 ('et', P(26083681), 0.2, .5, 'Homme en costume qui ajuste sa cravate : grands patrons'),
 ("l'aga", P(7534959), 2.0, .5, 'Homme inquiet devant son téléphone : tombent dans le panneau'),
 ('vingt', 'photos/photo-agakhan-08.jpg', 0, .8, 'PHOTO : l’Aga Khan IV, conférence de Londres, 4 février 2016 (Commons, CC BY 2.0), recadrée sur lui', 'crop=iw*0.30:ih*0.5:iw*0.63:ih*0.1'),
 ('un', P(32383883), 1.5, .5, 'Billets de 50 euros : 20 millions d’euros'),
 ('ce', P(6266289), 0.3, .5, 'Mallette de dollars : 47 millions de dollars'),
 ('un', P(5977258), 1.0, .5, 'Fun fact : mains sur un ordinateur portable (illustration)'),
 (('vouvoie', 'le'), 'photos/photo-sall-03.jpg', 0, .5, 'PHOTO : Macky Sall, président du Sénégal, 12 décembre 2022 (Commons, CC BY 2.0), recadrée pour garder le visage sous l’encart', 'crop=iw*0.26:ih*0.6:iw*0.54:0'),
 ('derrière', 'photos/photo-ledrian-02.jpg', 0, .5, 'PHOTO : Jean-Yves Le Drian, 2011 (Commons, CC BY 3.0) : le vrai Le Drian le tutoie'),
 ('gilbert', 'youtube-cc/P4bEWl0w-dw', 92.0, .17, 'Derrière le masque : têtes en silicone hyperréalistes dans l’atelier'),
 ('arrêté', P(32829410), 2.0, .5, 'Silhouette encapuchonnée devant des écrans (pas Chikli)'),
 ('il', P(14615718), 3.0, .5, 'Kiev, place de l’Indépendance vue du ciel : arrêté en Ukraine'),
 ('un', P(6266657), 0.5, .5, 'Menottes : il préparait la suite'),
 ('verdict', 'photos/photo-albert-01.jpg', 0, .5, 'PHOTO : le prince Albert II de Monaco, 15 novembre 2016 (Commons, CC BY 2.0)'),
 ('eux', '../28-om-va/pexels-10475256', 0.3, .5, 'Barreaux de cellule, détenu de dos (visage de face 10475372 écarté : pouvait passer pour Chikli)'),
 ('alors', P(4538212), 1.0, .5, 'Silhouette devant une ville de nuit : ils jurent que ce n’était pas eux'),
 ('réponds', 'youtube-cc/P4bEWl0w-dw', 94.5, .17, 'Masque en silicone hyperréaliste : génie ou voyou ?'),
 (None, P(20563164), 0.5, .5, 'Fin : silhouette devant un écran dans le noir'),
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
