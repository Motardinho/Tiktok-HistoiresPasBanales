"""Montage des deux dossiers sur les timings réels de la voix Hugo."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import re
import shutil

import yaml

from comparer_lot_16_18 import compare
from habillage_reference import layers
from montage_reel import ROOT, run
from monter_lot_16_18 import music
from narrateur import assemble
from produire_lot_16_18 import read, save
from securiser_habillage_tiktok import CARD, card, seconds, wrap_caption


ASSETS = ROOT / 'assets/lot-19-20'
CLOCK = 'jackie-VMw16PZHP7w'
TOWER = 'jackie-ticE-Eg7I8o'
POLICE_HOOK = ROOT/'assets/references-faiseemoc84/4hj7CXLKNC4-reference.mp4'
BOAT = 'bronx-IUodLjwwSBU'
OUTTAKES = 'bronx-TSh0Nm9eVlg'
PRESS = 'prise-rQoX0lBLXX0'
HANDS = 'prise-vZwcuSDE8sk'
DESK = 'prise-WwQD1s3iu_M'
ACTIVE_AREA = {CLOCK: 'crop=1280:536:0:92,',
               TOWER: 'crop=854:360:0:60,', BOAT: 'crop=1280:532:0:92,',
               OUTTAKES: 'crop=640:340:0:70,',
               (POLICE_HOOK.stem,5.65): 'crop=1280:660:0:60,',
               (OUTTAKES,106.65): 'crop=640:266:0:70,'}

# Fin sur la timeline, prise source, entrée source et cadrage.
PLANS = {
    19: [
        (5.92, CLOCK, 219.9, .43),
        (9.00, CLOCK, 222.5, .39),
        (10.60, CLOCK, 235.0, .55),
        (11.48, CLOCK, 237.35, .62),
        (14.70, CLOCK, 258.8, .49),
        (19.08, CLOCK, 263.6, .48),
        (49.94, TOWER, 8.8, .50),
        (52.00, TOWER, 12, .51),
        (55.88, TOWER, 23.45, ((0,.69),(.35,.55),(1.55,.63),(2.75,.78),(3.15,.55),(3.9,.64))),
        (60.30, TOWER, 34.2, ((0,.55),(1.35,.63),(1.8,.76),(2.7,.71),(3.15,.52),(4.4,.50))),
        (62.56, TOWER, 41.6, .60),
        (None, TOWER, 63.0, .55),
    ],
    20: [
        (2.30, HANDS, 66.5, .49),
        (3.63, DESK, 326.7, .47),
        (8.50, PRESS, 382.2, .45),
        (12.12, PRESS, 93.02, 'portrait'),
        (14.85, HANDS, 66.6, .49),
        (15.68, HANDS, 69.3, .50),
        (19.40, PRESS, 422.1, 'portrait'),
        (23.40, HANDS, 342.15, .49),
        (27.70, PRESS, 147.5, .50),
        (31.80, HANDS, 85.6, .55),
        (33.72, HANDS, 78.05, .50),
        (35.44, PRESS, 422.95, 'portrait'),
        (39.58, PRESS, 357, .54),
        (43.72, HANDS, 354.3, .56),
        (46.30, HANDS, 312.9, 'portrait'),
        (48.70, HANDS, 135, 'right'),
        (51.60, HANDS, 37.2, .49),
        (54.08, PRESS, 388, .47),
        (58.70, HANDS, 74.1, .49),
        (62.76, PRESS, 104.5, .60),
        (67.20, PRESS, 583.0, .54),
        (None, DESK, 328.4, .48),
    ],
}

NUMBERS = {
    'numéro trois': 'N°3', 'numéro deux': 'N°2', 'numéro un': 'N°1',
    'deux mille huit cent quatre-vingt-dix-neuf dollars': '2\u202f899 $',
    'deux mille vingt-six': '2026', 'six virgule cinq': '6,5',
    'trois cent neuf': '309', 'deux cent mille': '200\u202f000',
    'dix': '10', 'treize': '13', 'cent': '100', 'cinq': '5', 'trois': '3',
}

DISPLAY_PHRASES = {**NUMBERS, 'les trois âges': 'Les\u00a0Trois\u00a0Âges',
                   'côte à côte': 'côte\u00a0à\u00a0côte', 'taïm': 'TIME'}


def caption_words(words):
    tokens = [w['w'].lower().strip('.,:!?') for w in words]
    patterns = sorted(DISPLAY_PHRASES, key=lambda p: -len(p.split()))
    output = []
    i = 0
    while i < len(words):
        for p in patterns:
            end = i + len(p.split())
            if ' '.join(tokens[i:end]) != p:
                continue
            punctuation = re.search(r'[.,:!?]+$', words[end-1]['w'])
            output.append(dict(w=DISPLAY_PHRASES[p]+(punctuation.group() if punctuation else ''),
                               start=words[i]['start'], end=words[end-1]['end']))
            i = end
            break
        else:
            output.append(words[i])
            i += 1
    return output


def subtitles(m, n, timing, starts, fact, caption_start):
    cfg = yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf8'))
    cfg['render'].update(subtitle_size=78, words_per_caption=5, subtitle_wrap=19)
    assemble.YELLOW = '&H4AE2FF&'
    assemble.RED = '&H4E62FF&'
    path = m/'sous-titres.ass'
    words = caption_words([x for x in timing['words'] if x['start'] >= caption_start-.005])
    assemble.write_subtitles(cfg, words, path)
    lines = []
    for line in path.read_text(encoding='utf8').splitlines():
        if not line.startswith('Dialogue:'):
            lines.append(line)
            continue
        event = line.split(',',9)
        start, end = map(seconds, event[1:3])
        for a,b in [(start,end)]:  # la transcription continue pendant le fun fact
            if b-a < .01:
                continue
            p = event[:]
            p[1:3] = [assemble._ass_time(a),assemble._ass_time(b)]
            p[9] = r'{\an2\pos(540,1370)\fs90\fsp0}'+wrap_caption(event[9],90)
            lines.append(','.join(p))
    lines.append('')
    lines.insert(lines.index('[Events]')-1,
                 'Style: Tag,Poppins ExtraBold,46,&H004AE2FF,&H004AE2FF,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,3,16,0,8,75,75,420,1')
    tags = [(starts[1], starts[1]+3.0,'3 - L’HORLOGE'),
            (starts[3],starts[3]+3.1,'2 - JACKIE CHAN DANS LE BRONX'),
            (starts[6],starts[6]+3.1,'1 - QUI SUIS-JE ?')] if n==19 else [
            (starts[1],8.2,'GALAXY Z TRIFOLD - JANVIER 2026'),
            (19.4,23.4,'10 POUCES DÉPLIÉ'),(45,48.7,'12,9 MM FERMÉ'),(49.6,54.08,'309 G')]
    for a,b,label in tags:
        assert b<=fact[0] or a>=fact[1]
        lines.append(f'Dialogue: 1,{assemble._ass_time(a)},{assemble._ass_time(b)},Tag,,0,0,0,,{{\\an8\\pos(540,420)}}{label}')
    path.write_text('\n'.join(lines)+'\n',encoding='utf8')


def clip(row, m):
    name, at, frames, mode, i = row
    source = POLICE_HOOK if name == POLICE_HOOK.stem else ASSETS/(name+'.mp4')
    target = m/f'plan-{i:02}.mp4'
    if isinstance(mode,tuple):
        # Interpoler le centre du recadrage pendant la glissade sur la façade.
        center = str(mode[-1][1])
        for (a,x),(b,y) in reversed(list(zip(mode,mode[1:]))):
            center = f'if(lt(t,{b}),{x}+({y}-{x})*(t-{a})/({b}-{a}),{center})'
    else:
        center = {'portrait': .5, 'left': .38, 'right': .68}.get(mode, mode)
        assert isinstance(center,(int,float)) and 0<center<1
    portrait = (f"crop=trunc(min(iw\\,ih*9/16)/2)*2:trunc(min(ih\\,iw*16/9)/2)*2:"
                f"'iw*({center})-ow/2':(ih-oh)/2,scale=1080:1920,setsar=1")
    active_area = ACTIVE_AREA.get((name,at), ACTIVE_AREA.get(name,''))
    graph = '[0:v]'+active_area+portrait+'[v]'
    run(['ffmpeg','-v','error','-y','-ss',str(at),'-threads','2','-i',str(source),
         '-filter_complex_threads','1','-filter_complex',graph+';[v]fps=30,setsar=1[out]',
         '-map','[out]','-frames:v',str(frames),'-an','-c:v','libx264','-preset','ultrafast',
         '-crf','18','-threads','2','-pix_fmt','yuv420p',str(target)])
    actual = int(run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(target)]).strip())
    assert actual==frames,(target,frames,actual)


def build(n):
    w = ROOT/'out'/('19-cascades-jackie-chan' if n==19 else '20-telephone-2899-dollars')
    assert not (w/'validation-utilisateur.json').exists()
    m = w/'_montage'
    story = read(w/'histoire.json')
    timing = read(m/'timings-oraux.json')
    starts = [sum(timing['scene_durations'][:i]) for i in range(len(timing['scene_durations'])+1)]
    intro_shift = starts[1]-2.8 if n==19 else 0
    fact = (56.5,62.76)
    if n == 19:
        fact = (starts[5],starts[6])
    end = 0
    clips, manifest = [], []
    tower_shift = starts[6]-47.24 if n==19 else 0
    plans = [(until+(tower_shift if source == TOWER else intro_shift)
              if until is not None else timing['duration'], source, at, mode)
             for until, source, at, mode in PLANS[n]]
    if n == 19:
        tower_index = next(i for i, plan in enumerate(plans) if plan[1] == TOWER)
        plans[tower_index:tower_index] = [
            (starts[3]+2.96, BOAT, 2.05, .55),
            (starts[3]+5.28, BOAT, 10.85, .38),
            (starts[3]+7.12, BOAT, 13.4, ((0,.38),(.82,.39),(1.84,.45))),
            (starts[3]+9.52, BOAT, 16.32, ((0,.45),(.95,.43),(1.15,.44),(1.95,.58),(2.4,.59))),
            (starts[4], BOAT, 21.27, .49),
            (starts[4]+3.28, OUTTAKES, 34.7, .52),
            (starts[4]+5.28, OUTTAKES, 40.4, .63),
            (fact[0], OUTTAKES, 104.65, .56),
            (fact[1], OUTTAKES, 106.65, ((0,.51),(1.3,.43),(3.46,.44))),
        ]
        plans[:0] = [
            (.53, POLICE_HOOK.stem, 5.65, ((0,.56),(.53,.58))),
            (2.30, POLICE_HOOK.stem, .12, ((0,.52),(.3,.53),(.7,.51),(1.25,.6),(1.77,.52))),
            (starts[1], POLICE_HOOK.stem, 1.96, .49),
        ]
    for i,(until,source,at,mode) in enumerate(plans):
        nxt = round(until*30)
        clips.append((source,at,nxt-end,mode,i))
        manifest.append(dict(debut=end/30,fin=nxt/30,source=source,entree_source=at,cadrage=mode,type='video'))
        end = nxt
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda row:clip(row,m), clips))
    save(m/'montage.json',manifest)
    (m/'concat.txt').write_text(''.join(f"file 'plan-{i:02}.mp4'\n" for i in range(len(clips))),encoding='ascii')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','base.mp4'],m)
    music(w,m,timing,16 if n==19 else 18)
    layers(m,dict(title=story['titre_lignes'],series=story['serie'],credits='',title_bottom=1370,
                  title_left=100,title_width=750,title_size=100,title_stroke=6,tiktok_safe=True))
    CARD[n] = story['fun_fact']['texte']
    card(m,n,top=420 if n==19 else 400,padding=34)
    subtitles(m,n,timing,starts,fact,story.get('fin_annonce_titre',starts[1]))
    shutil.copy2(ROOT/'assets/fonts/Poppins-ExtraBold.ttf',m/'police.ttf')
    graph = ('[0:v]ass=sous-titres.ass:fontsdir=.[s];'
             f'[s][2:v]overlay=0:0:enable=lt(t\\,{min(2,starts[1])}):shortest=1[h];'
             '[h][3:v]overlay=0:0:shortest=1[q];'
             f'[q][4:v]overlay=60:0:enable=between(t\\,{fact[0]}\\,{fact[1]}):shortest=1[v]')
    duration = end/30
    target = m/'final.mp4'
    run(['ffmpeg','-v','error','-y','-i','base.mp4','-i','mix.wav',
         '-loop','1','-framerate','30','-i','titre-hook-reference.png',
         '-loop','1','-framerate','30','-i','header-footer-reference.png',
         '-loop','1','-framerate','30','-i','funfact-safe.png','-filter_complex_threads','2',
         '-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(duration),'-c:v','libx264',
         '-preset','veryfast','-crf','19','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
         '-movflags','+faststart',str(target)],m)
    run(['ffmpeg','-v','error','-i',str(target),'-map','0:v','-map','0:a','-f','null','-'])
    actual = float(run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration','-of','csv=p=0',str(target)]).strip())
    assert actual>60 and abs(actual-duration)<.05
    shutil.copy2(target,w/'final.mp4')
    story['fun_fact_affichage'] = dict(debut=fact[0],fin=fact[1],texte=CARD[n],mention='FUN FACT')
    story['statut'] = 'export de travail'
    save(w/'histoire.json',story)
    compare(w)
    save(m/'controle-export.json',dict(duree=actual,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                                     decodage_integral=True,comparaison_a_jour=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('numero',type=int,choices=[19,20])
    build(parser.parse_args().numero)
