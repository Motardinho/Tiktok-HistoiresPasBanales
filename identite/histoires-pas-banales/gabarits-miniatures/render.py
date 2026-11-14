"""Gabarits HPB déterministes : JSON éditable -> SVG vectoriel autonome + PNG.
Usage: python render.py --all
       python render.py --config chemin.json --background photo.png --out sortie
Dependencies: fonttools==4.68.0 resvg-py==0.5.0
"""
import argparse
import base64
import json
from pathlib import Path
from functools import lru_cache
import unicodedata
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import resvg_py

ROOT = Path(__file__).resolve().parent
FONTS = {'anton': ROOT/'polices/Anton-Regular.ttf',
         'russo': ROOT/'polices/RussoOne-Regular.ttf',
         'black': ROOT/'polices/Poppins-Black.ttf',
         'barlow': ROOT/'polices/BarlowCondensed-BlackItalic.ttf',
         'archivo': ROOT/'polices/ArchivoBlack-Regular.ttf',
         'bebas': ROOT/'polices/BebasNeue-Regular.ttf',
         'poppins': ROOT/'polices/Poppins-ExtraBold.ttf'}

@lru_cache(None)
def outlines(text, font, tracking=0):
    f = TTFont(FONTS[font]); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    svg = SVGPathPen(gs); bounds = BoundsPen(gs); x = 0
    for ch in text:
        if ord(ch) not in cmap:
            raise ValueError(f'Caractère non pris en charge: {ch}')
        g = gs[cmap[ord(ch)]]
        for p in (svg, bounds):
            g.draw(TransformPen(p, (1,0,0,1,x,0)))
        x += g.width + tracking
    return svg.getCommands(), bounds.bounds

def lettering(text, font, x, y, w, h, fill, slant=0, stroke=None, sw=0, cap=False, tracking=0, weight=0):
    d, (x0,y0,x1,y1) = outlines(text, font, tracking)
    if cap:
        _, (_,y0,_,y1) = outlines('H',font,tracking)
    # Slant is applied after normalization; dimensions remain deterministic.
    sx=w/(x1-x0); sy=h/(y1-y0)
    edge=f' stroke="{stroke}" stroke-width="{sw}" paint-order="stroke fill" stroke-linejoin="round"' if stroke else ''
    if weight and not stroke:
        edge=f' stroke="{fill}" stroke-width="{weight/min(sx,sy)}" paint-order="stroke fill" stroke-linejoin="round"'
    return f'<g transform="translate({x} {y})"><g transform="matrix(1 0 {-slant} 1 {slant*h} 0)"><g transform="matrix({sx} 0 0 {-sy} {-x0*sx} {y1*sy})"><path d="{d}" fill="{fill}"{edge} /></g></g></g>'

def band(x,y,w,h,color,slant=.28):
    k=h*slant
    return f'<path d="M{x+k},{y} H{x+w+k} L{x+w},{y+h} H{x} Z" fill="{color}"/>'

def logo():
    # Asset explicitly approved by Marc; no font substitution or redrawing.
    source=(ROOT.parent/'logos/hpb-reference-propre-v1.svg').read_text(encoding='utf-8')
    return source.replace('width="1020" height="1020"',
                          'x="800" y="24" width="240" height="240"',1)

@lru_cache(None)
def traced_library():
    library=json.loads((ROOT/'lettres-reference.json').read_text(encoding='utf-8'))
    extra=ROOT/'lettres-complements.json'
    if extra.exists():
        for family,glyphs in json.loads(extra.read_text(encoding='utf-8'))['alphabets'].items():
            library['alphabets'].setdefault(family,{}).update(glyphs)
    return library

