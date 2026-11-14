"""Dossier 44 : top 5 des buts les plus dégueulasses, chaque but montré en entier (demande de Marc, 12 novembre 2026).
Écrit histoire.json. Lancer depuis la racine : python assets/44-buts-top5/preparer.py
"""
import json
import os
import re

S = [
 (None, "Top 5 des buts les plus dégueulasses. Le numéro 1, son buteur l'a réclamé sur la vie de sa fille.",
        "Top cinq des buts les plus dégueulasses. Le numéro un, son buteur l'a réclamé sur la vie de sa fille."),
 (5, "Numéro 5. Mondial 2010, Angleterre contre États-Unis. Dempsey frappe de loin, sans conviction. Rob Green se couche dessus… et laisse filer le ballon entre ses gants.",
     "Numéro cinq. Mondial deux mille dix, Angleterre contre États-Unis. Dèmpsi frappe de loin, sans conviction. Rob Grine se couche dessus… et laisse filer le ballon entre ses gants."),
 (4, "Numéro 4. Wembley, 2010, Manchester United contre Chelsea. Chicharito rate complètement sa reprise. Le ballon lui rebondit en plein visage… et rentre. Son premier but avec le club.",
     "Numéro quatre. Ouèmblé, deux mille dix, Manchester Iounaïted contre Tchelsi. Tchitcharito rate complètement sa reprise. Le ballon lui rebondit en plein visage… et rentre. Son premier but avec le club."),
 (3, "Numéro 3. Bundesliga, 2013. La tête de Kießling passe à côté du poteau… et rentre par un trou dans le filet. L'arbitre accorde le but. Le match ne sera jamais rejoué.",
     "Numéro trois. Boundesliga, deux mille treize. La tête de Kisling passe à côté du poteau… et rentre par un trou dans le filet. L'arbitre accorde le but. Le match ne sera jamais rejoué."),
 (2, "Numéro 2. Premier League, 2009. Le tir de Darren Bent tape un ballon de plage, lancé par un supporter de Liverpool. Leur gardien se trompe de ballon.",
     "Numéro deux. Première Ligue, deux mille neuf. Le tir de Darène Bente tape un ballon de plage, lancé par un supporter de Liverpoul. Leur gardien se trompe de ballon."),
 (2, "Ce ballon de plage est aujourd'hui au musée.", "Ce ballon de plage est aujourd'hui au musée."),
 (1, "Numéro 1. Premier League, 2018. Coup franc d'Eriksen, direct au fond. Mais Kane jure l'avoir touché. Sur la vie de sa fille. Quatre jours plus tard, le but lui est accordé.",
     "Numéro un. Première Ligue, deux mille dix-huit. Coup franc d'Érikssène, direct au fond. Mais Kayne jure l'avoir touché. Sur la vie de sa fille. Quatre jours plus tard, le but lui est accordé."),
 (None, "Kane l'a touché : oui ou non ? Abonne-toi pour le prochain dossier. Pas banal, hein ?",
        "Kayne l'a touché : oui ou non ? Abonne-toi pour le prochain dossier. Pas banal, hein ?"),
]
scenes = []
for r, n, v in S:
    s = {"narration": n, "narration_voix": v}
    if r is not None:
        s["rang"] = r
    scenes.append(s)
B = [(1, "5 - COUPE DU MONDE - 2010\\NANGLETERRE - ÉTATS-UNIS"), (2, "4 - COMMUNITY SHIELD - 2010\\NMAN UNITED - CHELSEA"),
     (3, "3 - BUNDESLIGA - 2013\\NHOFFENHEIM - LEVERKUSEN"), (4, "2 - PREMIER LEAGUE - 2009\\NSUNDERLAND - LIVERPOOL"),
     (6, "1 - PREMIER LEAGUE - 2018\\NSTOKE - TOTTENHAM")]
