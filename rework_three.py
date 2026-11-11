"""Version avec de vraies séquences, proches de celles des posts de référence."""
import json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import yaml
from narrateur.voice import synthesize

ROOT=Path(__file__).resolve().parent
ITEMS=[
 ('astronautes-sport-en-orbite','Se peser dans l’espace','SE PESER DANS L’ESPACE ?',[
  'Dans l’espace, cette machine ne sert pas à faire du sport. Les astronautes s’y balancent pour mesurer leur masse. Mais comment est-ce possible ?',
  'Une balance de salle de bain mesure la force exercée sur elle. En orbite, en microgravité, cette méthode ne fonctionne plus comme sur Terre.',
  'Pourtant, ton corps contient toujours la même matière. Ta masse existe encore, même quand tu flottes. Il faut simplement la mesurer d’une autre façon.',
  'L’appareil utilise un ressort. L’astronaute se place sur le support, puis l’ensemble oscille. La fréquence de ce mouvement dépend de la masse installée dessus.',
  'Regarde la différence : avec une personne, les oscillations sont plus lentes. Sans elle, le dispositif est plus léger et bouge beaucoup plus vite.',
  'Dans sa démonstration, l’astronaute canadien David Saint-Jacques explique que cette mesure se fait une fois par mois. Elle aide à suivre leur santé.',
  'C’est important pendant les longues missions. La microgravité modifie le travail des muscles et des os. Les équipes surveillent donc l’état physique des équipages.',
  'Ce mouvement étrange est donc une sorte de pesée adaptée à l’espace. Tu aurais deviné son rôle ? Dossier clos. Mais l’histoire, elle, reste hors normes.'
 ],[
  'Agence spatiale canadienne, David Saint-Jacques, 21 juin 2019 : pesée mensuelle, oscillation du ressort, masse et fréquence. https://www.asc-csa.gc.ca/eng/multimedia/search/video/18332',
  'NASA, exercice et effets de la microgravité sur muscles et os. https://www.nasa.gov/missions/station/iss-research/astronaut-exercise/'
 ], [('astronautes-masse',24),('astronautes-masse',0),('astronautes-masse',9),('astronautes-masse',21),('astronautes-masse',51),('astronautes-masse',31),('astronautes-masse',42),('astronautes-masse',57)]),
 ('trois-records-voitures-vitesse','Trois hypercars hors normes','F5 • CHIRON • BOLIDE',[
  'Trois hypercars. Mais leurs chiffres cachent un piège.',
  'La Hennessey Venom F cinq vient du Texas. Son moteur est un V huit biturbo.',
  'À son lancement, elle annonce mille huit cent dix-sept horsepower. La puissance ne prouve pourtant pas un record de vitesse.',
  'Un record exige une mesure. Il faut aussi savoir dans quelles conditions elle a été faite.',
  'Le prototype Chiron Super Sport trois cents plus dépasse les quatre cent quatre-vingt-dix kilomètres heure en deux mille dix-neuf. Dans un seul sens.',
  'La Bugatti Bolide, elle, est réservée au circuit. On change donc de terrain de jeu.',
  'Le modèle client annonce trois cent quatre-vingts kilomètres heure à faible appui. Pas cinq cents.',
  'Puissance, pointe et circuit : compare les critères avant les chiffres. Tu choisis laquelle ? Dossier clos.'
 ],[
  'Hennessey : F5, Texas, V8 biturbo 6,6 l, 1817 hp à la présentation. https://www.hennesseyspecialvehicles.com/venom-f5/',
  'Bugatti : prototype Chiron, 2019, 490,484 km/h en un sens. https://newsroom.bugatti.com/press-releases/bugatti-chiron-super-sport-300-plus',
  'Bugatti : Bolide client circuit, 380 km/h en faible appui, priorité au comportement. https://newsroom.bugatti.com/press-releases/redefining-the-performance-experience-with-the-bugatti-bolide-1'
 ], [('bugatti-bolide',0),('hennessey-f5',96),('hennessey-f5',40),('hennessey-f5',112),('bugatti-record',80),('bugatti-bolide',8),('bugatti-bolide',16),('bugatti-bolide',24)]),
 ('villes-plus-lentes-tomtom-2024','Londres, New York, Paris : les heures perdues','LONDRES • NEW YORK • PARIS',[
  'Londres, New York, Paris. Dans ces grandes villes, les embouteillages prennent bien plus que quelques minutes. Ils peuvent engloutir l’équivalent de plusieurs journées par an.',
  'Regardons les données INRIX pour deux mille vingt-quatre. Le chiffre mesure les heures perdues dans la congestion par conducteur, selon la méthode du rapport.',
  'À Londres, le total atteint cent une heures sur l’année. Les célèbres bus rouges ne sont donc pas les seuls à avancer au rythme du trafic.',
  'À New York, on monte à cent deux heures. Imagine passer ce temps supplémentaire derrière un volant, simplement parce que la circulation ralentit ton trajet.',
  'À Paris, le rapport indique quatre-vingt-dix-sept heures. Ce sont des heures perdues dans les bouchons, pas la durée complète de tous les déplacements.',
  'Attention au classement : ces trois villes ne constituent pas le podium mondial du rapport. Elles illustrent le même problème dans trois grandes métropoles.',
  'Et une moyenne ne prédit pas ton trajet personnel. Selon l’heure et l’itinéraire, ton expérience peut être très différente de celle décrite par ces chiffres.',
  'Retenir la source, l’année et le critère change la lecture d’un top. Où as-tu connu ton pire bouchon ? Dossier clos. Dis-moi ton numéro un en commentaire.'
 ],[
  'INRIX Global Traffic Scorecard 2024, publié le 6 janvier 2025 : Londres 101 h, New York 102 h, Paris 97 h, heures perdues ; pas un podium mondial de ces seules villes. https://inrix.com/press-releases/2024-global-traffic-scorecard-uk/'
 ], [('londres',0),('londres',6),('londres',12),('new-york-bouchons',0),('paris-soir',3),('new-york-bouchons',0),('paris-soir',16),('londres',18)]),
]

