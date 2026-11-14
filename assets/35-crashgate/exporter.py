"""Export des dossiers 35 et 36 : moteur du lot 21-23, sous-titres de 3 lignes au plus, bandeaux a hauteur reglable (cle y).
python exporter.py 35|36 [habillage]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import monter_lot_21_23 as engine

n = int(sys.argv[1])
story = json.loads((engine.folder(n) / 'histoire.json').read_text(encoding='utf8'))
moved = {b['texte']: b['y'] for b in story.get('bandeaux', []) if 'y' in b}
original = engine.subtitles


def subtitles(m, *args):
    original(m, *args)
    file = m / 'sous-titres.ass'; lines = []
    for line in file.read_text(encoding='utf8').splitlines():
        if line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            label = next((t for t in moved if parts[9].endswith(t)), None)
            if label:
                parts[9] = parts[9].replace(r'\pos(540,420)', r'\pos(540,%d)' % moved[label])
            elif parts[9].count(r'\N') > 2:
                parts[9] = engine.wrap_caption(parts[9].replace(r'\fs90', r'\fs80'), 80)
            line = ','.join(parts)
        lines.append(line)
    file.write_text('\n'.join(lines) + '\n', encoding='utf8')


engine.subtitles = subtitles
engine.build(n, only_dress='habillage' in sys.argv)
