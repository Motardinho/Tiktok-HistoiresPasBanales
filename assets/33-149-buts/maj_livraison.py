"""Met à jour les textes de livraison.py après la révision « situer la compétition »."""
from pathlib import Path

f = Path('assets/33-149-buts/livraison.py')
t = f.read_text(encoding='utf8')


def rep(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)


rep('legend = """149 buts contre leur camp, exprès,', 'legend = """Championnat de Madagascar, 31 octobre 2002 : 149 buts contre leur camp, exprès,')
rep('Wikipédia, « AS Adema 149-0 SO l\'Emyrne » et « Arbroath 36-0 Bon Accord »', 'Wikipédia, « AS Adema 149-0 SO l\'Emyrne »')
rep("'141 captures du MP4 habillé (début, milieu, fin des 47 plans) : _montage/controle/final-page-0..11.jpg'",
    "'132 captures du MP4 habillé (début, milieu, fin des 44 plans) : _montage/controle/final-page-0..10.jpg'")
rep("« Exprès. » prononcé à 2,88 s, « Et en face, personne n’a bougé » fini vers 5,7 s",
    "« Exprès. » prononcé à 2,96 s, « Et en face, personne n’a bougé » fini vers 5,8 s")
rep("30,9-36,1 s, encart en haut", "34,2-38,5 s, encart en haut")
rep("        'Sources en vertical natif",
    "        'Révision demandée par Marc le 11/11/2026 (« on ne sait pas quelle est la compétition ») : « octobre 2002, phase finale du championnat national » et « dernière journée » dits à l’oral, bandeaux « CHAMPIONNAT NATIONAL » et « DERNIÈRE JOURNÉE », bandeau de série « FOOT - MADAGASCAR 2002 » ; phrase sur le record de 1885, « Et encore » et « Pendant tout le match » retirés pour tenir la durée',\n        'Sources en vertical natif")
rep("        'Durée 71,43 s : dans la limite de 75 s, légèrement au-dessus de la cible 61-70 s.',\n", "")
rep("        'Trophée avec un « 20 » décoratif ; ballon rouge moderne sur « 36 à 0 ».'", "        'Trophée avec un « 20 » décoratif.'")
rep("        '« L’ancien record » : Guinness homologue 149 comme record de buts contre son camp ; le 36-0 de 1885 reste pour certains le plus gros score « sportif ». Risque de correction en commentaire.',\n",
    "        '« Dernière journée » : déduit du déroulé de la poule finale (six journées, l’Adema sacré à une journée de la fin) d’après Wikipédia.',\n")
rep("revision=stamp + ' : première livraison'", "revision=stamp + ' : compétition située (championnat national, dernière journée)'")
f.write_text(t, encoding='utf8')
print('ok')
