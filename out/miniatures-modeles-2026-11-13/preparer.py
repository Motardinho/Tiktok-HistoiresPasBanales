import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent
(DEST / "sources").mkdir(exist_ok=True)
styles = {
    "racing": [14, 19, 25, 35],
    "affaire": [16, 26, 27, 28, 29, 30, 32, 34, 36, 37, 38, 39],
    "pop": [20, 41],
    "sticker": [17, 33, 44],
    "science": [13, 15, 18, 21, 22, 23],
}
def prepare(folder):
    number = int(folder.name.split("-")[0])
    if number in [24, 31, 40, 42, 43]:
        return None
    info = json.loads((folder / "histoire.json").read_text(encoding="utf-8-sig"))
    path = DEST / "sources" / f"{number}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(folder / "final.mp4"),
                    "-frames:v", "1", "-threads", "1", str(path)], check=True)
    return dict(number=number, folder=folder.name,
                title=info.get("titre_fixe") or info["titre"],
                banner=info.get("serie") or info["titre"],
                style=next(k for k,v in styles.items() if number in v),
                source=str(path), validated=(folder / "validation-utilisateur.json").exists())
folders = sorted(p for p in (ROOT / "out").iterdir()
                 if p.name[:2].isdigit() and (p / "final.mp4").exists())
with ThreadPoolExecutor(max_workers=4) as pool:
    rows = [row for row in pool.map(prepare, folders) if row]
(DEST / "manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(rows, ensure_ascii=False))
