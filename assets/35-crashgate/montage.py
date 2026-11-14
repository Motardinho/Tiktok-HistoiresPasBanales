"""Plans des dossiers 35 et 36, accrochés aux mots de timings-oraux.json (méthode du dossier 25).
python montage.py 35 | 36"""
import json, re, sys
from pathlib import Path

n = int(sys.argv[1])
w = next(Path('out').glob(f'{n}-*')); m = w / '_montage'
S = {35: '35-crashgate/', 36: '36-spygate/'}[n]
words = json.loads((m / 'timings-oraux.json').read_text(encoding='utf8'))['words']
tokens = [re.sub(r"[.,:;!?…]+$", '', x['w'].lower().replace('’', "'")) for x in words]
P = lambda i: f'pexels-{i}.mp4'
F = lambda k: f'photos/photo-{k}.jpg'
X = lambda d, i: f'../{d}/pexels-{i}.mp4'
R = lambda k: f'arch-{k}.mp4'  # vraie séquence préparée par archives.py

# (mot repère qui ouvre le plan suivant, source, entrée, cadrage, note[, zone]) ; None = dernier plan
ROWS = {35: [
 ('exprès', R('crash-hook'), 0, .5, "ARCHIVE : l'accident de Piquet Jr au virage 17, diffusion d'origine du Grand Prix de Singapour 2008"),
 ('singapour', R('muret'), 0, .5, "ARCHIVE : le muret des stands Renault pendant la course, diffusion d'origine"),
 ('premier', P(33279610), 0.6, .5, "Singapour de nuit vu du ciel, grande roue voisine du circuit (prise récente, timelapse)"),
 ('fernando', R('piste'), 0, .5, "ARCHIVE : le circuit de Marina Bay de nuit, diffusion d'origine"),
 ('son', F('alonso-2008'), 0, .5, "PHOTO : Fernando Alonso, juin 2008, tenue Renault (Mark McArdle, CC BY-SA 2.0)"),
 ('bizarre', R('stand'), 0, .5, "ARCHIVE : arrêt au stand de la Renault d'Alonso à Singapour, ralenti, diffusion d'origine"),
 ('deux', F('alonso-stand'), 0, .45, "PHOTO : arrêt au stand d'Alonso, Renault, Grand Prix de Chine 2008 (Bert van Dijk, CC BY-SA 2.0)"),
 ('nelson', F('piquet-singapour'), 0, .3, "PHOTO : la Renault de Nelson Piquet Jr à Singapour, 27 septembre 2008, virage 10 (Erik Estrada, CC BY-SA 2.0)"),
 ("s'écrase", F('piquet-australie'), 0, .56, "PHOTO : Nelson Piquet Jr, mars 2009, tenue Renault (Ann64, CC BY-SA 2.0)"),
 ('voiture', R('ralenti'), 0, .5, "ARCHIVE : l'accident de Piquet Jr, ralenti, diffusion d'origine"),
 ('les', R('sc'), 0, .5, "ARCHIVE : panneau lumineux SC, voiture de sécurité, diffusion d'origine"),
 ('pas', R('ravitaillement'), 0, .5, "ARCHIVE : la voie des stands sous voiture de sécurité, diffusion d'origine"),
 ('et', F('alonso-victoire'), 0, .4, "PHOTO : Alonso en tête à Singapour, 28 septembre 2008 (chensiyuan, CC BY-SA 4.0)"),
 ('le', R('alonso-gagne'), 0, .5, "ARCHIVE : Alonso vainqueur dans sa Renault, écran de télévision filmé le soir de la course"),
 ('et', R('grue'), 0, .5, "ARCHIVE : la Renault accidentée de Piquet Jr soulevée par une grue, vidéo de spectateur, 28 septembre 2008"),
 ('radio', F('piquet-europe'), 0, .45, "PHOTO : Piquet Jr en piste sur sa Renault, Valence, août 2008 (Alan, CC BY 2.0)"),
 ('un', F('stand-renault'), 0, .45, "PHOTO : la Renault dans son stand, casques radio et écrans, Chine, octobre 2008 (Bert van Dijk, CC BY-SA 2.0)"),
 ('alors', F('piquet-2009'), 0, .35, "PHOTO : la Renault de Piquet Jr dans la voie des stands, Turquie, juin 2009 (Homonihilis, CC BY 3.0)"),
 ('on', F('fia'), 0, .5, "PHOTO : siège de la FIA, place de la Concorde, Paris, 2010 (Supermac1961, CC BY 2.0)"),
 ('selon', F('piquet-canada'), 0, .5, "PHOTO : Piquet Jr quitte les stands sur sa Renault, Canada, juin 2008 (Mark McArdle, CC BY-SA 2.0)"),
 ('flavio', F('garage-renault'), 0, .5, "PHOTO : garage Renault du circuit de Marina Bay, 28 septembre 2008 (Oahiyeel, domaine public)"),
 ('et', F('briatore-2008'), 0, .5, "PHOTO : Flavio Briatore, patron de Renault F1, Chine, octobre 2008 (Bert van Dijk, CC BY-SA 2.0) ; original 1115 px"),
 ('renault', P(6101348), 0.5, .5, "Marteau de juge (illustration : plainte)"),
 ('briatoré', F('renault-singapour'), 0, .5, "PHOTO : une Renault au Grand Prix de Singapour 2008 (Sabincp, domaine public)"),
 ('mais', F('briatore-2006'), 0, .65, "PHOTO : Flavio Briatore, mars 2006 (domaine public)"),
 ('en', F('palais'), 0, .5, "PHOTO : palais de justice de Paris, 2019 (Chabe01, CC BY-SA 4.0)"),
 ('alonso', F('alpine-2024'), 0, .5, "PHOTO : Alpine de Pierre Gasly, Autriche, juin 2024 (Lukas Raich, CC BY-SA 4.0) - écurie d'Enstone, ex-Renault"),
 ('piqué', F('trophee'), 0, .5, "PHOTO : trophée du vainqueur de Singapour 2008, musée Fernando Alonso (Morio, CC BY-SA 4.0)"),
 ('et', F('piquet-italie'), 0, .6, "PHOTO : la Renault de Piquet Jr, Italie, septembre 2008 (Jane Belinda Smith, CC BY 2.0)"),
 ('en', F('massa-2008'), 0, .55, "PHOTO : Felipe Massa, mai 2008 (joevanni_99, CC BY 2.0)"),
 ('perdra', F('massa-singapour'), 0, .45, "PHOTO : la Ferrari de Massa à Singapour, 27 septembre 2008 (Erik Estrada, CC BY-SA 2.0)"),
 ('piqué', R('massa-podium'), 0, .5, "ARCHIVE : Felipe Massa sur le podium du Brésil 2008, titre perdu d'un point (Formula 1, chaîne officielle)"),
 ('réponds', F('piquet-australie'), 1000, .33, "PHOTO : Nelson Piquet Jr, mars 2009, gros plan de la même photo (Ann64, CC BY-SA 2.0)", 'crop=iw*0.62:ih*0.8:iw*0.36:ih*0.02'),
 ('pas', R('grue2'), 0, .5, "ARCHIVE : la Renault de Piquet Jr évacuée, vidéo de spectateur"),
 (None, R('apres'), 0, .5, "ARCHIVE : la Renault de Piquet Jr contre le mur, diffusion d'origine"),
], 36: [
 ('et', P(19897022), 9.5, .5, "Hook : feuille qui sort d'un photocopieur (illustration)"),
 ('formule', P(5909916), 5.5, .5, "Compteuse de billets en dollars (illustration : l'addition)"),
 ('mac', R('depart1'), 0, .5, "ARCHIVE : départ du Grand Prix du Brésil 2007, Ferrari et McLaren (Formula 1, chaîne officielle)"),
 ('un', R('depart2'), 0, .5, "ARCHIVE : premiers virages du Grand Prix du Brésil 2007 (Formula 1, chaîne officielle)"),
 ('refile', F('f2007-stand'), 0, .35, "PHOTO : Ferrari F2007 et mécaniciens dans la voie des stands, démonstration de 2012 (emperornie, CC BY-SA 2.0) - pas le cadre en cause"),
 ('mac', P(8371852), 15.0, .5, "Mains dans une boîte de dossiers (illustration)"),
 ('sept', F('mtc'), 0, .5, "PHOTO : McLaren Technology Centre, Woking, 2008 (Alistair Rickman, CC BY 2.0)"),
 ('pour', P(7710495), 1.5, .5, "Pages feuilletées (illustration : 780 pages, pas le dossier réel)"),
 ('selon', P(5473792), 4.5, .5, "Disque posé dans un lecteur (illustration)"),
 ('la', F('f2007-musee'), 0, .45, "PHOTO : Ferrari F2007, 2022 (Calreyn88, CC BY-SA 4.0)"),
 ('dans', P(6100897), 8.0, .5, "Mains et pile de feuilles sur un bureau (illustration, pas l'épouse de l'ingénieur)"),
 ('mauvaise', P(3201876), 17.0, .5, "Homme devant un photocopieur de bureau (illustration, pas la boutique)"),
 ("l'employé", P(19897022), 1.5, .5, "Photocopieur en gros plan (illustration)"),
 ('et', P(3201876), 29.5, .5, "Homme pensif devant le photocopieur (illustration, pas l'employé réel)"),
 (('ferrari', 'ferrari'), R('kimi-cockpit'), 0, .5, "ARCHIVE : Räikkönen dans sa Ferrari, Brésil 2007 (Formula 1, chaîne officielle)"),
 ('et', F('kimi-spa'), 0, .5, "PHOTO : Räikkönen vainqueur à Spa, 16 septembre 2007, la victoire dédiée à l'employé (CC BY 2.0)"),
 ('perquisition', R('ferrari-fete'), 0, .5, "ARCHIVE : l'équipe Ferrari fête le titre 2007 (Formula 1, chaîne officielle) ; aucune image de la visite de l'usine"),
 ('et', R('cartons'), 0, .5, "ARCHIVE : cartons de documents apportés à l'audience de la FIA, Paris, 13 septembre 2007 (AP Archive) - pas la perquisition"),
 ('deux', R('fia-plaque'), 0, .5, "ARCHIVE : siège de la FIA le jour de l'audience, 13 septembre 2007 (AP Archive)"),
 ('le', X('34-echecs-sms', 39494839), 2.0, .5, "Téléphone et messages (illustration, pas les SMS réels)"),
 ('pilotes', X('34-echecs-sms', 5647324), 8.0, .5, "Clavier (illustration : e-mails)"),
 ('selon', R('hongrie-stand'), 0, .5, "ARCHIVE : voie des stands, qualifications du Grand Prix de Hongrie 2007, diffusion d'origine"),
 ('fernando', R('dennis-conf'), 0, .5, "ARCHIVE : Ron Dennis, patron de McLaren, en conférence de presse après le verdict (AP Archive)"),
 ('menace', F('alonso-2008'), 0, .5, "PHOTO : Fernando Alonso, juin 2008, tenue Renault de la saison suivante (Mark McArdle, CC BY-SA 2.0) ; aucun portrait libre net de 2007"),
 ('verdict', R('hongrie'), 0, .5, "ARCHIVE : la McLaren d'Alonso immobile dans son stand, qualifications de Hongrie 2007, diffusion d'origine"),
 ('et', R('dennis-foule'), 0, .5, "ARCHIVE : Ron Dennis assailli par la presse à l'audience de la FIA, 13 septembre 2007 (AP Archive)"),
 ('un', P(6266430), 0.3, .5, "Compteuse de billets (illustration : amende)"),
 ('et', P(5909916), 14.0, .5, "Compteuse de billets, autre angle (illustration : record)"),
 ('devant', R('kimi-damier'), 0, .5, "ARCHIVE : Räikkönen passe le drapeau à damier, Brésil 2007 (Formula 1, chaîne officielle)"),
 ('et', F('hamilton-2007'), 0, .3, "PHOTO : Lewis Hamilton, 8 juillet 2007 (CC BY-SA 3.0)"),
 ('cent', F('alonso-2007'), 0, .5, "PHOTO : Alonso sur sa McLaren, Canada, 10 juin 2007 (Mark McArdle, CC BY-SA 2.0)"),
 ('réponds', R('dennis-conf2'), 0, .5, "ARCHIVE : Ron Dennis lit sa déclaration après le verdict (AP Archive)"),
 ('pas', R('kimi-podium'), 0, .5, "ARCHIVE : Räikkönen champion du monde sur le podium, Brésil 2007 (Formula 1, chaîne officielle)"),
 (None, R('kimi-champagne'), 0, .5, "ARCHIVE : Räikkönen champion du monde, Brésil 2007 (Formula 1, chaîne officielle)"),
]}[n]


def find(word, start):
    return next(i for i in range(start, len(tokens)) if tokens[i] == word)


plans, cursor = [], -1
for anchor, s, t, c, note, *zone in ROWS:
    end = None
    if anchor:
        for a in (anchor if isinstance(anchor, tuple) else (anchor,)):
            cursor = find(a, cursor + 1)
        end = round(words[cursor]['start'], 3)
    plan = dict(fin=end, source=s[3:] if s.startswith('../') else S + s, entree=t, cadrage=c, note=note)
    if zone:
        plan['zone'] = zone[0]
    plans.append(plan)
(m / 'plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf8')
prev = 0
for p in plans:
    f = p['fin'] if p['fin'] is not None else words[-1]['end']
    print(f"{prev:6.2f}-{f:6.2f} {f - prev:5.2f}s {p['source'].split('/')[-1]:30} {p['note'][:60]}")
    prev = f
