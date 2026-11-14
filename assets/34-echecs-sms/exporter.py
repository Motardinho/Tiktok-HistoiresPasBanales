"""Export local au dossier : musique, bip de transmission original et pause de révélation."""
import sys,subprocess,json,re
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
import monter_lot_21_23 as engine
original=engine.music
original_subtitles=engine.subtitles
def subtitles(m,*args):
 original_subtitles(m,*args)
 file=m/'sous-titres.ass';lines=[]
 for line in file.read_text(encoding='utf8').splitlines():
  if line.startswith('Dialogue:'):
   parts=line.split(',',9)
   if 'PHOTO - 2017' in parts[9]:parts[9]=parts[9].replace(r'\pos(540,420)',r'\pos(540,850)')
   elif parts[9].count(r'\N')>2:
    parts[9]=engine.wrap_caption(parts[9].replace(r'\fs90',r'\fs80'),80)
   line=','.join(parts)
  lines.append(line)
 file.write_text('\n'.join(lines)+'\n',encoding='utf8')
engine.subtitles=subtitles
def music(story,m,duration):
 track=original(story,m,duration)
 # Bip synthétique de 0,11 s, au départ et à l’arrivée du signal.
 # Pause musicale juste avant la révélation de la vice-présidente.
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(m/'musique.wav'),'-af',"volume=0:enable='between(t,39.58,41.14)'",str(m/'musique-pause.wav')],check=True)
 engine.mix_voice(m/'voix.mp3',m/'musique-pause.wav',m/'mix-voix.wav',duration,engine.run)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(m/'mix-voix.wav'),'-f','lavfi','-i','sine=frequency=1250:duration=0.11:sample_rate=44100','-filter_complex','[1:a]afade=t=out:st=0.04:d=0.07,volume=0.28,asplit=2[b1][b2];[b1]adelay=17830|17830[c1];[b2]adelay=20430|20430[c2];[0:a][c1][c2]amix=inputs=3:duration=first:normalize=0[out]','-map','[out]','-ar','44100','-ac','2',str(m/'mix.wav')],check=True)
 return track
engine.music=music
engine.build(34,only_dress='habillage' in sys.argv)
