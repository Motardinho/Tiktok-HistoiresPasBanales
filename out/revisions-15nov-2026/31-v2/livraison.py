"""Dossier 31, révision v2 : histoire.json, script, légende, crédits et contrôle daté."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

W = Path(__file__).resolve().parent
ROOT = W.parents[2]
SRC = ROOT / 'out/31-pogba-braque-pour-13-millions'
story = json.loads((SRC / 'histoire.json').read_text(encoding='utf-8'))
hook = "Pogba braqué pour 13 millions d'euros. Et parmi les condamnés… son propre frère."
story['hook'] = hook
story['scenes'][0].update(narration=hook, narration_voix="Pogba braqué pour treize millions d'euros. Et parmi les condamnés… son propre frère.",
                          visuel='VIDÉO réelle : Pogba à la Juventus, policiers au tribunal le jour du verdict, Mathias Pogba (AP).')
for k in ['fin_annonce_titre_mesuree', 'fun_fact_affichage', 'titre_fixe', 'titre_lignes', 'titre_interligne']:
    story.pop(k, None)
story.update(statut='revision_locale_a_valider', type_post='videos', bandeaux=[], logo='identite/histoires-pas-banales/logos/hpb-reference-propre-v1.svg',
             reference_fichier='out/31-pogba-braque-pour-13-millions/version-validee/final.mp4',
             reference_auteur='HPB, version validée du dossier 31', reference='hpb-31-version-validee',
             tiktokabilite={'verdict': 'adapté', 'limite': "Aucune image du braquage ni des billets : 6 plans Pexels signalés (10,96 à 17,80 s, puis 25,13 à 27,97 s). Le reste est réel : Pogba, Mathias, tribunal, Élysée 2018, Monaco 2025."},
             legende="Braqué pour 13 millions d'euros par des potes d'enfance… et son propre frère condamné. Toi, tu aurais pardonné ? Oui ou non ?")
(W / 'histoire.json').write_text(json.dumps(story, ensure_ascii=False, indent=2), encoding='utf-8')
(W / 'script.txt').write_text('\n\n'.join(s['narration'] for s in story['scenes']) + '\n', encoding='utf-8')

videos = """Images réelles (son d'origine coupé, extraits courts recadrés) :
- Juventus (chaîne officielle), « Pogback: Paul Pogba 30 iconic moments », 1er mars 2023 : https://www.youtube.com/watch?v=x8jKwFtoV7c
- AP / KINO Club, « Mathias Pogba arrives in court for sentencing », 19 décembre 2024 : https://www.youtube.com/watch?v=-VCsVIWLDCE
- AFP, « Procès Pogba : arrivée de Mathias Pogba au tribunal de Paris », 3 décembre 2024 : https://www.youtube.com/watch?v=eLUsfD5ZbH4
- AFP Images, « Pogba : le procès de six proches du footballeur s'ouvre à Paris », 26 novembre 2024 : https://www.youtube.com/watch?v=KCLUsiKZP1s
- Le Figaro / AFP, « Affaire Pogba : le frère du footballeur condamné », 19 décembre 2024 : https://www.youtube.com/watch?v=7yP3HAcCDQc
- Le Parisien, « Mathias Pogba publie une trentaine de vidéos d'accusations contre son frère Paul », 23 septembre 2022 : https://www.youtube.com/watch?v=8hD6fgR93jM
- L'Équipe, « Le show de Pogba à l'Élysée », 16 juillet 2018 : https://www.youtube.com/watch?v=17f320DMdLY
- CARRÉ, entretien de Paul Pogba, 27 octobre 2024 : https://www.youtube.com/watch?v=VFuZMU9rGA8
- adidas, publicité « Le créateur » avec Paul Pogba (copie Isaac Tuscano) : https://www.youtube.com/watch?v=S_sMDNY-9PA
- AS TV / Diario AS, Pogba en larmes à la signature à Monaco, 28 juin 2025 : https://www.youtube.com/watch?v=qhbAqh96OoA
- Photo publiée par Paul Pogba le 19 août 2025 : https://www.instagram.com/p/DNi-H1GCTmx/
Illustrations Pexels (aucune image réelle n'existe) pour le braquage et les billets : vidéos 4547598, 6670907, 6091316, 29992749, 31402662."""
base = (SRC / 'legende.txt').read_text(encoding='utf-8').split('\n\nImages d')[0]
base = base.replace('Braqué pour 13 millions par', "Braqué pour 13 millions d'euros par")
leg = base + '\n\n' + videos + '\n\nMusique : Greed - Arulo / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.\n'
for f in ['legende.txt', 'publication.txt']:
    (W / f).write_text(leg, encoding='utf-8')
credits = (SRC / 'CREDITS.md').read_text(encoding='utf-8').split('## Vidéos utilisées')[0]
credits += '## Vidéos utilisées\n' + videos + """

Identification de Mathias Pogba : homme en doudoune beige, nommé dans les titres AP (19 décembre 2024) et AFP (3 décembre 2024), comparé à sa vidéo de 2022 (Le Parisien). L'homme interviewé dans l'extrait AFP du 26 novembre 2024 n'est pas présenté comme Mathias (identité non certaine).
Écartés : plateaux télé (BFMTV, LCI, L'Équipe, FRANCE 24) sans image utile ; vidéo « Mathias Pogba » de Mohamed Henni (ce n'est pas Mathias) ; images de La Provence (billets en dollars, illustration de braqueur).
Pas d'image réelle du braquage ni de la soirée : 6 plans Pexels, signalés.

## Son
- Greed - Arulo, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/
- Narration synthétique ElevenLabs : hook resynthétisé le 14 novembre 2026 (« 13 millions d'euros »), suite identique à la voix validée.

Comparaison : version validée du dossier 31 à gauche, révision v2 à droite.
"""
(W / 'CREDITS.md').write_text(credits, encoding='utf-8')
data = {
    'date': datetime.now(ZoneInfo('Europe/Paris')).isoformat(timespec='seconds'),
    'statut': 'apercu_local_a_valider', 'publication_modifiee': False,
    'demande': "Marc, 14 novembre 2026 : « d'euros » dans le hook, vraies vidéos, dernières règles du skill",
    'examine': ['controle/plans-0.jpg … plans-6.jpg : début, milieu et fin des 37 plans dans final.mp4 avec habillage',
                'image à 0:00 (Pogba en action, Juventus), 3 plans avant 5 s, hook dit en 5,52 s',
                'fin : Pogba au micro à l’Élysée, question finale, signature'],
    'corrections_apres_controle': ['Élysée : Pogba hors cadre, recadré', 'adidas : coupes internes, entrées calées sur les plans',
                                   'logos AP, Le Parisien et CARRÉ hors cadre', 'photo des frères : visage sous le logo HPB, photo descendue'],
    'decode': 'final.mp4 et comparaison.mp4 décodés sans erreur ; vidéo 74,07 s, audio 74,06 s ; freezedetect (1,2 s) : aucun gel',
    'audio': {'ecoute_integrale': False, 'raison': "Pas d'écoute possible dans cette session ; raccord hook/suite à 5,52 s à écouter."},
    'pexels_signales': ['10,96-17,80 s : porte, cagoule, arme, billets (braquage)', '25,13-27,97 s : liasse d’euros'],
    'droits': 'Extraits de médias (AFP, AP, Le Parisien, L’Équipe, Juventus, CARRÉ, adidas, AS) : risque son coupé ou diffusion limitée.',
    'sha256': {f: hashlib.sha256((W / f).read_bytes()).hexdigest() for f in ['final.mp4', 'comparaison.mp4']},
}
(W / 'controle-livraison.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print('ok')
