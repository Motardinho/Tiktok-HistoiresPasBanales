# Planning de publication - 9 au 11 novembre 2026

Mis à jour le 9 novembre 2026 à 0 h 15 après la refonte des vidéos 13 à 18. Cinq vidéos validées par Marc, 1080x1920, plus de 60 s, empreinte SHA-256 identique à `validation-utilisateur.json` et à `version-validee/final.mp4`. Les comparaisons sont plus récentes que les finales.

**Anciens posts supprimés :** le 9 novembre, Marc a supprimé dans TikTok Studio les trois posts programmés le 8 novembre (astronautes, bouchons, voitures), qui contenaient les anciennes versions. Les cinq vidéos du tableau sont à programmer avec les nouveaux `final.mp4`. État : 13 (astronautes) programmée dans TikTok Studio le 9 novembre à 0 h 30 pour le 9 novembre 17 h 50, sans label IA ; 15 (bouchons) programmée pour le 10 novembre 12 h 15, sans label IA ; 14 (voitures) programmée pour le 10 novembre 17 h 40, sans label IA ; 18 (pays) programmée pour le 11 novembre 11 h 40, sans label IA ; 16 (armées) programmée pour le 11 novembre 18 h 10, sans label IA. **Les cinq vidéos sont programmées** (contrôlé dans TikTok Studio, Publications, le 9 novembre vers 0 h 50). Marc met systématiquement #record sur les tops : ajouté le 9 novembre aux `legende.txt` et `publication.txt` de 14, 15, 16 et 18. Dans TikTok, la légende des voitures porte en plus #voitures #byd #bugatti, et celle des bouchons, programmée avant cette règle, n'a pas #record.

| Jour | Heure | N° | Vidéo | Durée | Fichier | Légende |
|---|---|---|---|---|---|---|
| Lun 9 nov | 17 h 50 | 13 | Se peser dans l'espace | 70,5 s | [final.mp4](13-astronautes-sport-en-orbite/final.mp4) | [legende.txt](13-astronautes-sport-en-orbite/legende.txt) |
| Mar 10 nov | 12 h 15 | 15 | Villes les plus embouteillées | 65,9 s | [final.mp4](15-villes-plus-lentes-tomtom-2024/final.mp4) | [legende.txt](15-villes-plus-lentes-tomtom-2024/legende.txt) |
| Mar 10 nov | 17 h 40 | 14 | Voitures les plus rapides | 81,6 s | [final.mp4](14-trois-records-voitures-vitesse/final.mp4) | [legende.txt](14-trois-records-voitures-vitesse/legende.txt) |
| Mer 11 nov | 11 h 40 | 18 | Plus grands pays du monde | 79,3 s | [final.mp4](18-pays-plus-grands-superficie/final.mp4) | [legende.txt](18-pays-plus-grands-superficie/legende.txt) |
| Mer 11 nov | 18 h 10 | 16 | Armées les plus puissantes | 98,6 s | [final.mp4](16-armees-puissantes-gfp-2026/final.mp4) | [legende.txt](16-armees-puissantes-gfp-2026/legende.txt) |

Tous les créneaux sont choisis par Marc : le 11 novembre, pays à 11 h 40 puis armées à 18 h 10, à sa demande. La vidéo 17 (animaux) n'est pas validée et n'est pas programmée.

Le 9 novembre, `#histoirevraie` a été ajouté en tête des hashtags des cinq légendes (`legende.txt` et `publication.txt`). Chaque légende garde 4 ou 5 hashtags.

La légende complète à copier-coller est dans `legende.txt`, identique à `publication.txt`. Elle contient l'accroche, la question, les hashtags, les sources et les crédits.

## Points à vérifier à la main avant chaque post (R-09)

- **Voitures** : Yangwang U9 Xtreme à 503,17 km/h le 1er novembre 2026 à Abou Dhabi (FIA et BYD, 6 novembre 2026). C'est un record très récent, à revérifier le jour du post. Les trois vitesses sont des pointes dans un seul sens. Si un commentaire parle de la moyenne aller-retour, répondre en commentaire épinglé.
- **Bouchons** : INRIX 2025, Paris 90 h, Londres 91 h, New York 102 h. La narration dit « comparaison de trois villes », mais le titre à l'écran annonce « TOP 3 DES VILLES LES PLUS EMBOUTEILLÉES ». Si une ville hors de ces trois dépasse New York dans le classement mondial INRIX 2025, le titre sera contesté.
- **Armées** : Global Firepower 2026, SIPRI 2025, FAS 2026. Le repère Hiroshima donne un ordre de grandeur. Ce n'est pas la puissance de chaque ogive chinoise.
- **Pays** : superficies totales ONU et Statistique Canada, eaux comprises. Selon une autre convention, la Chine peut passer devant les États-Unis : c'est le commentaire le plus probable.
- **Astronautes** : sources ASC (Saint-Jacques, 2019) et NASA. Les plans autres que la pesée illustrent la microgravité.

## Label IA

D'après la décision du 8 novembre 2026 (`docs/decisions.md`), les posts sont publiés sans label « Contenu généré par IA », à la demande de Marc. Cela déroge au CLAUDE.md, car la voix est synthétique. La décision est à réévaluer en cas d'alerte TikTok.

## Checklist avant chaque post

- [ ] Fichier `final.mp4` du tableau (pas `_montage/` ni une ancienne copie)
- [ ] Légende copiée depuis `legende.txt`
- [ ] Le chiffre clé revérifié le jour même (voir ci-dessus)

## Après publication (J+1)

Noter la rétention à 3 s, le visionnage complet et les partages. Consigner dans `docs/decisions.md` toute décision de format.

**9 novembre, 18 h 30 :** la vidéo voitures corrigée (validée à 18 h 08, SHA-256 134230f3…) remplace l'ancien post, que Marc a supprimé. Elle est reprogrammée le 10 novembre à 17 h 40, avec la même légende (9 hashtags dont #record). L'astronautes est publiée. Contrôle dans Publications : cinq posts, un seul post voitures.

**9 novembre, soir - recentrage des sous-titres :** à la demande de Marc, les vidéos 13, 14, 15, 16 et 18 ont été réexportées avec sous-titres, bandeaux et fun fact centrés sur l'écran et sous-titres plus grands. Plans, audio et durées inchangés. Les fichiers `final.mp4` du tableau sont les nouveaux exports, pas encore validés ; les versions validées restent dans `version-validee/` de chaque dossier. **Les posts déjà programmés dans TikTok Studio (14, 15, 16, 18) et le post publié (13) contiennent encore les anciennes versions.**

**10 novembre, soir - vidéo 20 (téléphones) validée par Marc** (SHA-256 9205d6e8…, `version-validee/`). Programmée pour le **jeu 12 nov à 18 h 00** :
- YouTube Shorts, chaîne Histoires pas banales : programmée, https://youtube.com/shorts/PI5URKbYLEY (titre « Les 3 téléphones les plus chers en vente en France #shorts », légende de `legende.txt`, utilisation de l'IA « Non » selon les quatre cas listés par YouTube).
- TikTok : d'abord programmée par erreur sur le compte moovini.app ; Marc l'a retirée (« c bon », non revérifié côté moovini). Reprogrammée le 11 nov sur le compte **Histoires pas banales** pour le 12 nov 18 h 00 (contrôlé dans Publications : 01:03, légende complète). Label IA désactivé ; « Vérification de contenu simple » désactivée pour ce post car bloquée « en cours » plus de 10 min.

