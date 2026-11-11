"""Trois compositions distinctes : électro, ambient et groove percussif."""
import math
import wave
from pathlib import Path
import numpy as np


def create_bed(path: Path, duration: float, kind: str):
    sr=44100;n=math.ceil(duration*sr)
    out=np.zeros((n,2),np.float32)
    rng=np.random.default_rng({'voitures':1101,'espace':2202,'bouchons':3303}[kind])

    def tone(note,length,mode,level):
        t=np.arange(round(length*sr),dtype=np.float32)/sr
        f=440*2**((note-69)/12)
        if mode=='bass':
            y=np.sin(2*np.pi*f*t+1.3*np.exp(-t/.08)*np.sin(2*np.pi*f*2*t))
            env=np.minimum(t/.005,1)*np.exp(-t/.14)
        elif mode=='bell':
            y=np.sin(2*np.pi*f*t+.55*np.exp(-t/2)*np.sin(2*np.pi*f*2.01*t))
            env=np.minimum(t/.04,1)*np.exp(-t/2.3)
        elif mode=='wood':
            y=np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*f*3.97*t)*np.exp(-t/.03)
            env=np.minimum(t/.004,1)*np.exp(-t/.10)
        elif mode=='pad':
            y=np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*1.003*t)+.08*np.sin(2*np.pi*f*2*t)
            env=np.minimum(t/2.4,1)*np.minimum((length-t)/3,1)
        else:
            y=np.sin(2*np.pi*f*t)+.18*np.sin(2*np.pi*f*2*t)
            env=np.minimum(t/.004,1)*np.exp(-t/.075)
        return (level*y*env).astype(np.float32)

    def add(at,y,pan=0):
        offset=round(at*sr);count=min(len(y),n-offset)
        if count<=0:return
        out[offset:offset+count,0]+=y[:count]*math.sqrt((1-pan)/2)
        out[offset:offset+count,1]+=y[:count]*math.sqrt((1+pan)/2)

    def drum(at,mode,level,pan=0):
        length=.22 if mode=='kick' else .09
        t=np.arange(round(length*sr),dtype=np.float32)/sr
        if mode=='kick':
            phase=2*np.pi*(46*t+70*.023*(1-np.exp(-t/.023)))
            y=np.sin(phase)*np.exp(-t/.055)
        elif mode=='rim':
            y=(np.sin(2*np.pi*780*t)+.5*np.sin(2*np.pi*1130*t))*np.exp(-t/.009)
        elif mode=='bongo':
            y=np.sin(2*np.pi*(180*t+15*.02*(1-np.exp(-t/.02))))*np.exp(-t/.035)
        else:
            noise=rng.normal(0,1,len(t));noise=np.diff(noise,prepend=0)
            y=noise*np.exp(-t/(.024 if mode=='clap' else .012))
        add(at,(level*y*np.minimum(t/.0015,1)).astype(np.float32),pan)

    if kind=='voitures':
        # D mineur : basse syncopée FM, kick régulier et charleston serré.
        beat=60/124;roots=[38,38,34,36]
        for bar in range(math.ceil(duration/(beat*4))):
            base=bar*beat*4;root=roots[bar%4]
            for step in [0,3,6,8,11,14]:
                add(base+step*beat/4,tone(root+(12 if step==14 else 0),.38,'bass',.18))
            for b in range(4):
                drum(base+b*beat,'kick',.18)
                if b%2:drum(base+b*beat,'clap',.023)
            for step in range(8):drum(base+step*beat/2,'hat',.010,.45 if step%2 else -.45)
            for step,note in enumerate([62,65,69,65,60,65,69,72]):
                add(base+(step+.5)*beat/2,tone(note,.24,'pluck',.023),.25 if step%2 else -.25)
    elif kind=='espace':
        # D majeur : nappes lentes, cloches espacées, aucune batterie ni basse rythmique.
        chords=[(50,57,61,66),(54,61,64,69),(55,62,66,69)]
        for bar in range(math.ceil(duration/11)):
            for j,note in enumerate(chords[bar%3]):
                add(bar*11,tone(note,15,'pad',.040),[-.65,.35,-.2,.65][j])
        at=1.2;i=0
        while at<duration:
            add(at,tone([81,78,85,73,78,86][i%6],6,'bell',.052),.6 if i%2 else -.6)
            at += [4.7,6.2,3.9,7.1][i%4];i+=1
    else:
        # Mi bémol : petits bois/marimba et percussions sèches, swing léger.
        beat=60/96;roots=[39,36,41,34]
        chords=[(63,67,70),(60,63,67),(65,68,72),(62,65,70)]
        for bar in range(math.ceil(duration/(beat*4))):
            base=bar*beat*4
            for b in [0,2]:add(base+b*beat,tone(roots[bar%4],.38,'wood',.12))
            for b in range(4):
                drum(base+(b+.60)*beat,'bongo',.026,.35)
                if b%2:drum(base+b*beat,'rim',.030,-.2)
                drum(base+(b+.5)*beat,'hat',.006,.5)
                for j,note in enumerate(chords[bar%4]):
                    add(base+(b+.57)*beat+j*.014,tone(note,.3,'wood',.025),.25)
            for step,note in enumerate([75,74,70,67]):
                add(base+(step+.25)*beat,tone(note,.35,'wood',.035),-.4)

    fade=min(round(sr),n//2);out[:fade]*=np.linspace(0,1,fade,dtype=np.float32)[:,None]
    fade=min(round(2.4*sr),n//2);out[-fade:]*=np.linspace(1,0,fade,dtype=np.float32)[:,None]
    peak=float(np.max(np.abs(out)));rms=float(np.sqrt(np.mean(out*out)))
    if rms:out*=min(.105/rms,.8/max(peak,1e-8))
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
