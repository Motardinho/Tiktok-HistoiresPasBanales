import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import ImageFont

work = Path(__file__).resolve().parent
root = work.parent.parent
sys.path.insert(0, str(root))
import miniatures_hpb as miniature

def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-nostdin', '-hide_banner', '-loglevel', 'error',
                    *map(str, args)], cwd=work, check=True)

script = ' '.join((work / 'histoire.txt').read_text(encoding='utf-8').split())
alignment = json.loads((work / 'timings.json').read_text(encoding='utf-8'))
assert script.replace('Rice', 'Raïs').replace('Faye Yap', 'Faïe Yap') == ''.join(alignment['characters'])
starts = alignment['character_start_times_seconds']
words = list(re.finditer(r'130 %|(?:« )?\S+(?: »[.!?,]?| [?!])?', script))
duration = 66.48
reuse_plans = '--sous-titres' in sys.argv or '--chute' in sys.argv
caption_font = ImageFont.truetype(str(root / 'assets/fonts/Poppins-ExtraBold.ttf'), 90)

def ass_time(seconds):
    centiseconds = round(seconds * 100)
    minutes, remainder = divmod(centiseconds, 6000)
    seconds, fraction = divmod(remainder, 100)
    return f'0:{minutes:02}:{seconds:02}.{fraction:02}'

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
events = []
chunk = []

def word_start(token):
    return starts[token.start() + (2 if token[0].startswith('« ') else 0)]

for index, word in enumerate(words):
    chunk.append(word)
    next_word = words[index + 1] if index + 1 < len(words) else None
    line = script[chunk[0].start():word.end()]
    sentence_end = word[0].endswith(('.', '?', '!'))
    next_too_long = next_word and next_word.end() - chunk[0].start() > 46
    if not next_word or sentence_end or next_too_long or len(chunk) == 5:
        tokens = [token[0].replace(' %', '\u202f%').replace(' ?', '\u202f?')
                  .replace('« ', '«\u202f').replace(' »', '\u202f»') for token in chunk]
        split = min(range(1, len(tokens)),
                    key=lambda pos: abs(len(' '.join(tokens[:pos])) - len(' '.join(tokens[pos:]))),
                    default=0)
        for active, token in enumerate(chunk):
            following = chunk[active + 1] if active + 1 < len(chunk) else next_word
            first = word_start(token) if events else 0
            last = word_start(following) if following else duration
            colored = tokens.copy()
            colored[active] = r'{\1c&H47E4FF&}' + colored[active] + r'{\1c}'
            line = ' '.join(colored)
            if split and caption_font.getlength(' '.join(tokens)) > 685:
                line = ' '.join(colored[:split]) + r'\N' + ' '.join(colored[split:])
            events.append(f'Dialogue: 0,{ass_time(first)},{ass_time(last)},Oral,,0,0,0,,{line}')
        chunk.clear()
(work / 'sous-titres.ass').write_text(header + '\n'.join(events) + '\n', encoding='utf-8')

if reuse_plans:
    logo = root / 'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.png'
    new_voice = '--chute' in sys.argv
    graph = '[2:v]scale=206:206[logo];[0:v][logo]overlay=828:233,ass=sous-titres.ass:fontsdir=../../assets/fonts[v]'
    if new_voice:
        graph += ';[1:a]loudnorm=I=-16:TP=-1.5:LRA=7,apad[a]'
    audio_input = 'voix.mp3' if new_voice else 'final.mp4'
    audio_map = ['-map', '[a]', '-c:a', 'aac', '-ar', 48000, '-b:a', '192k'] if new_voice else [
        '-map', '1:a:0', '-c:a', 'copy']
    ffmpeg('-f', 'concat', '-safe', 0, '-i', 'liste.txt', '-i', audio_input, '-i', logo,
           '-filter_complex_threads', 2, '-filter_complex',
           graph, '-map', '[v]', *audio_map, '-t', duration, '-c:v', 'libx264', '-preset', 'fast',
           '-crf', 17, '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709',
           '-colorspace', 'bt709', '-movflags', '+faststart', 'final-sous-titres.mp4')
    sys.exit()

