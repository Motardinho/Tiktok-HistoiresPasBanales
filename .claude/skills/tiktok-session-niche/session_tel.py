"""Session de chauffe TikTok sur le téléphone (Redmi Note 11 Pro 5G, 1080x2400) par adb.

Usage : python session_tel.py <dossier_status> <durée_min> [<index_niche>] [<jeu>]
  jeu = hpb (défaut) ou sport. Écrit <dossier_status>/status.json (stats + journal).

Règles : vidéo lue en entier (barre de progression), 5-10 s de pause puis suivante,
zap 20 % après 5-10 s, vidéo > 3 min zappée, like 30 %, partage (copier le lien) 10 %,
commentaire 20 %, suivi 10 %, au hasard entre 30 et 85 % de la vidéo.
Recherches et commentaires sans accents : `adb shell input text` ne passe pas les accents.
"""
import io, json, random, subprocess, sys, time
from PIL import Image

ADB = r"C:\Users\Marc\AppData\Local\Android\Sdk\platform-tools\adb.exe"
OUT = sys.argv[1]  # dossier pour status.json
DUREE_MIN = float(sys.argv[2]) if len(sys.argv) > 2 else 45
JEUX = {
    # Compte @histoirespasbanales : tops, records, culture générale
    "hpb": (["le saviez vous", "culture generale", "records du monde", "histoire vraie incroyable",
             "le saviez vous geographie", "astronaute espace", "armees les plus puissantes",
             "faits incroyables", "classement top 3 monde", "top 3 record"], 6),
    # Sport insolite (demande de Marc, 11 novembre 2026) : 4 vidéos par recherche pour varier
    "sport": (["record insolite sport", "marathon des sables perdu desert", "jo 1904 marathon",
               "tricherie sport incroyable", "match le plus etrange football", "steven bradbury",
               "malediction sport", "coupe jules rimet volee", "records sportifs impossibles",
               "philippe croizon manche", "barkley marathons", "boris onischenko",
               "isner mahut wimbledon", "eric moussambani", "gino bartali", "match de la mort kiev",
               "bob beamon saut", "epreuves olympiques oubliees", "histoire du sport incroyable"], 4),
}
NICHES, PAR_NICHE = JEUX[sys.argv[4] if len(sys.argv) > 4 else "hpb"]
P = dict(zap=0.20, like=0.30, share=0.10, comment=0.20, follow=0.10)
DUREE_MAX = 180
MOTS = ["Fascinant", "Incroyable", "Passionnant", "Impressionnant", "Captivant", "Je ne savais pas",
        "On apprend un truc", "Merci pour le partage", "Top contenu", "Tellement fascinant",
        "Bravo pour le travail", "Excellent"]

stats = dict(debut=time.strftime("%H:%M:%S"), videos=0, lues=0, zaps=0, longues=0, illisibles=0,
             likes=0, partages=0, commentaires=0, suivis=0, niche="", count=0, log=[], err=None,
             stopped=False)
fin = time.time() + DUREE_MIN * 60
stats["fin"] = time.strftime("%H:%M:%S", time.localtime(fin))


