from production import *
import hashlib
v=WORK/'v5';q=v/'controle-export';r=json.loads((q/'resultat-technique.json').read_text(encoding='utf8'));assert r['decodage_exit']==0
sha=hashlib.file_digest((OUT/'essai-long-v5.mp4').open('rb'),'sha256').hexdigest()
h=json.loads((OUT/'histoire.json').read_text(encoding='utf8'));h['scenes'][0]['narration']=(OUT/'script-ssc-v5.txt').read_text(encoding='utf8').strip();h.update(export_actuel='essai-long-v5.mp4',script_actuel='script-v5.txt',statut='V4 acceptée ; seule accroche corrigée en V5, écoute du raccord à confirmer')
writej(OUT/'histoire.json',h)
m=json.loads((OUT/'livraison.json').read_text(encoding='utf8'));m.update(video='essai-long-v5.mp4',description='description-youtube-v5.txt',legende='legende-v5.txt',script='script-v5.txt',sous_titres='sous-titres-v5.srt',sha256=sha,revision='Uniquement la phrase d’ouverture demandée par Marc',rapport_revision='controle-livraison-v5.txt',statut='correction-accroche-a-ecouter',validation_precedente='V4 acceptée sauf phrase d’ouverture ; copie version-validee/final.mp4')
writej(OUT/'livraison.json',m)
(OUT/'controle-livraison-v5.txt').write_text(f'''CONTRÔLE V5 — 15 novembre 2026, Europe/Paris
Demande : seule la première phrase devient « À cette vitesse, n’importe quelle ligne droite devient trop courte. »
V4 acceptée par Marc avec cette réserve ; copie conservée dans version-validee/. V5 non encore examinée par Marc.
SHA-256 V5 : {sha}
Voix : seul le hook est régénéré. Raccord à 2,9 s, dans le silence V4 mesuré 2,582479–3,020708 s sous -45 dBFS. Hook ajusté au créneau par tempo 1,241379 ; aucune coupe de syllabe fondée sur les seuls timings. Suite du mix V4 réutilisée après 2,92 s, sans régénération. Fond musical du hook remixé ; microfondus de 20 ms au raccord.
Sous-titres : première phrase remplacée, trois groupes ; suite inchangée à partir de 3,081 s. Images : même montage muet V4, aucun changement de plans. Logo et miniature conservés.
Captures MP4 examinées : controle-export/final-0.jpg et final-1.jpg, aux instants {r['captures']}. Aperçu mobile.jpg 360 px : 0,3 / 1,3 / 2,4 / 3,2 s. Nouvelle phrase visible sans collision sur ces captures ; fin examinée à 481,9 s. Contrôles V4 applicables aux plans conservés.
Décodage intégral ffmpeg code 0, durée {r['duree']} s, 1920x1080, 30 i/s. Métadonnées et mesure des niveaux dans controle-export/.
Limites : aucune écoute réelle ni lecture continue effectuée ; contrôle du raccord sonore à confirmer. Ne pas confondre silence mesuré et raccord entendu. Archives tierces soumises aux éventuelles revendications de droits, sources inchangées.
''',encoding='utf8')
print('V5 livrable',sha,flush=True)
