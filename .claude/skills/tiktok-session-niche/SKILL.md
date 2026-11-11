---
name: tiktok-session-niche
description: Session TikTok automatique dans le Chrome de l'utilisateur pour entraîner l'algorithme d'un compte sur des niches (par défaut fitness à la maison, fitness pour les nuls, fitness pour débutants, fitness sans matériel) : chaque vidéo lue en entier, 5 à 10 s de pause puis la suivante, like sur 30 %, partage sur 10 %, mot gentil en commentaire sur 20 %, suivi de l'auteur sur 10 %, zap après 5 à 10 s sur 20 %, au hasard, pendant une durée donnée. Utiliser dès que l'utilisateur demande de regarder, faire défiler ou scroller TikTok, de chauffer ou entraîner un compte, de changer les vidéos du fil vers une niche, de liker, partager ou commenter automatiquement sur TikTok.
---

# Session TikTok par niche

Répondre en français, sans discuter : l'utilisateur veut que ça tourne. Faire un bilan court à la fin.

## Règles de l'utilisateur

- Pour TikTok, une vidéo **lue en entier** compte plus qu'un like ou un partage. Ne jamais passer une vidéo avant sa fin, sauf zap.
- Une vidéo de plus de 3 min est toujours zappée après 5 à 10 s, sans aucune action (`dureeMaxSec`, règle de l'utilisateur du 4 novembre 2026).
- Après la fin : attendre entre 5 et 10 s (au hasard), puis passer à la suivante.
- Niches par défaut (règle de l'utilisateur du 11 novembre 2026, pour TikTok et YouTube) : sport insolite, triche dans le sport, gossip sportifs, scandale sportif, exploit sportif incroyable, histoire vraie sport. **Jamais de fitness ni de musculation** (« pas d'histoire de fitness »). Adapter `mots` au sport (« Incroyable ! », « Je ne savais pas ! », « Quelle histoire »). On n'utilise pas le fil « Pour toi » mais les résultats de recherche (onglet Vidéos), 6 vidéos par niche, en boucle.
- Les niches suivent le compte connecté (règle de l'utilisateur, 9 novembre 2026 : « les niches en rapport avec ce compte, voir publications »). Pour @histoirespasbanales (tops, records, culture générale) : top 3 record, le saviez-vous, culture générale, records du monde, histoire vraie incroyable, le saviez vous géographie, astronaute espace, armées les plus puissantes, faits incroyables, classement top 3 monde. Adapter aussi `mots` au compte (« Fascinant ✨ », « Je ne savais pas ! », « J'ai appris un truc »…).
- Zap : 20 % des vidéos sont passées après 5 à 10 s (au hasard), sans like, partage, commentaire ni suivi, pour que le compte ait l'air humain.
- Au hasard, sur les autres vidéos : like 30 %, partage 10 %, commentaire 20 %, suivi de l'auteur 10 %, à un moment aléatoire entre 30 et 85 % de la vidéo.
- Commentaire : un mot gentil court tiré d'une liste (dans `session.js`). Jamais de lien, de nom d'app ni de promo.
- Durée : celle que l'utilisateur donne (25 min la première fois). Arrêt automatique.

## Procédure

1. Navigateur : **Claude in Chrome** (règle de l'utilisateur), outils chargés en un seul `ToolSearch`. L'onglet TikTok que l'utilisateur a déjà ouvert n'est pas visible depuis le groupe de la session : ouvrir un onglet avec `navigate` (le compte de l'utilisateur est déjà connecté dans son Chrome).
2. Aller sur `https://www.tiktok.com/search/video?q=<première niche>`, attendre 4 s.
3. **Vérifier le compte avant tout** (règle de l'utilisateur, 7 novembre 2026, après une session lancée sur le mauvais compte) : lire le pseudo connecté (`a[data-e2e="nav-profile"]`, attribut `href`, par exemple `/@ju.basicfrite`), le donner à l'utilisateur et attendre son accord explicite pour ce compte. Ne rien lancer avant, même s'il vient de dire « relance ». Revérifier à chaque nouvelle session : le compte connecté dans Chrome peut avoir changé.
4. Cliquer la première vignette : le lecteur s'ouvre avec le panneau de commentaires à droite.
5. Lire [session.js](session.js), régler `CONFIG` (niches, `dureeMin`, probabilités), puis coller tout le fichier dans `javascript_tool`. Il renvoie l'heure d'arrêt.
6. Suivre sans sonder en boucle : `sleep` en arrière-plan (Bash, `run_in_background`), puis lire `window.__autoNext` (`count`, `niche`, `stats`, `err`, `stopped`).
7. Bilan à la fin : vidéos lues, niches parcourues, likes, partages, commentaires avec leur texte (`stats.log`).

## Variante téléphone (adb)

Quand l'utilisateur dit « via le tel » ou « sur le téléphone » : Redmi Note 11 Pro 5G par `adb` (voir la mémoire `telephone-adb`), script [session_tel.py](session_tel.py), mêmes règles qu'en ligne.

1. `adb devices` doit lister `6403aa005318`. Réveiller l'écran (`input keyevent KEYCODE_WAKEUP`). Si une autre appli est devant, relancer TikTok (`monkey -p com.zhiliaoapp.musically -c android.intent.category.LAUNCHER 1`).
2. Vérifier le compte : onglet Profil (tap 972 2232), capture `adb exec-out screencap -p` (depuis Bash, pas PowerShell qui abîme le binaire), lire le pseudo, attendre l'accord de l'utilisateur.
3. Lancer en arrière-plan : `python -u session_tel.py <dossier> <minutes> [index_niche] [hpb|sport]`. Le script part de l'écran courant (profil, accueil ou lecteur).
4. Suivre par `status.json` (`videos`, `lues`, `likes`, `commentaires`, `suivis`, `log`, `err`, `stopped`) avec un `sleep` en arrière-plan, et une capture d'écran au premier contrôle.

Pièges relevés le 11 novembre 2026 :
- `uiautomator dump` ne rend presque rien : tout passe par des captures et la couleur des pixels.
- Fin de vidéo : barre de progression à y≈2131, deux gris (clair = lu, foncé = restant, valeurs variables selon le fond). Le script détecte le retour au début.
- Les boutons de droite se décalent d'environ 100 px quand une ligne « Recherche · … » s'affiche en bas : le script les retrouve par la bulle de commentaire et la flèche de partage.
- Après « Copier le lien », un bandeau couvre le bas de l'écran pendant quelques secondes : un tap dessus ouvre un réglage. Le script attend 6 s.
- Une fenêtre TikTok (demande de localisation) peut bloquer l'ouverture de la vidéo : répondre « Annuler » ou Retour, jamais « Ouvrir les paramètres ». Le script le fait seul.
- Le câble USB a décroché deux fois en 40 min : le script attend jusqu'à 10 min le retour du téléphone, puis s'arrête.
- `input text` ne passe ni accents ni emojis : recherches et commentaires en ASCII.
- Après un commentaire, la vidéo peut rester en pause sur sa fin au lieu de reboucler : 10 min perdues le 11 novembre 2026. Le script compte la vidéo comme lue après 5 s figée en fin de barre.

## Pièges connus (31 octobre 2026)

- TikTok met la vidéo en pause quand l'onglet est caché (fenêtre Chrome réduite, autre onglet devant) : sans parade, une session de 34 min a perdu 8 min (1er novembre 2026). `session.js` force `document.hidden` à faux, bloque `visibilitychange` et `blur`, et relance la lecture chaque seconde. La vidéo n'est pas en sourdine, l'onglet est donc audible et Chrome ne bride pas ses minuteries. Prévenir l'utilisateur que le son joue pendant la session.
- Une vidéo en sourdine est freinée par Chrome quand l'onglet n'est pas au premier plan : le 8 novembre 2026, 20 min de session n'ont fini qu'une vidéo (95 s lues en 11 min). TikTok mémorise la sourdine dans `localStorage['webapp-video-mute']` (par exemple après avoir coupé le son du lecteur). `session.js` la lève et remet `video.muted` à faux chaque seconde. Après le lancement, vérifier `video.muted === false` et que `currentTime` avance de 10 s en 10 s.
- Une vidéo peut refuser de se lancer (« Nous éprouvons des difficultés à lancer cette vidéo ») : la page n'a alors plus de `<video>` et l'ancien script restait bloqué (9 min perdues le 1er novembre 2026). `session.js` passe à la suivante après 15 s sans vidéo et compte ces cas dans `stats.illisibles`.
- Les vidéos TikTok tournent en boucle : l'événement `ended` n'arrive pas. Le script détecte le retour au début de la vidéo.
- **Ne jamais recharger la page ni changer `location.href`** pendant la session : ça tue le script. Pour changer de niche, `__switchQ` passe par le formulaire de recherche caché de la barre latérale (`input[data-e2e="search-user-input"]`, `requestSubmit`), puis rouvre la première vidéo.
- L'éditeur de commentaire est Draft.js. `document.execCommand('insertText')` ou une suppression du texte fait planter le panneau (« Une erreur est survenue ») : seul un `ClipboardEvent('paste')` avec un `DataTransfer` marche. Si le panneau plante quand même, le script le reconstruit au changement de vidéo (fermer puis rouvrir depuis la recherche).
- Like : bouton parent de `[data-e2e="browse-like-icon"]`, ne cliquer que si `aria-pressed` ne vaut pas `"true"` (sinon on retire un like).
- Partage : `[data-e2e="browse-copy"]` (« Copier le lien ») compte comme un partage sans rien publier. Ne pas utiliser « Republier » ni « Envoyer à des amis » sans accord de l'utilisateur.
- Suivre : bouton dont le texte est exactement « Suivre », dans la moitié droite de l'écran (en haut du panneau). La barre latérale a aussi un bouton « Suivis » : ne pas le confondre. `suivisDeja` évite de suivre deux fois le même compte.
- Onglet Chrome en arrière-plan : TikTok ne dessine pas le panneau de droite (pas de `browse-like-icon`), alors que la vidéo et la flèche marchent. Le 9 novembre 2026, l'ancien script prenait ça pour un panneau planté et relançait une recherche après chaque vidéo : 6 likes sur 61 vidéos. `session.js` passe désormais par la flèche même sans panneau, et retente les actions jusqu'à la fin de la vidéo tant que le panneau manque. Le panneau revient quand l'onglet repasse au premier plan.
- Vidéo suivante : `[data-e2e="arrow-right"]` dans le lecteur de recherche, `[data-e2e="feed-navigation-next"]` dans le fil « Pour toi ».
- Un `javascript_tool` qui attend plus de 45 s échoue : attendre côté Bash, pas dans la page.
- Après un rechargement du panneau, la recherche rouvre la première vidéo de la niche : une vidéo peut repasser. `deja` évite de la liker ou commenter deux fois.
- Chrome bloque la lecture avec le son tant que la page n'a pas reçu un vrai geste de l'utilisateur : si la première vignette a été ouverte par un clic lancé en script (`a.click()` dans `javascript_tool`), la vidéo reste en pause à 0 s malgré `v.play()` (7 novembre 2026, 90 s perdues). Ouvrir la première vignette avec un clic `computer`, ou cliquer une fois sur la vidéo avec `computer` après avoir collé le script, puis vérifier `video.paused` et `navigator.userActivation.hasBeenActive`.
- Pour marteler une seule niche (demande de l'utilisateur du 7 novembre 2026, « tabasser la niche fitness à la maison »), ne pas mettre une seule requête dans `niches` : à chaque changement, la recherche rouvrirait les mêmes premières vidéos. Mettre plusieurs formulations de la même niche (« fitness à la maison », « sport à la maison », « séance fitness maison », « entraînement à la maison », « fitness maison débutant », « exercices à la maison », « fitness chez soi », « sport chez soi sans matériel », « fitness à la maison femme », « remise en forme à la maison ») et monter `parNiche` à 8.
