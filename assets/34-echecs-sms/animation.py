"""Carte originale : Nancy -> Khanty-Mansiïsk, animation demandée par Marc.
Fond Natural Earth 1:110m, domaine public ; coordonnées WGS84 des villes.
La trajectoire est un effet narratif, pas le tracé physique du réseau télécom.
"""
import json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
p=Path(__file__).parent
W,H=1080,1920
font=lambda s:ImageFont.truetype('assets/fonts/Poppins-ExtraBold.ttf',s)
def project(lon,lat):return ((lon+16)*10.6,1410-(lat-30)*22)
base=Image.new('RGB',(W,H),'#071219');d=ImageDraw.Draw(base)
geo=json.loads((p/'countries.geojson').read_text(encoding='utf8'))
for f in geo['features']:
 g=f['geometry'];polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
 country=f['properties'].get('ADMIN','')
 for poly in polys:
  points=[project(lon,lat) for lon,lat,*_ in poly[0]]
  d.polygon(points,fill='#183c48' if country not in ['France','Russia'] else '#255563',outline='#376472',width=2)
# Discrètes lignes de visée, pas de légende scolaire.
for x in range(70,W,135):d.line((x,360,x,1190),fill='#203541',width=1)
for y in range(400,1200,135):d.line((45,y,1035,y),fill='#203541',width=1)
start=project(6.1844,48.6921);end=project(69.0189,61.0042)
def point(u):
 return (start[0]+(end[0]-start[0])*u,start[1]+(end[1]-start[1])*u-110*math.sin(math.pi*u))
frames=120
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(p/'transmission-france-russie.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(frames):
 t=i/30;im=base.copy();dr=ImageDraw.Draw(im)
 dr.text((100,400),'TRANSMISSION',font=font(57),fill='#a6d0d5')
 dr.text((100,463),'FRANCE > RUSSIE',font=font(43),fill='#f9d84c')
 u=max(0,min(1,(t-.35)/2.6))
 pts=[point(k/160) for k in range(int(u*160)+1)]
 glow=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(glow)
 if len(pts)>1:gd.line(pts,fill=(255,216,66,210),width=17)
 im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(13)))
 dr=ImageDraw.Draw(im)
 if len(pts)>1:dr.line(pts,fill='#ffe575',width=5)
 for xy,active in [(start,True),(end,u>=.98)]:
  x,y=xy;r=16+int(11*(.5+.5*math.sin(t*6)))
  dr.ellipse((x-r,y-r,x+r,y+r),outline='#ffe575' if active else '#6196a3',width=3)
  dr.ellipse((x-6,y-6,x+6,y+6),fill='#fff3b5' if active else '#6196a3')
 if u<1:
  x,y=point(u);dr.ellipse((x-10,y-10,x+10,y+10),fill='white')
 dr.text((110,1045),'NANCY',font=font(49),fill='white')
 dr.text((110,1103),'FRANCE',font=font(33),fill='#b9d4d8')
 dr.text((510,555),'KHANTY-',font=font(43),fill='white')
 dr.text((510,606),'MANSIÏSK',font=font(43),fill='white')
 if t>=2.95:dr.text((510,865),'SIGNAL REÇU',font=font(38),fill='#ffe575')
 if i in [0,45,105]:im.convert('RGB').save(p/f'animation-{i}.jpg')
 proc.stdin.write(im.convert('RGB').tobytes())
proc.stdin.close();assert proc.wait()==0
print('Animation 4 s créée')
