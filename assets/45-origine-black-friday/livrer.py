import json,subprocess,hashlib,shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'out/45-origine-black-friday';A=ROOT/'assets/45-origine-black-friday'
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=load(P/'histoire.json');plans=load(P/'plans.json');now=datetime.now(timezone(timedelta(hours=1))).isoformat()
sources=[]
for name in ['F19yTBhAsB0','L52yyJAT2EY','0Cs2xjzAJTU','rZLm9WR1sv4','moderne']:
 m=load(A/(name+'.info.json'));sources.append(dict(fichier=name+'.mp4',chaine=m.get('channel'),titre=m.get('title'),date_publication=m.get('upload_date'),url=m.get('webpage_url'),largeur=m.get('width'),hauteur=m.get('height'),licence=m.get('license') or 'Licence YouTube standard, autorisation non obtenue',extrait_source='60-180 s' if name=='moderne' else 'source complète'))
manifest=[]
for p in plans:
 s=next(x for x in sources if x['fichier']==p['source']);row=dict(p,provenance=s)
 row['entree_source_complete_approximative']=p['entree']+(60 if p['source']=='moderne.mp4' else 0)
 row['largeur_utile_estimee']=round(s['hauteur']*(.70 if p['source']=='L52yyJAT2EY.mp4' else .86 if p['source']=='0Cs2xjzAJTU.mp4' else 1)*9/16)
 manifest.append(row)
