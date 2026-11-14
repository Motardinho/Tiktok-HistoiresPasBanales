"""Consigne les contrôles réellement faits le 13 novembre 2026."""
import json
import subprocess
from pathlib import Path

a = Path('assets/44-buts-top5')
p = Path('out/44-top-5-buts-les-plus-degueulasses')
notes = json.loads((a/'controle-notes.json').read_text(encoding='utf8'))
notes['statut'] = 'finition exportée ; écoute et visionnage continu non certifiés'
notes['preuves_visuelles'] = [
    '_montage/controle-2026-11-13/page-0.jpg à page-4.jpg : 57 captures effectivement examinées du nouveau final (0–68,3 s), ouverture, suppression de phrase, cinq buts, fun fact, fin.',
    'apercu-tiktok.jpg régénéré et examiné : titre, fun fact, fin à 360 px avec interface simulée.',
    '_montage/controle/final-page-0.jpg à page-4.jpg : 54 captures régénérées ; les anciennes planches avaient été examinées avant retouche, ne vaut pas visionnage continu du nouvel export.',
    '_montage/controle-2026-11-13/comparaison.jpg : nouveau logo et absence de titre sur le côté HPB de la comparaison.'
]
notes['observations'] = [
    'Sélection confirmée par Marc le 13 novembre : Green, Chicharito, Kießling, Bent, Kane.',
    'Dernière demande de Marc du 13 novembre : titre d’ouverture retiré, bandeau de série permanent retiré, nouveau logo HPB jaune en haut à droite (x=873, y=240, 143x130). Rangs temporaires et fun fact conservés.',
    'Phrase « Son premier but avec le club » retirée du script, des sous-titres et de la voix entre 27,70 et 29,55 s. Célébration conservée sur la musique.',
    'Ballon dans le but observé : Green 16,5–16,8 s ; Chicharito 26,2–27,1 s ; Kießling passage latéral puis ballon derrière le filet 35,6–37,1 s ; Bent 50,2–50,4 s ; Kane 63,0–63,3 s.',
    'Archives toujours douces et filés de caméra conservés ; aucune nouvelle source introduite.',
    'Crédit de la photo de couverture ajouté aux deux légendes et aux crédits.',
    'Comparaison régénérée depuis le nouveau final ; deux pistes, HPB par défaut ; décodage complet sans erreur.'
]
notes['limites'] = [
    'Pas de visionnage continu ni d’écoute intégrale certifiés. Les captures et le décodage ne valident pas la prononciation ni la qualité subjective du mix.',
    'Première Ligue et Kayne : voix de la dernière révision conservée, hors suppression de la phrase à 27,70–29,55 s.',
    'Hook parlé complet après 5 s (premier rang à 6,8 s) : structure existante conservée.',
    'Direct Green tronqué au début ; son action complète est montrée au ralenti. Sources 720p et ralentis avec filés de caméra.',
    'Chicharito : ralenti supplémentaire préexistant. Bent : direct tronqué au début, ralenti conservé.',
    'Contrôle par captures espacées : ne garantit pas chaque image intermédiaire.'
]
notes['a_revoir_avant_de_poster'] = [
    'Écouter le final complet, notamment les prononciations et la coupe de narration à 27,70–29,55 s.',
    'Séquences de matchs sans autorisation : risque de restriction, retrait ou son coupé.',
    'Fun fact : fiche officielle du National Football Museum du 8 septembre 2020 consultée le 13 novembre 2026 ; collection confirmée par cette fiche, emplacement actuel non vérifié.',
    'Publier le TOP 5, pas également le TOP 10 avec les mêmes buts.'
]
(a/'controle-notes.json').write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding='utf8')
subprocess.run(['python', str(a/'livraison.py')], check=True)
idx = Path('out/versions-actuelles.json')
rows = json.loads(idx.read_text(encoding='utf8'))
row = next(x for x in rows if x.get('numero') == 44)
row['revision'] = '2026-11-13 : titre d’ouverture et bandeau de série retirés ; logo HPB en haut à droite ; comparaison actualisée ; écoute finale requise'
idx.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
print('Livraison et preuves actualisées ; aucune nouvelle validation utilisateur enregistrée.')
