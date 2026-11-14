"""Montage piloté par les données pour les dossiers 21 et suivants.

Tout ce qui est propre à une vidéo vit dans son dossier :
- `histoire.json` : titre, série, scènes, fun fact, bandeaux, musique, affichage des nombres ;
- `_montage/plans.json` : liste ordonnée de plans réels
  `{"fin": secondes sur la timeline ou null pour le dernier, "source": fichier
  relatif à assets/, "entree": seconde dans la source, "cadrage": centre 0-1,
  "portrait", ou liste [[t, centre], ...], "zone": recadrage ffmpeg optionnel}`.

Usage : python monter_lot_21_23.py voix 21 | plans 21 | montage 21
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import re
from pathlib import Path
import shutil

import wave

import numpy as np
from PIL import Image, ImageDraw
import yaml

from comparer_lot_16_18 import compare
from habillage_reference import layers
from montage_reel import ROOT, run
from monter_lot_16_18 import mix_voice
from narrateur import assemble
from produire_lot_16_18 import read, save, speech
from securiser_habillage_tiktok import CARD, card, seconds, wrap_caption

ASSETS = ROOT / 'assets'
RANGS = {'numéro trois': 'N°3', 'numéro deux': 'N°2', 'numéro un': 'N°1'}
# Volet entre les sujets d'un top (demande de Marc du 11 nov. 2026, d'après un Short d'actu foot
# en bleu) : panneau jaune uni à bords inclinés « / » qui entre par la gauche, couvre l'écran,
# puis repart vers la droite en découvrant le rang suivant. La coupe de plan tombe sous le panneau.
VOLET = dict(couleur='#FFE24A', biais=220, entree=.13, tenue=.40, sortie=.13, whoosh=.45)


def folder(n):
    return next((ROOT / 'out').glob(f'{n}-*'))


def scene_starts(timing):
    d = timing['scene_durations']
    return [sum(d[:i]) for i in range(len(d) + 1)]


def title_end(story, timing):
    """Début du premier mot qui suit l'annonce orale du titre."""
    if 'fin_annonce_titre' in story:
        return story['fin_annonce_titre']
    first = re.split(r'(?<=[.!?])\s', story['scenes'][0]['narration_voix'])[0]
    count = len(first.split())
    words = timing['words']
    return words[count]['start'] if count < len(words) else timing['duration']


def caption_words(words, phrases):
    tokens = [w['w'].lower().replace('’', "'").strip('.,:;!?') for w in words]
    table = {k.lower().replace('’', "'"): v for k, v in phrases.items()}
    patterns = sorted(table, key=lambda p: -len(p.split()))
    output, i = [], 0
    while i < len(words):
        for p in patterns:
            end = i + len(p.split())
            if ' '.join(tokens[i:end]) != p:
                continue
            punctuation = re.search(r'[.,:;!?]+$', words[end - 1]['w'])
            output.append(dict(w=table[p] + (punctuation.group() if punctuation else ''),
                               start=words[i]['start'], end=words[end - 1]['end']))
            i = end
            break
        else:
            output.append(words[i])
            i += 1
    # La ponctuation française haute reste attachée au mot précédent.
    for w in output:
        w['w'] = re.sub(r'\s+([?!:;])', ' \\1', w['w'])
    merged = []
    for w in output:
        if merged and re.fullmatch(r'[?!:;»]+', w['w']):
            merged[-1] = dict(merged[-1], w=merged[-1]['w'] + ' ' + w['w'], end=w['end'])
        else:
            merged.append(w)
    return merged


def fact_window(story, starts):
    f = story['fun_fact']
    return (f.get('debut', starts[f['scene']]), f.get('fin', starts[f['scene'] + 1]))


def tags(story, starts, fact):
    if story.get('bandeaux_classement_visibles') is False:
        return []
    rows = []
    for b in story.get('bandeaux', []):
        a = b['debut'] if 'debut' in b else starts[b['scene']] + b.get('apres', 0)
        z = b['fin'] if 'fin' in b else a + b.get('duree', 3.1)
        a = max(story.get('bandeaux_debut_min', 1.5), a)
        assert z <= fact[0] + .001 or a >= fact[1] - .001, ('bandeau pendant le fun fact', b)
        rows.append((a, z, b['texte']))
    return rows


