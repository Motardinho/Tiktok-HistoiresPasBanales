# Vérification - vidéo 18 - TOP 3 DES PLUS GRANDS PAYS DU MONDE

Contrôle refait les 9 et 10 novembre 2026. Chaque ligne indique ce qui a été lu directement à la source et ce qui ne l'a pas été.

## 1. Superficies - une même source pour tout le podium

Source unique retenue : **ONU, Demographic Yearbook 2024 (75e édition, la dernière en ligne au 10 novembre 2026 ; aucune édition 2025 publiée), tableau 3, colonne « Surface area (km²) 2024 »**.
PDF lu directement : https://unstats.un.org/unsd/demographic-social/products/dyb/documents/dyb2024/table03.pdf

| Pays | ONU DYB 2024 | CIA World Factbook (dernière édition) | Britannica |
|---|---|---|---|
| Russie | 17 098 246 km² | 17 098 242 km² | non vérifié (page inaccessible, 403) |
| Canada | 9 984 670 km² | 9 984 670 km² (terres 9 093 507 + eaux 891 163) | non vérifié |
| États-Unis | 9 833 517 km² | 9 833 517 km² (terres 9 147 593 + eaux 685 924) | non vérifié directement ; valeur citée par des sources secondaires : 9 525 067 km², hors eaux côtières et territoriales |
| Chine | 9 600 000 km² | 9 596 960 km² (terres 9 326 410 + eaux 270 550) | non vérifié directement ; valeur de mémoire non confirmée : environ 9 572 900 km² |

Précisions sur les sources :

