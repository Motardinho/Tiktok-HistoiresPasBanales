import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
P=R/'out/47-dortmund-attentat-en-bourse';P.mkdir(exist_ok=True)
textes=[
"Il attaque un bus de footballeurs pour gagner en Bourse.",
"Le onze avril deux mille dix-sept, en Allemagne, Dortmund doit affronter Monaco en quart de finale de la Ligue des champions.",
"Mais à la sortie de l'hôtel, trois explosions frappent le bus. Un joueur et un policier sont blessés. Le match est reporté.",
"Derrière cet attentat, un homme a préparé un pari glaçant. Il mise sur la chute de l'action du club.",
"Oui, Dortmund est coté en Bourse. Avec les produits financiers qu'il a achetés, une forte baisse peut lui rapporter gros.",
"Son calcul : attaquer l'équipe, faire paniquer les investisseurs, puis encaisser. Et il loge dans le même hôtel que les joueurs.",
"Mais il laisse une trace. Selon les enquêteurs, ses achats sont passés par la connexion Internet de cet hôtel.",
"Le détail fou ? Il avait réservé deux séjours, pour couvrir les deux dates possibles du match à domicile. Tout ça se préparait avant même de connaître le calendrier exact.",
"Dix jours après l'attentat, il est arrêté. En deux mille dix-huit, il est condamné à quatorze ans de prison pour tentatives de meurtre.",
"Quatorze ans, suffisant ou trop peu ? Abonne-toi pour le prochain dossier. Pas banal, hein ?"
]
aff={'onze avril deux mille dix-sept':'11 avril 2017','deux mille dix-huit':'2018','quatorze':'14','vingt-huit':'28'}
facts=[
('Attentat du 11 avril 2017, trois explosions, joueur et policier blessés, Monaco, arrestation dix jours après, condamnation 14 ans pour tentatives de meurtre','https://news.sky.com/story/man-who-bombed-borussia-dortmunds-bus-for-financial-gain-jailed-11565039'),
('Quart de finale et report du match au lendemain','https://time.com/4735973/dortmund-bus-explosion-germany-borussia-dortmund/'),
('Produits à la baisse, connexion de hôtel, même hôtel que équipe, deux réservations avant connaissance date domicile : communiqué du parquet fédéral du 21 avril 2017','https://www.bvb.de/de/de/aktuelles/news/news.html/News/Uebersicht/Pressemitteilung-des-Generalbundesanwalts.html'),
('Jugement du 27 novembre 2018','https://de.openlegaldata.io/case/lg-dortmund-2018-11-27-39-ks-400-js-20617')]
scenes=[]
for t in textes:
 n=t
 for a,b in aff.items():n=n.replace(a,b).replace(a.capitalize(),b)
 scenes.append(dict(narration=n,narration_voix=t))
d=dict(numero=47,titre_fixe='UN ATTENTAT POUR GAGNER EN BOURSE',format='histoire',type_post='videos',categorie='fait divers sport / business',scenes=scenes,affichage=aff,reference='local:out/28-om-a-achete-un-match/version-validee/final.mp4',reference_fichier='out/28-om-a-achete-un-match/version-validee/final.mp4',reference_auteur='HPB - OM-VA, ton validé',statut='préparation',sources_a_verifier=[dict(fait=f,url=u,verification='consulté le 14 novembre 2026') for f,u in facts],fun_fact='Deux réservations pour couvrir les deux dates possibles du match à domicile ; communiqué du parquet du 21 avril 2017.',hooks_etudies=['Il attaque un bus de footballeurs pour gagner en Bourse.','Son pari en Bourse commence par un attentat.','Ce bus de footballeurs était devenu son pari financier.','Il voulait encaisser grâce à la chute de Dortmund.','Trois explosions. Et derrière, un pari en Bourse.'],tiktokabilite=dict(verdict='adapté sous réserve',preuves=['Planches AFP nR0QCVgongM : prévenu escorté et menottes au tribunal','Planches euronews pHh8Fv8HfcQ : tribunal, titres BVB, courbe réelle et bus','Al Jazeera 45Opoq89Lfc : secours, police et supporters le soir de attentat','AFP K8LMgCVfUeg : évacuation du stade'],limites='Archives 720p et 1080p, certaines prises nocturnes douces. Explosion et achat en ligne non filmés dans les sources : suites réelles et contexte judiciaire uniquement, aucune reconstitution. Recadrages finaux à contrôler.'),autorisation='Marc choisit Dortmund et un post de vidéos avec de vraies archives, 14 novembre 2026.')
(P/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
(P/'script.txt').write_text('\n\n'.join(s['narration'] for s in scenes)+'\n',encoding='utf8')
print('Mots',len(' '.join(textes).split()))
if '--voix' in sys.argv:
 from produire_lot_16_18 import speech
 speech(P)

