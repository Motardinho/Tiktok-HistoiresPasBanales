import base64
import subprocess
from pathlib import Path

STYLE = (
    "Cinematic dark documentary photography, moody lighting, film grain, "
    "vertical 9:16 composition, no text, no watermark, no recognizable faces. "
)


PALETTES = [("0x0b1d3a", "0x1e6fd9"), ("0x2a0a3d", "0xc2338a"), ("0x062a2a", "0x14b8a6"),
            ("0x3a1205", "0xf59e0b"), ("0x111827", "0x6366f1")]


def card(cfg: dict, index: int, out: Path) -> Path:
    """Fond dégradé généré par ffmpeg, pour le mode brouillon sans API d'images."""
    if out.exists():
        return out
    c0, c1 = PALETTES[index % len(PALETTES)]
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i",
         f"gradients=s=1080x1920:c0={c0}:c1={c1}:seed={index + 3}:speed=0",
         "-frames:v", "1", out.name],
        cwd=out.parent, check=True, capture_output=True,
    )
    return out


def generate_image(cfg: dict, prompt: str, out: Path) -> Path:
    if out.exists():
        return out
    from openai import OpenAI

    c = cfg["images"]
    res = OpenAI().images.generate(
        model=c["model"], prompt=STYLE + prompt, size=c["size"], quality=c["quality"]
    )
    out.write_bytes(base64.b64decode(res.data[0].b64_json))
    return out
