"""V2 de la vidéo 20 (téléphones) : faux numéro 1 « Nokia 3310 » annoncé par une voix angélique,
tête de troll en effet « deep fried », loupé (disque rayé + tampon), rembobinage VHS, puis vrai numéro 1.

Entrées : out/20-telephone-2899-dollars/version-validee/final.mp4 (V1 validée, intacte)
          assets/refonte-14-20/telephone/troll/ (dessins, voix, bruitages)
Sortie   : out/20-telephone-2899-dollars/v2-troll/ (final.mp4, comparaison.mp4, histoire.json, CREDITS.md)
"""
import json, math, shutil, subprocess, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from comparer_lot_16_18 import compare  # noqa: E402

DOSSIER = ROOT/'out/20-telephone-2899-dollars'
V1 = DOSSIER/'version-validee/final.mp4'
W = DOSSIER/'v2-troll'
M = W/'_montage'
A = ROOT/'assets/refonte-14-20/telephone/troll'
FPS, WID, HEI, SR = 30, 1080, 1920, 44100
COUPE = 1129                      # image 1129 = 37,633 s, juste avant « Numéro un. » (37,64 s)

# Chronologie du gag (secondes, relatives au début du gag)
T_DESC = (0.15, 2.5)               # le Nokia descend du ciel (début, atterrissage)
T_TROLL = 3.6                      # coupure brutale : boom + troll
T_CRU = 4.6                        # « T'as cru ? »
T_LOUPE = 5.8                      # disque rayé, arrêt sur image
T_TAMPON = 5.9
T_REW = 6.5                        # rembobinage
DUREE = 7.1


def run(cmd, cwd=None, **kw):
    return subprocess.run(cmd, cwd=cwd, check=True, **kw)


def charger(f, vitesse=1.0, pitch=1.0):
    """Décode un fichier audio en stéréo float32 44,1 kHz, avec tempo et hauteur optionnels."""
    af = []
    if pitch != 1.0:
        af.append(f'asetrate={int(SR*pitch)},aresample={SR}')
    if vitesse != 1.0:
        af.append(f'atempo={vitesse}')
    cmd = ['ffmpeg', '-v', 'error', '-i', str(f)] + (['-af', ','.join(af)] if af else []) + \
          ['-f', 'f32le', '-ac', '2', '-ar', str(SR), '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def reverb(x, duree=2.2, mouille=0.35, graine=1):
    rng = np.random.default_rng(graine)
    n = int(duree*SR)
    t = np.arange(n)/SR
    ir = rng.standard_normal((n, 2))*np.exp(-t/(duree/6.9))[:, None]
    ir[:int(.012*SR)] = 0
    ir /= np.sqrt((ir**2).sum(0))
    L = len(x)+n
    N = 1 << (L-1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, N, axis=0)*np.fft.rfft(ir, N, axis=0), N, axis=0)[:L]
    out = np.zeros((L, 2), np.float32)
    out[:len(x)] += x*(1-mouille)
    out += y*mouille*3
    return out


def poser(piste, son, t, gain=1.0):
    i = int(t*SR)
    n = min(len(son), len(piste)-i)
    if n > 0:
        piste[i:i+n] += son[:n]*gain


def fondu(x, entree=0.0, sortie=0.0):
    x = x.copy()
    if entree:
        n = min(len(x), int(entree*SR)); x[:n] *= np.linspace(0, 1, n)[:, None]
    if sortie:
        n = min(len(x), int(sortie*SR)); x[-n:] *= np.linspace(1, 0, n)[:, None]
    return x


def db(x):
    return 10**(x/20)


