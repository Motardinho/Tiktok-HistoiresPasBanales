"""Révisions plein écran et comparaisons des deux autres sujets."""
import copy,json,shutil,sys
import yaml
from narrateur import assemble
from montage_reel import ROOT,SOURCES,run,compare

GROUPS={
 'trois-records-voitures-vitesse':[
  [('hennessey-f5',118,1.8,.47),('hennessey-f5',120,None,.47)],
  [('hennessey-f5',96,2.6,.49),('hennessey-f5',112,None,.49)],
  [('hennessey-f5',40,2.2,.5),('hennessey-f5',8,2.2,.5),('hennessey-f5',120,None,.47)],
  [('hennessey-f5',104,2.6,.5),('hennessey-f5',112,None,.48)],
  [('bugatti-record',24,2.5,.5),('bugatti-record',80,2.5,.5),('bugatti-record',160,None,.5)],
  [('bugatti-bolide',24,2.3,.5),('bugatti-bolide',0,None,.5)],
  [('bugatti-bolide',16,2.4,.5),('bugatti-bolide',24,None,.5)],
  [('hennessey-f5',120,2.2,.47),('bugatti-record',24,2.2,.5),('bugatti-bolide',2,None,.5)]
 ],
 'villes-plus-lentes-tomtom-2024':[
  [('new-york-bouchons',0,3,.5),('londres',1,3.3,.5),('paris-soir',18,None,.5)],
  [('londres',8,2.64,.4),('new-york-bouchons',3,2.64,.5),('paris-soir',12,None,.5)],
  [('londres',12,2.45,.5),('londres',17,2.45,.42),('londres',21,None,.55)],
  [('new-york-bouchons',0,2.9,.5),('new-york-bouchons',4,2.9,.5),('new-york-bouchons',1,None,.5)],
  [('paris-soir',4,2.5,.48),('paris-soir',14,2.5,.5),('paris-soir',24,None,.53)],
  [('londres',2,2.57,.5),('new-york-bouchons',2,2.57,.5),('paris-soir',20,None,.5)],
  [('londres',10,2.81,.5),('new-york-bouchons',5,2.81,.5),('paris-soir',8,None,.52)],
  [('new-york-bouchons',1,3.15,.5),('paris-soir',22,3.15,.5),('londres',16,None,.48)]
 ]}

def main(slug,only=None):
 w=ROOT/'out'/slug
 old=w/'version-reelle-v2';old.mkdir(exist_ok=True)
 for name in ['final.mp4','comparaison.mp4','sous-titres.ass','sources-visuelles.json']:
  if (w/name).exists() and not (old/name).exists():shutil.copy2(w/name,old/name)
 cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
 cfg['render'].update(words_per_caption=5,subtitle_wrap=19)
 t=json.loads((w/'timings.json').read_text(encoding='utf-8'))
 d=json.loads((w/'histoire.json').read_text(encoding='utf-8'))
 overlays=[(0,2.5,d['titre_fixe'],'Titre')]
 if 'villes' in slug:
  overlays.extend([(17.88,25.24,'LONDRES • 101 H','Bandeau'),(25.24,33.96,'NEW YORK • 102 H','Bandeau'),(33.96,41.44,'PARIS • 97 H','Bandeau')])
 else:overlays.extend([(21.08,28.64,'2019 • UN SEUL SENS','Bandeau'),(33.24,38.04,'BOLIDE CLIENT : 380 KM/H','Bandeau')])
 subs=w/'sous-titres-v3.ass';assemble.write_subtitles(cfg,t['words'],subs,overlays)
 subs.write_text(subs.read_text(encoding='utf-8').replace('8,50,50,1090,1','8,65,65,1240,1'),encoding='utf-8')
 total=0;files=[];edits=[]
 for s,(g,duration) in enumerate(zip(GROUPS[slug],t['scene_durations'])):
  end=round(sum(t['scene_durations'][:s+1])*30)
  for name,start,dur,cx in g:
   frames=round(dur*30) if dur is not None else end-total
   if s==7 and dur is None:frames+=15
   # Les deux films automobiles panoramiques ont des bandes noires intégrées.
   lead='crop=iw:trunc(ih*0.74/2)*2:0:(ih-oh)/2,' if name in ['hennessey-f5','bugatti-record'] else ''
   # Pour le hook trafic, concentrer l'ouverture sur les véhicules, plus bas dans l'image.
   special="crop=iw:trunc(ih*0.7/2)*2:0:ih-oh," if name=='new-york-bouchons' and s==0 else ''
   vf=lead+special+f"crop=trunc(ih*9/16/2)*2:ih:max(0\\,min(iw-ow\\,iw*{cx}-ow/2)):0,scale=1080:1920:flags=lanczos,fps=30,setsar=1"
   dest=w/f'dynamique{len(files):02d}.mp4'
   if only is None or len(files) in only or not dest.exists():
    run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(SOURCES/(name+'.mp4')),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','3','-pix_fmt','yuv420p',str(dest)])
   files.append(dest);edits.append(dict(scene=s,source=name,debut_source=start,debut_montage=total/30,duree=frames/30,cadrage='plein écran portrait'))
   total+=frames
   print(slug,'plan',len(files),flush=True)
 assemble.assemble(cfg,w,files,w/'voix.mp3',subs,w/'final-v3.mp4',assemble.stamp_time(t['words']))
 run(['ffmpeg','-v','error','-i',str(w/'final-v3.mp4'),'-f','null','-'])
 shutil.copy2(w/'final-v3.mp4',w/'final.mp4');shutil.copy2(subs,w/'sous-titres.ass')
 (w/'montage-v3.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2),encoding='utf-8')
 compare(slug);shutil.copy2(w/'comparaison.mp4',w/'comparaison-v3.mp4')
 print(slug,'V3 terminée',flush=True)

if __name__=='__main__':
 for slug in sys.argv[1:]:main(slug)
