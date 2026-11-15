from montage import *
def correct():
 old=json.loads((WORK/'plans.json').read_text(encoding='utf8'));plans();ps=json.loads((WORK/'plans.json').read_text(encoding='utf8'))
 changes={
 2:('road',1.3),4:('pov',3),9:('ssc',139),10:('ssc',36),11:('ssc',43),12:('ssc',160),
 17:('speed',38),19:('ssc',57),20:('ssc',44),27:('ssc',139),30:('ssc',160),31:('speed',21),
 40:('bug',25),41:('bug',67),42:('bug',59),
 77:('yang',60),78:('new',203.2),79:('film',153),81:('yang',37),83:('yang',51),87:('film',437),
 88:('new',184),89:('record',70),91:('new',194),93:('new',188),94:('record',83),
 95:('new',188),96:('film',101),97:('new',194),98:('record',60),
 104:('new',194),105:('new',203.3),106:('record',114),107:('new',215),
 112:('new',203.2),113:('record',120),116:('film',101),117:('yang',62),118:('new',203.3),121:('yang',54),
 }
 for i,(key,at) in changes.items():
  ps[i]['source'],ps[i]['zone']=SOURCES[key];ps[i]['entree']=at
 for p in ps:
  if p['zone']=='crop=1920:600:0:340,':p['zone']='crop=1920:480:0:440,'
  if p['i']==38:p['zone']=''
 changed=[p['i'] for p,o in zip(ps,old) if p!=o or p['i'] in [15,30,45,49,55,72,83,115]]
 writej(WORK/'plans.json',ps);writej(WORK/'corrections-plans.json',{'plans_modifies':changed,'raison':'raccords, pilote nommé, retrait des cartons tiers, recadrage des vues composites, effets demandés'})
 for i in changed:
  f=WORK/f'plan-{i:03}.mp4'
  if f.exists():f.unlink()
  for j in range(3):
   f=WORK/'controle'/f'p{i:03}-{j}.jpg'
   if f.exists():f.unlink()
 print('A recalculer',changed)
if __name__=='__main__':correct()
