"""Applique le hook et l'identité validée aux montages réels, sans sous-titres superposés."""
import copy,json,shutil,sys
from pathlib import Path
import yaml
from narrateur import assemble
from montage_reel import ROOT,run

ITEMS={
 'astronautes-sport-en-orbite':dict(count=23,hook=['IL SE PÈSE','COMME ÇA ?'],credits='Images : ASC / NASA',facts=[(33.6,38.08,'AVEC UNE PERSONNE'),(38.08,42.24,'SANS PERSONNE')]),
 'trois-records-voitures-vitesse':dict(count=19,hook=['3 HYPERCARS.','UN PIÈGE.'],credits='Images : Hennessey / Bugatti',facts=[(21.08,28.64,'CHIRON • 2019 • UN SEUL SENS'),(33.24,38.04,'BOLIDE CLIENT • 380 KM/H')]),
 'villes-plus-lentes-tomtom-2024':dict(count=24,hook=['DES JOURS','DANS LES','BOUCHONS.'],credits='Images : Pexels • INRIX 2024',facts=[(17.88,25.24,'LONDRES • 101 H'),(25.24,33.96,'NEW YORK • 102 H'),(33.96,41.44,'PARIS • 97 H')])}

def subtitles(w,t,item,cfg,duration):
 assemble.YELLOW='&H4AE2FF&';assemble.RED='&H4E62FF&'
 p=w/'habillage-hpb.ass';assemble.write_subtitles(cfg,t['words'],p)
 s=p.read_text(encoding='utf-8').replace('&H00FFFFFF','&H00E9F3F7')
 s=s.replace('8,50,50,1090,1','8,65,65,1220,1')
 styles=(
 'Style: Account,Poppins ExtraBold,33,&H00E9F3F7,&H00E9F3F7,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,1,3,1,7,62,62,70,1\n'
 'Style: Hook,Poppins ExtraBold,100,&H004AE2FF,&H004AE2FF,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,1,7,2,7,65,150,210,1\n'
 'Style: Fact,Poppins ExtraBold,53,&H004AE2FF,&H004AE2FF,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,3,14,0,8,75,75,230,1\n'
 'Style: Credits,Poppins ExtraBold,25,&H00E9F3F7,&H00E9F3F7,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,1,2,1,7,65,65,1790,1\n'
 'Style: Closing,Poppins ExtraBold,68,&H00E9F3F7,&H00E9F3F7,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,1,6,1,8,70,70,1500,1\n')
 s=s.replace('\n[Events]','\n'+styles+'\n[Events]')
 if item is ITEMS['astronautes-sport-en-orbite']:
  lines=[]
  for line in s.splitlines():
   if line.startswith('Dialogue:') and ',Default,' in line:
    parts=line.split(',',9)
    ts=parts[1].split(':');start=int(ts[0])*3600+int(ts[1])*60+float(ts[2])
    if start<7.92:parts[9]='{\\an8\\pos(540,620)}'+parts[9];line=','.join(parts)
   lines.append(line)
  s='\n'.join(lines)+'\n'
 end=assemble._ass_time(duration)
 s+=f'Dialogue: 2,0:00:00.00,{end},Account,,0,0,0,,HISTOIRES PAS BANALES\n'
 hook='\\N'.join(item['hook'])
 s+=f'Dialogue: 2,0:00:00.00,0:00:02.80,Hook,,0,0,0,,{{\\fad(60,140)}}{hook}\n'
 s+=f'Dialogue: 1,0:00:02.80,{end},Credits,,0,0,0,,{item["credits"]}\n'
 for a,b,label in item['facts']:
  s+=f'Dialogue: 2,{assemble._ass_time(a)},{assemble._ass_time(b)},Fact,,0,0,0,,{label}\n'
 s+=f'Dialogue: 2,{assemble._ass_time(duration-2.2)},{end},Closing,,0,0,0,,{{\\fad(130,80)}}HISTOIRES\\N{{\\c&H4AE2FF&}}PAS BANALES\n'
 p.write_text(s,encoding='utf-8');return p

