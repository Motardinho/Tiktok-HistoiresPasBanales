import json,hashlib,subprocess
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
R=Path.cwd();P=R/'out/48-faid-evasion-helicoptere';A=R/'assets/48-faid'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=read(P/'histoire.json');plans=read(P/'plans.json');sources=[]
for sid in sorted({Path(p['source']).stem for p in plans}):
 x=read(A/(sid+'.info.json'));sources.append(dict(id=sid,chaine=x.get('channel'),titre=x.get('title'),date=x.get('upload_date'),url=x.get('webpage_url'),width=x['width'],height=x['height']))
for p in plans:
 p['provenance']=next(s for s in sources if s['id']==Path(p['source']).stem)
 p['largeur_utile']=2*round(p['hauteur']*9/16/2)
 p['nature']='Archives réelles, son original retiré. Documents photographiques et captures de surveillance lorsque source TF1.'
 if p['source']=='rz7MsZ4KK54.mp4':
  p['action']='Document du dossier Réau 2018 diffusé par TF1 INFO : appareil, parloir, commando, portes ou arrestation selon horodatage source. Photo documentaire ou capture de vidéosurveillance.'
save(P/'sources-visuelles.json',plans)
credits='\n'.join(f"{s['chaine']} - {s['titre']} - {s['date']} - {s['url']}" for s in sources)
facts='\n'.join(s['fait']+' - '+s['url'] for s in d['sources_a_verifier'])
notes="Images de vidéosurveillance de Réau, vidéo filmée par un détenu et archives de récupération du véritable hélicoptère. Le gros plan en ouverture montre le véritable appareil dans la cour de Réau, document publié par TF1. Plusieurs pièces sont des photographies documentaires et des captures de vidéosurveillance présentées dans le reportage TF1 du procès de 2023. La copie LEnDeZyQV-I correspondait à 2013 et a été entièrement écartée après vérification. Le portrait de Faïd est une archive antérieure reprise dans le reportage. La photographie de Faïd arrêté provient des documents de la BRI repris par TF1. La prise d’otage du pilote et l’atterrissage ne sont pas directement filmés dans les extraits retenus. La vidéo du détenu conserve son habillage source pour garder l’appareil dans le cadre. Archives peu définies, notamment vidéosurveillance et hélicoptère lointain."
music='Musique - Masking the Masters, Eugenio Mininni, Mixkit. https://mixkit.co/free-stock-music/tag/documentary/ - https://mixkit.co/license/modal/musicFree/'
legend='Une évasion en hélicoptère, filmée depuis la prison. Trois mois de cavale, puis une condamnation à 14 ans pour cette évasion. Ça valait quoi, sa liberté ?\n\n#HistoiresPasBanales #HistoireVraie #FaitsDivers #Evasion\n\nSources des images\n'+credits+'\n\nSources des faits\n'+facts+'\n\n'+music+'\n\nNarration originale HPB, voix synthétique.\n'+notes+'\n'
for name in ['legende.txt','publication.txt']:(P/name).write_text(legend,encoding='utf8')
(P/'CREDITS.md').write_text('# Évasion de Rédoine Faïd\n\n'+credits+'\n\n'+facts+'\n\n'+music+'\n\n'+notes+'\n\nLa citation des sources ne vaut pas acquisition des droits. Les diffuseurs peuvent revendiquer les extraits, avec son coupé ou diffusion limitée sur TikTok/YouTube.\n',encoding='utf8')
final=P/'final.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'],check=True,capture_output=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,duration,width,height','-of','json',str(final)]))
v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert float(v['duration'])>60 and abs(float(v['duration'])-float(a['duration']))<.15
now=datetime.now(ZoneInfo('Europe/Paris')).isoformat()
report=dict(date=now,statut='montage à visionner et écouter',validation_utilisateur=False,technique=dict(info=info,decodage_integral=True,sha256=hashlib.sha256(final.read_bytes()).hexdigest()),preuves_examinees=['Planches horodatées des six sources repérées dans assets/48-faid/reperage-*','Portraits des 28 plans avant montage','Captures début/milieu/fin des 28 plans, controle/planche-0.jpg à planche-6.jpg','Miniature, comparaison avec modèle et avant/après des réglages photo','Simulation TikTok à 360 pixels','Reconnaissance vocale Windows sur le son exporté dans _montage/transcription-windows.json'],limites=['Écoute subjective et visionnage continu non réalisés dans cet environnement. Contrôle par captures et reconnaissance du signal audio, qui ne valide pas la diction ni le mix.','Archives peu définies. Hélicoptère lointain dans le film du détenu. Habillage natif conservé sur deux extraits pour préserver le sujet.','Des photographies documentaires du dossier 2018 complètent les séquences réelles, faute de vidéo continue de chaque étape. Les fumigènes sont racontés sur une capture du commando, sans prétendre en montrer le lancement.','Les droits des archives peuvent limiter la diffusion.'],corrections=['Archive mal identifiée de 2013 totalement retirée, remplacée par documents TF1 de 2018','Raccords de reportage avec micro supprimés','Portrait de Faïd recentré','Plan hélicoptère élargi pour préserver le sujet','Miniature recadrée pour supprimer le bandeau du diffuseur'],comparaison_requise=False)
save(P/'controle-livraison.json',report)
d.update(statut='à visionner et écouter',duree=float(v['duration']),comparaison_requise=False);save(P/'histoire.json',d)
index=R/'out/versions-actuelles.json';items=read(index);items=[x for x in items if x.get('numero')!=48];items.append(dict(numero=48,dossier=P.name,statut='a_visionner_et_ecouter',duree=float(v['duration']),revision=now,miniature='miniature.png',comparaison_requise=False));save(index,items)
mini=read(P/'miniature-manifeste.json');mini['statut']='examinée à 360 pixels, comparée au modèle et réglages avant/après examinés';save(P/'miniature-manifeste.json',mini)
print('Livraison préparée',v['duration'])
