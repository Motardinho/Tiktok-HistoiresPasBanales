"""Propose pour chaque plan une entrée qui tient dans un seul plan de la source."""
import json,subprocess,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'assets/49-vitesse-sans-moteur'
plans=json.loads((R/'out/49-top-3-records-vitesse-sans-moteur/plans.json').read_text(encoding='utf8'))
def cuts(src,a,b):
    r=subprocess.run(['ffmpeg','-hide_banner','-ss',str(max(a,0)),'-t',str(b-max(a,0)),'-i',str(A/src),'-vf',"scale=320:-2,select='gt(scene,0.28)',showinfo",'-an','-f','null','-'],capture_output=True,text=True)
    return [float(m)+max(a,0) for m in re.findall(r'pts_time:([\d.]+)',r.stderr)]
for n in map(int,sys.argv[1:]):
    p=plans[n];a,b=p['entree']-20,p['entree']+20;c=[max(a,0)]+cuts(p['source'],a,b)+[b]
    segs=[(x,y) for x,y in zip(c,c[1:]) if y-x>=p['duration']+.12]
    best=min(segs,key=lambda s:0 if s[0]<=p['entree']<=s[1] else min(abs(s[0]-p['entree']),abs(s[1]-p['entree'])))
    e=max(best[0]+.06,min(p['entree'],best[1]-p['duration']-.06))
    print(n,p['source'],'entrée',p['entree'],'->',round(e,2),'segment',[round(x,2) for x in best],'durée',round(p['duration'],2))
