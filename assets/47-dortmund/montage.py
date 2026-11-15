"""Montage archives 47. Points de coupe calés sur la voix Hugo produite le 14/11/2026."""
import sys,json,subprocess,shutil,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
import yaml
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
from monter_lot_21_23 import caption_words
from narrateur import assemble
P=R/'out/47-dortmund-attentat-en-bourse';A=R/'assets/47-dortmund';M=P/'_montage';Q=P/'controle';Q.mkdir(exist_ok=True)
d=json.loads((P/'histoire.json').read_text(encoding='utf8'));tim=json.loads((M/'timings-oraux.json').read_text(encoding='utf8'))
E='pHh8Fv8HfcQ';F='nR0QCVgongM';B='PDsHpswbOMg';S='K8LMgCVfUeg';J='45Opoq89Lfc';C='X97z19KgFwM';D='1KyH8bjNwTg'
# Fin HPB, source, entrée, centre x relatif, hauteur source, haut source, description.
rows=[
 (1.92,D,.2,.66,720,0,'Vrai bus de Dortmund identifiable par son nom et sa porte ouverte, après attentat'),
 (3.52,E,14.2,.53,720,0,'Menottes retirées au prévenu au tribunal, archives du procès'),
 (6.24,J,67,.51,860,0,'Supporters devant le stade, nuit du 11 avril 2017'),
 (8.08,S,0,.52,720,0,'Supporters de Dortmund quittant le stade après le report'),
 (10.36,S,30.2,.48,720,0,'Sortie des supporters le soir du report'),
 (13.76,D,11.0,.48,720,0,'Vitre détruite du vrai bus, après attentat'),
 (16.12,E,50.8,.52,720,0,'Marc Bartra au tribunal : suite de affaire, pas scène de blessure'),
 (18.0,S,12,.47,720,0,'Évacuation du stade après report, AFP'),
 (21.52,E,31.1,.52,720,0,'Auteur au tribunal, archives du procès'),
 (24.4,E,37.1,.49,650,45,'Écran filmé montrant la cotation BVB, contexte financier'),
 (26.8,E,35.0,.47,650,45,'Document financier BVB filmé, contexte de cotation'),
 (28.88,E,37.2,.50,650,45,'Courbe BVB réellement filmée ; ne représente pas son compte'),
 (31.36,E,31.1,.51,720,0,'Auteur au tribunal, novembre 2018'),
 (33.4,J,32.1,.50,850,0,'Bus et secours sur les lieux, après explosions'),
 (36.36,E,12.0,.60,680,20,'Prévenu et agent de justice au tribunal'),
 (38.84,D,63.0,.51,720,0,'Abords réels du site sous contrôle policier, contexte hôtel'),
 (41.56,J,24,.53,800,0,'Police à la conférence du 11 avril, contexte enquête sans reprendre déclarations'),
 (45.0,F,28.3,.49,720,0,'Presse au procès ; achat par Internet raconté, non filmé'),
 (47.92,D,65.0,.51,720,0,'Abords réels du site de attentat, contexte des réservations'),
 (50.93,E,28.0,.42,660,60,'Auteur au tribunal, contexte de préparation établi par enquête'),
 (53.0,D,60,.58,720,0,'Voiture de police sur le site de attentat'),
 (55.0,E,8.1,.58,720,0,'Tribunal au jugement de novembre 2018'),
 (57.52,E,1.0,.43,720,0,'Prévenu escorté à audience, pas archive de interpellation'),
 (59.72,E,22,.39,720,0,'Président du tribunal à audience de novembre 2018'),
 (61.8,E,28.4,.42,660,60,'Prévenu debout au tribunal'),
 (64.51,E,31.6,.52,720,0,'Prévenu au tribunal : question sur peine'),
 (round(tim['duration']*30)/30,S,30.2,.48,720,0,'Supporters quittant le stade après report, fin du récit')]
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
 extra=',eq=gamma=1.15:brightness=0.02:saturation=1.03' if p['numero']==0 else ',eq=gamma=1.12:brightness=0.012:saturation=1.03' if p['source'].startswith((B,J)) else ''
 return f"crop={w}:{h}:min(max(iw*{p['centre']}-{w}/2\\,0)\\,iw-{w}):{p['haut']},scale=1080:1920:flags=lanczos,setsar=1"+extra
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
 graph=f"[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=9[a];[3:a]volume='if(between(t,38.3,38.84),0,0.045)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={start-2.5}:d=2.5[m];[a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[out]"
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
