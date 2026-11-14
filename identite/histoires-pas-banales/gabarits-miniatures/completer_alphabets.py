"""Compléments vectoriels explicites pour le lot de miniatures.
Les caractères de référence restent tracés ; les absents sont dessinés, sans police de remplacement.
"""
import json, math, unicodedata
from pathlib import Path
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

ROOT=Path(__file__).resolve().parent
raw=json.loads((ROOT/'lettres-reference.json').read_text(encoding='utf-8'))
old=json.loads((ROOT/'lettres-complements.json').read_text(encoding='utf-8'))

def transform(d,m):
 p=SVGPathPen(None);parse_path(d,TransformPen(p,m));return p.getCommands()
def bounds(d):
 p=BoundsPen(None);parse_path(d,p);return p.bounds
def norm(d,angle=0):
 a=math.radians(angle);d=transform(d,(math.cos(a),math.sin(a),-math.sin(a),math.cos(a),0,0))
 x0,y0,x1,y1=bounds(d);s=100/(y1-y0)
 return transform(d,(s,0,0,s,-x0*s,-y0*s))
def poly(pts):return 'M'+' L'.join(f'{x:.3f},{y:.3f}' for x,y in pts)+' Z'
def rect(x,y,w,h):return f'M{x},{y}h{w}v{h}h{-w}Z'
def ring(w,s):
 return f'M0,20 Q0,0 20,0 H{w-20} Q{w},0 {w},20 V80 Q{w},100 {w-20},100 H20 Q0,100 0,80Z M{s},24 V76 Q{s},84 {s+8},84 H{w-s-8} Q{w-s},84 {w-s},76 V24 Q{w-s},16 {w-s-8},16 H{s+8} Q{s},16 {s},24Z'

