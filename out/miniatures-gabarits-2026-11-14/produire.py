"""Lot HPB : couvertures séparées, sans modification des dossiers vidéo."""
import base64,copy,html,json,sys,zipfile
from pathlib import Path
import resvg_py

ROOT=Path(__file__).resolve().parents[2]
DEST=Path(__file__).resolve().parent
TEMPLATES=ROOT/'identite/histoires-pas-banales/gabarits-miniatures'
sys.path.insert(0,str(TEMPLATES))
from render import write,title,logo,lot_library

LINES={
13:["SE PESER","DANS L'ESPACE"],
14:['TOP 3','DES VOITURES','LES PLUS RAPIDES','2026'],
15:['TOP 3 DES VILLES','LES PLUS','EMBOUTEILLÉES','2026'],
16:['TOP 3 DES ARMÉES','LES PLUS','PUISSANTES','2026'],
18:['TOP 3 DES','PLUS GRANDS PAYS','DU MONDE 2026'],
19:['TOP 3 DES','CASCADES DE','JACKIE CHAN'],
20:['TOP 3','DES TÉLÉPHONES','LES PLUS CHERS','2026'],
21:['TOP 3 DES LANGUES','LES PLUS PARLÉES','2026'],
22:['TOP 3 DES PAYS','LES PLUS RICHES','2026'],
23:['TOP 3 DES','GRATTE-CIEL','LES PLUS HAUTS','2026'],
24:['POURQUOI INONDER','UNE FUSÉE ?'],
25:['TOP 3 DES','MONTAGNES RUSSES','LES PLUS RAPIDES','2026'],
26:['PERDU','9 JOURS','DANS LE SAHARA'],
27:['DEMI-TOUR','DANS LA','TEMPÊTE'],
28:["L'OM A",'ACHETÉ','UN MATCH'],
29:["IL S'EST FAIT",'PASSER POUR','UN MINISTRE'],
30:['LA JUVE','ENVOYÉE','EN SÉRIE B'],
31:['POGBA','BRAQUÉ','POUR 13 MILLIONS'],
32:["L'ESPAGNE",'A VOLÉ',"L'OR PARALYMPIQUE"],
33:['ILS ONT MARQUÉ','149 BUTS','CONTRE LEUR CAMP'],
34:['IL TRICHAIT','AUX','ÉCHECS'],
35:['RENAULT A FAIT','CRASHER','SON PILOTE'],
36:['MCLAREN','TRAHIE','PAR UNE PHOTOCOPIE'],
37:['LA FIFA A PAYÉ','POUR LA MAIN',"D'HENRY"],
38:['TOP 10 DES PLUS','GROSSES','CORRUPTIONS DU FOOT'],
39:["L'ENTRAÎNEUR",'BOYCOTTÉ','DANS TOUT LE PAYS'],
40:['TOP 10','DES BUTS LES PLUS','DÉGUEULASSES'],
41:['TOP 10 DES MAILLOTS','LES PLUS MOCHES','DU FOOT FRANÇAIS'],
42:['TOP 10','DES PLUS BEAUX','BALLONS DE FOOT'],
43:['TOP 3 DES','MOTOS DE SÉRIE','LES PLUS RAPIDES','2026'],
44:['TOP 5','DES BUTS LES PLUS','DÉGUEULASSES']}

def fit(text,family,height,maxwidth=870):
    a=lot_library()['alphabets'][family]
    missing=set(text)-set(a)-{' '}
    assert not missing,(text,missing)
    width=sum(30 if ch==' ' else a[ch]['advance'] for ch in text)
    h=min(height,maxwidth*100/width)
    return width*h/100,h

