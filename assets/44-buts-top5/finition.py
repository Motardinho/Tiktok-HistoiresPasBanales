"""Retouches ciblées du 13 novembre, sans décaler les actions ni la voix restante."""
import json
import shutil
import subprocess
from pathlib import Path

p = Path('out/44-top-5-buts-les-plus-degueulasses')
m = p / '_montage'
b = m / 'avant-finition-2026-11-13'
b.mkdir(exist_ok=True)
for src in [p / 'histoire.json', p / 'script.txt', p / 'final.mp4', m / 'voix.mp3', m / 'timings-oraux.json']:
    if not (b / src.name).exists():
        shutil.copy2(src, b / src.name)

d = json.loads((b / 'histoire.json').read_text(encoding='utf8'))
for key in ['narration', 'narration_voix']:
    d['scenes'][2][key] = d['scenes'][2][key].replace(' Son premier but avec le club.', '')
d['titre_jusqua_annonce'] = True
d['sources_a_verifier'][0]['fait'] = d['sources_a_verifier'][0]['fait'].replace('8 -', '5 -', 1)
for row in d['sources_a_verifier']:
    if 'premier but avec United' in row['fait']:
        row['fait'] = row['fait'].replace('premier but avec United', 'but au Community Shield ; avait déjà marqué en amical le 28 juillet 2010')
        row['note'] = 'Correction vérifiée le 13 novembre 2026 : https://www.mlssoccer.com/news/chicharito-impresses-man-utd-debut'
d['fun_fact']['source'] = 'https://nationalfootballmuseum.com/stories/object-week-beach-ball-caused-goal/ — fiche du musée du 8 septembre 2020, consultée le 13 novembre 2026 : ballon conservé dans la collection ; emplacement actuel non confirmé.'
d['choix_editoriaux'].append('13 novembre 2026 : suppression de la phrase imprécise sur le premier but de Chicharito ; musique seule sur la célébration, sans déplacer les autres passages. Titre maintenu jusqu’à la fin de son annonce.')
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
(p / 'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']) + '\n', encoding='utf8')
t = json.loads((b / 'timings-oraux.json').read_text(encoding='utf8'))
t['words'] = [w for w in t['words'] if not 27.7 <= w['start'] < 29.55]
t['retouche_2026_11_13'] = 'Phrase supprimée à 27.70–29.55 s ; durées et repères suivants conservés.'
(m / 'timings-oraux.json').write_text(json.dumps(t, ensure_ascii=False, indent=2), encoding='utf8')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(b / 'voix.mp3'),
                '-af', "volume=0:enable='between(t,27.70,29.55)'", '-c:a', 'libmp3lame', '-b:a', '192k', str(m / 'voix.mp3')], check=True)
print('Script, voix et sous-titres corrigés sans décalage.')
