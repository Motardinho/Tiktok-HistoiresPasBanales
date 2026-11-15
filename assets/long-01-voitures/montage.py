from production import *
from concurrent.futures import ThreadPoolExecutor
SOURCES={
 'road':('assets/sources-reelles/ssc-road.mp4',''),
 'speed':('assets/sources-reelles/ssc-speed.mp4',''),
 'ssc':('assets/sources-reelles/ssc-tuatara.mp4',''),
 'pov':('assets/long-01-voitures/KXYkDkrF3rk.mp4',''),
 'bug':('assets/sources-reelles/bugatti-record.mp4','crop=iw:ih*0.76:0:ih*0.12,'),
 'bugrun':('assets/sources-reelles/bugatti-record.mp4','crop=1920:600:0:340,'),
 'detail':('assets/long-01-voitures/ezF-o6jRCLQ.mp4','crop=iw*0.86:ih*0.72:iw*0.06:ih*0.16,'),
 'f1':('assets/long-01-voitures/PziIkX-isGQ.mp4',''),
 'yang':('assets/sources-reelles/yangwang-u9-xtreme-2025.mp4','crop=iw:ih*0.86:0:ih*0.04,'),
 'film':('assets/long-01-voitures/ewf-q-U_b9A.mp4','crop=iw*0.90:ih*0.76:iw*0.05:ih*0.08,'),
 'new':('assets/long-01-voitures/PWWamnhY9pE.mp4','crop=iw*0.90:ih*0.74:iw*0.05:ih*0.07,'),
 'record':('assets/sources-reelles/yangwang-u9-xtreme-2026.mp4','crop=iw:ih*0.49:0:ih*0.08,'),
}
# Ordered source intervals, in seconds. No source speed change; no automatic loops.
BOARD={
0:[('speed',21,1.8),('speed',37,1.8)],
1:[('road',0,4),('ssc',122,2.5),('ssc',180,4),('road',11,4)],
2:[('road',17,4),('speed',12,4),('road',22,4)],
3:[('ssc',2,2),('ssc',183,5),('ssc',37,4),('ssc',150,5)],
4:[('pov',82,4),('pov',48,4),('pov',140,4),('pov',73,4)],
5:[('ssc',145,4),('ssc',43,4),('ssc',50,4),('ssc',153,4)],
6:[('speed',38,4),('road',12,4),('pov',20,4),('road',4,4),('pov',60,4)],
7:[('pov',9,4),('ssc',143,4),('pov',30,4),('speed',19,4),('ssc',158,4)],
8:[('ssc',0,4),('road',8,4),('pov',39,5)],
9:[('pov',67,4),('pov',109,4),('road',18,4)],
10:[('bug',156,4),('bug',128,2.5),('bug',161,4)],
11:[('bug',17,3),('bug',64,7),('bug',50,4),('bug',25,4)],
12:[('bug',56,4),('detail',23,4),('detail',34,5)],
13:[('detail',211,5),('detail',222,5),('detail',232,5),('detail',242,4),('detail',288,5)],
14:[('detail',168,5),('detail',180,5),('detail',322,5)],
15:[('detail',78,4),('detail',266,4),('detail',302,5)],
16:[('bug',67,4),('bugrun',84,5),('bugrun',97,4),('bugrun',108,5)],
17:[('bugrun',142,4),('bug',159,4),('detail',172,4)],
18:[('bugrun',114,4),('bugrun',121,4),('bugrun',133,4),('bug',153,5)],
19:[('detail',412,5),('detail',449,5),('detail',281,5)],
20:[('detail',64,4),('detail',155,4),('detail',315,4)],
21:[('detail',202,4),('detail',52,4)],
22:[('film',132,4),('new',201,4),('film',151,5)],
23:[('film',43,4),('film',92,4),('film',502,4),('film',532,4),('film',603,4)],
24:[('film',30,3),('film',101,3),('film',431,3)],
25:[('new',181,3),('new',189,6),('film',655,4),('new',194,2)],
26:[('record',96,5),('new',165,5),('new',173,6)],
27:[('new',164,4),('new',170,4),('new',178,4),('new',190,4)],
28:[('record',8,5),('record',18,5),('record',32,5),('record',44,5),('new',187,3)],
29:[('new',196,4),('new',201,4),('new',205,4)],
30:[('new',211,4),('new',215,3),('record',118,5)],
31:[('record',104,5),('record',110,5),('new',200,4),('new',207,4)],
32:[('pov',17,4),('detail',184,4),('film',107,4),('film',135,4)],
33:[('new',202,3),('detail',451,3),('film',153,3),('film',133,3)],
}
def plans():
 final=Path(__file__).with_name('plans-definitifs.json')
 if final.exists():
  writej(WORK/'plans.json',json.loads(final.read_text(encoding='utf-8')))
  print('Manifeste corrigé restauré');return
 rows=json.loads((WORK/'paragraphes.json').read_text(encoding='utf-8'));plans=[]
 for p in rows:
  selected=BOARD[p['i']];span=p['end']-p['start'];weights=sum(x[2] for x in selected);cursor=p['start']
  for j,(key,at,weight) in enumerate(selected):
   end=p['end'] if j==len(selected)-1 else cursor+span*weight/weights
   # Source duration remains equal to timeline duration: never slow or accelerate footage.
   source,zone=SOURCES[key]
   plans.append(dict(i=len(plans),paragraph=p['i'],start=cursor,end=end,source=source,entree=at,zone=zone,note=p['texte'][:90]))
   cursor=end
 writej(WORK/'plans.json',plans);print(len(plans),'plans')
