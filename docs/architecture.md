# Architecture

## Pile

Python 3.12, ffmpeg 9 (local, Windows). Pas de base de données : tout est fichier dans `out/<slug>/`.

## Dépendances autorisées

| Besoin | Paquet / service | Pourquoi | Écarté |
|---|---|---|---|
| Écriture du script | `anthropic`, modèle `claude-sonnet-5-5` | Qualité du français et du rythme oral | — |
| Voix | ElevenLabs API `with-timestamps` | Expressivité, timings par caractère pour les sous-titres | Edge TTS (trop plat) |
| Images | `openai`, `gpt-image-1` | Choix de l'utilisateur, bon rendu cinématographique | — |
| Animation | `google-genai` (Veo) ou API Kling | Choix de l'utilisateur, au choix dans `config.yaml` | — |
| Auth Kling | `PyJWT` | Jeton HS256 exigé par l'API | — |
| Config | `PyYAML`, `python-dotenv` | Simple | — |
| Montage | ffmpeg en sous-processus | Contrôle total, aucun surcoût | MoviePy (lent, fragile) |
| Tampon « DOSSIER CLOS » | `Pillow`, `numpy` | Image du tampon fabriquée par `narrateur/tampon.py` (cadre arrondi, encre usée) | Texte ASS (rendu trop plat) |
| Voix de brouillon | `edge-tts` | Mode `--brouillon` sans clé | — |

## Dépendances interdites

| Dépendance | Motif |
|---|---|
| Voix clonée d'une personne réelle | Droit à la voix et conditions TikTok |
| Scraping de vidéos ou scripts d'autres créateurs | Contenu non original |
| Musique non libre de droits | Retrait TikTok |

**Règle d'ajout** : toute dépendance non listée se propose avant de s'installer.

## Frontières externes

| Frontière | Variable | Notes |
|---|---|---|
| Anthropic | `ANTHROPIC_API_KEY` | |
| ElevenLabs | `ELEVENLABS_API_KEY`, `voice_id` dans `config.yaml` | Identifiant de voix, pas un secret |
| OpenAI | `OPENAI_API_KEY` | |
| Gemini / Veo | `GEMINI_API_KEY` | |
| Kling | `KLING_ACCESS_KEY`, `KLING_SECRET_KEY` | |

Secrets dans `.env` uniquement, jamais versionné.

## Flux

`story.py` → `voice.py` (timings) → `images.py` → `video.py` (optionnel) → `assemble.py` → `final.mp4`.
Les étapes sont idempotentes : un fichier déjà présent n'est pas régénéré (économie d'API).

## Pièges connus

- ffmpeg est lancé avec `cwd` = dossier de travail et des noms relatifs, pour éviter l'échappement des chemins Windows dans le filtre `ass`.
- Les timings ElevenLabs peuvent être normalisés différemment du texte brut : le calage des scènes se fait par ratio de caractères (`voice.py`).
