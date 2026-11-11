import json,hashlib,subprocess
from pathlib import Path
from securiser_habillage_tiktok import CARD
root=Path.cwd();out=root/'out'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
versions=[];audit=read(out/'controle-funfacts.json')
for n in range(13,19):
 w=next(out.glob(f'{n}-*'));m=w/'_montage';safe=m/'tiktok-safe';file=w/'final.mp4'
 streams=read(safe/'controle.json');sha=hashlib.sha256(file.read_bytes()).hexdigest();assert streams['sha256']==sha
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(file)]));dur={s['codec_type']:float(s['duration']) for s in probe['streams'] if s['codec_type'] in ('video','audio')}
 assert dur['video']>60 and abs(dur['video']-dur['audio'])<.3
 assert (w/'comparaison.mp4').stat().st_mtime>=file.stat().st_mtime
 d=read(w/'histoire.json')
 debut={13:2.107,14:2.96,15:2.6666666667,16:2.6666666667,17:3.04,18:4.007}[n]
 debut=d.get('correction_locale',{}).get('fin_annonce_titre',debut)
 if n==14:debut=max(4.8,debut)
 d.update(debut_sous_titres_secondes=debut,ouverture='Titre sans transcription redondante ; sous-titres à la première information suivante, synchronisés avec la voix.');save(w/'histoire.json',d)
 d.setdefault('habillage_tiktok',{}).update(titre_ancrage_bas=True,titre_bas=1370,sous_titres_ancrage_bas=True,sous_titres_position=[480,1370],sources_dans_legende=True);save(w/'histoire.json',d)
 if n>=14:d['fun_fact_affichage']['texte']=CARD[n];save(w/'histoire.json',d)
 c=read(m/'controle.json') if (m/'controle.json').exists() else {}
 c.update(sha256=sha,duration_mp4=dur['video'],comparaison_a_jour=True,decodage_integral=True,zone_texte=[90,250,880,1380],contour_titres_pixels=6,contour_funfacts_pixels=3,verification_visuelle='Hook, fun fact et fin contrôlés avec simulation du lecteur ; interface réelle variable.',apercu_simule='apercu-tiktok.jpg')
 c['sous_titres_debut_secondes']=debut
 c['sous_titres_position_fixe']=[480,1370]
 c['sous_titres_alignement']='an2'
 c['titre_bas_pixels']=read(safe/'titre-hook-layout.json')['ancrage_bas']
 assert c['titre_bas_pixels']==1370
 c['titre_oral_verifie']=read(m/'controle-titre-oral.json')['conforme']
 c['controle_collisions_ass']=not bool(read(safe/'controle-collisions.json')['risques'])
 save(m/'controle.json',c);streams['controle_visuel']=c['verification_visuelle'];save(safe/'controle.json',streams)
 if n>=14:
  f=d['fun_fact_affichage'];save(m/'controle-funfact-visible.json',dict(numero=n,debut=f['debut'],fin=f['fin'],texte=f['texte'],sha256=sha,comparaison_a_jour=True))
 for a in audit:
  if a['numero']==n:a.update(sha256=sha,duree=dur['video'],comparaison_a_jour=True)
 versions.append(dict(numero=n,dossier=w.name,duree=dur['video'],sha256=sha,comparaison_a_jour=True,apercu_simule='apercu-tiktok.jpg'))
 if (w/'validation-utilisateur.json').exists():versions[-1].update(statut='validee',validation=read(w/'validation-utilisateur.json'))
save(out/'versions-actuelles.json',versions);save(out/'controle-funfacts.json',audit)
rows=['# Vidéos 13 à 18 — versions actuelles','','Titres et sous-titres ancrés en bas sur les six vidéos ; titres annoncés à l’oral. Sources et crédits préparés dans les légendes en texte. Montage animaux entièrement en vidéo, accroche en course de guépard. Bandeaux plus descriptifs ; bandeau « MESURER LA MASSE » supprimé pour dégager les sous-titres des astronautes. Mention « HISTOIRES PAS BANALES » retirée. Titres et fun facts : contour sombre, accents détachés et interligne compact. Habillage déplacé dans la zone centrale pour dégager la recherche, la légende et les commandes TikTok. Les aperçus du lecteur sont des simulations ; son interface varie selon l’appareil et la longueur de la légende.','','Les comparaisons avec les références sont à jour. [Passages des fun facts](FUNFACTS-TOP.md).','','| N° | Vidéo | Comparaison | Aperçu simulé | Légende |','|---|---|---|---|---|']
for v in versions:
 w=out/v['dossier'];title=read(w/'histoire.json').get('titre_fixe',read(w/'histoire.json').get('titre',w.name))
 def link(name,label):return f'[{label}](</{(w/name).as_posix()}>)'
 statut=' — Validée' if v.get('statut')=='validee' else ''
 rows.append(f"| {v['numero']}{statut} | {link('final.mp4',title)} | {link('comparaison.mp4','Comparer')} | {link('apercu-tiktok.jpg','Voir')} | {link('legende.txt','Texte')} |")
(out/'LIVRAISON-13-18.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
print('Six vidéos et comparaisons vérifiées, index et contrôles actualisés')
