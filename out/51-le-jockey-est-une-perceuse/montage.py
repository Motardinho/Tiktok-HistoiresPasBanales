"""Montage du dossier 51 : plans réels calés sur les mots, sous-titres, logo HPB, voix et musique.

python montage.py            plans + sous-titres + export
python montage.py --habillage  réutilise les plans déjà rendus
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import ImageFont

work = Path(__file__).resolve().parent
root = work.parent.parent
m = work / '_montage'
story = json.loads((work / 'histoire.json').read_text(encoding='utf-8'))
timing = json.loads((m / 'timings-oraux.json').read_text(encoding='utf-8'))
FPS = 25
duration = round((timing['duration'] + 0.3) * FPS) / FPS


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-nostdin', '-hide_banner', '-loglevel', 'error', *map(str, args)],
                   cwd=work, check=True)


# ---------- Sous-titres : mots ElevenLabs, nombres en chiffres, ponctuation attachée ----------
def norm(text):
    return re.sub(r'[^\w\-]', '', text.lower())


words = [dict(w=x['w'], start=x['start'], end=x['end']) for x in timing['words']]
replacements = sorted(story['affichage'].items(), key=lambda kv: -len(kv[0].split()))
merged, i = [], 0
while i < len(words):
    for key, value in replacements:
        n = len(key.split())
        span = words[i:i + n]
        if len(span) == n and [norm(x['w']) for x in span] == [norm(k) for k in key.split()]:
            tail = re.search(r'[^\w\-]*$', span[-1]['w']).group()
            head = re.match(r'^[^\w\-]*', span[0]['w']).group()
            merged.append(dict(w=head + value + tail, start=span[0]['start'], end=span[-1]['end']))
            i += n
            break
    else:
        merged.append(words[i])
        i += 1
tokens = []
for x in merged:
    if re.fullmatch(r'[:;?!»]', x['w']) and tokens:
        tokens[-1]['w'] += ' ' + x['w']
        tokens[-1]['end'] = x['end']
    else:
        tokens.append(dict(x))
shown = ' '.join(t['w'] for t in tokens)
for key, value in story['affichage'].items():
    assert key not in shown, key

font = ImageFont.truetype(str(root / 'assets/fonts/Poppins-ExtraBold.ttf'), 90)


def ass_time(seconds):
    cs = round(seconds * 100)
    minutes, rest = divmod(cs, 6000)
    sec, frac = divmod(rest, 100)
    return f'0:{minutes:02}:{sec:02}.{frac:02}'


header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Oral,Poppins ExtraBold,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,8,4,2,145,145,550,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events, chunk = [], []
for index, tok in enumerate(tokens):
    chunk.append(tok)
    nxt = tokens[index + 1] if index + 1 < len(tokens) else None
    sentence_end = tok['w'].endswith(('.', '?', '!'))
    too_long = nxt and len(' '.join(t['w'] for t in chunk + [nxt])) > 46
    if not nxt or sentence_end or too_long or len(chunk) == 5:
        texts = [t['w'] for t in chunk]
        split = min(range(1, len(texts)), key=lambda p: abs(len(' '.join(texts[:p])) - len(' '.join(texts[p:]))), default=0)
        for active, t in enumerate(chunk):
            following = chunk[active + 1] if active + 1 < len(chunk) else nxt
            first = t['start'] if events else 0
            last = following['start'] if following else duration
            colored = texts.copy()
            colored[active] = r'{\1c&H47E4FF&}' + colored[active] + r'{\1c}'
            line = ' '.join(colored)
            if split and font.getlength(' '.join(texts)) > 685:
                line = ' '.join(colored[:split]) + r'\N' + ' '.join(colored[split:])
            events.append(f'Dialogue: 0,{ass_time(first)},{ass_time(last)},Oral,,0,0,0,,{line}')
        chunk.clear()
(work / 'sous-titres.ass').write_text(header + '\n'.join(events) + '\n', encoding='utf-8')

# ---------- Plans ----------
M = '4udO3omFo_k.webm'   # Al Marmoom, Dubaï, 4K (OFF The WALL, 2025)
W = 'F49r92NiZNo.webm'   # Al Wathba, Abou Dabi, 4K (Edu Ubeda, 2021)
Q = 'MkNnAv4liTI.webm'   # Al Shahaniya, Qatar, 4K (iLoveQatar.net, 2024)
J = 'Mapsiw8iy8A.mkv'    # « Boy Racers », ABC Australia, avril 2003, Émirats (Journeyman Pictures)
B = '3V-56_oPLoA.mkv'    # BBC World Service, Witness History, 2023 (photos d'archives)
K = '6lR-PZWstWY.mkv'    # K-Team, démonstration du robot jockey au Qatar
V = (1215, 2160)         # 9:16 plein cadre 4K
T = (1068, 1900)         # 9:16 4K sans le bas (sous-titres incrustés de la source)
# (début timeline, source, entrée source, vitesse, (l, h, x, y), note)
plans = [
    (0.00, M, 365.20, 0.80, (*T, 700, 0), 'départ en trombe, robots sur le dos'),
    (1.28, M, 276.40, 1.00, (*T, 1300, 0), 'robot au sol : perceuse et fouet qui balaie'),
    (2.84, M, 24.00, 0.85, (*T, 600, 0), 'sortie des stalles, contre-plongée'),
    (4.32, J, 164.00, 1.00, (900, 787, 610, 215), 'archive 2003 : enfant jockey en course'),
    (5.76, J, 156.00, 1.00, (1476, 787, 222, 215), 'archive 2003 : départ avec enfants jockeys'),
    (8.72, J, 28.00, 1.00, (1100, 787, 400, 215), 'archive 2003 : enfants en course'),
    (11.52, J, 16.00, 1.00, (1100, 787, 500, 215), 'archive 2003 : enfants alignés sur les chameaux'),
    (13.56, J, 540.00, 1.00, (1100, 787, 400, 215), 'archive 2003 : petit enfant hissé sur un grand chameau, de loin'),
    (15.84, J, 44.00, 1.00, (1000, 787, 500, 215), 'archive 2003 : enfant en course'),
    (17.76, J, 32.00, 1.00, (1300, 787, 300, 215), 'archive 2003 : course le long du 4x4'),
    (19.64, J, 160.00, 1.00, (1300, 787, 300, 215), 'archive 2003 : course'),
    (21.48, W, 2.60, 1.00, (*T, 1373, 130), 'stalles de départ, Al Wathba'),
    (24.88, M, 15.00, 1.00, (*T, 1000, 0), 'robots dans les stalles, vue du dessus'),
    (26.16, K, 8.00, 1.00, (640, 480, 0, 0), 'démo K-Team : robot sur un chameau'),
    (28.16, B, 70.00, 1.00, (900, 780, 300, 0), 'photo BBC : premiers robots à visage'),
    (30.24, K, 64.00, 1.00, (640, 480, 0, 0), 'démo K-Team : chameau monté par le robot'),
    (32.48, K, 24.00, 1.00, (640, 480, 0, 0), 'démo K-Team : dresseur à côté du robot'),
    (34.36, M, 318.00, 1.00, (*T, 618, 0), 'dresseurs et chameaux équipés'),
    (36.56, M, 271.00, 1.00, (*T, 1194, 0), 'un homme porte les robots à la main'),
    (39.20, M, 280.00, 1.00, (*T, 1386, 0), 'gros plan : perceuse'),
    (40.16, M, 278.00, 1.00, (*T, 1500, 0), 'gros plan : fouet'),
    (41.36, B, 95.60, 1.00, (1000, 770, 900, 0), 'photo BBC : robot et son boîtier radio'),
    (42.32, Q, 54.00, 1.00, (*V, 700, 0), 'les 4x4 suivent la course, Qatar'),
    (44.29, M, 192.00, 1.00, (*T, 2077, 0), 'chameau suivi depuis la voiture'),
    (45.76, B, 84.00, 1.00, (900, 700, 250, 100), 'photo BBC : propriétaire au talkie-walkie dans son 4x4'),
    (48.00, Q, 63.50, 1.00, (*V, 1500, 0), 'chameau et son robot en course, Qatar'),
    (49.12, W, 7.60, 1.00, (*T, 649, 130), 'piste d’Al Wathba, Abou Dabi'),
    (51.60, W, 19.50, 1.00, (*T, 2154, 130), 'course à Al Wathba, contre-plongée'),
    (54.56, W, 25.00, 1.00, (*T, 1002, 130), 'public et propriétaires au départ'),
    (57.08, W, 30.00, 1.00, (*T, 1373, 130), 'chameaux menés à la main'),
    (58.44, M, 350.00, 1.00, (*T, 1100, 0), 'robots dans les stalles, vue du dessus'),
    (61.52, W, 5.00, 1.00, (*T, 1385, 130), 'départ, chameaux en gros plan'),
    (63.95, Q, 42.00, 1.00, (*V, 1300, 0), 'un 4x4 suit la course sur la piste parallèle, Qatar'),
    (66.20, M, 283.00, 1.00, (*T, 1300, 0), 'robot jockey en gros plan'),
]
plans = [p for p in plans]


def render(index, plan):
    begin, source, src, speed, (w, h, x, y), note = plan
    end = plans[index + 1][0] if index + 1 < len(plans) else duration
    frames = round(end * FPS) - round(begin * FPS)
    chain = f'[0:v]crop={w}:{h}:{x}:{y},setpts=(PTS-STARTPTS)/{speed},fps={FPS},setsar=1'
    if abs(w / h - 9 / 16) < 0.01:
        chain += ',scale=1080:1920:flags=lanczos,format=yuv420p[out]'
    else:
        chain += (',split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
                  'gblur=sigma=35,eq=brightness=-0.18[bg];[b]scale=1080:-2:flags=lanczos[fg];'
                  '[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[out]')
    ffmpeg('-threads', 3, '-ss', src, '-i', f'sources/{source}', '-filter_complex', chain, '-map', '[out]',
           '-frames:v', frames, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', 16,
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', f'plans/{index:02}.mp4')
    return dict(debut=round(begin * FPS) / FPS, fin=round(end * FPS) / FPS, source=source, entree=src,
                sortie=round(src + frames / FPS * speed, 3), vitesse=speed, fenetre=[w, h, x, y], note=note)


if '--habillage' not in sys.argv:
    (work / 'plans').mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        manifest = list(pool.map(lambda pair: render(*pair), enumerate(plans)))
    (work / 'plans.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    (work / 'liste.txt').write_text(''.join(f"file 'plans/{i:02}.mp4'\n" for i in range(len(plans))), encoding='utf-8')

# ---------- Son : voix + musique discrète sous la parole ----------
music = root / 'assets/musique/mixkit/scandale.mp3'
logo = root / 'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.png'
ffmpeg('-f', 'concat', '-safe', 0, '-i', 'liste.txt', '-i', '_montage/voix.mp3', '-i', music, '-i', logo,
       '-filter_complex_threads', 2, '-filter_complex',
       '[3:v]scale=206:206[logo];[0:v][logo]overlay=828:233,ass=sous-titres.ass:fontsdir=../../assets/fonts[v];'
       '[1:a]loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000,asplit[voice][key];'
       f'[2:a]atrim=duration={duration},asetpts=PTS-STARTPTS,aresample=48000,volume=-21dB,'
       f'afade=t=in:d=0.6,afade=t=out:st={duration - 1.5}:d=1.5[bed];'
       '[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[ducked];'
       '[voice][ducked]amix=inputs=2:duration=first:normalize=0,apad,alimiter=limit=0.89[a]',
       '-map', '[v]', '-map', '[a]', '-t', duration, '-c:v', 'libx264', '-preset', 'fast', '-crf', 17,
       '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
       '-c:a', 'aac', '-ar', 48000, '-b:a', '192k', '-movflags', '+faststart', 'final.mp4')
print('final.mp4', duration, 's')