rice = 'rice.webm'
award = 'ceremonie.webm'
prey = 'ADVS-9-2201174-s004.mp4'
foam = 'ADVS-9-2201174-s005.mp4'
circuit = 'ADVS-9-2201174-s001.mp4'
handheld = 'ADVS-9-2201174-s003.mp4'
# Timeline in seconds, source in-point, playback speed and source crop (w, h, x, y).
plans = [
    (0.00, rice, 107.9, 0.86, (940, 1672, 1450, 445)),
    (1.60, rice, 111.25, 0.95, (1012, 1798, 1414, 280)),
    (3.84, rice, 97.10, 0.72, (2180, 1920, 460, 70)),
    (7.76, rice, 102.10, 0.77, (1380, 1920, 1690, 80)),
    (10.60, rice, 27.60, 0.8, (1032, 1834, 1450, 292)),
    (14.63, rice, 13.70, 0.89, (1188, 2112, 1550, 10)),
    (17.98, foam, 11.40, 1, (536, 952, 693, 70)),
    (21.50, rice, 106.35, 1.24, (934, 1660, 1460, 440)),
    (25.11, rice, 99.45, 1, (1550, 1650, 1080, 360)),
    (27.58, rice, 92.22, 1, (1510, 1490, 1010, 495)),
    (30.55, foam, 13.1, 1.1, (532, 946, 695, 78)),
    (34.46, rice, 80.1, 1.18, (1110, 1974, 1408, 160)),
    (38.40, handheld, 13.25, 0.9, (1130, 980, 190, 46)),
    (41.14, prey, 15.8, 1.35, (530, 942, 696, 100)),
    (44.99, foam, 13.3, 1.9, (532, 946, 695, 78)),
    (48.40, rice, 15.0, 0.7, (1050, 1866, 1630, 110)),
    (51.48, award, 0.85, 1, (2304, 1320, 192, 30)),
    (56.22, award, 11.25, 0.92, (2320, 1180, 115, 25)),
    (59.08, rice, 112.4, 0.74, (936, 1664, 1458, 365)),
    (62.19, foam, 19.65, 0.88, (532, 946, 695, 78)),
    (64.45, rice, 109.9, 1.07, (940, 1672, 1450, 400)),
]

def render(index, plan):
    begin, source, source_time, speed, crop = plan
    end = plans[index + 1][0] if index + 1 < len(plans) else duration
    frames = round(end * 25) - round(begin * 25)
    w, h, x, y = crop
    chain = f'[0:v]crop={w}:{h}:{x}:{y},setpts=(PTS-STARTPTS)/{speed},fps=25,setsar=1'
    if abs(w / h - 9 / 16) < 0.01:
        chain += ',scale=1080:1920:flags=lanczos[out]'
    else:
        chain += (',split[base][front];[base]scale=1080:1920:force_original_aspect_ratio=increase,'
                  'crop=1080:1920,gblur=sigma=35,eq=brightness=-0.18[bg];'
                  '[front]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[out]')
    ffmpeg('-threads', 3, '-ss', source_time, '-i', f'sources/{source}', '-filter_complex_threads', 2,
           '-filter_complex', chain, '-map', '[out]', '-frames:v', frames, '-an',
           '-c:v', 'libx264', '-threads', 3, '-preset', 'veryfast', '-crf', 16,
           '-pix_fmt', 'yuv420p', f'plans/{index:02}.mp4')
    return dict(debut=round(begin * 25) / 25, fin=round(end * 25) / 25, source=source,
                entree=source_time, sortie=round(source_time + frames / 25 * speed, 3),
                vitesse=speed, fenetre=crop)

(work / 'plans').mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    manifest = list(pool.map(lambda pair: render(*pair), enumerate(plans)))
(work / 'plans.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
(work / 'liste.txt').write_text(''.join(f"file 'plans/{i:02}.mp4'\n" for i in range(len(plans))), encoding='utf-8')
logo = root / 'identite/histoires-pas-banales/logos/hpb-reference-propre-v1.png'
ffmpeg('-f', 'concat', '-safe', 0, '-i', 'liste.txt', '-i', 'voix.mp3', '-i', logo,
       '-filter_complex_threads', 2, '-filter_complex',
       '[2:v]scale=206:206[logo];[0:v][logo]overlay=828:233,ass=sous-titres.ass:fontsdir=../../assets/fonts[v];'
       '[1:a]loudnorm=I=-16:TP=-1.5:LRA=7,apad[a]',
       '-map', '[v]', '-map', '[a]', '-t', duration, '-c:v', 'libx264', '-preset', 'fast',
       '-crf', 17, '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709',
       '-colorspace', 'bt709', '-c:a', 'aac', '-ar', 48000, '-b:a', '192k', '-movflags', '+faststart', 'final.mp4')

# Miniature : composée par `python miniatures_hpb.py 50` (entrée DOSSIERS[50], contrôle zones-50.jpg), puis copiée ici.
# L'ancien recadrage (crop=792:1408:1522:530) laissait voir le support noir en haut à gauche.
