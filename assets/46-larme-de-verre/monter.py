import sys,json,shutil,subprocess,math,importlib.util
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import yaml,resvg_py
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from monter_lot_21_23 import caption_words
from narrateur import assemble
P=ROOT/'out/46-larme-de-verre';A=ROOT/'assets/46-larme-de-verre';M=P/'_montage';Q=P/'controle';Q.mkdir(exist_ok=True)
d=json.loads((P/'histoire.json').read_text(encoding='utf8'));tim=json.loads((M/'timings-oraux.json').read_text(encoding='utf8'))
S='xe-f4gokRBs';U='lt-zvsGvtqg';H='A6NUNroyUys';T='tRUngxK2yXY'
# fin cible, source, entrée, centre horizontal, hauteur source, haut source, action
rows=[
 (2,S,69.1,.55,900,180,'Marteau sur tête intacte'),
 (4.6,U,.1,.40,850,230,'Forme de la larme'),
 (7,U,14.3,.43,1000,0,'Marteau et tête'),
 (9.3,U,57,.52,1000,0,'Tête et queue courbée'),
 (11.48,S,277.7,.50,980,40,'Queue filiforme en spirale, observation entre filtres'),
 (14.5,H,13.35,.60,2100,0,'Verre en fusion, puis chute dans eau'),
 (17.96,U,102.65,.48,1000,0,'Chute et trempe dans eau'),
 (21,U,89,.47,1000,0,'Verre encore chaud en formation'),
 (24,U,104,.46,1000,0,'Refroidissement réel dans eau'),
 (27.88,U,69,.50,1000,0,'Larme entre filtres polarisants'),
 (30.5,U,73.5,.63,940,0,'Franges photoélastiques de la tête'),
 (33.44,S,82,.57,900,180,'Marteau : tête résistante, avant rupture'),
 (35.5,S,172.1,.60,920,0,'Queue intacte et pince au ralenti'),
 (39.08,S,160.3,.43,960,50,'Rupture de queue puis désintégration'),
 (42.5,S,153.1,.38,960,50,'Front de fracture remontant la courbe'),
 (45.24,S,167.4,.60,920,0,'Tête qui se fragmente'),
 (48.3,U,47.4,.50,1000,0,'Archive scientifique de fragmentation'),
 (52.88,S,173.4,.60,920,0,'Propagation ultrarapide au ralenti'),
 (55.1,H,35,.49,2050,70,'Compression sous presse'),
 (58.56,H,38.5,.49,2050,70,'Rupture de la tête sous presse'),
 (61.5,S,151.3,.38,920,0,'Larme intacte et début de rupture de queue'),
 (round(tim['duration']*30)/30,H,41,.49,2050,70,'Fragmentation sous presse au ralenti')
]
plans=[];start=0
for n,(end,src,at,cx,h,y,action) in enumerate(rows):
 end=round(end*30)/30
 plans.append(dict(numero=n,start=start,duration=end-start,frames=round((end-start)*30),source=src+'.mp4',entree=at,centre=cx,hauteur=h,haut=y,action=action))
 start=end
(P/'plans.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2),encoding='utf8')
def ff(args,cwd=ROOT):
 r=subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],cwd=cwd,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf8',errors='replace')[-4000:])
def vf(p):
 h=p['hauteur'];w=2*round(h*9/16/2)
 return f"crop={w}:{h}:min(max(iw*{p['centre']}-{w}/2\\,0)\\,iw-{w}):{p['haut']},scale=1080:1920:flags=lanczos,setsar=1"
def preview():
 for k in range(0,len(plans),6):
  sheet=Image.new('RGB',(1080,math.ceil(len(plans[k:k+6])/3)*665),'#161616');draw=ImageDraw.Draw(sheet)
  for j,p in enumerate(plans[k:k+6]):
   f=A/f"cadre-{p['numero']:02}.jpg";ff(['-ss',p['entree']+.3,'-i',A/p['source'],'-vf',vf(p),'-frames:v',1,f]);im=Image.open(f).resize((360,640));x=j%3*360;y=j//3*665;sheet.paste(im,(x,y));draw.text((x+6,y+643),f"{p['numero']} / {p['start']:.2f}s / {p['action']}",fill='white')
  sheet.save(A/f'portrait-{k//6}.jpg')
def subtitles():
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf8'));cfg['render'].update(subtitle_size=90,words_per_caption=4,subtitle_wrap=19)
 words=caption_words(tim['words'],d['affichage']);words[0]['start']=0
 assemble.write_subtitles(cfg,words,M/'sous-titres.ass')
 lines=[]
 for l in (M/'sous-titres.ass').read_text(encoding='utf8').splitlines():
  if l.startswith('Dialogue:'):
   parts=l.split(',',9);parts[9]=r'{\an2\pos(500,1370)\fs90\fsp0}'+parts[9].replace(r'{\fad(0,90)}','');l=','.join(parts)
  lines.append(l)
 (M/'sous-titres.ass').write_text('\n'.join(lines)+'\n',encoding='utf8')
 shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',M/'police.ttf')
 spec=importlib.util.spec_from_file_location('brand',ROOT/'identite/histoires-pas-banales/gabarits-miniatures/render.py');brand=importlib.util.module_from_spec(spec);spec.loader.exec_module(brand)
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">'+brand.logo().replace('x="800" y="24"','x="734" y="272"')+'</svg>'
 (M/'logo.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg))
def render(p):
 target=M/f"plan-{p['numero']:02}.mp4"
 ff(['-ss',p['entree'],'-i',A/p['source'],'-vf',vf(p)+',fps=30,format=yuv420p,setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709','-frames:v',p['frames'],'-an','-c:v','libx264','-preset','veryfast','-crf',18,'-threads',2,target])
def build(refresh=True):
 subtitles()
 if refresh:
  with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,plans))
 (M/'concat.txt').write_text(''.join(f"file 'plan-{p['numero']:02}.mp4'\n" for p in plans),encoding='ascii')
 ff(['-f','concat','-safe',0,'-i','concat.txt','-c','copy','base.mp4'],M)
 graph="[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=9[a];[3:a]volume='if(between(t,35.2,36.0),0,0.055)':eval=frame,afade=t=in:d=0.4,afade=t=out:st=62.5:d=2.7[m];[a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[out]"
 ff(['-i','base.mp4','-i','voix.mp3','-loop',1,'-i','logo.png','-stream_loop',-1,'-i',ROOT/'assets/musique/mixkit/espace.mp3','-filter_complex_threads',1,'-filter_complex',graph,'-map','[v]','-map','[out]','-t',start,'-c:v','libx264','-preset','veryfast','-crf',18,'-threads',3,'-c:a','aac','-b:a','192k','-movflags','+faststart',P/'final.mp4'],M)
 print('Export',start,'s',flush=True)
if __name__=='__main__':
 if sys.argv[1]=='preview':preview()
 elif sys.argv[1]=='build':build()
 elif sys.argv[1]=='patch':
  render(plans[int(sys.argv[2])]);build(False)
 elif sys.argv[1]=='compare':
  from comparer_lot_16_18 import compare
  compare(P)
