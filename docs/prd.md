# PRD — Dossiers Hors Normes

Compte TikTok francophone d'histoires vraies qui sortent de l'ordinaire et de tops, narrés par une voix IA. Chaque vidéo est un « dossier » numéroté. Format vertical 45 à 120 s. Ce document porte le besoin et les règles. Les frontières externes sont dans `architecture.md`, l'historique dans `decisions.md`.

## 0. État du document

- §5 (pipeline) et §8 (dépendances) renvoient à `architecture.md` pour les frontières externes.
- Les arbitrages datés sont dans `decisions.md`. Une décision datée prime sur ce PRD.

## 1. Vision

Devenir un compte de référence en français pour l'histoire vraie à suspense et le top surprenant, avec une marque reconnaissable : le dossier numéroté, la voix, le rythme, la signature de fin « Dossier clos… », et un hook irrésistible dans les 3 premières secondes.

## 2. Public cible

| Persona | Besoin | Habitude |
|---|---|---|
| P1 Curieux de faits divers, 18-34 ans | Une histoire prenante en 90 s | Scroll TikTok le soir, aime les séries |
| P2 Fan de mystères inexpliqués | Du fond, des faits vérifiables | Commente, débat sous la vidéo |

## 3. Principe directeur

**Original, vérifié, étiqueté.** Style inspiré, jamais de texte ou d'histoire copiés d'un autre créateur. Chaque fait est vérifiable. Chaque publication porte le label IA de TikTok.

## 4. Format éditorial

Deux formats, choisis avec `--format` :

| Format | Prompt | Structure | Signature |
|---|---|---|---|
| `histoire` | `prompts/narrateur.md` | HOOK (0-3 s), CONTEXTE, ESCALADE (relance toutes les 10 s), CHUTE, FERMETURE | « Dossier clos. Mais l'histoire, elle, reste hors normes. » |
| `top` | `prompts/top.md` | HOOK chiffré, compte à rebours de 3 à 5 entrées, numéro un, FERMETURE | « Dossier clos. Dis-moi ton numéro un en commentaire. » |

Bandeaux à l'écran : « DOSSIER N°X » les 2,5 premières secondes, et « N°3 », « N°2 », « N°1 » pendant chaque entrée d'un top. Le numéro n'est jamais prononcé.
Séries histoires : Disparus, Survivants, Appels au 17, Le détail qui a tout changé, Inexpliqué. Séries tops : Records, Extrêmes, Curiosités, Classements de l'année.
Cadence cible : 1 vidéo par jour au lancement, en alternant histoire et top, 3 à 4 par semaine ensuite.

## 5. Pipeline (identifiants stables F-xx)

| ID | Fonction | Entrée | Sortie |
|---|---|---|---|
| F-01 | Écrire le script et le découper en scènes | sujet ou rien | `histoire.json` |
| F-02 | Synthèse vocale avec timings mot à mot | scènes | `voix.mp3`, `timings.json` |
| F-03 | Images par scène | `image_prompt` | `imgNN.png` |
| F-04 | Animation des 2-3 scènes fortes | image + `motion_prompt` | `clipNN.mp4` ou repli image fixe |
| F-05 | Montage 1080x1920, sous-titres, musique | tout ce qui précède | `final.mp4` |
| F-06 | Fiche de publication | `histoire.json` | `publication.txt` (légende, hashtags, faits à vérifier) |

Règle de repli : une animation qui échoue ne bloque jamais la vidéo.

## 6. Règles métier

- R-01 Script de 170 à 280 mots, 8 à 12 scènes, texte des scènes = script exact.
- R-02 Le hook est la première scène et la première scène est toujours animée.
- R-03 Pas d'affaire récente non jugée, pas d'accusation d'un vivant non condamné, pas de nom complet de victime mineure.
- R-04 Aucun fait inventé présenté comme réel. Incertitude dite à voix haute.
- R-05 Pas de gore détaillé, pas de contenu sexuel, pas de haine.
- R-06 Aucun sujet déjà traité (les dossiers de `out/` font foi).
- R-07 Label « contenu généré par IA » activé à chaque publication.
- R-08 Relecture humaine de `sources_a_verifier` avant de poster.
- R-09 Un top n'affiche que des chiffres exacts, datés et assortis d'un critère de classement. Tout chiffre non vérifié sur une source indépendante est retiré avant le montage.
- R-10 Script de top : 130 à 230 mots, 3 à 5 entrées, le numéro un en dernier.

## 7. Indicateurs de succès

| Indicateur | Cible à 60 jours |
|---|---|
| Rétention à 3 s | supérieure à 70 % |
| Taux de visionnage complet | supérieur à 35 % |
| Vidéos publiées | 50 |
| Abonnés | 5 000 |
| Retraits pour contenu non original | 0 |

## 8. Dépendances

Voir `architecture.md`.

## 9. Backlog

| Priorité | Item |
|---|---|
| P0 | Premier run réel complet avec clés API, choix de la voix |
| P0 | Calibrer le style sur 5 scripts, ajuster `prompts/narrateur.md` |
| P0 | Vérification web automatique des chiffres des tops avant montage |
| P1 | Commande de production par lot (file d'attente de sujets) |
| P1 | Vérification automatique des faits par recherche web avant montage |
| P2 | Miniature/cover générée |
| P2 | Version anglaise pour réutiliser les scripts |
| P2 | Suivi des statistiques TikTok dans `decisions.md` |
