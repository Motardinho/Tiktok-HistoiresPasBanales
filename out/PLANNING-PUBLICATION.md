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
- YouTube Shorts, chaîne Histoires pas banales : programmée, https://youtube.com/shorts/Pt5URKbYLEY (titre « Les 3 téléphones les plus chers en vente en France #shorts », légende de `legende.txt`, utilisation de l'IA « Non » selon les quatre cas listés par YouTube).
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
| Sam 14 nov | 18 h 00 | 28 | « L'OM a acheté un match en 1993… », légende de `legende.txt` | [L'OM a acheté un match en 1993 : l'affaire VA-OM](https://youtube.com/shorts/F2gouR167vo) |

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

**À faire à partir du 12 novembre 2026 vers 18 h (fin de la limite de 24 h des miniatures YouTube, signalée par Marc)** : dans YouTube Studio, remplacer la miniature automatique du Short 31 (https://youtube.com/shorts/Z01EJ1GyvSg) par `31-pogba-braque-pour-13-millions/_montage/upload/miniature-0s.jpg`, avant sa publication du 15 novembre à 18 h 00. Même chose pour la 30 si elle est programmée d'ici là.
