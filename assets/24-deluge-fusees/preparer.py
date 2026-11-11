import json
from pathlib import Path
p=Path('out/24-deluge-fusees')
texts=[
"Pourquoi inonder une fusée ? Regarde ce déluge. Au pied de la tour de lancement, des torrents d’eau jaillissent de partout. Et ils servent aussi à combattre quelque chose qu’on ne voit pas : le bruit.",
"Quand les moteurs s’allument, ils produisent des ondes de pression extrêmement puissantes. Elles peuvent rebondir sur la plateforme et remonter vers la fusée. Au point d’endommager le véhicule et ce qu’il transporte.",
"La NASA arrose donc le pas de tir pour atténuer ce choc acoustique. L’eau contribue aussi à protéger les installations de la chaleur. Ce n’est pas une simple douche : c’est une partie du système de protection.",
"Pour préparer Artémis deux, la NASA a testé un déluge d’environ un million et demi de litres. Imagine mille cinq cents tonnes d’eau qui se déversent autour de la plateforme.",
"Et ces énormes buses ont un petit nom : les rainbirds. Littéralement, les oiseaux de pluie. Drôles d’oiseaux : ils crachent des torrents autour de l’endroit où la fusée va décoller.",
"Mais même avec cette eau, le décollage reste assourdissant. Le but, c’est de réduire les contraintes sur la machine, pas de rendre les moteurs silencieux.",
"Voilà pourquoi on teste aussi le déluge tout seul, avant de lui confier une fusée. Ici, tu regardes un essai au sol, sans décollage.",
"Tu pensais que toute cette eau servait seulement contre la chaleur ? Pas banal, hein ?"
]
sources=[{'fait':'Eau, chaleur, 400000 gallons pour essais Artemis II, réservoirs et buses rainbirds','url':'https://www.nasa.gov/blogs/missions/2024/07/19/nasa-kennedy-teams-complete-water-flow-tests-for-artemis-ii-mission/','calcul':'400000 gallons US × 3,785411784 = 1514164,7 litres, environ 1500 tonnes'}, {'fait':'Ondes réfléchies vers le véhicule et risque de dommages','url':'https://www.nasa.gov/podcasts/houston-we-have-a-podcast/the-space-launch-system-part-2/'}, {'fait':'Réduction du bruit, sans silence','url':'https://www.nasa.gov/wp-content/uploads/2023/03/Artemis20I20Reference20Guide_Inter.pdf'}]
d=dict(titre_fixe='POURQUOI INONDER UNE FUSÉE ?',titre_lignes=['POURQUOI','INONDER','UNE FUSÉE ?'],titre_interligne=22,serie='ESPACE - LE DÉLUGE DES FUSÉES',format='histoire',reference='https://www.tiktok.com/@faiseemoc84/video/7320682957964905760',reference_fichier='out/20-telephone-2899-dollars/version-validee/final.mp4',reference_auteur='HPB - téléphones validée (étalon qualité demandé par Marc)',musique='espace',scenes=[dict(narration=t,narration_voix=t) for t in texts],affichage={'artémis deux':'Artémis II','un million et demi de litres':'1,5 million de litres','mille cinq cents tonnes':'1 500 tonnes'},bandeaux=[],fun_fact=dict(scene=4,texte=['LES BUSES S’APPELLENT','« OISEAUX DE PLUIE »'],source=sources[0]['url']),sources_a_verifier=sources,statut='script vérifié - avant synthèse')
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
(p/'script.txt').write_text('\n\n'.join(texts),encoding='utf8')
(p/'preparation.md').write_text('Préparation - 10 novembre 2026, Europe/Paris\n\nRéférence qualité : copie validée du dossier 20, conservée intacte.\n\nHooks : Pourquoi inonder une fusée ? (retenu) ; De l’eau contre le bruit ; La douche géante des fusées ; Une fusée menacée par son propre bruit ; Un million et demi de litres avant le décollage.\n\nSources NASA vérifiées. Volume total, pas un débit. Masse arrondie, densité approximée de l’eau à 1 kg/L. Rainbirds : traduction littérale du surnom documenté. Essais NASA du 24 octobre 2023 et décollage Artemis I de 2022. Ne pas présenter les essais comme un lancement.\n',encoding='utf8')
print('Mots',len(' '.join(texts).split()))
