import json,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone,timedelta
p=Path('out/24-deluge-fusees');m=p/'_montage'
stamp=datetime.now(timezone(timedelta(hours=1), 'Europe/Paris - CET')).isoformat()
legend='''Pourquoi inonder une fusée ? Toute cette eau protège aussi le lanceur du bruit. Tu pensais qu’elle servait seulement contre la chaleur ?

#histoirevraie #espace #NASA #science #HistoiresPasBanales

Sources : NASA, essais des systèmes d’eau pour Artemis II, 19 juillet 2024 (images d’essai du 24 octobre 2023) :
https://www.nasa.gov/blogs/missions/2024/07/19/nasa-kennedy-teams-complete-water-flow-tests-for-artemis-ii-mission/
NASA, The Space Launch System Part 2 :
https://www.nasa.gov/podcasts/houston-we-have-a-podcast/the-space-launch-system-part-2/
NASA, Artemis I Reference Guide :
https://www.nasa.gov/wp-content/uploads/2023/03/Artemis20I20Reference20Guide_Inter.pdf

400 000 gallons US représentent environ 1,5 million de litres, soit environ 1 500 tonnes d’eau. Quantité totale, pas débit par seconde. « Oiseaux de pluie » est la traduction littérale de rainbirds, surnom des buses.

Images : NASA / Kennedy Space Center, essais du 24 octobre 2023 et lancement d’Artemis I du 16 novembre 2022. Recadrages et montage HPB. Les essais sans fusée sont distincts des images de décollage.
Politique d’utilisation des images NASA : https://www.nasa.gov/nasa-brand-center/images-and-media/
Musique : « Masking the Masters », Eugenio Mininni / Mixkit - Stock Music Free License : https://mixkit.co/license/modal/musicFree/
Narration par voix de synthèse. Vidéo indépendante, sans affiliation ni approbation de la NASA.
'''
for name in ['legende.txt','publication.txt']:(p/name).write_text(legend,encoding='utf8')
items=json.loads(Path('assets/24-deluge-fusees/recherche-nasa.json').read_text(encoding='utf8'))
launch=json.loads(Path('assets/24-deluge-fusees/recherche-lancement.json').read_text(encoding='utf8'))
credits=['# Crédits du dossier 24','', 'Consultation des sources : 10 et 11 novembre 2026, Europe/Paris.','', 'Toutes les séquences retenues viennent de la médiathèque officielle NASA ; aucun visuel généré, aucune photo. Les vidéos de synthèse de mission, les vues isolées et la piste de 2018 recherchées mais non retenues ne sont pas dans le montage.','']
for i,name in [(0,'deluge-sol-2023.mp4'),(1,'deluge-drone-2023.mp4'),(2,'deluge-drone2-2023.mp4')]:
 a=items[i]['data'];credits += [f"- {name} : {a['title']} - NASA/KSC - {a['date_created']} - ID {a['nasa_id']}"]
for i,name in [(0,'lancement-suivi.mp4'),(2,'lancement-plateforme.mp4')]:
 a=launch[i]['data'][0];credits += [f"- {name} : {a['title']} - NASA/KSC - {a['date_created']} - ID {a['nasa_id']}"]
credits += ['', 'Provenance et descriptions complètes : assets/24-deluge-fusees/recherche-nasa.json et recherche-lancement.json. Découpes exactes : _montage/montage.json.', '', 'Usage éditorial éducatif : https://www.nasa.gov/nasa-brand-center/images-and-media/', 'Musique : Masking the Masters - Eugenio Mininni - Mixkit, licence https://mixkit.co/license/modal/musicFree/', '', 'Comparaison de travail uniquement : vidéo HPB des téléphones validée, à gauche. Aucun extrait des téléphones dans la nouvelle vidéo.']
(p/'CREDITS.md').write_text('\n'.join(credits),encoding='utf8')
export=json.loads((m/'controle-export.json').read_text(encoding='utf8'))
report=dict(date=stamp,statut='export à visionner - contrôle sonore et mouvement continu non validés',preuves_visuelles=['_montage/reference-telephone.jpg : copie validée des téléphones, échantillons à intervalle de 6 secondes','Planches sources NASA, puis 69 captures des 23 plans recadrés (début/milieu/fin)','69 captures du MP4 habillé à 360 px de large, réparties en 6 planches','Première image 0:00, fun fact, signature, et simulation du lecteur TikTok','Captures de comparaison début/fun fact/fin'],observations=['Titre seul au début, première transcription à 2,293 s ; reprise du titre présente dans l’alignement TTS','Logo et série présents sur tous les échantillons examinés','Fun fact à 46,58-53,70 s, sous-titres conservés en bas et encart séparé','Aucune collision visible sur les captures examinées','Plans 14 et 15 remplacés après contrôle pour montrer les buses et leur mise en eau','Aucune photo ; vitesse native des sources ; recadrages 9:16','Décodage intégral des deux exports réussi'],limites=['Aucune écoute subjective possible : tentative de lecture audio refusée par l’outil (audio input non pris en charge). Ne pas considérer le mix, la prononciation et la fluidité vocale comme validés.','Inspection visuelle par captures, pas visionnage continu en temps réel : mouvement continu et synchronisation perceptuelle restent à examiner.','La référence des téléphones a été examinée visuellement ; son audio n’a pas été écouté.'],technique=export,validation_utilisateur=False)
(p/'controle-livraison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
d=json.loads((p/'histoire.json').read_text(encoding='utf8'));d['statut']='export à visionner - écoute finale requise';(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
idx=Path('out/versions-actuelles.json');data=json.loads(idx.read_text(encoding='utf8'));data=[x for x in data if x.get('numero')!=24];data.append(dict(numero=24,dossier=p.name,duree=export['duree_video'],sha256=export['sha256'],comparaison_a_jour=True,statut='a_visionner_controle_audio_requis',revision=stamp+' : nouvelle vidéo, référence qualité téléphones validée',apercu_simule='apercu-tiktok.jpg'));idx.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Légende, crédits, contrôle et index écrits.')
