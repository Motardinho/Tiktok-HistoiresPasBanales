from pathlib import Path
import base64
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import resvg_py
p=Path('identite/histoires-pas-banales')
font=TTFont(p/'polices/Poppins-ExtraBold.ttf'); gs=font.getGlyphSet(); cmap=font.getBestCmap()
def line(t,x,y,w,h,color):
 paths=[]; advance=0
 from fontTools.pens.boundsPen import BoundsPen
 xmin=ymin=1e9; xmax=ymax=-1e9
 for c in t:
  g=gs[cmap[ord(c)]]; pen=SVGPathPen(gs);g.draw(pen)
  b=BoundsPen(gs);g.draw(b)
  if b.bounds:
   a,b0,c0,d=b.bounds; xmin=min(xmin,advance+a);xmax=max(xmax,advance+c0);ymin=min(ymin,b0);ymax=max(ymax,d)
  paths.append(f'<path transform="translate({advance} 0)" d="{pen.getCommands()}"/>');advance+=g.width
 return f'<g fill="{color}" transform="translate({x} {y+h}) scale({w/(xmax-xmin)} {-h/(ymax-ymin)}) translate({-xmin} {-ymin})">'+''.join(paths)+'</g>'
logo=(p/'logos/hpb-reference-propre-v1.svg').read_text(encoding='utf-8')
# Tight bounds of validated logo approx x268..475 y62..250.
logo=logo.replace('width="1020" height="1020" viewBox="240 32 255 255"','x="778" y="620" width="220" height="200" viewBox="268 62 207 188"',1)
bg=base64.b64encode((p/'banniere-youtube-v2.jpg').read_bytes()).decode()
s=f'<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1440" viewBox="0 0 2560 1440"><image width="2560" height="1440" href="data:image/jpeg;base64,{bg}"/><defs><linearGradient id="gx"><stop offset="0" stop-color="black"/><stop offset="0.045" stop-color="white"/><stop offset="0.955" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient><linearGradient id="gy" x2="0" y2="1"><stop offset="0" stop-color="black"/><stop offset="0.10" stop-color="white"/><stop offset="0.85" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient><mask id="mx"><rect x="725" y="515" width="1110" height="395" fill="url(#gx)"/></mask><mask id="my"><rect x="725" y="515" width="1110" height="395" fill="url(#gy)"/></mask></defs><g mask="url(#mx)"><rect x="725" y="515" width="1110" height="395" fill="#0F141A" mask="url(#my)"/></g>'+logo+line('HISTOIRES',1040,628,560,77,'#F8F5E9')+line('PAS BANALES',1040,728,730,77,'#FFE447')+'</svg>'
(p/'banniere-youtube-hpb-vectorielle.svg').write_text(s,encoding='utf-8')
(p/'banniere-youtube-hpb-vectorielle.png').write_bytes(resvg_py.svg_to_bytes(svg_string=s))
print((p/'banniere-youtube-hpb-vectorielle.png').stat().st_size)

