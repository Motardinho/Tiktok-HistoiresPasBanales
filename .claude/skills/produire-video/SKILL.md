---
name: produire-video
description: Lance, reprend ou dépanne la production d'une vidéo Histoires pas banales, histoire ou top (voix ElevenLabs, images OpenAI, animation Veo/Kling, montage ffmpeg). À utiliser pour générer une vidéo, refaire une étape, régler le rendu ou diagnostiquer une erreur du pipeline.
---

# Produire une vidéo

Lire les [règles de production du compte](references-hpb.md) avant tout rendu : elles contiennent les exigences impératives de durée, de transcription numérique, de hook, d’habillage et de chute. Refuser une livraison dont le MP4 final ne dépasse pas 60 secondes.

Les corrections les plus récentes de Marc priment sur les anciens scripts et exemples du lot. Ne pas recopier un ancien montage sans le confronter aux règles actuelles.

## Passage obligatoire avant livraison

Pour chaque vidéo révisée, renseigner dans son dossier un contrôle daté avec les passages et fichiers effectivement examinés. Ne pas marquer un contrôle visuel comme réussi sur la seule base du script ou d'un calcul de positions.

1. Vérifier titre prononcé, classement, année réelle des données et fun fact sourcé avant la voix.
2. Contrôler à l’arrêt la première image à 0:00 selon les [règles d’accroche](references-hpb.md#hook-et-habillage), puis regarder les 5 premières secondes. Elles doivent montrer le plan spectaculaire, la phrase-hameçon prononcée avant 5,0 s et au moins deux plans différents, sans logo ni filigrane d'un tiers. Examiner chaque plan recadré au début, au milieu, à la fin et aux changements de plan : bon sujet, bonne action, sujet identifiable, aucun remplissage statique évitable.
3. Examiner le rendu à 360 pixels de large, avec puis sans son : titre et sous-titres bas, accents, ponctuation, bandeaux, compteur et fun fact lisibles sans collision. Examiner aussi un aperçu simulé du lecteur TikTok.
4. Vérifier la fin : pas de paragraphe générique qui dilue la chute, invitation naturelle à réagir, puis signature ; aucune surcouche qui double la transcription.
5. Décoder le MP4, comparer durées audio/vidéo, confirmer plus de 60 secondes, puis régénérer et vérifier la comparaison issue du dernier export. **Liens cliquables à chaque livraison, systématiquement** (demande de Marc du 11 novembre 2026, pour lancer les vidéos facilement) : envoyer `final.mp4` et `comparaison.mp4` avec l'outil d'envoi de fichiers (carte cliquable dans la conversation), puis donner dans la réponse, pour la vidéo, la comparaison et la légende, un lien Markdown relatif (`[final.mp4](out/<dossier>/final.mp4)`) et un lien `file:///` absolu, espaces encodés en `%20` (`file:///C:/Projets/Tiktok%20-%20MrBallen/out/<dossier>/final.mp4`). Un chemin entre chevrons n'est pas cliquable : ne plus l'utiliser.

**Versions validées :** lorsqu'une vidéo est approuvée, conserver `final.mp4`, `comparaison.mp4`, le script et les légendes dans `version-validee/`, avec `validation-utilisateur.json` (date, fuseau, SHA-256). Mettre à jour l'index et le manifeste. Exclure ces vidéos de toute retouche globale ; ne les rouvrir que si Marc demande une nouvelle modification de cette vidéo. Le renderer du lot respecte ce verrou par défaut.

**Livraison systématique demandée par Marc : chaque vidéo et chaque révision sont livrées avec `final.mp4` ET `comparaison.mp4`, sans attendre qu’il le redemande.** Choisir et conserver la référence dans `histoire.json` avant la production. Référence à gauche, HPB à droite, départ simultané, deux pistes audio séparées et nommées, HPB par défaut. Figer l’image et compléter par du silence après la fin de la version la plus courte. Vérifier les deux fichiers et fournir leurs deux liens à la livraison. Une comparaison absente ou antérieure à la dernière révision signifie que la livraison est incomplète.

## Contrôles à appliquer avant chaque livraison

**Titres d’ouverture toujours en bas**, comme les sous-titres, au-dessus de la légende TikTok. Ancrer le bas du bloc, pas son haut, pour garder une position stable avec deux à quatre lignes. Réglage du lot : dernière encre à y = 1370 à 1080×1920. Adapter les plans de fond si nécessaire pour ne pas masquer un détail utile : montrer le compteur automobile après la disparition du grand titre.



- **Ouverture orale :** écouter ou vérifier l’alignement de la première phrase : le narrateur annonce le titre affiché, sans l’année, puis « Numéro 3… » pour un top. Interdire les introductions qui commencent par le rang ou une formule différente. Vérifier après synthèse, pas seulement dans le script prévu.
- **Vidéo par défaut :** préparer chaque plan en séquence vidéo réelle. Une photo n’est acceptée qu’après une recherche de vidéo réellement infructueuse, avec justification précise dans le manifeste, ou à la demande explicite de Marc (ex. archive d’Hiroshima). Un zoom sur une photo ne satisfait pas ce contrôle. Ne pas conserver une photo simplement parce qu’elle est déjà montée.
- **Sous-titres :** même ancrage bas sur toute la vidéo, sans alternance haut/bas. Contrôler les collisions avec tous les autres éléments et l’interface TikTok.
- **Identité visuelle :** logo et bandeau de série ensemble à leur emplacement fixe, de la première à la dernière image. Ajuster les plans autour de ce bloc.
- **Sources :** texte prêt à copier dans la légende du post, sans bandeau de crédits ajouté au film.

## Rigueur visuelle avant montage

**Contrôle obligatoire des collisions et superpositions avant livraison.** Vérifier ensemble titres, sous-titres, bandeaux, chiffres, fun facts, logo et interface TikTok, à chaque apparition et transition. Aucun texte ne doit être recouvert par un autre élément ; retirer les mentions redondantes ou réserver des zones distinctes. Voir le [contrôle des superpositions](references-hpb.md#collisions-et-superpositions).

**Au moins un fun fact vérifié dans chaque vidéo, systématiquement.** Avant production, identifier le passage exact, sa source et le visuel qui l’illustre ; compléter le script s’il n’en contient pas. Appliquer les [règles de fun facts](references-hpb.md#fun-facts-intégrés-aux-vidéos).

**Consigne permanente de Marc : être rigoureux jusque dans les petits détails.** Examiner chaque visuel avant de l’intégrer : identité réelle du sujet, pays, époque, uniformes, insignes, drapeaux, matériel et cohérence avec la narration. Vérifier la provenance et la légende des archives ; un drapeau ou le lieu d’un défilé ne suffit pas à identifier les soldats. Écarter ou remplacer les images ambiguës. Ne pas ajouter de drapeau ni d’accessoire décoratif sans raison liée à la scène.

**Contrôler le plan sur toute sa durée après recadrage vertical.** Vérifier début, milieu, fin et mouvements intermédiaires : le sujet ou détail annoncé doit rester net et identifiable. Écarter les plans dominés par une main, un intervenant tronqué ou un avant-plan qui masque le sujet ; une voiture floue derrière un interviewé ne constitue pas un bon plan de voiture. Les gros plans restent pertinents s’ils montrent volontairement un détail raconté. Remplacer ou recadrer les passages faibles avant livraison, puis regarder le résultat avec l’habillage.

**Le visuel doit être raccord avec l’action décrite au même moment.** Lorsque Marc demande de « mettre en avant » un mouvement, choisir d’abord une photo ou une vidéo qui le montre réellement : un faucon en piqué quand la narration dit qu’il plonge, un animal en pleine course pour un sprint. Privilégier une vidéo démonstrative lorsqu’elle est disponible. Un texte superposé, un zoom ou une image du bon animal dans une autre posture ne remplace pas cette correspondance. Vérifier l’action dans l’extrait retenu et dans le recadrage final ; remplacer le plan si elle n’est pas identifiable.

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

**Lisibilité des prochaines vidéos :** titre seul pendant les premières 1,5 seconde (jusqu’à 2 si nécessaire), puis transcription synchronisée ; le narrateur reprend le titre dès l’ouverture, sans prononcer l’année. Masquer la transcription de cette annonce jusqu’à la première information suivante : ne pas réafficher en sous-titres le titre qui vient d’être lu. Attacher toute ponctuation fermante au dernier mot avant le découpage des lignes et des blocs. Éviter les bandeaux qui répètent le même texte ; garder un seul encart de fun fact, avec une taille de police commune aux lignes et 8 pixels entre les corps des capitales, les accents débordant sans modifier l’interligne. Réserver les précisions de méthode sans intérêt visuel à la fiche de sources.

## Nouveau post avec la vidéo des téléphones comme étalon (dossiers 24 et 25)

Quand Marc demande un nouveau post « en prenant la vidéo des téléphones comme critère de qualité », suivre le chemin du dossier 25, validé le 11 novembre 2026. Ses scripts (`preparer.py`, `planches.py`, `montage.py`, `controle.py`, `apercu.py`, `livraison.py`) sont dans `assets/25-montagnes-russes/` : les copier dans `assets/<n>-<sujet>/` et adapter le numéro de dossier.

1. **Référence de comparaison** : `reference_fichier` = `out/20-telephone-2899-dollars/version-validee/final.mp4` dans `histoire.json`, avant la production.
2. **Faits** vérifiés sur le web le jour même (vitesses, prix, dates), avec dans `sources_a_verifier` les pièges probables en commentaire (attraction fermée, record démoli, valeur arrondie).
3. **Images** : rechercher d'abord les vidéos YouTube sous Creative Commons (`python -m yt_dlp` sur une recherche filtrée CC, licence lue dans `info.json`), puis faire des planches de repérage horodatées (`planches.py`). Méfiance envers un CC posé par un tiers sur une vidéo officielle : le signaler à Marc. Une vidéo en licence YouTube standard ne s'utilise que sur choix explicite de Marc, à consigner dans les crédits.
4. **Voix** : `python monter_lot_21_23.py voix <n>`. Mesurer : au-dessous de 60 s, ajouter un fait vérifié et régénérer ; au-dessus de 70 s, couper les phrases qui expliquent sans montrer, puis régénérer. Si le quota ElevenLabs bloque, demander à Marc de relever la limite de la clé.
5. **Découpage accroché aux mots** (`montage.py` du dossier 25) : chaque fin de plan est le début d'un mot repère, cherché dans l'ordre ; une nouvelle synthèse ne désynchronise rien. Faire tomber l'image clé sur le mot qui la nomme (plongée dans le tunnel sur « tunnel »).
6. **Montage** `python monter_lot_21_23.py montage <n>`, puis captures début, milieu et fin de chaque plan (`controle.py final`), aperçu du lecteur (`apercu.py`) et livraison (`livraison.py`) : légende, crédits, contrôle daté, index.
7. **Encart de fun fact** : en haut par défaut. Si le sujet raconté occupe le haut du cadre (visages), choisir d'abord d'autres plans ; sinon descendre l'encart avec `fun_fact_top` dans `histoire.json` (ex. 760, bas de l'encart < 1000), sans toucher les sous-titres, et le signaler à Marc.

## Commandes

**Sous-titres stables en bas :** conserver le même ancrage bas pendant toute la vidéo, au-dessus de la légende TikTok. Ne pas alterner haut et bas selon les plans ; résoudre les collisions en adaptant les bandeaux ou le cadrage. **Sources et crédits dans la légende du post, en texte**, préparés dans `publication.txt`, sans footer de sources incrusté.

**Prévoir l’interface TikTok avant l’export** : recherche en haut, légende en bas, commandes à droite. Placer titres, chiffres, fun facts et sous-titres dans la zone centrale ; ne pas incruster le nom du compte « HISTOIRES PAS BANALES » ; conserver le logo et le bandeau de série. Vérifier avec un aperçu simulé du lecteur, distinct du final. Voir les [réglages du lot](references-hpb.md#zones-réservées-au-lecteur-tiktok). Ajouter un fin contour sombre aux titres et fun facts pour détacher les accents en conservant l’interligne compact.

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
