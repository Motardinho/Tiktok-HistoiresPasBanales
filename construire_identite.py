"""Identité vectorielle et exports PNG de Histoires pas banales."""
from pathlib import Path
import base64,html,json,shutil,subprocess,zipfile
import requests
from PIL import Image,ImageDraw,ImageFont,ImageChops

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'identite'/'histoires-pas-banales'
OUT.mkdir(parents=True,exist_ok=True)
for folder in ['logos','gabarits','polices','apercus']: (OUT/folder).mkdir(exist_ok=True)
INK='#12151C';YELLOW='#FFE24A';CREAM='#F7F3E9';CORAL='#FF624E';MUTED='#99A1AF'
FONT=ROOT/'assets/fonts/Poppins-ExtraBold.ttf'
REG=Path('C:/Windows/Fonts/segoeui.ttf')
def font(size,bold=True):return ImageFont.truetype(str(FONT if bold else REG),size)
FONT64=base64.b64encode(FONT.read_bytes()).decode()
CSS="<style>@font-face{font-family:HPB;src:url(data:font/ttf;base64,"+FONT64+") format('truetype')}text{font-family:HPB,'Arial Black',sans-serif}</style>"
SHELL=[(125,210),(785,145),(835,715),(425,682),(302,790),(310,672),(190,662)]
QUESTION=[(290,355),(290,258),(515,258),(515,451),(415,451),(415,508),(334,508),(334,397),(420,397),(420,337),(375,337),(375,355)]
EXCLAMATION=[(540,258),(642,258),(642,508),(540,508)]
QDOT=[(334,558),(415,558),(415,639),(334,639)]
EDOT=[(550,558),(632,558),(632,640),(550,640)]

def mark_image(size=1024,color=YELLOW,spark=CORAL,punctuation='?!'):
 im=Image.new('RGBA',(1024,1024))
 d=ImageDraw.Draw(im)
 d.polygon(SHELL,fill=color)
 if punctuation=='!':
  d.rounded_rectangle((430,280,532,490),radius=27,fill=(0,0,0,0))
  d.ellipse((431,552,531,652),fill=(0,0,0,0))
 else:
  letters=Image.new('L',(1024,1024));ld=ImageDraw.Draw(letters)
  f=font(500);box=d.textbbox((0,0),'?!',font=f)
  x=280;y=450-(box[1]+box[3])/2
  ld.text((x,y),'?',font=f,fill=255)
  # Alléger uniquement les points, sans modifier le corps ni l'espacement des signes.
  ld.rectangle((310,525,680,654),fill=0)
  ld.ellipse((336,551,424,629),fill=255)
  exclamation=Image.new('L',(1024,1024));ed=ImageDraw.Draw(exclamation)
  ed.text((x+f.getlength('?')-44,y),'!',font=f,fill=255)
  ed.rectangle((530,525,700,654),fill=0)
  ed.ellipse((567,551,655,629),fill=255)
  exclamation=exclamation.rotate(-12,resample=Image.Resampling.BICUBIC,center=(611,590))
  letters=ImageChops.offset(letters,20,-26)
  exclamation=ImageChops.offset(exclamation,-20,0)
  letters=ImageChops.lighter(letters,exclamation)
  letters=letters.rotate(5.625,resample=Image.Resampling.BICUBIC,center=(480,450))
  letters=ImageChops.offset(letters,-22,0)
  im.putalpha(ImageChops.subtract(im.getchannel('A'),letters))
 return im.rotate(6,resample=Image.Resampling.BICUBIC).resize((size,size),Image.Resampling.LANCZOS)

def mark_svg(color=YELLOW,spark=CORAL):
 def poly(points,fill):return '<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{fill}"/>'
 f=font(500);b=f.getbbox('?!');baseline=450+f.getmetrics()[0]-(b[1]+b[3])/2
 mask=poly(SHELL,'white')+f'<g transform="translate(-22 0) rotate(-5.625 480 450)"><clipPath id="upper"><rect width="1024" height="525"/></clipPath><g transform="translate(20 -26)"><text x="280" y="{baseline}" font-size="500" fill="black" clip-path="url(#upper)">?</text><ellipse cx="380" cy="590" rx="44" ry="39" fill="black"/></g><g transform="translate(-20 0) rotate(12 611 590)"><text x="506" y="{baseline}" font-size="500" fill="black" clip-path="url(#upper)">!</text><ellipse cx="611" cy="590" rx="44" ry="39" fill="black"/></g></g>'
 return f'''<g transform="rotate(-6 512 512)"><mask id="cut"><rect width="1024" height="1024" fill="black"/>{mask}</mask><rect width="1024" height="1024" fill="{color}" mask="url(#cut)"/></g>'''

