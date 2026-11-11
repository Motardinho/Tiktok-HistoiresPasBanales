"""Montage démonstratif en portrait : coupes courtes, gestes et apesanteur visibles."""
import copy
import json
import shutil
from pathlib import Path
import yaml
from narrateur import assemble
from montage_reel import ROOT,SOURCES,run,compare

WORK=ROOT/'out'/'astronautes-sport-en-orbite'
# Chaque tuple : source, entrée, durée ; la dernière durée suit la fin de la scène.
# Les oscillations comparées restent à leur vitesse réelle.
GROUPS=[
 [('astronautes-masse',24,2.8,.53,.84),('astronautes-masse',32,2.8,.53,.78),('astronautes-masse',38,None,.53,.84)],
 [('williams-visite',290,2.64,.52),('nyberg-cheveux',96,2.64,.51),('astronautes-masse',55,None,.53)],
 [('williams-visite',310,2.8,.52),('nyberg-cheveux',128,2.8,.51),('williams-visite',18,None,.53)],
 [('astronautes-masse',54,2.6,.53),('astronautes-masse',24,3.4,.53),('astronautes-masse',34,None,.53)],
 [('astronautes-masse',29,4.48,.53),('astronautes-masse',55,None,.53)],
 [('astronautes-masse',47,2.56,.53),('astronautes-masse',16,2.56,.53),('astronautes-masse',34,None,.53)],
 [('williams-visite',247,2.8,.53),('williams-visite',263,2.8,.51),('nyberg-cheveux',143,None,.51)],
 [('astronautes-masse',27,3,.53),('nyberg-cheveux',125,2.6,.51),('williams-visite',289,None,.52)],
]

def main():
 archive=WORK/'version-reelle-v2'
 archive.mkdir(exist_ok=True)
 for name in ['final.mp4','comparaison.mp4','sous-titres.ass','sources-visuelles.json']:
  if (WORK/name).exists() and not (archive/name).exists():shutil.copy2(WORK/name,archive/name)
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
 cfg=copy.deepcopy(cfg)
 cfg['render']['words_per_caption']=5
 cfg['render']['subtitle_wrap']=19
 timing=json.loads((WORK/'timings.json').read_text(encoding='utf-8'))
 data=json.loads((WORK/'histoire.json').read_text(encoding='utf-8'))
 overlays=[(0,2.8,data['titre_fixe'],'Titre'),
           (33.6,38.08,'AVEC UNE PERSONNE','Bandeau'),
           (38.08,42.24,'SANS PERSONNE','Bandeau')]
 subs=WORK/'sous-titres-v3.ass'
 assemble.write_subtitles(cfg,timing['words'],subs,overlays)
 content=subs.read_text(encoding='utf-8').replace('8,50,50,1090,1','8,65,65,1240,1')
 credit='Style: Credit,Poppins ExtraBold,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,2,1,8,30,30,1820,1\n'
 content=content.replace('\n[Events]', '\n'+credit+'\n[Events]')
 content+='\nDialogue: 1,0:00:00.00,0:01:08.00,Credit,,0,0,0,,DOSSIER 13 • Images : ASC / NASA\n'
 subs.write_text(content,encoding='utf-8')
 cursor_frames=0
 files=[]
 edit=[]
 for scene,(group,scene_dur) in enumerate(zip(GROUPS,timing['scene_durations'])):
  end_frames=round(sum(timing['scene_durations'][:scene+1])*30)
  for name,start,duration,center,*window in group:
   frames=round(duration*30) if duration is not None else end_frames-cursor_frames
   if scene==7 and duration is None:frames+=15
   src=SOURCES/(name+'.mp4')
   n=len(files)
   target=WORK/f'dynamique{n:02d}.mp4'
   # Remplir le 9:16 et suivre le centre d'intérêt. Aucun fond flou.
   ch=window[0] if window else 1
   vf=(f"crop=w='trunc(ih*{ch}*9/16/2)*2':h='trunc(ih*{ch}/2)*2':x='max(0,min(iw-ow,iw*{center}-ow/2))':y=ih-oh,"
       'scale=1080:1920:flags=lanczos,fps=30,setsar=1')
   run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(src),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4','-pix_fmt','yuv420p',str(target)])
   files.append(target)
   edit.append(dict(plan=n,scene=scene,source=src.name,entree_s=start,debut_montage_s=cursor_frames/30,duree_s=frames/30,cadrage='plein écran 9:16',centre_horizontal=center,vitesse=1.0))
   cursor_frames+=frames
   print('Plan',n+1,'/',sum(len(g) for g in GROUPS),flush=True)
 assemble.assemble(cfg,WORK,files,WORK/'voix.mp3',subs,WORK/'final-v3.mp4',assemble.stamp_time(timing['words']))
 (WORK/'montage-v3.json').write_text(json.dumps(edit,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Montage V3 terminé',flush=True)
 finalize()

def finalize():
 run(['ffmpeg','-v','error','-i',str(WORK/'final-v3.mp4'),'-f','null','-'])
 shutil.copy2(WORK/'final-v3.mp4',WORK/'final.mp4')
 shutil.copy2(WORK/'sous-titres-v3.ass',WORK/'sous-titres.ass')
 compare('astronautes-sport-en-orbite')
 shutil.copy2(WORK/'comparaison.mp4',WORK/'comparaison-v3.mp4')
 info={'version':3,'plans':sum(len(g) for g in GROUPS),'cadrage':'1080x1920, plein écran, sans fond flou',
       'rythme':'coupes de 1,7 à 4,48 secondes, moyenne 2,8 secondes',
       'visuels':'trois sources ASC/NASA, déplacements, cheveux flottants, appareil avec et sans personne',
       'vitesse_images':'réelle, pas de modification des oscillations',
       'audio':'voix et timings conservés ensemble',
       'hook':'les 7,92 premières secondes montrent uniquement la machine en mouvement en gros plan',
       'validation':'décodage intégral et contrôle visuel de dix instants ; écoute intégrale manuelle non réalisée',
       'reproduction':'python astronautes_dynamique.py',
       'ancienne_version':'version-reelle-v2/'}
 (WORK/'controle.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
