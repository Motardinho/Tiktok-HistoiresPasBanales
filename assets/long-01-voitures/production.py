from pathlib import Path
import sys,json,re,subprocess,os
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'out/long-01-voitures-vitesse'
WORK=OUT/'_montage'
WORK.mkdir(exist_ok=True)
def writej(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def run(cmd): subprocess.run([str(x) for x in cmd],check=True)
def probe(p): return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
def voice():
 import yaml
 from narrateur.voice import synthesize
 text=(OUT/'script-travail.txt').read_text(encoding='utf-8')
 text=text[:text.index("Maintenant, imagine qu'on te laisse les clés")]+"La Yangwang gagne sur la vitesse. Mais est-ce qu'elle te fait plus rêver que la Bugatti ? Toi, tu prends laquelle ? Abonne-toi pour le prochain dossier. Pas banal, hein ?\n"
 (OUT/'script.txt').write_text(text,encoding='utf-8')
 marks=[0,text.index('Numéro deux :'),text.index('Numéro un :'),len(text)]
 chunks=[text[a:b].strip() for a,b in zip(marks,marks[1:])]
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
 replacements={'SSC':'Esse esse cé','Tuatara':'Touatara','Larry Caplin':'Lari Capline','VBOX':'Vi box','Racelogic':'Réïss lodjik','Super Sport':'Super Sport','Andy Wallace':'Andy Wallasse',"Ehra-Lessien":'Éra Lessienne','Yangwang':'Yangouang','BYD':'Bi Waï Di','Xtreme':'Extrême','Papenburg':'Papenbourg','Marc Basseng':'Marc Bassengue','Guinness':'Guiness'}
 allwords=[];offset=0;chap=[]
 for i,chunk in enumerate(chunks):
  oral=chunk
  for a,b in replacements.items(): oral=oral.replace(a,b)
  ap=WORK/f'voix-{i}.mp3';tp=WORK/f'timings-{i}.json'
  (WORK/f'texte-voix-{i}.txt').write_text(oral,encoding='utf-8')
  if not ap.exists() or not tp.exists():
   data=synthesize(cfg,[{'narration':oral}],ap);writej(tp,data)
  else:data=json.loads(tp.read_text(encoding='utf-8'))
  duration=float(probe(ap)['format']['duration'])
  chap.append({'chapitre':i,'start':offset,'end':offset+duration,'texte':chunk})
  allwords += [dict(w,start=w['start']+offset,end=w['end']+offset) for w in data['words']]
  offset+=duration
  print('Voix',i,'durée',round(duration,2),flush=True)
 (WORK/'concat-voix.txt').write_text(''.join(f"file 'voix-{i}.mp3'\n" for i in range(3)),encoding='utf-8')
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',WORK/'concat-voix.txt','-c:a','pcm_s16le',WORK/'voix.wav'])
 writej(WORK/'timings-oraux.json',{'words':allwords,'duration':offset,'chapitres':chap})
 writej(OUT/'histoire.json',{'titre':'TOP 3 - Ces voitures ont repoussé les limites de la vitesse','type_post':'videos','format':'youtube-long','width':1920,'height':1080,'duree_cible':[480,600],'chute':'B','chute_validee_par':'Marc, conversation du 15 novembre 2026','statut':'voix générée - montage en cours','reference_fichier':'out/14-trois-records-voitures-vitesse/final.mp4','scenes':[{'narration':c} for c in chunks],'prononciations':replacements})
 print('TOTAL',round(offset,2),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='voice':voice()
