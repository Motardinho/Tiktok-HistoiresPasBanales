"""Comparaisons locales : référence à gauche, HPB à droite, audios séparés."""
import argparse
import json
import shutil

from montage_reel import ROOT,run
from produire_lot_16_18 import FOLDERS,read,save

def compare(w):
    data=read(w/'histoire.json')
    if not data.get('reference'):
        raise ValueError('Livraison incomplète : choisir une vidéo de référence et renseigner histoire.json avant de produire la comparaison.')
    video_id=data['reference'].rstrip('/').split('/')[-1].split('?')[0]
    source=ROOT/'assets/references-faiseemoc84'/f'{video_id}.mp4'
    muxed_reference=source.with_name(f'{video_id}-reference.mp4')
    if data.get('reference_fichier'):
        source=ROOT/data['reference_fichier']
        if not source.is_file():raise FileNotFoundError(source)
    elif muxed_reference.exists():source=muxed_reference
    if not source.exists():
        # Un format contenant déjà vidéo et narration évite de télécharger
        # par erreur la piste musicale du post comme audio de référence.
        import sys
        run([sys.executable,'-m','yt_dlp','--no-playlist','--no-warnings',
             '-f','best[vcodec!=none][acodec!=none]','-o',str(source),data['reference']])
    final=w/'final.mp4';m=w/'_montage'
    reference_audio='Référence - '+data.get('reference_auteur','faiseemoc84')
    if data.get('reference_extrait'):reference_audio+=' (extrait)'
    def probe(p):return json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,duration,width,height','-of','json',str(p)]))
    source_info=probe(source);final_info=probe(final)
    for name,info in [('référence',source_info),('HPB',final_info)]:
        video=next(s for s in info['streams'] if s['codec_type']=='video')
        audio=next(s for s in info['streams'] if s['codec_type']=='audio')
        assert abs(float(video['duration'])-float(audio['duration']))<.3,f'Piste audio incohérente : {name}'
    duration=max(float(x['format']['duration']) for x in [source_info,final_info])
    shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
    graph=(
      '[0:v]setpts=PTS-STARTPTS,scale=540:960:force_original_aspect_ratio=decrease,'
      'pad=540:960:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[l];'
      '[1:v]setpts=PTS-STARTPTS,scale=540:960:force_original_aspect_ratio=decrease,'
      'pad=540:960:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[r];'
      '[l][r]hstack=inputs=2,pad=1080:1040:0:80:color=0x12151C,'
      "drawtext=fontfile=police.ttf:text='RÉFÉRENCE':fontcolor=0xF7F3E9:fontsize=28:x=(540-tw)/2:y=25,"
      "drawtext=fontfile=police.ttf:text='HISTOIRES PAS BANALES':fontcolor=0xFFE24A:fontsize=25:x=540+(540-tw)/2:y=25[v];"
      '[0:a]asetpts=PTS-STARTPTS,apad[a0];[1:a]asetpts=PTS-STARTPTS,apad[a1]')
    target=w/'comparaison.mp4'
    run(['ffmpeg','-v','error','-y','-i',str(source),'-i',str(final),'-filter_complex_threads','2','-filter_complex',graph,
         '-map','[v]','-map','[a0]','-map','[a1]','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','20','-threads','3','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','160k','-metadata:s:a:0',f'title={reference_audio}','-metadata:s:a:1','title=Histoires pas banales',
         '-metadata:s:a:0',f'handler_name={reference_audio}','-metadata:s:a:1','handler_name=Histoires pas banales',
         '-disposition:a:0','0','-disposition:a:1','default','-movflags','+faststart',str(target)],m)
    result=probe(target);streams=result['streams'];assert len([s for s in streams if s['codec_type']=='audio'])==2
    vs=next(s for s in streams if s['codec_type']=='video');assert (vs['width'],vs['height'])==(1080,1040)
    assert abs(float(vs['duration'])-duration)<.1
    run(['ffmpeg','-v','error','-i',str(target),'-map','0:v:0','-map','0:a','-f','null','-'])
    save(m/'controle-comparaison.json',dict(source_url=data['reference'],source_file=str(source.relative_to(ROOT)),source_duration=float(source_info['format']['duration']),hpb_duration=float(final_info['format']['duration']),comparison_duration=float(result['format']['duration']),layout='référence gauche - HPB droite',shorter_end='image figée et silence après la fin',audio_tracks=[reference_audio,'Histoires pas banales (par défaut)'],usage='comparaison locale de travail, non destinée à la publication'))
    print(w.name,'comparaison prête',round(duration,2),'s',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--numero',type=int);a=p.parse_args()
    for w in FOLDERS:
        if a.numero is None or int(w.name[:2])==a.numero:compare(w)