**État TikTok HPB relevé le 11 nov :** 13 astronautes publiée le 9 nov ; 15 bouchons (1:05) publiée le 10 nov à 12 h 15 et 14 voitures (1:21) publiée le 10 nov à 17 h 40, toutes deux en ANCIENNE version ; 18 pays (1:19, 11 nov 11 h 40) et 16 armées (1:38, 11 nov 18 h 10) toujours programmées en ANCIENNE version ; 20 téléphones (1:03, 12 nov 18 h 00), version validée.

**Vues relevées le 11 nov vers 13 h (téléphone + TikTok Studio web) :** voitures 331 vues (99,4 % Pour toi, visionnage moyen 10,3 s sur 82 s, 0,88 % jusqu'au bout) ; astronautes 0 ; bouchons 0 (visionnage moyen 7,7 s, uniquement les lectures de Marc) ; pays 0 (publiée depuis 1 h). Aucune restriction, violation ni avertissement affiché dans l'app, dans les notifications système ni dans Studio web ; contrôle du public 18+ désactivé. TikTok n'a simplement pas diffusé ces deux vidéos, sans donner de motif.

**10 novembre - refonte :** les vidéos 14, 15, 16, 17, 18 et 20 ont été entièrement refaites (voir `LIVRAISON-REFONTE-14-20.md`). Les posts programmés dans TikTok Studio contiennent les ANCIENNES versions ; à remplacer après validation de Marc. Nouveaux points à vérifier le jour du post dans `_montage/controle-livraison.json` de chaque dossier.

## Programmation du 13 novembre 2026 (faite le 11 novembre)

Vidéos validées par Marc et pas encore programmées : 24 (déluge des fusées) et 26 (perdu 9 jours dans le Sahara). Empreintes SHA-256 des fichiers importés identiques à `version-validee/final.mp4` (24 : d833704d…, 26 : 13e24c0f…). Comptes vérifiés avant import : TikTok Studio sur @histoirespasbanales, YouTube Studio sur Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Ven 13 nov | 12 h 00 | 24 | « Pourquoi inonder une fusée ? », légende de `legende.txt` | [Pourquoi inonder une fusée au décollage ?](https://youtube.com/shorts/U-6RRTQ0S2c) |
| Ven 13 nov | 18 h 00 | 26 | « Perdu 9 jours dans le Sahara… », légende de `legende.txt` | [Perdu 9 jours dans le Sahara en pleine course](https://youtube.com/shorts/0WUwNaSlO2U) |

- TikTok : vérification de contenu simple passée (« Aucun problème constaté ») avant de programmer ; importations haute qualité actives ; label IA désactivé (décision du 8 novembre) ; couverture = première image.
- YouTube : « Aucun problème détecté » sur les droits ; miniature personnalisée = image à 0:00 extraite du MP4 validé ; « Utilisation de l'IA » : Non, confirmé par Marc le 11 novembre ; pas pour enfants, sans limite d'âge ; descriptions = `publication.txt`.
- 26 : le fun fact « revenu courir la course 6 fois » ne repose que sur Wikipédia (une autre source parle de 8 participations). Publié à la demande de Marc : une erreur de détail fait commenter (règle notée dans le skill publier-tiktok). Répondre ou épingler si un commentaire corrige.
- L'appli TikTok du téléphone n'offre pas de programmation : la programmation passe par TikTok Studio dans Chrome.

## Programmation du 14 novembre 2026 (faite le 11 novembre)

Les deux dernières vidéos validées et pas encore programmées : 27 (demi-tour dans la tempête) et 28 (l'OM a acheté un match). La 25 (montagnes russes) était déjà programmée le 12 novembre à 12 h 00. Compte vérifié avant import : TikTok Studio sur Histoires pas banales (liste Publications et aperçu du lecteur).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Sam 14 nov | 12 h 00 | 27 | « Il fait demi-tour en pleine tempête… », légende de `legende.txt` | [Il fait demi-tour en pleine tempête pour sauver son rival](https://youtube.com/shorts/y-X2c4KQ1tc) |
| Sam 14 nov | 18 h 00 | 28 | « L'OM a acheté un match en 1993… », légende de `legende.txt` | [L'OM a acheté un match en 1993 : l'affaire VA-OM](https://youtube.com/shorts/s29Dw25xZkA) (v2, remplacée le 12 nov.) |

- Empreintes SHA-256 des fichiers importés, recalculées dans la page, identiques à `version-validee/final.mp4` (27 : fd7e2935…, 28 : d776598f…). Durées 69,8 s et 68,7 s, 1080 × 1920.
- Légendes collées depuis `legende.txt` (fins de ligne CRLF converties) et comparées caractère pour caractère dans l'éditeur.
- Vérification de contenu simple : « Aucun problème constaté » pour les deux avant de programmer. Pour la 27, le premier import est resté « en cours » plus de 15 minutes : il a été abandonné sans être enregistré, puis réimporté ; la seconde vérification est passée en quelques minutes.
- Importations haute qualité actives, label IA désactivé (vrais plans INA/Pexels, voix ElevenLabs du compte qui n'imite personne), couverture = première image.
- Contrôle final dans Publications : 27 au 14 nov 12:00 et 28 au 14 nov 18:00 (GMT+1 Paris), un seul post chacune. Le brouillon déjà présent (Brouillons 1) n'a pas été touché.
- 27 : le fun fact du fax ne repose que sur une source (anecdote secondaire, pas d'alerte selon la règle de Marc). 28 : affaire jugée en 1995, pas de victime mineure.
- YouTube Shorts (chaîne Histoires pas banales, UCoCQQfS6h1lhqHdB21PpAuw), demandé par Marc le 11 novembre : « toujours TikTok ET YouTube Shorts ». Mêmes fichiers (SHA-256 recalculé dans la page), description = `publication.txt` vérifiée caractère pour caractère, pas pour enfants, sans limite d'âge, « Contenu modifié ou synthétique » : Non. Programmation relue dans Studio : 27 au 14 nov 12:00 et 28 au 14 nov 18:00, fuseau GMT+1 heure locale. Revendications : « Cette vidéo ne fait l'objet d'aucune revendication » pour les deux (les archives INA de la 27 n'ont pas déclenché de Content ID).
- Miniatures YouTube : 27 = image à 0:00 extraite par ffmpeg et importée. Pour la 28, YouTube a demandé une « validation unique » du compte pour importer plus de miniatures personnalisées dans la journée : refusée par Claude (action de compte réservée à Marc), puis choisi dans « Sélectionner dans la vidéo » le premier plan proposé, identique à l'image d'ouverture (frappe de nuit, titre « L'OM A ACHETÉ UN MATCH »).

## Montagnes russes sur YouTube Shorts, 11 novembre 2026 à 20 h 00

À la demande de Marc (« essaye de la glisser ce soir vers 20h »), la 25 (montagnes russes), programmée sur TikTok seulement pour le 12 novembre à 12 h 00, est aussi programmée sur YouTube Shorts pour le **11 novembre à 20 h 00** (GMT+1, heure locale) : [Les 3 montagnes russes les plus rapides du monde](https://youtube.com/shorts/mVFPuhz3HxA). Fichier `version-validee/final.mp4`, SHA-256 a461bf57… recalculé dans la page ; description = `version-validee/publication.txt`, vérifiée caractère pour caractère ; pas pour enfants, sans limite d'âge, contenu modifié ou synthétique : Non. Revendications : aucune. Miniature : premier plan de « Sélectionner dans la vidéo », identique à l'image à 0:00 (titre « TOP 3 DES MONTAGNES RUSSES LES PLUS RAPIDES 2026 ») ; « Modifications enregistrées » et horaire 11 nov. 20:00 relus dans Studio.

**Synchro TikTok / YouTube Shorts à partir du 13 novembre** (règle de Marc du 11 novembre : toujours les deux plateformes, mêmes créneaux) :

| Jour | Heure | TikTok | YouTube Shorts |
|---|---|---|---|
| Ven 13 nov | 12 h 00 | 24 fusée | 24 fusée |
| Ven 13 nov | 18 h 00 | 26 Sahara | 26 Sahara |
| Sam 14 nov | 12 h 00 | 27 demi-tour | 27 demi-tour |
| Sam 14 nov | 18 h 00 | 28 OM-VA | 28 OM-VA |

Écarts restants, antérieurs à la règle : le 12 novembre à 12 h 00, TikTok publie la 25 (montagnes russes) et YouTube la 13 (astronautes, déjà publiée sur TikTok le 9) ; la 25 sort sur YouTube le 11 au soir. Le 12 à 18 h 00, la 20 (téléphones) sort sur les deux.

## Programmation du 15 novembre 2026 (faite le 11 novembre)

Vidéo 31 (Pogba braqué pour 13 millions), validée par Marc le 11 novembre après correction de la fin (désistement d'appel de Mathias, photo « Longue vie à mes frères »). Compte vérifié avant import : TikTok `histoirespasbanales`, YouTube chaîne Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Dim 15 nov | 18 h 00 | 31 | « Braqué pour 13 millions par des potes d'enfance… », légende de `legende.txt` | [Pogba braqué pour 13 millions… et son propre frère condamné](https://youtube.com/shorts/Z01EJ1GyvSg) |

- SHA-256 recalculé dans la page avant chaque import, identique à `version-validee/final.mp4` (39928c91…). Durée 73,9 s, 1080 × 1920.
- TikTok : légende comparée caractère pour caractère ; vérification de contenu simple « Aucun problème constaté » ; importations haute qualité actives ; label IA désactivé (vrais plans Pexels, voix du compte qui n'imite personne) ; couverture = première image. Contrôle dans Publications : 15 nov. 18:00 (GMT+1) Paris, un seul post. Un premier essai d'import a fait planter la page (vidage complet de l'éditeur de description) : abandonné sans enregistrement, réimporté dans un nouvel onglet ; ne plus vider entièrement l'éditeur, coller puis supprimer le nom de fichier au clavier.
- YouTube : description = `publication.txt` vérifiée caractère pour caractère ; pas pour enfants, sans limite d'âge ; « Utilisation de l'IA » : Non ; droits d'auteur « Aucun problème détecté » ; un seul Short dans l'onglet Shorts. **Miniature : pas l'image à 0:00.** L'import d'une miniature personnalisée demande la « validation unique » du compte (refusée par Claude, action réservée à Marc) et « Sélectionner dans la vidéo » ne proposait pas l'image d'ouverture ; miniature automatique de YouTube conservée. À corriger par Marc s'il fait la validation : `version-validee/` + `_montage/upload/miniature-0s.jpg`.
- Faits : désistement d'appel confirmé (Foot01, Le Lynx relayant Paris Match) ; virée Adidas 633 articles / 57 227 € (AFP via Blick et 90min), Foot01 donne 47 000 € (écart de détail, publié selon la règle de Marc).

## Vidéo 33 le 15 novembre 2026 à 12 h 00 (faite le 11 novembre)

Vidéo 33 (149 buts contre leur camp), validée par Marc le 11 novembre après ajout de la compétition (championnat national, dernière journée). Créneau choisi par Marc : dimanche 15 novembre à 12 h 00, premier créneau libre. Comptes vérifiés avant import : TikTok Studio sur Histoires pas banales (liste Publications et aperçu), YouTube Studio sur la chaîne Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Dim 15 nov | 12 h 00 | 33 | « Championnat de Madagascar, 31 octobre 2002 : 149 buts contre leur camp… », légende de `legende.txt` | [Ils ont marqué 149 buts contre leur camp… exprès](https://youtube.com/shorts/3Y4YC3aWgGE) |

- SHA-256 recalculé dans la page avant chaque import, identique à `version-validee/final.mp4` (07cf29ad…). Durée 69,8 s, 1080 × 1920.
- YouTube : description = `version-validee/publication.txt` vérifiée dans le champ ; pas pour enfants, sans limite d'âge ; « Utilisation de l'IA » : Non ; « Vérifications terminées. Aucun problème détecté. » ; relu dans l'onglet Shorts : programmée, 15 nov. 2026, un seul Short. **Miniature automatique de YouTube conservée** (limite de 24 h des miniatures personnalisées en cours le 11 novembre) : à remplacer par `33-149-buts-contre-leur-camp/_montage/upload/miniature-0s.jpg` avant le 15 novembre.
- TikTok : légende comparée au fichier dans l'éditeur ; importations haute qualité actives ; label IA désactivé (vrais plans Pexels, voix du compte qui n'imite personne) ; couverture = première image. Vérification de contenu simple : restée « en cours » plus de 15 minutes puis « Une erreur est survenue » ; relancée par Marc, résultat « Aucun problème constaté », puis programmée. Un second import lancé entre-temps dans un autre onglet a été abandonné sans être enregistré. Contrôle dans Publications : 15 nov. 12:00 (GMT+1) Paris, 01:09, un seul post.
- Faits à connaître : ville du match non dite (sources divergentes) ; « dernière journée » déduit du déroulé de la poule finale (Wikipédia) ; rôle du coach attribué à la presse locale. Voir `33-149-buts-contre-leur-camp/controle-livraison.json`.

**Fait le 12 novembre 2026 (voir « Miniatures YouTube mises à jour » plus bas).** ~~À faire à partir du 12 novembre 2026 vers 18 h (fin de la limite de 24 h des miniatures YouTube, signalée par Marc)~~ : dans YouTube Studio, remplacer la miniature automatique du Short 31 (https://youtube.com/shorts/Z01EJ1GyvSg) par `31-pogba-braque-pour-13-millions/_montage/upload/miniature-0s.jpg`, avant sa publication du 15 novembre à 18 h 00. Même chose pour la 30 si elle est programmée d'ici là.

## Vidéo 28 : v1 programmée remplacée par la v2 (12 novembre 2026, vers 1 h)

La 28 (OM-VA) avait été programmée le 11 novembre avec la v1 (SHA-256 d776598f…), puis Marc a validé une v2 avec la photo de Bernard Tapie (ec4a1c5d…, `version-validee/final.mp4`, v1 archivée dans `version-validee/v1-2026-11-11/`). À la demande de Marc (« remplace-la »), même créneau : **sam 14 nov 18 h 00**.

- **TikTok** (compte Histoires pas banales, vérifié dans l'aperçu et la liste Publications) : v2 importée, SHA-256 recalculé dans la page identique ; légende = `version-validee/legende.txt` (crédit photo Tapie ajouté), comparée caractère pour caractère ; importations haute qualité actives ; label IA désactivé ; vérification de contenu simple « Aucun problème constaté » ; couverture = première image. Le post v1 programmé a ensuite été supprimé (post jamais publié). Contrôle dans Publications : un seul post 28, 14 nov. 18:00 (GMT+1), avec le crédit Tapie.
- **YouTube Shorts** (chaîne Histoires pas banales) : nouveau Short [s29Dw25xZkA](https://youtube.com/shorts/s29Dw25xZkA), même titre, description = `version-validee/publication.txt` vérifiée, pas pour enfants, sans limite d'âge, « Utilisation de l'IA » : Non, vérifications « Aucun problème détecté », miniature = image à 0:00 importée (acceptée), programmé le 14 nov. 2026 à 18:00. L'ancien Short v1 (F2gouR167vo) est passé en **Privée** au lieu d'être supprimé : il ne sortira pas ; à supprimer par Marc s'il le souhaite.


## Programmation du 16 novembre 2026 (faite le 12 novembre vers 1 h)

Vidéos 35 (Crashgate) et 36 (Spygate), validées par Marc le 12 novembre (« Validées »), puis « Programmer ». Créneaux : premiers libres après le 15 novembre, pris par Claude. Comptes vérifiés avant import : TikTok Studio sur Histoires pas banales (liste Publications et aperçu), YouTube Studio sur la chaîne Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Lun 16 nov | 12 h 00 | 35 | « Singapour 2008 : un pilote Renault s'écrase dans le mur… », légende de `legende.txt` | [Renault a fait crasher son pilote exprès : le Crashgate de 2008](https://youtube.com/shorts/lOKRugjtazk) |
| Lun 16 nov | 18 h 00 | 36 | « 2007 : 780 pages de secrets Ferrari… », légende de `legende.txt` | [McLaren trahie par une photocopie : 100 millions de dollars d'amende](https://youtube.com/shorts/aMrwWVanZOw) |

- SHA-256 recalculé dans la page avant chaque import, identique à `version-validee/final.mp4` (35 : 3bea3124…, 36 : d1f0cf0c…). Durées 71,2 s et 68,5 s, 1080 × 1920.
- TikTok : légendes comparées au fichier dans l'éditeur ; vérification de contenu simple « Aucun problème constaté » pour les deux avant de programmer ; importations haute qualité actives ; label IA désactivé (vraies séquences et photos, voix du compte qui n'imite personne) ; couverture = première image. Contrôle dans Publications : 16 nov. 12:00 et 16 nov. 18:00 (GMT+1) Paris, un seul post chacune.
- YouTube : description = `publication.txt` vérifiée dans le champ ; pas pour enfants, sans limite d'âge ; « Utilisation de l'IA » : Non. Miniature automatique conservée (limite de 24 h des miniatures personnalisées) : à remplacer par `_montage/upload/miniature-0s.jpg` de chaque dossier avant le 16 novembre.
- **Droits d'auteur : risque réel.** Les deux vidéos contiennent des extraits de la diffusion du Grand Prix de Singapour 2008, de la chaîne officielle Formula 1 (Brésil 2007 et 2008) et d'AP Archive (audience FIA du 13 septembre 2007), cités dans la légende. Programmées avec les vérifications YouTube encore en cours : relire leur résultat dans l'onglet Shorts avant le 16 novembre.
- Faits : voir `controle-livraison.json` et `histoire.json` de chaque dossier. 35 : sanction de Briatore annulée en 2010 pour irrégularité, sans jugement sur les faits ; l'ordre est attribué à la fédération. 36 : montant réellement payé environ 64,5 M$ sur les 100 M$ (commentaire probable).

## Miniatures YouTube mises à jour (12 novembre 2026)

À la demande de Marc (« mets à jour les miniatures »), les miniatures automatiques des Shorts 31, 33, 35 et 36 ont été remplacées dans YouTube Studio (chaîne Histoires pas banales, UCoCQQfS6h1lhqHdB21PpAuw, vérifiée sur chaque page) par `_montage/upload/miniature-0s.jpg` de chaque dossier. Avant import, chaque fichier a été comparé pixel à pixel à l'image à 0:00 de `version-validee/final.mp4` : identiques, et les SHA-256 des MP4 correspondent à `validation-utilisateur.json`. Import accepté sans demande de validation du compte ; « Modifications enregistrées » pour chacun ; la liste Shorts montre l'image titre sur les quatre.

| N° | Short | Miniature |
|---|---|---|
| 31 | [Z01EJ1GyvSg](https://youtube.com/shorts/Z01EJ1GyvSg) | image à 0:00 importée |
| 33 | [3Y4YC3aWgGE](https://youtube.com/shorts/3Y4YC3aWgGE) | image à 0:00 importée |
| 35 | [lOKRugjtazk](https://youtube.com/shorts/lOKRugjtazk) | image à 0:00 importée |
| 36 | [aMrwWVanZOw](https://youtube.com/shorts/aMrwWVanZOw) | image à 0:00 importée |

L'identifiant du Short 35 commence par un L minuscule (`lOKRugjtazk`) : il était noté `IOKRugjtazk` (i majuscule), corrigé dans ce fichier.

## Vidéo 20 (téléphones) : miniature Boulanger (12 novembre 2026, 17 h 30)

À la demande de Marc, miniature personnalisée choisie parmi les essais de `20-telephone-2899-dollars/miniature-essai/` : **B1-photo-entiere.jpg** (photo de magasin Boulanger fournie par Marc, d'apparence générée par IA, avec le titre « TOP 3 DES TÉLÉPHONES LES PLUS CHERS 2026 »). Exception choisie par Marc à la règle « miniature = image à 0:00 ».

- **YouTube** : importée sur le Short [PI5URKbYLEY](https://youtube.com/shorts/PI5URKbYLEY), chaîne Histoires pas banales vérifiée, « Modifications enregistrées », toujours programmé le 12 nov. à 18 h 00. L'identifiant commence par un i majuscule (`PI5…`) : il était noté `Pt5URKbYLEY`, corrigé dans ce fichier.
- **Titre remonté** : à la demande de Marc, le titre de B1 a été replacé à la hauteur habituelle de l'ouverture (haut du « TOP 3 » à 993 px contre 992 px sur l'image à 0:00) ; ancienne version gardée dans `miniature-essai/B1-photo-entiere-titre-bas.jpg`. Le B1 corrigé a été réimporté sur YouTube (« Modifications enregistrées », 17 h 35).
- **TikTok, supprimé et remis** (« supprime et remet », Marc) : le post programmé ne pouvant pas être modifié, nouveau post importé vers 17 h 33 sur Histoires pas banales : `version-validee/final.mp4` (SHA-256 9205d6e8… recalculé dans la page, identique à `validation-utilisateur.json`), légende = `version-validee/legende.txt` comparée au texte du champ, **couverture = B1 importée** (« Importer une couverture »), importations haute qualité actives, label IA désactivé, programmé le **12 nov. à 18:00**. La vérification de contenu simple tournait encore à 17 h 42 ; sur décision de Marc (« Programmer 18 h sans attendre »), elle a été désactivée pour programmer à temps (la fenêtre de confirmation proposait « Publier maintenant », écartée). Ancien post (couverture première image) supprimé ensuite, jamais publié. Contrôle dans Publications : un seul post téléphones, 12 nov. 18:00 (GMT+1), couverture Boulanger.

## Programmation du 17 novembre 2026 (faite le 12 novembre vers 18 h 45)

Vidéo 42 (top 10 des plus beaux ballons de foot), validée par Marc le 12 novembre (« Valider la vidéo »), puis « Oui, programme-la ». Créneau : premier libre après le 16 novembre, pris par Claude. Comptes vérifiés avant import : TikTok Studio sur Histoires pas banales (liste Publications et aperçu), YouTube Studio sur la chaîne Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Mar 17 nov | 12 h 00 | 42 | « Notre top 10 des plus beaux ballons de foot… », légende de `legende.txt` | [Top 10 des plus beaux ballons de foot](https://youtube.com/shorts/2ws-ZQ2yQQo) |

- SHA-256 recalculé dans la page avant chaque import, identique à `version-validee/final.mp4` (4b976c54…). Durée 83,9 s, 1080 × 1920.
- YouTube : description = `version-validee/publication.txt` vérifiée dans le champ ; miniature = image à 0:00 importée (`_montage/upload/miniature-0s.jpg`), acceptée sans demande de validation ; pas pour enfants, sans limite d'âge ; « Utilisation de l'IA » : Non ; « Vérifications terminées. Aucun problème détecté » (droits compris) ; relu dans l'onglet Shorts : programmé le 17 nov. 2026, un seul Short.
- TikTok : légende = `version-validee/legende.txt` comparée au texte du champ ; importations haute qualité actives ; label IA désactivé (vraies séquences et photos, voix du compte qui n'imite personne) ; pas de lieu ; couverture = première image. Vérification de contenu simple : « Une erreur est survenue » après 15 minutes, relancée par Claude (« Réessayer »), puis « Aucun problème constaté » avant de programmer. Contrôle dans Publications : 17 nov. 12:00 (GMT+1) Paris, 01:23, un seul post.
- **Droits d'auteur : risque réel.** Extraits FIFA et UEFA (licence YouTube standard), cités dans la légende. La vérification YouTube n'a rien relevé à l'import ; relire les revendications avant le 17 novembre.
- Prononciations à contrôler à l'écoute si un commentaire les relève : Djabulani, Al Rila, Aztéka, Tim-gaïst.

## Vidéo 39 le 17 novembre 2026 à 18 h 00 (faite le 12 novembre vers 19 h)

Vidéo 39 (l'entraîneur boycotté dans tout le pays, Hong Myung-bo), validée par Marc le 12 novembre (« oui c bon g vu »), risque Content ID accepté par Marc le même jour. Créneau : 17 nov. 12 h 00 visé d'abord, mais la 42 (ballons) y a été programmée en parallèle par une autre session ; la 39 est passée à **18 h 00**, l'autre créneau habituel. Comptes vérifiés avant import : TikTok Studio sur Histoires pas banales (liste Publications et aperçu), YouTube Studio sur la chaîne Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Mar 17 nov | 18 h 00 | 39 | « Juin 2026 : la Corée du Sud sort au 1er tour du Mondial… », légende de `legende.txt` | [L'entraîneur boycotté dans tout le pays : Hong Myung-bo, héros de 2002](https://youtube.com/shorts/mkGCg2jpsyg) |

- SHA-256 recalculé dans la page avant chaque import, identique à `version-validee/final.mp4` (ac3fd633…). Durée 68,5 s, 1080 × 1920.
- TikTok : légende = `version-validee/legende.txt` comparée au texte du champ ; importations haute qualité actives ; label IA désactivé (vraies séquences et photos, voix du compte qui n'imite personne) ; couverture = première image. Vérification de contenu simple : « Une erreur est survenue » après 15 minutes, relancée (« Réessayer »), puis « Aucun problème constaté » avant de programmer. Contrôle dans Publications : 17 nov. 18:00 (GMT+1) Paris, 01:08, un seul post. La bannière « Une vidéo que tu étais en train d'éditer n'a pas été enregistrée » présente à l'ouverture n'a pas été touchée.
- YouTube : description = `version-validee/publication.txt` vérifiée dans le champ ; miniature = image à 0:00 importée (`_montage/upload/miniature-0s.jpg`), acceptée ; pas pour enfants, sans limite d'âge ; contenu modifié ou synthétique : Non ; « Vérifications terminées. Aucun problème détecté. » Programmé d'abord à 12:00, passé à 18:00 dans Détails > Visibilité, enregistré et relu après rechargement.
- **Droits d'auteur : risque accepté par Marc.** Extraits FIFA, KBS WORLD, Arirang et Yonhap News TV (licence YouTube standard), cités dans la légende et `CREDITS.md`. Relire les revendications YouTube avant le 17 novembre.
- Faits : voir `39-l-entraineur-boycotte-dans-tout-le-pays/controle-livraison.json`. Titre « boycotté dans tout le pays » choisi par Marc (panneaux documentés dans quelques commerces de plusieurs villes) ; Hong n'est accusé d'aucune infraction.


## 14 novembre 2026 - TOP 5 des buts (44), V8

Publication YouTube publique confirmée : https://www.youtube.com/shorts/F0R8Z9C-Zd4 . Export approuvé, miniature séparée importée et vérifiée dans Studio, description complète de version-validee/publication.txt relue. Contrôles droits et règlement terminés : aucun problème détecté. Preuve : 44-top-5-buts-les-plus-degueulasses/publication-2026-11-14/youtube-publie.jpg. TikTok non importé : session Chrome sur moovini.app ; connexion histoirespasbanales demandée à Marc.


### Correction du TOP 5 (44) - 14 novembre 2026

Marc voulait la suite du planning : **18 novembre 2026 a 12 h, Europe/Paris (GMT+1)** sur les deux comptes. YouTube F0R8Z9C-Zd4 : meme video remise en prive et programmee, date/heure relues apres rechargement. TikTok 7707810387852397846 : programmation confirmee dans Publications a 18 nov., 12:00 (GMT+1) Paris, miniature TOP 5 et legende complete. Verification TikTok : aucun probleme constate. Preuves dans 44-top-5-buts-les-plus-degueulasses/publication-2026-11-14/. La publication YouTube immediate precedente etait une erreur ; 296 vues avaient ete observees avant correction. Aucune suppression ni reimport YouTube. Brouillon Pogba preexistant sauvegarde sans publication.

### Horaire final TOP 5 (44) — 18 novembre 2026, 19 h Paris
À la demande de Marc, YouTube et TikTok sont programmés au 18 novembre à 19:00 (GMT+1). YouTube : même vidéo F0R8Z9C-Zd4, horaire enregistré et relu. TikTok : ancienne programmation de midi supprimée après confirmation explicite ; remplacement 7707824727716318486 confirmé dans Publications. Export V8, miniature et légende conservés. Contrôle TikTok : aucun problème constaté. Preuves : publication-2026-11-14/youtube-programme-19h.jpg et tiktok-programme-19h.jpg dans le dossier 44.


## Vidéo 45 le 19 novembre 2026 à 19 h 00 (faite le 14 novembre vers 14 h)

Vidéo 45 (origine du Black Friday, « le cauchemar des flics »), variante `videos/`, validée par Marc le 14 novembre (« Manque la miniature et on est bon »), miniature validée (« Oui, titre remonté »), puis « programme-la sur TikTok et YouTube ». **Nouvelle règle de Marc, 14 novembre : une vidéo par jour à 19 h 00**, premier jour libre (le 18 est pris par la 44). Comptes vérifiés : TikTok Studio sur Histoires pas banales (liste Publications, aperçu du profil), YouTube Studio sur la chaîne Histoires pas banales (UCoCQQfS6h1lhqHdB21PpAuw).

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Jeu 19 nov | 19 h 00 | 45 | « Le Black Friday, c'était d'abord le cauchemar des flics de Philadelphie… », légende de `videos/legende.txt` | [Black Friday : à l'origine, c'était le cauchemar des flics](https://youtube.com/shorts/uVJE7weMW9I) |

- SHA-256 recalculé dans la page avant chaque import, identique à `videos/final.mp4` (1d84a076…). Durée 67,1 s, 1080 × 1920.
- **Légende nettoyée** avec l'accord de Marc : l'ancienne `legende.txt` contenait des notes internes (« non destinées à la publication », risque de revendication, noms de fichiers) ; gardée dans `legende-interne-avant-nettoyage.txt`. Nouvelle légende = `videos/legende.txt` = `publication.txt`, comparée au texte du champ des deux côtés.
- Couverture / miniature = fichier séparé `out/miniatures-v4/45.jpg` (style magazine, photo Ed Betz / AP via HISTORY, titre remonté au niveau du gabarit Pogba), importée sur TikTok et YouTube.
- YouTube : pas pour enfants, sans limite d'âge, contenu modifié ou synthétique : Non ; « Vérifications terminées. Aucun problème détecté. » ; programmé public le 19 nov. 2026 à 19:00.
- TikTok : importations haute qualité actives ; label IA désactivé (vraies archives et séquences, voix du compte qui n'imite personne) ; contenu de marque désactivé ; pas de lieu. Vérification de contenu simple : « Une erreur est survenue » après ~15 minutes, relancée (« Réessayer »), puis « Aucun problème constaté » avant de programmer. Le toast affiché après « Programmer » dit « Vidéo publiée » : c'est le libellé générique, le post est bien programmé. Contrôle dans Publications après rechargement : 19 nov. 19:00 (GMT+1) Paris, 01:07, couverture Black Friday, un seul post (10 publications au total).
- Contrôle YouTube après rechargement de l'onglet Shorts : « Programmée », 19 nov. 2026, un seul Short, miniature importée.
- **Droits d'auteur : risque réel.** Extraits Reuters, British Pathé, Kinolibrary, Jim Downs, Superwalk Tours et photo AP, sans licence ; crédités dans la légende.

## Remplacement « ouverture directe » du 14 novembre 2026 (vers 15 h - 16 h)

Règle de Marc rappelée le 14 novembre : aucune lecture du titre, aucun carton ni bandeau (y compris fun facts), logo HPB en haut à droite. Les vidéos programmées 31, 33, 35, 36, 39, 42 et 45 lisaient leur titre (et 31 à 42 avaient carton + bandeau « ?! »). Versions refaites dans `revisions-intro-14nov-2026/<n>/version-validee/` (coupe jusqu'à la phrase de contexte, montage repris depuis `_montage/base.mp4`, sous-titres seuls, logo HPB), validées par Marc (« c parfait comme ça, le hook tient dans la miniature »). Couvertures : `miniatures-v4/<n>.jpg` (zones contrôlées). Légendes : crédit des photos de couverture ajouté pour 31, 35, 36, 39.

**Calendrier = horaires YouTube** (« prends le planning youtube et applique sur tiktok ») :

| Jour | Heure | N° | TikTok | YouTube |
|---|---|---|---|---|
| Ven 14 nov | 18 h 00 TikTok / 19 h 00 YouTube | 28 OM | reposté (v fluidité + couverture v5) | H_g4bENItb8 (horaire mis à 19 h par l'autre session) |
| Sam 15 nov | 12 h 00 | 33 | nouvelle version | NvFoUUSn_7o |
| Sam 15 nov | 18 h 00 | 31 | **v2 vraies séquences** (remplacée vers 16 h) | AfsT2pbrRyc (v2, Silent Descent) |
| Dim 16 nov | 12 h 00 | 35 | nouvelle version | tVLyVLNSuZs |
| Dim 16 nov | 18 h 00 | 36 | nouvelle version | _SJmJPZseRg (nouvelle version, « Aucun problème détecté ») |
| Lun 17 nov | 12 h 00 | 42 | nouvelle version | aw1lSTLGgEI |
| Lun 17 nov | 18 h 00 | 39 | nouvelle version | OwGjP9ItfwI |
| Mar 18 nov | 19 h 00 | 44 | inchangé | F0R8Z9C-Zd4 |
| Jeu 19 nov | 19 h 00 | 45 | nouvelle version | Q-o3ftYi54E |

- TikTok : anciens posts supprimés (plusieurs suppressions/reprogrammations dans la journée, signal négatif possible pour le compte) ; chaque nouveau post contrôlé avant « Programmer » : SHA-256 recalculé dans la page, légende identique au fichier, date/heure, HD actif, label IA et contenu de marque désactivés, vérification de contenu « Aucun problème constaté ». Liste Publications relue : un seul post par vidéo.
- YouTube : anciens Shorts 33, 35, 39, 42 supprimés par Marc ; ancien 45 (uVJE7weMW9I) et ancienne Pogba (Z01EJ1GyvSg) supprimés définitivement à sa demande.
- **Pogba YouTube : revendication audio** « Heart-Light 1617 » (@CassinoMcs, MusicPro) sur 0:02-1:06, vidéo bloquée dans le monde entier. Cause : la musique Mixkit « Greed - Arulo ». Version YouTube refaite avec « Silent Descent - Eugenio Mininni / Mixkit » (`revisions-intro-14nov-2026/31/musique-silent-descent/`, dcc0d675…), validée par Marc : vérifications « Aucun problème détecté ». **Risque** : 28, 36, 39 utilisent aussi Greed et peuvent être revendiquées plus tard.
- 36 YouTube : nouvelle version importée (_SJmJPZseRg, 16 nov. 18:00, aucun problème détecté) ; ancienne aMrwWVanZOw supprimée définitivement (14 nov. vers 16 h 10).

### Pogba (31) : v2 avec vraies séquences, 14 novembre vers 16 h
Erreur corrigée : la première révision partait de `version-validee/` (v1, illustrations Pexels) alors que Marc avait accepté la v2 aux vraies séquences (`revisions-15nov-2026/31-v2`, copiée à la racine du dossier 31). Nouvelle version : v2 coupée à 5,543 s (« Mars 2022 »), sans bandeau, logo HPB, musique Silent Descent (Greed revendiquée), `revisions-intro-14nov-2026/31-v2/version-validee/final.mp4` (fdcc1864…), validée (« Oui, remplace »). TikTok : ancien post supprimé, v2 programmée le 15 nov. 18:00 (contrôlée, un seul post). YouTube : AfsT2pbrRyc programmé 15 nov. 18:00, « Aucun problème détecté » ; HBqxBWtg7wU supprimé définitivement.
À noter : `revisions-15nov-2026/33` et `42-.../final.mp4` sont des v2 non validées ; les versions programmées restent les v1 révisées.


## Vidéo 46 — larmes de verre — 20 novembre 2026 à 19 h Paris

Programmée le 14 novembre à la demande de Marc, au prochain jour libre, selon la règle une vidéo par jour à 19 h.

- TikTok : https://www.tiktok.com/@histoirespasbanales/video/7708048732075396374 ; date et heure relues dans Publications après rechargement. HD actif, contrôle aucun problème constaté.
- YouTube : https://youtube.com/shorts/F8XooM5e7e4 ; confirmation « Vidéo programmée », 20 novembre 2026 à 19:00, GMT+1 local. Droits et règlement : aucun problème détecté.
- Vidéo 65,2 s, SHA-256 64333ccc4ceea8785744842baa9e3abb772c277f09995f66b3a57d028a9320d3. Miniature d’origine avec réglages photo validée, importée et examinée sur les deux plateformes.
- Légende nettoyée des notes internes, sources et crédits conservés ; texte contrôlé sur les deux plateformes. Ancien texte dans legende-interne-avant-publication.txt.
- Copie dans 46-larme-de-verre/version-validee/ ; preuves et détails dans programmation.json et publication-2026-11-14/.


## Vidéo 43 — top 3 des motos de série — 21 novembre 2026 à 19 h Paris

Programmée le 14 novembre vers 22 h 40 à la demande de Marc (« Oui, programme-le »), premier jour libre selon la règle une vidéo par jour à 19 h.

| Jour | Heure (Paris) | N° | TikTok | YouTube Shorts |
|---|---|---|---|---|
| Sam 21 nov | 19 h 00 | 43 | [7708154418910350614](https://www.tiktok.com/@histoirespasbanales/video/7708154418910350614) | [Hh3XS5phpWM](https://youtube.com/shorts/Hh3XS5phpWM) |

- Version validée `revisions-intro-14nov-2026/43/version-validee/` (copie dans `43-top-3-motos-plus-rapides/version-validee/`) : ouverture directe, faits BMW corrigés, compteurs bloqués à 299 km/h. 66,2 s, SHA-256 2f3be419… recalculé dans la page avant chaque import.
- Couverture = `miniatures-v4/43.jpg` (style course, fond Ducati 4K), importée des deux côtés ; aperçu profil TikTok 4:3 contrôlé (titre entier et logo).
- TikTok : compte Histoires pas banales vérifié, HD actif, label IA et contenu de marque désactivés (vraies séquences, voix du compte), vérification « Aucun problème constaté » ; Publications rechargée : un seul post, 21 nov. 19:00.
- YouTube : pas pour enfants, sans limite d'âge, contenu modifié ou synthétique : Non, « Aucun problème détecté » ; détails rechargés : programmée 21 nov. 2026 19:00.
- **À revérifier le jour du post (R-09)** : prix 37 000 €, 43 990 €, 58 000 €. Commentaires probables : 400 km/h au compteur (Kawasaki annonce 380), Lightning LS-218 écartée, Ducati 318 km/h contre BMW 314.
- **Droits** : extraits BMW, Ducati, Kawasaki, TMF, Den ProHD et Sim_Razz sans licence, crédités en légende ; musique Mixkit « Sports Highlights ».
- Preuves : `43-top-3-motos-plus-rapides/publication-2026-11-14/`.
- **Miniature passée en jaune (14 nov., vers 22 h 50)** à la demande de Marc (« Jaune HPB ») : plaques jaune HPB #FFE447 et texte marine au lieu du rouge, pour ressortir sur la Ducati rouge (style `course_jaune`, exception pour ce dossier). YouTube SA6VJLO76ds : miniature jaune importée, relue après rechargement. **TikTok : la couverture programmée reste la rouge** (TikTok interdit de modifier un post programmé). **À faire le 21 nov. juste après 19 h** : Publications > crayon > Modifier la couverture > importer `43-top-3-motos-plus-rapides/version-validee/miniature.jpg`. Ne pas supprimer ni reprogrammer le post.
- **Refait le 14 nov. vers 23 h - 23 h 50** à la demande de Marc (« supprime et refait le post tiktok », puis nouvelle fin validée) : fin « Et toi, tu prends laquelle ? » au lieu de « Réponds oui ou non » (voix régénérée, 67,7 s, SHA-256 169e0d56…), légende alignée, couverture jaune. TikTok : post 7708144063295327510 supprimé, nouveau 7708154418910350614 (vérification « Aucun problème constaté », Publications : un seul post, 21 nov. 19:00, 01:07). YouTube : nouveau Short Hh3XS5phpWM programmé 21 nov. 19:00 (« Aucun problème détecté »), ancien SA6VJLO76ds passé en privé puis **supprimé définitivement** à la demande de Marc (« le supprimer », 14 nov. vers 23 h 55) ; onglet Shorts relu : un seul Short motos. La ligne « couverture rouge à changer après publication » ci-dessus n'est plus à faire.

## Vidéo 47 — Dortmund, attentat pour la Bourse — 22 novembre 2026 à 19 h Paris

Programmée le 14 novembre vers 23 h 30 à la demande de Marc (« programme la vidéo Dortmund », valant validation de `final.mp4`, SHA-256 2307079b…), premier jour libre selon la règle une vidéo par jour à 19 h. Miniature refaite et validée le même soir (« Oui, validée ») : bus du BVB la nuit de l'attentat (Al Jazeera, 32 s), style magazine, `miniatures-v4/47.jpg`, zones contrôlées.

| Date | Heure | Dossier | TikTok | YouTube |
|---|---|---|---|---|
| Dim 22 nov | 19 h 00 | 47 | [7708157788672871702](https://www.tiktok.com/@histoirespasbanales/video/7708157788672871702) | [DE4uPWVHM5I](https://youtube.com/shorts/DE4uPWVHM5I) |

- Fichier envoyé réassemblé dans la page, SHA-256 contrôlé identique à `final.mp4` sur les deux plateformes.
- TikTok : compte Histoires pas banales vérifié (Publications, aperçu) ; légende = `legende.txt` comparée au champ ; couverture importée, aperçu profil 4:3 avec titre et logo entiers ; HD actif ; label IA et contenu de marque désactivés (vraies archives, voix du compte qui n'imite personne) ; pas de lieu ; vérification « Aucun problème constaté » ; Publications rechargée : un seul post Dortmund, 22 nov. 19:00 (GMT+1).
- YouTube : chaîne Histoires pas banales ; titre « Dortmund : un attentat contre le bus des joueurs pour gagner en Bourse », description = `publication.txt` ; miniature importée ; pas pour enfants ; contenu modifié ou synthétique : Non ; « Vérifications terminées. Aucun problème détecté » ; confirmation « Vidéo programmée… 22 novembre 2026 à 19:00 » ; onglet Shorts relu : un seul Short Dortmund.
- Droits : extraits DW, Al Jazeera, AFP et euronews sans licence, crédités dans la légende ; musique Mixkit.

## Vidéo 48 — évasion de Rédoine Faïd en hélicoptère — 23 novembre 2026 à 19 h Paris

Programmée le 15 novembre vers 13 h 30 à la demande de Marc (« programme la vidéo 48 sur TikTok et YouTube »), premier jour libre selon la règle une vidéo par jour à 19 h.

| Date | Heure | Dossier | TikTok | YouTube |
|---|---|---|---|---|
| Lun 23 nov | 19 h 00 | 48 | [7708369690422201622](https://www.tiktok.com/@histoirespasbanales/video/7708369690422201622) | [XlTuViKtLdE](https://youtube.com/shorts/XlTuViKtLdE) |

- Vidéo 64,7 s, réassemblée dans la page, SHA-256 75e73faf… identique à `version-validee/final.mp4` sur les deux plateformes.
- Couverture = `miniatures-v4/48.jpg` (variante A choisie par Marc : vidéosurveillance de la cour de Réau, avis de recherche, « FILMÉE PAR UN DÉTENU »), importée des deux côtés ; aperçu profil TikTok 4:3 : titre entier et logo visibles.
- Légende : paragraphe de notes internes retiré avant publication (ancien texte dans `legende-interne-avant-publication.txt`), sources et crédits conservés ; texte comparé au champ sur les deux plateformes.
- TikTok : compte Histoires pas banales vérifié ; HD actif ; label IA et contenu de marque désactivés (vraies archives, voix du compte qui n'imite personne) ; pas de lieu ; vérification « Aucun problème constaté » ; Publications : un seul post évasion, 23 nov. 19:00 (GMT+1).
- YouTube : chaîne Histoires pas banales ; titre « Évasion en hélico : un détenu filme Faïd quitter la prison » ; pas pour enfants ; IA : Non ; « Vérifications terminées. Aucun problème détecté » ; confirmation « Vidéo programmée… 23 novembre 2026 à 19:00 » ; onglet Shorts : un seul Short évasion.
- Droits : extraits TF1 INFO, BFMTV et Daily Mail sans licence, crédités dans la légende ; musique Mixkit.

## Vidéo 49 — top 3 des records de vitesse les plus fous sans moteur — 24 novembre 2026 à 19 h Paris

Programmée le 15 novembre vers 15 h à la demande de Marc (« Oui, programme-la »), premier jour libre selon la règle une vidéo par jour à 19 h.

| Date | Heure | Dossier | TikTok | YouTube |
|---|---|---|---|---|
| Mar 24 nov | 19 h 00 | 49 | [7708384528527641878](https://www.tiktok.com/@histoirespasbanales/video/7708384528527641878) | [lmrviF2XCXc](https://youtube.com/shorts/lmrviF2XCXc) |

- Vidéo 72,6 s, réassemblée dans la page, SHA-256 df31e153… identique à `version-validee/final.mp4` sur les deux plateformes.
- Couverture = `miniatures-v4/49.jpg` (style course, Baumgartner au bord de la capsule Stratos), importée des deux côtés ; aperçu profil TikTok 4:3 : titre entier et logo visibles.
- Légende : hashtags ramenés à 5 avec #histoirevraie avant publication (révision notée dans `validation-utilisateur.json`) ; texte comparé au champ sur les deux plateformes.
- TikTok : compte Histoires pas banales vérifié (aperçu profil) ; HD actif ; label IA et contenu de marque désactivés (vraies séquences, voix du compte qui n'imite personne) ; pas de lieu ; vérification « Aucun problème constaté » ; Publications : un seul post, 24 nov. 19:00 (GMT+1).
- YouTube : chaîne Histoires pas banales ; titre « 1 357 km/h sans moteur : les 3 records de vitesse les plus fous » ; pas pour enfants ; pas de promotion rémunérée ; IA : Non ; « Vérifications terminées. Aucun problème détecté » ; confirmation « Vidéo programmée… 24 novembre 2026 à 19:00 » ; onglet Shorts : un seul Short 49.
- Droits : extraits Red Bull, Wall Street Journal, Atomic Ski Fans, Jan Farrell, drunkskier02, archive 1997 et Cargospotter sans licence, crédités dans la légende ; musique Mixkit.

## Vidéo longue 01 — top 3 des voitures les plus rapides — importée en privé le 15 novembre 2026

Importée le 15 novembre vers 16 h 45 à la demande de Marc (« programme la vidéo longue sur YouTube », puis « maintenant mais en privé », « garde la en privé pour le moment que je vérifie »). **Non programmée, non publique** : en attente de la vérification de Marc. YouTube seulement (format 16:9 de 8 min 03).

| Date | Visibilité | Dossier | YouTube |
|---|---|---|---|
| Dim 15 nov (import) | Privée | long-01-voitures-vitesse | [UmTfE2OBAnQ](https://youtu.be/UmTfE2OBAnQ) · [Studio](https://studio.youtube.com/video/UmTfE2OBAnQ/edit) |

- Fichier : `long-01-voitures-vitesse/essai-long-v5.mp4` (V5, phrase d'ouverture corrigée), réassemblé dans la page, SHA-256 a54488db… identique. Marc a choisi de programmer la V5 sans l'avoir écoutée (« Programmer la V5 »).
- Titre « comme le short » : « Trois voitures de série qui ont dépassé les 450 km/h » (titre du Short kdbAWhNzqpI) ; description = `description-youtube-v5.txt`, comparée au champ (identique).
- Miniature personnalisée = `miniature-youtube-v4.jpg` (SSC Tuatara de profil, validée par Marc), importée et affichée dans la liste Contenu.
- Pas pour enfants ; pas de limite d'âge ; pas de promotion rémunérée ; IA : Non (vraies archives, voix du compte qui n'imite personne).
- Vérifications droits d'auteur et règlement : encore en cours à l'enregistrement (environ 10 min annoncées). À relire avant de la passer en public : les archives Bugatti, SSC et BYD sont sous licence YouTube standard, risque de revendication Content ID.
- Pour publier : Studio > Contenu > Vidéos > Visibilité, choisir Publique ou Programmer.
- **Test A/B titre et miniature** (Marc, 15 novembre : « met en place des A/B tests qu'on voit ce qui marche le mieux »), configuré et enregistré le 15 novembre vers 17 h. Statut « Inéligible » tant que la vidéo est privée (« Votre vidéo n'est pas publique ») : il démarre à la publication, dure jusqu'à deux semaines, puis YouTube applique la version gagnante à la durée de visionnage. Ne pas recliquer sur « Tests A/B » dans Studio : cela propose de supprimer le test en cours.

| Version | Titre | Miniature |
|---|---|---|
| A | Trois voitures de série qui ont dépassé les 450 km/h | `miniature-youtube-v4.jpg` (SSC Tuatara de profil) |
| B | TOP 3 des voitures les plus rapides du monde en 2026 | `miniature-youtube-variante-bugatti.jpg` |
| C | 503 km/h : la voiture de série la plus rapide du monde et ses 2 rivales | `miniature-youtube-variante-yangwang.jpg` |

  Titre C : 503,17 km/h est la pointe homologuée par Guinness (« highest speed achieved by a production car in a single direction run »), sources dans la description. À noter dans `docs/decisions.md` quand le résultat tombe.
- **Publiée le 15 novembre 2026 vers 17 h 15** à la demande de Marc (« publie et lance le test A/B »). Avant publication : page Revendications « Cette vidéo ne fait l'objet d'aucune revendication ». Visibilité Publique enregistrée (« Modifications enregistrées ») ; après rechargement, test A/B « En cours d'exécution » avec les trois titres et les trois miniatures. Rapport : Studio > Détails > « Afficher le rapport du test » (résultat sous deux semaines au plus).
- **Optimisations du 15 novembre (vers 17 h 30)**, choisies par Marc après une revue des menus de Studio :
  - Langue de la vidéo, du titre et de la description : Français (France). Elle n'était pas définie, ce qui grisait « Sous-titres ».
  - Sous-titres : `sous-titres-v5.srt` (calé sur la V5, « À cette vitesse… ») importé avec minutage et publié (traitement de quelques heures annoncé par YouTube).
  - Catégorie : Auto/Moto (au lieu de People et blogs). Tags : SSC Tuatara, Bugatti Chiron Super Sport 300+, Yangwang U9 Xtreme, voiture la plus rapide du monde, record de vitesse, hypercar.
  - Écran de fin de 7:42 à 8:02 : « Contenu adapté au spectateur » en haut à gauche, S'abonner à droite sous le logo HPB, sous-titres dégagés.
  - Fiche à 7:38 vers le Short voitures (kdbAWhNzqpI), message « Le top en 1 minute », accroche « Version Short ».
  - Short kdbAWhNzqpI : « Vidéo similaire » = la vidéo longue UmTfE2OBAnQ (lien présent dans la page publique du Short).
- **Commentaire épinglé sous le Short kdbAWhNzqpI** (15 novembre, à la demande de Marc, texte « Version longue sobre » choisi par lui) : « La version longue (8 min), avec les coulisses des 3 records : https://youtu.be/UmTfE2OBAnQ », publié par @histoirespasbanales et affiché « Épinglé » après rechargement. Statistiques de la vidéo longue une heure après publication : 0 vue, 0 impression ; test A/B « en cours », sans donnée, environ 14 jours restants.
- **15 novembre, 22 h 06 : on la laisse.** Marc pensait que la vidéo avait raté et demandait de la reposter. Studio montrait 640 impressions, 9 vues (suggestions), un taux de clics de 0,8 % et une durée moyenne de 4:23 (54 %). Pas de repost : le test A/B serait perdu et le fichier passerait pour un doublon. À revoir vers le 18 novembre : si le taux de clics reste sous 2 % pour les trois versions, changer titre et miniature sur la même vidéo.
- **Test A/B relancé** (Marc : « refait le test AB »). Le premier test avait disparu de la page de la vidéo, qui n'affichait plus que la version A ; la cause n'est pas connue. Il a été recréé à l'identique (mêmes trois titres, mêmes miniatures v4, Bugatti et Yangwang), puis la vidéo a été enregistrée. Après rechargement, titres et miniature sont « En cours d'exécution… ». Le délai d'environ deux semaines repart de zéro.
