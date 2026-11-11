"""Corriger le doublon de sous-titre « 4 4 moteurs », sans modifier l'audio."""
import shutil
from revision_hpb_v11 import CAR,ROOT,read,save,item_for,export
from revision_hpb_v10 import dedupe_overlapping_words


def main():
    w=ROOT/'out'/CAR
    t=read(w/'timings-hpb-v13.json')
    before=len(t['words'])
    t['words']=dedupe_overlapping_words(t['words'])
    assert before-len(t['words'])==1
    assert '4 4 moteurs' not in ' '.join(x['w'] for x in t['words'])
    assert '4 moteurs' in ' '.join(x['w'] for x in t['words'])
    save(w/'timings-hpb-v14.json',t)
    starts=[sum(t['scene_durations'][:i]) for i in range(len(t['scene_durations']))]
    item=item_for(CAR,t,starts)
    item['facts']=[(a,b,s.replace('490,484','490,48')) for a,b,s in item['facts']]
    export(CAR,w,t,item,'mix-hpb-v13.wav','base-hpb-v13.mp4',version=14)
    save(w/'timings.json',t)
    control=read(w/'controle-hpb-v13.json')
    control.update(read(w/'controle-hpb-v14.json'))
    control['correction']='Doublon de mot aligné retiré : 4 moteurs, audio et plans conservés'
    save(w/'controle-hpb-v14.json',control)
    shutil.copy2(w/'montage-hpb-v13.json',w/'montage-hpb-v14.json')
    print('v14 : 4 moteurs, durée inchangée',t['duration'],flush=True)


if __name__=='__main__':main()
