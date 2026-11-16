"""Montage du dossier 53 façon BoltMotivation : plans courts, cadre lumineux sur fond flou, noir et blanc
pour Berlin, sous-titres centrés de 2 à 3 mots avec un mot coloré, vrais sons intercalés, fin sur le son d'origine.
Lancer depuis le dossier de la vidéo : python montage.py [plans|titres|final]"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from calage import VOIX, REELS
from plans import PLANS, FIN, ECLAIRS, FINAL, ARCHIVE_BERLIN

W, H, FPS = 1080, 1920, 30
POLICE = '../../../assets/fonts/Montserrat-Variable.ttf'
JAUNE, ROUGE, CYAN, VERT, VIOLET, ORANGE = (255, 221, 0), (255, 60, 60), (40, 220, 255), (70, 255, 120), (200, 110, 255), (255, 150, 30)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit(1)


def filets(hauteur):
    """Deux filets blancs lumineux qui bordent la fenêtre."""
    p = Path(f'_montage/filets-{hauteur}.png')
    if not p.exists():
        y0 = (H - hauteur) // 2
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for y in (y0, y0 + hauteur):
            trait = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(trait).rectangle((0, y - 3, W, y + 3), fill=(255, 255, 255, 255))
            im.alpha_composite(trait.filter(ImageFilter.GaussianBlur(14)))
            im.alpha_composite(trait.filter(ImageFilter.GaussianBlur(5)))
            ImageDraw.Draw(im).rectangle((0, y - 2, W, y + 2), fill=(255, 255, 255, 255))
        im.save(p)
    return p


def plans():
    Path('_montage').mkdir(exist_ok=True)
    liste = []
    for i, (t0, src, s0, style, nb, (x, y, w, h), *reste) in enumerate(PLANS):
        ralenti = f'setpts=PTS/{reste[0]},' if reste else ''
        d = (PLANS[i + 1][0] if i + 1 < len(PLANS) else FIN) - t0
        n = round(d * FPS)
        out = f'_montage/p{i:02d}.mp4'
        liste.append(out)
        base = f'[0:v]crop={w}:{h}:{x}:{y},{ralenti}fps={FPS}' + (',hue=s=0,eq=contrast=1.15:brightness=-0.03' if nb else '')
        if src == ARCHIVE_BERLIN:
            base += ',eq=gamma=1.17:saturation=0.91'
        z0, z1 = (1.0, 1.07) if i % 2 == 0 else (1.07, 1.0)
        zoom = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps={FPS}"
        if style == 'plein':
            fc = f'{base},scale={W * 2}:{H * 2}:flags=lanczos,{zoom}:s={W}x{H},setsar=1,format=yuv420p[v]'
            entrees = []
        else:
            hf = int(round(W * h / w / 2) * 2)
            x_avant = -64 if i == len(PLANS) - 1 else 0
            fc = (f'{base},split[a][b];[b]scale=-2:{int(H * 1.12)},crop={W}:{H},gblur=sigma=30,eq=brightness=-0.24:saturation=0.9[bg];'
                  f'[a]scale={W * 2}:{hf * 2}:flags=lanczos,{zoom}:s={W}x{hf},setsar=1[fg];'
                  f'[bg][fg]overlay={x_avant}:{(H - hf) // 2}[c];[c][1:v]overlay=0:0,format=yuv420p[v]')
            entrees = ['-i', str(filets(hf))]
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s0:.3f}', '-i', f'sources/{src}.mp4', *entrees, '-filter_complex', fc,
             '-map', '[v]', '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-r', str(FPS), out])
        print(f'plan {i:02d} {d:.2f}s {style}')
    Path('_montage/plans.txt').write_text(''.join(f"file '{Path(p).name}'\n" for p in liste), encoding='utf-8')


# ---------- sous-titres ----------
def V(parle, affiche, coul=None):
    return (parle, affiche, coul)


def R(a, b, affiche, coul=None):
    return ((a, b), affiche, coul)


# le mot entre crochets est coloré ; « | » force un retour à la ligne
TITRES_VOIX = [[
    V('Aux championnats', 'AUX CHAMPIONNATS'), V("d'Europe,", "[D'EUROPE] 2018", CYAN), V('Kévin Maillère,', '[KEVIN MAYER]', CYAN),
    V('champion du monde', 'CHAMPION [DU MONDE]', JAUNE), V('de décathlon,', 'DE DÉCATHLON'), V('hurle de joie', 'HURLE DE [JOIE]', JAUNE),
    V('après son saut,', 'APRÈS SON SAUT'), V('mais le juge', 'MAIS LE JUGE'), V('lève un drapeau rouge :', 'LÈVE UN|DRAPEAU [ROUGE]', ROUGE),
    V('saut annulé,', '[SAUT ANNULÉ]', ROUGE), V('zéro point.', '[ZÉRO POINT]', ROUGE),
], [
    V('Mais quarante jours', 'MAIS [40 JOURS]', CYAN), V('plus tard,', 'PLUS TARD'), V('à Talence,', 'À [TALENCE]', JAUNE),
    V('il ne lui reste', 'IL NE LUI RESTE'), V("qu'une course", "QU'[UNE COURSE]", ORANGE), V('pour battre', 'POUR BATTRE'),
    V('le record du monde.', 'LE [RECORD DU MONDE]', VERT),
], [
    V('Il doit courir', 'IL DOIT COURIR'), V('en moins de', 'EN MOINS DE'), V('quatre minutes quarante-neuf.', '[4 MIN 49]', CYAN),
]]
# sous-titres des vrais sons, dans l'ordre de passage (calage.SEQUENCE) : instants dans la source
TITRES_REELS = [
    # Mayer à Berlin, interview télé du 7 août 2018
    [R(11.70, 12.92, '« JE SUIS TELLEMENT'), R(12.92, 13.84, '[DÉÇU] POUR MOI-MÊME', ROUGE), R(13.84, 14.66, 'TELLEMENT, TELLEMENT'),
     R(14.66, 15.58, '[DÉÇU] POUR TOUS CEUX', ROUGE), R(15.58, 16.32, 'QUI ATTENDAIENT|QUELQUE CHOSE'),
     R(16.32, 16.94, "DE MOI [AUJOURD'HUI] »", JAUNE)],
    # Mayer sur Europe 1, 8 août 2018
    [R(158.18, 159.10, '« J’ÉTAIS PRÉTENDANT'), R(159.10, 160.46, "AU TITRE DE|[CHAMPION D'EUROPE]", JAUNE),
     R(160.46, 161.26, 'ET JE SUIS DEVENU'), R(161.26, 161.90, '[RIEN DU TOUT] »', ROUGE)],
    # Mayer dans son film, novembre 2018
    [R(1712.03, 1713.22, '« DANS LES VESTIAIRES'), R(1713.22, 1714.56, 'TOUT LE MONDE|ÉTAIT LÀ'),
     R(1714.56, 1715.58, 'UN ÉNORME [SILENCE]', VIOLET), R(1715.58, 1716.95, 'ET LÀ, JE FONDS|[EN LARMES] »', CYAN)],
    # commentaire RMC Sport du 1 500 m
    [R(149.96, 150.41, '« ON EST'), R(150.41, 151.74, 'AUX ALENTOURS|DES [4’40] !', CYAN),
     R(151.74, 153.03, 'IL VA LE [RÉALISER] !', JAUNE), R(153.03, 154.43, 'IL VA LE [RÉALISER] !', JAUNE),
     R(154.50, 155.94, '[4’40] !', CYAN), R(155.94, 157.38, '[4’36]', JAUNE), R(157.38, 159.04, 'POUR [KEVIN MAYER] !', CYAN),
     R(159.04, 160.98, "C'EST [INCROYABLE] !", ORANGE), R(160.98, 162.00, '[4’36] !', JAUNE),
     R(162.00, 164.36, 'AU-DELÀ DES|[9 100 POINTS] !', VERT), R(164.36, 165.90, 'LE RECORD|[DU MONDE] !', VERT),
     R(165.90, 168.30, "C'EST [SENSATIONNEL] ! »", JAUNE)],
]


def minutage():
    """Associe chaque groupe de mots à son instant dans la sortie."""
    t = json.loads(Path('timings.json').read_text(encoding='utf-8'))
    texte = ''.join(t['characters'])
    deb, fin = t['character_start_times_seconds'], t['character_end_times_seconds']
    groupes, curseur = [], 0
    for bloc, (t_sortie, t_voix, _) in zip(TITRES_VOIX, VOIX):
        curseur = max(curseur, next(i for i, s in enumerate(deb) if s >= t_voix - 0.05))
        for parle, affiche, coul in bloc:
            i = texte.index(parle, curseur)
            j = i + len(parle) - 1
            curseur = j + 1
            groupes.append([deb[i] - t_voix + t_sortie, fin[j] - t_voix + t_sortie, affiche, coul])
    assert len(TITRES_REELS) == len(REELS)
    for bloc, (t_sortie, _, s0, _, _) in zip(TITRES_REELS, REELS):
        for (a, b), affiche, coul in bloc:
            groupes.append([a - s0 + t_sortie, b - s0 + t_sortie, affiche, coul])
    groupes.sort(key=lambda g: g[0])
    for g, suivant in zip(groupes, groupes[1:] + [[FIN]]):
        g[1] = suivant[0] if suivant[0] - g[1] < 0.25 else g[1] + 0.12   # tient jusqu'au groupe suivant, sans déborder sur le plan d'après
    groupes[-1][1] = min(groupes[-1][1], FIN - 0.38)                            # le panneau du record reste lisible à la fin
    return groupes


def police(taille):
    f = ImageFont.truetype(POLICE, taille)
    f.set_variation_by_name('Black')
    return f


def image_titre(affiche, coul, chemin, centre=960):
    mesure = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    lignes = affiche.split('|')
    taille = 66
    f = police(taille)
    while max(mesure.textlength(ligne.replace('[', '').replace(']', ''), font=f) for ligne in lignes) > 740:
        taille -= 2
        f = police(taille)
    haut = centre - (len(lignes) * 80) // 2
    ombre, lueur, net = (Image.new('RGBA', (W, H), (0, 0, 0, 0)) for _ in range(3))
    for n, ligne in enumerate(lignes):
        morceaux, reste = [], ligne
        while reste:                                    # découpe « AVANT [COLORÉ] APRÈS »
            if '[' in reste:
                avant, r = reste.split('[', 1)
                colore, reste = r.split(']', 1)
                morceaux += [(avant, None), (colore, coul)]
            else:
                morceaux.append((reste, None))
                reste = ''
        morceaux = [(m, c) for m, c in morceaux if m]
        x = (W - sum(mesure.textlength(m, font=f) for m, _ in morceaux)) / 2
        y = haut + n * 80
        for m, c in morceaux:
            ImageDraw.Draw(ombre).text((x, y), m, font=f, fill=(0, 0, 0, 255), stroke_width=9, stroke_fill=(0, 0, 0, 255))
            if c:
                ImageDraw.Draw(lueur).text((x, y), m, font=f, fill=c + (255,))
            ImageDraw.Draw(net).text((x, y), m, font=f, fill=(c or (255, 255, 255)) + (255,))
            x += mesure.textlength(m, font=f)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    im.alpha_composite(ombre.filter(ImageFilter.GaussianBlur(9)))
    im.alpha_composite(lueur.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(lueur.filter(ImageFilter.GaussianBlur(7)))
    im.alpha_composite(net)
    im.save(chemin)


def titres():
    Path('_montage/titres').mkdir(parents=True, exist_ok=True)
    Image.new('RGBA', (W, H), (0, 0, 0, 0)).save('_montage/titres/vide.png')
    groupes = minutage()
    lignes, t = [], 0.0

    def ajoute(nom, duree):
        if duree > 0.001:
            lignes.append(f"file 'titres/{nom}'\nduration {duree:.3f}\n")

    for n, (a, b, affiche, coul) in enumerate(groupes):
        a = max(a, t)
        ajoute('vide.png', a - t)
        centre = 1100 if a < 5.24 or FINAL + 1.95 <= a < FINAL + 6.0 else 960
        image_titre(affiche, coul, f'_montage/titres/t{n:03d}.png', centre=centre)
        ajoute(f't{n:03d}.png', b - a)
        t = b
    ajoute('vide.png', FIN + 0.5 - t)
    lignes.append("file 'titres/vide.png'\n")
    Path('_montage/titres.txt').write_text(''.join(lignes), encoding='utf-8')
    Path('sous-titres.json').write_text(
        json.dumps([[round(a, 2), round(b, 2), s.replace('|', ' ')] for a, b, s, _ in groupes], ensure_ascii=False, indent=0),
        encoding='utf-8')
    print(len(groupes), 'groupes de sous-titres')


def final():
    images = sum(round(((PLANS[i + 1][0] if i + 1 < len(PLANS) else FIN) - p[0]) * FPS) for i, p in enumerate(PLANS))
    logo = Image.open('maquette/logo.png').convert('RGBA')
    lw = 120
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    calque = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    calque.alpha_composite(logo, ((W - lw) // 2, 1310))
    calque.save('_montage/logo.png')
    eclairs = '+'.join(
        f'if(between(t,{t},{t}+0.14),{intensite}*(1-(t-{t})/0.14),0)'
        for t, intensite in zip(ECLAIRS, (0.37, 0.19), strict=True)
    )
    fc = [f"[0:v][1:v]overlay=0:0:format=auto[a];[a][2:v]overlay=0:0,eq=eval=frame:brightness='{eclairs}',"
          "format=yuv420p[v]"]
    entrees = ['-f', 'concat', '-safe', '0', '-i', '_montage/plans.txt', '-f', 'concat', '-safe', '0', '-i', '_montage/titres.txt',
               '-loop', '1', '-i', '_montage/logo.png']
    entrees += ['-i', '../final.mp4']
    run(['ffmpeg', '-v', 'error', '-y', *entrees, '-filter_complex', fc[0], '-map', '[v]', '-map', '3:a', '-t', f'{images / FPS:.3f}',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-r', str(FPS), '-pix_fmt', 'yuv420p', '-c:a', 'copy',
         '-movflags', '+faststart', 'final.mp4'])
    print('final.mp4 écrit')


if __name__ == '__main__':
    for etape in (sys.argv[1:] or ['plans', 'titres', 'final']):
        {'plans': plans, 'titres': titres, 'final': final}[etape]()
