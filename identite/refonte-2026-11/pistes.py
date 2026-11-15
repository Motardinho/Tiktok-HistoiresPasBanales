"""Refonte du branding HPB, 14 nov 2026 : quatre pistes d'avatar et de bannière YouTube, puis une planche.

Rendu : HTML/SVG -> PNG par Chrome sans interface. Usage : python identite/refonte-2026-11/pistes.py
"""
from pathlib import Path
import subprocess, sys

ICI = Path(__file__).resolve().parent
ROOT = ICI.parents[1]
FONTS = (ROOT / 'assets/fonts').as_uri()
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
SORTIE = ICI / 'pistes'
SORTIE.mkdir(exist_ok=True)

ENCRE, JAUNE, PAPIER, ROUGE, KRAFT = '#12151C', '#FFE24A', '#F7F3E9', '#E8141C', '#E3C27E'

CSS = f"""<style>
@font-face{{font-family:Epaules;src:url({FONTS}/BigShouldersDisplay-Variable.ttf);font-weight:100 900}}
@font-face{{font-family:Poppins;src:url({FONTS}/Poppins-ExtraBold.ttf);font-weight:800}}
@font-face{{font-family:Bebas;src:url({FONTS}/BebasNeue-Regular.ttf)}}
@font-face{{font-family:Montserrat;src:url({FONTS}/Montserrat-Variable.ttf);font-weight:100 900}}
html,body{{margin:0;padding:0;overflow:hidden}}
svg{{display:block}}
</style>"""

GRAIN = """<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/>
<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.15"/>
<feComposite in="SourceGraphic" operator="in"/></filter>
<filter id="tampon"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" result="b"/>
<feDisplacementMap in="SourceGraphic" in2="b" scale="9" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="11" result="n"/>
<feColorMatrix in="n" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.55" result="m"/>
<feComposite in="d" in2="m" operator="in"/></filter>"""

# --- Symboles : chacun dessiné dans un carré de 1080, contenu utile dans le cercle central (rayon ~ 450).

def symbole_a():  # Bulle XXL : évolution de l'actuel, HPB encre sur jaune, plus gros et plus lisible.
    return f"""<rect width="1080" height="1080" fill="{ENCRE}"/>
<g transform="rotate(-7 540 540)">
 <polygon points="150,250 930,215 955,760 470,790 345,925 350,795 170,800" fill="{JAUNE}"/>
 <text x="555" y="640" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="330"
  letter-spacing="-18" fill="{ENCRE}">HPB</text>
</g>"""

def symbole_b():  # Carton : sport + sanction. Carton rouge derrière, jaune devant.
    return f"""<rect width="1080" height="1080" fill="{ENCRE}"/>
<g transform="rotate(14 560 540)"><rect x="345" y="185" width="440" height="640" rx="34" fill="{ROUGE}"/></g>
<g transform="rotate(-9 520 560)">
 <rect x="275" y="215" width="470" height="680" rx="36" fill="{JAUNE}"/>
 <text x="510" y="660" text-anchor="middle" font-family="Epaules" font-weight="900" font-size="290"
  letter-spacing="-4" fill="{ENCRE}">HPB</text>
</g>"""

def symbole_c():  # Tabloïd : rouge plein, lettres blanches condensées, bandeau EXCLU.
    return f"""<rect width="1080" height="1080" fill="{ROUGE}"/>
<text x="540" y="700" text-anchor="middle" font-family="Epaules" font-weight="900" font-size="560"
 letter-spacing="-10" fill="#FFFFFF" transform="skewX(-6) translate(60 0)">HPB</text>
<g transform="rotate(-8 540 800)">
 <rect x="150" y="745" width="780" height="130" fill="{JAUNE}"/>
 <text x="540" y="845" text-anchor="middle" font-family="Epaules" font-weight="900" font-size="112"
  letter-spacing="8" fill="{ENCRE}">SCANDALE</text>
</g>"""

def symbole_d():  # Dossier : chemise kraft et tampon rouge HPB, dans la ligne des « dossiers » numérotés.
    return f"""<rect width="1080" height="1080" fill="{ENCRE}"/>
<g transform="rotate(-5 540 560)">
 <path d="M170 300 h250 l40 -60 h230 l30 60 h190 v520 h-740 z" fill="{KRAFT}"/>
 <rect x="170" y="300" width="740" height="10" fill="#C9A563"/>
</g>
<g transform="rotate(-13 540 560)" filter="url(#tampon)">
 <rect x="215" y="385" width="650" height="330" rx="26" fill="none" stroke="{ROUGE}" stroke-width="26"/>
 <rect x="250" y="420" width="580" height="260" rx="14" fill="none" stroke="{ROUGE}" stroke-width="9"/>
 <text x="540" y="652" text-anchor="middle" font-family="Bebas" font-size="300" letter-spacing="14"
  fill="{ROUGE}">HPB</text>
</g>"""