def wipe_times(story, timing, starts, cuts):
    """Milieu de chaque volet : le mot « numéro » qui ouvre une scène à bandeau de rang,
    recalé sur la coupe de plan la plus proche (moins de 0,5 s) pour la cacher sous le panneau."""
    if story.get('format') != 'top' or story.get('transitions') is False:
        return []
    times = []
    for b in story.get('bandeaux', []):
        if 'scene' not in b:
            continue
        a, z = starts[b['scene']] - .05, starts[b['scene'] + 1]
        hit = next((w['start'] for w in timing['words']
                    if a <= w['start'] < z and w['w'].lower().strip('.,:;!?') == 'numéro'), None)
        if hit is None:
            continue
        if hit < .34 and story.get('depart_direct_classement'):
            continue
        near = min(cuts, key=lambda c: abs(c - hit), default=hit)
        times.append(round(near if abs(near - hit) <= .5 else hit, 3))
    half = VOLET['tenue'] / 2 + max(VOLET['entree'], VOLET['sortie'])
    assert all(t - half >= 0 for t in times), ('volet avant le début', times)
    assert all(b - a > 2 * half for a, b in zip(times, times[1:])), ('volets qui se chevauchent', times)
    return times


def wipe_panel(path):
    """Parallélogramme jaune de 1080 + 2 × biais de large, bords lissés (dessin à 2x)."""
    s = VOLET['biais']
    width = 1080 + 2 * s
    big = Image.new('RGBA', (2 * width, 2 * 1920), (0, 0, 0, 0))
    ImageDraw.Draw(big).polygon([(2 * s, 0), (2 * width, 0), (2 * (width - s), 2 * 1920), (0, 2 * 1920)],
                                fill=VOLET['couleur'])
    big.resize((width, 1920), Image.LANCZOS).save(path)


def wipe_x(times):
    """Abscisse du panneau : entrée amortie, tenue plein écran, sortie accélérée, hors champ sinon."""
    s = VOLET['biais']
    width = 1080 + 2 * s
    e, h, o = VOLET['entree'], VOLET['tenue'], VOLET['sortie']
    expr = '2000'
    for c in reversed(times):
        t0, t1, t2, t3 = c - h / 2 - e, c - h / 2, c + h / 2, c + h / 2 + o
        enter = f'-{width}+{width - s}*(1-pow(1-(t-{t0:.3f})/{e},3))'
        leave = f'-{s}+{1080 + s}*pow((t-{t2:.3f})/{o},2)'
        expr = (f'if(between(t,{t0:.3f},{t1:.3f}),{enter},if(between(t,{t1:.3f},{t2:.3f}),-{s},'
                f'if(between(t,{t2:.3f},{t3:.3f}),{leave},{expr})))')
    return expr


def whoosh(seed=0, rate=44100):
    """Souffle de synthèse (aucun son tiers) : bruit dans un passe-bande glissant, montée 0,25 s
    jusqu'au plein écran jaune puis retombée 0,55 s, panoramique gauche → droite comme le panneau."""
    rise, fall = .25, .55
    t = np.arange(int((rise + fall) * rate)) / rate
    noise = np.random.default_rng(seed).standard_normal(len(t))
    up, down = np.clip(t / rise, 0, 1), np.clip((t - rise) / fall, 0, 1)
    env = np.where(t < rise, up ** 2.2, (1 - down) ** 2.5)
    f = 2 * np.sin(np.pi * np.where(t < rise, 350 + 3200 * up ** 1.5, 3550 - 2900 * down ** .7) / rate)
    low = band = 0.0
    out = np.empty(len(t))
    for i, x in enumerate(noise):  # filtre à variable d'état, Q = 1,4
        low += f[i] * band
        band += f[i] * (x - low - band / 1.4)
        out[i] = band
    out *= env / np.abs(out * env).max()
    pan = t / t[-1] * np.pi / 2
    return np.stack([out * np.cos(pan), out * np.sin(pan)], axis=1) * 1.3


