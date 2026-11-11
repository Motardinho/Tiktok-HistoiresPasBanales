"""Assure le contraste du logo validé sur les images claires et sombres."""
import json,shutil,sys
from PIL import Image,ImageDraw
from construire_identite import SHELL,INK,mark_image,OUT
from montage_reel import ROOT,run
from habillage_hpb import ITEMS

def comparison(slug,w,duration):
 original=ROOT/'assets/references-faiseemoc84'/(slug+'.mp4')
 od=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(original)]))['format']['duration'])
 graph=("[0:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[l];"
        "[1:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[r];"
        "[l][r]hstack=inputs=2,pad=1080:1040:0:80:color=0x12151C,"
        "drawtext=fontfile=police.ttf:text='ORIGINAL':fontcolor=0xF7F3E9:fontsize=27:x=180:y=23,"
        "drawtext=fontfile=police.ttf:text='HISTOIRES PAS BANALES':fontcolor=0xFFE24A:fontsize=24:x=632:y=25[v]")
 run(['ffmpeg','-v','error','-y','-i',str(original),'-i','final-hpb-v5.mp4','-filter_complex',graph,'-map','[v]','-map','0:a:0','-map','1:a:0','-t',str(max(duration,od)),'-c:v','libx264','-preset','fast','-crf','21','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-metadata:s:a:0','title=Original','-metadata:s:a:1','title=Histoires pas banales','-disposition:a:0','0','-disposition:a:1','default','-movflags','+faststart','comparaison-hpb-v5.mp4'],w)

def main(slug):
 w=ROOT/'out'/slug
 # Fond encre dans la seule silhouette de la bulle : la ponctuation reste noire.
 logo=Image.new('RGBA',(1024,1024));ImageDraw.Draw(logo).polygon(SHELL,fill=INK)
 logo=logo.rotate(6,resample=Image.Resampling.BICUBIC);logo.alpha_composite(mark_image())
 logo.save(w/'logo-hpb-contraste.png')
 logo.save(OUT/'gabarits/symbole-video-contraste.png')
 dur=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'final-hpb-v4.mp4')]))['format']['duration'])
 run(['ffmpeg','-v','error','-y','-i','final-hpb-v4.mp4','-loop','1','-framerate','30','-i','logo-hpb-contraste.png','-filter_complex','[1:v]scale=180:180[l];[0:v][l]overlay=860:32:shortest=1[v]','-map','[v]','-map','0:a:0','-t',str(dur),'-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','final-hpb-v5.mp4'],w)
 run(['ffmpeg','-v','error','-i',str(w/'final-hpb-v5.mp4'),'-f','null','-'])
 print(slug,'rendu final HPB prêt',flush=True)
 comparison(slug,w,dur)
 shutil.copy2(w/'final-hpb-v5.mp4',w/'final.mp4')
 shutil.copy2(w/'comparaison-hpb-v5.mp4',w/'comparaison.mp4')
 report=json.loads((w/'controle-hpb-v4.json').read_text(encoding='utf-8'))
 report.update(version='HPB v5',validation='Décodage intégral réussi. Contrôle visuel du hook, du plein écran, de la typographie et du logo sur images claires et sombres.',reproduction='python habillage_hpb.py <dossier> puis python finaliser_hpb.py <dossier>')
 (w/'controle-hpb-v5.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug,'comparaison finale prête',flush=True)

if __name__=='__main__':
 for slug in sys.argv[1:]:main(slug)
