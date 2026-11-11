# Dossiers Hors Normes — narrateur IA

Pipeline Python qui produit des vidéos TikTok verticales en français, narrées par une voix IA : histoires vraies hors du commun (`--format histoire`) et tops (`--format top`), chacune présentée comme un « dossier » numéroté. Pile : Claude (script), ElevenLabs (voix), OpenAI gpt-image-1 (images), Veo ou Kling (animation), ffmpeg (montage).

## Principe qui commande tout

**Original, vérifié, étiqueté.** Jamais de texte ou d'histoire copiés d'un autre créateur, jamais de fait inventé présenté comme réel, label IA TikTok quand il est vraiment justifié : images ou vidéos réalistes générées par IA, ou voix imitant une personne réelle (détail dans le skill `publier-tiktok`).

## Où chercher

| Besoin | Fichier |
|---|---|
| Besoin, règles métier R-xx, backlog | `docs/prd.md` |
| Dépendances, clés, flux | `docs/architecture.md` |
| Arbitrages datés, questions ouvertes | `docs/decisions.md` |
| Style du narrateur (histoires) | `prompts/narrateur.md` |
| Style des tops | `prompts/top.md` |
| Réglages (voix, modèles, rendu) | `config.yaml` |
| Skills du projet | `.claude/skills/` |

## Pièges

- **Contrôle visuel obligatoire avant montage :** pays, époque, uniformes, insignes, drapeaux et modèles de matériel doivent correspondre au propos. Un drapeau ajouté ne prouve jamais la nationalité d’une unité. Aucun drapeau ou accessoire décoratif inventé. Écarter les images ambiguës ; vérifier provenance et légende, puis contrôler le recadrage dans la vidéo finale. Les illustrations IA restent explicitement des illustrations et ne prouvent aucun fait.

- **Chaque livraison comprend `final.mp4` et `comparaison.mp4`, systématiquement, même après une retouche.** Référence à gauche, HPB à droite, audios séparés et HPB par défaut ; donner les deux liens. Conserver la référence avant production. Une comparaison manquante ou périmée rend la livraison incomplète.

- **Une vidéo avec sous-titres décalés vient des timings.** Les sous-titres et la durée des scènes viennent de `timings.json` (ElevenLabs). Changer le texte d'une scène sans régénérer la voix désynchronise tout.
- **Un top avec un chiffre faux détruit la crédibilité du compte.** Le LLM n'a pas accès au web : tout chiffre, record ou classement se vérifie à la main sur une source avant de poster (R-09).
- **Le numéro de dossier vient du nombre de dossiers dans `out/`.** Supprimer des dossiers fait réutiliser des numéros déjà publiés.
- **Le dossier `out/` fait foi des sujets déjà traités.** Le supprimer fait ressortir les mêmes histoires.
- **ffmpeg tourne avec `cwd` = dossier de la vidéo et des noms relatifs.** Passer des chemins absolus Windows dans le filtre `ass` casse silencieusement (échappement du `:`).
- **Les étapes sont idempotentes.** Pour refaire une image ou un clip, supprimer le fichier, pas le dossier.
- **Les API vidéo changent vite.** Un échec d'animation retombe sur l'image fixe sans erreur bloquante : lire la sortie console pour le voir.
- **Aucune clé n'est dans le dépôt.** `.env` seulement, jamais versionné.
