from production import *
import yaml
from narrateur.voice import synthesize
v=WORK/'v5';v.mkdir(exist_ok=True)
t="À cette vitesse, n'importe quelle ligne droite devient trop courte."
writej(v/'hook-timings.json',synthesize(yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf8')),[{'narration':t}],v/'hook.mp3'))
print(probe(v/'hook.mp3')['format']['duration'])