def draw(ch,w,s):
 # Uppercase skeletons share stem and bowl proportions with each source family.
 if ch=='A':return poly([(0,100),(w*.32,0),(w*.68,0),(w,100),(w-s,100),(w*.68,73),(w*.32,73),(s,100)])+' '+poly([(w*.41,52),(w*.59,52),(w*.5,25)])
 if ch=='B':return f'M0,0 H{w*.58} Q{w},0 {w},24 Q{w},41 {w*.78},48 Q{w},55 {w},77 Q{w},100 {w*.6},100 H0Z '+rect(s,17,w-2*s,23)+' '+rect(s,60,w-2*s,23)
 if ch=='C':return f'M{w},29 H{w-s} V24 Q{w-s},17 {w-s-7},17 H{s+7} Q{s},17 {s},24 V76 Q{s},83 {s+7},83 H{w-s-7} Q{w-s},83 {w-s},76 V70 H{w} V80 Q{w},100 {w-19},100 H19 Q0,100 0,80 V20 Q0,0 19,0 H{w-19} Q{w},0 {w},20 Z'
 if ch=='D':return f'M0,0 H{w*.6} Q{w},0 {w},25 V75 Q{w},100 {w*.6},100 H0Z M{s},18 V82 H{w-s-8} Q{w-s},82 {w-s},73 V27 Q{w-s},18 {w-s-8},18Z'
 if ch=='E':return poly([(0,0),(w,0),(w,18),(s,18),(s,40),(w*.88,40),(w*.88,58),(s,58),(s,82),(w,82),(w,100),(0,100)])
 if ch=='F':return poly([(0,0),(w,0),(w,18),(s,18),(s,40),(w*.88,40),(w*.88,58),(s,58),(s,100),(0,100)])
 if ch=='G':return f'M{w},28 H{w-s} V23 Q{w-s},17 {w-s-6},17 H{s+6} Q{s},17 {s},23 V77 Q{s},83 {s+6},83 H{w-s} V62 H{w*.48} V45 H{w} V100 H{w*.85} L{w*.79},93 Q{w*.7},100 {w*.55},100 H19 Q0,100 0,80 V20 Q0,0 19,0 H{w-19} Q{w},0 {w},20 Z'
 if ch=='H':return poly([(0,0),(s,0),(s,40),(w-s,40),(w-s,0),(w,0),(w,100),(w-s,100),(w-s,60),(s,60),(s,100),(0,100)])
 if ch=='I':return rect(0,0,s,100)
 if ch=='J':return f'M{w-s},0 H{w} V79 Q{w},100 {w-20},100 H20 Q0,100 0,80 V65 H{s} V77 Q{s},83 {s+6},83 H{w-s-6} Q{w-s},83 {w-s},77 Z'
 if ch=='K':return poly([(0,0),(s,0),(s,40),(w-s,0),(w,0),(w*.56,48),(w,100),(w-s,100),(s,61),(s,100),(0,100)])
 if ch=='L':return poly([(0,0),(s,0),(s,82),(w,82),(w,100),(0,100)])
 if ch=='M':return poly([(0,100),(0,0),(s,0),(w*.5,39),(w-s,0),(w,0),(w,100),(w-s,100),(w-s,36),(w*.5,70),(s,36),(s,100)])
 if ch=='N':return poly([(0,0),(s,0),(w-s,59),(w-s,0),(w,0),(w,100),(w-s,100),(s,41),(s,100),(0,100)])
 if ch=='O':return ring(w,s)
 if ch=='P':return f'M0,0 H{w-20} Q{w},0 {w},20 V40 Q{w},60 {w-20},60 H{s} V100 H0Z '+rect(s,18,w-2*s,24)
 if ch=='Q':return ring(w,s)+' '+poly([(w*.6,75),(w*.87,78),(w+4,106),(w*.74,106)])
 if ch=='R':return f'M0,0 H{w-20} Q{w},0 {w},20 V40 Q{w},54 {w*.72},58 L{w+2},100 H{w-s} L{w*.45},61 H{s} V100 H0Z '+rect(s,18,w-2*s,24)
 if ch=='S':return f'M{w},28 H{w-s} V23 Q{w-s},17 {w-s-6},17 H{s+6} Q{s},17 {s},23 V31 Q{s},37 {s+7},40 L{w-12},52 Q{w},58 {w},72 V81 Q{w},100 {w-19},100 H19 Q0,100 0,81 V72 H{s} V77 Q{s},83 {s+6},83 H{w-s-6} Q{w-s},83 {w-s},77 V70 Q{w-s},65 {w-s-6},62 L12,48 Q0,42 0,29 V19 Q0,0 19,0 H{w-19} Q{w},0 {w},19Z'
 if ch=='T':return poly([(0,0),(w,0),(w,19),(w/2+s/2,19),(w/2+s/2,100),(w/2-s/2,100),(w/2-s/2,19),(0,19)])
 if ch=='U':return f'M0,0 H{s} V77 Q{s},83 {s+6},83 H{w-s-6} Q{w-s},83 {w-s},77 V0 H{w} V80 Q{w},100 {w-20},100 H20 Q0,100 0,80 Z'
 if ch=='V':return poly([(0,0),(s,0),(w/2,72),(w-s,0),(w,0),(w*.67,100),(w*.33,100)])
 if ch=='W':return poly([(0,0),(s,0),(w*.26,66),(w*.40,0),(w*.60,0),(w*.74,66),(w-s,0),(w,0),(w*.86,100),(w*.64,100),(w*.5,47),(w*.36,100),(w*.14,100)])
 if ch=='X':return poly([(0,0),(s+2,0),(w/2,33),(w-s-2,0),(w,0),(w*.68,49),(w,100),(w-s-2,100),(w/2,67),(s+2,100),(0,100),(w*.32,49)])
 if ch=='Y':return poly([(0,0),(s+2,0),(w/2,36),(w-s-2,0),(w,0),(w/2+s/2,59),(w/2+s/2,100),(w/2-s/2,100),(w/2-s/2,59)])
 if ch=='Z':return poly([(0,0),(w,0),(w,18),(s,82),(w,82),(w,100),(0,100),(0,82),(w-s,18),(0,18)])
 if ch=='0':return ring(w,s)
 if ch=='1':return poly([(0,13),(w*.36,0),(w*.70,0),(w*.70,100),(w*.70-s,100),(w*.70-s,23),(0,37)])
 if ch=='2':return f'M0,29 V19 Q0,0 19,0 H{w-19} Q{w},0 {w},19 V34 Q{w},45 {w-10},55 L{s},82 H{w} V100 H0 V79 L{w-s},36 V23 Q{w-s},17 {w-s-6},17 H{s+6} Q{s},17 {s},23 V29 Z'
 if ch=='3':return f'M0,0 H{w-19} Q{w},0 {w},20 V30 Q{w},44 {w*.76},49 Q{w},54 {w},70 V81 Q{w},100 {w-19},100 H0 V82 H{w-s-6} Q{w-s},82 {w-s},76 V66 Q{w-s},58 {w-s-7},58 H{w*.28} V40 H{w-s-7} Q{w-s},40 {w-s},33 V24 Q{w-s},18 {w-s-6},18 H0 Z'
 if ch=='4':return poly([(w*.45,0),(w*.75,0),(w*.75,61),(w,61),(w,79),(w*.75,79),(w*.75,100),(w*.75-s,100),(w*.75-s,79),(0,79),(0,61)])+' '+poly([(s,61),(w*.75-s,61),(w*.75-s,24)])
 if ch=='5':return f'M0,0 H{w} V18 H{s} V39 H{w-19} Q{w},39 {w},59 V81 Q{w},100 {w-19},100 H0 V82 H{w-s-6} Q{w-s},82 {w-s},76 V63 Q{w-s},57 {w-s-6},57 H0 Z'
 if ch=='6':return f'M{w},27 H{w-s} V23 Q{w-s},17 {w-s-6},17 H{s+6} Q{s},17 {s},23 V43 Q{s+7},37 {w-19},37 Q{w},37 {w},58 V80 Q{w},100 {w-19},100 H19 Q0,100 0,80 V20 Q0,0 19,0 H{w-19} Q{w},0 {w},20 Z M{s},61 V77 Q{s},83 {s+6},83 H{w-s-6} Q{w-s},83 {w-s},77 V61 Q{w-s},55 {w-s-6},55 H{s+6} Q{s},55 {s},61 Z'
 if ch=='7':return poly([(0,0),(w,0),(w,18),(w*.42,100),(w*.08,100),(w-s,18),(0,18)])
 if ch=='8':return f'M0,20 Q0,0 19,0 H{w-19} Q{w},0 {w},20 V32 Q{w},43 {w*.8},49 Q{w},55 {w},70 V80 Q{w},100 {w-19},100 H19 Q0,100 0,80 V70 Q0,55 {w*.2},49 Q0,43 0,32 Z '+rect(s,17,w-2*s,23)+' '+rect(s,60,w-2*s,23)
 if ch=='9':return transform(draw('6',w,s),(-1,0,0,-1,w,100))
 if ch in ("'",'’'):return poly([(0,-5),(s,-5),(s-3,17),(0,25)])
 if ch=='-':return rect(0,44,w*.6,14)
 if ch=='?':return f'M0,27 V20 Q0,0 19,0 H{w-19} Q{w},0 {w},20 V33 Q{w},42 {w-10},49 L{w*.5+s/2},63 V73 H{w*.5-s/2} V56 L{w-s},33 V24 Q{w-s},17 {w-s-6},17 H{s+6} Q{s},17 {s},24 V27 Z '+rect(w*.5-s/2,82,s,18)
 raise ValueError(ch)

