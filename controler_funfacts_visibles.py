"""Index et captures des passages réellement exportés."""
import json,subprocess
from PIL import Image,ImageDraw
from montage_reel import ROOT,run
from rendre_funfacts_visibles import FACTS

sheet=Image.new('RGB',(1800,680),'#181818');draw=ImageDraw.Draw(sheet)
rows=['# Fun facts des cinq vidéos TOP\n','Chaque anecdote est signalée dans le rendu par « FUN FACT », au moment de la narration.\n','| TOP | Vidéo | Comparaison | Passage |','|---|---|---|---|']
audit=json.loads((ROOT/'out/controle-funfacts.json').read_text(encoding='utf-8'))
for i,(n,_) in enumerate(FACTS.items()):
    w=next((ROOT/'out').glob(f'{n}-*'));m=w/'_montage';r=json.loads((m/'controle-funfact-visible.json').read_text(encoding='utf-8'))
    story=json.loads((w/'histoire.json').read_text(encoding='utf-8'));fact=story['fun_fact_affichage'];start,end,lines=fact['debut'],fact['fin'],fact['texte']
    assert r['comparaison_a_jour'] and (w/'comparaison.mp4').stat().st_mtime>=(w/'final.mp4').stat().st_mtime
    p=m/'funfact-apres.png';run(['ffmpeg','-v','error','-y','-ss',str((start+end)/2),'-i',str(w/'final.mp4'),'-frames:v','1','-vf','scale=360:640',str(p)])
    sheet.paste(Image.open(p),(360*i,40));draw.text((360*i+10,10),f'TOP {n} - {start:.1f} s',fill='white')
    info=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'final.mp4')]))
    for a in audit:
        if a['numero']==n:a.update(sha256=r['sha256'],duree=float(info['format']['duration']),comparaison_a_jour=True,funfact=story.get('fun_fact',{}).get('texte',a['funfact']),source=story.get('fun_fact',{}).get('source',a['source']),funfact_visible=dict(debut=start,fin=end,texte=lines))
    rows.append(f'| {n} | [Vidéo](</{(w/"final.mp4").as_posix()}>) | [Comparer](</{(w/"comparaison.mp4").as_posix()}>) | {int(start)//60}:{int(start)%60:02d} — {" / ".join(lines)} |')
sheet.save(ROOT/'out/funfacts-top-apres.jpg')
(ROOT/'out/FUNFACTS-TOP.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
(ROOT/'out/controle-funfacts.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
index=ROOT/'out/LIVRAISON-13-18.md';s=index.read_text(encoding='utf-8');note='Les cinq TOP ont une mention FUN FACT lisible à l’écran. Passages, vidéos et comparaisons : [index des fun facts](FUNFACTS-TOP.md).\n\n'
if note not in s:s=s.replace('\n\n','\n\n'+note,1)
index.write_text(s,encoding='utf-8')
print('Index et captures des cinq exports prêts')
