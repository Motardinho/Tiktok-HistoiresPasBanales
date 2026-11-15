from production import *
import hashlib,datetime
v=WORK/'v4';qc=v/'controle-export'
r=json.loads((qc/'resultat-technique.json').read_text(encoding='utf-8'));assert r['decodage_exit']==0
video=OUT/'essai-long-v4.mp4';sha=hashlib.file_digest(video.open('rb'),'sha256').hexdigest()
h=json.loads((v/'histoire-travail.json').read_text(encoding='utf-8'))
h.update(statut='essai V4 — prononciation SSC reprise, vitesse du propriétaire explicitée ; écoute à confirmer',export_actuel=video.name,script_actuel='script-v4.txt',montage='_montage/v4/plans.json')
h['scenes']=[{'narration':(OUT/f'script-{n}-v4.txt').read_text(encoding='utf-8').strip()} for n in ['ssc','bugatti','yangwang']]
writej(OUT/'histoire.json',h)
m=json.loads((OUT/'livraison.json').read_text(encoding='utf-8'))
m.update(video=video.name,description='description-youtube-v4.txt',legende='legende-v4.txt',script='script-v4.txt',sous_titres='sous-titres-v4.srt',sha256=sha,revision='Prononciation SSC reprise dans les chapitres 3 et 1 ; 474,8 km/h annoncé directement avec Larry Caplin vers 0:50',rapport_revision='controle-livraison-v4.txt',plans='_montage/v4/plans.json')
writej(OUT/'livraison.json',m)
report=f'''CONTRÔLE V4 — 15 novembre 2026, Europe/Paris
Essai à visionner, aucune validation utilisateur.
Fichier : {video.name}
SHA-256 : {sha}
Corrections demandées par Marc : sigle SSC entendu comme SSSC ; vitesse de la nouvelle tentative du propriétaire pas assez explicite.
Voix SSC et Yangwang régénérées avec « èsse èsse cé », Bugatti conservée. Ajustement de tempo continu par chapitre à la durée précédente ; aucun mot découpé ni pause artificielle ajoutée.
Ajout : « Et avec lui au volant, la Tuatara atteint quatre cent soixante-quatorze virgule huit kilomètres-heure. » après Larry Caplin, le propriétaire. Sous-titre 474,8 KM/H de 49,889 à 53,924 s.
Montage image : manifeste des 231 plans identique V3, clips réutilisés sans modification. Les contrôles d'identité et de recadrage documentés en V3 restent applicables. Sous-titres et accents resynchronisés.
Captures finales réellement examinées : controle-export/final-0.jpg à final-3.jpg, 32 instants {r['captures']}. Aperçu mobile.jpg à 360 px. Contrôle des nouveaux sous-titres, début, transitions et fin. Pas de visionnage continu.
Décodage intégral ffmpeg réussi (code 0), durée {r['duree']} s. Résolution et niveaux : fichiers probe.json et niveaux.txt du même dossier.
Limite déterminante : aucune écoute réelle effectuée. Le texte phonétique et l'alignement ne permettent pas de certifier à eux seuls que le défaut SSSC est corrigé à l'oreille. Statut essai, pas prêt à publier.
Limites V3 conservées : certaines archives douces et réutilisées ; volet jaune baisse momentanément le contraste du logo et masque une partie du sous-titre ; scènes de contexte ne prouvent pas les actions non filmées. Miniature inchangée. Sources tierces créditées, revendications possibles.
'''
(OUT/'controle-livraison-v4.txt').write_text(report,encoding='utf-8')
print('Manifestes V4 enregistrés',sha,flush=True)
