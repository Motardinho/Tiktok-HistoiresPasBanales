# Gabarits fixes HPB

Cinq sources éditables : `pop.json`, `racing.json`, `sticker.json`, `magazine.json`, `science.json`. Chaque source fixe la police, les couleurs, les coordonnées, les dimensions, l'inclinaison, les bandes et leurs décalages. Les SVG et PNG transparents correspondants sont dans `exports/`.

Les références originales sont des images aplaties générées : aucune police source n'est identifiable avec certitude. Cette reconstruction utilise Russo One pour pop, Anton pour racing/science/magazine, Poppins Black pour sticker, Archivo Black pour « BRAQUÉ », Poppins ExtraBold pour le logo. Ce sont des rapprochements visuels figés, pas des polices originales certifiées. Ne pas déclarer ces nouveaux gabarits approuvés avant le retour de Marc.

Le logo est un masque vectoriel jaune avec évidement HPB : les lettres sont réellement transparentes. Aucun filtre, ombre ou bandeau. Les caractères des titres sont convertis en tracés pour que le rendu ne dépende pas des polices installées sur la machine qui ouvre le SVG.

## Rendu

Python avec `fonttools==4.68.0` et `resvg-py==0.5.0`.

```powershell
python render.py --all
python render.py --config animaux.json --background fond.png --out animaux-racing
```

La seconde commande produit un SVG autonome contenant la photo et un PNG 1080×1920. Copier le JSON d'un modèle pour adapter le titre ; conserver les réglages de style. `rows` définit les lignes et leur composition. Ne pas lancer `--all` pour changer une seule couverture. Aucun appel IA n'est utilisé par le renderer.

Le fond doit être déjà sans texte et sans logo. L'image est cadrée en remplissage centré. Le modèle racing s'applique notamment aux animaux rapides selon le choix explicite de Marc. Ne pas réinventer les couleurs, les ombres ou les caractères par génération d'image. Comparer le rendu à la référence et le vérifier à 360 pixels de large.

Révision des cinq gabarits : couleurs échantillonnées dans les références ; positions et polygones des bandes recalés ; graisse et approche ajustables ; hauteur mesurée sur H pour éviter que les accents et la queue du Q écrasent les capitales. Comparaison à échelle constante dans comparaison/. Les contours précis de certaines lettres restent des approximations typographiques ; ne pas annoncer une identité parfaite.


## Révision V3 : contours de racing et Pogba

Pour racing et magazine, `lettres-reference.json` remplace les polices de substitution sur les lignes de référence. `tracer_lettres.py` reconstruit ces contours à partir des références inchangées (OpenCV et NumPy nécessaires uniquement à cette extraction). Les exports sont de vrais tracés SVG, pas des captures de titres superposées. Les contours ont un léger lissage, les photos, textures et ombres des références ne font pas partie du lettrage.

La bibliothèque contient seulement les caractères visibles dans les références, répartis en alphabets racing-display, racing-text, magazine-tall et magazine-block. Un nouveau texte comportant un caractère absent est refusé avec un message explicite : compléter son dessin avant déclinaison, ne pas utiliser silencieusement une police de remplacement. Ne pas présenter ces sous-ensembles comme des polices complètes. Les autres styles gardent leurs réglages V2.

## Révision V4 : les cinq styles vectorisés

Les 16 lignes des cinq références utilisent désormais `lettres-reference.json` : Pop, Sticker et Science rejoignent Racing et Magazine. Aucun de ces titres de référence n'est composé avec une police de substitution. Les polices locales restent disponibles pour les autres éléments de l'outil, mais ne remplacent pas les glyphes tracés manquants.

Contours extraits de zones contrôlées, contreformes préservées, accents et point du point d'interrogation inclus. Les lettres E et A de PLUS BEAUX qui se touchent sont séparées en composants pour le réemploi sans supprimer de pixels du contour de la ligne. Les bandes Science ont été recalées dans les coordonnées de la référence : le texte source inclut déjà sa rotation. Le moteur garde une limite explicite : alphabets partiels, caractères absents à dessiner avant nouveaux titres.
