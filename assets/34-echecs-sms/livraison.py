import json,hashlib,subprocess
from datetime import datetime,timezone,timedelta
from pathlib import Path
p=Path('out/34-il-trichait-aux-echecs');m=p/'_montage';a=Path('assets/34-echecs-sms')
d=json.loads((p/'histoire.json').read_text(encoding='utf8'))
stamp=datetime.now(timezone(timedelta(hours=1))).isoformat()
plans=json.loads((m/'plans.json').read_text(encoding='utf8'))
source_lines=[]
for x in d['sources_a_verifier']:source_lines.append(f"- {x['fait']} : {x['url']} ({x.get('note','')})")
credits=[]
for src in dict.fromkeys(x['source'] for x in plans):
 stem=Path(src).stem
 if stem.startswith('pexels-'):
  j=a/(stem+'.json')
  info=json.loads(j.read_text(encoding='utf8')) if j.exists() else {}
  credits.append(f"- {info.get('auteur','Pexels')} : {info.get('source','https://www.pexels.com/video/'+stem[7:]+'/')} - licence Pexels https://www.pexels.com/license/ - extrait recadré, sans son original.")
credits.extend([
 '- Portrait Sébastien Feller en 2017 : Stefan64, https://commons.wikimedia.org/wiki/File:SebastienFeller17.jpg - CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/ ; recadrage et léger mouvement. Adaptation du portrait sous la même licence.',
 '- Carte : données Natural Earth, domaine public, https://www.naturalearthdata.com/about/terms-of-use/ ; animation HPB originale réalisée en Python. Nancy 48.6921 N, 6.1844 E ; Khanty-Mansiïsk 61.0042 N, 69.0189 E. Trajet narratif, pas routage télécom réel.',
 '- Musique : Greed - Arulo / Mixkit, https://mixkit.co/free-stock-music/tag/crime/ ; licence https://mixkit.co/license/modal/musicFree/ .',
 '- Voix synthétique ElevenLabs, prise initiale conservée ; deux phrases retirées par montage dans les pauses, débit inchangé. Deux bips de transmission originaux et une pause musicale avant la révélation.',
])
intro=d['legende']+'\n\n'+' '.join(d['hashtags'])
disclosure="Images d’illustration contemporaines : les séquences de jeu, de clavier et de téléphone ne montrent ni les parties de 2010 ni les messages ou appareils utilisés dans l’affaire. Seul le portrait identifié est celui de Sébastien Feller (photo 2017). Carte animée illustrative."
compact_sources='\n'.join(dict.fromkeys(x['url'] for x in d['sources_a_verifier']))
compact_clips=[]
for src in dict.fromkeys(x['source'] for x in plans):
 stem=Path(src).stem
 if stem.startswith('pexels-'):
  j=a/(stem+'.json');info=json.loads(j.read_text(encoding='utf8')) if j.exists() else {}
  compact_clips.append(info.get('auteur','Pexels').strip()+' : https://www.pexels.com/video/'+stem[7:]+'/')
publication=intro+'\n\n'+disclosure+'\n\nSources :\n'+compact_sources+'\n\nVidéos Pexels, recadrées, licence https://www.pexels.com/license/ :\n'+'\n'.join(compact_clips)+'\n\nPortrait : Stefan64, Sébastien Feller (2017), recadré. https://commons.wikimedia.org/wiki/File:SebastienFeller17.jpg - CC BY-SA 4.0 : https://creativecommons.org/licenses/by-sa/4.0/ (adaptation sous même licence).\nCarte : Natural Earth, domaine public ; animation HPB. Musique : Greed - Arulo / Mixkit, https://mixkit.co/license/modal/musicFree/ . Voix synthétique ElevenLabs.\n'
assert len(publication)<4000,len(publication)
(p/'legende.txt').write_text(publication,encoding='utf8');(p/'publication.txt').write_text(publication,encoding='utf8')
(p/'CREDITS.md').write_text('# Sources et crédits - dossier 34\n\n'+disclosure+'\n\n'+'\n'.join(source_lines)+'\n\n'+'\n'.join(credits)+'\n',encoding='utf8')
(p/'script.txt').write_text('\n\n'.join(x['narration'] for x in d['scenes'])+'\n',encoding='utf8')
export=json.loads((m/'controle-export.json').read_text(encoding='utf8'))
comparison=json.loads((m/'controle-comparaison.json').read_text(encoding='utf8'))
assert (p/'comparaison.mp4').stat().st_mtime >= (p/'final.mp4').stat().st_mtime
report=dict(date=stamp,statut='export de travail - contrôle audio et visionnage continu restant à effectuer',validation_utilisateur=False,
 sources_examinees=['Décision FIDE 2/2011, pages 17-25, faits, aveux, SMS, sanctions','RTL Infos du 28 mai 2019, condamnation avec sursis ; erreur de l’article sur la victoire de la compétition écartée','L’Est Républicain du 20 mai 2011 : complice à Nancy','Page Commons du portrait : auteur, date et licence'],
 montage_audio=dict(duree_initiale=72.64,duree_finale=68.5,coupes_originales=[[12.06,13.98],[34.12,36.34]],raison='Transitions retirées pour tenir 61-70 s ; quota ElevenLabs insuffisant pour seconde synthèse'),
 preuves_visuelles=[],
 observations=['Titre repris à l’oral 0-1.64 s, phrase-hameçon finie à 3.60 s (alignement de la synthèse). Deux plans avant 4.08 s.','Portrait réel sur le nom Sébastien Feller à 9.80 s, date de photo 2017 affichée.','Animation Nancy-Russie 17.48-21.28 s, bips de départ et arrivée.','Numéros de téléphone codés : fun fact 21.28-27.24 s.','Illustrations contemporaines documentées dans les crédits ; aucune photo d’un figurant présentée comme un protagoniste.','Recherche YouTube filtrée CC conservée ; trois résultats hors sujet, aucun extrait réutilisé.','Portrait de 2008 écarté : définition utile insuffisante ; portrait 2017 retenu.'],
 limites=['Aucune écoute humaine/aurale réalisée par l’agent : prononciation, qualité des coupes et balance musique/bips restent à écouter.','Contrôle visuel par captures : pas de visionnage continu de la vidéo réalisé.','Les gestes exacts du capitaine et le véritable SMS ne sont pas filmés dans les sources retenues.','Les smartphones des illustrations sont contemporains, pas ceux de 2010.'],technique=export,comparaison=comparison)
existing=p/'controle-livraison.json'
if existing.exists():
 prev=json.loads(existing.read_text(encoding='utf8'));report['preuves_visuelles']=prev.get('preuves_visuelles',[])
existing.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
d['statut']='export de travail - écoute et visionnage continu requis'
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
idx=Path('out/versions-actuelles.json');data=json.loads(idx.read_text(encoding='utf8'));data=[x for x in data if x.get('numero')!=34];data.append(dict(numero=34,dossier=p.name,duree=export['duree_video'],sha256=export['sha256'],comparaison_a_jour=True,statut='a_visionner',revision=stamp+' : nouvelle vidéo échecs, animation France-Russie demandée par Marc',apercu_simule='apercu-tiktok.jpg'));idx.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Livraison enregistrée',stamp)
