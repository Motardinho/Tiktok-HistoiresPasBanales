from production import *
import shutil,hashlib
p=OUT/'version-validee';p.mkdir(exist_ok=True)
for src,dst in [('essai-long-v4.mp4','final.mp4'),('script-v4.txt','script.txt'),('miniature-youtube.jpg','miniature-youtube.jpg'),('description-youtube-v4.txt','description-youtube.txt'),('legende-v4.txt','legende.txt')]:
 if not (p/dst).exists():shutil.copy2(OUT/src,p/dst)
writej(OUT/'validation-utilisateur.json',{'date':'2026-11-15','fuseau':'Europe/Paris','version':'V4','sha256':hashlib.file_digest((OUT/'essai-long-v4.mp4').open('rb'),'sha256').hexdigest(),'message':"OK Pour la video, juste le début il faut plutôt dire A cette vitesse, n'importe quelle ligne droite devient trop courte",'portee':'Vidéo acceptée avec correction explicite de la première phrase ; V5 non encore examinée par Marc.'})
