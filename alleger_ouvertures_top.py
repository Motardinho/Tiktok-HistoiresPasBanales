"""Une ouverture lisible : titre seul, puis rang et sous-titres. Corps et fun facts conservés."""
import json,re,shutil,hashlib
from concurrent.futures import ThreadPoolExecutor
from montage_reel import ROOT,run
from habillage_reference import layers
from comparer_lot_16_18 import compare
from narrateur.assemble import _ass_time

STAGES={15:'revision-donnees-2025-rapide-v15',16:'revision-spectaculaire-v9',17:'revision-spectaculaire-v4',18:'revision-spectaculaire-v5'}
TITLES={14:['TOP 3','DES VOITURES','LES PLUS RAPIDES','2026'],15:['TOP 3','DES VILLES','LES PLUS EMBOUTEILLÉES','2026'],16:['TOP 3','DES ARMÉES','LES PLUS PUISSANTES','2026'],17:['TOP 3','RECORDS DE','VITESSE ANIMALE','2026'],18:['TOP 3','DES PLUS GRANDS','PAYS DU MONDE','2026'],13:['SE PESER','DANS','L’ESPACE']}
SERIES={14:'TOP 3 - VITESSE',15:'TOP 3 - BOUCHONS',16:'LE CLASSEMENT QUI FAIT PARLER',17:'LE CHIFFRE QUI SURPREND',18:'LE CLASSEMENT QUI SURPREND'}
SERIES[13]='COMMENT C’EST POSSIBLE ?'
CREDITS={14:'SSC - Bugatti - BYD',15:'Données INRIX 2025 - Images d’illustration',16:'Photos et archives - crédits dans le dossier',17:'Guinness - Max Planck - Photos et archives',18:'Nations unies - Photos et archives'}
CREDITS[13]='JAXA - ASC - NASA'

def seconds(s):
    h,m,x=s.split(':');return int(h)*3600+int(m)*60+float(x)

def render(n):
    w=next((ROOT/'out').glob(f'{n}-*'));m=w/'_montage';a=m/'avant-ouverture-allegee';a.mkdir(exist_ok=True)
    for name in ['final.mp4','comparaison.mp4','histoire.json']:
        if not (a/name).exists():shutil.copy2(w/name,a/name)
    src=m if n in (13,14) else m/STAGES[n]/'_montage'
    base=m/'intro-pesee-demonstrative.mp4' if n==13 else m/'intro-ssc-kmh-original.mp4' if n==14 else src/'base.mp4'
    # Les autres premières phrases sont déjà génériques. La SSC démarre au n°3 :
    # laisser le titre porter seul la compréhension des premières 1,5 seconde.
    header=[];events=[]
    for line in (src/'sous-titres-reference.ass').read_text(encoding='utf-8').splitlines():
        if not line.startswith('Dialogue:'):header.append(line);continue
        p=line.split(',',9);start,end=seconds(p[1]),seconds(p[2])
        if start>=4 or end<=1.5:continue
        # Réserver le haut au rang, puis la zone centrale aux sous-titres.
        # Les précisions secondaires ne se cumulent pas avec l'ouverture.
        if p[3]!='Default' and ('POINTES EN UN SEUL SENS' in p[9] or 'TERRES + EAUX' in p[9]):continue
        p[1]=_ass_time(max(1.5,start));p[2]=_ass_time(min(4,end))
        if p[3]=='Default':
            p[9]=re.sub(r'\{\\an8\\pos\([^}]+\}','',p[9])
            p[9]=r'{\an8\pos(540,560)\fs76}'+p[9]
        events.append(','.join(p))
    (m/'ouverture-allegee.ass').write_text('\n'.join(header+events)+'\n',encoding='utf-8')
    item=dict(title=TITLES[n],series=SERIES[n],credits=CREDITS[n],title_top=750 if n==14 else 1138)
    layers(m,item)
    graph=('[0:v]trim=end=4,setpts=PTS-STARTPTS,fps=30,ass=ouverture-allegee.ass:fontsdir=.[s];'
           '[s][2:v]overlay=0:0:enable=lt(t\\,1.5):shortest=1[t];[t][3:v]overlay=0:0:shortest=1[p];'
           '[1:v]trim=start=4,setpts=PTS-STARTPTS,fps=30[q];[p][q]concat=n=2:v=1:a=0[v]')
    target=m/'final-ouverture-allegee.mp4'
    duration=float(json.loads(run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(a/'final.mp4')]))['format']['duration'])
    run(['ffmpeg','-v','error','-y','-i',str(base),'-i',str(a/'final.mp4'),'-loop','1','-framerate','30','-i','titre-hook-reference.png','-loop','1','-framerate','30','-i','header-footer-reference.png','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],m)
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    target.replace(w/'final.mp4');compare(w)
    story=json.loads((w/'histoire.json').read_text(encoding='utf-8'))
    if n==15:story.update(titre='TOP 3 DES VILLES LES PLUS EMBOUTEILLÉES - 2026',titre_fixe='TOP 3 DES VILLES LES PLUS EMBOUTEILLÉES - 2026')
    story['ouverture']='Titre seul pendant 1,5 s, puis rang et sous-titres ; aucune accumulation de titre, rang et transcription.'
    (w/'histoire.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf-8')
    sha=hashlib.sha256((w/'final.mp4').read_bytes()).hexdigest()
    control=m/('controle-funfact-visible.json' if n!=13 else 'controle.json');d=json.loads(control.read_text(encoding='utf-8'));d['sha256']=sha;control.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print(n,'ouverture allégée et comparaison prêtes',flush=True)

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,TITLES))
