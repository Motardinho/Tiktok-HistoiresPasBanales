"""Compare sans retoucher les références ni modifier les gabarits."""
import base64
import json
from pathlib import Path
import resvg_py
from render import ROOT, title, lettering

OUT = ROOT / 'comparaison'
OUT.mkdir(exist_ok=True)
names = [('pop','POP / BALLONS','06-ballons-pop.png'),
         ('racing','RACING / MOTOS','07-motos-racing.png'),
         ('sticker','STICKER / FOOT','08-foot-sticker.png'),
         ('magazine','MAGAZINE / POGBA','09-pogba-magazine.png'),
         ('science','SCIENCE / FUSÉE','10-fusee-yellow.png')]

def label(text,x,y,w,h,color='#F5F5F5'):
    return lettering(text,'poppins',x,y,w,h,color)

items=['<rect width="2200" height="850" fill="#14181D"/>',
       label('MODÈLES VALIDÉS',24,20,300,25),
       label('GABARITS VECTORISÉS',24,443,400,25)]
for i,(style,name,filename) in enumerate(names):
    x=20+i*436
    img=base64.b64encode((ROOT.parent/'modeles-miniatures'/filename).read_bytes()).decode()
    original=f'<image width="1080" height="1920" href="data:image/png;base64,{img}"/>'
    c=json.loads((ROOT/(style+'.json')).read_text(encoding='utf-8'))
    current='<rect width="1080" height="1920" fill="#28333B"/>'+title(c)
    for top,content in [(98,original),(520,current)]:
        # Same source viewport and scale: no per-title resizing to hide differences.
        items.append(f'<svg x="{x}" y="{top}" width="416" height="289" viewBox="0 850 1080 750">{content}</svg>')
    items.extend([label(name,x+8,66,300,19),label(name,x+8,488,300,19)])
    pair=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="650" viewBox="0 0 1600 650"><rect width="1600" height="650" fill="#14181D"/>{label("MODÈLE VALIDÉ",24,20,280,24)}{label("GABARIT FIXE",824,20,260,24)}<svg x="10" y="70" width="780" height="542" viewBox="0 850 1080 750">{original}</svg><svg x="810" y="70" width="780" height="542" viewBox="0 850 1080 750">{current}</svg></svg>'
    (OUT/(style+'.png')).write_bytes(resvg_py.svg_to_bytes(svg_string=pair))
sheet='<svg xmlns="http://www.w3.org/2000/svg" width="2200" height="850">'+''.join(items)+'</svg>'
(OUT/'cinq-modeles-vs-gabarits.svg').write_text(sheet,encoding='utf-8')
(OUT/'cinq-modeles-vs-gabarits.png').write_bytes(resvg_py.svg_to_bytes(svg_string=sheet))