- ONU : la note de l'édition définit la superficie comme « terres + eaux intérieures ». Les chiffres de la Chine excluent Hong Kong, Macao et Taïwan (note du tableau). La note 156 sur la Crimée porte sur la population de la Russie, pas sur la superficie (17 098 246 km² est la valeur publiée depuis avant 2014).
- CIA World Factbook : **publication arrêtée par la CIA le 4 février 2026** (dépêche AP reprise par WTOP : https://wtop.com/government/2026/02/cia-ends-publication-of-its-popular-world-factbook-reference-tool/). Les valeurs ci-dessus viennent du miroir public du dernier état du Factbook (https://github.com/factbook/factbook.json, fichiers `north-america/us.json`, `north-america/ca.json`, `central-asia/rs.json`, `east-n-southeast-asia/ch.json`). À citer comme « dernière édition du World Factbook (2026) », pas comme une source vivante.
- Britannica : les pages renvoient une erreur 403 aux outils automatiques ; je n'ai rien lu directement. **Ne pas citer Britannica dans la vidéo ni dans la légende sans relecture humaine de la page** https://www.britannica.com/topic/list-of-the-total-areas-of-the-worlds-countries-dependencies-and-territories-2130540

### Le piège du n°3 : États-Unis ou Chine

Décomposition officielle du chiffre américain (US Census Bureau, « State Area Measurements », limites au 1er janvier 2010, page révisée le 16 décembre 2021, lue directement : https://www.census.gov/geographies/reference-files/2010/geo/state-area.html) :

- terres : 9 147 593 km²
- eaux intérieures : 221 824 km²
- Grands Lacs : 155 643 km²
- eaux côtières : 109 652 km²
- eaux territoriales : 198 806 km²
- total : 9 833 517 km²

**Pourquoi les sources divergent, en une phrase :** le total américain de 9,83 millions de km² repris par l'ONU et la CIA inclut 308 458 km² d'eaux côtières et territoriales (mer), alors que le chiffre chinois d'environ 9,6 millions n'en compte pas ; sans ces eaux marines, les États-Unis tombent à 9 525 060 km² (calcul sur les données du Census), donc derrière la Chine, dont le chiffre dépend en plus du traitement de Taïwan et des zones contestées avec l'Inde.

**Recommandation : garder les États-Unis en n°3, mais en disant la convention, et faire de l'ex æquo avec la Chine le fun fact de l'entrée.**

- Raison : c'est le seul choix qui laisse les trois entrées dans une même source et une même édition (ONU, DYB 2024), et c'est aussi le classement du dernier World Factbook.
- Formulation exacte conseillée à l'oral : « Numéro trois : les États-Unis. Neuf virgule huit millions de kilomètres carrés selon l'ONU, eaux côtières comprises. »
- Suite conseillée (fun fact) : « Sans ses eaux côtières, le pays repasse derrière la Chine, à neuf virgule six millions : la troisième place se joue à la façon de compter. »
- Mention à l'écran : `9,8 MILLIONS DE KM²` puis `ONU - EAUX CÔTIÈRES COMPRISES` ou `CHINE : 9,6 MILLIONS`.

**À corriger par rapport à la version actuelle :**

1. `histoire.json` écrit « superficies de référence (terres et eaux, hors territoire maritime) ». C'est **faux pour les États-Unis** : 9 833 517 km² inclut 198 806 km² d'eaux territoriales et 109 652 km² d'eaux côtières.
2. « Environ 9,8 millions de kilomètres carrés, en comptant les terres et les eaux » : exact mais trompeur, car la phrase laisse croire à une convention identique à celle du Canada (terres + eau douce). Préciser « eaux côtières comprises ».
3. Le champ `critere` annonce « valeurs de référence ONU et Statistique Canada » : deux sources. Avec le DYB 2024, une seule source suffit pour les trois (le chiffre canadien y est identique à celui de Statistique Canada).
4. La Chine n'est jamais mentionnée dans le script actuel : un spectateur qui a appris « Chine 3e » criera à l'erreur en commentaire. La mentionner désamorce la critique.

## 2. Contrôle des phrases du script actuel

| Affirmation | Verdict | Détail |
|---|---|---|
| États-Unis environ 9,8 millions de km² | Confirmé avec réserve | 9 833 517 km² (ONU DYB 2024), eaux côtières et territoriales comprises |
| « L'Alaska fait bien partie du total » | Confirmé | Alaska : 1 723 337 km² au total, dont 1 477 953 de terres (Census, limites 2010), soit 17,5 % du total américain (calcul) |
| Canada « presque 10 millions de km² » | Confirmé | 9 984 670 km² (ONU DYB 2024 ; Statistique Canada, Annuaire du Canada 2012, archivé : https://www150.statcan.gc.ca/n1/pub/11-402-x/2012000/chap/geo/geo-eng.htm) |
| Canada : plus long littoral du monde, trois océans | Confirmé | « Canada has the longest coastline in the world, linking the Atlantic, Arctic, and Pacific oceans » - gouvernement du Canada, page datée du 7 juin 2024 : https://www.canada.ca/en/services/environment/our-environment/nature-based-climate-solutions/coastlines.html |
| Russie environ 17,1 millions de km² | Confirmé | 17 098 246 km² (ONU DYB 2024) |
| « De l'Europe jusqu'au nord de l'Asie » | Confirmé | Formulation générale exacte |
| Russie = environ 1,7 fois le Canada | Confirmé | 17 098 246 / 9 984 670 = 1,71 (calcul) |
| Ordre États-Unis, Canada, Russie | Confirmé selon ONU et dernier Factbook | Voir le piège du n°3 |

Rien n'a changé dans ces superficies entre 2025 et 2026 : ce sont des valeurs de référence, pas des mesures annuelles. Le millésime « 2026 » du titre ne doit pas laisser croire à une mesure nouvelle ; l'année réelle à citer est « ONU, édition 2024 ».

## 3. Chiffres complémentaires demandés

| Fait | Valeur | Année des données | Source | Statut |
|---|---|---|---|---|
| Part des terres émergées occupée par la Russie | environ 11 % (16 377 742 km² de terres / 148,94 millions de km² de terres émergées = 11,0 % ; 11,5 % en prenant la superficie totale) | dernier Factbook (2026) | Calcul sur les fiches `rs.json` et `xx.json` du miroir factbook.json | Calculé par moi, pas un chiffre publié tel quel. Dire « environ un neuvième » ou « environ 11 % » |
| Fuseaux horaires de la Russie | 11, de UTC+2 (Kaliningrad) à UTC+12 (Kamtchatka) | loi fédérale entrée en vigueur le 26 octobre 2014 | Dernier Factbook : « Russia has 11 time zones, the largest number of contiguous time zones of any country » ; Interfax, 22 juillet 2014 : https://interfax.com/newsroom/top-stories/41758/ | Confirmé (texte de loi russe non lu) |
| Fuseaux horaires du Canada | 6 (Pacifique, Rocheuses, Centre, Est, Atlantique, Terre-Neuve), sur 4 h 30 | en vigueur | Dernier Factbook : « Canada has six time zones » ; L'Encyclopédie canadienne : https://thecanadianencyclopedia.ca/en/article/time-zones-and-legal-time | Confirmé |
| Longueur du littoral canadien | 243 042 km, îles comprises | Annuaire du Canada 2012 (page archivée, modifiée le 7 octobre 2016) | Statistique Canada : https://www150.statcan.gc.ca/n1/pub/11-402-x/2012000/chap/geo/geo-eng.htm | Confirmé. Attention : le Factbook donne 202 080 km ; la longueur d'une côte dépend de l'échelle de mesure. Le record (1er mondial) tient dans les deux cas. Préférer « plus de 200 000 km » ou citer « 243 000 km selon Statistique Canada » |
| Distance est-ouest du Canada | 5 514 km | Annuaire du Canada 2012 | Statistique Canada (même page) | Confirmé |
| Frontière Canada - États-Unis | 8 890 km (StatCan) ; 8 891 km (Factbook), dont 2 475 km avec l'Alaska | idem | Statistique Canada ; dernier Factbook | Confirmé, plus longue frontière internationale du monde |
| Nombre de lacs du Canada | près de 900 000 lacs de plus de 10 hectares, soit 62 % des lacs de cette taille dans le monde (1,42 million au total) | étude publiée le 15 décembre 2016 | Messager, Lehner et al., Nature Communications (base HydroLAKES) ; résumé de l'université McGill lu directement : https://reporter.mcgill.ca/taking-stock-of-the-worlds-lakes/ | Confirmé via le communiqué de McGill ; article de Nature non ouvert (redirection d'authentification). Le Factbook écrit « at least 2 million and possibly over 3 million lakes, more than all other countries combined » (tous seuils confondus) |
| Eau douce du Canada | 891 163 km² d'eau douce, près de 9 % du territoire | Annuaire du Canada 2012 | Statistique Canada ; dernier Factbook | Confirmé |
| Distance est-ouest de la Russie | environ 9 000 km | - | Valeur courante (Britannica) | **Non vérifié** auprès d'une source primaire. Préférer les 11 fuseaux horaires ou le Transsibérien |
| Transsibérien Moscou - Vladivostok | 9 288 à 9 289 km | - | Britannica (extrait de moteur de recherche, page non lue) | **Non vérifié directement** ; chiffre concordant dans toutes les sources secondaires. Dire « près de 9 300 km » |
| Lac Baïkal | lac le plus profond du monde, 1 642 m ; environ un cinquième de l'eau douce de surface non gelée | - | Dernier Factbook (note géographique Russie) : « the deepest lake in the world, is estimated to hold one fifth of the world's fresh surface water » ; profondeur : Wikipédia citant INTAS | Part confirmée via le Factbook ; profondeur de source secondaire (l'UNESCO arrondit à 1 700 m, page non lue) |
| Écart Russie - États-Unis aux îles Diomède | 3,8 km entre la Grande Diomède (Russie) et la Petite Diomède (États-Unis) ; 21 heures de décalage (20 en été) | image Landsat 8 du 6 juin 2017 | NASA Earth Observatory, « Yesterday and Tomorrow Islands » : https://earthobservatory.nasa.gov/images/91638/yesterday-and-tomorrow-islands | Confirmé par l'extrait du moteur de recherche ; la page elle-même n'a pas pu être ouverte par l'outil |
| « La Russie est plus grande que Pluton » | **FAUX depuis 2015** | survol New Horizons, juillet 2015 | NASA, fiche Pluton mise à jour le 22 avril 2025 : diamètre 2 377 km (https://science.nasa.gov/dwarf-planets/pluto/facts/) ; surface = π × d² = 17,75 millions de km² (calcul) | La Russie (17,10 millions) fait 96 % de la surface de Pluton. Formulation juste : « presque la surface de Pluton » |
| Mont Elbrouz | plus haut sommet d'Europe | - | Dernier Factbook (note géographique Russie) | Confirmé |
| Chine : un seul fuseau horaire | la Chine est le plus grand pays à n'avoir qu'un seul fuseau ; cinq avant 1949 | - | Dernier Factbook (fiche Chine) | Confirmé |

## 4. Fun facts proposés

1. **États-Unis - la 3e place se joue à l'eau salée.** Avec leurs eaux côtières : 9,83 millions de km². Sans : 9,53 millions, derrière la Chine (9,6 millions). Sources : ONU DYB 2024, US Census. Plan raccord : oui (côte et glaciers de l'Alaska pour les « eaux côtières », puis Grande Muraille, Zhangjiajie, Shanghai ou Tibet pour la Chine).
2. **États-Unis / Russie - 3,8 km entre les deux pays.** Aux îles Diomède, dans le détroit de Béring, les deux géants se font face, avec 21 heures de décalage. Source : NASA Earth Observatory, 2017. Plan raccord : oui, reportage Voice of America tourné à Little Diomede (voir catalogue).
3. **Canada - 62 % des lacs du monde.** Près de 900 000 lacs de plus de 10 hectares : plus que tous les autres pays réunis. Source : Messager et al., Nature Communications, 2016 (McGill). Plan raccord : oui (lacs turquoise des Rocheuses, survol de Canmore).
4. **Canada - le plus long littoral du monde**, plus de 200 000 km sur trois océans (243 042 km selon Statistique Canada). Source : gouvernement du Canada, 2024 ; Statistique Canada. Plan raccord : oui (côte de Terre-Neuve, icebergs).
5. **Russie - 11 fuseaux horaires.** Quand il est midi à Kaliningrad, il est 22 h au Kamtchatka. Source : loi de 2014, dernier Factbook. Plan raccord : oui (Moscou au couchant, puis volcans et côte du Kamtchatka).
6. **Russie - presque la surface de Pluton.** 17,1 millions de km² contre 17,7 millions pour la planète naine. Attention : la version virale « plus grande que Pluton » est fausse depuis la mesure de New Horizons en 2015. Source : NASA. Plan raccord : non (aucune image de Pluton téléchargée ; une image NASA de New Horizons, domaine public, conviendrait, mais c'est une photo).

Les trois meilleurs : 1 (désamorce la polémique Chine / États-Unis), 2 (très visuel et peu connu), 3 (chiffre fort et images spectaculaires).

## 5. Pièges de formulation

- Ne pas dire « plus grande que Pluton ».
- Ne pas dire « le Canada a plus de lacs que le reste du monde » sans le seuil : la donnée solide est « 62 % des lacs de plus de 10 hectares ».
- Ne pas donner 243 042 km comme une mesure exacte et actuelle : c'est une valeur de référence de Statistique Canada, et d'autres sources donnent 202 080 km.
- Ne pas dire « terres et eaux intérieures » pour les États-Unis.
- Ne pas présenter la Chine comme « 4e sans discussion » : selon la convention, elle est 3e.
- « 2026 » dans le titre : édition de la vidéo, pas année de mesure. Année réelle des données : ONU, édition 2024.
- Images du Caucase : ne pas les légender « Sibérie ». Images de Banff et Canmore : Alberta, pas « Grand Nord ».
