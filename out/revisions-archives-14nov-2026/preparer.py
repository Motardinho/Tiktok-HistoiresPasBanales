from pathlib import Path
import json, subprocess, sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SOURCES={'doc':'assets/27-demi-tour-tempete/archives/UmjAM3qvUew.webm','ina27':'assets/27-demi-tour-tempete/arch-k791y4C_aGs.mkv','ina28':'assets/28-om-va/archives/L9nURpKZWMo.webm','om':'assets/28-om-va/archives/gKkRJ4dMTTQ.mkv'}
# Fin du plan dans la chronologie originale, source, entree, centre horizontal, description.
P27=[(3.37,'doc',1840,.5,'Mer du Sud, archives du documentaire'),(6.17,'doc',229,.5,'Pete Goss au depart 1996'),(9.27,'doc',1789,.5,'Dinelli interview archive'),(12.73,'doc',479,.5,'Depart du Vendee Globe 1996'),(15.93,'doc',1790,.5,'Dinelli archive'),(19.2,'doc',249,.5,'Preparatifs au ponton 1996'),(21.4,'doc',1845,.5,'Mer du Sud'),(25.37,'doc',1898,.5,'Conditions de mer, contexte de course'),(29,'doc',1917,.5,'Algimouss dans la tempete'),(32,'ina27',98,.5,'Dinelli sur Algimouss'),(35.27,'doc',2117,.5,'Aqua Quorum jaune'),(38.63,'doc',1867,.5,'Navigation dans le gros temps'),(41.03,'doc',1898,.5,'Mer du Sud'),(44.07,'ina27',100,.5,'Dinelli sur epave'),(46.8,'doc',2017,.5,'Radeau de Dinelli filme depuis avion'),(48.97,'doc',2068,.5,'Radeau contre le bateau de Goss'),(52.73,'doc',2207,.5,'Aqua Quorum au retour'),(54.53,'doc',3587,.5,'Goss et Dinelli reunis'),(58.57,'doc',3596,.5,'Goss et Dinelli au retour'),(62.03,'doc',2217,.5,'Fax montre dans le documentaire'),(64.13,'doc',2227,.5,'Aqua Quorum en navigation'),(66.8,'doc',3587,.5,'Retour de Goss et Dinelli'),(69.833333,'doc',3568,.5,'Aqua Quorum arrive au port')]
P28=[(8.03,'ina28',34,.5,'VA-OM 20 mai 1993'),(10.77,'om',54,.5,'Tapie finale 1993'),(14.07,'ina28',38,.5,'VA-OM match'),(17.43,'ina28',99,.5,'Jean-Jacques Eydelie archive affaire'),(21.67,'ina28',29,.5,'Joueurs OM 1993 entrainement'),(25.6,'ina28',73,.5,'Christophe Robert archive affaire'),(28.03,'ina28',153,.5,'Billets saisis archive INA'),(30.67,'ina28',53,.5,'Jacques Glassmann interview identifiee'),(32.63,'ina28',57,.5,'Glassmann interview'),(34.13,'ina28',38,.5,'VA-OM match'),(35.73,'om',82,.5,'OM coupe europeenne 1993'),(38.97,'ina28',116,.5,'Procureur de Montgolfier'),(41.2,'ina28',154,.5,'Billets presentes par reportage'),(43.13,'ina28',183,.5,'Bernard Tapie interview 1993'),(46.47,'ina28',186,.5,'Tapie interview archive, pas proces'),(47.8,'ina28',241,.5,'Suites judiciaires, contexte affaire'),(50.83,'ina28',110,.5,'Noel Le Graet instances football'),(53.07,'om',83,.5,'Coupe europeenne OM'),(56.73,'ina28',50,.5,'Jacques Glassmann'),(58.6,'ina28',58,.5,'Glassmann interview'),(62,'ina28',54,.5,'Glassmann pendant fun fact'),(65,'om',57,.5,'Tapie fete finale 1993'),(68.733333,'om',83,.5,'Coupe europeenne 1993')]
def ff(args):subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],check=True)
def crop(w,h,c):
 cw=int(h*9/16)//2*2;x=int((w-cw)*c)//2*2
 return f'crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos,setsar=1'
def prepare(n,rows,start):
 dst=OUT/str(n);dst.mkdir(exist_ok=True)
 plans=[];prev=start
 for end,key,ss,c,note in rows:
  src=ROOT/SOURCES[key]
  wh=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(src)]))['streams'][0]
  plans.append(dict(start=round(prev-start,6),duration=round(end-prev,6),source=str(src),ss=ss,crop=crop(wh['width'],wh['height'],c),note=note,resolution=wh))
  prev=end
 (dst/'plans.json').write_text(json.dumps(plans,indent=2,ensure_ascii=False),encoding='utf-8')
 for page in range(0,len(plans),8):
  sheet=Image.new('RGB',(3*180,8*340),'#202020');d=ImageDraw.Draw(sheet)
  for r,p in enumerate(plans[page:page+8]):
   for j,t in enumerate([0,p['duration']/2,max(0,p['duration']-.12)]):
    f=dst/'probe.jpg';ff(['-ss',p['ss']+t,'-i',p['source'],'-frames:v','1','-vf',p['crop']+',scale=180:320',f])
    sheet.paste(Image.open(f),(j*180,r*340));d.text((j*180,r*340+320),f"{page+r}: {p['ss']+t:.2f}",fill='yellow')
  sheet.save(dst/f'plans-{page//8}.jpg')
if __name__=='__main__':
 prepare(27,P27,53/30)
 prepare(28,P28,182/30)