def whoosh_track(path, times, duration, rate=44100):
    """Piste stéréo des whooshs, crête du souffle sur l'instant où le panneau couvre l'écran.
    Gain .45 : environ 6 dB sous la voix (validé par Marc le 11 nov. 2026 sur l'aperçu du 25)."""
    buf = np.zeros((int((duration + 1) * rate), 2))
    for k, c in enumerate(times):
        start = int((c - VOLET['tenue'] / 2 - .02 - .25) * rate)
        w = whoosh(k, rate) * VOLET['whoosh']
        buf[start:start + len(w)] += w
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(rate)
        f.writeframes((np.clip(buf, -1, 1) * 32767).astype('<i2').tobytes())


def subtitles(m, story, timing, starts, fact, caption_start):
    cfg = yaml.safe_load((ROOT / 'config.yaml').read_text(encoding='utf8'))
    cfg['render'].update(subtitle_size=78, words_per_caption=5, subtitle_wrap=19)
    assemble.YELLOW = '&H4AE2FF&'
    assemble.RED = '&H4E62FF&'
    path = m / 'sous-titres.ass'
    phrases = {**RANGS, **story.get('affichage', {})}
    words = caption_words([x for x in timing['words'] if x['start'] >= caption_start - .005], phrases)
    assemble.write_subtitles(cfg, words, path)
    lines = []
    for line in path.read_text(encoding='utf8').splitlines():
        if not line.startswith('Dialogue:'):
            lines.append(line)
            continue
        event = line.split(',', 9)
        start, end = map(seconds, event[1:3])
        # Demande de Marc : la transcription continue pendant le fun fact.
        for a, b in [(start, end)]:
            if b - a < .01:
                continue
            p = event[:]
            p[1:3] = [assemble._ass_time(a), assemble._ass_time(b)]
            p[9] = r'{\an2\pos(540,1370)\fs90\fsp0}' + wrap_caption(event[9], 90)
            lines.append(','.join(p))
    lines.append('')
    lines.insert(lines.index('[Events]') - 1,
                 'Style: Tag,Poppins ExtraBold,96,&H004AE2FF,&H004AE2FF,&H001C1512,&H001C1512,0,0,0,0,100,100,0,0,3,16,0,8,75,75,420,1')
    # `bandeau_y` : haut du bandeau de rang (420 par défaut) ; 380 au-dessus des extraits posés à y = 610 (dossier 40).
    y = story.get('bandeau_y', 420)
    for a, b, label in tags(story, starts, fact):
        lines.append(f'Dialogue: 1,{assemble._ass_time(a)},{assemble._ass_time(b)},Tag,,0,0,0,,{{\\an8\\pos(540,{y})}}{label}')
    path.write_text('\n'.join(lines) + '\n', encoding='utf8')


def clip(row, m):
    source, at, frames, mode, zone, i = row
    target = m / f'plan-{i:02}.mp4'
    if isinstance(mode, list):
        center = str(mode[-1][1])
        for (a, x), (b, y) in reversed(list(zip(mode, mode[1:]))):
            center = f'if(lt(t,{b}),{x}+({y}-{x})*(t-{a})/({b}-{a}),{center})'
    else:
        center = .5 if mode == 'portrait' else mode
        assert isinstance(center, (int, float)) and 0 < center < 1, mode
    portrait = (f"crop=trunc(min(iw\\,ih*9/16)/2)*2:trunc(min(ih\\,iw*16/9)/2)*2:"
                f"'min(max(iw*({center})-ow/2\\,0)\\,iw-ow)':(ih-oh)/2,scale=1080:1920:flags=lanczos,setsar=1")
    still = Path(source).suffix.lower() in ('.jpg', '.jpeg', '.png')
    if still:
        # Photo d'archive (exception documentée) : zoom lent, recadrage 9:16 fixe.
        d = frames / 30
        portrait = portrait.replace('scale=1080:1920', 'scale=1188:2112') + \
            f",crop=1080:1920:'(iw-ow)/2*(1-0.6*t/{d:.3f})':'(ih-oh)/2*(1-0.6*t/{d:.3f})'"
    # Une source HDR (HLG/PQ, BT.2020) convertie sans tonemapping sort délavée : la refuser.
    transfer = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer',
                    '-of', 'csv=p=0', str(ASSETS / source)]).strip()
    assert transfer not in ('arib-std-b67', 'smpte2084'), ('source HDR refusée', source, transfer)
    graph = '[0:v]' + (zone + ',' if zone else '') + portrait + '[v]'
    source_input = ['-loop', '1', '-framerate', '30', '-i', str(ASSETS / source)] if still else \
        ['-ss', str(at), '-i', str(ASSETS / source)]
    # Tous les plans en BT.709, plage TV : des paramètres hétérogènes cassent le décodage
    # aux coupes de la concaténation sans réencodage (images sans habillage, dossier 26).
    normalize = ('scale=out_range=tv:out_color_matrix=bt709,format=yuv420p,'
                 'setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709')
    run(['ffmpeg', '-v', 'error', '-y', '-threads', '2', *source_input,
         '-filter_complex_threads', '1', '-filter_complex', graph + f';[v]setpts=PTS-STARTPTS,fps=30,setsar=1,{normalize}[out]',
         '-map', '[out]', '-frames:v', str(frames), '-an', '-c:v', 'libx264', '-preset', 'veryfast',
         '-crf', '17', '-threads', '2', '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-colorspace', 'bt709',
         '-color_primaries', 'bt709', '-color_trc', 'bt709', str(target)])
    actual = int(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                      'stream=nb_frames', '-of', 'csv=p=0', str(target)]).strip().split(',')[0])
    assert actual == frames, (target.name, source, at, frames, actual)


