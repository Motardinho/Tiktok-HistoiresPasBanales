"""Montage archives 47. Points de coupe calés sur la voix Hugo produite le 14/11/2026."""
import sys,json,subprocess,shutil,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
import yaml
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
from monter_lot_21_23 import caption_words
from narrateur import assemble
P=R/'out/49-top-3-records-vitesse-sans-moteur';A=R/'assets/49-vitesse-sans-moteur';M=P/'_montage';Q=P/'controle';Q.mkdir(exist_ok=True)
d=json.loads((P/'histoire.json').read_text(encoding='utf8'));tim=json.loads((M/'timings-oraux.json').read_text(encoding='utf8'))
S='pLxmZ9M3b2k'; J='yNLc3iCntQM'; P97='tw5doHjd0Ug'; D='dEXyNhIj2Z4'; W='CoUmgMhn2iY'; F='FHtvDA0W34I'; H='Hz2F_S3Tl0Y'; AV='9XThBa6NMK0'
rows=[
 (1.28,S,12.0,.5,1080,0,'Accroche : vue casque d un skieur de vitesse, Vars 2023, sans nom ni rang'),
 (2.43,W,1050,.67,2160,0,'Accroche : cycliste dans l abri du dragster, sans nom ni rang'),
 (5.28,AV,138.5,.72,2160,0,'Airbus A380 en croisière, raccord « avion de ligne »'),
 (7.20,J,90.11,.57,1080,0,'N°3 : départ réel d un skieur de vitesse à Vars'),
 (8.88,S,36.2,.56,1080,0,'Simon Billy identifiable au mot « Simon Billy »'),
 (10.40,J,97.41,.5,1080,0,'Skieur lancé à pleine vitesse, Vars 2023'),
 (12.04,S,39.31,.40,1080,0,'Simon Billy avec le panneau 255.500'),
 (14.72,D,9.27,.5,1080,0,'Vars et les Alpes vus du ciel, jour du record'),
 (16.00,S,42.0,.5,1080,0,'Simon Billy fête le record du monde'),
 (17.44,S,8.0,.5,1080,0,'Piste de Chabrières vue du ciel, raccord « cette piste »'),
 (20.92,J,93.6,.56,1080,0,'Drone qui suit un skieur qui accélère sur la piste'),
 (21.89,J,129.0,.5,1080,0,'Relance : skieur de vitesse avec son casque profilé'),
 (23.48,P97,0.3,.32,480,0,'Archive 1997 : départ à Vars'),
 (27.04,P97,16.0,.5,480,0,'Archive 1997 : skieur lancé à Vars, raccord « son père », identité non certifiée'),
 (28.88,W,529.17,.42,2160,0,'N°2 : dragster qui tracte la cycliste à Bonneville'),
 (31.12,W,1098.41,.47,2160,0,'Denise Mueller-Korenek identifiable au mot de son nom'),
 (33.04,W,1060.0,.68,2160,0,'Run réel dans l abri du dragster'),
 (35.28,W,24.38,.5,2160,0,'Bonneville Salt Flats, États-Unis'),
 (36.88,W,300.0,.5,2160,0,'Le vélo du record, grand plateau visible'),
 (38.68,W,320.0,.45,2160,0,'Le vélo et sa transmission démultipliée'),
 (39.90,W,279.72,.5,2160,0,'Le vrai dragster rouge de Shea Holbrook, vu de face'),
 (40.84,W,560.0,.4,2160,0,'Dragster qui tracte la cycliste'),
 (42.72,W,1040.0,.62,2160,0,'Elle pédale dans l abri du dragster'),
 (44.59,W,540.0,.5,2160,0,'Relance : vue de l abri, cycliste dans le sillage'),
 (46.88,W,998.64,.5,2160,0,'Relance : run vu de l avant, « ce vélo »'),
 (48.92,F,61.44,.5,1080,0,'N°1 : Baumgartner en chute libre depuis la capsule'),
 (49.88,F,0.3,.55,1080,0,'Lancement du ballon, 2012'),
 (51.04,F,11.5,.55,1080,0,'Felix Baumgartner identifiable dans son casque'),
 (54.00,F,50.5,.6,1080,0,'Debout sur la marche de la capsule, puis saut'),
 (56.24,H,53.83,.5,1080,0,'Vue caméra du sauteur en chute libre, Terre en dessous'),
 (57.92,H,108.92,.45,1080,0,'Baumgartner en chute, vu depuis la capsule'),
 (59.84,F,23.5,.45,1080,0,'Public qui suit la mission en direct'),
 (61.80,H,15.26,.5,1080,0,'Équipe de la mission qui suit le saut en direct'),
 (63.64,F,84.0,.62,1080,0,'Chute : atterrissage, « il est juste tombé »'),
 (65.56,W,526.0,.35,2160,0,'Chute : dragster qui tire la cycliste'),
 (67.92,D,65.0,.5,1080,0,'Chute : skis et chaussures d un skieur de vitesse, « que ses skis »'),
 (70.00,F,49.6,.6,1080,0,'Question finale : Baumgartner au bord de la capsule'),
 (round(tim['duration']*30)/30,J,47.35,.4,1080,0,'Signature : Simon Billy et le panneau 255.500')]
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
 graph=f"[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=9[a];[3:a]volume='if(between(t,46.3,46.88),0,0.045)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={start-2.5}:d=2.5[m];[a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[out]"
 ff(['-i','base.mp4','-i','voix.mp3','-loop',1,'-i','logo.png','-stream_loop',-1,'-i',R/'assets/musique/mixkit/voitures.mp3','-filter_complex_threads',1,'-filter_complex',graph,'-map','[v]','-map','[out]','-t',start,'-c:v','libx264','-preset','veryfast','-crf',18,'-threads',3,'-c:a','aac','-b:a','192k','-movflags','+faststart',P/'final.mp4'],M)
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

