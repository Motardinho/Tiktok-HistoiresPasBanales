import sys,json,shutil,math,importlib.util
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import yaml,resvg_py
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from montage_reel import run
from monter_lot_21_23 import caption_words
from narrateur import assemble
from comparer_lot_16_18 import compare
P=ROOT/'out/45-origine-black-friday';A=ROOT/'assets/45-origine-black-friday';M=P/'_montage'
d=json.loads((P/'histoire.json').read_text(encoding='utf8'));t=json.loads((M/'timings-oraux.json').read_text(encoding='utf8'))
def ff(args,cwd=ROOT):return run(['ffmpeg','-v','error','-y',*map(str,args)],cwd)
# Source, entrée, centre horizontal, zone préalable. Archives historiques de contexte.
R='F19yTBhAsB0.mp4';K='L52yyJAT2EY.mp4';C='0Cs2xjzAJTU.mp4';F='rZLm9WR1sv4.mp4';N='moderne.mp4'
rows=[
 [(R,1,.48,'crop=iw:ih*0.83:0:ih*0.06'),(R,19.5,.52,'crop=iw:ih*0.68:0:ih*0.05')],
 [(C,395,.53,'crop=iw*0.90:ih*0.86:iw*0.05:ih*0.04'),(C,400,.58,'crop=iw*0.90:ih*0.86:iw*0.05:ih*0.04'),(K,61,.54,'crop=iw:ih*0.70:0:ih*0.12')],
 [(F,4,.5,None),(F,78,.52,None)],
 [(K,66,.5,'crop=iw:ih*0.70:0:ih*0.12'),(K,30,.56,'crop=iw:ih*0.70:0:ih*0.12'),(C,410,.5,'crop=iw*0.90:ih*0.86:iw*0.05:ih*0.04')],
 [(K,5,.5,'crop=iw:ih*0.70:0:ih*0.12'),(K,84,.5,'crop=iw:ih*0.70:0:ih*0.12')],
 [(K,73,.55,'crop=iw:ih*0.70:0:ih*0.12'),(K,90,.52,'crop=iw:ih*0.70:0:ih*0.12'),(K,99,.52,'crop=iw:ih*0.70:0:ih*0.12')],
 [(N,8,.45,None),(N,43,.54,None)],
 [(N,57,.5,None),(N,72,.56,None)],
 [(R,58,.5,'crop=iw:ih*0.84:0:ih*0.10'),(N,86,.48,None)],
 [(N,101,.5,None)]
]
photo_names=['1980s-1990s-americas-shopping-holiday-is-born.jpg','1950s-1960s-from-black-friday-to-big-friday-and-back.jpg']
plans=[];frame=0
for si,(duration,shots) in enumerate(zip(t['scene_durations'],rows)):
 end=round(sum(t['scene_durations'][:si+1])*30)
 for j,(src,at,crop,zone) in enumerate(shots):
  stop=round(frame+(end-frame)/(len(shots)-j));n=len(plans)
  plans.append(dict(numero=n,scene=si,start=frame/30,duration=(stop-frame)/30,frames=stop-frame,source=src,entree=at,centre=crop,zone=zone,contexte='archives de contexte historique' if src in [K,C,F] else 'Black Friday contemporain'))
  frame=stop