def traced_text(row,fill):
    library=traced_library(); original=library['rows'][row['traced_row']]
    if row['text']==original['text'] and not row.get('compose'):
        b=original['layout']; sx=row['w']/b['w']; sy=row['h']/b['h']
        return f'<path transform="matrix({sx} 0 0 {sy} {row["x"]-sx*b["x"]} {row["y"]-sy*b["y"]})" d="{original["path"]}" fill="{fill}" fill-rule="evenodd"/>'
    glyphs=(lot_library() if row.get('alphabet')=='lot' else library)['alphabets'][row['traced_family']]
    missing=sorted(set(row['text'])-set(glyphs)-{' '})
    if missing:
        raise ValueError('Glyphes non présents dans la référence : '+','.join(missing)+'. Compléter le lettrage avant déclinaison ; aucune substitution silencieuse.')
    cursor=0; elements=[]
    for ch in row['text']:
        if ch==' ': cursor+=30; continue
        g=glyphs[ch]
        elements.append(f'<path transform="translate({cursor} 0)" d="{g["path"]}" fill="{fill}" fill-rule="evenodd"/>')
        cursor+=g['advance']
    return f'<g transform="translate({row["x"]} {row["y"]}) scale({row["w"]/cursor} {row["h"]/100})">'+''.join(elements)+'</g>'

@lru_cache(None)
def lot_library():
    return json.loads((ROOT/'lettres-complements-lot.json').read_text(encoding='utf-8'))

def title(c):
    style=c['style']; out=[]
    for row in c['rows']:
        t=row['text']; x=row['x']; y=row['y']; w=row['w']; h=row['h']
        slant=row.get('slant', c.get('slant',0)); font=row.get('font',c['font'])
        color=row.get('color','#FFFFFF'); bg=row.get('band')
        extra=dict(cap=row.get('cap',c.get('cap',False)),tracking=row.get('tracking',c.get('tracking',0)),weight=row.get('weight',c.get('weight',0)))
        def text_at(dx=0,dy=0,fill=color,stroke=None,sw=0):
            if row.get('traced_row'):
                edge=f' stroke="{stroke}" stroke-width="10" stroke-linejoin="round" paint-order="stroke fill"' if stroke else ''
                return f'<g transform="translate({dx} {dy})"{edge}>{traced_text(row,fill)}</g>'
            letters=lettering(t,font,x+dx,y+dy,w,h,fill,slant,stroke,sw,**extra)
            return f'<g transform="rotate({row.get("text_rotation",0)} {x} {y})">{letters}</g>'
        if bg:
            pad=row.get('padding',16)
            bx=x-pad; by=y-pad; bw=w+2*pad+slant*h; bh=h+2*pad
            if row.get('polygon'):
                pts=row['polygon']
                for layer in row.get('layers',[]):
                    shifted=' '.join(f'{a+layer[0]},{b+layer[1]}' for a,b in pts)
                    out.append(f'<polygon points="{shifted}" fill="{layer[2]}"/>')
                points=' '.join(f'{a},{b}' for a,b in pts)
                out.append(f'<polygon points="{points}" fill="{bg}"/>')
            elif style=='pop':
                out.append(band(bx-22,by+25,bw,bh,'#FF007A',.26))
            if not row.get('polygon') and style=='sticker':
                out.append(band(bx+12,by+21,bw,bh,'#030303',.16))
                out.append(band(bx+8,by+13,bw,bh,'#B700FF',.16))
            if not row.get('polygon') and style in ('racing','science'):
                out.append(band(bx+15,by+16,bw,bh,'#090E20',.35 if style=='racing' else .13))
            if not row.get('polygon'):
                out.append(band(bx,by,bw,bh,bg,.35 if style=='racing' else .16))
        if style=='sticker' and not bg:
            for dx,dy in [(15,20),(8,10),(0,0)]:
                out.append(text_at(dx,dy,'#000000','#000000',row.get('outline',85)))
        if style=='racing' and not bg:
            out.append(text_at(12,12,'#000A24'))
        out.append(text_at())
    body=''.join(out)
    if c.get('rotation'):
        body=f'<g transform="rotate({c["rotation"]} 540 1200)">{body}</g>'
    if style=='pop':
        mx,my=c.get('pop_mark',[798,1166])
        body+=band(mx,my,38,55,'#FFF000',.3)
    return body