def music(story, m, duration):
    directory = ASSETS / 'musique/mixkit'
    track = next(x for x in read(directory / 'sources.json') if x['slug'] == story['musique'])
    bed = m / 'musique.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(track['start']), '-i', str(directory / (track['slug'] + '.mp3')),
         '-af', f'atrim=duration={duration},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2:LRA=9,'
                f'afade=t=in:d=0.8,afade=t=out:st={duration - 2}:d=2', '-ar', '44100', '-ac', '2', str(bed)])
    mix_voice(m / 'voix.mp3', bed, m / 'mix.wav', duration, run)
    return track


def base(n):
    """Découpe et assemble les plans sans habillage (base.mp4)."""
    w = folder(n)
    m = w / '_montage'
    timing = read(m / 'timings-oraux.json')
    plans = read(m / 'plans.json')
    end, clips, manifest = 0, [], []
    for i, p in enumerate(plans):
        until = timing['duration'] if p['fin'] is None else p['fin']
        nxt = round(until * 30)
        assert nxt - end >= 15, ('plan trop court', i, p)
        clips.append((p['source'], p['entree'], nxt - end, p['cadrage'], p.get('zone'), i))
        manifest.append(dict(debut=end / 30, fin=nxt / 30, source=p['source'], entree_source=p['entree'],
                             cadrage=p['cadrage'], type='video', note=p.get('note', '')))
        end = nxt
    # Aucun extrait répété : les intervalles d'une même source restent disjoints.
    spans = sorted((c[0], c[1], c[1] + c[2] / 30) for c in clips)
    for a, b in zip(spans, spans[1:]):
        assert a[0] != b[0] or a[2] <= b[1] + .05, ('extraits qui se chevauchent', a, b)
    for old in m.glob('plan-*.mp4'):
        old.unlink()
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda row: clip(row, m), clips))
    save(m / 'montage.json', manifest)
    (m / 'concat.txt').write_text(''.join(f"file 'plan-{i:02}.mp4'\n" for i in range(len(clips))), encoding='ascii')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'base.mp4'], m)
    return end / 30