def comparison(slug,w,duration):
 original=ROOT/'assets/references-faiseemoc84'/(slug+'.mp4')
 od=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(original)]))['format']['duration'])
 font='police.ttf'
 graph=("[0:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[l];"
        "[1:v]scale=540:960,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=180[r];"
        "[l][r]hstack=inputs=2,pad=1080:1040:0:80:color=0x12151C,"
        f"drawtext=fontfile={font}:text='ORIGINAL':fontcolor=0xF7F3E9:fontsize=27:x=180:y=23,"
        f"drawtext=fontfile={font}:text='HISTOIRES PAS BANALES':fontcolor=0xFFE24A:fontsize=24:x=632:y=25[v]")
 target=w/'comparaison-hpb-v4.mp4'
 run(['ffmpeg','-v','error','-y','-i',str(original),'-i','final-hpb-v4.mp4','-filter_complex',graph,'-map','[v]','-map','0:a:0','-map','1:a:0','-t',str(max(duration,od)),'-c:v','libx264','-preset','fast','-crf','21','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-metadata:s:a:0','title=Original','-metadata:s:a:1','title=Histoires pas banales','-disposition:a:0','0','-disposition:a:1','default','-movflags','+faststart',target.name],w)
 print(slug,'comparaison HPB prête',flush=True)

def main(slug):
 item=ITEMS[slug];w=ROOT/'out'/slug
 t=json.loads((w/'timings.json').read_text(encoding='utf-8'))
 duration=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'voix.mp3')]))['format']['duration'])
 cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
 cfg['render'].update(words_per_caption=5,subtitle_wrap=19,subtitle_size=88)
 files=[w/f'dynamique{i:02d}.mp4' for i in range(item['count'])]
 assert all(p.exists() for p in files)
 if slug=='astronautes-sport-en-orbite':
  # Deux cadrages du même mouvement, dont un miroir : effet visuel, pas deux mesures.
  hook=w/'hook-double-hpb.mp4'
  vf='split=2[a][b];[a]crop=540:1920:510:0[l];[b]crop=540:1920:510:0,hflip[r];[l][r]hstack=inputs=2,drawbox=x=538:y=0:w=4:h=ih:color=0x12151C:t=fill[v]'
  run(['ffmpeg','-v','error','-y','-i',str(files[0]),'-filter_complex',vf,'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','3','-pix_fmt','yuv420p',str(hook)])
  files[0]=hook
 concat=w/'concat-hpb.txt';concat.write_text(''.join(f"file '{p.name}'\n" for p in files),encoding='utf-8')
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat.name,'-c','copy','base-hpb.mp4'],w)
 subs=subtitles(w,t,item,cfg,duration)
 shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',w/'police.ttf')
 shutil.copy2(ROOT/'identite/histoires-pas-banales/logos/symbole-couleur.png',w/'logo-hpb.png')
 graph=f'[0:v]ass={subs.name}:fontsdir=.[cap];[2:v]scale=180:180[logo];[cap][logo]overlay=860:32:shortest=1[v]'
 run(['ffmpeg','-v','error','-y','-i','base-hpb.mp4','-i','voix.mp3','-loop','1','-framerate','30','-i','logo-hpb.png','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','20','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','final-hpb-v4.mp4'],w)
 run(['ffmpeg','-v','error','-i',str(w/'final-hpb-v4.mp4'),'-f','null','-'])
 print(slug,'hook + habillage HPB rendus',flush=True)
 comparison(slug,w,duration)
 report=dict(version='HPB v4',logo='validé v16',hook=item['hook'],plein_ecran=True,plans=item['count'],double_hook=slug=='astronautes-sport-en-orbite',couleurs=['#12151C','#FFE24A','#F7F3E9'],audio='narration et timings réutilisés ensemble ; deux pistes séparées dans la comparaison',validation='Décodage intégral réussi ; contrôle visuel à compléter.')
 (w/'controle-hpb-v4.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
 for slug in sys.argv[1:] or ITEMS:main(slug)
