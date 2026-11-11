"""Animation d'une image en clip court (image-to-video).

Les API vidéo évoluent vite : les noms de modèles et champs ci-dessous sont à valider
sur ton compte au premier essai (voir README).
"""
import os
import time
from pathlib import Path


def animate(cfg: dict, image: Path, motion_prompt: str, out: Path) -> Path | None:
    if out.exists():
        return out
    provider = cfg["video"]["provider"]
    try:
        if provider == "veo":
            return _veo(cfg, image, motion_prompt, out)
        if provider == "kling":
            return _kling(cfg, image, motion_prompt, out)
        raise ValueError(f"Fournisseur vidéo inconnu : {provider}")
    except Exception as e:  # une animation ratée ne doit pas bloquer la vidéo, on retombe sur l'image
        print(f"  ! animation échouée ({provider}) : {e} -> image fixe")
        return None


def _veo(cfg, image, prompt, out):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    op = client.models.generate_videos(
        model=cfg["video"]["veo_model"],
        prompt=prompt + ". Cinematic, dark, subtle motion, no text.",
        image=types.Image(image_bytes=image.read_bytes(), mime_type="image/png"),
        config=types.GenerateVideosConfig(aspect_ratio="9:16"),
    )
    while not op.done:
        time.sleep(10)
        op = client.operations.get(op)
    video = op.response.generated_videos[0]
    client.files.download(file=video.video)
    video.video.save(str(out))
    return out


def _kling_headers():
    import jwt

    now = int(time.time())
    token = jwt.encode(
        {"iss": os.environ["KLING_ACCESS_KEY"], "exp": now + 1800, "nbf": now - 5},
        os.environ["KLING_SECRET_KEY"],
        algorithm="HS256",
        headers={"alg": "HS256", "typ": "JWT"},
    )
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _kling(cfg, image, prompt, out):
    import base64

    import requests

    base ="https://api.klingai.com/v1/videos/image2video"
    body = {
        "model_name": cfg["video"]["kling_model"],
        "image": base64.b64encode(image.read_bytes()).decode(),
        "prompt": prompt,
        "duration": str(cfg["video"]["clip_seconds"]),
        "aspect_ratio": "9:16",
        "mode": "std",
    }
    r = requests.post(base, headers=_kling_headers(), json=body, timeout=120)
    r.raise_for_status()
    task_id = r.json()["data"]["task_id"]
    while True:
        time.sleep(10)
        s = requests.get(f"{base}/{task_id}", headers=_kling_headers(), timeout=60).json()["data"]
        if s["task_status"] == "succeed":
            url = s["task_result"]["videos"][0]["url"]
            out.write_bytes(requests.get(url, timeout=300).content)
            return out
        if s["task_status"] == "failed":
            raise RuntimeError(s.get("task_status_msg", "kling failed"))
