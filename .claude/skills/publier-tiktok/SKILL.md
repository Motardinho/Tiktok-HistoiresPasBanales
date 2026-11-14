---
name: publier-tiktok
description: Checklist de publication d'une vidéo Histoires pas banales sur TikTok (label IA, vérification des faits, légende, hashtags, horaire, suivi). À utiliser avant de poster ou pour préparer la légende et le planning.
---

# Publier sur TikTok

Publier est une action de l'utilisateur : ce skill prépare et contrôle, il ne poste pas.

## Checklist (dans l'ordre)

0. **Durée** : mesurer le MP4 final, strictement plus de 60 secondes. Contrôler la nouvelle signature orale, les nombres en chiffres et les unités françaises selon les [règles du compte](../produire-video/references-hpb.md).
1. **Faits** : relire `sources_a_verifier` dans `publication.txt` et vérifier chaque point sur une source indépendante. Si un fait ne se vérifie pas, corriger la narration et regénérer la voix, ou abandonner la vidéo.
   **Détail sourcé mais incertain (règle de Marc, 11 novembre 2026)** : on ne cherche pas l'exactitude parfaite. Un détail secondaire repris d'une source publiée (Wikipédia, presse), même contesté par une autre source, ne bloque pas la publication : une erreur de détail fait réagir et les gens viennent corriger en commentaire, ce qui crée de l'engagement. Exemple : vidéo 26, « il est revenu courir la course 6 fois » (Wikipédia ; d'autres sources disent 8). Signaler l'écart à Marc, puis programmer. La limite reste le principe du compte : jamais de fait inventé, et le chiffre central d'un top (record, classement) se vérifie toujours (R-09). Si un commentaire corrige, répondre ou épingler la précision.
