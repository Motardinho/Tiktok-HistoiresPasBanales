import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
P=ROOT/'out/46-larme-de-verre';P.mkdir(exist_ok=True)
textes=[
"Ce verre résiste au marteau. Mais son point faible est minuscule.",
"Ça s'appelle une larme de verre. Sa grosse tête encaisse les coups, alors que sa queue est aussi fine qu'un fil.",
"Pour obtenir cet objet, on fait tomber du verre en fusion dans de l'eau froide. L'extérieur durcit presque immédiatement.",
"Mais à l'intérieur, le verre reste chaud. En refroidissant à son tour, il se contracte. Résultat : la surface se retrouve comprimée, et le cœur sous tension.",
"Cette compression empêche les fissures de progresser facilement. C'est ce qui rend la tête aussi résistante.",
"Mais regarde la queue. Il suffit de casser cette petite extrémité pour déclencher une réaction en chaîne.",
"La fracture remonte vers la tête. Et toute la larme se transforme en une pluie de minuscules fragments.",
"Le détail fou ? Des chercheurs ont mesuré des fissures dépassant six mille kilomètres à l'heure. Bien trop rapide pour suivre ça à l'œil nu.",
"Attention, elle n'est pas indestructible : une presse suffisamment puissante peut aussi faire céder la tête.",
"Alors, tu connaissais ce point faible ? Réponds oui ou non. Abonne-toi pour la prochaine curiosité. Pas banal, hein ?"
]
d=dict(numero=46,titre_fixe='CE VERRE CACHE UN POINT FAIBLE',format='histoire',type_post='videos',categorie='science insolite',scenes=[dict(narration=t.replace('six mille kilomètres à l\'heure','6 000 KM/H'),narration_voix=t) for t in textes],affichage={"six mille kilomètres à l'heure":"6 000 KM/H"},reference='local:out/20-telephone-2899-dollars/version-validee/final.mp4',reference_fichier='out/20-telephone-2899-dollars/version-validee/final.mp4',reference_auteur='HPB - téléphones (version validée)',statut='préparation',sources_a_verifier=[dict(fait='Résistance au marteau, trempe, surface comprimée, cœur sous tension, destruction par queue ou charge élevée',url='https://www.purdue.edu/newsroom/archive/releases/2017/Q2/research-solves-centuries-old-riddle-of-prince-ruperts-drops.html'),dict(fait='Mesure de fissures > 4000 mph, soit > 6437 KM/H ; formulation conservatrice > 6000 KM/H',url='https://www.purdue.edu/newsroom/archive/releases/2017/Q2/research-solves-centuries-old-riddle-of-prince-ruperts-drops.html'),dict(fait='Étude des contraintes et rupture finale sous charge croissante',url='https://doi.org/10.1063/1.4971339')],fun_fact='Fissures mesurées à plus de 6000 KM/H, et non vitesse des éclats.',hooks_etudies=['Ce verre résiste au marteau. Mais son point faible est minuscule.','Un marteau ne suffit pas. Un petit bout cassé, si.','Cette goutte de verre cache un point faible étonnant.','Le marteau échoue. Mais cette fine queue peut tout détruire.','Ce verre est très résistant, jusqu’à ce qu’on casse sa queue.'],tiktokabilite=dict(verdict='adapté sous réserve',preuves=['Planches réelles de A6NUNroyUys : fabrication vers 10-18 s, presse et fragmentation vers 30-45 s','Planches xe-f4gokRBs : marteau vers 70-100 s, fragmentation queue vers 150-180 s','Planches lt-zvsGvtqg : gouttes, marteau, polarisation, fabrication'],limites='Sources de laboratoire/ralentis parfois 1080p seulement ; recadrages et mouvement détaillé encore à vérifier. Aucun visuel de synthèse ni photo de remplacement prévu.'))
(P/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
(P/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes'])+'\n',encoding='utf8')
print('Mots :',len(' '.join(textes).split()))
if '--voix' in sys.argv:
 from produire_lot_16_18 import speech
 speech(P)
