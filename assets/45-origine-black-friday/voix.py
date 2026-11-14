import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from produire_lot_16_18 import speech
p=ROOT/'out/45-origine-black-friday';d=json.loads((p/'histoire.json').read_text(encoding='utf8'))
url='https://moodmedia.com/be-fr/blog-be-fr/la-grande-histoire-derriere-le-black-friday/'
if not any(s['url']==url for s in d['sources_a_verifier']): d['sources_a_verifier'].append(dict(fait='Source fournie par Marc : récit Philadelphie, Big Friday, réinterprétation comptable ; source secondaire citant HISTORY',url=url))
d['tiktokabilite'].update(verdict='adapté sous réserve',preuves=['reuters.jpg : foule et magasins, séquences Nutella et métro exclues','police.jpg : police de Philadelphie vers 1960, cérémonie et non Black Friday','football.jpg : Army-Navy, 1961 ; contexte du rendez-vous sportif, pas le lendemain de Thanksgiving 1961','philadelphie.jpg : marchés, datation large années 1960-1970 ; ne pas dater une prise précise de 1961','moderne.jpg : vrai Black Friday Ontario Mills, source 4K'],limites='Archives anciennes en faible définition. Archives de contexte, aucun film du premier Black Friday. Variante photos : photographies de presse et photogrammes documentaires identifiés. Contrôle final non encore réalisé.')
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
speech(p)