families={
 'racing-display':(76,24,.40),'racing-text':(58,18,.40),
 'magazine-tall':(43,13,0),'magazine-block':(86,25,0),
 'science-condensed':(43,13,.12),
 'pop-display':(96,25,.20),'pop-wide':(96,25,0),
 'sticker-display':(82,25,.20),'sticker-text':(81,24,.20)}
result={'provenance':'Lot 14 novembre 2026. Glyphes de référence normalisés pour la composition (rotation de ligne retirée pour Science, hauteur de capitale constante). Glyphes absents dessinés avec les proportions de la famille ; pas de police de remplacement. Les titres de référence complets restent les contours d’origine.','alphabets':{},'constructed':{}}
for family,(w,s,slant) in families.items():
 alpha={};constructed=[]
 for ch,g in raw['alphabets'][family].items():
  if ch in 'É?':continue
  angle=6 if family=='science-condensed' else (2.3 if family=='sticker-text' and ch in 'DGA' else 0)
  alpha[ch]=dict(g,path=norm(g['path'],angle),origin='reference-normalized')
 for ch,g in old['alphabets'].get(family,{}).items():
  if ch not in alpha:alpha[ch]=g
 for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'-?":
  if ch in alpha:continue
  ww=w*(1.25 if ch in 'MW' else 1)
  d=draw(ch,ww,s);d=transform(d,(1,0,-slant,1,slant*100,0))
  x0,y0,x1,y1=bounds(d)
  advance=(ww+8) if ch not in "I'-" else (s+9 if ch in "I'" else ww*.6+9)
  alpha[ch]={'path':d,'advance':advance,'origin':'constructed'};constructed.append(ch)
 for accented in 'ÉÈÊËÀÂÎÏÔÙÛÜÇ':
  base=unicodedata.normalize('NFD',accented)[0];d=alpha[base]['path'];adv=alpha[base]['advance']
  cx=adv*.5+slant*100
  if accented=='Ç':mark=poly([(adv*.45,98),(adv*.45-5,108),(adv*.45+6,111),(adv*.45+3,119),(adv*.45-8,119),(adv*.45-8,127),(adv*.45+9,127),(adv*.45+15,111),(adv*.45+5,104)])
  elif accented in 'É':mark=poly([(cx-12,-6),(cx+2,-24),(cx+21,-24),(cx+2,-6)])
  elif accented in 'ÈÀÙ':mark=poly([(cx+12,-6),(cx-2,-24),(cx-21,-24),(cx-2,-6)])
  elif accented in 'ËÏÜ':mark=rect(cx-19,-22,13,13)+' '+rect(cx+6,-22,13,13)
  else:mark=poly([(cx-24,-6),(cx-7,-25),(cx+7,-25),(cx+24,-6),(cx+8,-6),(cx,-15),(cx-8,-6)])
  alpha[accented]={'path':d+' '+mark,'advance':adv,'origin':'reference-base+constructed-accent'}
 result['alphabets'][family]=alpha;result['constructed'][family]=constructed
(ROOT/'lettres-complements-lot.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Alphabets complétés, provenance explicite enregistrée.')