d40 = json.load(open('out/40-top-10-buts-les-plus-degueulasses/histoire.json', encoding='utf-8'))
garde = ('8 -', '4 -', '3 -', '2 -', '1 -')
d = {
 "numero": 44,
 "titre": "Top 5 des buts les plus dégueulasses",
 "titre_fixe": "TOP 5 DES BUTS LES PLUS DÉGUEULASSES",
 "titre_lignes": ["TOP 5 DES", "BUTS LES PLUS", "DÉGUEULASSES"],
 "serie": "TOP 5 - BUTS DÉGUEULASSES",
 "format": "top",
 "type_post": "videos",
 "statut": "script prêt",
 "hook": scenes[0]["narration"],
 "scenes": scenes,
 "affichage": {"top cinq": "Top 5", "le numéro un": "le N°1", "deux mille dix": "2010", "deux mille dix-huit": "2018",
   "deux mille treize": "2013", "deux mille neuf": "2009", "dèmpsi": "Dempsey", "rob grine": "Rob Green",
   "ouèmblé": "Wembley", "manchester iounaïted": "Manchester United", "tchelsi": "Chelsea", "tchitcharito": "Chicharito",
   "boundesliga": "Bundesliga", "kisling": "Kießling", "première ligue": "Premier League", "darène bente": "Darren Bent",
   "liverpoul": "Liverpool", "érikssène": "Eriksen", "d'érikssène": "d'Eriksen", "kayne": "Kane",
   "numéro cinq": "N°5", "numéro quatre": "N°4", "numéro trois": "N°3", "numéro deux": "N°2", "numéro un": "N°1"},
 "bandeaux": [{"scene": s, "duree": 3.5, "texte": t} for s, t in B],
 "reference_fichier": "out/25-montagnes-russes-plus-rapides/version-validee/final.mp4",
 "reference_auteur": "HPB - montagnes russes validée (top), comme les dossiers 38 et 40",
 "reference": "hpb-25-montagnes-russes-version-validee",
 "fun_fact": {"scene": 5, "rang": 2, "texte": ["LE BALLON DE PLAGE", "EST AU MUSÉE"],
   "source": "https://nationalfootballmuseum.com/?p=38291 - National Football Museum (Manchester), « Object of the Week: History's most controversial beach ball » ; à revérifier : exposé ou en réserve"},
 "legende": "Notre top 5 des buts les plus dégueulasses, montrés en entier : un gardien qui se troue, un nez, un trou dans le filet, un ballon de plage… et un but réclamé sur la vie d'une fille. Kane l'a touché, oui ou non ?",
 "hashtags": ["#histoirevraie", "#foot", "#football", "#top", "#record", "#HistoiresPasBanales"],
 "musique": "voitures",
 "bandeau_y": 380,
 "fun_fact_top": 380,
 "choix_editoriaux": [
  "Demande de Marc du 12 novembre 2026 : « fais un top 5 mais on doit voir l'entièreté des buts ». Cinq buts choisis par Marc parmi les dix du dossier 40 (option « les plus visuels ») : Rob Green, Chicharito, Kießling, Darren Bent, Kane.",
  "Chaque but est montré en continu : l'action en direct du départ jusqu'au ballon au fond, puis son ralenti, sans photo ni plan de coupe au milieu. Les coupes sont celles du réalisateur d'origine.",
  "Faits repris du dossier 40, vérifiés le 11-12 novembre 2026 ; ajouts tirés des mêmes sources : premier but de Chicharito avec United, but de Kießling accordé et match non rejoué (DFB, 28 octobre 2013), but attribué à Kane le 11 avril 2018, quatre jours après le match du 7 avril.",
  "Classement éditorial, pas une mesure. Kane n°1 pour la question finale clivante.",
  "Prononciation corrigée par Marc le 12 novembre 2026 : « Première Ligue » à la française et « Kayne » (pas « Kané »). Voix régénérée, plans recalés.",
  "Images : extraits des diffuseurs et clubs en licence YouTube standard, sans autorisation, sur choix explicite de Marc ; sources citées en légende.",
 ],
 "sources_a_verifier": [x for x in d40["sources_a_verifier"] if x["fait"].startswith(garde)],
}
out = 'out/44-top-5-buts-les-plus-degueulasses/histoire.json'
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
mots = lambda t: len(re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?|\d+", t))
print("44 :", mots(" ".join(s["narration"] for s in scenes)), "mots,", len(d["sources_a_verifier"]), "sources")