(P/'plans.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2),encoding='utf8')
cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf8'));cfg['render'].update(subtitle_size=82,words_per_caption=4,subtitle_wrap=19)
words=caption_words(t['words'],d['affichage']);words[0]['start']=0
assemble.write_subtitles(cfg,words,M/'sous-titres.ass')
lines=[]
for l in (M/'sous-titres.ass').read_text(encoding='utf8').splitlines():
 if l.startswith('Dialogue:'):
  parts=l.split(',',9);parts[9]=r'{\an2\pos(500,1370)\fs82\fsp0}'+parts[9];l=','.join(parts)
 lines.append(l)
(M/'sous-titres.ass').write_text('\n'.join(lines)+'\n',encoding='utf8')
shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',M/'police.ttf')
spec=importlib.util.spec_from_file_location('brand',ROOT/'identite/histoires-pas-banales/gabarits-miniatures/render.py');brand=importlib.util.module_from_spec(spec);spec.loader.exec_module(brand)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">'+brand.logo().replace('x="800" y="24"','x="734" y="272"')+'</svg>'
(M/'logo.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg))
def cropfilter(p):
 z=(p['zone']+',' if p['zone'] else '')
 return z+f"crop=trunc(min(iw\\,ih*9/16)/2)*2:trunc(min(ih\\,iw*16/9)/2)*2:'min(max(iw*{p['centre']}-ow/2\\,0)\\,iw-ow)':(ih-oh)/2,scale=1080:1920:flags=lanczos,setsar=1"
def preview(p):
 i=p['numero'];f=A/f'cadre-{i:02}.jpg'
 ff(['-ss',p['entree'],'-i',A/p['source'],'-vf',cropfilter(p),'-frames:v',1,f])
 return f
def preview_all():
 for p in plans:preview(p)
 for start in range(0,len(plans),8):
  s=Image.new('RGB',(1440,1340),'#151515');draw=ImageDraw.Draw(s)
  for j,p in enumerate(plans[start:start+8]):
   im=Image.open(A/f"cadre-{p['numero']:02}.jpg").resize((360,640));x=j%4*360;y=j//4*670;s.paste(im,(x,y));draw.text((x+5,y+643),f"{p['numero']:02} scene {p['scene']} / {p['source']}",fill='white')
  s.save(A/f'cadres-{start//8}.jpg')
def render_clip(p,variant):
 target=M/variant/f"plan-{p['numero']:02}.mp4";target.parent.mkdir(exist_ok=True)
 if variant=='videos':inputs=['-ss',p['entree'],'-i',A/p['source']];vf=cropfilter(p)
 else:
  si=p['scene'];i=p['numero'];source=A/f'cadre-{i:02}.jpg'
  # Photographies de presse contemporaines ; les scènes historiques restent des photogrammes identifiés.
  if i in [0,1,17,20]:
   name={0:photo_names[0],1:'2006-black-friday-mayhem-turns-violent.jpg',17:'black-friday-hero.jpg',20:photo_names[0]}[i]
   source=A/name
   c={0:.50,1:.54,17:.52,20:.32}[i]
   vf=f"crop=trunc(min(iw\\,ih*9/16)/2)*2:trunc(min(ih\\,iw*16/9)/2)*2:'min(max(iw*{c}-ow/2\\,0)\\,iw-ow)':(ih-oh)/2,scale=1080:1920,setsar=1"
  else:vf='scale=1080:1920,setsar=1'
  inputs=['-loop','1','-framerate','30','-i',source]
  vf+=f",scale=1188:2112,crop=1080:1920:x='54+20*t/{p['duration']}':y='96-35*t/{p['duration']}'"
 norm=',fps=30,format=yuv420p,setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709'
 ff([*inputs,'-vf',vf+norm,'-frames:v',p['frames'],'-an','-c:v','libx264','-preset','veryfast','-crf',19,'-threads',2,target])
def build(variant):
 dest=P/variant;dest.mkdir(exist_ok=True);work=M/variant;work.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda p:render_clip(p,variant),plans))
 (work/'concat.txt').write_text(''.join(f"file 'plan-{p['numero']:02}.mp4'\n" for p in plans),encoding='ascii')
 ff(['-f','concat','-safe',0,'-i','concat.txt','-c','copy','base.mp4'],work)
 for f in ['sous-titres.ass','police.ttf','logo.png']:shutil.copy2(M/f,work/f)
 music=ROOT/'assets/musique/mixkit/bouchons.mp3'
 graph="[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=9[a];[3:a]volume=0.06,afade=t=out:st=64:d=3[m];[a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[out]"
 ff(['-i','base.mp4','-i',M/'voix.mp3','-loop',1,'-i','logo.png','-stream_loop',-1,'-i',music,'-filter_complex_threads',1,'-filter_complex',graph,'-map','[v]','-map','[out]','-t',frame/30,'-c:v','libx264','-preset','veryfast','-crf',19,'-threads',3,'-c:a','aac','-b:a','192k','-movflags','+faststart',dest/'final.mp4'],work)
 dv=dict(d,type_post=variant,statut='export de travail, contrôle en cours')
 (dest/'histoire.json').write_text(json.dumps(dv,ensure_ascii=False,indent=2),encoding='utf8');(dest/'_montage').mkdir(exist_ok=True)
 compare(dest)
 print(variant,'exporte',frame/30,flush=True)
if __name__=='__main__':
 if sys.argv[1]=='preview':preview_all()
 else:build(sys.argv[1])
