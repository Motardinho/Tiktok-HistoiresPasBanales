"""Montage archives 47. Points de coupe calés sur la voix Hugo produite le 14/11/2026."""
import sys,json,subprocess,shutil,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
import yaml
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
from monter_lot_21_23 import caption_words
from narrateur import assemble
P=R/'out/48-faid-evasion-helicoptere';A=R/'assets/48-faid';M=P/'_montage';Q=P/'controle';Q.mkdir(exist_ok=True)
d=json.loads((P/'histoire.json').read_text(encoding='utf8'));tim=json.loads((M/'timings-oraux.json').read_text(encoding='utf8'))
C='rz7MsZ4KK54'; B='suJa80TNlLo'; H='S6uGa2p7PfU'; F='99EQ3yqL8Pg'; V='LEDq7qdD2D8'
rows=[
 (2.97,C,28.2,.51,900,45,'Vrai hélicoptère récupéré après évasion, ouverture sur appareil'),
 (5.8,V,30,.49,740,170,'Vraie vidéo du détenu derrière les barreaux'),
 (7.56,B,48,.5,500,12,'Extérieur réel de la prison de Réau'),
 (9.48,B,53,.5,510,20,'Bâtiments réels de Réau'),
 (10.88,F,7,.68,500,10,'Rédoine Faïd dans une archive antérieure reprise par BFMTV, identification'),
 (12.72,C,48,.5,850,60,'Parloir filmé le jour de évasion'),
 (15.64,C,22,.51,900,45,'Cour filmée pendant évasion, contexte arrivée'),
 (17.4,H,0,.5,510,0,'Vrai appareil récupéré après évasion, contexte pilote otage non filmé'),
 (19.92,C,25,.51,900,45,'Cour de Réau pendant opération, contexte atterrissage'),
 (21.52,C,34,.5,900,45,'Commando dans cour, vidéo de surveillance'),
 (23.56,C,36,.5,900,45,'Fumigènes dans les locaux, vraie vidéosurveillance'),
 (27.44,C,39.8,.53,850,100,'Commando ouvrant passage, vidéosurveillance'),
 (30.48,C,44.8,.49,850,90,'Progression du commando dans couloir'),
 (33.72,C,34.5,.5,900,45,'Progression dans couloir sous caméra'),
 (35.44,F,7,.68,500,10,'Portrait vidéo de Faïd pour identification'),
 (38.29,B,48,.5,500,12,'Parloir du jour de évasion, contexte visite avancée'),
 (40.84,B,53,.5,500,12,'Parloir réel, prétexte football raconté, aucun match montré'),
 (43.84,V,47.7,.5,1080,0,'Appareil en vol filmé par le détenu'),
 (45.8,V,33,.49,740,170,'Détenu filme à travers ses barreaux'),
 (48.12,V,49,.5,1080,0,'Hélicoptère lointain dans le ciel, film du détenu'),
 (50.6,H,17,.5,510,0,'Appareil à Gonesse récupéré par enquêteurs'),
 (52.24,H,60,.5,510,0,'Appareil chargé dans camion pour analyse'),
 (54.56,F,7,.68,500,10,'Archive identification Faïd, contexte cavale'),
 (56.6,C,.2,.5,900,45,'Contrôle policier pendant la recherche, pas son interpellation'),
 (58.04,B,48,.5,510,20,'Prison de Réau, contexte retour en détention'),
 (60.37,B,53,.5,510,20,'Extérieur prison, contexte condamnation'),
 (62.32,C,27.8,.51,900,45,'Rappel de la fuite réelle'),
 (round(tim['duration']*30)/30,B,54,.5,500,12,'Prison de Réau, conclusion')]
plans=[];start=0
for i,(end,src,at,cx,h,y,note) in enumerate(rows):
 end=round(end*30)/30
 plans.append(dict(numero=i,start=start,duration=end-start,frames=round((end-start)*30),source=src+'.mp4',entree=at,centre=cx,hauteur=h,haut=y,action=note));start=end
(P/'plans.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2),encoding='utf8')
def ff(args,cwd=R):
 r=subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],cwd=cwd,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf8',errors='replace')[-3000:])
