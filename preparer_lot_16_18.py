"""Préparation éditoriale du lot du 8 novembre 2026, sans appel payant."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
DATE = '2026-11-08'

VIDEOS = [
    dict(numero=16, slug='armees-puissantes-gfp-2026', titre='Les 3 armées en tête de Global Firepower 2026',
         titre_fixe='TOP 3 DES ARMÉES - GFP 2026', serie='LE CLASSEMENT QUI FAIT PARLER',
         critere='Classement Global Firepower 2026 des capacités conventionnelles estimées. Ce classement ne prédit pas le résultat d’une guerre.',
         reference='https://www.tiktok.com/@faiseemoc84/video/7244969332604767514',
         hooks=['Numéro 3 des armées selon Global Firepower : la Chine. Plus de 2 millions de militaires actifs.', 'La Chine possède la plus grande armée active, mais reste troisième de ce classement.', 'Numéro 3 en 2026 : la Chine et ses effectifs gigantesques.', 'Pourquoi la plus grande armée active n’est-elle que troisième ?', 'La Chine ouvre ce top 3. Et le nombre de soldats ne suffit pas.'],
         scenes=[
             (3, 'Numéro 3 des armées selon Global Firepower en 2026 : la Chine. Plus de 2 millions de militaires actifs, selon les estimations du site.', '3 - CHINE - 2 MILLIONS', 'Défilé chinois en mouvement, puis panorama de formation ; aucune image américaine.', 'Chinese military parade with anonymous adult soldiers, authentic Chinese equipment, documentary composition, no identifiable faces.'),
             (3, 'C’est le plus gros effectif actif de sa base. Pourtant, la quantité de soldats ne suffit pas pour prendre la première place du classement.', 'LE PLUS GROS EFFECTIF ACTIF', 'Formation au sol, puis bâtiment naval chinois identifié.', 'Wide view of anonymous adult Chinese soldiers in formation, documentary illustration.'),
             (3, 'Global Firepower croise plus de 60 facteurs : équipements, finances, logistique et géographie. Il compare les capacités conventionnelles de 145 pays.', '145 PAYS COMPARÉS', 'Carte explicative sobre et pictogrammes originaux ; rester sur la Chine.', 'Original conceptual military logistics illustration with ships, supply trucks and aircraft, no flags.'),
             (2, 'Numéro 2 : la Russie. Le site lui attribue le deuxième parc aérien militaire de son classement, en comptant les avions et les hélicoptères.', '2 - RUSSIE', 'Plans russes identifiés : avion puis hélicoptère ; aucun plan de combat.', 'Russian military aircraft parked on a runway, no combat, documentary illustration.'),
             (2, 'Mais un inventaire reste un inventaire. Il ne dit pas que tous les appareils peuvent décoller ensemble, ni comment une opération se déroulerait réellement.', 'PARC AÉRIEN - ESTIMATIONS GFP', 'Maintenance et hangars russes ; pas de destruction ni de victoire suggérée.', 'Anonymous adult mechanics inspecting an aircraft in a Russian airbase hangar, no readable text.'),
             (1, 'Numéro 1 : les États-Unis. Global Firepower leur attribue plus de 13 000 appareils militaires, avions et hélicoptères réunis. Un parc aérien immense.', '1 - ÉTATS-UNIS - 13 000+', 'Avion américain en mouvement, puis plan large du parc aérien.', 'US military aircraft and helicopters on a large airbase, documentary illustration, no combat.'),
             (1, 'Ce top mesure donc bien plus que les effectifs. La Chine mène sur les militaires actifs ; les États-Unis arrivent premiers au classement général.', 'EFFECTIFS ET CLASSEMENT GLOBAL', 'Plans américains, rappel graphique textuel des trois entrées après leur révélation.', 'Wide cinematic view of a US military transport aircraft on a runway.'),
             (None, 'Et toi, quel pays attendais-tu dans ce podium ? Donne ton choix et ton critère en commentaire. Pas banal, hein ?', 'QUEL PAYS ATTENDAIS-TU ?', 'Récapitulatif original 3 - 2 - 1 ; aucun drapeau d’un pays absent.', 'Abstract documentary background for a military ranking recap, no symbols or text.'),
         ],
         sources=[
             ('Classement 2026 : Chine 3, Russie 2, États-Unis 1 ; 145 pays, plus de 60 facteurs, capacités conventionnelles.', 'https://www.globalfirepower.com/countries-listing.php'),
             ('Chine : 2 035 000 militaires actifs estimés, premier effectif actif dans GFP.', 'https://www.globalfirepower.com/country-military-strength-detail.php?country_id=china'),
             ('Russie : deuxième rang du parc aérien GFP, avions et hélicoptères.', 'https://www.globalfirepower.com/country-military-strength-detail.php?country_id=russia'),
             ('États-Unis : Aircraft Total Stock 13 032 ; distinction entre stock et readiness.', 'https://www.globalfirepower.com/country-military-strength-detail.php?country_id=united-states-of-america'),
         ],
         precision='GFP est un indice privé fondé sur des estimations, pas un classement officiel ni une prédiction de victoire. Mention GFP 2026 visible. Ne pas illustrer le score conventionnel par des explosions nucléaires.',
         legende='Chine, Russie, États-Unis : le podium Global Firepower 2026. Quel pays attendais-tu, et selon quel critère ?',
         hashtags=['#top3', '#armees', '#culturegenerale', '#HistoiresPasBanales'], musique='Tension documentaire légère, pulsation sourde ; voix prioritaire.'),
    dict(numero=17, slug='animaux-trois-records-vitesse', titre='3 animaux aux vitesses folles',
         titre_fixe='3 ANIMAUX AUX VITESSES FOLLES', serie='LE CHIFFRE QUI SURPREND',
         critere='Trois performances sélectionnées, par vitesse croissante. Course, vol mesuré par rapport au sol et piqué sont des catégories différentes ; ce n’est pas le podium absolu de tous les animaux.',
         reference='https://www.tiktok.com/@faiseemoc84/video/7234159601367764250',
         hooks=['Numéro 3 de ces records de vitesse : le guépard, autour de 100 kilomètres heure en pointe.', 'Le guépard ouvre cette sélection. Mais la suite se passe dans les airs.', 'Ce sprinteur atteint autour de 100 kilomètres heure.', 'Trois performances animales, avec un guépard pour commencer.', 'Numéro 3 : courir à la vitesse d’une voiture.'],
         scenes=[
             (3, 'Numéro 3 de ces records de vitesse : le guépard. Autour de 100 kilomètres heure en pointe, selon Guinness. Et tout ça, sur ses propres pattes.', '3 - GUÉPARD - ENVIRON 100 KM/H', 'Guépard en course plein cadre dès la première image, vitesse de lecture réelle.', 'A cheetah sprinting across flat savanna, full body visible, wildlife documentary composition.'),
             (3, 'Mais cette vitesse ne dure pas pendant des kilomètres. C’est une performance sur courte distance. Le guépard est un sprinteur, pas un marathonien.', 'SPRINT SUR COURTE DISTANCE', 'Deux prises distinctes de course puis ralentissement naturel.', 'A cheetah slowing down after a sprint in natural savanna, wildlife documentary illustration.'),
             (2, 'Numéro 2 de notre sélection : une chauve-souris. Le molosse du Brésil. Une étude a enregistré des pointes autour de 160 kilomètres heure par rapport au sol.', '2 - MOLOSSE DU BRÉSIL - ENVIRON 160 KM/H', 'Espèce Tadarida brasiliensis correctement identifiée, sortie en vol ; aucune roussette.', 'Brazilian free-tailed bat Tadarida brasiliensis flying, species-accurate long free tail, wildlife documentary illustration.'),
             (2, 'Les chercheurs suivaient les animaux grâce à de petits émetteurs. Une chauve-souris minuscule pouvait donc parcourir le ciel à une vitesse franchement surprenante.', 'SUIVIE PAR ÉMETTEUR', 'Schéma original du suivi aérien, clairement présenté comme schéma.', 'Scientific conceptual illustration of a small radio-tagged Brazilian free-tailed bat in flight, no text.'),
             (2, 'Attention au détail : une vitesse mesurée par rapport au sol peut être influencée par le vent. Ce chiffre n’est pas sa vitesse de croisière habituelle.', 'VITESSE AU SOL - MESURE PONCTUELLE', 'Flèche explicative du vent ajoutée au montage ; pas d’accélération du film.', 'Brazilian free-tailed bat flying above open landscape, realistic wildlife illustration.'),
             (1, 'Numéro 1 de cette sélection : le faucon pèlerin. En piqué, il peut atteindre environ 320 kilomètres heure. Là, il ne vole plus simplement à l’horizontale.', '1 - FAUCON PÈLERIN - ENVIRON 320 KM/H', 'Vrai piqué identifiable, ailes repliées ; pas de vol plané présenté comme record.', 'Peregrine falcon in a steep hunting stoop with folded wings, no visible prey injury, wildlife documentary illustration.'),
             (1, 'Il plonge vers sa proie. La course du guépard, le vol de la chauve-souris et ce plongeon sont trois façons très différentes d’aller vite.', 'EN PIQUÉ', 'Poursuivre le piqué puis déploiement des ailes ; pas de capture sanglante.', 'Peregrine falcon opening its wings after a dive, wildlife documentary illustration.'),
             (None, 'Lequel t’a le plus surpris ? Le sprinteur, la chauve-souris ou le faucon ? Donne ton choix en commentaire. Pas banal, hein ?', 'LEQUEL T’A SURPRIS ?', 'Récapitulatif des trois performances avec catégorie sous chaque vitesse.', 'Three distinct wildlife habitats, savanna and open sky, conceptual illustration with no text.'),
         ],
         sources=[
             ('Guépard : environ 100 km/h, courte distance ; ne pas annoncer 120 km/h comme valeur vérifiée ici.', 'https://www.guinnessworldrecords.com/world-records/70463-fastest-mammal-on-land-over-short-distances'),
             ('Tadarida brasiliensis : pointes à 160,2 km/h au sol, émetteurs, précautions vent/plongée.', 'https://www.guinnessworldrecords.com/world-records/549644-fastest-bat'),
             ('Équipe de recherche, novembre 2016 : suivi et pointes au-delà de 160 km/h.', 'https://www.mpg.de/10820289/freischwanz-fledermaus-ist-der-schnellste-flieger-im-tierreich?c=987944'),
             ('Faucon pèlerin : environ 320 km/h en piqué, catégorie explicite.', 'https://www.guinnessworldrecords.com/world-records/70929-fastest-bird-diving'),
         ],
         precision='Sélection de trois performances, jamais « les 3 animaux les plus rapides du monde ». Ne pas recycler le podium terre-mer-air de la référence, dont certaines vitesses marines sont fragiles. Titres et unités doivent toujours conserver environ et les conditions.',
         legende='Un guépard, une chauve-souris et un faucon : 3 performances de vitesse impressionnantes. Lequel t’a surpris ?',
         hashtags=['#animaux', '#vitesse', '#records', '#HistoiresPasBanales'], musique='Percussions organiques discrètes, progression vive, différente du top armées.'),
    dict(numero=18, slug='pays-plus-grands-superficie', titre='Les 3 plus grands pays par superficie totale',
         titre_fixe='TOP 3 DES PLUS GRANDS PAYS', serie='LE CLASSEMENT QUI SURPREND',
         critere='Pays souverains, superficie totale selon les valeurs de référence ONU et Statistique Canada, eaux incluses. Pas la seule superficie terrestre. Valeurs arrondies dans la narration.',
         reference='https://www.tiktok.com/@faiseemoc84/video/7243108338471341339',
         hooks=['Numéro 3 des plus grands pays par superficie totale : les États-Unis, avec environ 9,8 millions de kilomètres carrés.', 'Les États-Unis sont immenses. Pourtant, ils n’ouvrent ce top qu’à la troisième place.', 'Numéro 3 : les États-Unis, Alaska compris.', 'Ce pays approche les 10 millions de kilomètres carrés. Il n’est que troisième.', 'Voici le top 3 par superficie totale, avec les États-Unis pour commencer.'],
         scenes=[
             (3, 'Numéro 3 des plus grands pays par superficie totale : les États-Unis. Environ 9,8 millions de kilomètres carrés, en comptant les terres et les eaux.', '3 - ÉTATS-UNIS - 9,8 MILLIONS KM²', 'Globe original vers États-Unis, Alaska et Hawaï inclus ; ne pas montrer le numéro 1.', 'Satellite-style original globe centered on North America with Alaska and Hawaii visible, no borders or labels.'),
             (3, 'Et il faut bien inclure l’Alaska. Si tu regardes seulement le grand bloc situé entre le Canada et le Mexique, tu oublies une partie du pays.', 'ALASKA COMPRIS', 'Carte géographique exacte ; déplacement vers Alaska, sans déplacer l’archipel artificiellement.', 'Aerial view of Alaskan mountain landscape, realistic documentary illustration.'),
             (2, 'Numéro 2 : le Canada. Presque 10 millions de kilomètres carrés. Il dépasse les États-Unis avec ce critère, même si l’écart paraît petit à cette échelle.', '2 - CANADA - PRESQUE 10 MILLIONS KM²', 'Zoom vers Canada, puis paysages canadiens réellement identifiés.', 'Canadian boreal forest and freshwater lakes seen from above, documentary illustration.'),
             (2, 'Le détail important, c’est l’eau. Les lacs et les autres eaux intérieures font partie de cette superficie totale. On ne mesure pas seulement la terre ferme.', 'TERRES ET EAUX', 'Lacs canadiens puis schéma de la superficie ; pas de chiffre non sourcé.', 'Aerial view of Canadian freshwater lakes and forest, realistic documentary illustration.'),
             (1, 'Numéro 1 : la Russie. Environ 17,1 millions de kilomètres carrés. Cette fois, le changement d’échelle est énorme. Elle dépasse très largement les deux précédents.', '1 - RUSSIE - 17,1 MILLIONS KM²', 'Révélation du contour russe sur globe à aire fidèle ; frontières internationalement reconnues.', 'Original globe centered on northern Eurasia, realistic earth curvature, no political borders or labels.'),
             (1, 'Pour comparer, son territoire est environ 1,7 fois aussi grand que celui du Canada. Ce rapport vient des superficies, pas de la taille apparente sur une carte.', 'ENVIRON 1,7 FOIS LE CANADA', 'Comparaison de surfaces à échelle identique calculée ; pas de projection Mercator.', 'Neutral dark background for an original equal-area geography comparison, no text or symbols.'),
             (1, 'Voilà pourquoi le critère compte : on vient de comparer la superficie totale. Un classement des terres seules peut placer les pays dans un autre ordre.', 'CRITÈRE - SUPERFICIE TOTALE', 'Récapitulatif des trois cartes ; mention source discrète.', 'Satellite-style original globe with natural colors, no borders or labels.'),
             (None, 'Tu avais trouvé ce podium avant la fin ? Écris ton score sur 3 en commentaire et envoie la vidéo à quelqu’un qui aime la géographie. Pas banal, hein ?', 'TON SCORE SUR 3 ?', 'Récapitulatif lisible 3 - États-Unis, 2 - Canada, 1 - Russie.', 'Nighttime earth from space, realistic documentary illustration, no text.'),
         ],
         sources=[
             ('États-Unis : superficie totale 9 833 517 km², arrondie à 9,8 millions.', 'https://data.un.org/en/iso/US.html'),
             ('Canada : 9 984 670 km² au total, 9 093 507 de terres et 891 163 d’eau douce. Tableau historique de référence, pas une mesure de 2026.', 'https://www150.statcan.gc.ca/n1/pub/11-402-x/2010000/chap/geo/tbl/tbl06-fra.htm'),
             ('Russie : annuaire statistique ONU 2024, superficie 17 098 milliers de km², arrondie à 17,1 millions.', 'https://desapublications.un.org/file/20893/download'),
             ('Chine : superficie ONU 9 600 000 km², inférieure aux États-Unis selon cette convention.', 'https://data.un.org/en/iso/CN.html'),
         ],
         precision='Rapport dérivé : 17 098 000 / 9 984 670 = 1,7124, arrondi à 1,7. Ne pas inclure les territoires ukrainiens occupés dans le tracé de la Russie. Les superficies américaines varient selon la convention des eaux : critère et source conservés à l’écran et dans la fiche.',
         legende='Superficie totale, eaux comprises : avais-tu trouvé le podium ? Ton score sur 3 en commentaire.',
         hashtags=['#geographie', '#pays', '#top3', '#HistoiresPasBanales'], musique='Instrumental découverte, léger et rythmé, distinct des deux autres pistes.'),
]

def main():
    for v in VIDEOS:
        folder = OUT / f"{v['numero']:02d}-{v['slug']}"
        folder.mkdir(exist_ok=True)
        scenes = []
        for i, (rank, text, screen, visual, prompt) in enumerate(v['scenes']):
            voice = text
            for a, b in [('2026','deux mille vingt-six'), ('145','cent quarante-cinq'), ('13 000','treize mille'), ('320','trois cent vingt'), ('160','cent soixante'), ('100','cent'), ('60','soixante'), ('17,1','dix-sept virgule un'), ('9,8','neuf virgule huit'), ('1,7','un virgule sept'), ('10','dix'), ('3','trois'), ('2','deux'), ('1','un')]:
                voice = voice.replace(a, b)
            scenes.append(dict(narration=text, narration_voix=voice, rang=rank, texte_ecran=screen,
                               visuel=visual, image_prompt=prompt + ' Vertical 9:16. No text, no logo, no blood.',
                               animate=i == 0, motion_prompt='Natural movement, steady camera, no artificial speed increase.' if i == 0 else ''))
        data = {k: v[k] for k in ['numero','titre','titre_fixe','serie','critere','reference','legende','hashtags']}
        data.update(format='top', date_verification=DATE, statut='Préparation éditoriale - voix et montage non produits',
                    hook=scenes[0]['narration'], hooks_alternatifs=v['hooks'], scenes=scenes,
                    sources_a_verifier=[f'{fact} {url}' for fact, url in v['sources']],
                    musique_direction=v['musique'], duree_cible_secondes=[65,80])
        data['script'] = ' '.join(s['narration'] for s in scenes)
        (folder/'histoire.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        (folder/'script.txt').write_text('\n\n'.join(s['narration'] for s in scenes)+'\n', encoding='utf-8')
        (folder/'voix-texte.txt').write_text('\n\n'.join(s['narration_voix'] for s in scenes)+'\n', encoding='utf-8')
        verification = f"# Sources - vidéo {v['numero']}\n\nVérification web du 8 novembre 2026.\n\nCritère : {v['critere']}\n\n"
        verification += '\n\n'.join(f'- {fact} [Source]({url})' for fact,url in v['sources'])
        verification += '\n\n' + v['precision'] + '\n\nLes faits sont documentés ; les droits de réutilisation des visuels restent à contrôler asset par asset. Aucune séquence du créateur de référence à reprendre.\n'
        (folder/'verification.md').write_text(verification, encoding='utf-8')
        brief = f"# Montage - vidéo {v['numero']}\n\nStatut : préparation. Objectif 65 à 80 s ; durée réelle à mesurer après synthèse puis sur MP4.\n\n"
        brief += 'Images réelles identifiées et autorisées en priorité. Les prompts JSON sont uniquement des solutions illustratives, jamais des archives. Ne pas déclencher le pipeline générique : son habillage historique doit être remplacé par le layout HPB actuel.\n\n'
        brief += 'Logo haut gauche, header/footer permanents, hook bas gauche pendant 4 s, dernière ligne jaune. Sous-titres de 5 mots maximum, mot actif jaune. Plans portrait plein écran, prises distinctes, pas de miroir ni de boucle répétitive.\n\n'
        brief += f"Musique : {v['musique']} Piste de bibliothèque autorisée, provenance conservée et atténuation sous la voix.\n\n"
        brief += '\n\n'.join(f"## Scène {i+1} - rang {s['rang'] if s['rang'] else 'fin'}\n\n{s['narration']}\n\nÉcran : {s['texte_ecran']}\n\nPlan : {s['visuel']}" for i,s in enumerate(scenes))
        (folder/'montage.md').write_text(brief+'\n', encoding='utf-8')
        (folder/'publication.txt').write_text(v['legende']+'\n\n'+' '.join(v['hashtags'])+'\n\nPréparation : vidéo non rendue. Label IA pour la voix synthétique lors de la publication.\n', encoding='utf-8')
        print(folder.name, len(data['script'].split()), 'mots', len(scenes), 'scènes')

if __name__ == '__main__':
    main()