def build(n, only_dress=False):
    w = folder(n)
    assert not (w / 'validation-utilisateur.json').exists(), 'version validée : ne pas remonter'
    m = w / '_montage'
    story = read(w / 'histoire.json')
    timing = read(m / 'timings-oraux.json')
    starts = scene_starts(timing)
    fact = fact_window(story, starts)
    duration = round(timing['duration'] * 30) / 30
    if not only_dress or not (m / 'base.mp4').exists():
        duration = base(n)
    music(story, m, timing['duration'])
    cuts = [x['debut'] for x in read(m / 'montage.json')][1:]
    wipes = wipe_times(story, timing, starts, cuts)
    audio = 'mix.wav'
    if wipes:
        whoosh_track(m / 'volets-whoosh.wav', wipes, timing['duration'])
        audio = 'mix-volets.wav'
        run(['ffmpeg', '-v', 'error', '-y', '-i', 'mix.wav', '-i', 'volets-whoosh.wav', '-filter_complex',
             '[0:a][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[a]',
             '-map', '[a]', '-ar', '44100', '-c:a', 'pcm_s16le', audio], m)
    layers(m, dict(title=story['titre_lignes'], series=story['serie'], credits='', title_bottom=1370,
                   title_left=100, title_width=750, title_size=story.get('titre_taille', 100), title_stroke=6, title_line_gap=story.get('titre_interligne', 8),
                   tiktok_safe=True))
    if story.get('habillage_entete_fichier'):
        shutil.copy2(ROOT / story['habillage_entete_fichier'], m / 'header-footer-reference.png')
    CARD[n] = story['fun_fact']['texte']
    # Encart en haut par défaut ; `fun_fact_top` pour une vidéo dont le sujet occupe le haut du cadre.
    card(m, n, top=story.get('fun_fact_top', 420), padding=34)
    announce = title_end(story, timing)
    title_duration = announce if story.get('titre_jusqua_annonce') else min(2, announce)
    if story.get('titre_ouverture_visible') is False:
        title_duration = 0
    subtitles(m, story, timing, starts, fact, announce)
    shutil.copy2(ROOT / 'assets/fonts/Poppins-ExtraBold.ttf', m / 'police.ttf')
    graph = ('[0:v]ass=sous-titres.ass:fontsdir=.[s];'
             f'[s][2:v]overlay=0:0:enable=lt(t\\,{title_duration}):shortest=1[h];'
             '[h][3:v]overlay=0:0:shortest=1[q];'
             f'[q][4:v]overlay=60:0:enable=between(t\\,{fact[0]}\\,{fact[1]}):shortest=1[v]')
    wipe_input = []
    if wipes:
        wipe_panel(m / 'volet-jaune.png')
        wipe_input = ['-loop', '1', '-framerate', '30', '-i', 'volet-jaune.png']
        graph = graph.replace('[v]', '[f]') + f";[f][5:v]overlay=x='{wipe_x(wipes)}':y=0:shortest=1[v]"
    target = m / 'final.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-i', 'base.mp4', '-i', audio,
         '-loop', '1', '-framerate', '30', '-i', 'titre-hook-reference.png',
         '-loop', '1', '-framerate', '30', '-i', 'header-footer-reference.png',
         '-loop', '1', '-framerate', '30', '-i', 'funfact-safe.png', *wipe_input, '-filter_complex_threads', '2',
         '-filter_complex', graph, '-map', '[v]', '-map', '1:a:0', '-t', str(duration), '-c:v', 'libx264',
         '-preset', 'veryfast', '-crf', '19', '-threads', '3', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
         '-movflags', '+faststart', str(target)], m)
    run(['ffmpeg', '-v', 'error', '-i', str(target), '-map', '0:v', '-map', '0:a', '-f', 'null', '-'])
    probe = lambda kind: float(run(['ffprobe', '-v', 'error', '-select_streams', f'{kind}:0', '-show_entries',
                                    'stream=duration', '-of', 'csv=p=0', str(target)]).strip())
    video, audio = probe('v'), probe('a')
    assert video > 60, f'vidéo trop courte : {video}'
    assert abs(video - duration) < .05 and abs(video - audio) < .3, (video, audio, duration)
    shutil.copy2(target, w / 'final.mp4')
    story['fin_annonce_titre_mesuree'] = announce
    story['fun_fact_affichage'] = dict(debut=fact[0], fin=fact[1], texte=CARD[n], mention='FUN FACT')
    story['volets_jaunes'] = wipes
    story['statut'] = 'export de travail'
    save(w / 'histoire.json', story)
    compare(w)
    save(m / 'controle-export.json', dict(duree_video=video, duree_audio=audio,
                                         sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                                         decodage_integral=True, comparaison_a_jour=True))
    print(n, 'final et comparaison prêts', round(video, 2), 's', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('etape', choices=['voix', 'montage', 'habillage'])
    parser.add_argument('numero', type=int)
    args = parser.parse_args()
    if args.etape == 'voix':
        speech(folder(args.numero))
        t = read(folder(args.numero) / '_montage/timings-oraux.json')
        print('durée', round(t['duration'], 2), 'scènes', [round(x, 2) for x in scene_starts(t)])
    else:
        build(args.numero, only_dress=args.etape == 'habillage')
