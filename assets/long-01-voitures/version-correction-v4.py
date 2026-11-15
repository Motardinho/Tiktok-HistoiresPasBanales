from production import *
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageFont
import numpy as np,wave,math
from narrateur.assemble import _ass_time
from monter_lot_21_23 import caption_words

V=WORK/'v4';V.mkdir(exist_ok=True);TOTAL=482.0
NAMES=['ssc','bugatti','yangwang']
# Editorial pools refer to the individually inspected, uncaptioned V2 clips.
POOLS=[
 [[0,1],[4,14,16,13,34,26,28],[4,13,15,16,23,26,28,33,35,114],[16,14,23,34,4],
  [10,19,11,14,16,25,3],[3,18,19,23,20,27,3],[17,27,14,16,25,3,23],
  [27,17,15,25,22,3,14],[3,10,16,25,19],[34,23,16,14]],
 [[37,38,39,53,47],[40,41,42,43,37,44],[47,48,49,50,51,37,46],
  [49,50,51,57,48,37],[53,115,60,53,37,115,60],[55,56,57,72,73,74,45],
  [58,59,60,37,61,38],[59,60,61,37,65,66,67,68,63],[38,62,64,63,67,37],
  [44,69,70,71,45,46,75,76],[72,73,74,37,47,51,75,76]],
 [[117,79,78,83,82],[80,81,82,83,84,79,117,85],[88,89,90,91,93,105,98,104],
  [92,93,94,104,95,106,97],[95,96,87,97,86,93,85,103,96],
  [79,86,87,83,95,96,105,98,93],[99,103,100,91,101,95,102,104,93],
  [96,103,97,86,95,104,99,87],[104,105,106,107,108,109,105,93],
  [110,112,111,105,109,113,78],[16,3,53,37,96,93,117],
  [118,119,120,121,79,117]]
]

