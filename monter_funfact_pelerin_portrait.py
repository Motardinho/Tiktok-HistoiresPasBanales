"""Portrait naturel du gerfaut et nouveau fun fact sur le pèlerin, sans changer la durée."""
import shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
from montage_reel import ROOT,run
from produire_lot_16_18 import read,save
from revision_hpb_v10 import display_words
from monter_lot_16_18 import music
w=next((ROOT/'out').glob('17-*'));r=w/'_montage';m=r/'funfact-pelerin-portrait';assets=ROOT/'assets/lot-16-18/nouveaux-rapaces'
if (m/'termine.json').exists():sys.exit(0)
d=read(w/'histoire.json');t=read(r/'timings.json');a=54.04;b=60.7733333333;span=b-a
save(m/'histoire-avant.json',d);save(m/'timings-avant.json',t);shutil.copy2(r/'voix.mp3',m/'voix-avant.mp3')
it=read(m/'phrase/_montage/timings-oraux.json');ratio=max(it['duration'],it['words'][-1]['end']+.05)/span
run(['ffmpeg','-v','error','-y','-i',str(m/'phrase/_montage/voix.mp3'),'-af',f'atempo={ratio},apad,atrim=duration={span}',str(m/'phrase.wav')])
g=f'[0:a]atrim=end={a},asetpts=PTS-STARTPTS[x];[1:a]asetpts=PTS-STARTPTS[y];[0:a]atrim=start={b},asetpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=0:a=1[o]'
run(['ffmpeg','-v','error','-y','-i',str(m/'voix-avant.mp3'),'-i',str(m/'phrase.wav'),'-filter_complex',g,'-map','[o]','-c:a','libmp3lame','-b:a','192k',str(m/'voix.mp3')])
t['words']=[x for x in t['words'] if x['start']<a-.005]+[dict(w=x['w'],start=a+x['start']/ratio,end=a+x['end']/ratio) for x in display_words(it['words'])]+[x for x in t['words'] if x['start']>=b-.005]
save(m/'timings.json',t);music(w,m,t,17)
run(['ffmpeg','-v','error','-y','-i',str(m/'mix.wav'),'-c:a','aac','-b:a','192k',str(m/'audio-corrige.m4a')])
base=w/d['correction_locale']['base'];ga=368/30;gb=578/30
g=(f'[0:v]trim=end={ga},setpts=PTS-STARTPTS,setsar=1[x0];'
   '[1:v]crop=trunc(ih*9/16/2)*2:ih:iw*0.4-ow/2:0,scale=1080:1920,fps=30,trim=end_frame=210,setpts=PTS-STARTPTS,setsar=1[x1];'
   f'[0:v]trim=start={gb}:end={a},setpts=PTS-STARTPTS,setsar=1[x2];'
   '[2:v]scale=1080:1920,fps=30,trim=end_frame=202,setpts=PTS-STARTPTS,setsar=1[x3];'
   f'[0:v]trim=start={b},setpts=PTS-STARTPTS,setsar=1[x4];[x0][x1][x2][x3][x4]concat=n=5:v=1:a=0[v]')
run(['ffmpeg','-v','error','-y','-i',str(base),'-ss','198','-i',str(assets/'gyrfalcon-bbc.mp4'),'-ss','1','-i',str(assets/'reference-gerfaut-marc.mp4'),'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(m/'base.mp4')])
phrase='Son détail fou : une troisième paupière, translucide, protège ses yeux pendant le piqué. Comme des lunettes intégrées !'
for key in ['narration','narration_voix']:d['scenes'][6][key]=phrase+' C’est une pointe en descente, pas sa vitesse de vol habituelle.'
d['script']=' '.join(s['narration'] for s in d['scenes']);(w/'script.txt').write_text('\n\n'.join(s['narration'] for s in d['scenes']),encoding='utf-8')
d['correction_locale'].update(base=str((m/'base.mp4').relative_to(w)),audio=str((m/'audio-corrige.m4a').relative_to(w)))
source='https://www.nps.gov/articles/000/view-from-the-aerie-peregrine-falcon-watch-in-2024.htm'
d['fun_fact']=dict(texte='Une troisième paupière translucide protège les yeux du pèlerin pendant le piqué.',source=source)
d['fun_fact_affichage']=dict(debut=a,fin=b,texte=['DES LUNETTES NATURELLES'],mention='FUN FACT')
save(w/'histoire.json',d)
for file in ['timings.json','voix.mp3']:shutil.copy2(m/file,r/file)
old=read(r/'timings-oraux.json');old.update(words=t['words']);save(r/'timings-oraux.json',old)
credit='\nFun fact : troisième paupière protectrice du pèlerin — National Park Service : '+source+'\nVidéo du pèlerin : BBC Earth / Scott Sessions — https://www.youtube.com/shorts/QIH5XV3Vays\n'
for name in ['publication.txt','legende.txt']:
 p=w/name;s=p.read_text(encoding='utf-8');assert len(s+credit)<=2200,(name,len(s+credit));p.write_text(s+credit,encoding='utf-8')
with (w/'CREDITS.md').open('a',encoding='utf-8') as f:f.write(credit+'\nLe Short montre un pèlerin, utilisé uniquement au passage du pèlerin. Gerfaut : BBC Earth, extrait 198–205 s, recadrage portrait naturel. Aucun droit libre revendiqué.\n')
save(m/'termine.json',dict(debut=a,fin=b,ratio_voix=ratio,source_video='https://www.youtube.com/shorts/QIH5XV3Vays',espece='Faucon pèlerin',source_funfact=source))
print('17 nouveau fun fact et portraits vidéo prêts',flush=True)
