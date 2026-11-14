from concurrent.futures import ThreadPoolExecutor
from html import escape
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

DEST = Path(__file__).resolve().parent
OUT = DEST.parent
IDENTITY = OUT.parent / "identite/histoires-pas-banales"
FONT = Path("C:/Windows/Fonts")
INK = "#10141c"
YELLOW = "#ffe34e"
WHITE = "#fffaf1"
SIZE = (1080, 1920)
BRAND = Image.open(IDENTITY / "logos/logo-horizontal-sombre.png").convert("RGBA")
BRAND = BRAND.crop(BRAND.getbbox())
BRAND.thumbnail((590, 153), Image.Resampling.LANCZOS)

# Motifs, styles et palettes choisis selon le sujet.
THEMES = {
    "espace": ("#38e4ff", "#7866ff", "#a4e8ff", "Orbite", "Mission", "Laboratoire"),
    "vitesse": ("#ff512f", "#ffe456", "#56e5ff", "Racing", "Chrono", "Piste"),
    "geo": ("#31e8bb", "#ffbe56", "#69caff", "Atlas", "Vue aérienne", "Grand angle"),
    "nature": ("#b6f957", "#ffb756", "#74d6ac", "Instinct", "Terrain", "Documentaire"),
    "tech": ("#bcff28", "#b993ff", "#45eaff", "Acide", "Studio", "Tech"),
    "cinema": ("#ff5040", "#ffcb56", "#ff9fe4", "Affiche", "Cascade", "Pellicule"),
    "enquete": ("#ff4d60", "#ffd857", "#a7caff", "Alerte", "Dossier", "Enquête"),
    "foot": ("#8ef456", "#ff6262", "#62ccff", "Stade", "Score", "Tribune"),
    "mer": ("#45ddff", "#ffab54", "#80f3db", "Tempête", "Survie", "Horizon"),
    "jeu": ("#b58aff", "#ffcf69", "#56ecc1", "Échec", "Stratégie", "Échiquier"),
}
TOPICS = dict(zip(range(13, 45), """
espace vitesse geo enquete nature geo cinema tech geo geo geo espace vitesse
nature mer enquete enquete foot enquete enquete foot jeu vitesse vitesse enquete
foot foot foot foot foot vitesse foot
""".split(), strict=True))


def font(filename, size):
    return ImageFont.truetype(str(FONT / filename), size)


def wrap(draw, text, face, width):
    lines = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and draw.textlength(candidate, font=face) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + [line]


def source(folder, number):
    special = {
        20: "miniature-essai/B1-photo-entiere-titre-bas.jpg",
        31: "miniature-essai/E1-diagonale-bleus-cagoule.jpg",
        44: "miniature-v2.jpg",
    }
    if number in special and (folder / special[number]).exists():
        frame = Image.open(folder / special[number]).convert("RGB")
    else:
        movie = folder / "final.mp4"
        time = "0.72" if number == 14 else "0.34"
        frame_bytes = subprocess.check_output([
            "ffmpeg", "-v", "error", "-threads", "1", "-ss", time, "-i", str(movie),
            "-frames:v", "1", "-threads", "1", "-f", "image2pipe", "-vcodec", "png", "-"
        ])
        frame = Image.open(BytesIO(frame_bytes)).convert("RGB")
    frame = ImageOps.fit(frame, SIZE)
    top = {16: 493, 23: 470, 33: 452, 40: 565, 44: 425}.get(number, 360)
    bottom = {16: 1000, 23: 985, 33: 1057, 40: 1090, 44: 1135}.get(number, 965)
    return frame.crop((0, top, 1080, bottom))


def motif(draw, theme, color):
    if theme in {"espace", "tech", "geo"}:
        for offset in (0, 25, 50):
            draw.arc((680-offset, 990-offset, 1190+offset, 1500+offset),
                     20, 335, fill=color, width=2)
    elif theme in {"vitesse", "cinema", "enquete"}:
        for x in range(770, 1150, 42):
            draw.line((x, 1510, x-250, 1900), fill=color, width=3)
    elif theme == "foot":
        draw.arc((610, 1175, 1320, 1885), 90, 270, fill=color, width=3)
        draw.line((790, 1530, 1080, 1530), fill=color, width=3)
    elif theme == "jeu":
        for i in range(8):
            for j in range(3):
                if (i+j) % 2:
                    x, y = 680+50*i, 1590+50*j
                    draw.rectangle((x,y,x+28,y+28), fill=color)
    else:
        for i in range(5):
            draw.arc((570, 1450+i*25, 1180, 1770+i*25), 190, 350,
                     fill=color, width=2)


