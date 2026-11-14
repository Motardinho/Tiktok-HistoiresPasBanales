"""Révision du 11/11/2026 (Marc : « on ne sait pas quelle est la compétition ») : situer le match."""
import json
from pathlib import Path

p = Path('out/33-149-buts-contre-leur-camp')
d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
s = d['scenes']
s[1]['narration'] = ("Madagascar, octobre 2002. Phase finale du championnat national. L'Emyrne, champion en titre, joue le titre. "
                     "En fin de match, l'arbitre siffle un penalty très contesté. Égalisation. Titre perdu.")
s[1]['narration_voix'] = ("Madagascar, octobre deux mille deux. Phase finale du championnat national. L'Émirne, champion en titre, joue le titre. "
                          "En fin de match, l'arbitre siffle un penalty très contesté. Égalisation. Titre perdu.")
s[3]['narration'] = "Dernière journée. " + s[3]['narration'].removeprefix("Dernière journée. ")
s[3]['narration_voix'] = "Dernière journée. " + s[3]['narration_voix'].removeprefix("Dernière journée. ")
s[4]['narration'] = "Et là, accroche-toi : un but toutes les 36 secondes."
s[4]['narration_voix'] = "Et là, accroche-toi : un but toutes les trente-six secondes."
d['serie'] = 'FOOT - MADAGASCAR 2002'
d['bandeaux'] = [
    dict(scene=1, duree=1.85, texte='MADAGASCAR - 2002'),
    dict(scene=1, apres=2.3, duree=2.0, texte='CHAMPIONNAT NATIONAL'),
    dict(scene=3, duree=1.5, texte='DERNIÈRE JOURNÉE'),
]
d['legende'] = ("Championnat de Madagascar, 31 octobre 2002 : 149 buts contre leur camp, exprès, pour protester contre l'arbitre. "
                "Ce coach : génie ou honte du football ? Réponds en un mot.")
note = "Révision du 11/11/2026 (Marc) : compétition située à l'oral et à l'écran (phase finale du championnat national, dernière journée) ; « Pendant tout le match » retiré pour tenir la durée."
if note not in d['choix_editoriaux']:
    d['choix_editoriaux'].append(note)
for k in ('fin_annonce_titre_mesuree', 'fun_fact_affichage'):
    d.pop(k, None)
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
for f in ('voix.mp3', 'timings-oraux.json'):
    (p / '_montage' / f).unlink(missing_ok=True)
print('ok')
