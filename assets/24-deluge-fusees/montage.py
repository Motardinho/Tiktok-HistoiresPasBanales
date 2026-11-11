import json
from pathlib import Path
p=Path('out/24-deluge-fusees');m=p/'_montage'
d=json.loads((p/'histoire.json').read_text(encoding='utf8'))
d['bandeaux']=[dict(debut=3.8,fin=6.5,texte='ESSAI AU SOL - 2023'),dict(debut=34.16,fin=38.8,texte='1,5 MILLION DE LITRES'),dict(debut=55,fin=58,texte='ARTEMIS I - 2022')]
d['fun_fact']['debut']=46.58;d['fun_fact']['fin']=53.7
d['reference_qualite']='Copie validée du dossier téléphones, comparaison locale demandée comme étalon qualité ; la référence URL du dossier 20 est conservée à titre documentaire.'
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
# Fin timeline, fichier source, entrée, centre horizontal, commentaire.
rows=[
 (2.3,'deluge-sol-2023',34.5,.50,'Accroche : jets actifs, vue plongeante'),
 (6.5,'deluge-drone2-2023',22,.48,'Déluge trois-quarts'),
 (9.3,'deluge-sol-2023',48.3,.46,'Eau sur la plateforme'),
 (11.68,'deluge-drone-2023',25,.50,'Vue en plongée'),
 (15.2,'lancement-plateforme',15,.50,'Allumage moteurs Artemis I'),
 (18.7,'lancement-plateforme',29,.52,'Déluge et propulsion'),
 (22.68,'lancement-suivi',50,.50,'Fusée entière lors du décollage'),
 (26.0,'deluge-drone2-2023',30,.48,'Déluge protégeant la plateforme'),
 (29.6,'deluge-sol-2023',60,.46,'Eau ruisselant sur les installations'),
 (32.0,'lancement-plateforme',35,.50,'Eau au pied des moteurs'),
 (34.16,'deluge-sol-2023',72,.48,'Ruissellement sur la tour'),
 (37.5,'deluge-drone-2023',17,.50,'Essai de 2023, montée du débit'),
 (40.8,'deluge-sol-2023',39,.50,'Jets en vue plongeante'),
 (44.0,'deluge-drone2-2023',36,.48,'Déluge de trois-quarts'),
 (46.58,'deluge-drone2-2023',11,.48,'Buses avant le déluge, vue de trois-quarts'),
 (50.2,'deluge-drone2-2023',15,.48,'Buses et démarrage des jets, vue de trois-quarts'),
 (54.76,'deluge-drone-2023',30,.50,'Buses autour des ouvertures moteurs'),
 (58.0,'lancement-plateforme',41.5,.50,'Allumage des propulseurs'),
 (60.5,'lancement-suivi',58,.50,'Décollage Artemis I'),
 (63.04,'lancement-suivi',68,.50,'Ascension, cadrage sur le lanceur'),
 (66.5,'deluge-sol-2023',66,.48,'Retour explicite à l’essai au sol'),
 (70.64,'deluge-drone2-2023',42,.48,'Plateforme sans fusée'),
 (None,'deluge-sol-2023',75,.48,'Question et signature sur l’eau')
]
(m/'plans.json').write_text(json.dumps([dict(fin=f,source='24-deluge-fusees/'+s+'.mp4',entree=t,cadrage=c,note=n) for f,s,t,c,n in rows],ensure_ascii=False,indent=2),encoding='utf8')