def prepare():
 story=json.loads((V/'histoire-travail.json').read_text(encoding='utf8'))
 chunks=[];wordsets=[];dur=[]
 for i,name in enumerate(NAMES):
  chunks.append((OUT/f'script-{name}-v4.txt').read_text(encoding='utf8').strip())
  fn='voix.mp3' if i==0 else f'voix-{name}.mp3';tn='timings.json' if i==0 else f'timings-{name}.json'
  dur.append(float(probe(V/fn)['format']['duration']));wordsets.append(json.loads((V/tn).read_text(encoding='utf8'))['words'])
 rate=sum(dur)/(TOTAL-.3);rows=[];words=[];offset=0;chapters=[]
 def clean(s):return re.sub(r'[^\w]+',' ',s.lower()).strip()
 for ci,chunk in enumerate(chunks):
  chapters.append(offset/rate);local=wordsets[ci];tokens=[clean(w['w']) for w in local];cursor=0
  for pi,p in enumerate(chunk.split('\n\n')):
   oral=p
   for a,b in story['prononciations'].items():oral=oral.replace(a,b)
   target=[clean(x) for x in oral.split()[:5]]
   j=next(j for j in range(cursor,len(tokens)-len(target)+1) if tokens[j:j+len(target)]==target)
   cursor=j+1;rows.append(dict(i=len(rows),chapter=ci,paragraph=pi,start=(offset+local[j]['start'])/rate,texte=p))
  words.extend(dict(w,start=(offset+w['start'])/rate,end=min(TOTAL,(offset+w['end'])/rate)) for w in local)
  offset+=dur[ci]
 for i,r in enumerate(rows):r['end']=rows[i+1]['start'] if i+1<len(rows) else TOTAL
 (OUT/'script-v4.txt').write_text('\n\n'.join(chunks)+'\n',encoding='utf8')
 writej(V/'paragraphes.json',rows);writej(V/'timings-complets.json',{'words':words,'duration':TOTAL,'rate':rate,'chapitres':chapters})
 (V/'concat-voix.txt').write_text("file 'voix.mp3'\nfile 'voix-bugatti.mp3'\nfile 'voix-yangwang.mp3'\n",encoding='utf8')
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',V/'concat-voix.txt','-af',f'atempo={rate},apad,atrim=duration={TOTAL}','-ar','48000','-ac','1','-c:a','pcm_s16le',V/'voix-complete.wav'])
 # Caption formatting follows the HPB format; the new alignment replaces all old timings.
 replacements={v:k for k,v in story['prononciations'].items()}
 replacements.update({'numéro trois':'N°3','numéro deux':'N°2','numéro un':'N°1','quatre cent soixante-quatorze virgule huit':'474,8','quatre cent quatre-vingt-dix virgule quarante-huit':'490,48','quatre cent quatre-vingt-seize virgule vingt-deux':'496,22','cinq cent trois virgule dix-sept':'503,17','deux cent quatre-vingt-quinze':'295','quatre cent quatre-vingt-dix':'490','cinq cent onze':'511','cinq cent trois':'503','trois mille':'3 000','mille six cents':'1 600','cent trente-deux':'132','cent quarante':'140','deux mille vingt-deux':'2022','deux mille dix-neuf':'2019','deux mille vingt-cinq':'2025','deux mille vingt-six':'2026','deux mille vingt et un':'2021','deux mille vingt':'2020','vingt-cinq':'25','trois cents plus':'300+','trois cents':'300','deux cents':'200','cinq cents':'500','kilomètres-heure':'KM/H','u neuf':'U9','w seize':'W16','huit virgule huit':'8,8','soixante-dix':'70','trente Super':'30 Super'})
 cap=caption_words(words,replacements);groups=[];buf=[];font=ImageFont.truetype(str(ROOT/'assets/fonts/Poppins-ExtraBold.ttf'),92)
 for w in cap:
  if buf and (len(buf)>=5 or font.getlength(' '.join(x['w'] for x in buf+[w]))>1600 or w['start']-buf[-1]['end']>.5):groups.append(buf);buf=[]
  buf.append(w)
  if re.search(r'[.!?]$',w['w']):groups.append(buf);buf=[]
 if buf:groups.append(buf)
 header=(WORK/'sous-titres.ass').read_text(encoding='utf8').split('Dialogue:')[0].replace('ExtraBold,80,','ExtraBold,92,')
 events=[];srt=[]
 def st(t):
  n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
 for i,g in enumerate(groups):
  end=min(g[-1]['end']+.12,groups[i+1][0]['start']) if i+1<len(groups) else TOTAL
  for j,w in enumerate(g):
   stop=g[j+1]['start'] if j+1<len(g) else end
   txt=' '.join((r'{\c&H47E4FF&}'+v['w']+r'{\c&HFFFFFF&}') if j==k else v['w'] for k,v in enumerate(g))
   events.append(f'Dialogue: 0,{_ass_time(w["start"])},{_ass_time(stop)},Default,,0,0,0,,{txt}')
  srt.append(f'{i+1}\n{st(g[0]["start"])} --> {st(end)}\n'+ ' '.join(v['w'] for v in g)+'\n')
 accents=[r['start'] for r in rows if r['paragraph'] in [2,4,6,8] and r['start']>5]
 for t in chapters[1:]:
  shape=r'{\an7\move(-2400,0,2200,0)\bord0\shad0\1c&H47E4FF&\p1}m 0 0 l 1800 0 1400 1080 -400 1080{\p0}'
  events.append(f'Dialogue: 5,{_ass_time(t-.17)},{_ass_time(t+.17)},Default,,0,0,0,,{shape}')
 for t in accents:
  shape=r'{\an7\move(-700,0,2300,0)\bord0\shad0\1c&H47E4FF&\1a&H35&\p1}m 0 0 l 80 0 -320 1080 -400 1080{\p0}'
  events.append(f'Dialogue: 4,{_ass_time(t-.1)},{_ass_time(t+.1)},Default,,0,0,0,,{shape}')
 (V/'sous-titres.ass').write_text(header+'\n'.join(events),encoding='utf8');(OUT/'sous-titres-v4.srt').write_text('\n'.join(srt),encoding='utf8')
 sr=48000;fx=np.zeros(round(TOTAL*sr),dtype=np.float32);rng=np.random.default_rng(26)
 for t in chapters[1:]+accents:
  n=int(.24*sr);tt=np.arange(n)/sr;env=np.sin(np.linspace(0,np.pi,n))**2
  whoosh=rng.normal(0,1,n)*env*.026
  hit=np.sin(2*np.pi*(80*tt-80*tt*tt))*np.exp(-25*tt)*.045
  a=max(0,round((t-.10)*sr));fx[a:a+n]+=whoosh+hit
 with wave.open(str(V/'effets.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((fx*32767).astype('<i2').tobytes())
 old=json.loads((WORK/'plans.json').read_text(encoding='utf8'));ps=[];use={}
 cadence=[2.5,1.7,2.8,2.1,1.4,2.6]
 for r in rows:
  pool=POOLS[r['chapter']][r['paragraph']];cursor=round(r['start']*30);end=round(r['end']*30);j=0
  while cursor<end:
   idx=pool[j%len(pool)];p=old[idx];available=round(p['end']*30)-round(p['start']*30)
   n=min(round(cadence[(j+r['i'])%len(cadence)]*30),available,end-cursor)
   if end-cursor-n<15 and end-cursor<=available:n=end-cursor
   times=use.get(idx,0);use[idx]=times+1
   # Alternate valid portions of the already reviewed clip, without speed changes.
   at=0 if times%2==0 else max(0,available-n)/30
   ps.append(dict(i=len(ps),paragraph=r['i'],old_plan=idx,start=cursor/30,end=(cursor+n)/30,entree=at,source=p['source'],source_time=p['entree']+at,zone=p['zone']))
   cursor+=n;j+=1
 # Remove two immediate repetitions identified in the visual review.
 for index,old_index in {39:25,205:88}.items():
  if index<len(ps):
   p=old[old_index];ps[index].update(old_plan=old_index,entree=0,source=p['source'],source_time=p['entree'],zone=p['zone'])
 # V4 is a narration correction: retain the reviewed V3 image edit.
 ps=json.loads((WORK/'v3/plans.json').read_text(encoding='utf8'))
 writej(V/'plans.json',ps)
 print('Préparé',len(ps),'plans',round(rate,4),'tempo',chapters,flush=True)

def shot(p):
 dst=V/f'plan-{p["i"]:03}.mp4'
 if dst.exists():return
 frames=round((p['end']-p['start'])*30)
 vf='fps=30,setsar=1'
 if p['old_plan']==3:vf='crop=1280:720:0:200,scale=1920:1080:flags=lanczos,'+vf
 if p['i']%8==4:vf+=f",zoompan=z='1+0.045*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30"
 run(['ffmpeg','-y','-v','error','-threads','1','-ss',str(p['entree']),'-i',WORK/f'plan-{p["old_plan"]:03}.mp4','-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','18','-threads','2',dst])

def render():
 ps=json.loads((V/'plans.json').read_text(encoding='utf8'))
 with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(shot,ps))
 (V/'concat.txt').write_text(''.join(f"file 'plan-{p['i']:03}.mp4'\n" for p in ps),encoding='utf8')
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',V/'concat.txt','-c','copy',V/'muet.mp4'])
 filt="[0:v]ass=sous-titres.ass:fontsdir='../../../../assets/fonts'[sub];[sub][3:v]overlay=0:0[vout];[1:a]highpass=f=65,loudnorm=I=-16:TP=-1.5:LRA=8,asplit=2[v][sc];[2:a]volume=0.09,afade=t=in:d=0.3,afade=t=out:st=479:d=3[m];[m][sc]sidechaincompress=threshold=.02:ratio=6:attack=10:release=180[duck];[v][duck][4:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=.89[a]"
 subprocess.run(['ffmpeg','-y','-v','error','-threads','4','-i','muet.mp4','-i','voix-complete.wav','-stream_loop','-1','-i',str(ROOT/'assets/musique/mixkit/voitures.mp3'),'-i',str(WORK/'logo.png'),'-i','effets.wav','-filter_complex_threads','2','-filter_complex',filt,'-map','[vout]','-map','[a]','-t',str(TOTAL),'-c:v','libx264','-preset','fast','-crf','19','-threads','4','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'essai-long-v4.mp4')],cwd=V,check=True)
 print('V4 EXPORTÉE',flush=True)

def boards():
 ps=json.loads((V/'plans.json').read_text(encoding='utf8'));folder=V/'controle';folder.mkdir(exist_ok=True)
 def grab(p):
  for j,t in enumerate([.03,(p['end']-p['start'])/2,max(.03,p['end']-p['start']-.08)]):
   f=folder/f'p{p["i"]:03}-{j}.jpg'
   if not f.exists():run(['ffmpeg','-y','-v','error','-threads','1','-ss',str(t),'-i',V/f'plan-{p["i"]:03}.mp4','-frames:v','1','-vf','scale=240:135',f])
 with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(grab,ps))
 for k in range(math.ceil(len(ps)/10)):
  im=Image.new('RGB',(720,1550),'#181818');d=ImageDraw.Draw(im)
  for row,p in enumerate(ps[k*10:k*10+10]):
   for j in range(3):im.paste(Image.open(folder/f'p{p["i"]:03}-{j}.jpg'),(240*j,155*row))
   d.text((5,155*row+137),f"{p['i']:03} | {p['start']:.1f}s | source plan {p['old_plan']}",fill='white')
  im.save(folder/f'page-{k:02}.jpg',quality=88)
 print('Planches prêtes',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
