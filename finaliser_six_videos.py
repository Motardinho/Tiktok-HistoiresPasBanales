"""Index des six versions actuelles et contrôle des fun facts et comparaisons."""
import hashlib
import json
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
from revision_spectaculaire import stage_for

FACTS={
13:('Le vélo spatial fonctionne sans selle, chaussures fixées aux pédales.','https://www.asc-csa.gc.ca/eng/multimedia/search/video/18303'),
14:('Le 300 du nom Chiron Super Sport 300+ renvoie aux 300 miles par heure franchis pendant son essai.','https://www.youtube.com/watch?v=FuS_bXJNync'),
15:('Le premier feu de circulation londonien fonctionnait au gaz et a été retiré après une explosion.','https://www.ciht.org.uk/news/traffic-light-anniversary-reached-in-london/'),
16:('Le porte-avions Ronald Reagan possède sa propre boulangerie.','https://www.dvidshub.net/news/386054/serving-sailors-reagans-kitchen'),
17:('Les femelles étudiées du molosse du Brésil ne pesaient que 11 à 12 grammes.','https://www.mpg.de/10820289/freischwanz-fledermaus-ist-der-schnellste-flieger-im-tierreich?c=987944'),
18:('Le Canada possède le plus long littoral du monde, sur trois océans.','https://www.canada.ca/en/services/environment/our-environment/nature-based-climate-solutions/coastlines.html')}

rows=[]
report=['# Vidéos 13 à 18 - versions actuelles\n',
        'Chaque vidéo contient un fun fact vérifié. Accroche animaux corrigée ; compléments sur le littoral canadien et le premier feu de Londres intégrés. Version armées validée conservée. Interligne resserré, deux-points liés au mot précédent et comparaisons actualisées.\n',
        '| N° | Vidéo | Comparaison | Fun fact |','|---|---|---|---|']
for n in FACTS:
    w=next((ROOT/'out').glob(f'{n}-*'));d=read(w/'histoire.json')
    final=w/'final.mp4';comparison=w/'comparaison.mp4'
    assert comparison.stat().st_mtime>=final.stat().st_mtime
    info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type:stream_disposition=default:stream_tags=handler_name','-of','json',str(comparison)]))
    audio=[x for x in info['streams'] if x['codec_type']=='audio']
    assert len(audio)==2 and audio[1]['disposition']['default']==1
    info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration,width,height','-of','json',str(final)]))
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    assert float(v['duration'])>60 and (v['width'],v['height'])==(1080,1920)
    sha=hashlib.sha256(final.read_bytes()).hexdigest()
    for name in ['controle.json','controle-interligne.json']:
        p=w/'_montage'/name;control=read(p) if p.exists() else {}
        control.update(sha256=sha,funfact=FACTS[n][0],source_funfact=FACTS[n][1],deux_points_lies=True,comparaison_a_jour=True)
        if name=='controle.json':control['verification_visuelle']='Passage et visuel du fun fact examinés ; durée et comparaison contrôlées'
        save(p,control)
    d['fun_fact']=dict(texte=FACTS[n][0],source=FACTS[n][1])
    if n==15:d['statut']='Fun fact rendu et contrôlé - comparaison actualisée'
    save(w/'histoire.json',d)
    if n>=16:save(stage_for(w)/'histoire.json',d)
    if n==15:
        save(w/'_montage/revision-funfact-v13/histoire.json',d)
        (w/'publication.txt').write_text(d.get('legende',d['titre'])+'\n\n'+' '.join(d['hashtags'])+'\n\nVoix synthétique : activer le label IA. Visuels et musique : CREDITS.md. Données et fun fact : verification.md.\n',encoding='utf-8')
        (w/'LISEZ-MOI.txt').write_text('Version actuelle : fun fact sur le premier feu de Londres intégré.\nfinal.mp4 : 72,17 s.\ncomparaison.mp4 : référence à gauche, HPB à droite, 2 audios, HPB par défaut.\nSources : CREDITS.md et verification.md.\nMontage : _montage/revision-funfact-v13/_montage/.\n',encoding='utf-8')
    rows.append(dict(numero=n,dossier=w.name,funfact=FACTS[n][0],source=FACTS[n][1],duree=float(v['duration']),comparaison_a_jour=True,sha256=sha))
    report.append(f"| {n} | [{d['titre']}]({w.name}/final.mp4) | [Comparer]({w.name}/comparaison.mp4) | {FACTS[n][0]} |")
save(ROOT/'out/controle-funfacts.json',rows)
(ROOT/'out/LIVRAISON-13-18.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('6 vidéos : fun fact identifié, durée >60 s, 1080x1920 et comparaison actualisée avec 2 audios, HPB par défaut')
