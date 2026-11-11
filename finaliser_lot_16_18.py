"""Contrôles techniques et documentation de livraison du lot 16-18."""
import hashlib
import html
import json
import re
from pathlib import Path

from montage_reel import ROOT,run
from produire_lot_16_18 import FOLDERS,read,save
from narrateur.validation import validate_duration

def clean(value):return html.unescape(re.sub('<[^>]*>','',value or '')).strip().replace('\n',' ')

def main():
    if any(read(w/'histoire.json').get('revision','').startswith('spectaculaire') for w in FOLDERS):
        from finaliser_revision_spectaculaire import finalize
        return finalize()
    source_folder=ROOT/'assets/lot-16-18';sources=read(source_folder/'sources-visuelles.json')
    music_sources=read(ROOT/'assets/musique/mixkit/sources.json')
    results=[]
    for w in FOLDERS:
        comparison=w/'comparaison.mp4'
        if not comparison.exists() or comparison.stat().st_mtime < (w/'final.mp4').stat().st_mtime:
            from comparer_lot_16_18 import compare
            compare(w)
        m=w/'_montage';d=read(w/'histoire.json');t=read(m/'timings.json');edits=read(m/'montage.json')
        duration=validate_duration(w/'final.mp4')
        info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,duration,r_frame_rate:format=duration','-of','json',str(w/'final.mp4')]))
        v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
        assert (v['width'],v['height'])==(1080,1920)
        assert abs(float(v['duration'])-float(a['duration']))<.2
        assert abs(sum(t['scene_durations'])-duration)<.2
        assert abs(sum(e['duration'] for e in edits)-duration)<.2
        assert t['words'][-1]['end']<=duration+.1
        assert all(x['start']<=x['end'] for x in t['words'])
        assert all(x['start']<=y['start']+.02 for x,y in zip(t['words'],t['words'][1:]))
        script=' '.join(s['narration'] for s in d['scenes'])
        assert script.endswith('Pas banal, hein ?') and 'Dossier clos' not in script
        used={e['source'] for e in edits if not e['source'].startswith('graphic:')}
        selected=[s for s in sources if s['slug'] in used]
        save(m/'sources-visuelles.json',selected)
        credits=f"# Crédits - vidéo {d['numero']}\n\nSéquences réelles sélectionnées et recadrées en portrait, assemblées avec narration, sous-titres, musique et graphiques originaux. Son des archives retiré. Les scènes ne prétendent pas filmer les mesures citées.\n\n"
        for s in selected:
            credits+=f"## {s['file']}\n\n{clean(s.get('artist'))} - {s['title'] if 'title' in s else 'ABoVE Summer 2022 B-Roll'}\n\n[Source]({s['page']}) - {s['license']}"
            if s.get('license_url'):credits+=f" - [Licence]({s['license_url']})"
            credits+='\n\nModifications : extraits, recadrage vertical, montage et habillage.\n\n'
        credits+='Cartes et schémas : création originale Histoires pas banales. Données cartographiques [Natural Earth](https://www.naturalearthdata.com/about/terms-of-use/), domaine public ; projection cylindrique équivalente, parallèle standard 45°, comparaison Canada/Russie à échelle identique. La péninsule de Crimée n’est pas coloriée comme russe.\n\n' if d['numero']==18 else 'Graphiques et schémas : création originale Histoires pas banales.\n\n'
        if d['numero']==17:
            credits+='Les adaptations des extraits de Pi3.124 et Paul Hurtado sont proposées sous [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), avec attribution et indication des modifications. Les éléments tiers, notamment la musique, conservent leurs licences propres. Conserver ces attributions et la mention de partage à l’identique avec la diffusion.\n\n'
        track=d['musique'];credits+=f"Musique : {track['title']} - {track['artist']} - [Source]({track['page']}) - [Mixkit Stock Music Free License]({track['license_url']}). Mixage avec atténuation sous la parole.\n\nVoix : Hugo, ElevenLabs, modèle {t['model']}.\n"
        (w/'CREDITS.md').write_text(credits,encoding='utf-8')
        hashtags=d['hashtags']
        if '#histoirevraie' not in hashtags:hashtags=['#histoirevraie']+hashtags
        d.update(hashtags=hashtags,statut='Export terminé - contrôles techniques et planches visuelles vérifiés')
        save(w/'histoire.json',d)
        publication=d['legende']+'\n\n'+' '.join(hashtags)+'\n\n'
        publication+='Voix synthétique : activer le label IA lors de la publication.\nSources factuelles : verification.md.\n\nCrédits visuels à conserver :\n'
        for s in selected:
            publication+=f"{clean(s.get('artist'))} - {s.get('title','ABoVE Summer 2022 B-Roll')} - {s['license']} - {s['page']}"
            if s.get('license_url'):publication+=' - '+s['license_url']
            publication+=' - Extraits recadrés et montés.\n'
        if d['numero']==17:publication+='Adaptations des extraits Pi3.124 et Paul Hurtado : CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/ .\n'
        publication+=f"Musique : {track['title']} - {track['artist']} - Mixkit.\n"
        (w/'publication.txt').write_text(publication,encoding='utf-8')
        (w/'LISEZ-MOI.txt').write_text(f"VIDÉO {d['numero']} - {d['titre']}\n\nfinal.mp4 : export 1080x1920, 30 images/s, {duration:.2f} secondes.\ncomparaison.mp4 : référence à gauche, HPB à droite, deux audios séparés ; HPB par défaut.\npublication.txt : légende, hashtags, mention IA et attributions.\nCREDITS.md : provenance et licences des visuels et de la musique.\nverification.md : sources des faits.\n_montage : voix, timings réels, sous-titres, plans et mixage.\n\nLes schémas sont explicatifs, les archives ne sont pas des mesures filmées.\nAucune publication ni programmation TikTok effectuée.\n",encoding='utf-8')
        digest=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest()
        control=read(m/'controle.json');control.update(verification_visuelle='Planches des scènes inspectées, zones de texte corrigées',sha256=digest,largeur=1080,hauteur=1920,fps=v['r_frame_rate'],duree_video=float(v['duration']),duree_audio=float(a['duration']))
        save(m/'controle.json',control)
        results.append(dict(numero=d['numero'],dossier=w.name,titre=d['titre'],duree=duration,sha256=digest))
        print(d['numero'],duration,'s - validé',flush=True)
    save(ROOT/'out/controle-lot-16-18.json',results)
    content='# Livraisons - vidéos 16 à 18\n\nExports verticaux 1080x1920, 30 images/s. Voix Hugo, timings réels ElevenLabs, trois musiques Mixkit distinctes et habillage HPB. Décodage intégral et durées contrôlés ; planches des scènes inspectées. Pas de publication effectuée.\n\n| N° | Sujet | Durée | Vidéo | Comparaison | Crédits |\n|---|---|---|---|---|---|\n'
    for r in results:
        comparison=f"[Comparer]({r['dossier']}/comparaison.mp4)" if (ROOT/'out'/r['dossier']/'comparaison.mp4').exists() else 'À produire'
        content+=f"| {r['numero']} | {r['titre']} | {r['duree']:.1f} s | [Ouvrir]({r['dossier']}/final.mp4) | {comparison} | [Crédits]({r['dossier']}/CREDITS.md) |\n"
    content+='\nComparaisons locales : référence à gauche, HPB à droite ; deux pistes audio séparées, HPB par défaut. Image figée et silence après la fin de la version la plus courte.\n'
    content+='\nLes textes de publication se trouvent dans chaque dossier. Le dossier 17 présente trois performances sélectionnées ; il ne prétend pas être le podium absolu de tous les animaux. Les archives militaires sont des illustrations des pays, pas la preuve de leurs inventaires actuels.\n'
    (ROOT/'out/LIVRAISON-16-18.md').write_text(content,encoding='utf-8')

if __name__=='__main__':main()