def save():
    with open(OUT + "/status.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)


def log(m):
    stats["log"].append(time.strftime("%H:%M:%S ") + m)
    stats["log"] = stats["log"][-80:]
    save()


def adb(*a):
    return subprocess.run([ADB, "shell", *a], capture_output=True, text=True, timeout=30).stdout


def tap(x, y):
    adb("input", "tap", str(x), str(y))


def attendre_tel():
    """Le téléphone a décroché d'adb : attendre son retour (jusqu'à 10 min)."""
    log("téléphone déconnecté, attente")
    t = time.time()
    while time.time() - t < 600:
        out = subprocess.run([ADB, "devices"], capture_output=True, text=True).stdout
        if "\tdevice" in out:
            log("téléphone revenu")
            time.sleep(3)
            return
        time.sleep(5)
    raise RuntimeError("téléphone absent depuis 10 min")


def cap():
    for _ in range(3):
        b = subprocess.run([ADB, "exec-out", "screencap", "-p"], capture_output=True, timeout=30).stdout
        try:
            return Image.open(io.BytesIO(b)).convert("RGB")
        except Exception:
            attendre_tel()
    raise RuntimeError("capture impossible")


def gris(p, v, tol=18):
    r, g, b = p
    return abs(r - g) < 10 and abs(g - b) < 10 and abs(r - v) < tol


def progression(im):
    """Fraction lue d'après la barre : deux niveaux de gris (clair = lu à gauche, foncé = restant),
    valeurs variables selon le fond. None si pas de barre lisible."""
    xs = list(range(60, 1030, 10))
    for y in range(2060, 2200, 2):
        px = [im.getpixel((x, y)) for x in xs]
        if sum(1 for p in px if abs(p[0] - p[1]) < 10 and abs(p[1] - p[2]) < 10) < len(xs) * 0.95:
            continue
        v = [p[0] for p in px]
        clair, fonce = v[0], v[-1]
        if not (clair - fonce > 50 and fonce >= 40 and clair >= 120):
            continue
        lu = [abs(a - clair) < 15 for a in v]
        reste = [abs(a - fonce) < 15 for a in v]
        if sum(1 for a, b in zip(lu, reste) if a or b) < len(xs) * 0.9:
            continue
        # la barre est fine : 10 px au-dessus et en dessous, autre couleur
        fine = all(abs(im.getpixel((500, y + dy))[0] - v[len(v) // 2]) > 12 for dy in (-10, 10))
        if not fine:
            continue
        # une seule transition clair -> foncé
        n_lu = 0
        while n_lu < len(v) and not reste[n_lu]:
            n_lu += 1
        return n_lu / len(xs)
    return None


def decalage(im):
    """Décalage vertical de la colonne de boutons par rapport à la mise en page de référence
    (bulle commentaire blanche avec ses points, flèche de partage blanche). None si introuvable."""
    W = lambda y: est_blanc(im.getpixel((996, y)))
    for d in range(-140, 42, 2):
        if (W(1505 + d) and W(1545 + d) and not W(1529 + d)
                and W(1830 + d) and W(1850 + d) and W(1870 + d)):
            return d
    return None


def est_rouge(p):
    return p[0] > 200 and p[1] < 110 and p[2] < 140


def est_blanc(p):
    return min(p) > 215


def au_premier_plan():
    out = adb("dumpsys", "window", "|", "grep", "mCurrentFocus")
    if not out.strip():
        attendre_tel()
        out = adb("dumpsys", "window", "|", "grep", "mCurrentFocus")
    return "com.zhiliaoapp.musically" in out


def like():
    im = cap()
    d = decalage(im)
    if d is None:
        return "absent"
    p = im.getpixel((996, 1370 + d))
    if est_rouge(p):
        return "deja"
    if not est_blanc(p):
        return "absent"
    tap(996, 1370 + d)
    time.sleep(1.2)
    return "ok" if est_rouge(cap().getpixel((996, 1370 + d))) else "?"


def suivre():
    im = cap()
    d = decalage(im)
    if d is None:
        return "absent"
    if not est_rouge(im.getpixel((1014, 1270 + d))):
        return "absent"
    tap(996, 1252 + d)
    time.sleep(1.5)
    return "ok"


def partager():
    im = cap()
    d = decalage(im)
    if d is None:
        return "absent"
    h = im.getpixel((996, 1370 + d))
    if not (est_blanc(h) or est_rouge(h)):
        return "absent"
    tap(996, 1855 + d)
    time.sleep(2.2)
    p = cap().getpixel((446, 1806))
    if not (p[2] > 200 and p[0] < 120):
        adb("input", "keyevent", "KEYCODE_BACK")
        time.sleep(1)
        return "absent"
    tap(486, 1806)
    time.sleep(6)  # laisser partir le bandeau « Ton profil s'affichera… »
    return "ok"


def commenter():
    mot = random.choice(MOTS)
    tap(288, 2203)
    time.sleep(2)
    adb("input", "text", mot.replace(" ", "%s"))
    time.sleep(1.2)
    p = cap().getpixel((1014, 1502))
    if not est_rouge(p):
        adb("input", "keyevent", "KEYCODE_BACK")
        time.sleep(0.8)
        adb("input", "keyevent", "KEYCODE_BACK")
        time.sleep(1)
        return "absent", mot
    tap(974, 1502)
    time.sleep(2)
    return "ok", mot


def suivante():
    adb("input", "swipe", "540", "1700", "540", "450", "250")
    time.sleep(2.5)


def ouvrir_niche(q, premiere=False):
    stats["niche"] = q
    if premiere:
        tap(108, 2208)      # onglet Accueil
        time.sleep(2.5)
        tap(1002, 168)      # loupe : page de recherche vide
        time.sleep(2.5)
    else:
        adb("input", "keyevent", "KEYCODE_BACK")  # lecteur -> résultats
        time.sleep(2)
        tap(450, 162)       # champ de recherche
        time.sleep(1.5)
        tap(720, 162)       # croix : effacer
        time.sleep(0.8)
    adb("input", "text", q.replace(" ", "%s"))
    time.sleep(0.8)
    adb("input", "keyevent", "KEYCODE_ENTER")
    time.sleep(4)
    for essai in range(3):
        tap(528, 288)       # onglet Vidéos
        time.sleep(3)
        tap(272, 720)       # première vignette
        time.sleep(3)
        if "DetailActivity" in adb("dumpsys", "window", "|", "grep", "mCurrentFocus"):
            break
        # une fenêtre TikTok (localisation…) bloque : Retour = Annuler, puis on réessaie
        log("lecteur pas ouvert, fenêtre fermée par Retour")
        adb("input", "keyevent", "KEYCODE_BACK")
        time.sleep(2)
    log(f"niche « {q} »")


def regarder():
    """Regarde la vidéo courante selon les règles. Renvoie un résumé."""
    t0 = time.time()
    zap = random.random() < P["zap"]
    if zap:
        time.sleep(random.uniform(5, 10))
        stats["zaps"] += 1
        return "zap"
    actions = {k: random.uniform(0.30, 0.85) for k in ("like", "share", "comment", "follow")
               if random.random() < P[k]}
    if actions:
        log("prévu : " + ", ".join(f"{k} à {int(v * 100)} %" for k, v in actions.items()))
    faites = []
    hist = []  # (t, p)
    sans_barre = 0
    fin_vue = None
    while True:
        if time.time() > fin + 200:
            return "fin"
        im = cap()
        p = progression(im)
        t = time.time() - t0
        if p is None:
            sans_barre += 1
            if sans_barre >= 8 and not hist:  # ~15-20 s sans barre : photo, live, erreur
                stats["illisibles"] += 1
                return "sans barre"
            if hist and t - hist[-1][0] > 40:  # barre perdue en cours de route
                stats["illisibles"] += 1
                return "barre perdue"
            time.sleep(1.5)
            continue
        if hist and p < hist[-1][1] - 0.25:
            stats["lues"] += 1
            return f"lue ({int(t)} s)" + (" " + ",".join(faites) if faites else "")
        hist.append((t, p))
        if len(hist) >= 3 and hist[-1][1] > hist[0][1] + 0.01:
            duree = (hist[-1][0] - hist[0][0]) / (hist[-1][1] - hist[0][1])
            if duree > DUREE_MAX and not faites:
                time.sleep(max(0, random.uniform(5, 10) - (time.time() - t0)))
                stats["longues"] += 1
                return f"longue (~{int(duree)} s) zappée"
        if p >= 0.985:
            # fin imminente : attendre le bouclage. Après un commentaire, TikTok peut laisser
            # la vidéo figée sur sa fin sans reboucler (10 min perdues le 11 novembre 2026) :
            # au-delà de 5 s en fin de barre, la vidéo compte comme lue.
            fin_vue = fin_vue or time.time()
            if time.time() - fin_vue > 5:
                stats["lues"] += 1
                return f"lue, figée en fin ({int(t)} s)" + (" " + ",".join(faites) if faites else "")
            time.sleep(1)
            continue
        fin_vue = None
        for k, seuil in list(actions.items()):
            if p >= seuil:
                del actions[k]
                if k == "like":
                    r = like()
                    if r == "ok": stats["likes"] += 1
                    faites.append(f"like:{r}")
                elif k == "follow":
                    r = suivre()
                    if r == "ok": stats["suivis"] += 1
                    faites.append(f"suivi:{r}")
                elif k == "share":
                    r = partager()
                    if r == "ok": stats["partages"] += 1
                    faites.append(f"partage:{r}")
                elif k == "comment":
                    r, mot = commenter()
                    if r == "ok":
                        stats["commentaires"] += 1
                        faites.append(f"commentaire « {mot} »")
                    else:
                        faites.append("commentaire:absent")
                break  # une action par tour, puis relire la barre
        if t > 240:
            stats["lues"] += 1
            return "plafond 240 s" + (" " + ",".join(faites) if faites else "")
        time.sleep(1.2)


def main():
    save()
    log(f"départ, arrêt prévu à {stats['fin']}")
    i_niche = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    dans_lecteur = "DetailActivity" in adb("dumpsys", "window", "|", "grep", "mCurrentFocus")
    ouvrir_niche(NICHES[i_niche], premiere=not dans_lecteur)
    n = 0
    while time.time() < fin:
        if not au_premier_plan():
            stats["err"] = "TikTok n'est plus au premier plan"
            log(stats["err"])
            break
        r = regarder()
        stats["videos"] += 1
        stats["count"] = stats["videos"]
        n += 1
        log(f"vidéo {stats['videos']} : {r}")
        if time.time() >= fin:
            break
        time.sleep(random.uniform(5, 10))
        if n >= PAR_NICHE:
            n = 0
            i_niche = (i_niche + 1) % len(NICHES)
            ouvrir_niche(NICHES[i_niche])
        else:
            suivante()
    stats["stopped"] = True
    log("arrêt")


try:
    main()
except Exception as e:
    stats["err"] = repr(e)
    stats["stopped"] = True
    log("erreur " + repr(e))
