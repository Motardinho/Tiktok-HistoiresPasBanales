"""Resserre les titres des six exports et reconstruit leurs comparaisons."""
import argparse
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
from habillage_reference import hook_layer
from revision_spectaculaire import TITLES,stage_for
from comparer_lot_16_18 import compare
from narrateur.validation import validate_duration

LEGACY={13:['SE PESER','DANS',"L'ESPACE"],14:['TOP 3','DES VOITURES','LES PLUS RAPIDES','2026'],15:['TOP 3','JUSQU’À 102 H','DANS LES BOUCHONS','2026']}
LEGACY_SLUG={13:'astronautes-sport-en-orbite',14:'trois-records-voitures-vitesse',15:'villes-plus-lentes-tomtom-2024'}

def revise(w,source_override=None,intro_override=None,replace_duration=4):
    number=int(w.name[:2]);d=read(w/'histoire.json');root_m=w/'_montage'
    m=(stage_for(w)/'_montage' if number>=16 else root_m/('revision-donnees-2025-v14/_montage' if d.get('revision')=='donnees-2025-v14' else 'revision-funfact-v13/_montage') if number==15 else root_m)
    archive=root_m/'avant-interligne-visible-8px';archive.mkdir(exist_ok=True)
    for name in ['final.mp4','comparaison.mp4']:
        if not (archive/name).exists():shutil.copy2(w/name,archive/name)
    if not (archive/'titre-hook-reference.png').exists():shutil.copy2(m/'titre-hook-reference.png',archive/'titre-hook-reference.png')
    hook_layer(m,dict(title=LEGACY[number] if number<16 else TITLES[number],title_line_gap=8,title_top=650 if number==14 else 1138))
    base=intro_override or (m/'base.mp4' if number>=15 else next(m.glob('base-*.mp4')))
    final=w/'final.mp4';source_final=source_override or final;target=m/'final-interligne-visible-8px.mp4'
    info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration','-of','json',str(source_final)]))
    duration=float(next(x['duration'] for x in info['streams'] if x['codec_type']=='video'))
    def audio_hash(path):
        return run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).strip()
    original_audio_hash=audio_hash(source_final)
    # Refaire seulement l’ouverture ; le reste du montage actuel garde ses effets et sous-titres.
    graph=(f'[0:v]trim=end={replace_duration},fps=30,setpts=PTS-STARTPTS,ass=sous-titres-reference.ass:fontsdir=.[cap];'
           f'[3:v]trim=end={replace_duration},format=rgba,fade=t=out:st=3.8:d=0.2:alpha=1[hook];'
           f'[2:v]trim=end={replace_duration},format=rgba[brand];'
           '[cap][hook]overlay=0:0:shortest=1[h];[h][brand]overlay=0:0:shortest=1[intro];'
           f'[1:v]trim=start={replace_duration},fps=30,setpts=PTS-STARTPTS[tail];'
           '[intro][tail]concat=n=2:v=1:a=0[v]')
    run(['ffmpeg','-v','error','-y','-i',str(base),'-i',str(source_final),'-loop','1','-framerate','30','-i','header-footer-reference.png',
         '-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,
         '-map','[v]','-map','1:a:0','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','3',
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
    actual=validate_duration(target);assert abs(actual-duration)<.05
    assert audio_hash(target)==original_audio_hash
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    target.replace(final)
    d.pop('titre_interligne_pixels',None);d['titre_espace_visible_pixels']=8;save(w/'histoire.json',d)
    if number>=16:save(stage_for(w)/'histoire.json',d)
    elif number==15:save(m.parent/'histoire.json',d)
    compare(w)
    run(['ffmpeg','-v','error','-y','-ss','1','-i',str(final),'-frames:v','1',str(w/'apercu.png')])
    save(root_m/'controle-interligne.json',dict(espace_visible_pixels=8,methode='Limites des glyphes rendus, contours compris',layout=read(m/'titre-hook-layout.json'),duree_video=actual,audio_sha256=original_audio_hash,voix='AAC conservé sans réencodage, empreinte vérifiée',comparaison_regeneree=True,decodage_integral=True))
    print(number,'interligne visible uniforme et comparaison mis à jour',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--numero',type=int);args=parser.parse_args()
    folders=sorted(p for p in (ROOT/'out').iterdir() if p.is_dir() and p.name[:2] in ['13','14','15','16','17','18'] and (p/'histoire.json').exists() and (args.numero is None or int(p.name[:2])==args.numero))
    with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(revise,folders))