def prepare(item):
 slug,title,fixed,texts,sources,clips=item
 work=ROOT/'out'/slug
 data=json.loads((work/'histoire.json').read_text(encoding='utf-8'))
 archive=work/'premiere-version-ia'
 archive.mkdir(exist_ok=True)
 for name in ['histoire.json','voix.mp3','timings.json','final.mp4','publication.txt','verification.md','sous-titres.ass']:
  p=work/name
  if p.exists() and not (archive/name).exists():shutil.copy2(p,archive/name)
 data.update(titre=title,titre_fixe=fixed,hook=texts[0],format='histoire',sources_a_verifier=sources)
 data['scenes']=[dict(narration=t,animate=False,image_prompt='Séquence réelle : '+clips[i][0],motion_prompt='') for i,t in enumerate(texts)]
 if 'voitures' in slug:
  data['scenes'][3]['bandeau']='PUISSANCE ≠ RECORD MESURÉ'
  data['scenes'][6]['bandeau']='BOLIDE CLIENT : 380 KM/H'
 if 'villes' in slug:data['scenes'][1]['bandeau']='INRIX • DONNÉES 2024'
 data['legende']=title+'. Tu en pensais quoi ?'
 (work/'histoire.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (work/'verification.md').write_text('# Version avec séquences réelles\n\nTexte original, sujets des posts de référence. Sources consultées le 7 novembre 2026.\n\n'+'\n\n'.join(sources)+'\n\nLes images proviennent de séquences identiques ou proches, sans les sous-titres des posts. Voir sources-visuelles.json. Aucune illustration IA dans cette version.\n',encoding='utf-8')
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
 # La narration ayant changé, audio et timings sont régénérés ensemble.
 t=synthesize(cfg,data['scenes'],work/'voix-v2.mp3')
 (work/'timings-v2.json').write_text(json.dumps(t,ensure_ascii=False),encoding='utf-8')
 shutil.copy2(work/'voix-v2.mp3',work/'voix.mp3')
 shutil.copy2(work/'timings-v2.json',work/'timings.json')
 (work/'sources-visuelles.json').write_text(json.dumps([dict(scene=i,fichier=n+'.mp4',debut_s=start) for i,(n,start) in enumerate(clips)],ensure_ascii=False,indent=2),encoding='utf-8')
 print(slug,len(' '.join(texts).split()),'mots',t['duration'],'s',flush=True)

if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(prepare,ITEMS))
