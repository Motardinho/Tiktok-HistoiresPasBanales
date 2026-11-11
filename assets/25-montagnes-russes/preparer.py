"""Dossier 25 : histoire.json, script et sources. Faits vérifiés le 11 novembre 2026 (Europe/Paris).

Noms étrangers écrits en phonétique française dans narration_voix (demande de Marc du 11 nov. 2026) :
prononciation avec un accent français, orthographe d’origine à l’écran via `affichage`."""
import json
from pathlib import Path
p = Path('out/25-montagnes-russes-plus-rapides')
scenes = [
 (None, "Top 3 des montagnes russes les plus rapides. Attache bien ta ceinture.",
        "Top trois des montagnes russes les plus rapides. Attache bien ta ceinture."),
 (3, "Numéro 3. Top Thrill 2, à Cedar Point, aux États-Unis. 193 km/h. Le train est lancé en avant, puis en arrière, puis encore en avant. Et il grimpe à la verticale, jusqu’à 130 mètres de haut.",
     "Numéro trois. Top Trile deux, à Cédar Poïnte, aux États-Unis. Cent quatre-vingt-treize kilomètres-heure. Le train est lancé en avant, puis en arrière, puis encore en avant. Et il grimpe à la verticale, jusqu’à cent trente mètres de haut."),
 (2, "Numéro 2. Formula Rossa, au parc Ferrari World d’Abou Dhabi. 240 km/h. De 0 à 100 en 2 secondes environ. Elle a été la plus rapide du monde pendant 15 ans.",
     "Numéro deux. Formula Rossa, au parc Ferrari Weurld d’Abou Dhabi. Deux cent quarante kilomètres-heure. De zéro à cent en deux secondes environ. Elle a été la plus rapide du monde pendant quinze ans."),
 (2, "Ici, les passagers doivent porter des lunettes de protection, contre la poussière du désert. Même les pilotes Ferrari Fernando Alonso et Felipe Massa les ont mises, en 2010.",
     "Ici, les passagers doivent porter des lunettes de protection, contre la poussière du désert. Même les pilotes Ferrari Fernando Alonso et Félipé Massa les ont mises, en deux mille dix."),
 (None, "Mais le numéro 1 va encore 10 km/h plus vite.",
        "Mais le numéro un va encore dix kilomètres-heure plus vite."),
 (1, "Numéro 1. Falcons Flight, en Arabie saoudite. 250 km/h. Ouverte fin 2025, c’est aussi la plus haute et la plus longue du monde : plus de 4 kilomètres de rails.",
     "Numéro un. Falkonz Flaïte, en Arabie saoudite. Deux cent cinquante kilomètres-heure. Ouverte fin deux mille vingt-cinq, c’est aussi la plus haute et la plus longue du monde : plus de quatre kilomètres de rails."),
 (1, "Elle escalade une falaise en plein désert. Puis, au bord du vide, le train plonge à la verticale, droit dans un tunnel. Et le trajet dure plus de 3 minutes.",
     "Elle escalade une falaise en plein désert. Puis, au bord du vide, le train plonge à la verticale, droit dans un tunnel. Et le trajet dure plus de trois minutes."),
 (None, "Toi, tu monterais dans laquelle ? Pas banal, hein ?",
        "Toi, tu monterais dans laquelle ? Pas banal, hein ?"),
]
sources = [
 "Critère : vitesse maximale des montagnes russes existantes, relevée le 11 novembre 2026. Kingda Ka (206 km/h) a fermé en 2024 et a été démolie : non classée.",
 "Falcons Flight (Six Flags Qiddiya City, Arabie saoudite) : 250 km/h (155,3 mph), 163 m de haut, 4 250 m de long, ouverture officielle le 31 décembre 2025, trois lancements LSM, trajet de 3 min 35 s, montée sur la falaise de Tuwaiq, freinage au bord de la falaise puis descente à 90° dans un tunnel - Wikipedia (révision du 6 nov. 2026, sources Intamin et Six Flags) ; RCDB https://rcdb.com/21315.htm",
 "Formula Rossa (Ferrari World Abu Dhabi) : 240 km/h, 0 à 240 km/h en 4,9 s, 0 à 100 km/h en 2 s environ, lunettes de protection obligatoires contre la poussière - Wikipedia (révision du 5 nov. 2026). Record du monde de vitesse du 4 nov. 2010 au 31 déc. 2025.",
 "Fernando Alonso et Felipe Massa à bord de Formula Rossa : vidéo Ferrari publiée par Motor1 le 14 novembre 2010 (week-end du Grand Prix d’Abou Dhabi 2010), lunettes visibles à l’image.",
 "Top Thrill 2 (Cedar Point, Ohio, États-Unis) : 120 mph (193 km/h), 420 ft (128 m, arrondi à 130 m par Wikipedia), lancements avant - arrière - avant, ouverture le 4 mai 2024 - Wikipedia.",
 "Pièges : Formula Rossa est fermée « pour maintenance » depuis le 12 mai 2026 selon Wikipedia ; Top Thrill 2 a connu des fermetures prolongées. Le classement porte sur la vitesse, pas sur l’ouverture du jour. Falcons Flight : 250 km/h (fiche) ou 249 km/h (texte), même vitesse de 155 mph.",
]
d = dict(
 titre_fixe='TOP 3 DES MONTAGNES RUSSES LES PLUS RAPIDES 2026',
 titre_lignes=['TOP 3 DES', 'MONTAGNES RUSSES', 'LES PLUS RAPIDES', '2026'],
 titre_interligne=22,
 serie='TOP 3 - MONTAGNES RUSSES RAPIDES',
 format='top',
 reference='https://www.tiktok.com/@faiseemoc84/video/7320682957964905760',
 reference_fichier='out/20-telephone-2899-dollars/version-validee/final.mp4',
 reference_auteur='HPB - téléphones validée (étalon qualité demandé par Marc)',
 musique='voitures',
 scenes=[dict(**({'rang': r} if r else {}), narration=n, narration_voix=v) for r, n, v in scenes],
 affichage={
  'top trile deux': 'Top Thrill 2',
  'cédar poïnte': 'Cedar Point',
  'ferrari weurld': 'Ferrari World',
  'félipé': 'Felipe',
  'cent quatre-vingt-treize kilomètres-heure': '193 KM/H',
  'cent trente mètres': '130 mètres',
  'deux cent quarante kilomètres-heure': '240 KM/H',
  'zéro à cent': '0 à 100',
  'deux secondes': '2 secondes',
  'deux mille dix': '2010',
  'le numéro un': 'le N°1',
  'dix kilomètres-heure': '10 KM/H',
  'falkonz flaïte': 'Falcons Flight',
  'deux cent cinquante kilomètres-heure': '250 KM/H',
  'deux mille vingt-cinq': '2025',
  'quatre kilomètres': '4 kilomètres',
  'quinze ans': '15 ans',
  'trois minutes': '3 minutes',
 },
 bandeaux=[
  dict(scene=1, duree=4.5, texte=r'3 - TOP THRILL 2\N193 KM/H'),
  dict(scene=2, duree=4.0, texte=r'2 - FORMULA ROSSA\N240 KM/H'),
  dict(scene=5, duree=4.5, texte=r'1 - FALCONS FLIGHT\N250 KM/H'),
 ],
 fun_fact=dict(scene=3, rang=2, texte=['LUNETTES DE PROTECTION', 'OBLIGATOIRES'],
               source='Wikipedia, Formula Rossa : « Riders are required to wear safety goggles to protect from airborne particles such as dust » (révision du 5 nov. 2026)'),
 fun_fact_top=760,  # visages des pilotes dans le haut du cadre : encart sous les visages, au-dessus des sous-titres
 sources_a_verifier=sources,
 statut='script vérifié - avant synthèse',
)
p.mkdir(exist_ok=True)
(p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
(p / 'script.txt').write_text('\n'.join(s[1] for s in scenes) + '\n', encoding='utf8')
print('mots', len(' '.join(s[2] for s in scenes).split()))
