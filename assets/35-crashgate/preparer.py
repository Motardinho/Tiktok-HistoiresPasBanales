"""Scripts des dossiers 35 (Crashgate) et 36 (Spygate) : histoire.json, script.txt, hooks.txt."""
import json
from pathlib import Path

REF = dict(reference_fichier='out/28-om-a-achete-un-match/version-validee/final.mp4',
           reference_auteur='HPB - OM-VA validée, étalon du ton', reference='hpb-28-om-va-version-validee')
WMSC = 'https://www.crash.net/f1/news/152586/1/full-detailed-wmsc-singapore-gate-transcript'
PIQUET = 'https://www.crash.net/f1/news/152109/1/nelson-piquet-jrs-statement-to-the-fia-on-singapore'
VERDICT = 'https://www.autosport.com/f1/news/78771/the-full-verdict-from-the-fia-wmsc'
GP = 'https://en.wikipedia.org/wiki/2008_Singapore_Grand_Prix'
FIA07 = 'https://www.autosport.com/f1/news/the-full-decision-by-the-fias-wmsc-4413938/4413938/'

D = {
 35: dict(
  dossier='35-renault-a-fait-crasher-son-pilote', titre='Renault a fait crasher son pilote',
  titre_lignes=['RENAULT A FAIT', 'CRASHER', 'SON PILOTE'], serie='F1 - SINGAPOUR 2008', musique='voitures',
  scenes=[
   "Renault a fait crasher son pilote. Exprès, pour faire gagner l'autre.",
   "Singapour, septembre 2008. Premier Grand Prix de nuit de la Formule 1. Fernando Alonso part quinzième.",
   "Son équipe l'arrête au stand très tôt. Bizarre. Deux tours plus tard, son coéquipier, Nelson Piquet Junior, s'écrase dans le mur.",
   "Voiture de sécurité. Les autres doivent encore ravitailler. Pas Alonso. Il passe devant, et il gagne.",
   "Le pire ? Le virage était choisi : le plus loin des grues. Et Piquet a demandé plusieurs fois à la radio : on est à quel tour ?",
   "Un an plus tard, Renault l'écarte. Alors il balance tout : on lui a demandé de se crasher.",
   "Selon la fédération, l'ordre venait du patron, Flavio Briatore. Lui nie, et porte plainte pour chantage. Renault ne conteste rien.",
   "Briatore est exclu. Mais un tribunal français annule la sanction, jugée irrégulière. En 2024, il revient dans la même écurie.",
   "Alonso garde sa victoire. Piquet ne courra plus jamais en Formule 1. Et Felipe Massa, en tête avant le crash, perdra le titre pour un point.",
   "Piquet : victime ou complice ? Réponds en un mot, et abonne-toi pour le prochain dossier. Pas banal, hein ?"],
  voix=[('2008', 'deux mille huit'), ('2024', 'deux mille vingt-quatre'), ('Formule 1', 'Formule Un'), ('Piquet', 'Piqué'),
        ('Briatore', 'Briatoré'), ('Felipe', 'Félipé')],
  affichage={'deux mille huit': '2008', 'deux mille vingt-quatre': '2024', 'formule un': 'Formule 1', 'piqué': 'Piquet',
             'briatoré': 'Briatore', 'félipé': 'Felipe', 'quinzième': '15e', 'deux tours': '2 tours', 'un an': '1 an',
             'un point': '1 point', 'un mot': '1 mot'},
  bandeaux=[dict(scene=1, duree=2.2, texte='SINGAPOUR - SEPTEMBRE 2008'), dict(scene=1, apres=2.4, duree=2.6, texte='1ER GRAND PRIX DE NUIT')],
  fun_fact=dict(scene=4, texte=['IL DEMANDAIT', 'LE NUMÉRO DU TOUR'], source=PIQUET),
  legende="Singapour 2008 : un pilote Renault s'écrase dans le mur… sur ordre, pour faire gagner son coéquipier Fernando Alonso. Un an plus tard, Nelson Piquet Jr balance tout à la fédération. Victime ou complice ?",
  hashtags=['#histoirevraie', '#f1', '#formule1', '#triche', '#insolite', '#HistoiresPasBanales'],
  hooks=["Renault a fait crasher son pilote. Exprès, pour faire gagner l'autre.",
         "Ce pilote s'est crashé exprès. Sur ordre de sa propre écurie.",
         "Il a mis sa Formule 1 dans le mur. C'était le plan.",
         "Un crash à pleine vitesse, commandé par radio.",
         "Pour gagner une course, Renault a sacrifié une voiture. Et un pilote.",
         "Choix : premier, titre-accusation dit tel quel puis le mobile en six mots."],
  choix=["Marc choisit le sujet 1 (Crashgate) le 11 novembre 2026, catégorie automobile insolite.",
         "Pat Symonds n'est pas nommé : pas de photo d'époque libre ; l'ordre est attribué à la fédération (« selon la fédération »), Briatore ayant toujours nié.",
         "Sanction de Briatore : « exclu », annulée en 2010 par le TGI de Paris pour irrégularité, sans jugement sur les faits. Ne pas dire « blanchi » ni « banni à vie ».",
         "Retour de Briatore : conseiller exécutif d'Alpine le 21 juin 2024, écurie d'Enstone, ex-Renault : « la même écurie ».",
         "Massa : « perdra le titre pour un point » est un fait (98-97) ; aucun lien de causalité affirmé. Procédure Massa en cours à Londres : non évoquée.",
         "Aucune image du crash : droits F1 ; la seule photo libre fait 438x678. Plans de course Pexels = illustrations, pas le Grand Prix 2008."],
  sources=[
   dict(fait='28 septembre 2008, Marina Bay, premier Grand Prix de nuit ; Alonso 15e sur la grille ; arrêt au tour 12', url=GP, note='Wikipedia en appoint, concordant avec la décision FIA'),
   dict(fait='Crash volontaire de Piquet Jr au virage 17, tour 14', url=WMSC, note='« At Turn 17 of Lap 14 [...] deliberately crashed »'),
   dict(fait='Virage le plus éloigné des engins de levage ; Piquet demande plusieurs fois le numéro du tour à la radio (fun fact)', url=PIQUET, note='Déclaration de Piquet à la FIA, 30 juillet 2009 ; commissaires : « furthest away from any of the safety or lifting equipment »'),
   dict(fait='Alonso gagne ; première victoire Renault depuis le Japon 2006', url='https://en.wikipedia.org/wiki/Renault_Formula_One_crash_controversy', note=''),
   dict(fait='Piquet écarté après la Hongrie 2009 puis déclaration sous serment à la FIA ; immunité', url=PIQUET, note='Écarté le 26 juillet, déclaration le 30 juillet, départ confirmé le 3 août 2009'),
   dict(fait='Ordre attribué à Briatore et Symonds ; Briatore nie ; plainte pour chantage (Renault et Briatore, 11 septembre 2009)', url='https://www.grandprix.com/news/renault-and-briatore-to-take-legal-action-against-piquets.html', note='Décision FIA : ' + WMSC),
   dict(fait='21 septembre 2009 : Renault ne conteste pas, exclusion avec sursis ; Briatore exclu pour une durée illimitée ; Alonso hors de cause', url=VERDICT, note=''),
   dict(fait='5 janvier 2010 : le TGI de Paris annule la sanction, jugée irrégulière ; 15 000 € à Briatore', url='https://www.autosport.com/f1/feature/2583/analysing-the-french-court-briatore-verdict', note='Le tribunal ne se prononce pas sur les faits'),
   dict(fait='Briatore conseiller exécutif d’Alpine le 21 juin 2024', url='https://racer.com/2024/06/21/briatore-returns-to-alpine-in-advisor-role/', note='Alpine = écurie d’Enstone, ex-Renault'),
   dict(fait='Résultat inchangé ; Piquet : aucun Grand Prix après la Hongrie 2009 ; Massa en pole et en tête avant le crash ; titre 2008 Hamilton 98, Massa 97', url='https://en.wikipedia.org/wiki/2008_Formula_One_World_Championship', note='Piège en commentaire : Massa a perdu ses points à Singapour sur l’incident du tuyau d’essence')]),
 36: dict(
  dossier='36-mclaren-trahie-par-une-photocopie', titre='McLaren trahie par une photocopie',
  titre_lignes=['McLAREN TRAHIE', 'PAR UNE', 'PHOTOCOPIE'], serie='F1 - SAISON 2007', musique='scandale',
  scenes=[
   "McLaren trahie par une photocopie. Et l'addition : cent millions de dollars.",
   "Formule 1, saison 2007. McLaren et Ferrari se battent pour le titre mondial.",
   "Un cadre de Ferrari refile en douce à l'ingénieur en chef de McLaren un dossier secret : sept cent quatre-vingts pages de données techniques.",
   "Pour tout mettre sur disque, selon Ferrari, la femme de l'ingénieur apporte le dossier dans une boutique de photocopie, en Angleterre.",
   "Mauvaise idée. L'employé comprend ce qu'il a entre les mains… et prévient Ferrari.",
   "Ferrari lui dédiera même une victoire, et l'invitera à l'usine.",
   "Perquisition chez l'ingénieur : le dossier est là. Et la fédération compte deux cent quatre-vingt-huit SMS entre les deux hommes.",
   "Le pire ? Des e-mails montrent que des pilotes McLaren parlaient de ces infos. Selon son patron, Fernando Alonso le menace même de tout révéler.",
   "Verdict : McLaren exclue du championnat des constructeurs, et cent millions de dollars d'amende. Un record.",
   "Et le titre des pilotes ? Ferrari, pour un point, devant Lewis Hamilton et Alonso.",
   "Cent millions : mérité ou exagéré ? Réponds en un mot, et abonne-toi pour le prochain dossier. Pas banal, hein ?"],
  voix=[('2007', 'deux mille sept'), ('Formule 1', 'Formule Un'), ('McLaren', 'Mac Larène'), ('SMS', 'S M S'),
        ('Lewis Hamilton', 'Louisse Amiltonne')],
  affichage={'deux mille sept': '2007', 'formule un': 'Formule 1', 'mac larène': 'McLaren', 's m s': 'SMS',
             'louisse amiltonne': 'Lewis Hamilton', 'cent millions de dollars': '100 millions de dollars',
             'cent millions': '100 millions', 'sept cent quatre-vingts pages': '780 pages',
             'deux cent quatre-vingt-huit': '288', 'un point': '1 point', 'un mot': '1 mot'},
  bandeaux=[dict(scene=1, duree=2.0, texte='FORMULE 1 - SAISON 2007'), dict(scene=1, apres=2.2, duree=2.4, texte='McLAREN CONTRE FERRARI')],
  fun_fact=dict(scene=5, texte=['FERRARI LUI DÉDIE', 'UNE VICTOIRE'], source='https://www.autosport.com/f1/news/ferrari-hail-photocopy-shop-employee-4413797/4413797/'),
  legende="2007 : 780 pages de secrets Ferrari atterrissent chez l'ingénieur en chef de McLaren. Tout s'effondre à cause d'une boutique de photocopie. Résultat : 100 millions de dollars d'amende. Mérité ou exagéré ?",
  hashtags=['#histoirevraie', '#f1', '#formule1', '#triche', '#insolite', '#HistoiresPasBanales'],
  hooks=["McLaren trahie par une photocopie. Et l'addition : cent millions de dollars.",
         "Cent millions de dollars d'amende. À cause d'une photocopie.",
         "Sept cent quatre-vingts pages volées à Ferrari. Et une boutique de photocopie.",
         "Le plus gros scandale de la F1 a été découvert par un employé de photocopie.",
         "Ils espionnaient Ferrari. Un inconnu les a dénoncés.",
         "Choix : premier, objet banal devenu arme et chiffre choc dans la même respiration."],
  choix=["Marc ajoute le sujet 2 (Spygate) le 11 novembre 2026 pendant la préparation du dossier 35.",
         "Mike Coughlan et Nigel Stepney ne sont pas nommés : aucune photo libre sur Commons (règle photo à chaque nom). Désignés par leur fonction.",
         "L'épisode de la boutique est attribué (« selon Ferrari ») : déclaration de l'avocat de Ferrari devant la Haute Cour le 10 juillet 2007. Ville non dite : sources divergentes (Woking, Walton-on-Thames).",
         "Employé anonyme : ni nom, ni « fan de Ferrari », ni e-mail, non confirmés. Pas de logo vu sur les pages.",
         "Menace d'Alonso attribuée à Ron Dennis (« selon son patron ») : audience FIA du 13 septembre 2007.",
         "« Un record » : amende record du sport automobile selon Autosport ; montant réellement payé environ 64,5 M$ après déduction des revenus perdus (hors narration).",
         "Mort de Stepney en 2014 et citation prêtée à Mosley non évoquées : hors sujet et source contestée.",
         "Plans de photocopieur, documents, disque et téléphone = illustrations Pexels, pas les objets de l'affaire."],
  sources=[
   dict(fait='Dossier d’environ 780 pages Ferrari saisi au domicile du chef designer de McLaren, perquisition du 3 juillet 2007', url='https://www.grandprix.com/news/the-fia-decision-in-full.html', note=''),
   dict(fait='Source des documents : cadre de Ferrari (Nigel Stepney), condamné en 2010 à 20 mois avec sursis après accord', url='https://www.grandprix.com/news/stepney-plea-bargain-ends-spy-case.html', note='Non nommé dans la vidéo'),
   dict(fait='La femme de l’ingénieur apporte le dossier dans une boutique de photocopie pour le transférer sur disques ; l’alerte vient de la boutique', url='https://www.autosport.com/f1/news/spy-case-court-hearing-adjourned-4411536/4411536/', note='Allégation de Ferrari devant la Haute Cour : « tip-off by the photocopying agency »'),
   dict(fait='Fun fact : Montezemolo dédie la victoire de Spa (16 septembre 2007) à l’employé puis l’invite au Mugello et à l’usine', url='https://www.autosport.com/f1/news/ferrari-hail-photocopy-shop-employee-4413797/4413797/', note='Invitation : https://www.autosport.com/f1/news/ferrari-invite-photocopy-shop-guy-to-italy-4418527/4418527/'),
   dict(fait='Au moins 288 SMS et 35 appels entre les deux hommes, du 11 mars au 3 juillet 2007', url=FIA07, note=''),
   dict(fait='E-mails entre Alonso et de la Rosa sur les informations Ferrari ; Alonso menace Dennis de les transmettre (Hongrie, 5 août 2007)', url='https://www.autosport.com/f1/news/transcript-highlights-dennis-alonso-row-4413734/4413734/', note='Récit de Ron Dennis à l’audience ; pilotes non sanctionnés (immunité)'),
   dict(fait='13 septembre 2007 : exclusion du championnat constructeurs et amende de 100 M$', url=FIA07, note='Payé : environ 64,5 M$ (jugement Upper Tribunal 2014). Piège en commentaire : « ils n’ont pas payé 100 millions »'),
   dict(fait='Championnat pilotes 2007 : Räikkönen (Ferrari) 110, Hamilton 109, Alonso 109', url='https://en.wikipedia.org/wiki/2007_Formula_One_World_Championship', note='Recoupé Sky Sports')]),
}