save(P/'sources-visuelles.json',manifest)
facts='\n'.join('- '+x['fait']+' : '+x['url'] for x in d['sources_a_verifier'])
video_credits='\n'.join(f"- {s['chaine']} — {s['titre']} — publication {s['date_publication']} — {s['url']}" for s in sources)
photo_credits='''- Tasos Katopodis / Getty Images : clients à l’ouverture d’un magasin, photographie reproduite par HISTORY. https://www.history.com/articles/black-friday-thanksgiving-origins-history
- Ed Betz / AP Photo : policier du comté de Nassau lors d’un Black Friday contemporain, photographie reproduite par HISTORY. Cette image ne représente pas la police de Philadelphie des années 1960. https://www.history.com/articles/black-friday-thanksgiving-origins-history
- Rob Stothard / Getty Images : vitrines Black Friday, photographie reproduite par HISTORY. https://www.history.com/articles/black-friday-thanksgiving-origins-history
- Autres images fixes : photogrammes extraits des séquences documentaires listées ci-dessus ; ce ne sont pas des photos de reportage indépendantes.'''
notes='''Archives de contexte : la cérémonie de la police de Philadelphie est donnée comme datant de 1960 par son diffuseur ; elle ne montre pas une intervention pendant le Black Friday. Le match Army–Navy illustré est celui du 2 décembre 1961, pas le lendemain de Thanksgiving 1961. Les rues et marchés sont datés largement des années 1960–1970 par Kinolibrary. Aucune image n’est présentée ici comme un film du tout premier Black Friday. Plans récents : Brésil, Royaume-Uni, Afrique du Sud dans la compilation Reuters, et Ontario Mills, Californie, dans la promenade Superwalk Tours. Nutella France 2018 et métro londonien exclus.

Les fichiers HISTORY dont le nom contient 1950s ou 1980s illustrent des sections historiques de l’article : leur nom n’est PAS la date de prise de vue. Le panneau de soldes (1950s-1960s...) a été étudié puis écarté de l’export définitif. Les images Mood Media ont été examinées mais écartées : provenance/date précise insuffisamment établies.

Images de tiers : crédits fournis, aucune licence obtenue pour les extraits sous licence standard et photos de presse. Une citation de source ne vaut pas autorisation ; risque de revendication, son coupé ou diffusion limitée par TikTok/YouTube.

Musique : Lily J, Hip Hop 02, Mixkit Stock Music Free License. https://mixkit.co/license/modal/musicFree/
Narration : voix synthétique ElevenLabs Hugo, eleven_v4. Son original des archives coupé. Comparaisons locales avec la vidéo HPB des téléphones validée, non destinées à la publication.'''
for variant in ['videos','photos']:
 w=P/variant
 legend="Le Black Friday : un cauchemar pour les policiers devenu une fête des promos. Bonnes affaires ou piège à achats ?\n\n#BlackFriday #HistoireVraie #HistoiresPasBanales\n\nSources historiques :\n"+facts+'\n\nCrédits des images :\n'+video_credits
 if variant=='photos':legend+='\n'+photo_credits
 legend+='\n\n'+notes+'\n'
 for f in ['legende.txt','publication.txt']:(w/f).write_text(legend,encoding='utf8')
 (w/'CREDITS.md').write_text('# Origine du Black Friday — sources et crédits\n\n'+facts+'\n\n'+video_credits+'\n\n'+(photo_credits+'\n\n' if variant=='photos' else '')+notes,encoding='utf8')
 shutil.copy2(P/'script.txt',w/'script.txt')
 checks={}
 for file in ['final.mp4','comparaison.mp4']:
  f=w/file
  subprocess.run(['ffmpeg','-v','error','-i',str(f),'-map','0:v','-map','0:a','-f','null','-'],check=True,capture_output=True)
  pr=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,duration,width,height:stream_tags=handler_name:stream_disposition=default','-of','json',str(f)]))
  vs=next(s for s in pr['streams'] if s['codec_type']=='video');aud=[s for s in pr['streams'] if s['codec_type']=='audio']
  assert float(vs['duration'])>60
  assert all(abs(float(vs['duration'])-float(a['duration']))<.15 for a in aud)
  if file=='comparaison.mp4':assert len(aud)==2 and aud[1]['disposition']['default']==1
  checks[file]=dict(probe=pr,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),decodage_integral=True)
 assert (w/'comparaison.mp4').stat().st_mtime>=(w/'final.mp4').stat().st_mtime
 report=dict(date=now,statut='version de travail, écoute et mouvement continu non validés',validation_utilisateur=False,technique=checks,
 preuves_examinees=['Sources : reuters.jpg, philadelphie.jpg, police.jpg, football.jpg, moderne.jpg, photos-history.jpg','Captures de début/milieu/fin des 22 plans du MP4 : controle/planche-0.jpg à planche-4.jpg','Première image 0:00, simulation TikTok et comparaison ; voir journal de contrôle pour la dernière passe'],
 constats=['Hook terminé vers 3,4 s, deux plans avant 5 s','Logo SVG HPB validé, lettres transparentes ; aucun bandeau de contexte ni fun fact','Sous-titres bas, mots Black Friday et Big Friday normalisés ; année 1961','Durée vidéo 67,13 s ; comparaison à jour, deux pistes séparées, HPB par défaut'],
 limites=['Archives historiques douces et parfois fortement agrandies ; cette version ne satisfait pas partout le niveau de netteté des sources récentes 4K','Contrôle visuel par captures, pas visionnage continu en temps réel','Pas d’écoute subjective du mix ni de la diction. Transcription indépendante du son exporté tentée : API speech-to-text refusée HTTP 401. Aucun contrôle sonore annoncé comme validé.','Images de contexte : les scènes ne montrent pas la naissance du terme ; voir CREDITS.md','Photos : mélange de photos de presse et de photogrammes documentaires, avec mouvements légers'])
 save(w/'controle-livraison.json',report)
 dv=load(w/'histoire.json');dv['statut']='export de travail à visionner et écouter';save(w/'histoire.json',dv)
d['statut']='deux variantes exportées, contrôles limités documentés';d['exports']={v:dict(video=v+'/final.mp4',comparaison=v+'/comparaison.mp4',legende=v+'/legende.txt',duree=67.133333) for v in ['videos','photos']};save(P/'histoire.json',d)
idx=ROOT/'out/versions-actuelles.json';data=load(idx);data=[x for x in data if x.get('numero')!=45];data.append(dict(numero=45,dossier=P.name,statut='a_visionner_et_ecouter',duree=67.133333,comparaison_a_jour=True,variantes=d['exports'],revision=now));save(idx,data)
print('Crédits, contrôle technique et index mis à jour')
