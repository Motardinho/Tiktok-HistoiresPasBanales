"""Calage du dossier 53 : tout part de timings.json (voix ElevenLabs) et de la liste SEQUENCE.

La narration est dite d'un trait, puis découpée en blocs entre lesquels passent les vrais sons.
Ce module donne les blocs de voix, le début de chaque vrai son, la fin de la vidéo, et l'instant de sortie
d'un mot (mot) ou d'un point d'un vrai son (reel). Changer de voix ou de texte ne demande donc pas de recaler à la main.
"""
import json
import subprocess
from pathlib import Path

FPS = 30
B, F, T, D, E = 'ZeCP1Hj0uMA', '7WYz8FYSkI0', 'xk8sQnCkrRA', 'S4UltS2SoXc', '6yCtrUOWLco'

# premier et dernier groupe de mots de chaque bloc de voix
BLOCS = [('Aux championnats', 'zéro point.'), ('Mais quarante', 'record du monde.'), ('Il doit courir', 'quarante-neuf.')]
# vrais sons : nom -> (source, début dans la source, durée, gain)
SONS = {
    'r0': (D, 11.70, 5.24, 2.2),     # Mayer à Berlin : « Je suis tellement déçu pour moi-même… »
    'r1': (E, 158.18, 3.72, 3.0),    # Mayer sur Europe 1 : « …je suis devenu rien du tout. »
    'r3': (F, 1712.03, 4.92, 1.15),   # Mayer dans son film : les larmes du vestiaire
    'r2': (T, 149.90, 18.70, 1.6),  # commentaire RMC Sport : toute la dernière ligne droite et le record
}
# ordre de la bande son ; le nombre est le silence laissé après l'élément
SEQUENCE = [('r0', 0.15), (0, 0.10), ('r1', 0.18), (1, 0.10), ('r3', 0.18), (2, 0.08), ('r2', 0.0)]

_t = json.loads(Path('timings.json').read_text(encoding='utf-8'))
TEXTE = ''.join(_t['characters'])
DEB, FINS = _t['character_start_times_seconds'], _t['character_end_times_seconds']
_duree = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'voix.mp3'],
                              capture_output=True, text=True).stdout)


def image(t):
    return round(t * FPS) / FPS


def _bloc(k):
    a, b = BLOCS[k]
    i, j = TEXTE.index(a), TEXTE.index(b) + len(b) - 1
    lettre = j - 1 if not TEXTE[j].isalnum() else j          # la ponctuation finale porte le silence qui suit
    debut = max(0.0, DEB[i] - 0.04)
    suivant = DEB[j + 2] - 0.03 if j + 2 < len(DEB) else _duree
    fin = min(FINS[lettre] + 0.10, suivant, _duree)
    return i, j, round(debut, 2), round(fin - debut, 2)


VOIX, REELS_T, _bornes, _t0 = [None] * len(BLOCS), {}, [None] * len(BLOCS), 0.0   # VOIX : (début sortie, début voix.mp3, durée)
for element, silence in SEQUENCE:
    if isinstance(element, int):
        i, j, debut, duree = _bloc(element)
        VOIX[element], _bornes[element] = (round(_t0, 2), debut, duree), (i, j)
        _t0 = round(_t0 + duree + silence, 2)
    else:
        REELS_T[element] = image(_t0)
        _t0 = round(REELS_T[element] + SONS[element][2] + silence, 2)
FIN = image(_t0)
# (début dans la sortie, source, début dans la source, durée, gain), dans l'ordre de passage
REELS = [(REELS_T[n], *SONS[n]) for n, _ in SEQUENCE if not isinstance(n, int)]
NOMS_REELS = [n for n, _ in SEQUENCE if not isinstance(n, int)]


def mot(groupe, decalage=0.0):
    """Instant de sortie où commence ce groupe de mots de la narration, calé sur une image."""
    i = TEXTE.index(groupe)
    k = next(n for n, (a, b) in enumerate(_bornes) if a <= i <= b)
    return image(max(0.0, DEB[i] - VOIX[k][1] + VOIX[k][0] - 0.05 + decalage))


def reel(nom, decalage=0.0):
    """Instant de sortie situé `decalage` secondes après le début du vrai son `nom`."""
    return image(REELS_T[nom] + decalage)


if __name__ == '__main__':
    print('VOIX', VOIX)
    print('REELS', {n: round(t, 3) for n, t in REELS_T.items()}, 'FIN', round(FIN, 3))
    voix, sons = sum(v[2] for v in VOIX), sum(s[2] for s in SONS.values())
    print(f'narration {voix:.1f} s ({100 * voix / FIN:.0f} %), vrais sons {sons:.1f} s ({100 * sons / FIN:.0f} %)')
