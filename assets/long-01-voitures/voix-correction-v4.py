from production import *
import yaml,shutil
from narrateur.voice import synthesize
v=WORK/'v4';old=WORK/'v3'
cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
h=json.loads((v/'histoire-travail.json').read_text(encoding='utf-8'))
for name in ['ssc','bugatti','yangwang']:
 fn='voix.mp3' if name=='ssc' else f'voix-{name}.mp3';tn='timings.json' if name=='ssc' else f'timings-{name}.json'
 if name=='bugatti':
  shutil.copy2(old/fn,v/fn);shutil.copy2(old/tn,v/tn);continue
 oral=(OUT/f'script-{name}-v4.txt').read_text(encoding='utf-8').strip()
 for a,b in h['prononciations'].items():oral=oral.replace(a,b)
 (v/f'texte-voix-{name}.txt').write_text(oral,encoding='utf-8')
 raw=v/f'brut-{name}.mp3';tp=v/f'brut-{name}.json'
 if not raw.exists():writej(tp,synthesize(cfg,[{'narration':oral}],raw))
 target=float(probe(old/fn)['format']['duration']);actual=float(probe(raw)['format']['duration']);rate=actual/target
 run(['ffmpeg','-y','-v','error','-i',raw,'-af',f'atempo={rate},apad,atrim=duration={target}','-c:a','libmp3lame','-b:a','192k',v/fn])
 data=json.loads(tp.read_text(encoding='utf-8'))
 for w in data['words']:w['start']/=rate;w['end']/=rate
 data['duration']=target;writej(v/tn,data)
 print(name,'généré',rate,flush=True)
