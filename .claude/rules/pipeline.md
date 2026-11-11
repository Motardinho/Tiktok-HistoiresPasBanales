---
paths:
  - "narrateur/**/*.py"
  - "config.yaml"
  - ".env.example"
---

# Règles du pipeline

- Toute étape qui appelle une API payante vérifie d'abord si son fichier de sortie existe, car on ne repaie pas une image ou un clip.
- Une animation qui échoue renvoie `None` et ne lève pas, car le pipeline ne doit jamais bloquer sur une API vidéo.
- Les clés viennent de l'environnement (`os.environ`), jamais d'un fichier versionné ni de `config.yaml`.
- ffmpeg s'exécute avec `cwd` = dossier de travail et des noms de fichiers relatifs, car l'échappement des chemins Windows casse le filtre `ass`.
- Toute nouvelle dépendance se propose et s'ajoute au tableau de `docs/architecture.md` avant `requirements.txt`.
- Tester le montage sans clé API avec une image et un son synthétiques avant de lancer un run payant.
