"""Repère les changements de plan d'une source à l'intérieur de chaque plan monté."""
import json,subprocess,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'assets/49-vitesse-sans-moteur'
plans=json.loads((R/'out/49-top-3-records-vitesse-sans-moteur/plans.json').read_text(encoding='utf8'))
only={int(x) for x in sys.argv[1:]}
for p in plans:
    if only and p['numero'] not in only:continue
    r=subprocess.run(['ffmpeg','-hide_banner','-ss',str(p['entree']),'-t',str(p['duration']),'-i',str(A/p['source']),'-vf',"scale=320:-2,select='gt(scene,0.28)',showinfo",'-an','-f','null','-'],capture_output=True,text=True)
    cuts=[round(float(m)+p['entree'],2) for m in re.findall(r'pts_time:([\d.]+)',r.stderr)]
    if cuts:print(p['numero'],p['source'],'entrée',p['entree'],'durée',round(p['duration'],2),'coupes source',cuts)
