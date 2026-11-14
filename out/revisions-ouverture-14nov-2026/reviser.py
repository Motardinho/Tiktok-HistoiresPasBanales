from pathlib import Path
import subprocess, json, shutil, hashlib
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
REF=ROOT/'out/20-telephone-2899-dollars/version-validee/final.mp4'
JOBS=[(27,'27-demi-tour-dans-la-tempete',53),(28,'28-om-a-achete-un-match',182)]
def run(args):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def duration(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True))
def render(job):
    n,name,frames=job; start=frames/30; src=ROOT/'out'/name; dst=OUT/str(n);dst.mkdir(exist_ok=True)
    final=dst/'final.mp4'
    run(['-ss',start,'-i',src/'final.mp4','-map','0:v:0','-map','0:a:0',*(['-vf','trim=start_frame=1,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=0.033333333'] if n==28 else []),'-c:v','libx264','-preset','fast','-crf','18','-threads','4','-c:a','aac','-b:a','192k','-af','afade=t=in:st=0:d=0.008','-movflags','+faststart',final])
    dur=duration(final); assert dur>60,dur
    total=max(dur,duration(REF))
    graph=f'[0:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[l];[1:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[r];[l][r]hstack=inputs=2[v];[0:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a0];[1:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a1]'
    run(['-i',REF,'-i',final,'-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','[a1]','-map','[a0]','-c:v','libx264','-preset','fast','-crf','21','-threads','4','-c:a','aac','-b:a','128k','-metadata:s:a:0','title=HPB nouvelle version','-metadata:s:a:1','title=Reference telephones','-disposition:a:0','default','-disposition:a:1','0','-movflags','+faststart',dst/'comparaison.mp4'])
    run(['-i',final,'-t','8','-vf','scale=360:640','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac',dst/'ouverture.mp4'])
    run(['-i',final,'-t','8','-vn','-ac','1','-ar','24000',dst/'ouverture-finale.wav'])
    for t in [0,0.1,1,2,3,4,5,8,dur-1]:
        run(['-ss',t,'-i',final,'-frames:v','1','-vf','scale=360:640',dst/f'controle-{t:.1f}.jpg'])
    run(['-ss','1','-i',dst/'comparaison.mp4','-frames:v','1',dst/'comparaison-controle.jpg'])
    for f in ['final.mp4','comparaison.mp4']:
        run(['-i',dst/f,'-map','0:v','-map','0:a','-f','null','-'])
    for f in ['publication.txt','legende.txt','CREDITS.md']:
        shutil.copy2(src/f,dst/f)
    story=json.loads((src/'histoire.json').read_text(encoding='utf-8-sig'))
    story['revision_ouverture']={'date':'2026-11-14','source':str(src/'final.mp4'),'coupe_secondes':start,'lecture_titre':False,'regeneration_voix':False}
    story['reference_fichier']=str(REF)
    (dst/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
    words=json.loads((src/'_montage/timings-oraux.json').read_text(encoding='utf-8'))['words']
    words=[dict(w,start=round(max(0,w['start']-start),3),end=round(w['end']-start,3)) for w in words if w['end']>start]
    (dst/'timings-oraux.json').write_text(json.dumps({'words':words},ensure_ascii=False,indent=2),encoding='utf-8')
    (dst/'script.txt').write_text(' '.join(w['w'] for w in words)+'\n',encoding='utf-8')
    result={'numero':n,'dossier_source':name,'coupe_secondes':start,'duree':dur,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'reference':str(REF),'statut':'a_visionner','controles_techniques':'decodage integral video et pistes audio sans erreur ; comparaison deux pistes, HPB par defaut','audio':'piste existante conservee apres coupe ; fondu 8 ms au depart ; ecoute humaine non effectuee par cet outil'}
    (dst/'controle-livraison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return result
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(render,JOBS))
    (OUT/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
