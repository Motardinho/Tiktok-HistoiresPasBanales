"""Livraison des trois versions photographiques avec leurs comparaisons."""
import hashlib
import html
import json
import re
import shutil
from PIL import Image,ImageDraw
from montage_reel import ROOT,run
from produire_lot_16_18 import FOLDERS,read,save
from revision_spectaculaire import stage_for,PHOTOS
from narrateur.validation import validate_duration

def clean(s):return html.unescape(re.sub('<[^>]*>','',s or '')).strip().replace('\n',' ')

def finalize():
    all_photos=read(PHOTOS/'sources.json');all_clips=read(ROOT/'assets/lot-16-18/sources-visuelles.json');rows=[]
    for w in FOLDERS:
        d=read(w/'histoire.json');n=d['numero'];assert d['revision'].startswith('spectaculaire-')
        stage=stage_for(w);m=stage/'_montage';t=read(m/'timings.json');edits=read(m/'montage.json')
        assert all(e['source'].startswith(('photo:','clip:')) for e in edits)
        assert d['scenes'][0]['rang'] is None and d['scenes'][1]['rang']==3
        duration=validate_duration(w/'final.mp4')
        assert abs(duration-t['duration'])<.2
        assert (w/'comparaison.mp4').stat().st_mtime>=(w/'final.mp4').stat().st_mtime
        info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration,width,height:stream_disposition=default:stream_tags=handler_name','-of','json',str(w/'comparaison.mp4')]))
        audio=[s for s in info['streams'] if s['codec_type']=='audio'];assert len(audio)==2 and audio[1]['disposition']['default']==1
        clips={e['source'].split(':')[1] for e in edits if e['source'].startswith('clip:')}
        photos={e['source'].split(':')[1] for e in edits if e['source'].startswith('photo:')}
        sources=[x for x in all_clips if x['slug'] in clips]+[x for x in all_photos if x['slug'] in photos]
        assert len(sources)==len(clips)+len(photos)
        save(m/'sources-visuelles.json',sources);save(w/'_montage/sources-visuelles.json',sources)
        credits=f'# Crédits - vidéo {n} - révision spectaculaire\n\nPhotographies réelles et extraits vidéo. Modifications : recadrages portrait, mouvements lents sur les photos, extraits, montage, mentions et sous-titres. Aucune image de la vidéo de référence dans le montage final. Les illustrations ne sont pas des prises de mesure des performances citées.\n\n'
        attribution=[]
        for source in sources:
            title=source.get('title','ABoVE Summer 2022 B-Roll');artist=clean(source.get('artist'));lic=source['license'];url=source['page'];license_url=source.get('license_url')
            credits+=f"## {source['file']}\n\n{artist} - {title}\n\n[Source]({url}) - {lic}"
            if license_url:credits+=f' - [Licence]({license_url})'
            credits+='\n\nExtrait ou photographie recadrée et montée ; photo animée par déplacement/zoom.\n\n'
            attribution.append(f'{artist} - {title} - {lic} - {url}'+(f' - {license_url}' if license_url else '')+' - Recadrage et montage.')
        if any('SA' in x['license'] for x in sources):credits+='Les adaptations des éléments sous CC BY-SA sont fournies sous [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Conserver les attributions, les liens et la mention des modifications avec la diffusion. La musique et les autres éléments tiers conservent leurs licences propres.\n\n'
        track=d['musique'];credits+=f"Musique : {track['title']} - {track['artist']} - [Source]({track['page']}) - [Licence Mixkit]({track['license_url']}).\n\nVoix : Hugo, ElevenLabs {t['model']}, nouvelle narration avec alignement réel.\n"
        (w/'CREDITS.md').write_text(credits,encoding='utf-8')
        publication=d['legende']+'\n\n'+' '.join(d['hashtags'])+'\n\nActiver le label IA pour la voix synthétique.\nSources : verification.md.\n\nCrédits des visuels, à conserver avec la diffusion :\n'+'\n'.join(attribution)
        if any('SA' in x['license'] for x in sources):publication+='\nAdaptations visuelles concernées : CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/ .'
        publication+=f"\nMusique : {track['title']} - {track['artist']} - Mixkit.\n"
        (w/'publication.txt').write_text(publication,encoding='utf-8')
        (w/'voix-texte.txt').write_text('\n\n'.join(s['narration_voix'] for s in d['scenes']),encoding='utf-8')
        (w/'verification.md').write_text('# Vérification - révision photographique\n\nSources contrôlées le 8 novembre 2026.\n\n'+'\n\n'.join('- '+s for s in d['sources_a_verifier'])+'\n\n'+d['critere']+'\n\nLe podium conventionnel est celui de Global Firepower 2026 ; les dépenses militaires sont celles de 2025 selon SIPRI ; le nucléaire est vérifié séparément auprès de FAS et ne détermine pas ce podium. Les archives et les photos illustrent les pays et les espèces ; elles ne sont pas datées comme prises de vue de ces mesures.\n',encoding='utf-8')
        (w/'montage.md').write_text('# Montage actuel - spectaculaire avec teasing\n\nPremière image : accroche générique, aucun nom, rang ou chiffre de performance. Décompte ensuite 3, 2, 1 ; nom et image du n°1 à son entrée. Photos et archives plein écran, mentions courtes sur les images. Aucun panneau, quadrillage, tableau, carte ou schéma.\n\n'+ '\n\n'.join(f"Scène {i+1} - {s['narration']}" for i,s in enumerate(d['scenes']))+'\n',encoding='utf-8')
        d['statut']='Révision spectaculaire terminée - vidéo et comparaison vérifiées';save(w/'histoire.json',d);save(stage/'histoire.json',d)
        (w/'LISEZ-MOI.txt').write_text(f"VIDÉO {n} - VERSION PHOTOGRAPHIQUE AVEC TEASING\n\nfinal.mp4 : {duration:.2f} s, 1080x1920, 30 images/s.\ncomparaison.mp4 : référence à gauche, HPB à droite, 2 audios nommés ; HPB par défaut.\nPremière image sans nom ni rang : l’accroche précède le n°3.\nSources et licences : CREDITS.md et verification.md.\nLégende et attributions : publication.txt.\nSources actuelles : {stage.relative_to(w).as_posix()}/_montage/.\nL’ancienne version est conservée dans _montage/avant-revision-spectaculaire/.\n",encoding='utf-8')
        # Planche de contrôle : accroche, chaque entrée et mentions photographiques.
        ends=[];cursor=0
        for duration_scene in t['scene_durations']:
            ends.append(cursor);cursor+=duration_scene
        times=[1,ends[1]+1,ends[2]+2,ends[3]+2,ends[4]+2,ends[5]+2,ends[6]+2,ends[-1]+1]
        canvas=Image.new('RGB',(1080,1040),'#12151C')
        for j,at in enumerate(times):
            pic=m/f'controle-{j:02d}.png';run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(w/'final.mp4'),'-vf','scale=270:480','-frames:v','1',str(pic)])
            canvas.paste(Image.open(pic),((j%4)*270,(j//4)*520));ImageDraw.Draw(canvas).text(((j%4)*270+6,(j//4)*520+484),f'{at:.1f} s',fill='white')
        canvas.save(w/'_montage/planche-controle.png')
        run(['ffmpeg','-v','error','-y','-ss','1','-i',str(w/'final.mp4'),'-frames:v','1',str(w/'apercu.png')])
        control=read(w/'_montage/controle.json');control.update(verification_visuelle='Planches contrôlées',accroche_sans_revelation=True,tableaux=False,cartes=False,schemas=False,photos_et_archives=True,sha256=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest());save(w/'_montage/controle.json',control)
        rows.append(dict(numero=n,dossier=w.name,titre=d['titre'],duree=duration,sha256=control['sha256']))
        print(n,'livraison photographique',round(duration,2),'s',flush=True)
    save(ROOT/'out/controle-lot-16-18.json',rows)
    report='# Livraisons - vidéos 16 à 18 - révision spectaculaire\n\nPhotos et archives plein écran, nouvelles narrations Hugo, mentions courtes superposées. Première image sans révélation, puis décompte 3 - 2 - 1 et relance avant le n°1. Aucun tableau, fond quadrillé, schéma ou carte. Exports 1080x1920 à 30 images/s, décodés intégralement ; deux pistes audio distinctes dans les comparaisons, HPB par défaut.\n\n| N° | Vidéo | Durée | Comparaison |\n|---|---|---|---|\n'
    for row in rows:report+=f"| {row['numero']} | [{row['titre']}]({row['dossier']}/final.mp4) | {row['duree']:.1f} s | [Comparer]({row['dossier']}/comparaison.mp4) |\n"
    report+='\nLes anciennes versions sont conservées dans les sous-dossiers de montage. Aucune publication effectuée.\n';(ROOT/'out/LIVRAISON-16-18.md').write_text(report,encoding='utf-8')

if __name__=='__main__':finalize()
