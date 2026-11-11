"""Montage animalier entièrement en séquences vidéo."""
from concurrent.futures import ThreadPoolExecutor
import hashlib,shutil
from pathlib import Path
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
w=next((ROOT/'out').glob('17-*'));root=w/'_montage';m=root/'rapaces-video-v2';m.mkdir(exist_ok=True);a=ROOT/'assets/lot-16-18/nouveaux-rapaces'
# bornes temporelles finales, source, entrée source, cadrage
plans=[
(0,91/30,ROOT/'assets/lot-16-18/cheetah.webm',37.3,'hook'),
(91/30,4.9,a/'gyrfalcon-bbc.mp4',232,'large'),
(4.9,9.5,a/'gyrfalcon-bbc.mp4',169,'gyr-stoop'),
(9.5,368/30,a/'avion-tourisme-pexels-31662106.mp4',0,'base'),
(368/30,578/30,a/'gyrfalcon-bbc.mp4',198,'large-fact'),
(578/30,684/30,a/'gyrfalcon-bbc.mp4',205,'large'),
(684/30,774/30,a/'golden-rrp.mp4',1,'portrait'),
(774/30,1003/30,a/'golden-cornell-stoop.mp4',3,'golden-stoop'),
(1003/30,1228/30,a/'golden-natgeo.mp4',26,'large'),
(1228/30,1321/30,a/'golden-rrp.mp4',61,'portrait'),
(1321/30,49,a/'natgeo-attaque-faucon.mp4',35,'large'),
(49,51.1,a/'natgeo-attaque-faucon.mp4',75.7,'pelerin-stoop'),
(51.1,1621/30,a/'natgeo-attaque-faucon.mp4',78.2,'large'),
(1621/30,1741/30,a/'peregrine-ryan.mp4',42,'portrait'),
(1741/30,1804/30,a/'natgeo-attaque-faucon.mp4',75.7,'pelerin-stoop'),
(1804/30,1927/30,a/'natgeo-attaque-faucon.mp4',85,'portrait'),
(1927/30,2017/30,a/'gyrfalcon-bbc.mp4',8,'large'),
(2017/30,2107/30,a/'golden-natgeo.mp4',45,'large'),
(2107/30,2124/30,a/'peregrine-ryan.mp4',46,'portrait')]
def one(item):
 i,(start,end,src,at,kind)=item;frames=round(end*30)-round(start*30);target=m/f'clip-{i:02d}.mp4'
 if kind=='hook':g="[0:v]split[a][b];[a]crop=iw:trunc(ih*0.12/2)*2:0:trunc(ih*0.88/2)*2,scale=1080:1920,gblur=sigma=12[bg];[b]scale=1080:-2,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/65,(H-Y-1)/65))'[fg];[bg][fg]overlay=0:400[v]"
 elif kind=='gyr':g='[0:v]crop=405:720:675:0,scale=1080:1920[v]'
 elif kind=='gyr-fact':g='[0:v]crop=540:720:620:0,scale=1080:1440,pad=1080:1920:0:400:color=0xcbd2d5[v]'
 elif kind in ('gyr-stoop','golden-stoop'):
  rows=read(a/('suivi-gerfaut.json' if kind=='gyr-stoop' else 'suivi-aigle.json'));side=280 if kind=='gyr-stoop' else 460
  def expr(key):
   terms=[]
   for left,right in zip(rows,rows[1:]):
    lo,hi=left['t'],right['t'];terms.append(f"gte(t,{lo})*lt(t,{hi})*({left[key]}+({right[key]}-{left[key]})*(t-{lo})/({hi}-{lo}))")
   return '+'.join(terms)+f"+gte(t,{rows[-1]['t']})*{rows[-1][key]}"
  x,y=expr('x'),expr('y')
  g=f"[0:v]split[a][b];[a]crop=trunc(iw/2/2)*2:40:trunc(iw/4/2)*2:0,scale=1080:1920,gblur=sigma=18[bg];[b]crop={side}:{side}:x='{x}':y='{y}',scale=1080:1080,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/65,(H-Y-1)/65))'[fg];[bg][fg]overlay=0:310[v]"
 elif kind=='pelerin-stoop':g="[0:v]scale=1280:720,crop=405:720:x='500-20*t':y=0,scale=1080:1920[v]"
 elif kind in ('large','large-fact'):
  g="[0:v]split[a][b];[a]crop=trunc(iw/4/2)*2:trunc(ih/8/2)*2:trunc(iw/2/2)*2:0,scale=1080:1920,gblur=sigma=14[bg];[b]scale=1080:-2,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/65,(H-Y-1)/65))'[fg];[bg][fg]overlay=0:450[v]"
  if kind=='large-fact':g=g.replace('overlay=0:450','overlay=0:720')
 elif kind=='portrait':g='[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v]'
 else:g='[0:v]null[v]'
 g+=';[v]fps=30,trim=end_frame='+str(frames)+',settb=1/30,setpts=N,format=yuv420p,setsar=1[out]'
 run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(src),'-filter_complex_threads','1','-filter_complex',g,'-map','[out]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(target)])
 return target
with ThreadPoolExecutor(max_workers=2) as p:files=list(p.map(one,enumerate(plans)))
args=[]
for p in files:args+=['-threads','1','-i',str(p)]
g=';'.join(f'[{i}:v]settb=1/30,setpts=N[v{i}]' for i in range(len(files)))+';'+''.join(f'[v{i}]' for i in range(len(files)))+f'concat=n={len(files)}:v=1:a=0[v]'
run(['ffmpeg','-v','error','-y']+args+['-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'base.mp4')])
d=read(w/'histoire.json');d.setdefault('correction_locale',{})['base']=str((m/'base.mp4').relative_to(w));save(w/'histoire.json',d)
manifest=[]
for start,end,src,at,kind in plans:
 row=dict(debut=start,fin=end,source=str(src.relative_to(ROOT)),entree_source=at,type='photo' if kind=='base-photo' else 'video')
 if kind=='base-photo':row.update(justification_photo='Seule exception : gerfaut lors de la vitesse en piqué. Aucun clip de piqué exploitable et identifié à cette espèce trouvé après recherche. Le lien NatGeo fourni montre un pèlerin ; le clip libre de falcon atterrissant montre des milans ; le clip Natuurbeelden montre la perdrix, pas le gerfaut.',pistes_examinees=['https://www.nationalgeographic.fr/video/animaux/limpressionnante-attaque-du-faucon','https://www.youtube.com/watch?v=hdYulpJqn_0','https://www.youtube.com/watch?v=w_uJiR9ICUw'])
 manifest.append(row)
save(m/'montage.json',manifest);print('17 : montage entièrement en vidéo prêt',flush=True)
