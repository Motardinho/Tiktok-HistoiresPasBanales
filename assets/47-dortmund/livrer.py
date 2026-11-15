import json,subprocess,hashlib
from pathlib import Path
from datetime import datetime,timezone,timedelta
R=Path(__file__).resolve().parents[2];P=R/'out/47-dortmund-attentat-en-bourse';A=R/'assets/47-dortmund'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=read(P/'histoire.json');plans=read(P/'plans.json');now=datetime.now(timezone(timedelta(hours=1))).isoformat()
sources=[]
for sid in sorted({Path(p['source']).stem for p in plans}):
 x=read(A/(sid+'.info.json'));sources.append(dict(id=sid,chaine=x.get('channel'),titre=x.get('title'),date=x.get('upload_date'),url=x.get('webpage_url'),width=x['width'],height=x['height'],licence=x.get('license') or 'Licence standard ; droits non acquis'))
for p in plans:
 s=next(x for x in sources if x['id']==Path(p['source']).stem)
 p['provenance']=s;p['largeur_utile']=2*round(p['hauteur']*9/16/2);p['nature']='archive réelle du dossier ; son original retiré'
 p['limite']='Archive 720p ou 1080p recadrée : définition inférieure à une prise verticale native. Les plans de tribunal et de police illustrent aussi les faits non filmés.'
save(P/'sources-visuelles.json',plans)
credits='\n'.join(f"{x['chaine']} - {x['titre']} - {x['date']} - {x['url']}" for x in sources)
facts='\n'.join(x['fait']+' : '+x['url'] for x in d['sources_a_verifier'])
music='Musique : Eugenio Mininni, Masking the Masters, Mixkit Stock Music Free License. https://mixkit.co/free-stock-music/tag/documentary/ - https://mixkit.co/license/modal/musicFree/'
legend='Un attentat contre des footballeurs pour miser sur la chute du club en Bourse. 14 ans : suffisant ou trop peu ?\n\n#histoirevraie #HistoiresPasBanales #Football #FaitsDivers\n\nArchives :\n'+credits+'\n\nSources des faits :\n'+facts+'\n\n'+music+'\nNarration originale HPB, voix synthétique Hugo. Images du bus, des suites de l’attentat et du procès ; aucune reconstitution de l’explosion.\n'
for name in ['legende.txt','publication.txt']:(P/name).write_text(legend,encoding='utf8')
notes='''Les achats financiers, les réservations et l’interpellation ne sont pas montrés directement. Ils sont racontés sur des images du site, de l’enquête et du procès. Le portrait de Marc Bartra provient de sa venue au tribunal ; il ne représente pas le moment de sa blessure. La courbe BVB dans le reportage est un document de contexte, pas le compte de l’auteur ni une animation inventée. Les images du tribunal diffusées par euronews incluent des archives du procès.
Les sources 360p ont été écartées du montage. Les plans retenus sont en 720p et 1080p avant recadrage ; une douceur reste visible, notamment la nuit. Aucun plan générique Pexels ni image générée.
Le communiqué du parquet rapporte 15000 options et l’achat via la connexion de l’hôtel. Aucun montant de gain non établi n’est raconté. Le nombre de tentatives de meurtre diffère entre presse et jugement (29 dans le dispositif du jugement consulté) : ce chiffre a été omis.
La citation des sources ne vaut pas licence : risques de revendication, de son coupé ou de diffusion limitée sur TikTok/YouTube.
Comparaison non livrée selon la nouvelle instruction de Marc. Un export était déjà terminé quand cette instruction est arrivée ; il reste un fichier de travail hors livraison.
'''
(P/'CREDITS.md').write_text('# Dortmund - archives et sources\n\n'+credits+'\n\n'+facts+'\n\n'+music+'\n\n'+notes,encoding='utf8')
final=P/'final.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(final),'-map','0:v','-map','0:a','-f','null','-'],check=True,capture_output=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,duration,width,height','-of','json',str(final)]))
v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert float(v['duration'])>60 and abs(float(v['duration'])-float(a['duration']))<.15
stats=subprocess.run(['ffmpeg','-hide_banner','-i',str(final),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,encoding='utf8',errors='replace',check=True)
(P/'_montage/analyse-audio.txt').write_text(stats.stderr,encoding='utf8')
report=dict(date=now,statut='version à visionner et écouter ; contrôle visuel par captures effectué, écoute subjective restante',validation_utilisateur=False,
 technique=dict(informations=info,sha256=hashlib.sha256(final.read_bytes()).hexdigest(),decodage_integral=True),
 preuves_examinees=['Sources : planches horodatées AFP, euronews, DW et Al Jazeera dans assets/47-dortmund/reperage-*','Recadrages : portrait-0 à portrait-4 puis corrections','Export : controle/planche-0.jpg à planche-6.jpg, début/milieu/fin des 27 plans ; planches 2, 4, 5, 6 réexaminées après correction','Première image et aperçu TikTok à 360 pixels','Miniature : miniature-comparaison.jpg et miniature-reglages.jpg, puis seconde version avec regard visible et fond noirci','Son exporté : analyse du signal et reconnaissance vocale Windows fr-FR dans _montage/transcription-windows.json ; pas simple lecture des timings ElevenLabs'],
 corrections=['Restes de filigranes retirés par recadrage des plans 19 et 24','Plan final de véhicule trop flou remplacé par sortie des supporters','Plan 8 remplacé pour éviter passage vers un autre sujet à la fin de extrait','Ponctuation isolée rattachée au mot précédent avant génération des sous-titres','Nombre de tentatives de meurtre retiré face à divergence presse/jugement'],
 limites=['Pas de lecture continue en temps réel ni écoute subjective : entrée audio non prise en charge par cet environnement. Une écoute humaine reste requise pour juger diction et mix.','Reconnaissance Windows imparfaite : retrouve le récit, la connexion Internet, les deux séjours et les 14 ans, mais confond certains noms et mots. Elle ne prouve pas leur mauvaise prononciation.','Archives nocturnes et 720p plus douces que vidéo native ; aucune reconstitution des actes non filmés.','Réutilisation soumise aux droits des diffuseurs.'],
 comparaison=dict(requise=False,motif='Marc : plus besoin de comparaison à avenir, 14 novembre 2026'),
 constats=['67,13 secondes, accroche orale complète avant cinq secondes, deux plans avant 3,52 secondes','Logo validé et sous-titres seuls ; aucun bandeau de contexte ni de fun fact','Vraies archives de affaire, sons originaux retirés ; narration originale','Aucune publication effectuée'])
save(P/'controle-livraison.json',report)
d.update(statut='à visionner et écouter',duree=float(v['duration']),comparaison_requise=False);save(P/'histoire.json',d)
index=R/'out/versions-actuelles.json';items=read(index);items=[x for x in items if x.get('numero')!=47];items.append(dict(numero=47,dossier=P.name,statut='a_visionner_et_ecouter',duree=float(v['duration']),comparaison_requise=False,revision=now,miniature='miniature.png'));save(index,items)
mini=read(P/'miniature-manifeste.json');mini['statut']='examinée à 360 pixels et comparée au modèle ; en attente de retour utilisateur';mini['preuves']=['miniature-comparaison.jpg','miniature-reglages.jpg'];save(P/'miniature-manifeste.json',mini)
print('Vidéo décodée, légende et contrôle enregistrés. Durée :',v['duration'],flush=True)
