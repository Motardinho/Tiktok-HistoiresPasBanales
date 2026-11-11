"""Remplace les seules fins de narration par la signature Histoires pas banales."""
import copy,json,shutil,sys
from pathlib import Path
import yaml
from narrateur import voice
from montage_reel import ROOT,run
from habillage_reference import ITEMS,layers,subs,compare

ENDINGS={
 'astronautes-sport-en-orbite':'Se peser en rebondissant. Tu l’aurais deviné ? Pas banal, hein ?',
 'trois-records-voitures-vitesse':'Un chiffre fou, ça se vérifie. Tu choisis laquelle ? Pas banal, hein ?',
 'villes-plus-lentes-tomtom-2024':'Où as-tu connu ton pire bouchon ? Pas banal, hein ?'}

def prepare(slug):
 w=ROOT/'out'/slug
 backup=w/'avant-chute-hpb-v8';backup.mkdir(exist_ok=True)
 for name in ['histoire.json','timings.json','voix.mp3']:
  if not (backup/name).exists():shutil.copy2(w/name,backup/name)
 data=json.loads((backup/'histoire.json').read_text(encoding='utf-8'))
 old=json.loads((backup/'timings.json').read_text(encoding='utf-8'))
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
 tail=w/'chute-hpb-v8.mp3';timing_path=w/'chute-timings-hpb-v8.json'
 if tail.exists() and timing_path.exists():new=json.loads(timing_path.read_text(encoding='utf-8'))
 elif slug=='villes-plus-lentes-tomtom-2024':
  # Réutiliser la question déjà dite et la signature nouvellement enregistrée,
  # dans la même voix. Pas de nouvelle requête payante pour cette troisième fin.
  q_start=62.107;q_end=63.96
  astro=ROOT/'out/astronautes-sport-en-orbite'
  sig=json.loads((astro/'chute-timings-hpb-v8.json').read_text(encoding='utf-8'))
  sig_words=next(i for i,x in enumerate(sig['words']) if x['w']=='Pas')
  begin=sig['words'][sig_words]['start']-0.025
  run(['ffmpeg','-v','error','-y','-i',str(backup/'voix.mp3'),'-i',str(astro/'chute-hpb-v8.mp3'),'-filter_complex',f'[0:a]atrim=start={q_start}:end={q_end},asetpts=PTS-STARTPTS[q];[1:a]atrim=start={begin},asetpts=PTS-STARTPTS[s];[q][s]concat=n=2:v=0:a=1[a]','-map','[a]','-c:a','libmp3lame','-b:a','128k',str(tail)])
  words=[dict(w=x['w'],start=x['start']-q_start,end=x['end']-q_start) for x in old['words'] if q_start<=x['start']<q_end]
  words += [dict(w=x['w'],start=x['start']-begin+q_end-q_start,end=x['end']-begin+q_end-q_start) for x in sig['words'][sig_words:]]
  new=dict(words=words,duration=q_end-q_start+sig['duration']-begin)
  new['scene_durations']=[new['duration']]
  timing_path.write_text(json.dumps(new,ensure_ascii=False),encoding='utf-8')
 else:
  new=voice.synthesize(cfg,[{'narration':ENDINGS[slug]}],tail)
  timing_path.write_text(json.dumps(new,ensure_ascii=False),encoding='utf-8')
 cut=sum(old['scene_durations'][:-1])
 run(['ffmpeg','-v','error','-y','-i',str(backup/'voix.mp3'),'-i',str(tail),'-filter_complex',f'[0:a]atrim=0:{cut:.6f},asetpts=PTS-STARTPTS[h];[1:a]asetpts=PTS-STARTPTS[t];[h][t]concat=n=2:v=0:a=1[a]','-map','[a]','-c:a','libmp3lame','-b:a','128k',str(w/'voix-hpb-v8.mp3')])
 new_t=dict(scene_durations=old['scene_durations'][:-1]+[new['duration']],words=[x for x in old['words'] if x['start']<cut],duration=cut+new['duration'])
 new_t['words'] += [dict(w=x['w'],start=x['start']+cut,end=x['end']+cut) for x in new['words']]
 data['scenes'][-1]['narration']=ENDINGS[slug]
 data['hashtags']=[x.replace('#DossiersHorsNormes','#HistoiresPasBanales') for x in data['hashtags']]
 (w/'histoire-hpb-v8.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (w/'timings-hpb-v8.json').write_text(json.dumps(new_t,ensure_ascii=False),encoding='utf-8')
 print(slug,'nouvelle chute générée',round(new['duration'],2),'s',flush=True)

def render(slug):
 w=ROOT/'out'/slug
 t=json.loads((w/'timings-hpb-v8.json').read_text(encoding='utf-8'))
 cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
 cfg['render'].update(subtitle_size=88,words_per_caption=5,subtitle_wrap=19)
 layers(w,ITEMS[slug]);subs(w,t,ITEMS[slug],cfg)
 dur=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(w/'voix-hpb-v8.mp3')]))['format']['duration'])
 graph=('[0:v]tpad=stop_mode=clone:stop_duration=10,ass=sous-titres-reference.ass:fontsdir=.[cap];'
        '[3:v]format=rgba,fade=t=out:st=3.8:d=0.2:alpha=1[hook];'
        '[cap][hook]overlay=0:0:enable=lt(t\\,4):shortest=1[h];[h][2:v]overlay=0:0:shortest=1[v]')
 run(['ffmpeg','-v','error','-y','-i','base-reference.mp4','-i','voix-hpb-v8.mp3','-loop','1','-framerate','30','-i','header-footer-reference.png','-loop','1','-framerate','30','-i','titre-hook-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(dur),'-c:v','libx264','-preset','fast','-crf','19','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','final-hpb-v8.mp4'],w)
 run(['ffmpeg','-v','error','-i',str(w/'final-hpb-v8.mp4'),'-f','null','-'])
 compare(slug,w,dur,version=8)
 for src,dst in [('voix-hpb-v8.mp3','voix.mp3'),('timings-hpb-v8.json','timings.json'),('histoire-hpb-v8.json','histoire.json'),('final-hpb-v8.mp4','final.mp4'),('comparaison-hpb-v8.mp4','comparaison.mp4')]:shutil.copy2(w/src,w/dst)
 info=dict(version='HPB v8 chute orale',chute=ENDINGS[slug],ancienne_signature=False,header_footer='permanents',miroir=False,voix='même voix ElevenLabs ; seule la dernière scène a été régénérée',timings='nouveaux timings de fin ; reste de la narration conservé',validation='Décodage intégral réussi ; contrôle de la fin à compléter.')
 for name in ['controle.json','controle-hpb-v8.json']:(w/name).write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug,'vidéo et comparaison v8 prêtes',flush=True)

if __name__=='__main__':
 mode,*slugs=sys.argv[1:]
 for slug in slugs or ENDINGS:
  if mode=='prepare':prepare(slug)
  else:render(slug)