PISTES = [
    dict(cle='a-bulle', nom='A - Bulle XXL', symbole=symbole_a, fond=ENCRE, texte=PAPIER, accent=JAUNE,
         idee="Évolution de l'actuel : même bulle jaune, HPB deux fois plus gros, lisible en 40 px.",
         police='Poppins', poids=800),
    dict(cle='b-carton', nom='B - Carton', symbole=symbole_b, fond=ENCRE, texte=PAPIER, accent=JAUNE,
         idee="Le carton d'arbitre : sport et sanction en un signe, compris sans lire.",
         police='Epaules', poids=900),
    dict(cle='c-tabloid', nom='C - Tabloïd', symbole=symbole_c, fond=ROUGE, texte='#FFFFFF', accent=JAUNE,
         idee='Une de journal à scandale : rouge plein, ton gossip et provoc assumé.',
         police='Epaules', poids=900),
    dict(cle='d-dossier', nom='D - Dossier', symbole=symbole_d, fond=ENCRE, texte=PAPIER, accent=ROUGE,
         idee='Chemise kraft et tampon : chaque vidéo est un dossier numéroté.',
         police='Bebas', poids=400),
]

BASELINE = 'Scandales, triches et histoires vraies du sport'
RYTHME = 'UNE VIDÉO PAR JOUR · 19 H'


def page(svg, w, h):
    return f'<!doctype html><meta charset="utf-8">{CSS}<body><svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{GRAIN}</defs>{svg}</svg>'


def banniere(p):
    """Bannière YouTube 2560x1440. Zone sûre tous écrans : 1546x423 centrée (y 508 à 931)."""
    s = p['symbole']()
    titre_attr = f'font-family="{p["police"]}" font-weight="{p["poids"]}"'
    return f"""<rect width="2560" height="1440" fill="{p['fond']}"/>
<g transform="translate(507 505) scale(.4)"><svg width="1080" height="1080" viewBox="90 90 900 900">{s}</svg></g>
<text x="1000" y="700" {titre_attr} font-size="150" textLength="1050" lengthAdjust="spacingAndGlyphs" fill="{p['texte']}">HISTOIRES PAS BANALES</text>
<text x="1004" y="790" font-family="Montserrat" font-weight="600" font-size="52" textLength="1046" lengthAdjust="spacingAndGlyphs" fill="{p['texte']}" opacity=".85">{BASELINE}</text>
<rect x="1004" y="830" width="720" height="74" fill="{p['accent']}"/>
<text x="1364" y="884" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="42" textLength="660" lengthAdjust="spacingAndGlyphs"
 fill="{ENCRE if p['accent'] == JAUNE else '#FFFFFF'}">{RYTHME}</text>"""


def rendre(html, png, w, h):
    src = SORTIE / (png.stem + '.html')
    src.write_text(html, encoding='utf-8')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=1', f'--window-size={w},{h}', '--virtual-time-budget=3000',
                    f'--screenshot={png}', src.as_uri()], check=True, capture_output=True)


def planche():
    cols = ''
    for p in PISTES:
        a = (SORTIE / f"{p['cle']}-avatar.png").as_uri()
        b = (SORTIE / f"{p['cle']}-banniere.png").as_uri()
        cols += f"""<div class="col"><h2>{p['nom']}</h2><p>{p['idee']}</p>
<img class="av" src="{a}">
<div class="row dark"><img src="{a}" style="width:96px"><img src="{a}" style="width:56px"><img src="{a}" style="width:32px"><span>@histoirespasbanales</span></div>
<div class="row light"><img src="{a}" style="width:96px"><img src="{a}" style="width:56px"><img src="{a}" style="width:32px"><span>@histoirespasbanales</span></div>
<img class="ban" src="{b}"></div>"""
    html = f"""<!doctype html><meta charset="utf-8">{CSS}<style>
body{{background:#1B1E26;font-family:Montserrat;color:#F7F3E9;width:2400px}}
h1{{font-family:Epaules;font-weight:900;font-size:76px;margin:40px 50px 10px;letter-spacing:1px}}
.sub{{margin:0 50px 30px;font-size:24px;opacity:.7}}
.grid{{display:flex;gap:30px;padding:0 50px 50px}}
.col{{flex:1;background:#252934;border-radius:22px;padding:26px}}
h2{{font-family:Epaules;font-weight:900;font-size:52px;margin:0 0 6px}}
p{{font-size:20px;line-height:1.35;min-height:56px;margin:0 0 18px;opacity:.85}}
.av{{width:100%;border-radius:50%;display:block}}
.row{{display:flex;align-items:center;gap:16px;margin-top:14px;padding:12px 16px;border-radius:14px}}
.row img{{border-radius:50%}}.row span{{font-size:18px;font-weight:700}}
.dark{{background:#000}}.light{{background:#fff;color:#161823}}
.ban{{width:100%;margin-top:16px;border-radius:10px;display:block}}
</style><body><h1>HPB - REFONTE : 4 PISTES</h1>
<div class="sub">Avatar recadré en rond comme sur TikTok et YouTube, en grand puis aux tailles réelles (fil, commentaires, notifications). Dessous : bannière YouTube 2560 x 1440.</div>
<div class="grid">{cols}</div>"""
    rendre(html, ICI / 'planche-pistes.png', 2400, 1480)


if __name__ == '__main__':
    for p in PISTES:
        rendre(page(p['symbole'](), 1080, 1080), SORTIE / f"{p['cle']}-avatar.png", 1080, 1080)
        rendre(page(banniere(p), 2560, 1440), SORTIE / f"{p['cle']}-banniere.png", 2560, 1440)
        print(p['nom'], 'ok', flush=True)
    planche()
    print('planche ok')
