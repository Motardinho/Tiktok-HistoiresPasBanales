"""Montage du dossier 53 façon BoltMotivation : plans courts, cadre lumineux sur fond flou, noir et blanc
pour Berlin, sous-titres centrés de 2 à 3 mots avec un mot coloré, vrais sons intercalés, fin sur le son d'origine.
Lancer depuis le dossier de la vidéo : python montage.py [plans|titres|final]"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from calage import VOIX, REELS, REELS_T
from plans import PLANS, FIN, ECLAIRS, ENTREE, FINAL, DOUX

W, H, FPS = 1080, 1920, 30
POLICE = '../../assets/fonts/Montserrat-Variable.ttf'
JAUNE, ROUGE, CYAN, VERT, VIOLET, ORANGE = (255, 221, 0), (255, 60, 60), (40, 220, 255), (70, 255, 120), (200, 110, 255), (255, 150, 30)
# Musique Mixkit « A New Life » (Eugenio Mininni) : introduction très douce, l'orchestre entre à 24,5 s de la piste.
ELAN, ELAN_ENTREE, ELAN_AVANT = 'musique/543.mp3', 24.5, 7.5


# « Daylight (Instrumental) », David Kushner : la musique du Short de Bolt de référence, retrouvée par reconnaissance
# audio. Bolt démarre à 141,15 s du morceau et fait éclater le refrain final (164,25 s) sur la victoire. Ici, le refrain
# éclate quand Mayer franchit la ligne, 5,6 s après le début du vrai son final ; le morceau n'est ni coupé ni bouclé.
DAYLIGHT, DAYLIGHT_REFRAIN = 'sources/daylight-instrumental.mp4', 164.25
ARRIVEE = REELS_T['r2'] + 5.6


def courbe(points, u):
    """Gain linéaire par morceaux : points = [(instant de sortie, gain), ...]."""
    e = f'{points[-1][1]}'
    for (t0, g0), (t1, g1) in reversed(list(zip(points, points[1:]))):
        e = f'if(lt({u},{t1:.3f}),{g0}+({g1}-{g0})*({u}-{t0:.3f})/({t1:.3f}-{t0:.3f}),{e})'
    return e


def bandes_son():
    """Trois bandes à comparer. Chez Bolt, la musique est continue et forte, 4 à 5 dB sous la voix : chaque bande
    garde donc un lit audible dès la première seconde, monte au revirement et grandit jusqu'à la fin.
    Chaque morceau : (fichier, début dans la piste, début dans la sortie, durée, lit, entrée, sommet, fondu d'entrée)."""
    e, f = ENTREE, FINAL
    a = ARRIVEE
    return {
        # D, bande validée par Marc le 16 novembre 2026 : « Daylight (Instrumental) ». Le morceau est fort à la fin de son premier refrain (joie), s'éteint tout seul
        # sur le drapeau rouge, reste dépouillé pendant la chute et les larmes, monte sur la dernière ligne droite et
        # éclate sur la ligne d'arrivée. La courbe ramène le tout vers un niveau régulier, comme le mixage de Bolt.
        'D': [(DAYLIGHT, DAYLIGHT_REFRAIN - a, 0.0, FIN,
               [(0.0, 0.50), (7.2, 0.50), (7.8, 0.45), (9.6, 0.45), (10.8, 0.8), (13.5, 1.2), (a - 5.6, 1.2), (a - 4.9, 0.75),
                (a - 0.3, 0.75), (a - 0.05, 0.42), (FIN, 0.42)])],
        # A : « I Won't Surrender » en lit, puis l'orchestre de « A New Life » au revirement
        'A': [('musique/846.mp3', 22.0, 0.0, e + 0.5, 0.56, 0.56, 0.56, 0.5),
              ('musique/543.mp3', ELAN_ENTREE - 4.0, e - 4.0, FIN - e + 4.0, 1.6, 1.0, 1.2, 2.0)],
        # B : « Silent Descent » seule, sa grande montée (69,5 s de la piste) calée sur le revirement
        'B': [('musique/614.mp3', 69.5 - e, 0.0, FIN, 0.7, 0.5, 0.58, 0.5)],
        # C : « Drawing the Sky » seule, orchestre dense et régulier, son sommet (76 s) calé sur l'arrivée
        'C': [('musique/606.mp3', 76.0 - f, 0.0, FIN, 0.5, 0.7, 0.78, 0.5)],
    }

# Voix Jayce (choisie par Marc sur essais, plus grave que Hugo). Les blocs de voix, le début des vrais sons et la fin
# viennent de calage.py, donc de timings.json : après un changement de voix ou de texte, relancer voix.py puis ce script.
GAIN_VOIX = 2.8   # voix.mp3 à -25,8 LUFS, amenée à -16,8 LUFS
# Les vrais sons (source, début, durée, gain) et leur ordre sont décrits dans calage.py.


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
        z0, z1 = (1.0, 1.07) if i % 2 == 0 else (1.07, 1.0)
        zoom = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps={FPS}"
        if style == 'plein':
            fc = f'{base},scale={W * 2}:{H * 2}:flags=lanczos,{zoom}:s={W}x{H},setsar=1,format=yuv420p[v]'
            entrees = []
        else:
            hf = int(round(W * h / w / 2) * 2)
            fc = (f'{base},split[a][b];[b]scale=-2:{int(H * 1.12)},crop={W}:{H},gblur=sigma=30,eq=brightness=-0.24:saturation=0.9[bg];'
                  f'[a]scale={W * 2}:{hf * 2}:flags=lanczos,{zoom}:s={W}x{hf},setsar=1[fg];'
                  f'[bg][fg]overlay=0:{(H - hf) // 2}[c];[c][1:v]overlay=0:0,format=yuv420p[v]')
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
    [R(149.96, 151.78, 'AUX ALENTOURS|DES [4’40] !', CYAN), R(151.78, 154.50, 'IL VA LE [RÉALISER] !', JAUNE),
     R(154.50, 155.94, '[4’40] !', CYAN), R(155.94, 157.38, '[4’36]', JAUNE), R(157.38, 159.04, 'POUR [KEVIN MAYER] !', CYAN),
     R(159.04, 160.98, "C'EST [INCROYABLE] !", ORANGE), R(160.98, 162.00, '[4’36] !', JAUNE),
     R(162.00, 164.36, 'AU-DELÀ DES|[9 100 POINTS] !', VERT), R(164.36, 165.90, 'LE RECORD|[DU MONDE] !', VERT),
     R(165.90, 168.30, "C'EST [SENSATIONNEL] !", JAUNE)],
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
    groupes[-1][1] = min(groupes[-1][1], FIN - 1.3)                            # le panneau du record reste lisible à la fin
    return groupes


def police(taille):
    f = ImageFont.truetype(POLICE, taille)
    f.set_variation_by_name('Black')
    return f


def image_titre(affiche, coul, chemin):
    f = police(66)
    mesure = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    lignes = affiche.split('|')
    haut = 960 - (len(lignes) * 80) // 2
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
        image_titre(affiche, coul, f'_montage/titres/t{n:03d}.png')
        ajoute(f't{n:03d}.png', b - a)
        t = b
    ajoute('vide.png', FIN + 0.5 - t)
    lignes.append("file 'titres/vide.png'\n")
    Path('_montage/titres.txt').write_text(''.join(lignes), encoding='utf-8')
    Path('sous-titres.json').write_text(
        json.dumps([[round(a, 2), round(b, 2), s.replace('|', ' ')] for a, b, s, _ in groupes], ensure_ascii=False, indent=0),
        encoding='utf-8')
    print(len(groupes), 'groupes de sous-titres')


def final(bande='D', sortie='final.mp4'):
    images = sum(round(((PLANS[i + 1][0] if i + 1 < len(PLANS) else FIN) - p[0]) * FPS) for i, p in enumerate(PLANS))
    logo = Image.open('maquette/logo.png').convert('RGBA')
    lw = 120
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    calque = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    calque.alpha_composite(logo, ((W - lw) // 2, 1430))
    calque.save('_montage/logo.png')
    eclairs = '+'.join(f'if(between(t,{t},{t}+0.14),0.28*(1-(t-{t})/0.14),0)' for t in ECLAIRS + ([ARRIVEE] if bande == 'D' else []))
    fc = [f"[0:v][1:v]overlay=0:0:format=auto[a];[a][2:v]overlay=0:0,eq=eval=frame:brightness='{eclairs}',"
          f"fade=t=out:st={FIN - 0.35}:d=0.35,format=yuv420p[v]"]
    entrees = ['-f', 'concat', '-safe', '0', '-i', '_montage/plans.txt', '-f', 'concat', '-safe', '0', '-i', '_montage/titres.txt',
               '-loop', '1', '-i', '_montage/logo.png']
    pistes, k = [], 3
    for t_sortie, t_voix, d in VOIX:
        entrees += ['-ss', f'{t_voix}', '-t', f'{d}', '-i', 'voix.mp3']
        fc.append(f'[{k}:a]afade=t=in:d=0.02,afade=t=out:st={d - 0.04}:d=0.04,volume={GAIN_VOIX},adelay={int(t_sortie * 1000)}:all=1[s{k}]')
        pistes.append(f'[s{k}]')
        k += 1
    for t_sortie, src, s0, d, gain in REELS:
        entrees += ['-ss', f'{s0}', '-t', f'{d}', '-i', f'sources/{src}.mp4']
        fc.append(f'[{k}:a]aformat=channel_layouts=stereo,afade=t=in:d=0.15,afade=t=out:st={d - 0.35}:d=0.35,volume={gain},'
                  f'adelay={int(t_sortie * 1000)}:all=1[s{k}]')
        pistes.append(f'[s{k}]')
        k += 1
    if bande:
        for n, morceau in enumerate(bandes_son()[bande]):
            if len(morceau) == 5:                           # morceau piloté par une courbe de gain
                fichier, ss, t0, duree, points = morceau
                entrees += ['-ss', f'{ss:.3f}', '-t', f'{duree:.3f}', '-i', fichier]
                fc.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d=0.4,afade=t=out:st={duree - 1.2:.3f}:d=1.2,"
                          f"volume='({courbe(points, 't')})*(1-0.25*between(t,{DOUX[0]:.3f},{DOUX[1]:.3f}))':eval=frame[m{n}]")
                pistes.append(f'[m{n}]')
                k += 1
                continue
            fichier, ss, t0, duree, lit, entree, sommet, fondu = morceau
            entrees += ['-ss', f'{ss:.3f}', '-t', f'{duree:.3f}', '-i', fichier]
            u = f'(t+{t0:.3f})'                             # instant dans la sortie
            fin_piste = duree - (0.9 if t0 + duree < FIN - 0.1 else 1.0)
            fc.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d={fondu},afade=t=out:st={fin_piste:.3f}:d=0.9,"
                      f"volume='if(lt({u},{ENTREE:.3f}),{lit},if(lt({u},{FINAL - 0.3:.3f}),"
                      f"{entree}+({sommet}-{entree})*({u}-{ENTREE:.3f})/({FINAL - 0.3:.3f}-{ENTREE:.3f}),{sommet}))"
                      f"*(1-0.55*between({u},{DOUX[0]:.3f},{DOUX[1]:.3f}))':eval=frame,adelay={int(t0 * 1000)}:all=1[m{n}]")
            pistes.append(f'[m{n}]')
            k += 1
    else:
        # musique : introduction douce et montée sous le début, entrée de l'orchestre sur ENTREE, puis de plus en plus fort jusqu'à la fin
        decalage = ELAN_ENTREE - ENTREE                    # la piste est décalée pour que l'orchestre entre sur ENTREE
        assert decalage >= 0, "le retournement arrive trop tard pour cette musique"
        entrees += ['-ss', f'{decalage:.3f}', '-t', f'{FIN:.3f}', '-i', ELAN]
        fc.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d=0.6,afade=t=out:st={FIN - 1.0:.3f}:d=1.0,"
                  f"volume='if(lt(t,{ENTREE - ELAN_AVANT:.3f}),3.0,if(lt(t,{ENTREE:.3f}),1.2,"
                  f"if(lt(t,{FINAL - 0.3:.3f}),0.6+0.25*(t-{ENTREE:.3f})/({FINAL - 0.3:.3f}-{ENTREE:.3f}),0.88)))"
                  f"*(1-0.6*between(t,{DOUX[0]:.3f},{DOUX[1]:.3f}))':eval=frame[m2]")
        pistes.append('[m2]')
    fc.append(''.join(pistes) + f'amix=inputs={len(pistes)}:normalize=0:duration=longest,alimiter=limit=0.95,aresample=48000[au]')
    run(['ffmpeg', '-v', 'error', '-y', *entrees, '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[au]', '-t', f'{images / FPS:.3f}',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-r', str(FPS), '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
         '-movflags', '+faststart', sortie])
    print(sortie, 'écrit')


if __name__ == '__main__':
    for etape in (sys.argv[1:] or ['plans', 'titres', 'final']):
        if etape in ('A', 'B', 'C', 'D'):
            final(etape, f'essai-musique-{etape}.mp4')
        else:
            {'plans': plans, 'titres': titres, 'final': final}[etape]()