def video_mark_image(size=1024):
 im=Image.new('RGBA',(1024,1024));ImageDraw.Draw(im).polygon(SHELL,fill=INK)
 im=im.rotate(6,resample=Image.Resampling.BICUBIC);im.alpha_composite(mark_image())
 return im.resize((size,size),Image.Resampling.LANCZOS)

def svg_file(name,width,height,body,background=None):
 bg=f'<rect width="{width}" height="{height}" fill="{background}"/>' if background else ''
 (OUT/'logos'/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{CSS}{bg}{body}</svg>',encoding='utf-8')

def text(d,xy,s,size,fill=CREAM,bold=True):d.text(xy,s,font=font(size,bold),fill=fill,stroke_width=0)
def label(d,xy,s,fill=MUTED):text(d,xy,s,22,fill)

def logos():
 mark=mark_image()
 mark.save(OUT/'logos/symbole-couleur.png')
 svg_file('symbole-couleur.svg',1024,1024,mark_svg())
 avatar=Image.new('RGBA',(1024,1024),INK);avatar.alpha_composite(mark)
 avatar.convert('RGB').save(OUT/'logos/avatar-tiktok-1024.png')
 svg_file('avatar-tiktok.svg',1024,1024,mark_svg(),INK)
 # Tests réels du signe au format miniature.
 for size in [48,96,180]:avatar.resize((size,size),Image.Resampling.LANCZOS).save(OUT/f'apercus/avatar-{size}.png')
 for name,fg,accent in [('sombre',CREAM,YELLOW),('clair',INK,INK)]:
  im=Image.new('RGBA',(2400,720));im.alpha_composite(mark_image(680),(0,5))
  d=ImageDraw.Draw(im)
  text(d,(710,125),'HISTOIRES',138,fg)
  text(d,(710,300),'PAS BANALES',157,accent)
  im.save(OUT/f'logos/logo-horizontal-{name}.png')
  body='<g transform="translate(0 5) scale(0.6640625)">'+mark_svg()+'</g>'
  body+=f'<text x="710" y="278" font-size="138" fill="{fg}">HISTOIRES</text><text x="710" y="474" font-size="157" fill="{accent}">PAS BANALES</text>'
  svg_file(f'logo-horizontal-{name}.svg',2400,720,body)
 for name,color in [('blanc',CREAM),('noir',INK)]:
  mono=mark_image(color=color,spark=color);mono.save(OUT/f'logos/symbole-{name}.png')
  svg_file(f'symbole-{name}.svg',1024,1024,mark_svg(color,color))
 stack=Image.new('RGB',(1600,1600),INK);stack.paste(mark_image(740),(430,40),mark_image(740))
  # Signature composée pour les présentations, pas pour l'avatar miniature.
 d=ImageDraw.Draw(stack)
 for s,y,size,col in [('HISTOIRES',820,138,CREAM),('PAS BANALES',1000,153,YELLOW)]:
  x=(1600-d.textlength(s,font=font(size)))/2;text(d,(x,y),s,size,col)
 text(d,(300,1300),'Le réel a de quoi surprendre.',52,CREAM)
 stack.save(OUT/'logos/logo-empile-fond-encre.png')

def source_frame(video,t,out,center=.53):
 vf=f"crop=trunc(ih*9/16/2)*2:ih:max(0\\,min(iw-ow\\,iw*{center}-ow/2)):0,scale=1080:1920"
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-vf',vf,str(out)],check=True)

def cover(name,source,t,title_lines,topic,center=.53):
 raw=OUT/'apercus'/f'{name}-image.png';source_frame(source,t,raw,center)
 im=Image.open(raw).convert('RGBA')
 # Habillage éditorial, le plan vidéo réel reste la matière principale.
 shade=Image.new('RGBA',im.size);d=ImageDraw.Draw(shade)
 for y in range(1920):
  a=int(205*max(0,(y-850)/1070))
  if a:d.line((0,y,1080,y),fill=(18,21,28,a))
 im.alpha_composite(shade)
 badge=video_mark_image(170);im.alpha_composite(badge,(32,35))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((225,79,225+int(d.textlength(topic,font=font(35)))+60,150),radius=14,fill=INK)
 bbox=d.textbbox((0,0),topic,font=font(35))
 text(d,(255,79+(71-(bbox[3]-bbox[1]))/2-bbox[1]),topic,35,YELLOW)
 y=1110
 for i,s in enumerate(title_lines):
  color=YELLOW if i==len(title_lines)-1 else CREAM
  # Taille du titre adaptée à la longueur réelle du mot.
  sz=112
  while d.textlength(s,font=font(sz))>930:sz-=2
  d.text((75,y),s,font=font(sz),fill=color,stroke_width=5,stroke_fill=INK)
  y+=139
 text(d,(76,1780),'HISTOIRES PAS BANALES',32,CREAM)
 im.convert('RGB').save(OUT/f'gabarits/{name}.png')
 return im

def board():
 W,H=2000,2240
 im=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,760),fill=INK)
 label(d,(90,58),'IDENTITÉ VISUELLE • 01',MUTED)
 logo=Image.open(OUT/'logos/logo-horizontal-sombre.png');logo.thumbnail((1510,490));im.paste(logo,(20,150),logo)
 text(d,(105,635),'Le réel a de quoi surprendre.',46,CREAM)
 av=Image.open(OUT/'logos/avatar-tiktok-1024.png').convert('RGBA').resize((340,340),Image.Resampling.LANCZOS)
 mask=Image.new('L',(340,340));ImageDraw.Draw(mask).ellipse((0,0,339,339),fill=255)
 im.paste(av,(1570,220),mask)
 label(d,(1570,590),'AVATAR • LISIBLE EN PETIT',CREAM)
 label(d,(90,815),'01 / UNE PALETTE QUI RÉVEILLE',INK)
 cols=[('ENCRE',INK,'#12151C'),('DÉCLIC',YELLOW,'#FFE24A'),('PAPIER',CREAM,'#F7F3E9'),('SURPRISE',CORAL,'#FF624E')]
 for i,(name,col,hx) in enumerate(cols):
  x=90+i*475;d.rounded_rectangle((x,875,x+440,1065),radius=26,fill=col,outline=INK,width=2)
  fg=CREAM if i==0 else INK
  text(d,(x+24,900),name,33,fg);text(d,(x+24,997),hx,24,fg)
 label(d,(90,1123),'02 / UNE VOIX DIRECTE',INK)
 text(d,(90,1180),'Montrer d’abord.',81,INK)
 text(d,(90,1285),'Expliquer ensuite.',81,INK)
 text(d,(95,1430),'Curieux. Concret. Vivant.',37,INK)
 text(d,(95,1500),'Des histoires vraies. Des faits qui étonnent.',30,INK,False)
 label(d,(90,1620),'03 / LE SYSTÈME TYPOGRAPHIQUE',INK)
 text(d,(90,1680),'Poppins ExtraBold',58,INK)
 text(d,(95,1772),'Les mots qui accrochent.',33,INK)
 text(d,(95,1840),'Poppins Regular pour les textes courants.',28,INK,False)
 label(d,(90,2000),'SIGNATURE',INK)
 text(d,(90,2050),'« Pas banal, hein ? »',45,INK)
 # Exemples éditoriaux sur de vrais plans : pas une planche d'images IA.
 for i,name in enumerate(['couverture-espace','couverture-trafic']):
  image=Image.open(OUT/f'gabarits/{name}.png');image.thumbnail((430,840))
  x=1060+i*460
  d.rounded_rectangle((x-10,1150,x+440,1940),radius=35,fill=INK)
  im.paste(image,(x,1160))
 label(d,(1060,1990),'PLEIN ÉCRAN. ACTION. MOTS FORTS.',INK)
 text(d,(1060,2045),'Le hook commence dans l’image.',29,INK,False)
 im.save(OUT/'apercu-identite.png')

