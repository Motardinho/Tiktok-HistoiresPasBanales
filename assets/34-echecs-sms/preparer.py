import json
from pathlib import Path

p = Path('out/34-il-trichait-aux-echecs')
p.mkdir(exist_ok=True)
(p/'_montage').mkdir(exist_ok=True)
texts = [
"Il trichait aux échecs. Son capitaine faisait l'antenne.",
"Russie, septembre 2010. Olympiades d'échecs : les équipes nationales s'affrontent. Sébastien Feller joue pour la France.",
"À Nancy, un complice suit ses parties sur Internet. Un logiciel calcule les coups. Lui, il les envoie par SMS au capitaine, en Russie.",
"Le plus tordu ? Les messages ressemblent à des numéros de téléphone. Sauf que les chiffres cachent les coups à jouer.",
"Et le capitaine fait quoi ? Il se place dans la salle pour transmettre les indications au joueur.",
"Mais leur combine se retourne contre eux. Le complice laisse son téléphone sur une table. Un message arrive : on lui réclame les coups.",
"La personne qui le voit ? La vice-présidente de la fédération française. Oui, le téléphone traînait chez elle. Elle donne l'alerte.",
"Le complice finit par avouer. Devant la fédération internationale, il explique avoir fait ça pour l'argent.",
"En 2019, les trois sont condamnés à six mois de prison avec sursis. Toute cette organisation, trahie par un téléphone laissé sur une table.",
"Six mois avec sursis : trop léger ou suffisant ? Réponds en deux mots, et abonne-toi pour le prochain dossier. Pas banal, hein ?"
]
voice = [s.replace('2010','deux mille dix').replace('2019','deux mille dix-neuf').replace('SMS','S M S') for s in texts]
fide='https://www.fide.com/images/stories/NEWS_2012/FIDE/FIDE_Ethics_Commission_Judgement_in_the_case_French_Team.pdf'
d=dict(numero=34,titre='Il trichait aux échecs',titre_fixe='IL TRICHAIT AUX ÉCHECS',titre_lignes=['IL TRICHAIT','AUX ÉCHECS'],serie='ÉCHECS - OLYMPIADES 2010',format='histoire',statut='script vérifié - production',hook=texts[0],
scenes=[dict(narration=t,narration_voix=v,animate=False) for t,v in zip(texts,voice)],
affichage={'deux mille dix':'2010','deux mille dix-neuf':'2019','six mois':'6 mois','s m s':'SMS'},
bandeaux=[dict(scene=1,duree=2.0,texte='RUSSIE - SEPTEMBRE 2010'),dict(scene=1,apres=2.3,duree=2.3,texte='OLYMPIADES PAR ÉQUIPES')],
fun_fact=dict(scene=3,texte=['DES COUPS CACHÉS','DANS DES NUMÉROS'],source=fide),
legende="Un logiciel en France, des SMS vers la Russie, un capitaine qui transmet les coups… et un téléphone laissé chez la mauvaise personne. Olympiades d'échecs 2010. En 2019 : six mois de prison avec sursis pour les trois protagonistes. Trop léger ou suffisant ?",
hashtags=['#histoirevraie','#echecs','#triche','#insolite','#HistoiresPasBanales'],
reference_fichier='out/28-om-a-achete-un-match/version-validee/final.mp4',reference_auteur='HPB - OM-VA validée, étalon du ton',reference='hpb-28-om-va-version-validee',musique='scandale',
choix_editoriaux=["Marc choisit le deuxième sujet le 11 novembre 2026. Animation France-Russie façon film d'agent secret expressément demandée pendant la préparation.","Seul Sébastien Feller est nommé à l'oral : vrai portrait au nom. Les autres personnes sont désignées par leur fonction.","Ne pas dire que Feller a gagné les Olympiades : distinction individuelle au cinquième échiquier, pas victoire de la France.","Les plans d'échiquiers, téléphone et clavier sont des illustrations, pas des archives de la triche. Animation du trajet illustrative.","La FIDE ne fixe pas un code spatial unique : pas de fausse démonstration case par case.","Condamnation de 2019 rapportée comme datée ; ne pas affirmer un état actuel de suspension."],
sources_a_verifier=[
dict(fait='Compétition en Russie, 21 septembre au 3 octobre 2010 ; Feller dans l’équipe française',url=fide,note='pages 17-18 examinées'),
dict(fait='Logiciel en France, SMS au capitaine ; numéros en apparence téléphoniques ; déplacements dans la salle',url=fide,note='pages 18-22 ; méthode spatiale non précisée de façon univoque'),
dict(fait='SMS aperçu le 27 septembre chez la vice-présidente à Nancy, téléphone laissé sur une table, alerte au président',url=fide,note='page 18'),
dict(fait='Aveux du complice et motivation financière',url=fide,note='page 21, audience du 6 avril 2012'),
dict(fait='Six mois de prison avec sursis pour chacun en 2019',url='https://infos.rtl.lu/news/frontieres/un-champion-dechecs-mosellan-condamne-avec-sursis-1354409',note='Article publié le 28 mai 2019. Ne pas reprendre son erreur sur la victoire de la compétition.')])
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(p/'script.txt').write_text('\n\n'.join(texts)+'\n',encoding='utf8')
(p/'hooks.txt').write_text('\n'.join([texts[0],"Son meilleur coup venait d'un SMS.","Un logiciel, trois complices, un téléphone de trop.","Le capitaine se promenait. Le joueur recevait les réponses.","Ils cachaient leurs coups dans des numéros de téléphone."])+ '\nChoix : premier, court et lié au relais humain.\n',encoding='utf8')
print('Mots:',len(' '.join(texts).split()))
