import sys,json,subprocess,requests
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from narrateur.voice import _api_key
p=ROOT/'out/45-origine-black-friday';m=p/'_montage'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'videos/final.mp4'),'-vn','-c:a','pcm_s16le','-ar','16000','-ac','1',str(m/'audio-export.wav')],check=True)
with (m/'audio-export.wav').open('rb') as f:
 r=requests.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':_api_key()},data={'model_id':'scribe_v2','language_code':'fr','tag_audio_events':'false'},files={'file':('audio-export.wav',f,'audio/wav')},timeout=180)
if not r.ok:print('STT indisponible',r.status_code);sys.exit(1)
d=r.json();(m/'transcription-export.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print(d['text'])
