from production import *
ps=json.loads((WORK/'plans.json').read_text(encoding='utf8'))
entries={4:12,13:47,15:90,16:102,23:42,26:72,28:36,33:17,35:56,114:40}
for i,t in entries.items():
 ps[i]['source']='assets/long-01-voitures/grg-br4sKUw.mp4';ps[i]['entree']=t;ps[i]['zone']='eq=brightness=0.015:gamma=1.12,'
for i,t in {14:1,25:5,34:8}.items():
 ps[i]['source']='assets/long-01-voitures/ywdcgVUWffY.mp4';ps[i]['entree']=t;ps[i]['zone']=''
ps[0]['entree']=38.7
ps[1].update(source='assets/sources-reelles/road.mp4' if False else 'assets/sources-reelles/ssc-road.mp4',entree=1.4)
changed=list(entries)+[14,25,34,0,1]
for i in changed:
 f=WORK/f'plan-{i:03}.mp4'
 if f.exists():f.unlink()
 for j in range(3):
  f=WORK/'controle'/f'p{i:03}-{j}.jpg'
  if f.exists():f.unlink()
assert not any('KXY' in p['source'] for p in ps)
writej(WORK/'plans.json',ps)
writej(WORK/'correction-identite.json',{'source_exclue':'KXYkDkrF3rk - description mentionne Tuatara Striker','remplacements_officiels':['grg-br4sKUw','ywdcgVUWffY'],'plans':changed})
print(changed)
