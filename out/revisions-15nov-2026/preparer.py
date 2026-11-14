from pathlib import Path
import json,sys,shutil,subprocess,re
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from produire_lot_16_18 import speech

def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for n in [31,33]:
 d=OUT/str(n);d.mkdir(exist_ok=True)
 src=next((ROOT/'out').glob(f'{n}-*'))
 story=json.loads((src/'histoire.json').read_text(encoding='utf-8'))
 story.update(statut='revision_locale_a_valider',bandeaux=[],comparaison_reference=str(src/'version-validee/final.mp4'))
 if n==31:
  story['scenes']=story['scenes'][1:]
  story['tiktokabilite']={'verdict':'adapté sous réserve','limite':'Aucune image du braquage : interviews de Paul, archives de Mathias et du procès. Photo originale effectivement citée pour août 2025.'}
  story['sources_a_verifier'].append({'fait':'Photo originale publiée le 19 août 2025, vérifiée sur le compte de Paul','url':'https://www.instagram.com/p/DNi-H1GCTmx/'})
 else:
  texts=[
   "Cent quarante-neuf buts contre leur propre camp. Exprès. Ce n'est pas une faute de frappe.",
   "Madagascar, octobre deux mille deux. Phase finale du championnat national. Un penalty contesté prive l'Émirne de ses chances de titre.",
   "Les images de l'Adéma que tu vois datent de deux mille dix-huit. Pour le match de deux mille deux, on s'appuie sur les documents.",
   "Le match suivant, face à l'Adéma déjà champion, tourne à la protestation. Les joueurs de l'Émirne tirent dans leur propre but. Engagement. Et ils recommencent.",
   "En face, les adversaires regardent. Au bout des quatre-vingt-dix minutes, cent quarante-neuf à zéro. Ça fait, en moyenne, un but toutes les trente-six secondes.",
   "Le pire ? Selon la presse de l'époque, des spectateurs demandent le remboursement de leur billet. Ils étaient venus voir un match, pas ça.",
   "La fédération sanctionne : trois ans de suspension pour le coach. Quatre joueurs suspendus aussi. L'arbitre, lui, n'est pas sanctionné.",
   "Le score entre au Guinness. Mais ce record, ils l'ont obtenu en sabotant leur propre match.",
   "Alors, protestation géniale ou honte du football ? Réponds en un mot, et abonne-toi pour le prochain dossier. Pas banal, hein ?"
  ]
  story['scenes']=[{'narration':t,'narration_voix':t,'visuel':'Documents sourcés et séquences Adema 2018 clairement distinguées du match de 2002.'} for t in texts]
  story['affichage'].update({'cent quarante-neuf':'149','deux mille dix-huit':'2018','quatre-vingt-dix minutes':'90 minutes','quatre joueurs':'4 joueurs'})
  story['type_post']='videos_documentaire_sourcee'
  story['tiktokabilite']={'verdict':'adapté sous réserve','limite':'Aucune archive authentifiée du match 2002 retrouvée. Exception documentaire expressément choisie par Marc. Club filmé en 2018, annoncé à la voix et dans les sous-titres avant les images.'}
 save(d/'histoire.json',story)
 (d/'script.txt').write_text('\n\n'.join(s['narration'] for s in story['scenes']),encoding='utf-8')
 shutil.copy2(src/'_montage/police.ttf',d/'police.ttf')
 shutil.copy2(ROOT/'out/revisions-fluidite-14nov-2026/27/logo.png',d/'logo.png')
 if n==33:speech(d)