def templates():
 # Calque réutilisable, transparent ; les sous-titres sont produits séparément.
 overlay=Image.new('RGBA',(1080,1920));overlay.alpha_composite(video_mark_image(128),(24,32))
 overlay.save(OUT/'gabarits/logo-video-transparent-1080x1920.png')
 end=Image.new('RGBA',(1080,1920),INK);end.alpha_composite(mark_image(570),(255,360));d=ImageDraw.Draw(end)
 for s,y,sz,c in [('HISTOIRES',980,86,CREAM),('PAS BANALES',1090,91,YELLOW),('Pas banal, hein ?',1370,53,CREAM)]:
  x=(1080-d.textlength(s,font=font(sz)))/2;text(d,(x,y),s,sz,c)
 end.convert('RGB').save(OUT/'gabarits/signature-fin.png')

def guide():
 tokens={'nom':'Histoires pas banales','baseline':'Le réel a de quoi surprendre.','signature':'Pas banal, hein ?',
 'couleurs':{'encre':INK,'declic':YELLOW,'papier':CREAM,'surprise':CORAL},'typographies':{'titres':'Poppins ExtraBold','textes':'Poppins Regular'},
 'video':{'format':[1080,1920],'hook':'Action la plus étonnante visible dès la première image ; préserver cette démonstration pendant les premières secondes.',
 'plans':'En général 1,7 à 3 secondes ; prolonger jusqu’à 4,5 secondes pour laisser lire un mouvement utile.',
 'sous_titres':{'police':'Poppins ExtraBold','taille':84,'mots_max':5,'couleur':CREAM,'mot_actif':YELLOW,'contour':INK},
 'logo':'Petit signe dans un coin libre ; pas d’écran logo avant le hook.'}}
 (OUT/'brand-tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2),encoding='utf-8')
 doc='''# Histoires pas banales

**Le réel a de quoi surprendre.**

Une marque curieuse, accessible et vivante pour des histoires vraies, des faits étonnants et des classements expliqués. Le nom se prononce naturellement. La promesse : montrer ce qui surprend, puis donner les clés pour le comprendre.

## Le logo

Une bulle de récit jaune, légèrement inclinée, avec une interrogation et une exclamation en réserve sans point extérieur. La bulle raconte ; l’interrogation suscite la curiosité ; l’exclamation signale le déclic ; les angles francs donnent du caractère.

- Avatar : le symbole seul sur fond encre. Le nom entier serait illisible en miniature.
- Logo horizontal : pour les présentations, bandeaux et génériques. Variante sombre sur fond sombre ; variante claire sur fond clair.
- Espace libre : au moins la largeur du point de l’exclamation autour du logo.
- Taille : symbole au moins 32 px ; logo complet au moins 260 px de large. Exports avatar en 1024 px.
- Garder les proportions. Ne pas ajouter de lueur, relief, ombre ou contour. Les SVG restent éditables ; les PNG ont un rendu fixe.

## Couleurs

| Nom | Hex | Usage |
|---|---|---|
| Encre | #12151C | Fonds, contours, contraste |
| Déclic | #FFE24A | Symbole, mot prononcé, chiffre qui accroche |
| Papier | #F7F3E9 | Texte principal, fonds clairs |
| Surprise | #FF624E | Petit détail, contrepoint ou précision ponctuelle |

Sur les supports graphiques : environ 65 % d’encre, 25 % de papier, 8 % de jaune et 2 % de corail. Dans une vidéo, l’image réelle reste dominante : ces proportions ne servent pas à couvrir le plan. Texte encre sur jaune ou corail ; papier sur encre. Éviter jaune ou corail en petits caractères sur papier.

## Typographie

**Poppins ExtraBold** : logo, titres, couvertures et sous-titres. Titres courts, deux à quatre mots par ligne. **Poppins Regular** : légendes de présentation et textes courants. Les polices et la licence SIL OFL sont dans `polices/`.

## La règle vidéo

**Le hook se voit avant de s’expliquer.**

1. Première image : montrer l’action, l’objet ou le détail le plus intéressant, en gros plan quand il le faut. Pour les astronautes : la machine doit déjà osciller, pas de visage qui parle ni de logo en introduction.
2. Laisser voir la démonstration pendant les premières secondes. Un changement de plan doit servir la compréhension ; ne pas couper l’action intéressante trop tôt.
3. Ensuite : expliquer avec des images qui prouvent ce que raconte la voix. Alterner gros plan, geste, plan de situation. Cheveux flottants pour la microgravité ; moteur ou véhicule pour la voiture ; circulation dense pour les bouchons.
4. Plein écran portrait 1080 × 1920. Recadrage pensé pour le sujet ; éviter les petites vidéos perdues dans un grand fond flou.
5. Plans courts et variés, en général 1,7 à 3 secondes. Laisser jusqu’à 4,5 secondes si un mouvement mérite d’être compris. Pas d’accélération qui fausse une démonstration.
6. Sous-titres : cinq mots maximum, papier avec contour encre, mot prononcé en jaune. Garder visages, mains et mécanismes lisibles ; adapter la position au plan.
7. Pas d’introduction de marque avant le hook. Petit signe dans un coin libre, facultatif. Ne pas laisser un grand titre permanent manger les cheveux, le visage ou le geste.
8. Fin courte : « Pas banal, hein ? » ou question liée au sujet. Le carton fourni est une signature de moins d’une seconde, pas une pause obligatoire.

## Le ton

Curieux, précis, oral. Une idée à la fois. Nommer le détail concret : « Le support oscille plus vite quand il est vide. » Faire sentir l’étonnement sans promettre l’impossible. Dire la source, la date et les limites d’un classement quand elles changent le sens.

Éviter les « Tu ne vas JAMAIS croire », le faux mystère, les capitales partout et les adjectifs grandiloquents. La surprise vient des faits et des images.

## Signature éditoriale

- Nom affiché : **Histoires pas banales**.
- Identifiant visé : **@histoirespasbanales** ; disponibilité à confirmer dans TikTok, non réservé par cette livraison.
- Bio proposée : **Des faits fous. Des histoires vraies. 👀 Rien de banal.**
- Baseline : **Le réel a de quoi surprendre.**
- Signature orale : **Pas banal, hein ?**
- Séries : **Le détail qui change tout**, **Comment c’est possible ?**, **Vrai, mais surprenant**.
- « Dossier clos » peut rester la signature d’une série d’enquêtes ; il n’a pas besoin de fermer tous les faits et tous les tops.

## Fichiers

- `logos/` : avatar, symbole, versions horizontales, variantes monochromes, PNG et SVG.
- `gabarits/` : deux exemples de couvertures sur des séquences réelles, calque de logo transparent et carton de fin.
- `apercu-identite.png` : planche d’ensemble.
- `brand-tokens.json` : couleurs et réglages vidéo réutilisables.
- `sources.md` : crédits des images de démonstration et des polices.

Ce kit définit la nouvelle identité. Aucun nom ni avatar n’a été modifié sur TikTok. Les vidéos comparatives restent des livraisons distinctes ; le kit ne réécrit pas leurs narrations ni leurs tampons déjà rendus.
'''
 (OUT/'charte.md').write_text(doc,encoding='utf-8')
 (OUT/'sources.md').write_text('''# Sources et fabrication

Logo et habillage créés en vectoriel par code, avec exports PNG. Aucun générateur d’images n’a été utilisé pour ce kit.

Le symbole est un dessin géométrique original, avec une bulle en quadrilatère irrégulier à angles francs et une ponctuation Poppins ExtraBold, agrandie et resserrée. Les textes SVG utilisent Poppins embarqué ; la police est également fournie avec sa licence.

Polices : [Poppins, Google Fonts / Indian Type Foundry](https://github.com/google/fonts/tree/main/ofl/poppins), licence SIL OFL 1.1.

Exemple espace : [Agence spatiale canadienne / NASA, David Saint-Jacques](https://www.asc-csa.gc.ca/eng/multimedia/search/video/18332).

Exemple trafic : [ubeyonroad / Pexels, Urban Traffic Jam in New York City](https://www.pexels.com/video/urban-traffic-jam-in-new-york-city-34118766/).

Les images d’exemple illustrent l’habillage et ne constituent pas des images exclusives de la marque. Les fichiers sources vidéo sont conservés dans le projet. Génération reproductible : `construire_identite.py`.
''',encoding='utf-8')
 # Page autonome à ouvrir localement : tous les aperçus restent dans le même dossier.
 page='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Histoires pas banales — identité</title><style>@font-face{font-family:Poppins;src:url(polices/Poppins-ExtraBold.ttf);font-weight:800}*{box-sizing:border-box}body{margin:0;background:#12151c;color:#f7f3e9;font:18px/1.6 system-ui}main{max-width:1180px;margin:auto;padding:48px 28px}h1,h2{font-family:Poppins;font-weight:800;line-height:1.15}h1{font-size:clamp(32px,6vw,66px)}h2{font-size:32px;margin-top:64px}p{max-width:760px}a{color:#ffe24a}img{max-width:100%;height:auto}.board{border-radius:18px;margin:28px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:22px}.card{background:#212631;padding:24px;border-radius:18px}.swatch{height:90px;border-radius:12px;margin-bottom:14px}.small{color:#99a1af;font-size:15px}.avatar{width:140px;border-radius:50%}li{margin:12px 0}.button{display:inline-block;padding:12px 20px;background:#ffe24a;color:#12151c;border-radius:10px;text-decoration:none;font-weight:700;margin:8px 10px 8px 0}</style><main><img class="avatar" src="logos/avatar-tiktok-1024.png" alt="Symbole"><p class="small">IDENTITÉ VISUELLE</p><h1>Histoires<br>pas banales.</h1><p>Le réel a de quoi surprendre.</p><a class="button" href="logos/avatar-tiktok-1024.png" download>Avatar TikTok</a><a class="button" href="charte.md">Lire la charte</a><img class="board" src="apercu-identite.png" alt="Planche d’identité complète"><h2>Le hook se voit avant de s’expliquer.</h2><p>Montrer le plus étonnant dès la première image. Laisser l’action se lire. Expliquer ensuite avec des plans qui démontrent ce que raconte la voix.</p><div class="grid"><div class="card"><h2 style="margin-top:0">Le signe</h2><img src="logos/symbole-couleur.png" alt="Bulle avec exclamation"><p>Une bulle qui raconte. Des angles francs. Une ponctuation forte.</p></div><div class="card"><h2 style="margin-top:0">Le rythme</h2><p>Portrait plein écran. Plans variés. Mots forts. Une signature courte.</p><p>« Pas banal, hein ? »</p></div></div><h2>Les couleurs</h2><div class="grid">'''
 for name,c in [('Encre',INK),('Déclic',YELLOW),('Papier',CREAM),('Surprise',CORAL)]:page+=f'<div class="card"><div class="swatch" style="background:{c}"></div><b>{name}</b><br>{c}</div>'
 page+='</div><h2>Des couvertures qui donnent envie de voir.</h2><div class="grid"><img src="gabarits/couverture-espace.png" alt="Exemple de couverture espace"><img src="gabarits/couverture-trafic.png" alt="Exemple de couverture trafic"></div><h2>Prêt à utiliser</h2><ul><li><a href="logos/logo-horizontal-sombre.svg">Logo sur fond sombre — SVG</a></li><li><a href="logos/logo-horizontal-clair.svg">Logo sur fond clair — SVG</a></li><li><a href="gabarits/logo-video-transparent-1080x1920.png">Calque vidéo transparent</a></li><li><a href="gabarits/signature-fin.png">Carton de signature</a></li><li><a href="brand-tokens.json">Palette et réglages</a></li><li><a href="sources.md">Sources et crédits</a></li></ul><p class="small">Identité préparée pour le projet. Aucun changement de compte TikTok effectué.</p></main></html>'
 (OUT/'index.html').write_text(page,encoding='utf-8')

def main():
 shutil.copy2(FONT,OUT/'polices/Poppins-ExtraBold.ttf')
 for name in ['OFL.txt','Poppins-Regular.ttf']:
  url='https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/'+name
  r=requests.get(url,timeout=30);r.raise_for_status();(OUT/'polices'/name).write_bytes(r.content)
 logos()
 cover('couverture-espace',ROOT/'assets/sources-reelles/astronautes-masse.mp4',30,['SE PESER','DANS','L’ESPACE ?'],'COMMENT C’EST POSSIBLE ?')
 cover('couverture-trafic',ROOT/'assets/sources-reelles/new-york-bouchons.mp4',2,['102 HEURES','DANS LES','BOUCHONS.'],'LE CHIFFRE QUI SURPREND',.5)
 templates();board();guide()
 with zipfile.ZipFile(OUT.parent/'Histoires-pas-banales-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in OUT.rglob('*'):
   if p.is_file() and not p.name.startswith(('avatar-tiktok-v','comparaison-logos-v')):z.write(p,p.relative_to(OUT.parent))
 print(OUT,flush=True)

if __name__=='__main__':main()
