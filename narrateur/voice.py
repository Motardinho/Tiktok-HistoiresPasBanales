import base64
import os
import subprocess
from pathlib import Path


def _duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path.name],
        cwd=path.parent, check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def synthesize_edge(cfg: dict, scenes: list[dict], out_audio: Path) -> dict:
    """Voix de brouillon gratuite (Edge TTS), une scène à la fois.

    Les timings des mots sont estimés au prorata des lettres dans chaque scène.
    """
    import asyncio

    import edge_tts

    v = cfg["voice"]
    work = out_audio.parent
    durations, words, cursor, files = [], [], 0.0, []
    for i, s in enumerate(scenes):
        text = s["narration"].strip()
        part = work / f"voix{i:02d}.mp3"
        if not part.exists():
            asyncio.run(
                edge_tts.Communicate(
                    text, v.get("edge_voice", "fr-FR-HenriNeural"), rate=v.get("edge_rate", "+0%")
                ).save(str(part))
            )
        d = _duration(part)
        tokens = text.split()
        total = sum(len(t) + 1 for t in tokens)
        t0 = cursor
        for tok in tokens:
            span = d * (len(tok) + 1) / total
            words.append({"w": tok, "start": t0, "end": t0 + span})
            t0 += span
        durations.append(d)
        cursor += d
        files.append(part.name)

    (work / "voix_liste.txt").write_text("".join(f"file '{n}'\n" for n in files), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "voix_liste.txt",
         "-c:a", "libmp3lame", "-b:a", "128k", out_audio.name],
        cwd=work, check=True, capture_output=True,
    )
    return {"scene_durations": durations, "words": words, "duration": cursor}


_KEY_FILES = [
    Path(r"C:\Projets\Tiktok - PasSonHeure\montage\.env.voix.local"),
    Path(r"C:\Projets\Moovini\.env.voix.local"),
]


def _api_key() -> str:
    """Clé ElevenLabs : environnement d'abord, sinon fichier local ignoré d'un projet frère. Jamais affichée."""
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for f in _KEY_FILES:
        if f.exists():
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit("ELEVENLABS_API_KEY introuvable (environnement ou .env.voix.local).")


def synthesize(cfg: dict, scenes: list[dict], out_audio: Path) -> dict:
    """Génère la voix pour tout le script et renvoie les timings par scène et par mot."""
    import requests

    v = cfg["voice"]
    texts =[s["narration"].strip() for s in scenes]
    full = " ".join(texts)

    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{v['voice_id']}/with-timestamps",
        params={"output_format": v["output_format"]},
        headers={"xi-api-key": _api_key()},
        json={"text": full, "model_id": v["model_id"], "seed": 7112026,
              "voice_settings": {"stability": v.get("stability", 0.6), "similarity_boost": 0.75}},
        timeout=300,
    )
    r.raise_for_status()
    data = r.json()
    out_audio.write_bytes(base64.b64decode(data["audio_base64"]))

    al = data.get("normalized_alignment") or data["alignment"]
    chars = al["characters"]
    starts = al["character_start_times_seconds"]
    ends = al["character_end_times_seconds"]

    # Timings des scènes : on suit les offsets de caractères du texte envoyé.
    # Les timings normalisés peuvent différer légèrement du texte brut, on se cale sur le ratio.
    total_chars = len(chars)
    scale = total_chars / max(len(full), 1)
    scene_times, cursor = [], 0
    for t in texts:
        a = min(int(cursor * scale), total_chars - 1)
        cursor += len(t) + 1
        b = min(int(cursor * scale) - 1, total_chars - 1)
        scene_times.append((starts[a], ends[max(a, b)]))
    # Aucune coupure noire entre les scènes : chaque scène dure jusqu'au début de la suivante.
    scene_durations = []
    for i, (s, e) in enumerate(scene_times):
        nxt = scene_times[i + 1][0] if i + 1 < len(scene_times) else e
        scene_durations.append(max(nxt - s, 0.8))

    words, cur, w_start = [], "", None
    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            if cur:
                words.append({"w": cur, "start": w_start, "end": last_end})
                cur, w_start = "", None
            continue
        if w_start is None:
            w_start = s
        cur += c
        last_end = e
    if cur:
        words.append({"w": cur, "start": w_start, "end": last_end})

    return {"scene_durations": scene_durations, "words": words, "duration": ends[-1]}
