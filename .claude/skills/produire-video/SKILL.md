---
name: produire-video
description: Lance, reprend ou dépanne la production d'une vidéo Histoires pas banales, histoire ou top (voix ElevenLabs, images OpenAI, animation Veo/Kling, montage ffmpeg). À utiliser pour générer une vidéo, refaire une étape, régler le rendu ou diagnostiquer une erreur du pipeline.
---

# Produire une vidéo

## Vérifier la tiktokabilité avant production

**Consigne de Marc, 14 novembre 2026 : bien vérifier que les sujets sont « tiktokables ».** Avant la voix, les téléchargements de production et le montage, appliquer le [contrôle de tiktokabilité](references-hpb.md#tiktokabilité-du-sujet). Un sujet intéressant ne suffit pas : vérifier son accroche, son potentiel visuel réel et sa capacité à tenir un récit court. Consigner le verdict et les limites dans la préparation du dossier ; signaler un sujet mal adapté avant de le produire.

## Ouverture directe — correction prioritaire du 14 novembre 2026

**Dernière correction de Marc, 14 novembre 2026 : aucun bandeau ni encart dans les vidéos, y compris pour les fun facts.** Les anecdotes restent dans la narration et les sous-titres ordinaires, sans mention « FUN FACT » ni surcouche dédiée. Cette règle remplace l’autorisation précédente des encarts centrés sous le logo avec 60 px d’espace. Garder le logo HPB validé et les sous-titres. Voir [la règle courante](references-hpb.md#bandeaux-de-contexte-interdits). Lors d’une révision, retirer aussi les anciens calques de fun fact.

Commencer immédiatement par une action, un détail ou un enjeu du récit : aucune lecture du titre, aucun carton ni temps réservé au titre. La miniature reste une couverture séparée. La première phrase doit être compréhensible sans avoir vu la miniature ; afficher les sous-titres dès les premiers mots. Cette règle remplace les anciennes annonces de titre pour les histoires et les tops. Sur une vidéo existante, couper à une frontière de phrase cohérente, préserver la version validée et contrôler raccord, transcription et durée finale supérieure à 60 s. Voir [les règles actualisées](references-hpb.md#ouverture-directe).

## Miniatures — direction validée le 13 novembre 2026

Logo approuvé : réutiliser sans modification `identite/histoires-pas-banales/logos/hpb-reference-propre-v1.svg` (jaune, lettres transparentes, sans ombre), selon [references-miniatures.md](references-miniatures.md).

Pour créer ou modifier une miniature, lire [les modèles de miniatures](references-miniatures.md). Marc a choisi les cinq modèles de la planche conservée dans `identite/histoires-pas-banales/modeles-miniatures/`. Choisir le style selon le sujet. Sa dernière correction impose **la bulle jaune HPB en haut à droite, sans bandeau**, sur les miniatures et dans les vidéos, de la première à la dernière image.

Lire les [règles de production du compte](references-hpb.md) avant tout rendu : elles contiennent les exigences impératives de durée, de transcription numérique, de hook, d’habillage et de chute. Refuser une livraison dont le MP4 final ne dépasse pas 60 secondes.

Les corrections les plus récentes de Marc priment sur les anciens scripts et exemples du lot. Ne pas recopier un ancien montage sans le confronter aux règles actuelles.

**Demander à Marc avant de commencer : post de photos ou post de vidéos ?** (Marc, 12 novembre 2026). Poser la question pour chaque nouveau dossier, en même temps que la validation du sujet ou, si le sujet est déjà imposé, avant tout téléchargement de plans. Ne pas trancher seul, même quand le sujet s'y prête (objets peu filmés comme les maillots du dossier 41). Indiquer en une ligne ce qui existe en vraies vidéos pour le sujet, puis attendre sa réponse. Noter le choix dans `histoire.json` (`type_post` : `photos` ou `videos`).

**De vraies vidéos, peu importe la source** (Marc, 12 novembre 2026 : « il faut de vraies vidéos, peu importe les sources. Note les sources en légende »). Pour un post de vidéos, chaque plan est une séquence réelle du sujet raconté : chaîne officielle, diffuseur, reprise YouTube, compte fan, TikTok, archive télé, tout est admis du moment que la séquence est la bonne et la plus nette trouvée. L'absence de source officielle ne justifie jamais une photo ou une illustration générique. Chaque source retenue va **en texte dans la légende du post** (`legende.txt` et `publication.txt`, et `CREDITS.md`) : chaîne ou compte, titre, date si connue, URL.

## Passage obligatoire avant livraison

Pour chaque vidéo révisée, renseigner dans son dossier un contrôle daté avec les passages et fichiers effectivement examinés. Ne pas marquer un contrôle visuel comme réussi sur la seule base du script ou d'un calcul de positions.

1. Vérifier accroche directe sans lecture du titre, classement, année réelle des données et fun fact sourcé avant la voix.
2. Contrôler à l’arrêt la première image à 0:00 selon les [règles d’accroche](references-hpb.md#hook-et-habillage), puis regarder les 5 premières secondes. Elles doivent montrer le plan spectaculaire, la phrase-hameçon prononcée avant 5,0 s et au moins deux plans différents, sans logo ni filigrane d'un tiers. Examiner chaque plan recadré au début, au milieu, à la fin et aux changements de plan : bon sujet, bonne action, sujet identifiable, aucun remplissage statique évitable.
3. Examiner le rendu à 360 pixels de large, avec puis sans son : sous-titres bas, accents, ponctuation et compteur lisibles sans collision ; absence de bandeaux et d’encarts de fun fact. Examiner aussi un aperçu simulé du lecteur TikTok.
4. Vérifier la fin : pas de paragraphe générique qui dilue la chute, invitation naturelle à réagir, puis signature ; aucune surcouche qui double la transcription.
5. Décoder le MP4, comparer durées audio/vidéo, confirmer plus de 60 secondes, puis régénérer et vérifier la comparaison issue du dernier export. **Liens cliquables à chaque livraison, systématiquement** (demande de Marc du 11 novembre 2026, pour lancer les vidéos facilement) : envoyer `final.mp4` et `comparaison.mp4` avec l'outil d'envoi de fichiers (carte cliquable dans la conversation), puis donner dans la réponse, pour la vidéo, la comparaison et la légende, un lien Markdown relatif (`[final.mp4](out/<dossier>/final.mp4)`) et un lien `file:///` absolu, espaces encodés en `%20` (`file:///C:/Projets/Tiktok%20-%20MrBallen/out/<dossier>/final.mp4`). Un chemin entre chevrons n'est pas cliquable : ne plus l'utiliser.

**Versions validées :** lorsqu'une vidéo est approuvée, conserver `final.mp4`, `comparaison.mp4`, le script et les légendes dans `version-validee/`, avec `validation-utilisateur.json` (date, fuseau, SHA-256). Mettre à jour l'index et le manifeste. Exclure ces vidéos de toute retouche globale ; ne les rouvrir que si Marc demande une nouvelle modification de cette vidéo. Le renderer du lot respecte ce verrou par défaut.

**Livraison systématique demandée par Marc : chaque vidéo et chaque révision sont livrées avec `final.mp4` ET `comparaison.mp4`, sans attendre qu’il le redemande.** Choisir et conserver la référence dans `histoire.json` avant la production. Référence à gauche, HPB à droite, départ simultané, deux pistes audio séparées et nommées, HPB par défaut. Figer l’image et compléter par du silence après la fin de la version la plus courte. Vérifier les deux fichiers et fournir leurs deux liens à la livraison. Une comparaison absente ou antérieure à la dernière révision signifie que la livraison est incomplète.

## Contrôles à appliquer avant chaque livraison

**Sous-titres dès les premiers mots**, ancrés en bas au-dessus de la légende TikTok. Aucun carton ni grand titre introductif ; garder le sujet et l’action lisibles.



- **Ouverture orale :** commencer directement par une action ou un enjeu compréhensible, sans lecture du titre. Vérifier la première phrase dans l’export ; aucune introduction réservée au titre, même pour un top.
- **Vidéo par défaut, sauf si Marc a choisi un post de photos :** préparer chaque plan en séquence vidéo réelle, de n'importe quelle source citée en légende. Une photo n’est acceptée qu’après une recherche de vidéo réellement infructueuse, avec justification précise dans le manifeste, ou à la demande explicite de Marc (ex. archive d’Hiroshima). Un zoom sur une photo ne satisfait pas ce contrôle. Ne pas conserver une photo simplement parce qu’elle est déjà montée.
- **Sous-titres :** même ancrage bas sur toute la vidéo, sans alternance haut/bas. Contrôler les collisions avec tous les autres éléments et l’interface TikTok.
- **Identité visuelle (correction du 14 novembre) :** asset validé `hpb-reference-propre-v1.svg`, bulle jaune en haut à droite, lettres HPB réellement transparentes, sans ombre et sans bandeau de série, de la première à la dernière image. Ne pas redessiner le logo. Ajuster les plans pour préserver les visages et l’action.
- **Sources :** texte prêt à copier dans la légende du post, sans bandeau de crédits ajouté au film.

## Rigueur visuelle avant montage

**Contrôle obligatoire des collisions et superpositions avant livraison.** Vérifier ensemble sous-titres, chiffres, logo et interface TikTok, à chaque apparition et transition. Aucun texte ne doit être recouvert par un autre élément ; retirer les mentions redondantes ou réserver des zones distinctes. Voir le [contrôle des superpositions](references-hpb.md#collisions-et-superpositions).

**Au moins un fun fact vérifié dans chaque vidéo, systématiquement.** Avant production, identifier le passage exact, sa source et le visuel qui l’illustre ; compléter le script s’il n’en contient pas. Appliquer les [règles de fun facts](references-hpb.md#fun-facts-intégrés-aux-vidéos).

**Consigne permanente de Marc : être rigoureux jusque dans les petits détails.** Examiner chaque visuel avant de l’intégrer : identité réelle du sujet, pays, époque, uniformes, insignes, drapeaux, matériel et cohérence avec la narration. Vérifier la provenance et la légende des archives ; un drapeau ou le lieu d’un défilé ne suffit pas à identifier les soldats. Écarter ou remplacer les images ambiguës. Ne pas ajouter de drapeau ni d’accessoire décoratif sans raison liée à la scène.

**Contrôler le plan sur toute sa durée après recadrage vertical.** Vérifier début, milieu, fin et mouvements intermédiaires : le sujet ou détail annoncé doit rester net et identifiable. Écarter les plans dominés par une main, un intervenant tronqué ou un avant-plan qui masque le sujet ; une voiture floue derrière un interviewé ne constitue pas un bon plan de voiture. Les gros plans restent pertinents s’ils montrent volontairement un détail raconté. Remplacer ou recadrer les passages faibles avant livraison, puis regarder le résultat avec l’habillage.

**Le visuel doit être raccord avec l’action décrite au même moment.** Lorsque Marc demande de « mettre en avant » un mouvement, choisir d’abord une photo ou une vidéo qui le montre réellement : un faucon en piqué quand la narration dit qu’il plonge, un animal en pleine course pour un sprint. Privilégier une vidéo démonstrative lorsqu’elle est disponible. Un texte superposé, un zoom ou une image du bon animal dans une autre posture ne remplace pas cette correspondance. Vérifier l’action dans l’extrait retenu et dans le recadrage final ; remplacer le plan si elle n’est pas identifiable.

**L'action racontée se voit en vrai, sources citées (Marc, 12 novembre 2026, vidéo 37 : « il faut des vidéos officielles en citant les sources. On ne voit pas l'action, c'est intolérable »).** Quand l'histoire repose sur un geste filmé (une main, un but, une faute, un accident, une célébration), montrer la vraie séquence au moment où elle est racontée. Une illustration générique à la place de l'action est refusée.
- Toutes les sources sont admises (voir « De vraies vidéos, peu importe la source » plus haut). La chaîne officielle (FIFA, UEFA, fédération, club, diffuseur d'origine) passe devant seulement à qualité égale ; sinon prendre la copie la plus nette, quelle que soit la chaîne.
- Citer la source dans `publication.txt`, `legende.txt` et `CREDITS.md` : diffuseur ou chaîne, titre, date, URL. Noter dans le manifeste le passage, l'horodatage dans la source et sa résolution.
- Garder des extraits courts, limités à l'action et à son ralenti, recadrés et montés avec la narration et l'habillage HPB : jamais un extrait viral posté tel quel. Recadrer le logo de la chaîne quand c'est possible sans perdre l'action ; sinon le laisser plutôt que de masquer le geste.
- Les archives anciennes sont souvent en 480p ou en 720p : l'exigence de 1 000 px utiles cède ici devant la vraie action. Signaler à Marc les plans doux.
- Prévenir Marc du risque droits d'auteur à la livraison : son coupé ou diffusion limitée par TikTok ou YouTube.
- Rappel de Marc du 12 novembre 2026 sur le dossier 40 (« des vraies séquences en citant les sources »). Une source qui n'est pas en 4K se pose sur fond flou du même plan, sans logo de diffuseur ni tableau de score, avec `assets/40-buts-degueulasses/archives.py`. **Ne pas poser l'image 16:9 entière** : sur un plan large, joueurs et ballon deviennent minuscules (Marc, 12 novembre 2026 : « y'en a qu'on ne voit pas assez bien »). Chaque plan reçoit sa propre fenêtre carrée de 640 à 1000 px source, centrée sur l'action par images clés repérées sur des planches quadrillées, affichée en 1080x1080 au centre de l'écran ; 4:3 seulement pour garder deux personnes côte à côte. Pour un plan large dont la source plafonne en 480p, chercher un autre angle mieux défini (caméra au ras du sol, ralenti). **Le moment raconté doit être à l'écran** (Marc, 12 novembre 2026 : « certains on ne voit même pas le but ») : repérer image par image l'instant clé (ballon qui franchit la ligne), le faire tomber dans le plan avant le volet jaune avec le but dans le cadre, et le vérifier par une capture du MP4 final à cet instant ; il passe avant la photo du joueur ou la célébration. Quand un nom est prononcé, préférer un plan de la séquence où la personne est reconnaissable, et à défaut sa photo Commons. Pexels sert seulement à l'accroche sans révélation et aux relances.

**Aussi pour les suites d’une affaire, pas seulement l’action de jeu (Marc, 12 novembre 2026, dossier 39).** Les deux règles ci-dessus valent pour tout ce qui a été filmé : conférence de presse, démission, arrivée à l’aéroport, panneaux, supporters, réaction officielle. Les chercher sur les chaînes d’info et les agences (Yonhap, KBS, SBS, franceinfo…). Vérifier la date, le lieu et les personnes de chaque extrait. Son d’origine coupé : on ne reprend ni le texte ni la voix d’un autre créateur. Pexels ne comble qu’un passage sans aucune séquence réelle, et ce passage se signale à la livraison.

**Préférence de Marc : séquences vidéo réelles plutôt que photos quand c’est possible.** Chercher d’abord une séquence identifiable, adaptée au geste décrit et exploitable dans le recadrage vertical. Ne pas remplir le montage de photos animées si de bonnes vidéos existent. Garder les photos pour un détail documentaire mieux visible ou lorsqu’aucune séquence pertinente et vérifiable n’a été trouvée ; un zoom sur une photo n’est pas une vidéo de l’action.

**Qualité d’image des vidéos (Marc, 11 novembre 2026) : une image floue, pixelisée ou baveuse fait décrocher.** La pertinence d’un plan ne rattrape jamais une mauvaise définition.
- **Vérifier la résolution avant de télécharger**, dans `info.json` ou avec `yt_dlp -F`. Le recadrage 9:16 d’une vidéo horizontale ne garde qu’un tiers de sa largeur : une source 1080p donne environ 600 px agrandis à 1080, ce qui reste flou. Exiger une **largeur utile d’au moins 1 000 px après recadrage**, soit une source horizontale en **4K (2160p)**, éventuellement 1440p pour un plan bref et net, ou une source **verticale native d’au moins 1080×1920**.
- **Télécharger le meilleur flux disponible** (`-f "bv*+ba/b"`), jamais une version réduite. Écarter les vidéos réencodées ou agrandies : blocs de compression, contours baveux, aplats de couleur, bruit dans les ombres, image traitée ou « IA ».
- **Contrôler à 100 % une capture de chaque plan retenu**, recadrée en 1080×1920, au début, au milieu et à la fin. Écarter le plan au moindre flou de mise au point, flou de bougé non voulu, compression visible ou filigrane. Les flous de mouvement d’un passage rapide restent acceptables si le sujet est identifiable.
- **Préférer un plan moins parfait mais net** à un plan idéal mais flou. Si aucune source nette n’existe pour un passage, le signaler à Marc plutôt que de livrer une image dégradée.
- Noter la résolution de la source et la largeur utile de chaque plan dans le manifeste.
- **Écarter les sources HDR** (HLG `arib-std-b67`, PQ `smpte2084`, BT.2020) : sans tonemapping, elles sortent délavées. `monter_lot_21_23.py` les refuse et normalise chaque plan en BT.709.

Pour les images générées, vérifier aussi anatomie, mains, équipements, attaches, proportions et mécanique ; ne pas présenter une illustration comme une photo documentaire. Contrôler de nouveau ces détails dans le recadrage du MP4 final, avec les textes superposés, avant de livrer. Voir les [règles détaillées de contrôle visuel](references-hpb.md#contrôle-des-visuels-et-des-petits-détails).

Pour les tops, garder le teasing sans imposer de faux n°1 ni de pause troll ; voir la [correction de Marc](references-hpb.md#petit-troll-dans-les-tops). Les « : » restent attachés au mot précédent par une espace insécable, y compris aux limites de blocs de sous-titres.

**Lisibilité des prochaines vidéos :** transcription synchronisée dès les premiers mots, sans écran de titre préalable. Attacher la ponctuation fermante au dernier mot avant le découpage des blocs. Aucun bandeau ni encart, même pour les fun facts ; vérifier la lisibilité des sous-titres sans collision.

## Nouveau post avec la vidéo des téléphones comme étalon (dossiers 24 et 25)

Quand Marc demande un nouveau post « en prenant la vidéo des téléphones comme critère de qualité », suivre le chemin du dossier 25, validé le 11 novembre 2026. Ses scripts (`preparer.py`, `planches.py`, `montage.py`, `controle.py`, `apercu.py`, `livraison.py`) sont dans `assets/25-montagnes-russes/` : les copier dans `assets/<n>-<sujet>/` et adapter le numéro de dossier.

1. **Référence de comparaison** : `reference_fichier` = `out/20-telephone-2899-dollars/version-validee/final.mp4` dans `histoire.json`, avant la production.
2. **Faits** vérifiés sur le web le jour même (vitesses, prix, dates), avec dans `sources_a_verifier` les pièges probables en commentaire (attraction fermée, record démoli, valeur arrondie).
3. **Images** : rechercher d'abord les vidéos YouTube sous Creative Commons (`python -m yt_dlp` sur une recherche filtrée CC, licence lue dans `info.json`), puis faire des planches de repérage horodatées (`planches.py`). Méfiance envers un CC posé par un tiers sur une vidéo officielle : le signaler à Marc. Une vidéo en licence YouTube standard ne s'utilise que sur choix explicite de Marc, à consigner dans les crédits. Ce choix est acquis, depuis le 12 novembre 2026, pour montrer l'action réelle d'une histoire (voir « L'action racontée se voit en vrai »).
4. **Voix** : `python monter_lot_21_23.py voix <n>`. Mesurer : au-dessous de 60 s, ajouter un fait vérifié et régénérer ; au-dessus de 70 s, couper les phrases qui expliquent sans montrer, puis régénérer. Si le quota ElevenLabs bloque, demander à Marc de relever la limite de la clé.
5. **Découpage accroché aux mots** (`montage.py` du dossier 25) : chaque fin de plan est le début d'un mot repère, cherché dans l'ordre ; une nouvelle synthèse ne désynchronise rien. Faire tomber l'image clé sur le mot qui la nomme (plongée dans le tunnel sur « tunnel »).
6. **Montage** `python monter_lot_21_23.py montage <n>`, puis captures début, milieu et fin de chaque plan (`controle.py final`), aperçu du lecteur (`apercu.py`) et livraison (`livraison.py`) : légende, crédits, contrôle daté, index.
7. **Fun fact** : conserver l’anecdote sourcée dans la narration et sa transcription normale, sans bandeau, encart, étiquette « FUN FACT » ni texte récapitulatif superposé. Ne plus générer ni incruster les anciens assets `funfact*.png`.

## Commandes

**Sous-titres stables en bas :** conserver le même ancrage bas pendant toute la vidéo, au-dessus de la légende TikTok. Ne pas alterner haut et bas selon les plans ; résoudre les collisions en adaptant les bandeaux ou le cadrage. **Sources et crédits dans la légende du post, en texte**, préparés dans `publication.txt`, sans footer de sources incrusté.

**Prévoir l’interface TikTok avant l’export** : recherche en haut, légende en bas, commandes à droite. Placer les chiffres et sous-titres dans la zone centrale ; ne pas incruster le nom du compte « HISTOIRES PAS BANALES » ; conserver uniquement le logo HPB jaune validé en haut à droite, sans bandeau de série. Vérifier avec un aperçu simulé du lecteur, distinct du final. Voir les [réglages du lot](references-hpb.md#zones-réservées-au-lecteur-tiktok). Conserver le contour des sous-titres pour leur lisibilité.

```bash
python -m narrateur --sujet "..."                       # histoire, run complet
python -m narrateur --format top --sujet "..."          # top (classement)
python -m narrateur --script-seulement                  # valider le script avant de payer
python -m narrateur --dossier <nom> --sans-video        # reprendre sans clips animés
```

Dossiers de vidéos numérotés dans `out/<numero>-<titre>/`, sans renuméroter les dossiers existants : `histoire.json`, sources et timings, `final.mp4`, `comparaison.mp4`, `publication.txt` et `legende.txt`. Les noms d'images de l'ancien pipeline ne constituent pas une consigne de produire des photos : vidéo réelle par défaut.

## Avant le premier run

1. `pip install -r requirements.txt`, copier `.env.example` en `.env` et remplir les clés.
2. Renseigner `voice.voice_id` dans `config.yaml`.
3. Toujours commencer par `--script-seulement`.

## Refaire une étape

Les étapes sont idempotentes : supprimer le fichier concerné (pas le dossier) et relancer avec `--dossier`.
- Une image à refaire : supprimer `imgNN.png`.
- Un clip à refaire : supprimer `clipNN.mp4`.
- La voix : supprimer `voix.mp3` **et** `timings.json` ensemble, sinon les sous-titres se décalent.

## Diagnostic

| Symptôme | Cause probable | Action |
|---|---|---|
| Sous-titres décalés | Texte modifié sans régénérer la voix | Supprimer `voix.mp3` et `timings.json` |
| Pas de sous-titres, ffmpeg muet | Chemin absolu dans le filtre `ass` | Garder `cwd` = dossier de la vidéo et des noms relatifs |
| Clip absent, image fixe à la place | Animation échouée (modèle ou champ API changé) | Lire la console, ajuster `veo_model` / `kling_model` |
| Erreur 401 ou 403 | Clé manquante dans `.env` | Vérifier la variable de `docs/architecture.md` |
| Scènes qui durent trop peu | Narration très courte (minimum 0,8 s) | Allonger la narration de la scène |

## Test sans clé API

Le montage se teste avec une image et un son synthétiques ffmpeg (voir `narrateur/assemble.py`) avant tout run payant.

## Après la vidéo

Passer par la skill `publier-tiktok`.
