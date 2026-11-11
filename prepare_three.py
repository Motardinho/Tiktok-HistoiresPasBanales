"""Prépare trois scripts originaux et leurs dossiers de production."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
NASA = 'https://www.nasa.gov/missions/station/iss-research/astronaut-exercise/'
CSA = 'https://www.asc-csa.gc.ca/eng/astronauts/living-in-space/physical-activity-in-space.asp'
TOM = 'https://media.tomtom.com/f/178460/x/1f90a06375/tomtom-unveils-data-driven-insights-from-over-700-billion-kilometers-driven-in-2024-eu.pdf'

VIDEOS = [
 dict(slug='astronautes-sport-en-orbite', titre='Pourquoi courir dans l’espace ?', format='histoire',
      reference='https://www.tiktok.com/@faiseemoc84/video/7697972924183121184',
      titre_fixe='COURIR DANS L’ESPACE ?',
      hooks=['Dans l’espace, même courir demande de s’attacher.', 'En orbite, le sport fait partie de la mission.', 'Le piège de l’espace, c’est de ne plus porter son poids.', 'Pourquoi courir quand on peut flotter ?', 'Ce tapis roulant protège bien plus que leur endurance.'],
      textes=[
       'Dans l’espace, même courir demande de s’attacher. Sans un harnais pour te maintenir contre le tapis, tes pieds ne resteraient pas dessus.',
       'À bord de la Station spatiale internationale, flotter semble facile. Mais cette liberté a un prix : les muscles et les os travaillent moins.',
       'Sur Terre, porter ton propre poids les sollicite déjà. En microgravité, cette charge disparaît presque. Sans entraînement, le corps perd de sa force.',
       'La réponse, c’est une véritable salle de sport en orbite. Les astronautes utilisent notamment un tapis roulant, un vélo et une machine de résistance.',
       'Cette dernière permet de reproduire des efforts de musculation. Des pistons et un volant d’inertie créent une charge, même quand les haltères ne pèsent presque plus.',
       'Selon la NASA, les équipages consacrent en moyenne deux heures par jour à l’exercice. Les programmes évoluent pour mieux protéger leurs capacités physiques.',
       'L’objectif dépasse la performance sportive. Il faut aussi pouvoir sortir dans l’espace, réagir en situation d’urgence et retrouver la pesanteur au retour.',
       'Le plus étonnant ? Là-haut, se laisser porter est facile. Rester capable de marcher ici demande du travail. Tu tiendrais ce rythme ? Dossier clos. Mais l’histoire, elle, reste hors normes.'
      ],
      sources=[f'NASA, 20 mai 2024 : microgravité, ARED, T2, CEVIS, moyenne de deux heures quotidiennes, pistons et volant d’inertie. {NASA}', f'Agence spatiale canadienne : rôle de la gravité, harnais du tapis, sorties et procédures au retour. {CSA}'],
      legende='Flotter, oui. Renoncer au sport, impossible. Tu tiendrais ce rythme en orbite ?', hashtags=['#histoirevraie','#espace','#astronautes','#science','#DossiersHorsNormes']),
 dict(slug='trois-records-voitures-vitesse', titre='Trois voitures, trois records de vitesse', format='top',
      reference='https://www.tiktok.com/@faiseemoc84/video/7488419683847179542',
      titre_fixe='3 RECORDS DE VITESSE',
      hooks=['Ces trois voitures ont dépassé les quatre cents kilomètres heure.', 'À cette vitesse, les conditions du record changent tout.', 'Trois machines, trois chiffres presque irréels.', 'Quelle différence entre une pointe et une moyenne ?', 'Le chiffre le plus élevé ne raconte pas toute l’histoire.'],
      textes=[
       'Ces trois voitures ont dépassé les quatre cents kilomètres heure. Mais attention : leurs records ne se comparent pas tous de la même manière.',
       'Voici trois performances historiques, classées par vitesse annoncée. Ce classement concerne uniquement cette sélection, pas un podium mondial actuel de toutes les voitures.',
       'Numéro trois : la Koenigsegg Agera RS. En deux mille dix-sept, elle atteint une moyenne de quatre cent quarante-sept virgule dix-neuf kilomètres heure au Nevada.',
       'Pourquoi une moyenne ? Pour ce type de record, parcourir la route dans les deux sens aide à limiter l’influence du vent et de la pente.',
       'Numéro deux : la SSC Tuatara. En janvier deux mille vingt et un, sa moyenne sur deux passages atteint quatre cent cinquante-cinq virgule trois kilomètres heure.',
       'Numéro un de cette sélection : le prototype de la Bugatti Chiron Super Sport trois cents plus. En deux mille dix-neuf : quatre cent quatre-vingt-dix virgule quatre cent quatre-vingt-quatre kilomètres heure.',
       'La nuance est essentielle : Bugatti réalise cette pointe dans un seul sens. Ce chiffre ne représente donc pas la même mesure que les deux moyennes précédentes.',
       'Derrière un record, regarde toujours la date, la voiture exacte et le protocole. Laquelle te fascine le plus ? Dossier clos. Dis-moi ton numéro un en commentaire.'
      ],
      sources=[
       'Koenigsegg : Agera RS, 4 novembre 2017, Nevada, 447,19 km/h, moyenne des passages opposés. https://www.koenigsegg.com/history',
       'SSC : Tuatara, 17 janvier 2021, 455,3 km/h, moyenne de deux passages, mesures Racelogic. https://www.sscnorthamerica.com/model/records',
       'Bugatti : prototype dérivé de Chiron, 2019, 490,484 km/h en un sens ; pas un record bidirectionnel. https://newsroom.bugatti.com/press-releases/bugatti-chiron-super-sport-300-plus'],
      legende='Trois records historiques, trois machines extrêmes. Tu choisis laquelle ? Vitesses et protocoles précisés dans la vidéo.', hashtags=['#histoirevraie','#automobile','#vitesse','#records','#DossiersHorsNormes']),
 dict(slug='villes-plus-lentes-tomtom-2024', titre='Les trois villes les plus lentes en 2024', format='top',
      reference='https://www.tiktok.com/@faiseemoc84/video/7487657087770692886',
      titre_fixe='10 KM EN VILLE • 2024',
      hooks=['Dix kilomètres peuvent prendre plus d’une demi-heure.', 'Dans ces villes, dix kilomètres deviennent une épreuve de patience.', 'Tu trouves ton trajet lent ? Regarde ces chiffres.', 'La ville la plus lente n’est pas forcément la plus embouteillée.', 'Le compteur avance moins vite que l’horloge.'],
      textes=[
       'Dix kilomètres peuvent prendre plus d’une demi-heure. Voici les trois villes les plus lentes du classement TomTom pour l’année deux mille vingt-quatre.',
       'Le critère est précis : le temps moyen pour parcourir dix kilomètres en ville. On compare les déplacements mesurés, pas uniquement les bouchons du matin.',
       'Numéro trois : Bengaluru, en Inde. Pour ces dix kilomètres, le temps moyen atteint trente-quatre minutes et dix secondes. Il faut donc prévoir une vraie marge.',
       'Numéro deux : Kolkata, également en Inde. La même distance demande trente-quatre minutes et trente-trois secondes. Quelques secondes suffisent ici à changer le classement.',
       'Numéro un : Barranquilla, en Colombie. Dix kilomètres y prennent trente-six minutes et six secondes en moyenne. Tu comprends pourquoi la distance ne suffit pas.',
       'Mais voici le détail qui change tout : une ville lente n’est pas automatiquement celle où la congestion est la plus forte. Les deux classements mesurent des choses différentes.',
       'La vitesse dépend aussi du réseau routier, des limitations et des intersections. La congestion mesure le ralentissement par rapport à une circulation fluide.',
       'Ces résultats décrivent deux mille vingt-quatre. Ton trajet actuel peut être très différent. Quelle ville te fait perdre patience ? Dossier clos. Dis-moi ton numéro un en commentaire.'
      ],
      sources=[f'TomTom, rapport publié le 8 janvier 2025, données 2024 : classement du temps moyen par 10 km, Bengaluru 34:10, Kolkata 34:33, Barranquilla 36:06. Infographie page 2. {TOM}', f'TomTom : distinguer lenteur et taux de congestion, facteurs statiques et dynamiques. {TOM}'],
      legende='Les villes les plus lentes selon TomTom, données 2024. Où as-tu vécu ton pire trajet ?', hashtags=['#histoirevraie','#villes','#trafic','#culturegenerale','#DossiersHorsNormes'])
]

if __name__ == '__main__':
    next_number = len([p for p in OUT.iterdir() if p.is_dir()]) + 1
    for i, v in enumerate(VIDEOS):
        folder = OUT / v['slug']
        folder.mkdir(exist_ok=True)
        data = {k: val for k, val in v.items() if k not in ('slug','textes','sources','hooks')}
        data['numero'] = next_number + i
        data['hook'] = v['textes'][0]
        data['sources_a_verifier'] = v['sources']
        data['scenes'] = [dict(narration=t, image_prompt='Original cinematic illustrative scene; see visuels-prompts.txt', animate=j in (0,4), motion_prompt='Slow cinematic push in', **({'rang': {2:3,4:2,5:1}.get(j)} if i==1 else {'rang': {2:3,3:2,4:1}.get(j)} if i==2 else {})) for j,t in enumerate(v['textes'])]
        if i==1:
            data['scenes'][1]['bandeau']='SÉLECTION HISTORIQUE'
            data['scenes'][6]['bandeau']='BUGATTI : UN SEUL SENS'
        if i==2:
            data['scenes'][1]['bandeau']='TOMTOM • DONNÉES 2024'
        (folder/'histoire.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        (folder/'verification.md').write_text('# Vérification éditoriale\n\nTexte original. Sujet repéré sur : '+v['reference']+'\n\nSources consultées le 7 novembre 2026 :\n\n'+'\n\n'.join(v['sources'])+'\n\nIllustrations synthétiques : ne pas présenter comme des images d’archives. Activer le label IA lors de la publication.\n\nHooks envisagés :\n'+'\n'.join('- '+h for h in v['hooks']),encoding='utf-8')
        count = len(' '.join(v['textes']).split())
        print(v['slug'],count,'mots,',len(data['scenes']),'scènes')