def vf(p):
 h=p['hauteur'];w=2*round(h*9/16/2)
 return f"crop={w}:{h}:min(max(iw*{p['centre']}-{w}/2\\,0)\\,iw-{w}):{p['haut']},scale=1080:1920:flags=lanczos,setsar=1,eq=gamma=1.04:saturation=1.03"

def preview():
 for k in range(0,len(plans),6):
  sh=Image.new('RGB',(1080,math.ceil(len(plans[k:k+6])/3)*665),'#161616');dr=ImageDraw.Draw(sh)
  for j,p in enumerate(plans[k:k+6]):
   f=A/f"cadre-{p['numero']:02}.jpg";ff(['-ss',p['entree']+.3,'-i',A/p['source'],'-vf',vf(p),'-frames:v',1,f]);sh.paste(Image.open(f).resize((360,640)),(j%3*360,j//3*665));dr.text((j%3*360+5,j//3*665+642),f"{p['numero']} - {p['start']:.2f}s",fill='white')
  sh.save(A/f'portrait-{k//6}.jpg')
def subtitles():
 cfg=yaml.safe_load((R/'config.yaml').read_text(encoding='utf8'));cfg['render'].update(subtitle_size=90,words_per_caption=4,subtitle_wrap=19)
 words=caption_words(tim['words'],d['affichage']);words[0]['start']=0
 # Fermer la ponctuation avec le mot précédent, avant découpage des sous-titres.
 merged=[]
 for w in words:
  if w['w'] in [':','?','!',';',',','.'] and merged:
   merged[-1]['w']+=('\u00a0' if w['w'] in [':','?','!',';'] else '')+w['w'];merged[-1]['end']=w['end']
  else:merged.append(w.copy())
 assemble.write_subtitles(cfg,merged,M/'sous-titres.ass')
 lines=[]
 for l in (M/'sous-titres.ass').read_text(encoding='utf8').splitlines():
  if l.startswith('Dialogue:'):
   parts=l.split(',',9);parts[9]=r'{\an2\pos(500,1370)\fs90\fsp0}'+parts[9].replace(r'{\fad(0,90)}','');l=','.join(parts)
  lines.append(l)
 (M/'sous-titres.ass').write_text('\n'.join(lines)+'\n',encoding='utf8');shutil.copy2(R/'assets/fonts/Poppins-ExtraBold.ttf',M/'police.ttf')
 import resvg_py
 logo=resvg_py.svg_to_bytes(svg_path=str(R/'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.svg'),width=240,height=240)
 import io
 canvas=Image.new('RGBA',(1080,1920));canvas.alpha_composite(Image.open(io.BytesIO(logo)).convert('RGBA'),(734,272));canvas.save(M/'logo.png')
def render(p):
 ff(['-ss',p['entree'],'-i',A/p['source'],'-vf',vf(p)+',fps=30,format=yuv420p,setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709','-frames:v',p['frames'],'-an','-c:v','libx264','-preset','veryfast','-crf',18,'-threads',2,M/f"plan-{p['numero']:02}.mp4"])
def build(refresh=True):
 subtitles()
 if refresh:
  with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,plans))
 (M/'concat.txt').write_text(''.join(f"file 'plan-{p['numero']:02}.mp4'\n" for p in plans),encoding='ascii')
 ff(['-f','concat','-safe',0,'-i','concat.txt','-c','copy','base.mp4'],M)
 graph=f"[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=9[a];[3:a]volume='if(between(t,37.7,38.29),0,0.045)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={start-2.5}:d=2.5[m];[a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[out]"
 ff(['-i','base.mp4','-i','voix.mp3','-loop',1,'-i','logo.png','-stream_loop',-1,'-i',R/'assets/musique/mixkit/espace.mp3','-filter_complex_threads',1,'-filter_complex',graph,'-map','[v]','-map','[out]','-t',start,'-c:v','libx264','-preset','veryfast','-crf',18,'-threads',3,'-c:a','aac','-b:a','192k','-movflags','+faststart',P/'final.mp4'],M)
 print('Export',start,flush=True)
if __name__=='__main__':
 if sys.argv[1]=='preview':preview()
 elif sys.argv[1]=='build':build()
 elif sys.argv[1]=='patch':
  for n in sys.argv[2:]:render(plans[int(n)])
  build(False)
 elif sys.argv[1]=='compare':
  from comparer_lot_16_18 import compare
  compare(P)

