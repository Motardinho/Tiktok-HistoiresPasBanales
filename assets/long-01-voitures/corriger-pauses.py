from production import *
import wave
import numpy as np

def readwav(path):
 with wave.open(str(path),'rb') as f:
  assert f.getnchannels()==1 and f.getsampwidth()==2
  return f.getframerate(),np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()

def main():
 raw=json.loads((WORK/'timings-oraux.json').read_text(encoding='utf8'))
 timing=json.loads((WORK/'timings.json').read_text(encoding='utf8'))
 sr,x=readwav(WORK/'voix.wav');data=x.astype(float)/32768
 fixed=[]
 for old in timing['pauses_source']:
  hop=round(.01*sr);lo=max(0,round((old-.7)*sr));hi=round((old+.02)*sr)
  frames=[(a/sr,20*np.log10(np.sqrt(np.mean(data[a:a+hop]**2))+1e-9)) for a in range(lo,hi,hop)]
  runs=[];first=None
  for i,(t,db) in enumerate(frames):
   if db < -55 and first is None:first=i
   if (db >= -55 or i==len(frames)-1) and first is not None:
    end=i if db>=-55 else i+1
    if end-first>=5:runs.append((frames[first][0],frames[end-1][0]+.01))
    first=None
  if not runs:raise ValueError(f'Pas de respiration sûre près de {old}')
  # Select a verified quiet interval adjacent to the paragraph, not a TTS word boundary.
  a,b=max(runs,key=lambda z:z[1]-z[0]);new=(a+b)/2
  fixed.append({'ancienne_coupure_source':old,'nouvelle_coupure_source':new,'silence_source':[a,b]})
 # Apply tempo once to the continuous voice: no independent WSOLA boundary at a syllable.
 rate=timing['tempo_voix'];target=round(raw['duration']/rate*48000)
 run(['ffmpeg','-y','-v','error','-i',WORK/'voix.wav','-af',f'atempo={rate}',
      '-ar','48000','-ac','1','-c:a','pcm_s16le',WORK/'voix-continue-v2.wav'])
 sr,slow=readwav(WORK/'voix-continue-v2.wav')
 slow=np.pad(slow,(0,max(0,target-len(slow))))[:target]
 cuts=[0]+[round(v['nouvelle_coupure_source']/rate*sr) for v in fixed]+[target]
 chunks=[]
 for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
  chunks.append(slow[a:b])
  if i<len(fixed):chunks.append(np.zeros(2*sr,dtype='<i2'))
 result=np.concatenate(chunks)
 with wave.open(str(WORK/'voix-longue-v2.wav'),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(result.tobytes())
 total=timing['duration']
 audio=f'[0:a]highpass=f=65,loudnorm=I=-16:TP=-1.5:LRA=8,asplit=2[v][sc];[1:a]volume=0.075,afade=t=in:d=2,afade=t=out:st={total-4}:d=4[m];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[duck];[v][duck][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]'
 run(['ffmpeg','-y','-v','error','-i',WORK/'voix-longue-v2.wav','-stream_loop','-1','-i',ROOT/'assets/musique/mixkit/voitures.mp3','-i',WORK/'transitions.wav','-filter_complex',audio,'-map','[a]','-t',str(total),'-c:a','aac','-b:a','192k',WORK/'mix-v2.m4a'])
 run(['ffmpeg','-y','-v','error','-i',OUT/'essai-long-v1.mp4','-i',WORK/'mix-v2.m4a','-map','0:v:0','-map','1:a:0','-c','copy','-t',str(total),'-movflags','+faststart',OUT/'essai-long-v2.mp4'])
 run(['ffmpeg','-y','-v','error','-ss','247','-i',OUT/'essai-long-v2.mp4','-t','18','-vn','-c:a','libmp3lame','-q:a','2',OUT/'extrait-audio-4m07-v2.mp3'])
 writej(WORK/'correction-pauses-v2.json',{'signalement':'Marc : vers 4:15 un mot coupé, un silence puis reprise','diagnostic':'Coupure à 223,68 s de la source, niveau RMS environ -18,5 dBFS au milieu de La ; intervalle calme disponible de 223,23 à 223,60 s.','pauses':fixed,'tempo_continu':rate,'duree':len(result)/sr,'video_reencodee':False,'ecoute_effectuee':False})
 print('V2 exportée',flush=True)

if __name__=='__main__':main()