# ---------------------------------------------------------------- audio
def audio():
    piste = np.zeros((int(DUREE*SR)+SR*3, 2), np.float32)
    # A : sans voix. Chœur + harpe qui descendent avec le téléphone, carillon à l'atterrissage
    choeur = charger(A/'sfx-descente-1.mp3', vitesse=0.8)
    choeur = fondu(reverb(choeur, 2.6, .3, 2)[:int(T_TROLL*SR)], 0.04, 0.02)
    poser(piste, choeur, 0, db(-4))
    poser(piste, reverb(charger(A/'sfx-carillon-1.mp3'), 1.8, .35, 5), 0.0, db(-12))
    poser(piste, reverb(charger(A/'sfx-carillon-2.mp3'), 2.2, .4, 6), T_DESC[1]-0.04, db(-2))
    piste[int(T_TROLL*SR):] = 0                 # coupure sèche : le paradis s'arrête net
    # B : boom, rire de troll, « T'as cru ? » grave et saturé
    poser(piste, charger(A/'sfx-boom-2.mp3'), T_TROLL, db(0))
    rire = fondu(charger(A/'sfx-rire-1.mp3', pitch=1.06)[:int(1.0*SR)], 0, .08)
    poser(piste, rire, T_TROLL+0.12, db(-5))
    troll = charger(A/'troll-callum.mp3', pitch=0.9)
    debut_cru = int(1.44/0.9*SR)                 # « T'as cru ? » après les « hé hé »
    cru = troll[debut_cru:]
    cru = np.tanh(cru*db(14))*db(-4)            # saturation « bass boosted »
    poser(piste, fondu(cru, .01, .05), T_CRU, db(0))
    piste[int(T_LOUPE*SR):] = 0
    # C : loupé
    poser(piste, charger(A/'sfx-scratch-1.mp3'), T_LOUPE, db(-3))
    poser(piste, charger(A/'sfx-tampon-2.mp3'), T_TAMPON, db(6))
    rew = fondu(charger(A/'sfx-rembobinage-2.mp3')[:int((DUREE-T_REW)*SR)], .03, .04)
    poser(piste, rew, T_REW, db(-4))
    piste = piste[:int(DUREE*SR)]
    piste = fondu(piste, 0.01, 0.015)
    crete = np.abs(piste).max()
    if crete > db(-1):
        piste *= db(-1)/crete
    brut = M/'gag-brut.wav'
    ecrire_wav(brut, piste)
    # Sonie alignée sur la V1 autour du raccord (-16,6 LUFS intégrés)
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(brut), '-af',
         'loudnorm=I=-16:TP=-1.5:LRA=11:linear=true', '-ar', str(SR), str(M/'gag.wav')])


def ecrire_wav(f, x):
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-',
         '-c:a', 'pcm_s16le', str(f)], input=np.clip(x, -1, 1).astype(np.float32).tobytes())


# ---------------------------------------------------------------- images
def ease_out(x):
    x = min(max(x, 0), 1)
    return 1-(1-x)**3


def ressort(x):
    """Rebond qui dépasse puis se stabilise (0 -> 1)."""
    x = min(max(x, 0), 1)
    return 1-math.exp(-6*x)*math.cos(10*x)


