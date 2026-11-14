from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
S={27:[('France TV','Vendée Globe 96-97 : la course qui a viré au cauchemar - Documentaire complet','Archives 1996-1997 dans un documentaire rétrospectif','https://www.youtube.com/watch?v=UmjAM3qvUew'),],28:[('INA Sport','Résumé OM/Valenciennes','Reportage du 18 juillet 1993, match du 20 mai 1993','https://www.youtube.com/watch?v=L9nURpKZWMo'),('Olympique de Marseille','OM 1-0 MILAN AC 1993 : La fin du match','Finale du 26 mai 1993','https://www.youtube.com/watch?v=gKkRJ4dMTTQ')]}
results=[]
for n in [27,28]:
 dst=OUT/str(n);old=ROOT/'out/revisions-ouverture-14nov-2026'/str(n)
 links='\n'.join(f'{ch} - {title} - {date} - {url}' for ch,title,date,url in S[n])
 original=(old/'legende.txt').read_text(encoding='utf-8');prefix=original.split('Images :')[0] if n==27 else original.split('Photo de Bernard')[0]
 music='Musique :'+original.split('Musique :')[1]
 context=('Images de course, de Dinelli sur Algimouss, du radeau auprès d’Aqua Quorum et du retour des marins. La vue aérienne de Dinelli sur Algimouss semble être une photographie d’époque reprise dans le documentaire ; le fax est également un document historique filmé. Ces deux exceptions sont précisées dans plans.json ; les plans de mer servent de contexte et ne constituent pas des images du chavirage.' if n==27 else 'Vraies archives de VA-OM et de la finale 1993 ; Glassmann, Robert, Eydelie et Tapie dans les archives de l’affaire. Les interviews illustrent les protagonistes : elles ne sont pas des images du procès de 1995. Aucune image ne prétend montrer la remise de l’enveloppe ou son enfouissement.')
 text=prefix+'Images d’archives :\n'+links+'\n\n'+context+'\nSon original des archives retiré.\n'+music
 for f in ['legende.txt','publication.txt']:(dst/f).write_text(text,encoding='utf-8')
 (dst/'CREDITS.md').write_text('# Sources des images - révision du 14 novembre 2026\n\n'+links+'\n\n'+context+'\n\n'+music+'\nLes horodatages et recadrages exacts figurent dans plans.json. Les droits des archives restent détenus par leurs ayants droit.\n',encoding='utf-8')
 story=json.loads((dst/'histoire.json').read_text(encoding='utf-8'));story['revision_archives']={'date':'2026-11-14','sources':S[n],'plans':'plans.json','logo':'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.svg','bandeau':False,'type_post':'videos','contexte':context};(dst/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dst/'final.mp4')]))
 duration=float(probe['format']['duration']);assert duration>60
 result={'numero':n,'date':'2026-11-14','duree':duration,'sha256':hashlib.sha256((dst/'final.mp4').read_bytes()).hexdigest(),'statut':'a_visionner','publication_en_ligne':'non_remplacee','sources':S[n],'preuves_visuelles':['hook-5-secondes.jpg','controle-final-0.jpg','controle-final-1.jpg','controle-final-2.jpg','controle-final-3.jpg','controle-0.jpg','controle-3.jpg','controle-55.jpg','comparaison.jpg'],'controle_technique':'Decodage complet des deux MP4 ; plus de 60 secondes ; comparaison 2 pistes audio ; audio HPB par defaut','audio':'Voix et musique conservees de la revision ouverture, sans nouvelle synthese. Ecoute humaine non effectuee par cet outil.','limites':'Archives anciennes de definition limitee. Plans de contexte identifies dans plans.json et les credits.'}
 (dst/'controle-livraison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');results.append(result)
 im=Image.open(dst/'controle-3.jpg').convert('RGB');d=ImageDraw.Draw(im);d.text((15,20),'Pour toi                       Rechercher',fill='white');d.text((305,310),'♡\n\n+\n\n↗',fill='white');d.rectangle((0,560,360,640),fill='#171717');d.text((15,570),'@histoirespasbanales\nLegende du post...\nSimulation interface TikTok',fill='white');im.save(dst/'apercu-tiktok.jpg')
(OUT/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
p=ROOT/'out/versions-actuelles.json';index=json.loads(p.read_text(encoding='utf-8-sig'))
for row in index:
 if row.get('numero') in [27,28]:
  n=row['numero'];row['revision_proposee_2026_11_14']={'dossier':f'out/revisions-archives-14nov-2026/{n}','statut':'a_visionner','modifications':'Archives epoque, ouverture directe, logo HPB jaune evide sans bandeau','publication_en_ligne':'non_remplacee'}
p.write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