for n, x in D.items():
    p = Path('out') / x['dossier']
    (p / '_montage').mkdir(parents=True, exist_ok=True)
    voice = []
    for s in x['scenes']:
        for a, b in x['voix']:
            s = s.replace(a, b)
        voice.append(s)
    d = dict(numero=n, titre=x['titre'], titre_fixe=x['titre'].upper(), titre_lignes=x['titre_lignes'], serie=x['serie'], format='histoire',
             statut='script vérifié - production', hook=x['scenes'][0],
             scenes=[dict(narration=t, narration_voix=v, animate=False) for t, v in zip(x['scenes'], voice)],
             affichage=x['affichage'], bandeaux=x['bandeaux'], fun_fact=x['fun_fact'], legende=x['legende'], hashtags=x['hashtags'],
             **REF, musique=x['musique'], choix_editoriaux=x['choix'], sources_a_verifier=x['sources'])
    (p / 'histoire.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    (p / 'script.txt').write_text('\n\n'.join(x['scenes']) + '\n', encoding='utf8')
    (p / 'hooks.txt').write_text('\n'.join(x['hooks']) + '\n', encoding='utf8')
    print(n, 'mots :', len(' '.join(x['scenes']).replace(' ?', '').replace(' :', '').split()), '| scènes :', len(x['scenes']))
