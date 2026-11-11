"""Tampon encreur « DOSSIER CLOS » : cadre arrondi, texte condensé, rouge usé, incliné.

L'image est fabriquée une fois (graine fixe, donc toujours la même) puis posée par ffmpeg
avec une animation d'écrasement (voir assemble.py).
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RED = (200, 22, 32)


def make_stamp(out: Path, text: str = "DOSSIER CLOS", angle: float = 17.0, seed: int = 7) -> Path:
    if out.exists():
        return out
    font_path = ROOT / "assets" / "fonts" / "BebasNeue-Regular.ttf"
    font = ImageFont.truetype(str(font_path), 250)
    tw = int(font.getlength(text))
    w, h = tw + 150, 380
    img = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=46, outline=255, width=20)
    d.rounded_rectangle((40, 40, w - 40, h - 40), radius=26, outline=255, width=5)
    d.text((w / 2, h / 2 + 8), text, font=font, fill=255, anchor="mm")

    # encre usée : taches claires dispersées et fines éraflures
    rng = np.random.default_rng(seed)
    mask = np.array(img, dtype=np.float32) / 255
    noise = rng.random(mask.shape)
    blotch = np.array(Image.fromarray((noise * 255).astype("uint8")).resize(
        (w // 6, h // 6)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255
    wear = (noise > 0.965) | (blotch > 0.7)
    mask[wear] *= 0.0
    art = Image.fromarray((mask * 255).astype("uint8"))
    d2 = ImageDraw.Draw(art)
    for _ in range(18):
        x, y = rng.integers(0, w), rng.integers(0, h)
        d2.line((x, y, x + rng.integers(-90, 90), y + rng.integers(-14, 14)), fill=0, width=int(rng.integers(1, 3)))

    pad = 24
    canvas = (w + 2 * pad, h + 2 * pad)
    ink = Image.new("L", canvas, 0)
    ink.paste(art, (pad, pad))
    shadow = ink.filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * 0.55))
    out_img = Image.new("RGBA", canvas, (0, 0, 0, 0))
    black = Image.new("RGBA", canvas, (0, 0, 0, 255))
    black.putalpha(shadow)
    out_img.alpha_composite(black, (5, 8))
    red = Image.new("RGBA", canvas, RED + (255,))
    red.putalpha(ink)
    out_img.alpha_composite(red)
    out_img = out_img.rotate(angle, expand=True, resample=Image.BICUBIC)
    out_img.save(out)
    return out
