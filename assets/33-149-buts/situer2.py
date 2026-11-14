"""Suite de la révision : tenir sous 75 s après l'ajout de la compétition, et adapter le découpage."""
import json
from pathlib import Path

p = Path('out/33-149-buts-contre-leur-camp')
d = json.loads((p / 'histoire.json').read_text(encoding='utf8'))
s = d['scenes']
for k in ('narration', 'narration_voix'):
    s[3][k] = s[3][k].replace(' Encore. Et encore.', ' Encore.')
s[7]['narration'] = "Score final : 149 à 0."
s[7]['narration_voix'] = "Score final : cent quarante-neuf à zéro."
s[7]['visuel'] = "VIDÉO : ballon au fond des filets."
d['sources_a_verifier'] = [x for x in d['sources_a_verifier'] if 'Arbroath' not in x['fait']]
d['choix_editoriaux'] = [x for x in d['choix_editoriaux'] if not x.startswith('« L\'ancien record »')]
d['choix_editoriaux'].append("Phrase sur l'ancien record de 1885 (36-0) et « Et encore » retirés : la voix dépassait 75 s, et le statut de « record » du 149-0 est discuté.")
for k in ('fin_annonce_titre_mesuree', 'fun_fact_affichage'):
    d.pop(k, None)
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
for f in ('voix.mp3', 'timings-oraux.json'):
    (p / '_montage' / f).unlink(missing_ok=True)

m = Path('assets/33-149-buts/montage.py')
t = m.read_text(encoding='utf8')


def rep(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)


rep(""" ("l'émirne", P(38870678), 4.0, .5, 'Lémurs catta, emblème de Madagascar (lieu de tournage non précisé)'),
 ('joue', A('28-om-va', 7005912), 1.0, .5, 'Trophée de foot : champion en titre'),
 ('en', P(34841978), 1.0, .5, 'Équipes alignées avant un match (stade générique)'),
""", """ ('phase', P(38870678), 4.0, .5, 'Lémurs catta, emblème de Madagascar (lieu de tournage non précisé)'),
 ("l'émirne", P(34841978), 1.0, .5, 'Équipes alignées avant un match (stade générique) : championnat national'),
 ('joue', A('28-om-va', 7005912), 1.0, .5, 'Trophée de foot : champion en titre'),
 ('en', P(36296347), 4.0, .5, 'Équipes qui entrent sur le terrain : joue le titre'),
""")
rep("('le', P(11271465), 6.0, .5, 'Jeu vu à travers les filets : égalisation'),",
    "('titre', P(11271465), 6.0, .5, 'Jeu vu à travers les filets : égalisation'),")
rep("'Joueur assis sur un ballon, tête basse : le titre s’envole'", "'Joueur assis sur un ballon, tête basse : titre perdu'")
rep("('coup', P(6078635), 9.0,", "('dernière', P(6078635), 9.0,")
rep("'Rond central vu de haut : coup d’envoi'", "'Rond central vu de haut : dernière journée, coup d’envoi'")
rep(""" ('et', P(6077705), 4.6, .5, 'Nouvelle frappe : et encore'),
""", "")
rep("""('pendant', P(6077714), 0.5, .5, 'Fun fact : gardien face au ballon, sous l’encart'),
 ('en', P(11271465), 0.5, .5, 'Jeu vu à travers les filets : pendant tout le match'),
""", """('en', P(6077714), 0.5, .5, 'Fun fact : gardien face au ballon, sous l’encart'),
""")
rep("""("l'ancien", P(31430984), 1.75, .5, 'Ballon au fond des filets : score final, 149 à 0'),
 ('trente-six', P(17154933), 0.4, .5, 'Vieux ballon en cuir en l’air : record de 1885'),
 ('la', P(12788730), 4.0, .5, 'Pied sur le ballon : 36 à 0'),
""", """('la', P(31430984), 1.75, .5, 'Ballon au fond des filets : score final, 149 à 0'),
""")
m.write_text(t, encoding='utf8')
print('ok')