def configure(item):
    n=item['number'];style=item['style'];lines=LINES[n]
    if n in (24,31):
        return json.loads((TEMPLATES/(style+'.json')).read_text(encoding='utf-8'))
    rows=[]
    for i,text in enumerate(lines):
        last=i==len(lines)-1
        if style=='racing':
            family='racing-display' if i==0 or text=='2026' else 'racing-text'
            height=94 if i==0 else 87
        elif style=='pop':
            family='pop-display' if i==0 else 'pop-wide';height=94 if i==0 else 80
        elif style=='sticker':
            family='sticker-display' if i==0 else 'sticker-text';height=125 if i==0 else 88
        elif style=='science':family='science-condensed';height=125 if len(lines)==2 else 102
        else:
            emphasis=2 if n==16 else 1
            family='magazine-block' if i==emphasis else 'magazine-tall'
            height=205 if i==0 else (110 if i==emphasis else 150)
            if n==16 and i==1:height=85
            if text=='2026':height=92
        w,h=fit(text,family,height,850 if style=='science' else 870)
        r=dict(text=text,x=110,y=0,w=round(w,3),h=round(h,3),traced_row=style+'-0',traced_family=family,compose=True,alphabet='lot',color='#FFFFFF')
        if style=='magazine':
            if i==(2 if n==16 else 1):r['band']='#FB3231'
            elif i>=2:r['color']='#F8FB35'
        elif style=='science':r.update(band='#FBD203',color='#000000')
        elif style=='pop':r.update(band='#0413BF' if i<2 else '#FCEB03',color='#FFFFFF' if i<2 else '#050509')
        elif style=='sticker' and last:r.update(band='#FBD91A',color='#000000')
        elif style=='racing' and (i==0 or i==2 or text=='2026'):r['band']='#E81A03'
        rows.append(r)
    gap=34 if style in ('science','pop') else (22 if style=='magazine' else 28)
    total=sum(r['h'] for r in rows)+gap*(len(rows)-1)
    y=1445-total
    for i,r in enumerate(rows):
        r['y']=round(y,3)
        if style=='sticker':r['x']=110+(870-r['w'])/2
        if 'band' in r:
            x=r['x'];w=r['w'];h=r['h']
            if style=='magazine':
                r['polygon']=[[x-20,y-15],[x+w+20,y-15],[x+w+20,y+h+15],[x-20,y+h+15]]
            else:
                skew=40 if style=='racing' else 25
                r['polygon']=[[x-14+skew,y-16],[x+w+26+skew,y-16],[x+w+26,y+h+16],[x-14,y+h+16]]
                if style=='racing':r['layers']=[[24,22,'#000A24']]
                if style=='science':r['layers']=[[10,14,'#090E20']]
                if style=='pop':r['layers']=[[-25,26,'#FC0076']]
                if style=='sticker':r['layers']=[[20,18,'#000000'],[10,11,'#8A00CD']]
        y+=r['h']+gap
    c=dict(style=style,font='anton',slant=0,rows=rows)
    if style=='science':c['rotation']=-6
    if style=='pop':c['pop_mark']=[rows[0]['x']+rows[0]['w']+46,rows[0]['y']+40]
    return c

def run():
    items=json.loads((DEST/'manifest.json').read_text(encoding='utf-8'))
    done=[]
    for r in items:
        n=r['number'];background=DEST/'fonds'/f'{n}.png'
        if not background.exists():continue
        c=configure(r)
        assert ' '.join(LINES[n])==r['title'],(n,' '.join(LINES[n]),r['title'])
        (DEST/'configs'/f'{n}.json').write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
        src=write(c,DEST/'png'/str(n),background)
        (DEST/'png'/f'{n}.svg').replace(DEST/'svg'/f'{n}.svg')
        (DEST/'apercus'/f'{n}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=src,width=360))
        r['png']=f'png/{n}.png';r['config']=f'configs/{n}.json';r['background']=f'fonds/{n}.png'
        done.append(r)
    (DEST/'livraison.json').write_text(json.dumps(done,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Miniatures rendues :',len(done),'/',len(items))
    return done

def gallery(items):
    cards=[]
    for r in items:
        n=r['number'];s=html.escape(r['style']);t=html.escape(r['title'])
        cards.append(f'<article data-style="{s}"><a href="png/{n}.png"><img src="apercus/{n}.png" alt="{t}" loading="lazy"></a><p><b>{n} · {s}</b><br>{t}</p><a href="png/{n}.png" download>PNG HD</a> · <a href="svg/{n}.svg" download>SVG</a></article>')
    page='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HPB — 31 miniatures</title><style>body{margin:0;background:#10141b;color:#f5f5f5;font:16px system-ui}header{padding:28px 4vw;position:sticky;top:0;background:#10141bf5;z-index:2;border-bottom:1px solid #333}h1{margin:0 0 8px;font-size:25px}select{padding:8px;margin-top:14px}main{padding:25px 4vw;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:24px}article{background:#1b222d;padding:12px;border-radius:12px}img{width:100%;display:block;border-radius:5px}p{font-size:14px;line-height:1.4}a{color:#ffe447}small{color:#bcc5d4}</style><header><h1>Histoires pas banales — miniatures</h1><small>31 propositions · 14 novembre 2026 · Logo HPB validé · Cliquez sur une miniature pour l'ouvrir en HD.</small><br><select id="style"><option value="all">Tous les styles</option><option>racing</option><option>pop</option><option>science</option><option>magazine</option><option>sticker</option></select></header><main>'''+''.join(cards)+'''</main><script>document.querySelector('#style').onchange=e=>document.querySelectorAll('article').forEach(a=>a.hidden=e.target.value!=='all'&&a.dataset.style!==e.target.value);</script></html>'''
    (DEST/'galerie.html').write_text(page,encoding='utf-8')
    for start in range(0,len(items),8):
        parts=[]
        for j,r in enumerate(items[start:start+8]):
            data=base64.b64encode((DEST/r['png']).read_bytes()).decode();x=j%4*270;y=j//4*505
            parts.append(f'<image x="{x}" y="{y}" width="270" height="480" href="data:image/png;base64,{data}"/><text x="{x+8}" y="{y+499}" fill="white" font-size="16">{r["number"]} · {r["style"]}</text>')
        sheet='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1010"><rect width="1080" height="1010" fill="#111"/>'+''.join(parts)+'</svg>'
        (DEST/f'planche-{start//8+1}.png').write_bytes(resvg_py.svg_to_bytes(svg_string=sheet))

if __name__=='__main__':
    if '--gallery' in sys.argv:gallery(json.loads((DEST/'livraison.json').read_text(encoding='utf-8')))
    else:run()
