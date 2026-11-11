"""Rattache les deux-points avant découpage et réexporte les vidéos existantes sans changer la voix."""
import copy
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yaml
from montage_reel import ROOT
from narrateur import assemble
from produire_lot_16_18 import read
from revision_spectaculaire import stage_for
from resserrer_titres import revise

def update(w):
    n=int(w.name[:2]);m=stage_for(w)/'_montage' if n>=16 else w/'_montage'
    p=m/'sous-titres-reference.ass';old=p.read_text(encoding='utf-8')
    backup=m/'sous-titres-avant-deux-points.ass'
    if not backup.exists():backup.write_text(old,encoding='utf-8')
    cfg=copy.deepcopy(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8')))
    cfg['render'].update(subtitle_size=83 if n>=16 else 88,words_per_caption=5,subtitle_wrap=20)
    assemble.YELLOW='&H4AE2FF&';assemble.RED='&H4E62FF&'
    tmp=m/'sous-titres-deux-points.ass';assemble.write_subtitles(cfg,read(m/'timings.json')['words'],tmp)
    def seconds(s):
        h,mi,se=s.split(':');return int(h)*3600+int(mi)*60+float(se)
    new=[]
    for line in tmp.read_text(encoding='utf-8').splitlines():
        if not line.startswith('Dialogue:'):continue
        parts=line.split(',',9)
        if seconds(parts[2])<=4:continue
        if seconds(parts[1])<4:parts[1]='0:00:04.00'
        new.append(','.join(parts))
    keep=[line for line in old.splitlines() if not (line.startswith('Dialogue:') and line.split(',',4)[3]=='Default')]
    p.write_text('\n'.join(keep+new)+'\n',encoding='utf-8')
    revise(w)

if __name__=='__main__':
    folders=[w for w in sorted((ROOT/'out').iterdir()) if w.is_dir() and w.name[:2] in ['13','14','15','17','18']]
    with ThreadPoolExecutor(max_workers=2) as executor:list(executor.map(update,folders))
