---
name: short-bolt-like
description: Écrit et monte un Short « bolt-like » pour Histoires pas banales, c'est-à-dire un personnage inspirant raconté à la façon de la chaîne BoltMotivation (ouverture sur un vrai son, narrateur grave qui relie, vraies images, fin sur le son d'origine). À utiliser dès que Marc parle de Short façon Bolt, de format Bolt, de bolt-like, de personnage inspirant, de sportif qui échoue puis revient, ou demande de refaire un dossier « comme Bolt ». Ne sert pas aux tops ni aux histoires HPB classiques.
---

# Short « bolt-like »

Format demandé par Marc le 16 novembre 2026 : « TOUT PAREIL » que https://www.youtube.com/@BoltMotivationYT/shorts. Pour ce format, les codes de Bolt passent devant les règles HPB habituelles. Gabarit : `out/53-kevin-mayer-zero-puis-record/` (`voix.py`, `calage.py`, `plans.py`, `montage.py`). Le gabarit est la version de 49 s validée par Marc le 16 novembre 2026 (« ET BAH VOILA !! ON RESSENT TOUT LAAAA ») ; les versions de 35 s et de 69 s restent dans `_version-bolt-35s/` et `_version-vrai-son-69s/`.

## Ce qui reste HPB

- **Aucune durée minimale** (Marc, 16 novembre 2026 : « on enlève cette règle partout, seul compte la référence »). La durée et le rythme sont ceux du Short de Bolt pris comme référence, soit 25 à 58 s. Rester sous une minute protège aussi du blocage mondial qui frappe un Short de plus d'une minute revendiqué par Content ID.
- Original, vérifié, étiqueté : aucun texte, image ou histoire repris de Bolt ; chaque fait vérifié sur une source ; sources citées en légende et dans `CREDITS.md`.
- Sujet validé par Marc avant production : 5 propositions, personnages français d'abord, et il choisit.
- Rien n'est programmé ni commité sans sa demande.

## Ce qui a fait la différence sur le dossier 53

Six versions le même soir. Celle que Marc a validée d'un coup a deux choses que les autres n'avaient pas :

1. **La musique de la référence elle-même**, identifiée par reconnaissance audio puis calée comme chez Bolt : son temps fort (le refrain final) tombe sur le dénouement, et ses passages dépouillés sur la chute et les larmes. Aucune musique de stock n'avait convaincu.
2. **Les séquences d'émotion gardées même si elles allongent** : la voix du héros au plus bas, ses larmes, le dénouement entier au son d'origine. Marc : « si certaines séquences peuvent ajouter de l'intensité (ex : larmes), on peut dépasser ».

**La bande-son est prioritaire pour chaque vidéo Bolt.** Choisir la référence et identifier sa musique, puis préparer trois variantes audio et les faire écouter à Marc avant de commencer le montage. Attendre son choix avant de monter.

## Les trois critères de Marc

« Intensité, émotion et revirement de situation » (16 novembre 2026). Avant d'écrire, nommer pour le sujet :

- **l'émotion** : le vrai son et le visage où le héros est au plus bas ou au plus haut ;
- **le revirement** : la phrase unique qui retourne l'histoire (« Mais 40 jours plus tard, à Talence, il fait ça »), avec éclair blanc et entrée de l'orchestre au même instant ;
- **l'intensité** : musique qui grandit, commentaire d'origine, dernière image qui prouve l'exploit.

Si l'un des trois manque dans les sources, le dire à Marc avant de produire.

## La recette