def compose(photo, title, series, theme, palette, style):
    accent = palette[style]
    canvas = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(canvas)
    motif(draw, theme, "#313c4e")
    if style == 0:
        canvas.paste(ImageOps.fit(photo, (1080, 730)), (0, 310))
        draw.polygon([(0, 1035), (1080, 944), (1080, 1001), (0, 1092)], fill=accent)
        family, align, title_y = "impact.ttf", "left", 1100
    elif style == 1:
        draw.rectangle((63, 351, 1017, 1008), fill=accent)
        canvas.paste(ImageOps.fit(photo, (924, 627)), (78, 366))
        draw.line((74, 1051, 1006, 1051), fill=accent, width=5)
        family, align, title_y = "segoeuib.ttf", "center", 1112
    else:
        canvas.paste(ImageOps.fit(photo, (1080, 676)), (0, 321))
        draw.polygon([(0, 950), (1080, 1000), (1080, 1050), (0, 998)], fill=accent)
        draw.rectangle((80, 1070, 93, 1510), fill=accent)
        family = "georgiab.ttf" if theme in {"enquete", "mer", "nature", "geo", "jeu"} else "arialbd.ttf"
        align, title_y = "left", 1095

    canvas.paste(BRAND, (80, 92), BRAND)
    badge = font("arialbd.ttf", 44)
    draw.rounded_rectangle((866, 103, 1000, 167), radius=12, outline=WHITE, width=3)
    draw.text((933, 135), "HPB", anchor="mm", font=badge, fill=WHITE)
    draw.rectangle((80, 259, 1000, 319), fill="#232c38")
    draw.rectangle((80, 259, 87, 319), fill=YELLOW)
    series_size = 36
    while draw.textlength(series, font=font("arialbd.ttf", series_size)) > 865:
        series_size -= 1
    draw.text((105, 289), series, anchor="lm", font=font("arialbd.ttf", series_size), fill=YELLOW)

    start_x = 112 if style == 2 else 83
    for size in range(132 if style == 0 else 114, 48, -2):
        face = font(family, size)
        lines = wrap(draw, title, face, 868)
        if (len(lines) <= 4 and len(lines) * (size+14) <= 520
                and all(draw.textlength(line, font=face) <= 868 for line in lines)):
            break
    line_height = size + 14
    for index, line in enumerate(lines):
        last = index == len(lines)-1
        y = title_y + index * line_height
        x = 540 if align == "center" else start_x
        anchor = "mt" if align == "center" else "lt"
        if style == 0 and last:
            w = draw.textlength(line, font=face)
            draw.rectangle((x-11, y-12, x+w+12, y+size+15), fill=accent)
        color = INK if style == 0 and last else accent if last else WHITE
        draw.text((x, y), line, anchor=anchor, font=face, fill=color)
    return canvas


def build(folder):
    number = int(folder.name.split("-")[0])
    info = json.loads((folder / "histoire.json").read_text(encoding="utf-8-sig"))
    title = (info.get("titre_fixe") or info["titre"]).upper()
    series = (info.get("serie") or info["titre"]).upper()
    theme = TOPICS[number]
    colors = THEMES[theme]
    photo = source(folder, number)
    target = DEST / folder.name
    target.mkdir(exist_ok=True)
    cards = []
    for index, name in enumerate(colors[3:]):
        path = target / f"{index+1}-{name.lower().replace(' ', '-')}.jpg"
        compose(photo, title, series, theme, colors, index).save(path, quality=94, subsampling=0)
        cards.append((name, path.relative_to(DEST).as_posix()))
    return number, title, cards


folders = sorted(p for p in OUT.iterdir() if p.is_dir() and p.name[:2].isdigit()
                 and (p / "histoire.json").is_file())
with ThreadPoolExecutor(max_workers=5) as pool:
    rows = list(pool.map(build, folders))

sections = []
for number, title, cards in rows:
    items = "".join(f'<a href="{escape(path)}"><img loading="lazy" src="{escape(path)}" '
                    f'alt="{escape(title)} - {escape(name)}"><span>{escape(name)}</span></a>'
                    for name, path in cards)
    sections.append(f'<section id="video-{number}"><h2>{number} - {escape(title)}</h2>'
                    f'<div class="cards">{items}</div></section>')
nav = " ".join(f'<a href="#video-{n}">{n}</a>' for n, _, _ in rows)
html = """<!doctype html><html lang="fr"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>96 miniatures - Histoires pas banales</title>
<style>body{margin:30px auto;padding:0 18px;max-width:1100px;background:#10141c;color:#fffaf1;
font:16px system-ui}a{color:inherit;text-decoration:none}nav{display:flex;gap:8px;flex-wrap:wrap}
nav a{padding:6px 10px;background:#262d3d;border-radius:6px}section{padding:24px 0;border-bottom:1px solid #343a47}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
img{width:100%;aspect-ratio:9/16;display:block;border-radius:8px}span{display:block;margin-top:8px}
h2{font-size:18px}a:hover span,nav a:hover{color:#ffe34e}</style>
<h1>96 miniatures - Histoires pas banales</h1><nav>""" + nav + "</nav>" + "".join(sections)
(DEST / "galerie.html").write_text(html, encoding="utf-8")

for start in range(0, len(rows), 8):
    board = Image.new("RGB", (1728, 800), "#232c38")
    for slot, (_, _, cards) in enumerate(rows[start:start+8]):
        for index, (_, path) in enumerate(cards):
            image = Image.open(DEST / path).resize((144, 256), Image.Resampling.LANCZOS)
            board.paste(image, ((slot % 4)*432+index*144, (slot//4)*400+30))
        ImageDraw.Draw(board).text(((slot % 4)*432+12, (slot//4)*400+303),
                                    str(rows[start+slot][0]), font=font("arialbd.ttf", 34), fill=WHITE)
    board.save(DEST / f"controle-{start//8+1}.jpg", quality=92)
print(f"{len(rows)} vidéos, {sum(len(cards) for _, _, cards in rows)} miniatures")
