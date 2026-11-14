from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
def ff(a):subprocess.run(['ffmpeg','-v','error','-y',*map(str,a)],check=True)
results=[]
for n in [27,28]:
 d=OUT/str(n);old=ROOT/'out/revisions-habillage-14nov-2026'/str(n)
 times=([18,36,52.8,55,60.2,61] if n==27 else [6,8,52.6,54,55.8,57])
 sheet=Image.new('RGB',(1080,1280))
 for i,t in enumerate(times):
  f=d/f'verification-{t}.jpg';ff(['-ss',t,'-i',d/'final.mp4','-frames:v','1','-vf','scale=360:640',f]);sheet.paste(Image.open(f),(i%3*360,i//3*640))
 sheet.save(d/'controle-habillage.jpg')
 audio=[]
 for f in [old/'final.mp4',d/'final.mp4']:
  audio.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-f','hash','-hash','sha256','-'],text=True).strip())
 assert audio[0]==audio[1]
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(d/'final.mp4')]))
 duration=float(info['format']['duration']);assert duration>60
 compare=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(d/'comparaison.mp4')]))
 audios=[s for s in compare['streams'] if s['codec_type']=='audio'];assert len(audios)==2 and audios[0]['disposition']['default']==1
 result={'numero':n,'date':'2026-11-14','statut':'a_visionner','duree':duration,'sha256':hashlib.sha256((d/'final.mp4').read_bytes()).hexdigest(),'correction':'Suppression de tous les bandeaux, y compris fun facts ; logo decale sous la zone de recherche ; sous-titres conserves','logo_bbox':Image.open(d/'logo.png').getbbox(),'position_logo':'Haut visible a 300 px ; marge droite 124 px en 1080x1920. Verification sur simulation, pas dans application TikTok.','audio_pcm_identique':True,'ecoute':'Pas de nouvelle ecoute ; piste strictement identique verifiee par hash PCM','comparaison':'Deux pistes audio, HPB par defaut, issue du nouvel export','preuves':['controle-habillage.jpg','controle-final-3.jpg','comparaison.jpg'],'publication_en_ligne':'Non remplacee'}
 (d/'controle-livraison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');results.append(result)
 story=json.loads((d/'histoire.json').read_text(encoding='utf-8'));story['revision_habillage']=result;(d/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
 im=Image.open(d/'controle-55.jpg').convert('RGB');draw=ImageDraw.Draw(im);draw.text((12,15),'Pour toi',fill='white');draw.rounded_rectangle((12,38,348,76),radius=8,fill='#333333');draw.text((24,50),'Rechercher',fill='white');draw.rectangle((0,565,360,640),fill='#171717');draw.text((12,575),'@histoirespasbanales\nLegende...\nSimulation du lecteur TikTok',fill='white');im.save(d/'apercu-tiktok.jpg')
(OUT/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
p=ROOT/'out/versions-actuelles.json';index=json.loads(p.read_text(encoding='utf-8-sig'))
for row in index:
 if row.get('numero') in [27,28]:row['revision_proposee_2026_11_14']={'dossier':f'out/revisions-sans-bandeaux-14nov-2026/{row["numero"]}','statut':'a_visionner','modifications':'Sans aucun bandeau ni encart de fun fact','publication_en_ligne':'non_remplacee'}
p.write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
