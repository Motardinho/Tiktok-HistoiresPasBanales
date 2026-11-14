"""Plans du dossier 42, accrochés aux mots de timings-oraux.json (méthode des dossiers 25 et 40).

Demande de Marc du 12 nov. 2026 : comme pour les maillots, photos des vrais ballons entrecoupées de séquences
vidéo. Photos des ballons et extraits officiels déjà en 1080x1920 (archives.py, image entière sur fond flou) :
`entree` y est compté depuis le début de l'extrait. Photos de personnes plein cadre au moment où le nom est dit.
Lancer depuis la racine du projet : python assets/42-beaux-ballons/montage.py
"""
import json
import re
from pathlib import Path

m = Path('out/42-top-10-plus-beaux-ballons-de-foot/_montage')
S = '42-beaux-ballons/'
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', w['w'].lower()) for w in words]


def a(key, t=0):
    return S + f'arch-{key}.mp4', t, .5


NASA = S + 'yt/84id2dzpwU0.mp4'
# (mot repère qui ouvre le plan suivant, (source, entrée, cadrage), note) ; None = dernier plan
rows = [
 ('le', (NASA, 42.0, .55), 'Accroche : ballons qui flottent dans la coupole de l’ISS devant la Terre (NASA, 4K), aucun rang'),
 ('zidane', (NASA, 17.4, .55), 'Accroche : autre vue de la coupole (NASA)'),
 ('deux', (S + 'photos/photo-zidane.jpg', 0, .5), 'Accroche : photo de Zinedine Zidane sur son nom'),
 ('numéro', a('fra26', 3.8), 'Accroche : gardien qui plonge, France - Sénégal 2026 (FIFA)'),
 ('coupe', a('p-trionda'), 'N°10 : photo du Trionda'),
 ('une', a('fra26', 0.8), 'N°10 : le Trionda en match, France - Sénégal 2026 (FIFA)'),
 ('et', (S + 'photos/photo-trionda-match.jpg', 0, .5), 'N°10 : le Trionda sur la pelouse de France - Sénégal (photo Commons)'),
 ('numéro', (NASA, 96.0, .47), 'Fun fact : le Trionda devant le hublot de la coupole (NASA)'),
 ('onze', a('p-jabulani'), 'N°9 : le Jabulani entier, ballon officiel des demi-finales 2010 (photo Agência Brasil)'),
 ('un', (S + 'photos/photo-jab-bra-chi.jpg', 0, .72), 'N°9 : Brésil - Chili 2010, Dani Alves frappe le Jabulani (photo Agência Brasil)'),
 ('numéro', (S + 'photos/photo-jab-bc1.jpg', 0, .3), 'N°9 : Brésil - Chili 2010, le gardien chilien et le Jabulani, sur « un gardien » (photo Agência Brasil)'),
 ('italie', a('p-etrusco-entier'), 'N°8 : l’Etrusco Unico entier (photo Commons)'),
 ('regarde', a('etr'), 'N°8 : Italie 1990, l’Etrusco en jeu (FIFA)'),
 ('numéro', a('p-etrusco'), 'N°8 : gros plan de l’Etrusco Unico, têtes de lion (photo Commons)'),
 ('euro', a('uefa', 0.2), 'N°7 : le Beau Jeu sur la pelouse (UEFA)'),
 ('bleu', a('uefa', 6.2), 'N°7 : « BEAU JEU », « EURO 2016 FRANCE » (UEFA)'),
 ('numéro', a('p-beaujeu'), 'N°7 : photo du Beau Jeu, bleu blanc rouge'),
 ('ronaldo', a('p-alrihla'), 'N°6 : photo de l’Al Rihla'),
 ('et', a('por-but', 0.9), 'N°6 : Ronaldo célèbre, Portugal - Uruguay 2022 (FIFA), sur son nom'),
 ('numéro', a('por-but', 3.6), 'N°6 : ralenti du centre de Bruno Fernandes, le ballon passe Ronaldo'),
 ('celui', a('p-azteca'), 'N°5 : photo de l’Azteca'),
 ('et', a('p-maradona'), 'N°5 : la main de Dieu, Maradona et le ballon (photo, domaine public), main et ballon dégagés du logo'),
 ('numéro', a('azt', 1.0), 'Relance : Maradona en 1986 (FIFA), sans révélation'),
 ('doré', a('tg-avant'), 'N°4 : finale 2006, Zidane et le ballon doré avant le match (FIFA)'),
 ('oui', a('p-teamgeist'), 'N°4 : photo du Teamgeist Berlin doré'),
 ('numéro', a('tg-coup', 1.4), 'N°4 : le coup de tête de Zidane (FIFA)'),
 ('son', a('p-tango'), 'N°3 : photo du Tango'),
 ('numéro', a('tango'), 'N°3 : finale 1978, Kempes et le Tango (FIFA)'),
 ('noir', a('p-telstar'), 'N°2 : photo du Telstar'),
 (('et', 'et'), a('telstar'), 'N°2 : finale 1970, Pelé et le Telstar (FIFA)'),
 (('numéro', 'numéro'), a('telstar2'), 'Relance : finale 1970, sans révélation du n°1'),
 (('le', 'le'), a('p-tricolore'), 'N°1 : photo du Tricolore'),
 ('zidane', a('z98-0', 0.25), 'N°1 : finale 1998, corner (FIFA)'),
 ('deux', a('z98-1', 0.3), 'N°1 : Zidane de près, sur son nom'),
 ("c'est", a('z98-2', 0.8), 'N°1 : la première tête de Zidane, ralenti'),
 ('abonne-toi', a('z98-3', 0.3), 'Fin : Zidane embrasse son maillot'),
 (None, a('z98-4', 3.0), 'Fin : les Bleus soulèvent la Coupe'),
]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], 0
for anchor, (src, t, c), note in rows:
    end = None
    if anchor:
        for w in (anchor if isinstance(anchor, tuple) else (anchor,)):
            cursor = find(w, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plans.append(dict(fin=end, source=src, entree=t, cadrage=c, note=note))
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
print(len(plans), 'plans :', [p['fin'] for p in plans])
