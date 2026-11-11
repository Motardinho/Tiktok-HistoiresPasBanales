"""Extrait les plans des planches originales et reprend le pipeline du projet."""
import json
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image
import yaml
from narrateur import assemble

ROOT = Path(__file__).resolve().parent
MAPPINGS = {
    'astronautes-sport-en-orbite': [0,3,1,0,2,1,2,3],
    'trois-records-voitures-vitesse': [2,3,0,3,1,2,2,3],
    'villes-plus-lentes-tomtom-2024': [0,3,0,1,2,3,1,2],
}

def prepare(slug):
    work=ROOT/'out'/slug
    sheet=Image.open(work/'planche.png')
    w,h=sheet.size
    for i,panel in enumerate(MAPPINGS[slug]):
        # Extraction des quatre plans, sans retouche des illustrations.
        left=(panel%2)*(w//2)
        top=(panel//2)*(h//2)
        frame=sheet.crop((left,top,left+w//2,top+h//2))
        fw,fh=frame.size
        cw=int(fh*9/16)
        if cw<fw:
            frame=frame.crop(((fw-cw)//2,0,(fw+cw)//2,fh))
        frame.save(work/f'img{i:02d}.png')
    return work

if __name__=='__main__':
    for slug in sys.argv[1:]:
        prepare(slug)
        print('Montage',slug,flush=True)
        subprocess.run([sys.executable,'-m','narrateur','--dossier',slug,'--sans-video'],cwd=ROOT,check=True)
        work=ROOT/'out'/slug
        data=json.loads((work/'histoire.json').read_text(encoding='utf-8'))
        # Les arrondis au nombre d'images peuvent écourter la dernière syllabe.
        # Prolonger le dernier plan, puis laisser -shortest conserver tout l'audio.
        cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
        timing=json.loads((work/'timings.json').read_text(encoding='utf-8'))
        last=len(data['scenes'])-1
        assemble.render_scene(cfg,work,work/f'img{last:02d}.png',None,
                              timing['scene_durations'][-1]+0.5,work/f'scene{last:02d}.mp4')
        assemble.assemble(cfg,work,[work/f'scene{i:02d}.mp4' for i in range(last+1)],
                          work/'voix.mp3',work/'sous-titres.ass',work/'final.mp4',assemble.stamp_time(timing['words']))
        with (work/'publication.txt').open('a',encoding='utf-8') as f:
            f.write('\n\nLabel IA à activer. Visuels synthétiques illustratifs, pas des archives.\nSources consultées : voir verification.md.\n')
        print('TERMINÉ',slug,flush=True)
