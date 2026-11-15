import json,subprocess,hashlib
from pathlib import Path
from datetime import datetime,timezone,timedelta
R=Path(__file__).resolve().parents[2];P=R/'out/46-larme-de-verre';A=R/'assets/46-larme-de-verre'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=load(P/'histoire.json');plans=load(P/'plans.json');now=datetime.now(timezone(timedelta(hours=1))).isoformat()
sources=[]
for sid in sorted({Path(p['source']).stem for p in plans}):
 x=load(A/(sid+'.info.json'));sources.append(dict(id=sid,chaine=x.get('channel'),titre=x.get('title'),date=x.get('upload_date'),url=x.get('webpage_url'),width=x['width'],height=x['height'],licence=x.get('license') or 'Licence standard, autorisation de réutilisation non obtenue'))
for p in plans:
 s=next(s for s in sources if s['id']==Path(p['source']).stem)
 p['provenance']=s;p['largeur_utile']=2*round(p['hauteur']*9/16/2);p['nature']='séquence réelle, son original coupé, ralenti conservé quand présent dans la source'
 p['limite_definition']='source 1080p recadrée ; douceur visible du ralenti' if s['height']==1080 else 'source 4K, recadrage de plus de 1000 pixels utiles'
save(P/'sources-visuelles.json',plans)
facts='\n'.join('- '+x['fait']+' : '+x['url'] for x in d['sources_a_verifier'])
credits='\n'.join(f"- {x['chaine']} - {x['titre']} - {x['date']} - {x['url']}" for x in sources)
notes="""Musique : Eugenio Mininni, Masking the Masters, Mixkit Stock Music Free License. https://mixkit.co/free-stock-music/tag/documentary/ ; https://mixkit.co/license/modal/musicFree/
Narration originale HPB : voix synthétique ElevenLabs Hugo, eleven_v4. Aucun texte ni son original des vidéastes repris.
La vitesse évoquée est celle des fissures, pas celle des éclats. La tête peut céder sous une charge suffisante. Les images polarisées montrent des contraintes dans le verre ; ce ne sont pas des couleurs naturelles.
Les ralentis proviennent des sources, sans accélération destinée à inventer une performance. Archives de recherche et macro 1080p plus douces que les passages 4K.
Créditer les sources ne vaut pas autorisation : extraits sous licence standard, susceptibles de revendication, de son coupé ou de diffusion limitée sur TikTok/YouTube.
Comparaison locale : référence HPB téléphones validée à gauche, nouvelle vidéo à droite ; elle n'est pas destinée à la publication."""
legend="Un marteau sur la tête… mais une petite rupture de la queue suffit à tout fragmenter. Tu connaissais les larmes de verre ?\n\n#Science #Insolite #Verre #HistoiresPasBanales\n\nSources scientifiques :\n"+facts+'\n\nSources des séquences :\n'+credits+'\n\n'+notes+'\n'
for name in ['legende.txt','publication.txt']:(P/name).write_text(legend,encoding='utf8')
(P/'CREDITS.md').write_text('# Larme de verre - sources\n\n'+facts+'\n\n'+credits+'\n\n'+notes,encoding='utf8')
checks={}
for name in ['final.mp4','comparaison.mp4']:
 f=P/name
 subprocess.run(['ffmpeg','-v','error','-i',str(f),'-map','0:v','-map','0:a','-f','null','-'],check=True,capture_output=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,duration,width,height:stream_tags=handler_name:stream_disposition=default','-of','json',str(f)]))
 v=next(s for s in info['streams'] if s['codec_type']=='video');aa=[s for s in info['streams'] if s['codec_type']=='audio']
 assert float(v['duration'])>60
 assert all(abs(float(v['duration'])-float(a['duration']))<.15 for a in aa)
 if name=='comparaison.mp4':assert len(aa)==2 and aa[1]['disposition']['default']==1
 checks[name]=dict(informations=info,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),decodage_integral=True)
assert (P/'comparaison.mp4').stat().st_mtime >= (P/'final.mp4').stat().st_mtime
# Analyse du signal effectivement exporté, distincte de la transcription TTS.
stats=subprocess.run(['ffmpeg','-hide_banner','-i',str(P/'final.mp4'),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,encoding='utf8',errors='replace')
(P/'_montage/analyse-audio.txt').write_text(stats.stderr,encoding='utf8')
report=dict(date=now,statut='première version à visionner et écouter',validation_utilisateur=False,technique=checks,
 preuves_examinees=['Sources : planches horodatées dans assets/46-larme-de-verre/reperage-*','Rendu : controle/planche-0.jpg à planche-5.jpg, début/milieu/fin des 22 plans','Première image, simulation TikTok à 360 pixels et miniature comparée à la référence science','Son réellement exporté : reconnaissance vocale Windows fr-FR, transcription-windows.json. Le moteur retrouve notamment la chaîne rupture-fracture-fragments et 6000 kilomètres à l’heure.'],
 corrections=['Raccords source vers animation et interview supprimés','Recadrages de la queue et des filigranes ajustés','Sous-titres 90 px sans fondu parasite','Presse : séquence 4K plus nette retenue ; ralenti 380000 fps pixellisé écarté'],
 limites=['Contrôle visuel par captures réelles et séquences de photogrammes ; pas de visionnage continu en temps réel','Reconnaissance vocale indépendante imparfaite : pas une validation subjective de diction et de mix. Écoute humaine encore nécessaire.','Certaines macros et archives de laboratoire sont en 1080p et restent douces après recadrage, largeur utile 506 à 562 px environ','Réutilisation des images tierces non autorisée par une licence acquise, risque de revendication.'],
 constats=['65,2 secondes, deux plans avant cinq secondes, accroche directe','Aucun encart de contexte ou fun fact ; logo validé ; sous-titres bas','Pas de publication effectuée'])
save(P/'controle-livraison.json',report)
d['statut']='première version à visionner et écouter';d['duree']=65.2;d['tiktokabilite']['verdict']='adapté sous réserve';d['tiktokabilite']['limites']=report['limites'][2];save(P/'histoire.json',d)
index=R/'out/versions-actuelles.json';rows=load(index);rows=[x for x in rows if x.get('numero')!=46];rows.append(dict(numero=46,dossier=P.name,statut='a_visionner_et_ecouter',duree=65.2,comparaison_a_jour=True,revision=now,miniature='miniature.png'));save(index,rows)
mini=load(P/'miniature-manifeste.json');mini['statut']='examinée à 360 pixels, en attente du retour de Marc';save(P/'miniature-manifeste.json',mini)
print('Livraison documentée, décodage réussi ; écoute humaine reste à faire.',flush=True)
