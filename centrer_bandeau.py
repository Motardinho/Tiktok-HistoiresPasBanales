"""Correction du centrage optique du bandeau de série, sur toute la vidéo."""
import json,shutil,sys
from PIL import Image,ImageDraw
from habillage_reference import ITEMS,compare
from construire_identite import font,INK,YELLOW
from montage_reel import ROOT,run

def main(slug):
 w=ROOT/'out'/slug;label=ITEMS[slug]['series']
 patch=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(patch);sz=35
 while d.textlength(label,font=font(sz))>740:sz-=1
 width=d.textlength(label,font=font(sz))
 d.rectangle((225,79,225+width+60,150),fill=INK)
 bbox=d.textbbox((0,0),label,font=font(sz))
 y=79+(71-(bbox[3]-bbox[1]))/2-bbox[1]
 d.text((255,y),label,font=font(sz),fill=YELLOW)
 patch.save(w/'bandeau-centre.png')
 dur=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'final-hpb-v6.mp4')]))['format']['duration'])
 run(['ffmpeg','-v','error','-y','-i','final-hpb-v6.mp4','-loop','1','-framerate','30','-i','bandeau-centre.png','-filter_complex','[0:v][1:v]overlay=0:0:shortest=1[v]','-map','[v]','-map','0:a:0','-t',str(dur),'-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','final-hpb-v7.mp4'],w)
 run(['ffmpeg','-v','error','-i',str(w/'final-hpb-v7.mp4'),'-f','null','-'])
 print(slug,'bandeau centré',flush=True)
 compare(slug,w,dur,version=7)
 shutil.copy2(w/'final-hpb-v7.mp4',w/'final.mp4');shutil.copy2(w/'comparaison-hpb-v7.mp4',w/'comparaison.mp4')
 info=json.loads((w/'controle-hpb-v6.json').read_text(encoding='utf-8'))
 info.update(version='HPB v7 bandeau centré',centrage_bandeau='centrage calculé sur la hauteur visible des lettres, marges haute et basse égales',validation='Décodage intégral réussi ; contrôles visuels du hook et du bandeau à compléter.',fichiers={'video':'final-hpb-v7.mp4','comparaison':'comparaison-hpb-v7.mp4'})
 (w/'controle-hpb-v7.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
 (w/'controle.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug,'comparaison v7 prête',flush=True)

if __name__=='__main__':
 for slug in sys.argv[1:]:main(slug)
