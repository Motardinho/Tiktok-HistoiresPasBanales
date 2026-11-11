"""Fonds instrumentaux originaux et mixage discret sous une narration.

Aucun échantillon externe : oscillateurs et percussions synthétisés localement.
"""
import math
import wave
from pathlib import Path

import numpy as np


def create_bed(path: Path, duration: float, kind: str):
    rate = 44100
    profiles = {'voitures': (118, .065, .075),
                'espace': (72, .085, .022), 'bouchons': (92, .065, .040)}
    bpm, pad_gain, pulse_gain = profiles[kind]
    n = math.ceil(duration*rate)
    track = np.zeros((n,2),dtype=np.float32)
    rng = np.random.default_rng(20261108)
    beat = 60/bpm
    chords = [(57,60,64,71),(53,57,60,64),(60,64,67,71),(55,59,62,69)]

    def add(start, signal, pan=0):
        offset = round(start*rate)
        count = min(len(signal), n-offset)
        if count <= 0:return
        track[offset:offset+count,0] += signal[:count]*math.sqrt((1-pan)/2)
        track[offset:offset+count,1] += signal[:count]*math.sqrt((1+pan)/2)

    for bar in range(math.ceil(duration/(beat*4))):
        chord = chords[(bar//2)%4]
        length = min(beat*4+.35,duration-bar*beat*4)
        t = np.arange(round(length*rate),dtype=np.float32)/rate
        env = np.minimum(t/.45,1)*np.minimum((length-t)/.45,1)
        for j,note in enumerate(chord):
            freq=440*2**((note-69)/12)
            signal=pad_gain/len(chord)*env*(np.sin(2*np.pi*freq*t)+.18*np.sin(2*np.pi*freq*2.001*t))
            add(bar*beat*4,signal,(-.5,.3,-.25,.5)[j])
    for b in range(math.ceil(duration/beat)):
        chord=chords[(b//8)%4]
        length=.42 if kind=='espace' else .23
        t=np.arange(round(length*rate),dtype=np.float32)/rate
        note=chord[b%len(chord)]+(12 if kind=='espace' else 0)
        freq=440*2**((note-69)/12)
        env=np.minimum(t/.008,1)*np.exp(-t/(.14 if kind=='espace' else .065))
        add(b*beat,pulse_gain*env*(np.sin(2*np.pi*freq*t)+.15*np.sin(2*np.pi*freq*2*t)),.25 if b%2 else -.25)
        if kind=='voitures':
            t=np.arange(round(.19*rate),dtype=np.float32)/rate
            phase=2*np.pi*(50*t+50*.028*(1-np.exp(-t/.028)))
            add(b*beat,.07*np.minimum(t/.003,1)*np.exp(-t/.045)*np.sin(phase))
        if kind!='espace' and b%2:
            t=np.arange(round(.055*rate),dtype=np.float32)/rate
            noise=rng.normal(0,1,len(t)).astype(np.float32)
            noise=np.diff(noise,prepend=0)
            add(b*beat+beat*.5,.005*np.minimum(t/.003,1)*np.exp(-t/.014)*noise,.55)
    fade=min(round(1.2*rate),n//2)
    track[:fade]*=np.linspace(0,1,fade,dtype=np.float32)[:,None]
    fade_out=min(round(2.5*rate),n//2)
    track[-fade_out:]*=np.linspace(1,0,fade_out,dtype=np.float32)[:,None]
    peak=float(np.max(np.abs(track)))
    if peak:track*=.5/peak
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as wav:
        wav.setnchannels(2);wav.setsampwidth(2);wav.setframerate(rate)
        wav.writeframes((np.clip(track,-1,1)*32767).astype('<i2').tobytes())


def mix_voice(voice: Path, music: Path, output: Path, duration: float, run):
    graph=('[0:a]loudnorm=I=-16:TP=-1.5:LRA=9,aformat=sample_rates=44100:channel_layouts=stereo,'
           'asplit=2[voice][side];'
           '[1:a]aformat=sample_rates=44100:channel_layouts=stereo,highpass=f=60,lowpass=f=6500,volume=0.20[bed];'
           '[bed][side]sidechaincompress=threshold=0.035:ratio=3:attack=25:release=280[duck];'
           '[voice][duck]amix=inputs=2:duration=first:normalize=0,'
           'alimiter=limit=0.95:level=false[mix]')
    run(['ffmpeg','-v','error','-y','-i',str(voice),'-i',str(music),
         '-filter_complex',graph,'-map','[mix]','-t',str(duration),
         '-ar','44100','-c:a','pcm_s16le',str(output)])
