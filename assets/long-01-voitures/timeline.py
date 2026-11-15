from production import *
from PIL import Image
import wave,numpy as np
def clean(s):return re.sub(r"[^\w]+",' ',s.lower()).strip()
def prepare():
 raw=json.loads((WORK/'timings-oraux.json').read_text(encoding='utf-8'));story=json.loads((OUT/'histoire.json').read_text(encoding='utf-8'))
 words=raw['words'];tokens=[clean(w['w']) for w in words]
 paras=(OUT/'script.txt').read_text(encoding='utf-8').strip().split('\n\n');cursor=0;rows=[]
 for i,p in enumerate(paras):
  oral=p
  for a,b in story['prononciations'].items():oral=oral.replace(a,b)
  target=[clean(x) for x in oral.split()[:5]]
  found=next((j for j in range(cursor,len(tokens)-len(target)) if tokens[j:j+len(target)]==target),None)
  if found is None:raise ValueError((i,target))
  rows.append({'i':i,'start_raw':words[found]['start'],'word_index':found,'texte':p});cursor=found+1
 # Nine short breaths at paragraph boundaries, maintaining the original performance speed of video.
 gap_indices=[6,10,14,18,22,26,28,30,32]
 gaps=[rows[i]['start_raw'] for i in gap_indices if i<len(rows)]
 rate=.90
 def mapstart(t):return t/rate+2*sum(g<=t+.00001 for g in gaps)
 def mapend(t):return t/rate+2*sum(g<t-.00001 for g in gaps)
 mapped=[dict(w,start=mapstart(w['start']),end=mapend(w['end'])) for w in words]
 total=raw['duration']/rate+2*len(gaps)
 for i,r in enumerate(rows):
  r['start']=mapstart(r['start_raw']);r['end']=mapstart(rows[i+1]['start_raw']) if i+1<len(rows) else total
 writej(WORK/'paragraphes.json',rows);writej(WORK/'timings.json',{'words':mapped,'duration':total,'pauses_source':gaps,'tempo_voix':rate})
 # Decode once, slow speech without changing pitch, and insert precisely timed silences.
 edges=[0]+gaps+[raw['duration']]; filters=[];labels=[]
 for i,(a,b) in enumerate(zip(edges,edges[1:])):
  filters.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,atempo={rate}[a{i}]');labels.append(f'[a{i}]')
  if i<len(edges)-2:filters.append(f'anullsrc=r=44100:cl=mono,atrim=duration=2[s{i}]');labels.append(f'[s{i}]')
 filters.append(''.join(labels)+f'concat=n={len(labels)}:v=0:a=1[voice]')
 (WORK/'audio-filter.txt').write_text(';'.join(filters),encoding='utf-8')
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',WORK/'voix.wav','-filter_complex',';'.join(filters),'-map','[voice]','-ar','48000','-c:a','pcm_s16le',WORK/'voix-longue.wav'])
 print('DURATION',total)
 for r in rows:print(r['i'],round(r['start'],1),round(r['end'],1),r['texte'][:85])
 # Captions restore proper spellings and numerals from the synthesized pronunciations.
 from monter_lot_21_23 import caption_words
 replacements={v:k for k,v in story['prononciations'].items()}
 replacements.update({'numéro trois':'N°3','numéro deux':'N°2','numéro un':'N°1','quatre cent soixante-quatorze virgule huit':'474,8','quatre cent quatre-vingt-dix virgule quarante-huit':'490,48','quatre cent quatre-vingt-seize virgule vingt-deux':'496,22','cinq cent trois virgule dix-sept':'503,17','deux cent quatre-vingt-quinze':'295','quatre cent quatre-vingt-dix':'490','cinq cent onze':'511','cinq cent trois':'503','trois mille':'3 000','mille six cents':'1 600','cent trente-deux':'132','cent trente-six':'136','cent quarante':'140','six cent soixante':'660','deux mille vingt-deux':'2022','deux mille dix-neuf':'2019','deux mille vingt-cinq':'2025','deux mille vingt-six':'2026','vingt-cinq':'25','trois cents plus':'300+','trois cents':'300','deux cents':'200','cinq cents':'500','kilomètres-heure':'KM/H','u neuf':'U9','w seize':'W16','trente exemplaires':'30 exemplaires'})
 cap=caption_words(mapped,replacements)
 from narrateur.assemble import _ass_time
 header='[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Default,Poppins ExtraBold,80,&H00FFFFFF,&H00FFFFFF,&H00100F0D,&H80000000,0,0,0,0,100,100,0,0,1,3.5,1.5,2,100,100,72,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
 groups=[];buf=[]
 for w in cap:
  if buf and (len(buf)>=5 or len(' '.join(x['w'] for x in buf+[w]))>40 or w['start']-buf[-1]['end']>.8):groups.append(buf);buf=[]
  buf.append(w)
  if re.search(r'[.!?]$',w['w']):groups.append(buf);buf=[]
 if buf:groups.append(buf)
 events=[];srt=[]
 for idx,g in enumerate(groups):
  end=min(g[-1]['end']+.25,groups[idx+1][0]['start']) if idx+1<len(groups) else min(total,g[-1]['end']+.4)
  for j,w in enumerate(g):
   finish=g[j+1]['start'] if j+1<len(g) else end
   text=' '.join((r'{\c&H47E4FF&}'+v['w']+r'{\c&HFFFFFF&}') if j==k else v['w'] for k,v in enumerate(g))
   events.append(f'Dialogue: 0,{_ass_time(w["start"])},{_ass_time(finish)},Default,,0,0,0,,{text}')
  def st(t):
   ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
  srt.append(f'{idx+1}\n{st(g[0]["start"])} --> {st(end)}\n'+ ' '.join(x['w'] for x in g)+'\n')
 (WORK/'sous-titres.ass').write_text(header+'\n'.join(events),encoding='utf-8');(OUT/'sous-titres.srt').write_text('\n'.join(srt),encoding='utf-8')
 logo=Image.open(ROOT/'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.png').convert('RGBA');logo.thumbnail((166,166))
 layer=Image.new('RGBA',(1920,1080));layer.alpha_composite(logo,(1718,25));layer.save(WORK/'logo.png')
if __name__=='__main__':prepare()
