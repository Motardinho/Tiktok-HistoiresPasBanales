from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib,json,subprocess
OUT=Path(__file__).resolve().parent
for n in [31,33]:
 d=OUT/str(n);story=json.loads((d/'histoire.json').read_text(encoding='utf-8'))
 for k in ['fin_annonce_titre_mesuree','fun_fact_affichage']:story.pop(k,None)
 story.update(bandeaux=[],bandeaux_classement_visibles=False,logo='identite/histoires-pas-banales/logos/hpb-reference-propre-v1.svg',validation_audio_integrale=False)
 (d/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
 data={'date':datetime.now(ZoneInfo('Europe/Paris')).isoformat(),'statut':'apercu_local_a_valider','publication_modifiee':False,
 'preuves_visuelles':['controle-0.jpg','controle-1.jpg','controle-2.jpg','controle-3.jpg','frame-0.jpg','simulation-tiktok.jpg','comparaison.jpg'],
 'methode':'Examen des captures du MP4 au début, milieu et fin de chaque plan ; premières images et fin ; aperçu à 360 px ; comparaison avant/après. Ce relevé ne prétend pas à une écoute intégrale ni à un visionnage continu avec son.',
 'audio':{'ecoute_integrale':False,'raison':'Les outils de cette session ne permettent pas de percevoir le flux audio. Tentative de lecture du WAV renvoyée comme entrée audio non prise en charge. Contrôles techniques séparés, sans prétendre remplacer l’écoute.','mesures':'controle-audio-technique.txt'},
 'decode':['final.mp4.decode.txt','comparaison.mp4.decode.txt'],
 'fluidite':{'preuve':'controle-images-repetees.json','limite':'freezedetect signale aussi les documents volontairement fixes et les pauses de personnes en entretien. Pas de boucle ni de prolongation gelée pour remplir les plans.'},
 'comparaison':'Ancienne version validée à gauche, nouvelle version à droite ; deux pistes audio, nouvelle version par défaut ; image figée et silence après fin de la plus courte.',
 'sha256':{f:hashlib.sha256((d/f).read_bytes()).hexdigest() for f in ['final.mp4','comparaison.mp4']}}
 if n==33:data['exception_documentaire']='Choix explicite de Marc : documents sourcés et club Adema filmé en 2018. Cette date est dite et sous-titrée ; aucune prétention à montrer le match 2002. Extraits de documents recomposés, pas fac-similés.'
 (d/'controle-livraison.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'date':'2026-11-14','lot':'15 novembre 2026','statut':'deux aperçus locaux ; validation utilisateur et écoute nécessaires avant remplacement','publications_modifiees':False,'videos':[{'numero':33,'heure':'12:00','final':'33/final.mp4','comparaison':'33/comparaison.mp4'},{'numero':31,'heure':'18:00','final':'31/final.mp4','comparaison':'31/comparaison.mp4'}]}
(OUT/'livraison.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
