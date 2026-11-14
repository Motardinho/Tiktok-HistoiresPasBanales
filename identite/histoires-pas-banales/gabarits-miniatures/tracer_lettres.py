"""Vectorise les caractères des cinq références, sans modifier leurs images.
Contours de lettres et contreformes, pas une image du titre collée dans le SVG.
"""
import json
from pathlib import Path
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parent
SPECS={
 'pop':('06-ballons-pop.png',[
  ('TOP 10',(150,1117,780,1225),'pop-display'),
  ('PLUS BEAUX',(150,1240,950,1332),'pop-wide'),
  ('BALLONS DE FOOT',(125,1356,975,1442),'pop-wide')]),
 'sticker':('08-foot-sticker.png',[
  ('TOP10',(195,1025,760,1170),'sticker-display'),
  ('BUTS LES PLUS',(130,1168,890,1266),'sticker-text'),
  ('DÉGUEULASSES',(100,1260,940,1408),'sticker-text')]),
 'science':('10-fusee-yellow.png',[
  ('POURQUOI INONDER',(85,915,867,1109),'science-condensed'),
  ('UNE FUSÉE ?',(90,1070,780,1312),'science-condensed')]),
 'racing':('07-motos-racing.png',[
  ('TOP 3',(135,953,540,1056),'racing-display'),
  ('MOTOS DE SÉRIE',(95,1058,885,1174),'racing-text'),
  ('LES PLUS RAPIDES',(80,1190,950,1290),'racing-text'),
  ('2026',(85,1311,425,1410),'racing-display')]),
 'magazine':('09-pogba-magazine.png',[
  ('POGBA',(105,956,710,1189),'magazine-tall'),
  ('BRAQUÉ',(126,1198,775,1334),'magazine-block'),
  ('POUR',(100,1360,283,1485),'magazine-tall'),
  ('13 MILLIONS',(300,1350,950,1523),'magazine-tall')])}

def contours(mask,dx=0,dy=0,scale=1):
 paths=[]
 for c in cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]:
  if abs(cv2.contourArea(c))<3: continue
  a=cv2.approxPolyDP(c,.65,True).reshape(-1,2)
  points=[((float(x)+dx)*scale,(float(y)+dy)*scale) for x,y in a]
  # Small quadratic corner smoothing removes pixel stairs, retaining silhouette.
  turns=[]
  for i,point in enumerate(points):
   v=np.array(point); before=np.array(points[i-1])-v; after=np.array(points[(i+1)%len(points)])-v
   nb=float(np.linalg.norm(before)); na=float(np.linalg.norm(after))
   radius=min(1.1*scale,nb/3,na/3)
   turns.append((v+before*radius/nb,v,v+after*radius/na))
  start=turns[0][2]
  data=f'M{start[0]:.3f},{start[1]:.3f}'
  for entry,corner,leave in turns[1:]+turns[:1]:
   data+=f' L{entry[0]:.3f},{entry[1]:.3f} Q{corner[0]:.3f},{corner[1]:.3f} {leave[0]:.3f},{leave[1]:.3f}'
  paths.append(data+' Z')
 return ' '.join(paths)

library={'provenance':'Contours des références validées, seuil de couleur puis vectorisation, tolérance 0.65 pixel et lissage des angles sur 1.1 pixel maximum. Images sources inchangées.','rows':{},'alphabets':{}}
for style,(filename,rows) in SPECS.items():
 im=cv2.imread(str(ROOT.parent/'modeles-miniatures'/filename))
 config=json.loads((ROOT/(style+'.json')).read_text(encoding='utf-8'))
 for i,(text,box,family) in enumerate(rows):
  x,y,r,b=box; roi=im[y:b,x:r]
  lo=roi.min(2); hi=roi.max(2)
  mask=((lo>190)&((hi-lo)<50)).astype(np.uint8)*255
  if style=='science' or (style in ('pop','sticker') and i==2):
   mask=(hi<70).astype(np.uint8)*255
   polygons={
    ('sticker',2):[[108,1291],[955,1259],[938,1382],[90,1420]],
    ('science',0):[[97,994],[875,913],[861,1038],[84,1118]],
    ('science',1):[[98,1145],[808,1072],[755,1254],[76,1326]]}
   if (style,i) in polygons:
    gate=np.zeros(mask.shape,np.uint8)
    poly=np.array(polygons[(style,i)],np.int32)-np.array([x,y])
    cv2.fillPoly(gate,[poly],255)
    # The accented E protrudes above the band; include its separate shape.
    accent_boxes={('sticker',2):(224,1263,270,1306),('science',1):(583,1073,625,1110)}
    if (style,i) in accent_boxes:
     ax,ay,ar,ab=accent_boxes[(style,i)]
     gate[max(0,ay-y):ab-y,max(0,ax-x):ar-x]=255
    mask=cv2.bitwise_and(mask,gate)
  if text=='13 MILLIONS':
   mask=((roi[:,:,1]>180)&(roi[:,:,2]>180)&(roi[:,:,0]<120)).astype(np.uint8)*255
  count,labels,stats,_=cv2.connectedComponentsWithStats(mask)
  if style=='pop' and i==1:
   # E and A touch at their feet. Split labels only; retain every source pixel.
   merged=next(j for j in range(1,count) if stats[j,2]>150)
   cols=np.indices(labels.shape)[1]
   labels[(labels==merged)&(cols>=683-x)]=count
   stats=np.vstack([stats,np.zeros((1,5),dtype=stats.dtype)])
   for j in (merged,count):
    yy,xx=np.where(labels==j)
    stats[j]=[xx.min(),yy.min(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,len(xx)]
   count+=1
  main=[j for j in range(1,count) if stats[j,4]>500 and stats[j,3]>40]
  main.sort(key=lambda j:stats[j,0])
  letters=text.replace(' ','')
  assert len(main)==len(letters),(text,len(main),len(letters))
  keep=np.isin(labels,main)
  # Detached accents are included with their letter, never treated as extra glyphs.
  accents=[j for j in range(1,count) if stats[j,4]>100 and j not in main and stats[j,3]<=40]
  for j in accents: keep|=labels==j
  clean=keep.astype(np.uint8)*255
  key=f'{style}-{i}'
  layout={k:config['rows'][i][k] for k in ('x','y','w','h')}
  library['rows'][key]={'text':text,'family':family,'path':contours(clean,x,y),'box':box,'layout':layout}
  alphabet=library['alphabets'].setdefault(family,{})
  baseline=float(np.median([stats[j,1]+stats[j,3]-1 for j in main]))
  capheight=float(np.median([stats[j,3] for j in main]))
  for ch,j in zip(letters,main):
   gx,gy,gw,gh,_=stats[j]; gm=labels==j
   if ch in ('É','?'):
    for a in accents:
     ax,ay,aw,ah,_=stats[a]
     if gx-10<ax+aw/2<gx+gw+10: gm|=labels==a
   if ch not in alphabet:
    alphabet[ch]={'path':contours(gm.astype(np.uint8)*255,-float(gx),capheight-baseline,100/capheight),'advance':round((float(gw)-(capheight*.27 if style=='racing' else 0)+capheight*.08)*100/capheight,3)}
  config['rows'][i]['traced_row']=key
  config['rows'][i]['traced_family']=family
  config['rows'][i]['text_rotation']=0
  # Text path carries the actual original positions, incl. accents and slant.
 (ROOT/(style+'.json')).write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'lettres-reference.json').write_text(json.dumps(library,ensure_ascii=False,indent=2),encoding='utf-8')
