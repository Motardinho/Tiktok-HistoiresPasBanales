from production import *
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter
import numpy as np,wave
def effects():
 from narrateur.assemble import _ass_time
 path=WORK/'sous-titres.ass';s=path.read_text(encoding='utf-8').split('; FX HPB')[0]
 rows=json.loads((WORK/'paragraphes.json').read_text(encoding='utf-8'));tim=json.loads((WORK/'timings.json').read_text(encoding='utf-8'))
 marks=[rows[i]['start']-.15 for i in [10,22]]
 events=['; FX HPB - transitions demandées par Marc']
 for t in marks:
  a=t-.24;b=t+.24
  shape=r'{\an7\move(-2600,0,2200,0)\bord0\shad0\1c&H47E4FF&\p1}m 0 0 l 1800 0 1400 1080 -400 1080{\p0}'
  events.append(f'Dialogue: 5,{_ass_time(a)},{_ass_time(b)},Default,,0,0,0,,{shape}')
 # Six brief diagonal accents on editorial pivots, narrow enough to leave the scene readable.
 accents=[rows[i]['start'] for i in [6,13,18,25,29,32]]
 for t in accents:
  shape=r'{\an7\move(-700,0,2300,0)\bord0\shad0\1c&H47E4FF&\1a&H35&\p1}m 0 0 l 95 0 -305 1080 -400 1080{\p0}'
  events.append(f'Dialogue: 4,{_ass_time(t-.13)},{_ass_time(t+.13)},Default,,0,0,0,,{shape}')
 path.write_text(s+'\n'+'\n'.join(events)+'\n',encoding='utf-8')
 sr=48000;buf=np.zeros(round((tim['duration']+.1)*sr),dtype=np.float32);rng=np.random.default_rng(20261115)
 for t in marks+accents:
  n=round(.28*sr);noise=rng.normal(0,1,n);smooth=np.convolve(noise,np.ones(9)/9,mode='same');env=np.sin(np.linspace(0,np.pi,n))**2
  sound=(noise-smooth)*env*.025;at=round((t-.14)*sr);buf[at:at+n]+=sound
 with wave.open(str(WORK/'transitions.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(buf,-1,1)*32767).astype('<i2').tobytes())
 writej(WORK/'effets.json',{'demande':'Marc : transitions stylées et effets dynamiques','volets_chapitres':marks,'accents_diagonaux':accents,'zoom_details_plans':[15,30,45,49,55,72,83,115],'son':'souffles courts synthétisés, niveau discret','vitesse_images':'inchangée'})
def cover():
 import miniatures_hpb as mh
 raw=WORK/'miniature-source.png'
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss','153','-i',ROOT/'assets/long-01-voitures/ewf-q-U_b9A.mp4','-frames:v','1',raw])
 im=Image.open(raw).convert('RGB');w,h=im.size;im=im.crop((0,int(h*.08),w,int(h*.94)))
 # Fit the genuine frame to the horizontal YouTube canvas.
 ratio=max(1920/im.width,1080/im.height);im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS);im=im.crop(((im.width-1920)//2,(im.height-1080)//2,(im.width+1920)//2,(im.height+1080)//2))
 im.save(WORK/'miniature-avant.jpg',quality=95)
 im=ImageEnhance.Brightness(im).enhance(1.16);im=ImageEnhance.Contrast(im).enhance(1.08);im=ImageEnhance.Color(im).enhance(1.13);im=im.filter(ImageFilter.UnsharpMask(1.25,110,3))
 im.save(WORK/'miniature-apres.jpg',quality=95);out=im.convert('RGBA')
 shade=Image.new('RGBA',out.size);d=ImageDraw.Draw(shade)
 for y in range(1080):d.line((0,y,1920,y),fill=(5,10,25,round(130*max(0,(y-350)/730))))
 out.alpha_composite(shade)
 title,_=mh.bloc_cale([mh.N('TOP 3'),mh.N('À LA LIMITE'),mh.N('DE LA VITESSE')],'course');title=title.crop(title.getbbox());title.thumbnail((1190,500),Image.Resampling.LANCZOS);out.alpha_composite(title,(70,1030-title.height))
 logo=Image.open(ROOT/'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.png').convert('RGBA');logo.thumbnail((230,230));out.alpha_composite(logo,(1640,25))
 out.convert('RGB').save(OUT/'miniature-youtube.jpg',quality=96);out.resize((480,270)).convert('RGB').save(WORK/'miniature-mobile.jpg',quality=95)
 check=Image.new('RGB',(960,270));check.paste(Image.open(WORK/'miniature-avant.jpg').resize((480,270)),(0,0));check.paste(Image.open(WORK/'miniature-apres.jpg').resize((480,270)),(480,0));check.save(WORK/'miniature-reglages.jpg')
 writej(WORK/'miniature-manifeste.json',{'source':'BYD Europe ewf-q-U_b9A, 153 s','style':'course de miniatures_hpb.py, adapté 16:9','luminosite':1.16,'contraste':1.08,'couleurs':1.13,'netteté':{'rayon':1.25,'pourcent':110,'seuil':3},'logo':'hpb-reference-propre-v1.png','texte':['TOP 3','À LA LIMITE','DE LA VITESSE']})
if __name__=='__main__':effects();cover()