Référence à garder sous les yeux : « He Was Disqualified… Then Came Back For Revenge » (https://www.youtube.com/shorts/i3xxhn5ZDb4, 22 M de vues).

1. **Ouvrir sur un vrai son**, 4 à 6 s : la voix du héros ou du commentateur au moment où tout bascule, sur l'image de sa réaction. Pas de narrateur avant.
2. **Le narrateur relie**, il ne raconte pas tout : qui, où, quand, l'enjeu, et la promesse du dénouement dans les 12 premières secondes (« et pourtant, 40 jours plus tard, il battra le record du monde »).
3. **Retour en arrière** sur le moment clé, puis un vrai son de témoignage.
4. **La remontée** en 2 ou 3 étapes chiffrées, avec un vrai son si on en a un.
5. **Finir sur le son d'origine** du dénouement (commentaire, public), sans conclusion du narrateur, sans chute maison, sans appel, sans « Pas banal, hein ? ». Ne pas redemander la chute à Marc pour ce format.

Viser les deux tiers de la durée en vrai son, comme la référence (Marc : « il faut peut-être plus de vrai son », puis « refais la vidéo au rythme de celle de Bolt ») : le narrateur ne dit que deux ou trois phrases, une trentaine de mots.

## Le hook

- **Compréhensible sans connaître la discipline.** Tout signe propre au sport s'explique en trois mots : « le juge lève un drapeau rouge : saut annulé, zéro point ».
- **Le héros au fond du trou se voit de face** (Marc : « on ne voit pas la déception […] il doit être au fond du trou ») : son visage en gros plan, au plus bas, ralenti sous sa propre voix si besoin. De dos ou de loin, cela ne suffit pas.
- **Le contraste d'émotion se voit**, « le côté douche froide » : une image de la joie, une image de l'effondrement, et le basculement marqué (éclair blanc, passage au noir et blanc, musique qui s'efface).
- Vérifier avant la voix qu'on possède vraiment l'image de chaque émotion annoncée. Sinon, le dire à Marc plutôt que de plaquer la phrase sur une autre image.

## La voix

- **Jayce** (ElevenLabs `jhQTaVBI6hnd0ESpmfIu`), choisie par Marc sur essais : le narrateur de Bolt est grave (environ 88 Hz), Hugo est trop aigu pour ce format. Hugo reste la voix des tops et des histoires HPB.
- **Ton de Bolt = phrases enchaînées**, reliées par « mais », « et », « et pourtant », peu de points : viser moins de 15 % de silence dans la narration. Le style haché HPB (« Trois fautes. Zéro point. Il abandonne. ») donne 22 à 24 % de silence et ne sonne pas Bolt.
- Noms étrangers en phonétique française dans `narration_voix`, orthographe d'origine à l'écran.
- Pour un doute de voix ou de ton, faire écouter à Marc 3 ou 4 pistes son courtes avec la musique, plutôt que d'argumenter avec des mesures.

## L'habillage

- 100 % vraies images, une coupe toutes les 2 s environ, des plans plus longs sur les visages et les vrais sons, aucun plan sous 0,75 s.
- Alternance plein écran et cadre entre deux filets blancs lumineux sur fond flou.
- Couleur partout quand la référence est en couleur ; le noir et blanc pour le passé reste possible si la référence choisie l'utilise.
- Sous-titres de 2 à 3 mots, capitales blanches, centrés, un mot coloré lumineux ; les vrais sons sont sous-titrés entre guillemets.
- Logo HPB petit, centré en bas.
- Aucun logo ni incrustation d'une autre chaîne dans le cadre : recadrer.

## L'émotion et la musique

**Règle de Marc (16 novembre 2026) : « la courbe de la musique doit marquer les moments importants de la video ».** Avant de monter, poser côte à côte la courbe du morceau (passages pleins, creux, montées, temps fort) et les moments clés du récit (joie, chute, larmes, revirement, dénouement), et décaler les plans et les vrais sons jusqu'à ce que chaque moment clé tombe sur un événement du morceau. Le noter dans `CONTROLE.md`, moment par moment.

Marc : « il faut intégrer beaucoup d'émotion et la musique qui s'intensifie joue aussi beaucoup ».

- **Mesurer la musique avant de la choisir** (niveau par tranches de 4 s) : une piste qui ne gagne que 3 dB en 90 s est plate, même si son titre promet le contraire. Chercher un morceau avec une vraie entrée d'orchestre, 10 dB ou plus au-dessus de son introduction.
- **Caler l'entrée de l'orchestre sur le retournement** (le retour du héros), pas au hasard : fond discret pendant la chute, silence ou presque sur la douche froide, montée, entrée, puis volume qui grandit jusqu'au dénouement.
- **Un lit de musique continu dès la première seconde**, comme la référence : mesuré chez Bolt, le fond reste 4 à 5 dB sous la voix et ne tombe jamais entre les phrases. Une introduction presque muette laisse le son « pomper » entre voix et silence ; Marc l'a entendu tout de suite. Mesurer le plancher du fond passage par passage, et compter les sauts de plus de 8 dB.
- Adoucir l'entrée et la sortie de chaque vrai son (0,15 s et 0,35 s).
- Baisser la musique sous un vrai son à voix basse, et vérifier par transcription que chaque mot reste compris.
- L'émotion vient d'abord des vraies voix et des visages : garder les larmes, les étreintes, les mains sur la tête, et les laisser un peu plus longtemps que les plans d'action.
- Musiques sous licence compatible avec la publication, créditées dans `CREDITS.md` et en légende. Marc demande de ne plus utiliser Mixkit pour ce format (16 novembre 2026).
- Identifier la musique de la référence par reconnaissance audio (12 s d'extrait envoyés à api.audd.io) : celle de « He Was Disqualified… » est « Daylight (Instrumental) » de David Kushner, dernière partie du morceau. C'est un titre du commerce : incrusté dans le fichier, il n'est pas sous licence. Le dire à Marc, avec la voie autorisée (la bibliothèque de sons des Shorts dans YouTube, ou une bibliothèque payante), et le laisser décider.
- Présenter trois extraits audio directement écoutables, avec des musiques réellement distinctes, sur le même passage et avec les mêmes voix et sons originaux. Faire entendre la chute, le revirement et la montée jusque dans le dénouement, à niveau comparable. Marc choisit à l'oreille.

## Production

Depuis le dossier de la vidéo, en copiant les quatre scripts du gabarit :

1. Télécharger les sources en 1080p (`yt-dlp --js-runtimes node`) dans `sources/`, repérer les plans à la seconde exacte par extraction d'images, jamais sur une planche approximative.
2. Transcrire les vrais sons avec horodatage des mots (faster-whisper, `reperage/tr.py`) pour les couper proprement et les sous-titrer.
3. `histoire.json` : scènes de narration et scènes `son_reel`. `python voix.py` écrit `voix.mp3` et `timings.json`.
4. `calage.py` : blocs de voix (`BLOCS`), vrais sons (`SONS`) et ordre (`SEQUENCE`). `plans.py` : chaque plan est accroché à un mot (`mot('…')`) ou à un vrai son (`reel('r1', 1.9)`). Changer la voix ou le texte ne demande donc aucun recalage à la main.
5. `python montage.py plans`, puis `titres`, puis `final`.

## Contrôles avant de livrer

- Durée vidéo et audio égales, sous une minute ; la durée peut dépasser celle de la référence si ce sont des séquences d'émotion qui l'allongent. Niveau autour de -12 LUFS, comme la référence.
- Réécoute automatique du final (Whisper) : phrases entières, aucun mot coupé aux raccords.
- Une image par plan, et l'ouverture image par image : chaque plan tombe sur son mot, aucun logo tiers.
- Part de narration et part de vrai son (`python calage.py` les affiche).
- Écrire `CONTROLE.md` avec ce qui a été réellement examiné et les limites. Claude n'entend pas le son et ne voit pas le mouvement : le dire à chaque livraison.

## Livraison

`final.mp4`, `publication.txt`, `legende.txt`, `CREDITS.md`, `CONTROLE.md`, avec liens cliquables. `comparaison.mp4` (Short de Bolt à gauche, HPB à droite, deux pistes son) seulement si Marc la demande. Miniature après validation du montage. Signaler le risque de réclamation de droits sur les images et les sons de tiers.
