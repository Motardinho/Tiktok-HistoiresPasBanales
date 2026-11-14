import json,re,sys
from pathlib import Path
p=Path('out/34-il-trichait-aux-echecs');m=p/'_montage';prefix='34-echecs-sms/'
t=json.loads((m/'timings-oraux.json').read_text(encoding='utf8'));words=t['words']
P=lambda i:prefix+f'pexels-{i}.mp4'
# Fin sur un mot de la prise audio conservée (index + mot contrôlés).
rows=[
 (4,'Son',P(33688494),.7,.5,'Hook : déplacement réel de pièce, déjà en action'),
 (8,'Russie,',P(7688807),2.1,.5,'Deuxième plan du hook : coup sur échiquier'),
 (13,'Olympiades',P(6689107),3.5,.5,'Échiquier en travelling : contexte, illustration'),
 (20,'Sébastien',P(8427425),2,.5,'Échiquier avec pendule : compétition, illustration'),
 (26,'À',prefix+'feller2017.jpg',0,.5,'Portrait réel de Feller (2017), Stefan64, CC BY-SA 4.0 ; photo 2008 rejetée pour résolution insuffisante'),
 (35,'Un',P(5647324),8,.5,'Clavier : complice en France, illustration sans visage'),
 (40,'Lui,',P(5647327),8,.5,'Calcul des coups : détail du clavier, illustration'),
 (52,'Le',prefix+'transmission-france-russie.mp4',0,.5,'Animation originale demandée par Marc : Nancy -> Khanty-Mansiïsk, trajet illustratif du SMS'),
 (64,'Sauf',P(39494839),2,.5,'Téléphone : messages codés, illustration, pas un véritable SMS de l’affaire'),
 (73,'Et',P(6032047),2,.5,'Pièces : les chiffres cachent des coups, illustration'),
 (85,'pour',P(8427425),7,.5,'Échiquier et pendule, relais du capitaine évoqué sans lui attribuer un figurant'),
 (91,'Mais',P(10388941),6,.5,'Main déplaçant une pièce : indication reçue, illustration'),
 (98,'Le',P(7196206),.5,.5,'Relance : déplacement de pièce'),
 (106,'Un',P(5081435),.2,.62,'Téléphone sur table, illustration moderne signalée en légende'),
 (115,'La',P(39494839),8,.5,'Écran de téléphone : arrivée du message, illustration sans citation fabriquée'),
 (121,'La',P(6689890),2,.5,'Pause de révélation : gros plan de pièce blanche'),
 (127,'Oui,',P(6374206),.8,.5,'Téléphone sur une table dans un intérieur : pas une image de la vice-présidente'),
 (133,'Elle',P(5081435),4,.62,'Retour au téléphone laissé sur la table'),
 (136,'Le',P(39494839),14,.5,'Téléphone : alerte donnée'),
 (141,'Devant',P(5647324),13.3,.5,'Complice : clavier, illustration ; passage 16 s rejeté, doigt masque le cadre'),
 (145,'il',P(7196206),6.5,.5,'Échiquier : aveux devant la fédération'),
 (152,'En','31-pogba/pexels-29992749.mp4',9,.5,'Billets en euros : motivation financière, illustration'),
 (161,'six',P(6599643),5,.5,'Pièces d’échecs : verdict de 2019'),
 (167,'Toute',P(6689107),12,.5,'Échiquier : condamnation avec sursis, pas de prison ferme illustrée'),
 (170,'trahie',P(5647327),13,.5,'Organisation : clavier'),
 (178,'Six',P(6374206),6,.5,'Retour au téléphone sur table : chute'),
 (188,'Réponds',P(8427425),12,.5,'Question : jeu et temps de réflexion'),
 (198,'Pas',P(10388941),20,.5,'Appel à réagir et abonnement sur partie en cours'),
 (None,None,P(33688494),4.8,.5,'Signature sur mouvement de pièce'),
]
plans=[]
for idx,word,src,at,c,note in rows:
 if idx is not None:assert words[idx]['w']==word,(idx,words[idx],word)
 plans.append(dict(fin=words[idx]['start'] if idx is not None else None,source=src,entree=at,cadrage=c,note=note))
(m/'plans.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2),encoding='utf8')
d=json.loads((p/'histoire.json').read_text(encoding='utf8'))
d['bandeaux']=[b for b in d['bandeaux'] if b.get('texte')!='PHOTO - 2017']+[dict(debut=9.8,fin=12.16,texte='PHOTO - 2017')]
d['sources_a_verifier']=[s for s in d['sources_a_verifier'] if s.get('fait')!='Complice à Nancy']+[dict(fait='Complice à Nancy',url='https://www.estrepublicain.fr/actualite/2011/05/20/rififi-sur-l-echiquier',note='Nancy cité explicitement, recoupé avec le SMS reçu chez la vice-présidente à Nancy dans la décision FIDE')]
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('Plans',len(plans))
