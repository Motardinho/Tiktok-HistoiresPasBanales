# Dossiers Hors Normes – narrateur IA d'histoires et de tops en français (TikTok)

Pipeline qui produit une vidéo verticale 1080x1920 prête à poster, en une commande.

| Étape | Outil | Fichier |
|---|---|---|
| Script + découpage en scènes | Claude | `narrateur/story.py`, `prompts/narrateur.md` |
| Voix + timings mot à mot | ElevenLabs | `narrateur/voice.py` |
| Images | OpenAI `gpt-image-1` | `narrateur/images.py` |
| Animation des 2-3 scènes fortes | Veo (Gemini) ou Kling | `narrateur/video.py` |
| Montage, sous-titres, musique | ffmpeg | `narrateur/assemble.py` |

## Installation

```bash
pip install -r requirements.txt
copy .env.example .env
```

Remplis `.env` (clés API) et `voice_id` dans `config.yaml`.

## Utilisation

```bash
python -m narrateur --sujet "la disparition de l'équipage du Mary Celeste"
python -m narrateur --format top --sujet "les voitures de série les plus rapides en 2026"
python -m narrateur --script-seulement          # juste le script, pour valider avant de payer voix/images
python -m narrateur --dossier <nom> --sans-video  # reprendre un dossier, sans clips animés
```

Tout est écrit dans `out/<titre>/` : `histoire.json`, `voix.mp3`, `final.mp4`, `publication.txt` (légende, hashtags, faits à vérifier). Les étapes déjà faites (images, clips) ne sont pas refaites.

## À valider au premier essai

- **ElevenLabs** : j'ai mis `eleven_v3` dans `config.yaml`. Si tu as accès à un modèle plus récent, change `model_id`. Choisis une voix grave et posée, et teste-la sur un script avant de produire en série.
- **Veo / Kling** : les noms de modèles et champs d'API changent souvent. Si une animation échoue, la vidéo retombe automatiquement sur l'image avec un zoom lent, donc rien ne bloque.
- Le code n'a pas été exécuté avec de vraies clés API : lance d'abord `--script-seulement`, puis une vidéo complète.

## Avant de publier

- **Étiquette IA** : TikTok impose d'activer le label « contenu généré par IA » pour les voix et images synthétiques. Fais-le à chaque publication.
- **Faits** : relis `sources_a_verifier` dans `publication.txt`. Le narrateur est calé pour éviter les affaires récentes non jugées, mais un LLM peut se tromper sur des détails.
- **Originalité** : le style est inspiré, les histoires et les textes sont originaux. Ne recopie jamais une histoire d'un autre créateur : c'est la meilleure façon de se faire retirer le compte pour contenu non original.
- **Monétisation** : TikTok favorise les contenus originaux et pénalise la production de masse identique. Soigne le hook et varie les formats.

## Idées de séries

« Disparus », « Survivants », « Appels au 17 », « Le détail qui a tout changé », « Inexpliqué ».