class Decor:
    def __init__(self):
        # Vraie photo : « Nokia 3310 Blue R7309170 (retouch).png », smial, Wikimedia Commons, Licence Art Libre
        self.nokia = Image.open(A/'photo/Nokia_3310_Blue_R7309170_retouch.png').convert('RGBA')
        h = 900
        self.nokia = self.nokia.resize((round(self.nokia.width*h/self.nokia.height), h), Image.LANCZOS)
        self.aura_ext = self._aura((255, 200, 80), 220, 60, 80)
        self.aura_int = self._aura((255, 252, 235), 180, 14, 22)
        rng = np.random.default_rng(5)
        self.plumes = [(rng.uniform(100, 980), rng.uniform(-400, 1900), rng.uniform(.5, 1.2),
                        rng.uniform(0, 6.28), rng.uniform(26, 44)) for _ in range(9)]
        self.troll = Image.open(A/'dessins/troll.png').convert('RGBA').resize((920, 920), Image.LANCZOS)
        rng = np.random.default_rng(7)
        self.etincelles = [(rng.uniform(80, 1000), rng.uniform(500, 1800), rng.uniform(.6, 1.6),
                            rng.uniform(0, 6.28), rng.uniform(10, 26)) for _ in range(46)]
        self.ciel = self._ciel()
        self.nuages = self._nuages()
        self.tampon = self._tampon()
        self.police = ImageFont.truetype(str(ROOT/'assets/fonts/Poppins-ExtraBold.ttf'), 64)

    def _aura(self, couleur, pad, dilate, flou):
        a = ImageOps.expand(self.nokia.split()[3], pad, fill=0)
        a = a.filter(ImageFilter.MaxFilter(dilate | 1)).filter(ImageFilter.GaussianBlur(flou))
        im = Image.new('RGBA', a.size, couleur+(0,))
        im.putalpha(a)
        return im

    def _ciel(self):
        y, x = np.mgrid[0:HEI, 0:WID].astype(np.float32)
        d = np.sqrt(((x-540)/1.0)**2+((y-1000)/1.25)**2)/1100
        d = np.clip(d, 0, 1)[..., None]
        centre = np.array([255, 251, 232], np.float32)
        bord = np.array([70, 135, 230], np.float32)
        return Image.fromarray((centre*(1-d)+bord*d).astype(np.uint8), 'RGB')

    def _nuages(self):
        a = Image.new('L', (WID+600, 520), 0)
        dr = ImageDraw.Draw(a)
        rng = np.random.default_rng(3)
        for _ in range(40):
            cx, cy, r = rng.uniform(0, WID+600), rng.uniform(180, 480), rng.uniform(70, 170)
            dr.ellipse((cx-r*1.4, cy-r, cx+r*1.4, cy+r), fill=235)
        im = Image.new('RGBA', a.size, (255, 255, 255, 0))
        im.putalpha(a.filter(ImageFilter.GaussianBlur(18)))
        return im

    def _tampon(self):
        police = ImageFont.truetype(str(ROOT/'assets/fonts/BebasNeue-Regular.ttf'), 300)
        im = Image.new('RGBA', (980, 420), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        rouge = (214, 24, 32, 255)
        dr.rounded_rectangle((10, 10, 970, 410), 40, outline=rouge, width=22)
        dr.rounded_rectangle((44, 44, 936, 376), 24, outline=rouge, width=9)
        dr.text((490, 222), 'LOUPÉ !', font=police, fill=rouge, anchor='mm')
        # grain de tampon encreur
        rng = np.random.default_rng(11)
        a = np.array(im.split()[3], np.float32)
        a *= (rng.random(a.shape) > 0.18)
        im.putalpha(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6)))
        return im.rotate(14, resample=Image.BICUBIC, expand=True)

    # -------------------------------------------- A : descente céleste (sans voix)
    def celeste(self, t):
        d0, d1 = T_DESC
        p = ease_out((t-d0)/(d1-d0))
        cx = 540+math.sin(t*1.9)*40*(1-p)
        cy = -560+(1060+560)*p+math.sin(max(0, t-d1)*2.4)*10
        ang = 6*math.sin(t*2.3)*(1-p)+1.2*math.sin(t*1.6)
        atterri = max(0.0, t-d1)
        im = self.ciel.copy()
        # rayons divins tournants centrés sur le téléphone, plus forts après l'atterrissage
        r = Image.new('L', (WID//2, HEI//2), 0)
        dr = ImageDraw.Draw(r)
        rx, ry = cx/2, max(cy, 200)/2
        force = int(70+80*ease_out(atterri/0.4))
        for k in range(18):
            a0 = t*0.25+k*2*math.pi/18
            a1 = a0+math.pi/18*0.6
            dr.polygon([(rx, ry), (rx+1700*math.cos(a0), ry+1700*math.sin(a0)),
                        (rx+1700*math.cos(a1), ry+1700*math.sin(a1))], fill=force)
        # colonne de lumière qui tombe du ciel
        col = Image.new('L', (WID//2, HEI//2), 0)
        dc = ImageDraw.Draw(col)
        larg = 70+30*math.sin(t*3)
        dc.polygon([(270-larg, 0), (270+larg, 0), (270+larg*2.6, HEI//2), (270-larg*2.6, HEI//2)],
                   fill=int(150*ease_out(t/0.35)))
        r = Image.fromarray(np.maximum(np.asarray(r), np.asarray(col.filter(ImageFilter.GaussianBlur(28)))))
        r = r.filter(ImageFilter.GaussianBlur(10)).resize((WID, HEI), Image.BILINEAR)
        im = Image.composite(Image.new('RGB', (WID, HEI), (255, 240, 170)), im, r).convert('RGBA')
        # nuages : ceux du haut s'écartent, ceux du bas dérivent
        dx = int(-t*40) % 600
        im.alpha_composite(self.nuages.crop((dx, 0, dx+WID, 520)), (0, HEI-430))
        # aura : halo doré externe + lueur blanche, qui pulse et éclate à l'atterrissage
        eclat = math.exp(-atterri*5) if atterri > 0 else 0.0
        pulse = 1.7+0.35*math.sin(t*5)+0.8*eclat
        for aura, gain, ech in ((self.aura_ext, pulse, 1+0.25*eclat), (self.aura_int, 1.4+0.4*eclat, 1)):
            au = aura if ech == 1 else aura.resize((int(aura.width*ech), int(aura.height*ech)), Image.BILINEAR)
            au = au.rotate(ang, resample=Image.BILINEAR, expand=True)
            if gain != 1:
                au.putalpha(au.split()[3].point(lambda v, g=gain: min(255, int(v*g))))
            im.alpha_composite(au, (int(cx-au.width/2), int(cy-au.height/2)))
        ph = self.nokia.rotate(ang, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(ph, (int(cx-ph.width/2), int(cy-ph.height/2)))
        # onde de lumière à l'atterrissage
        if 0 < atterri < 0.6:
            on = Image.new('RGBA', (WID, HEI), (0, 0, 0, 0))
            do = ImageDraw.Draw(on)
            rr = 120+900*ease_out(atterri/0.6)
            do.ellipse((cx-rr, cy-rr*0.75, cx+rr, cy+rr*0.75),
                       outline=(255, 214, 110, int(240*(1-atterri/0.6))), width=40)
            im.alpha_composite(on.filter(ImageFilter.GaussianBlur(16)))
        # étincelles : traîne pendant la descente, gerbe à l'atterrissage
        sp = Image.new('RGBA', (WID, HEI), (0, 0, 0, 0))
        ds = ImageDraw.Draw(sp)
        for n, (x0, y0, v, ph0, s) in enumerate(self.etincelles):
            if atterri > 0 and n % 2 == 0:
                dist = 80+700*ease_out(atterri/0.8)*v/1.6
                xx, yy = cx+math.cos(ph0)*dist, cy+math.sin(ph0)*dist*0.9
                a = max(0.0, 1-atterri/0.9)
            else:
                xx = cx+(x0-540)*0.55
                yy = cy-200-((t*260*v+y0) % 900)
                a = max(0.0, math.sin(t*6*v+ph0))
            if a < .05:
                continue
            s2 = s*a
            c = (255, 250, 215, int(255*a))
            ds.polygon([(xx, yy-s2*2), (xx+s2*.35, yy), (xx, yy+s2*2), (xx-s2*.35, yy)], fill=c)
            ds.polygon([(xx-s2*2, yy), (xx, yy-s2*.35), (xx+s2*2, yy), (xx, yy+s2*.35)], fill=c)
        im.alpha_composite(sp)
        im = im.convert('RGB')
        if t < 0.18:
            im = Image.blend(im, Image.new('RGB', im.size, 'white'), 1-t/0.18)
        if 0 < atterri < 0.12:
            im = Image.blend(im, Image.new('RGB', im.size, (255, 250, 230)), 0.5*(1-atterri/0.12))
        return im

    # -------------------------------------------- B : troll « deep fried »
    def troll_image(self, t):
        u = t-T_TROLL
        # fond hypnotique tournant, couleurs qui changent
        fond = Image.new('RGB', (WID//2, HEI//2))
        dr = ImageDraw.Draw(fond)
        cx, cy = 270, 480
        rot = u*3.2
        teinte = (u*2.2) % 1
        c1 = tuple(int(255*v) for v in hsv(teinte, 1, 1))
        c2 = tuple(int(255*v) for v in hsv((teinte+.5) % 1, 1, .9))
        dr.rectangle((0, 0, WID, HEI), fill=c2)
        for k in range(14):
            a0 = rot+k*2*math.pi/14
            a1 = a0+math.pi/14
            dr.polygon([(cx, cy), (cx+1500*math.cos(a0), cy+1500*math.sin(a0)),
                        (cx+1500*math.cos(a1), cy+1500*math.sin(a1))], fill=c1)
        im = fond.resize((WID, HEI), Image.NEAREST).convert('RGBA')
        # tête qui claque, palpite, tremble et tourne
        echelle = 1+1.8*(1-ressort(u/0.3))
        battements = [0.12, 0.27, 0.42, 0.57, 0.72, 0.87, T_CRU-T_TROLL, T_CRU-T_TROLL+.28]
        for b in battements:
            if 0 <= u-b < .18:
                echelle *= 1+0.12*(1-(u-b)/.18)
        if u > T_CRU-T_TROLL:
            echelle *= 1+0.35*ease_out((u-(T_CRU-T_TROLL))/0.25)      # zoom sur la bouche
        rng = np.random.default_rng(int(t*FPS))
        force = 34 if u < .5 or u > T_CRU-T_TROLL else 16
        dx, dy = rng.uniform(-force, force, 2)
        ang = math.sin(u*38)*7
        tr = self.troll.resize((int(920*echelle), int(920*echelle)), Image.BILINEAR).rotate(
            ang, resample=Image.BILINEAR, expand=True)
        decal_y = 110*(echelle-1) if u > T_CRU-T_TROLL else 0
        im.alpha_composite(tr, (int(540-tr.width/2+dx), int(960-tr.height/2+dy-decal_y)))
        # yeux rouges incandescents (repère : pupilles du dessin)
        lu = Image.new('RGBA', (WID, HEI), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lu)
        intens = 0.6+0.4*abs(math.sin(u*14))
        for px, py in ((405, 400), (705, 398)):
            ex = 540+dx+(px*0.92-460)*echelle*math.cos(math.radians(-ang))-(py*0.92-460)*echelle*math.sin(math.radians(-ang))
            ey = 960+dy-decal_y+(px*0.92-460)*echelle*math.sin(math.radians(-ang))+(py*0.92-460)*echelle*math.cos(math.radians(-ang))
            for rr, coul in ((70, (255, 20, 10, 110)), (38, (255, 40, 20, 220)), (16, (255, 235, 200, 255))):
                rr *= echelle*intens
                dl.ellipse((ex-rr, ey-rr, ex+rr, ey+rr), fill=coul)
            dl.line((ex-230*echelle, ey, ex+230*echelle, ey), fill=(255, 140, 90, 210), width=5)
        im.alpha_composite(lu.filter(ImageFilter.GaussianBlur(6)))
        im = im.convert('RGB')
        return frire(im, rng)

    # -------------------------------------------- C : loupé + rembobinage
    def loupe(self, gele, t):
        u = t-T_LOUPE
        im = ImageOps.grayscale(gele).convert('RGB')
        im = ImageEnhance.Contrast(im).enhance(1.2)
        z = 1+0.04*ease_out(u/0.5)
        im = im.resize((int(WID*z), int(HEI*z)), Image.BILINEAR)
        im = im.crop(((im.width-WID)//2, (im.height-HEI)//2, (im.width-WID)//2+WID, (im.height-HEI)//2+HEI))
        im = Image.blend(im, Image.new('RGB', im.size, (30, 30, 30)), .25).convert('RGBA')
        v = t-T_TAMPON
        if v >= 0:
            e = 2.4-1.4*ressort(v/0.25)
            tp = self.tampon.resize((int(self.tampon.width*e), int(self.tampon.height*e)), Image.BILINEAR)
            rng = np.random.default_rng(int(t*FPS))
            sec = 18*max(0, 1-v/0.3)
            dx, dy = rng.uniform(-sec, sec, 2)
            im.alpha_composite(tp, (int(540-tp.width/2+dx), int(980-tp.height/2+dy)))
        return im.convert('RGB')


def hsv(h, s, v):
    import colorsys
    return colorsys.hsv_to_rgb(h, s, v)


def frire(im, rng):
    """Effet « deep fried » des mèmes : saturation, contraste, netteté, JPEG massacré, aberration chromatique."""
    im = ImageEnhance.Color(im).enhance(2.3)
    im = ImageEnhance.Contrast(im).enhance(1.45)
    im = im.filter(ImageFilter.UnsharpMask(4, 220, 2))
    from io import BytesIO
    b = BytesIO()
    im.resize((WID//2, HEI//2), Image.BILINEAR).save(b, 'JPEG', quality=9)
    im = Image.open(b).convert('RGB').resize((WID, HEI), Image.BILINEAR)
    a = np.asarray(im).copy()
    k = 14
    a[:, k:, 0] = a[:, :-k, 0]
    a[:, :-k, 2] = a[:, k:, 2]
    bruit = rng.integers(-18, 18, a.shape, dtype=np.int16)
    a = np.clip(a.astype(np.int16)+bruit, 0, 255).astype(np.uint8)
    return Image.fromarray(a)


def vhs(petite, rng, t):
    """Image de rembobinage : lignes de balayage, bandes décalées, bruit, logo ◀◀."""
    a = np.asarray(petite.resize((WID, HEI), Image.BILINEAR)).astype(np.int16)
    for _ in range(6):
        y0 = int(rng.uniform(0, HEI-120)); h = int(rng.uniform(20, 120))
        a[y0:y0+h] = np.roll(a[y0:y0+h], int(rng.uniform(-90, 90)), axis=1)
    a[::4] = (a[::4]*0.55).astype(np.int16)
    a += rng.integers(-40, 40, a.shape, dtype=np.int16)
    a[..., 2] = np.roll(a[..., 2], 8, axis=1)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    dr = ImageDraw.Draw(im)
    if int(t*6) % 2 == 0:
        x, y = 90, 430
        for k in range(2):
            dr.polygon([(x+k*62+60, y), (x+k*62, y+40), (x+k*62+60, y+80)], fill='white')
    return im


def images():
    d = Decor()
    n = round(DUREE*FPS)
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{WID}x{HEI}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264',
                             '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', str(M/'gag-images.mp4')],
                            stdin=subprocess.PIPE)
    memoire, gele = [], None
    i_loupe, i_rew = round(T_LOUPE*FPS), round(T_REW*FPS)
    for i in range(n):
        t = i/FPS
        if t < T_TROLL:
            im = d.celeste(t)
        elif i < i_loupe:
            im = d.troll_image(t)
            gele = im
        elif i < i_rew:
            im = d.loupe(gele, t)
        else:
            # remonte le gag à toute vitesse, de l'arrêt sur image au début du paradis
            p = (i-i_rew)/max(1, n-1-i_rew)
            j = int((len(memoire)-1)*(1-p)**0.8*0.95)
            im = vhs(memoire[j], np.random.default_rng(i), t)
            if i == n-1:
                im = Image.new('RGB', (WID, HEI), 'white')
        if i < i_rew:
            memoire.append(im.resize((WID//3, HEI//3), Image.BILINEAR))
        proc.stdin.write(im.tobytes())
        if i % 30 == 0:
            print(f'  image {i}/{n}', flush=True)
    proc.stdin.close()
    assert proc.wait() == 0


# ---------------------------------------------------------------- sous-titres du gag
def ass_temps(s):
    return f'{int(s//3600)}:{int(s % 3600//60):02}:{s % 60:05.2f}'


def sous_titres():
    styles = (DOSSIER/'_montage/sous-titres.ass').read_text(encoding='utf-8').split('[Events]')[0]
    ev = []
    debut_tag = T_DESC[1]+0.08
    ev.append(f'Dialogue: 1,{ass_temps(debut_tag)},{ass_temps(T_TROLL)},Tag,,0,0,0,,'
              r'{\an8\pos(540,420)}1 - NOKIA 3310\NINCASSABLE')
    # Troll : sous-titres qui tremblent
    gros = r'{\an2\pos(540,1420)\fs118\fsp0\bord10}'
    ev.append(f'Dialogue: 0,{ass_temps(T_TROLL+.1)},{ass_temps(T_CRU)},Default,,0,0,0,,'
              + gros + r'{\c&H4AE2FF&\t(0,150,\frz-6)\t(150,300,\frz6)\t(300,450,\frz-6)\t(450,600,\frz6)\t(600,750,\frz-4)}Hé hé hé hé !')
    ev.append(f'Dialogue: 0,{ass_temps(T_CRU)},{ass_temps(T_LOUPE)},Default,,0,0,0,,'
              + gros + r'{\c&H4E62FF&\fscx60\fscy60\t(0,120,\fscx115\fscy115)\t(120,220,\fscx100\fscy100)}T’as cru ?')
    (M/'gag.ass').write_text(styles+'[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
                             + '\n'.join(ev)+'\n', encoding='utf-8')


# ---------------------------------------------------------------- assemblage
def assembler():
    shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf', M/'police.ttf')
    shutil.copy2(DOSSIER/'_montage/header-footer-reference.png', M/'header-footer-reference.png')
    run(['ffmpeg', '-v', 'error', '-y', '-i', 'gag-images.mp4', '-i', 'gag.wav',
         '-loop', '1', '-framerate', '30', '-i', 'header-footer-reference.png',
         '-filter_complex', '[0:v]ass=gag.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v]',
         '-map', '[v]', '-map', '1:a', '-t', str(DUREE), '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
         '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', 'gag.mov'], M)
    t_coupe = COUPE/FPS
    graphe = (f'[0:v]trim=end_frame={COUPE},setpts=PTS-STARTPTS[v0];'
              f'[0:v]trim=start_frame={COUPE},setpts=PTS-STARTPTS[v2];'
              f'[0:a]atrim=end={t_coupe:.6f},asetpts=PTS-STARTPTS,afade=t=out:st={t_coupe-0.02:.6f}:d=0.02[a0];'
              f'[0:a]atrim=start={t_coupe:.6f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[a2];'
              '[1:v]setpts=PTS-STARTPTS,fps=30,setsar=1[v1];[1:a]aresample=44100,asetpts=PTS-STARTPTS[a1];'
              '[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]')
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(V1), '-i', 'gag.mov', '-filter_complex', graphe,
         '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'final.mp4'], M)
    run(['ffmpeg', '-v', 'error', '-i', 'final.mp4', '-f', 'null', '-'], M)
    shutil.copy2(M/'final.mp4', W/'final.mp4')


def documents():
    histoire = json.loads((DOSSIER/'version-validee/histoire.json').read_text(encoding='utf-8'))
    histoire['version'] = 'V2 troll Nokia 3310'
    histoire['statut'] = 'export de travail'
    histoire['gag_troll'] = dict(
        insertion=round(COUPE/FPS, 3), duree=DUREE,
        deroule=['sans voix : vraie photo du Nokia 3310 qui descend du ciel avec une aura, chœur et harpe, carillon à l’atterrissage (bandeau 1 - NOKIA 3310 / INCASSABLE)',
                 'coupure : boom, tête de troll « deep fried », rire, « T’as cru ? »',
                 'loupé : disque rayé, arrêt sur image en noir et blanc, tampon LOUPÉ !',
                 'rembobinage VHS puis vrai numéro 1 inchangé'],
        note='Gag assumé, aucun fait : le Nokia 3310 n’est pas présenté comme un téléphone cher.')
    (W/'histoire.json').write_text(json.dumps(histoire, ensure_ascii=False, indent=2), encoding='utf-8')
    credits = (DOSSIER/'version-validee/CREDITS.md').read_text(encoding='utf-8')
    credits = credits.replace('## Son', '## Séquence gag (V2)\n'
        '- Nokia 3310 : photo « Nokia 3310 Blue R7309170 (retouch).png », smial, Wikimedia Commons, '
        'Licence Art Libre 1.3 (http://artlibre.org/licence/lal/), '
        'https://commons.wikimedia.org/wiki/File:Nokia_3310_Blue_R7309170_(retouch).png. Photo non '
        'modifiée, posée sur un décor animé. Nokia est une marque de Nokia Corporation, citée pour '
        'désigner le produit.\n'
        '- Tête de troll : illustration originale dessinée pour la vidéo (SVG, '
        'assets/refonte-14-20/telephone/troll/dessins), sans reprise du mème « Trollface ».\n'
        '- Voix du troll : ElevenLabs, voix Callum.\n'
        '- Bruitages (chœur et harpe, carillons, boom, rire, disque rayé, tampon, rembobinage) : '
        'ElevenLabs Sound Effects.\n\n## Son')
    (W/'CREDITS.md').write_text(credits, encoding='utf-8')
    for f in ('legende.txt', 'publication.txt', 'script.txt'):
        shutil.copy2(DOSSIER/'version-validee'/f, W/f)


if __name__ == '__main__':
    M.mkdir(parents=True, exist_ok=True)
    etapes = sys.argv[1:] or ['audio', 'images', 'sous_titres', 'assembler', 'documents', 'comparer']
    for e in etapes:
        print('>>', e, flush=True)
        if e == 'comparer':
            compare(W)
        else:
            globals()[e]()
