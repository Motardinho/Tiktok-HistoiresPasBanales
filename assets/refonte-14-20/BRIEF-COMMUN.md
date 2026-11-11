# Brief commun - refonte des vidéos 14 à 20 (9 novembre 2026)

Projet : `C:\Projets\Tiktok - MrBallen` (Windows, PowerShell, python 3.12, ffmpeg/ffprobe et `python -m yt_dlp` installés). Compte TikTok « Histoires pas banales » : vidéos verticales en français, voix de synthèse, plans vidéo RÉELS plein écran.

Marc demande de refaire entièrement cette vidéo : script, voix, images, montage. L'agent principal écrit le script, synthétise la voix et monte. **Toi, tu livres des FAITS REVÉRIFIÉS aujourd'hui et des PLANS VIDÉO RÉELS téléchargés et contrôlés.** Tu n'écris pas le script et tu ne touches à rien dans `out/` (lecture seule) ni ailleurs que ton dossier de sortie.

## Point de départ à lire

- Le dossier existant de la vidéo dans `out/` : `histoire.json` (script actuel, fun fact, référence), `script.txt`, `CREDITS.md`, les fichiers `verification*.md` s'il y en a.
- Les règles du compte : `.claude/skills/produire-video/references-hpb.md` (lis en entier ; plusieurs paragraphes concernent précisément ton sujet).
- Les sources déjà téléchargées (indiquées dans ta mission) : réutilise celles qui sont bonnes et correctement licenciées, complète le reste.

## Partie 1 - faits : `verification.md` dans ton dossier de sortie

- Revérifie sur le web, auprès des sources primaires, CHAQUE chiffre, nom, date et classement du script actuel. Nous sommes le 9 novembre 2026 : signale tout ce qui a changé ou qui est faux, et tout piège de formulation.
- Pour chaque fait : valeur, année réelle des données, source, URL. Écris « non vérifié » si tu ne trouves pas. Aucune invention.
- Propose 4 à 6 fun facts concrets, surprenants, montrables en vidéo, chacun rattaché à une entrée du classement (ou au sujet pour une histoire), avec source identifiable. Dis lesquels ont un plan raccord dans ton catalogue.

## Partie 2 - plans vidéo réels

Règles : VIDÉO RÉELLE par défaut (pas de photo, pas d'image IA, pas de rendu 3D présenté comme réel), plein écran 9:16 par recadrage d'une source paysage ou source portrait native. Images spectaculaires, pas scolaires : ni carte, ni tableau, ni schéma. Chaque plan doit montrer réellement ce que la narration dira au même moment : bon sujet, bon modèle, bon pays, bonne époque, bonne action (un animal qui court pour un sprint, la bonne voiture, la bonne ville). Vérifie titre, description et légende de chaque source ; n'attribue jamais une image générique à un sujet précis. Aucun drapeau ni accessoire ajouté.

Licences acceptées uniquement, à documenter par fichier : Wikimedia Commons (CC BY, CC BY-SA, CC0, domaine public), vidéos YouTube dont le champ `license` de yt-dlp vaut « Creative Commons Attribution license (reuse allowed) » (à vérifier dans le `.info.json` ; écarte les chaînes qui ré-uploadent manifestement le contenu d'autrui), Pexels / Pixabay / Mixkit / Coverr, agences publiques dont le contenu est dans le domaine public (NASA, armée américaine via DVIDS, etc.). Rien d'autre. Si une source déjà présente dans le projet n'entre pas dans ces licences, dis-le clairement dans ton rapport.

Besoin : de quoi couvrir environ 75 s de montage avec des plans de 2 à 5 s, sans répéter un extrait :
- 1 à 2 plans d'accroche spectaculaires, lisibles sans son, qui ne révèlent aucune entrée d'un top ;
- pour CHAQUE entrée du classement (ou chaque étape de l'histoire) : 6 à 8 plans distincts, identifiables, en mouvement, sous des angles variés ;
- un plan raccord pour chaque fun fact proposé, si possible.

Téléchargement : 1080p de préférence (720p accepté), mp4 h264 (`-f "bv*[height<=1080][vcodec^=avc1]+ba[ext=m4a]/b[height<=1080]" --write-info-json` pour yt-dlp), nom `<slug>.mp4`. Environ 8 à 16 fichiers, aucun au-delà de ~400 Mo (utilise `--download-sections` pour les sources longues). Wikimedia limite les requêtes : espace-les et mets un User-Agent générique du type `HistoiresPasBanales/1.0 editorial research`.

CONTRÔLE VISUEL OBLIGATOIRE : pour chaque source, génère des planches-contact horodatées avec ffmpeg (une image toutes les 2 à 5 s, avec le cadre 9:16 conseillé tracé) et REGARDE-LES avec l'outil Read avant de cataloguer. Vérifie que les horodatages affichés sont exacts (extrais 2 ou 3 images isolées pour contrôler). Écarte les plans flous, tremblés, dominés par un intervenant, ou portant un logo, un filigrane ou un texte incrusté dans le cadre 9:16.

## Livrables dans ton dossier de sortie

1. `verification.md`.
2. `sources.json` : liste `{fichier, url_page, auteur, titre, licence, url_licence, lieu_et_sujet_verifies, preuve}`. Mets dans `licence` un libellé court (ex. « CC BY 3.0 », « Licence Pexels », « Domaine public - NASA »).
3. `catalogue.json` : liste `{fichier, debut_s, fin_s, description, entree (nom de l'entrée du classement, ou "accroche", ou l'étape de l'histoire), centre_x (fraction 0-1 du centre horizontal du recadrage 9:16, ou "portrait"), zone (filtre ffmpeg crop=... si la source a des bandes noires, sinon vide), remarques}`. Seulement des plans réellement vus ; bornes exactes à ~0,5 s, à l'intérieur d'un même plan (pas de coupe ni de fondu dedans).
4. Les planches-contact (`<slug>-reperage.jpg`).

Rapport final court : faits confirmés ou corrigés avec source et année, les 3 meilleurs fun facts, nombre de plans par entrée, et toutes les faiblesses (entrée mal couverte, doute de licence, d'identification ou d'horodatage). Ne prétends rien que tu n'as pas vérifié toi-même.
