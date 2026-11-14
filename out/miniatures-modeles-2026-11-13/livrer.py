import json
import subprocess
from html import escape
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
rows = json.loads((ROOT / "catalogue.json").read_text(encoding="utf-8"))
cards = []
for row in rows:
    number = row["number"]
    path = ROOT / "final" / f"{number}.png"
    if not path.exists():
        continue
    cards.append(f'<a href="final/{number}.png"><img src="final/{number}.png" loading="lazy">'
                 f'<p>{number} - {escape(row["title"])}<br><small>{row["style"]}</small></p></a>')
html = ('<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>Miniatures HPB</title>'
        '<style>body{background:#11151c;color:#f8f6ec;font:16px system-ui;margin:24px}'
        'main{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}'
        'a{color:inherit;text-decoration:none}img{width:100%;border-radius:6px}small{color:#ffe24a}'
        '</style><h1>Miniatures HPB</h1><main>' + ''.join(cards) + '</main></html>')
(ROOT / "galerie.html").write_text(html, encoding="utf-8")
files = sorted((ROOT / "final").glob("*.png"))
for start in range(0, len(files), 8):
    group = files[start:start+8]
    command = ["ffmpeg", "-v", "error", "-y"]
    for path in group:
        command.extend(["-i", str(path)])
    filters = [f"[{i}:v]scale=270:480[s{i}]" for i in range(len(group))]
    inputs = "".join(f"[s{i}]" for i in range(len(group)))
    layout = "|".join(f"{(i%4)*270}_{(i//4)*480}" for i in range(len(group)))
    filters.append(f"{inputs}xstack=inputs={len(group)}:layout={layout}")
    command.extend(["-filter_complex", ";".join(filters), "-frames:v", "1",
                    str(ROOT / f"planche-{start//8+1}.jpg")])
    subprocess.run(command, check=True)
with ZipFile(ROOT / "miniatures-hpb.zip", "w") as archive:
    for path in files + [ROOT / "galerie.html"]:
        archive.write(path, path.relative_to(ROOT))
print(f"{len(files)} miniatures dans la galerie")
