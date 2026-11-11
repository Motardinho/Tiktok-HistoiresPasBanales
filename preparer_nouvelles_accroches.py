"""Plans réels pour montrer le mécanisme de pesée et la télémétrie KM/H."""
from montage_reel import ROOT,SOURCES,run
from produire_lot_16_18 import save

def render(source,start,seconds,target,vf):
    run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(source),'-vf',vf+',fps=30,setsar=1','-frames:v',str(round(seconds*30)),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(target)])

def concat(m,files,target):
    (m/'nouvelle-intro-concat.txt').write_text(''.join(f"file '{f.name}'\n" for f in files),encoding='utf-8')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','nouvelle-intro-concat.txt','-c','copy',target.name],m)

w=next((ROOT/'out').glob('13-*'));m=w/'_montage'
render(SOURCES/'astronautes-masse-jaxa-2014.mp4',39.4,4,m/'intro-jaxa-oblique.mp4','crop=340:590:375:0,scale=1080:1920')
render(SOURCES/'astronautes-masse.mp4',60,4,m/'intro-mecanisme-detail.mp4','crop=500:888:740:0,scale=1080:1920')
concat(m,[m/'intro-jaxa-oblique.mp4',m/'intro-mecanisme-detail.mp4'],m/'intro-pesee-demonstrative.mp4')
save(m/'nouvelle-intro-source.json',dict(source='https://www.youtube.com/watch?v=PlKciJ26lEk',credit='JAXA - Koichi Wakata Weekly Activity Report Vol.12, prise du 6 janvier 2014',debut=39.4,duree=4,complement='ASC/NASA, détail du mécanisme à 60 s',illustration='Prise oblique avec appareil visible puis détail mécanique ; vitesse originale'))
w=next((ROOT/'out').glob('14-*'));m=w/'_montage'
render(SOURCES/'ssc-vbox-2022.mp4',47.8,2.5,m/'intro-ssc-kmh.mp4','crop=608:1080:420:0,scale=1080:1920')
render(m/'base-hpb-v13.mp4',2.5,1.5,m/'intro-ssc-exterieur.mp4','null')
concat(m,[m/'intro-ssc-kmh.mp4',m/'intro-ssc-exterieur.mp4'],m/'intro-ssc-kmh-original.mp4')
save(m/'nouvelle-intro-source.json',dict(source='https://www.youtube.com/watch?v=IgXuBBe017Q',credit='VBOX Motorsport - télémétrie originale SSC 2022',debut=47.8,duree=2.5,unite_visible='KM/H',valeurs='environ 470 à 475',compteur_invente=False,vitesse_originale=True))
