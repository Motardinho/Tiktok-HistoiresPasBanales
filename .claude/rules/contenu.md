---
paths:
  - "prompts/**/*.md"
  - "narrateur/story.py"
  - "out/**/histoire.json"
---

# Règles éditoriales

- Tout script fait entre 170 et 280 mots et 8 à 12 scènes, car au-delà la rétention TikTok chute.
- La première scène est le hook, animée, sans salutation, car les 3 premières secondes décident du visionnage.
- Aucune affaire récente non jugée, aucune accusation d'une personne vivante non condamnée, car risque de diffamation.
- Aucun nom complet de victime mineure, car protection des personnes.
- Chaque fait clé figure dans `sources_a_verifier`, car un LLM peut se tromper sur les détails.
- Ne jamais reprendre le texte ni l'histoire d'un autre créateur, car le compte serait retiré pour contenu non original.
- Toute modification du prompt narrateur qui change le style ou la structure se consigne dans `docs/decisions.md`.