2. **Règles** : R-03 à R-05 du PRD respectées (pas d'affaire récente non jugée, pas de nom de victime mineure, pas de gore).
3. **Rendu** : regarder `final.mp4` en entier, son activé : voix, sous-titres synchrones. Regarder aussi les 5 premières secondes sans le son, selon la [règle du hook](../ecrire-histoire/SKILL.md#hook-des-5-premières-secondes-et-temps-de-visionnage-marc-11-novembre-2026) : plan spectaculaire, phrase-hameçon, aucun logo d'un tiers à l'écran.
4. **Label IA, seulement s'il est vraiment justifié** (choix de Marc du 11 novembre 2026). Activer « contenu généré par IA » quand la vidéo contient des images ou des vidéos réalistes générées par IA (gpt-image-1, Veo, Kling), ou une voix qui imite une personne réelle : c'est ce que la règle de TikTok vise. Pas de label pour une vidéo de vrais plans (Pexels, archives) narrée par la voix ElevenLabs du compte, qui n'imite personne : exemple de la vidéo 28. En cas de doute, demander à Marc.
5. **Légende** : une accroche et une question d'engagement (voir `publication.txt`), sans spoiler de la chute.
6. **Hashtags** : 3 à 5, dont `#histoirevraie` et un hashtag de série.
7. **Horaire** : tester la plage 18 h à 22 h puis ajuster selon les statistiques du compte.
8. **Top** : chaque chiffre et chaque classement confirmé sur une source datée (R-09). En cas de doute, retirer l'entrée.
9. **Vérification de contenu** : la laisser activée et attendre son résultat avant de programmer. Si TikTok signale la vidéo comme non éligible au fil Pour toi ou relève un problème de droits, corriger la vidéo avant de publier. Ne la désactiver que sur décision explicite de Marc, à noter dans le planning.
10. **Compte** : la publication se fait sur Histoires pas banales (voir la mémoire sur le compte actif dans Chrome), depuis un appareil déjà utilisé.
11. **Qualité d'envoi** : dans « Plus d'options », activer « Autoriser les importations de haute qualité » et le revérifier à chaque post, car le réglage se désactive parfois tout seul. Sinon, TikTok recompresse fort la vidéo.
12. **Miniature (couverture) = fichier séparé de la vidéo** (règle de Marc, 13 novembre 2026, qui remplace celle du 11 « première image de la vidéo »), sur TikTok comme sur YouTube Shorts. Elle se compose avec `python miniatures_hpb.py <n>` (sortie dans `out/miniatures-v4/<n>.jpg`) et s'importe comme couverture ; elle n'est pas incrustée dans `final.mp4`. Habillage : seule la bulle jaune « HPB », lettres découpées qui laissent voir l'image, en haut à droite (ni bandeau de chaîne, ni bandeau de série), et un titre dans l'un des cinq styles de `STYLES` retenus par Marc le 13 novembre 2026 (`pop`, `course`, `autocollant`, `magazine`, `jaune` ; maquettes 06 à 10 de `out/miniatures-10-variantes-2026-11-12/`), choisi selon le sujet. Le style `magazine` demande trois lignes (mot géant, mot sur plaque rouge, ligne jaune). Les cinq styles sont calés au pixel sur leurs maquettes (polices, pentes, plaques, ombres) : ne pas donner de taille aux lignes hors `magazine`, le style la fixe et réduit seul une ligne trop longue. Contrôle : `out/miniatures-v4/controle-<n>.jpg` (maquette à gauche, rendu à droite) pour les dossiers 24, 31, 40, 42 et 43. Pour un nouveau dossier, ajouter une entrée à `DOSSIERS` (fond réel sans titre, style, lignes).
13. **Description** : la recherche ne pèse qu'environ 1 à 2 % des vues. La légende sert surtout à relancer l'appel au commentaire (« Oui ou non 👇 ») ; inutile de l'allonger pour le référencement.

## Distribution : éviter les vidéos à 0 vue (11 novembre 2026)

Constat du 11 novembre : astronautes et bouchons sont restées à 0 vue. TikTok ne les a montrées à personne, sans avertissement ni restriction visible dans l'app, les notifications système ou TikTok Studio web. Le compte lui-même n'est pas bloqué : les voitures ont fait 331 vues, à 99 % depuis le fil Pour toi. Causes probables : compte créé le 8 novembre et pas chauffé, publications supprimées puis remises en ligne, images déjà présentes sur TikTok (logo ESA, clips Pexels), connexions depuis plusieurs appareils. Règles qui en découlent, complétées par la vidéo de Paul Agd demandée par Marc (https://www.youtube.com/watch?v=Bqy8_lkE_a4) :

- **Ne jamais supprimer une vidéo publiée : la passer en privé.** Une suppression envoie à TikTok un signal négatif, et des suppressions répétées freinent tout le compte. Pour les posts programmés, valider la version avant de programmer, pour ne pas avoir à les supprimer et les reprogrammer (trois suppressions les 8 et 9 novembre).
- **Ne jamais remettre en ligne le même fichier** : il serait traité comme un doublon. Une seconde chance n'est possible qu'avec une vraie nouvelle version : autre hook, autres premières secondes, autre couverture. Pas avant que l'ancienne ait été passée en privé.
- **Vidéo à 0 vue** : attendre 48 h avant de juger, car une vidéo bloquée à 0 après 48 h ne repart quasiment jamais. Ensuite, la passer en privé si Marc le souhaite, et relever dans le planning ce qui la distingue des vidéos qui ont été diffusées.
- **Chauffer le compte, à la main** : sur le téléphone, environ 1 h par jour pendant les premiers jours, puis un peu chaque jour. Regarder des vidéos de la niche (records, tops, science, véhicules, phénomènes spectaculaires), s'abonner à quelques comptes de la niche, liker, mettre en favoris, partager. Ne pas lancer la session automatique `tiktok-session-niche` sur ce compte sans demande explicite de Marc : l'objectif est justement de prouver à TikTok que le compte n'est pas un robot.
- **Rester dans la niche** : des tops et des faits spectaculaires et vérifiés, sous le même habillage. Pas de sujet hors thème pour tester.
- **Régularité** : au moins une vidéo par jour, à des heures stables, même quand les statistiques déçoivent. Ne pas sacrifier la qualité pour en publier davantage.
- **Effet boule de neige** (vidéo de Paul Agd, https://www.youtube.com/watch?v=N-iXZM3ray0) : quand une vidéo décolle, publier la suivante vite, sans attendre le créneau du lendemain, et reprendre son concept (même type d'histoire, même angle, même structure de hook) avec un sujet nouveau. Pour trouver des concepts, trier les vidéos d'un concurrent de la niche par popularité, par exemple @secretdusport_. On reprend un concept, jamais un texte, une histoire racontée de la même façon ou des images.
- **Contenu original** : aucun logo ni filigrane d'un tiers à l'écran, aucun extrait viral repris tel quel en ouverture ; toujours de la narration et un montage propres à HPB. Les vidéos qui se contentent de reprendre un reportage ou un extrait ne sont plus mises en avant.
- **Appareils** : publier toujours depuis les mêmes appareils et limiter les nouvelles connexions au compte. Ne pas basculer entre HPB et moovini.app dans la même session Chrome juste avant de publier.

## Programmer depuis Chrome (11 novembre 2026)

- **Programmer = TikTok Studio web.** L'appli TikTok du téléphone ne propose que « Publier » (immédiat) ou brouillon : ne jamais toucher « Publier » sur le téléphone.
- **Import des MP4 de plus de 10 Mo** : l'outil d'import de Claude in Chrome plafonne à 10 Mo par appel, et TikTok bloque un `fetch` vers 127.0.0.1. Découper le MP4 validé en morceaux de 9 Mo, les charger un par un dans un `input type=file` ajouté à la page, les réassembler en `Blob`, contrôler le SHA-256 dans la page contre `validation-utilisateur.json`, puis l'affecter au champ d'import (TikTok : premier `input[type=file]` ; YouTube : `input[name=Filedata]`, l'import démarre après quelques secondes). Charger `legende.txt` ou `publication.txt` de la même façon, pour un texte exact.
- **Légende TikTok** : coller par `ClipboardEvent('paste')` dans l'éditeur, curseur placé à la fin ; le nom du fichier reste devant : placer le curseur au début et l'effacer avec la touche Suppr (outil clavier). Ne jamais vider tout l'éditeur par sélection + `execCommand('delete')` : TikTok Studio plante (« Une erreur est survenue ») et l'import est perdu (11 novembre 2026). **YouTube** : `execCommand('insertText')` dans les deux `#textbox` (titre, description).
- **YouTube** : miniature = le fichier séparé `out/miniatures-v4/<n>.jpg`, importé (voir le point 12). Sans « validation unique » du compte, YouTube limite les miniatures personnalisées sur 24 h (une seule passée le 11 novembre 2026), et Marc ne peut pas la faire pour l'instant. Une fois la limite atteinte, garder la miniature automatique, noter dans le planning les Shorts à corriger, et les reprendre dans YouTube Studio (Contenu > Shorts > Détails > Miniature) le lendemain, avant leur date de publication. Heure dans la liste déroulante (taper l'heure ne marche pas). Fuseau par défaut : heure locale GMT+1.
- **Contrôle final** : relire la liste Publications de TikTok Studio et l'onglet Shorts de YouTube Studio (date, heure, pas de doublon).

## Après publication

- À J+1 et J+2, dans TikTok Studio : vues, temps de visionnage moyen, pourcentage de visionnages complets, seconde où la plupart des spectateurs décrochent, sources de trafic (visibles à partir de 100 vues), partages. Les noter dans le planning.
- Si les spectateurs décrochent avant 0:03, c'est le hook visuel qu'il faut revoir. S'ils décrochent entre 0:03 et 0:10, c'est le hook audio ou la promesse. Après, c'est le rythme et les relances.
- Si une métrique décide d'un choix de style ou de format, consigner la décision datée dans `docs/decisions.md`.

## Pièges

- Ne jamais présenter la voix comme celle d'une personne réelle.
- Ne pas republier une histoire déjà traitée (dossiers de `out/`).
- Un commentaire qui signale une erreur factuelle se traite vite : corriger en commentaire épinglé.