def shot(p):
 dst=WORK/f'plan-{p["i"]:03}.mp4'
 if dst.exists():return
 frames=round(p['end']*30)-round(p['start']*30)
 crop=r"crop=trunc(min(iw\,ih*16/9)/2)*2:trunc(min(ih\,iw*9/16)/2)*2:(iw-ow)/2:(ih-oh)/2,"
 vf=p['zone']+crop+'scale=1920:1080:flags=lanczos,setsar=1,fps=30,format=yuv420p,setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709'
 if p['i'] in [15,30,45,49,55,72,83,115]:vf+=f",zoompan=z='1+0.035*sin(PI*on/{frames})':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30"
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-threads','2','-ss',str(p['entree']),'-i',str(ROOT/p['source']),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','2',str(dst)]
 subprocess.run(cmd,check=True)
 return p['i']
def render():
 ps=json.loads((WORK/'plans.json').read_text(encoding='utf-8'))
 with ThreadPoolExecutor(max_workers=3) as pool:
  for i in pool.map(shot,ps):
   if i is not None and i%10==0:print('Plan',i,'/',len(ps),flush=True)
 (WORK/'concat-plans.txt').write_text(''.join(f"file 'plan-{p['i']:03}.mp4'\n" for p in ps),encoding='utf-8')
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',WORK/'concat-plans.txt','-c','copy',WORK/'muet.mp4'])
 finish()
def finish():
 ps=json.loads((WORK/'plans.json').read_text(encoding='utf-8'));total=ps[-1]['end']
 # Voice dominates; music is further ducked while speech is present.
 audio=f'[1:a]highpass=f=65,loudnorm=I=-16:TP=-1.5:LRA=8,asplit=2[v][sc];[2:a]volume=0.075,afade=t=in:d=2,afade=t=out:st={total-4}:d=4[m];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[duck];[v][duck][4:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]'
 video="[0:v]ass=sous-titres.ass:fontsdir='../../../assets/fonts'[sub];[sub][3:v]overlay=0:0[vout]"
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-threads','4','-i','muet.mp4','-i','voix-longue.wav','-stream_loop','-1','-i',str(ROOT/'assets/musique/mixkit/voitures.mp3'),'-i','logo.png','-i','transitions.wav','-filter_complex_threads','2','-filter_complex',video+';'+audio,'-map','[vout]','-map','[a]','-t',str(total),'-c:v','libx264','-preset','fast','-crf','19','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'essai-long-v1.mp4')]
 subprocess.run(cmd,cwd=WORK,check=True);print('EXPORT TERMINE',flush=True)
if __name__=='__main__':
 if sys.argv[1]=='plans':plans()
 elif sys.argv[1]=='render':render()
 elif sys.argv[1]=='finish':finish()