def svg(c,background=None,preview=False):
    bg=''
    if background:
        path=Path(background); mime='image/jpeg' if path.suffix.lower() in ('.jpg','.jpeg') else 'image/png'
        data=base64.b64encode(path.read_bytes()).decode()
        bg=f'<image width="1080" height="1920" preserveAspectRatio="xMidYMid slice" href="data:{mime};base64,{data}"/>'
    elif preview:
        bg='<rect width="1080" height="1920" fill="#28333B"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">{bg}{title(c)}{logo()}</svg>'

def write(c,out,background=None,preview=False):
    out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    source=svg(c,background,preview)
    out.with_suffix('.svg').write_text(source,encoding='utf-8')
    out.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_string=source))
    return source

def row(text,x,y,w,h,**kw):
    return dict(text=text,x=x,y=y,w=w,h=h,**kw)

def defaults():
    return [
      dict(style='pop',font='russo',slant=.14,rows=[row('TOP 10',145,1117,580,94,band='#0917D5'),row('PLUS BEAUX',145,1240,750,77,band='#0917D5',slant=0),row('BALLONS DE FOOT',120,1360,805,67,band='#FFF000',color='#050509',slant=0)]),
      dict(style='racing',font='anton',slant=.25,rows=[row('TOP 3',125,960,380,92,band='#F32007'),row('MOTOS DE SÉRIE',110,1088,735,89),row('LES PLUS RAPIDES',100,1211,800,87,band='#F32007'),row('2026',90,1337,300,87,band='#F32007')]),
      dict(style='sticker',font='poppins',slant=.18,rows=[row('TOP 10',215,1040,500,128),row('BUTS LES PLUS',145,1190,700,77),row('DÉGUEULASSES',120,1311,785,90,band='#FFE500',color='#000000')]),
      dict(style='magazine',font='anton',slant=0,rows=[row('POGBA',105,970,590,215),row('BRAQUÉ',125,1220,640,110,font='poppins',band='#FF302C'),row('POUR',105,1375,175,105),row('13 MILLIONS',310,1366,630,155,color='#F8FF24')]),
      dict(style='science',font='anton',slant=.09,rotation=-6,rows=[row('POURQUOI INONDER',110,970,745,97,band='#FFDF00',color='#000000'),row('UNE FUSÉE ?',100,1118,650,155,band='#FFDF00',color='#000000')])
    ]

def all_templates():
    blocks=[]
    for i,c in enumerate(defaults()):
        path=ROOT/(c['style']+'.json')
        if not path.exists(): path.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
        c=json.loads(path.read_text(encoding='utf-8'))
        write(c,ROOT/'exports'/c['style'])
        # Five title samples on one compact sheet; no new thumbnail generation.
        blocks.append(f'<g transform="translate({i*400} 0) scale(.37) translate(0 -900)">{title(c)}</g>')
    sheet='<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="280" viewBox="0 0 2000 280"><rect width="2000" height="280" fill="#28333B"/>'+''.join(blocks)+'</svg>'
    (ROOT/'apercu-cinq-styles.png').write_bytes(resvg_py.svg_to_bytes(svg_string=sheet))
    logo_svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">'+logo()+'</svg>'
    (ROOT/'exports/logo-hpb-transparent.svg').write_text(logo_svg,encoding='utf-8')
    (ROOT/'exports/logo-hpb-transparent.png').write_bytes(resvg_py.svg_to_bytes(svg_string=logo_svg))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--all',action='store_true'); p.add_argument('--config'); p.add_argument('--background'); p.add_argument('--out')
    a=p.parse_args()
    if a.all: all_templates()
    elif a.config and a.out:
        write(json.loads(Path(a.config).read_text(encoding='utf-8')),a.out,a.background)
    else: p.error('--all ou --config et --out requis')
