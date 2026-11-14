"""Dossier 31, révision v2 (Marc, 14 novembre 2026) : hook « 13 millions d'euros » et vraies séquences.

Chaque plan finit au début d'un mot repère (timings-oraux.json). Sources 16:9 : fenêtre carrée
centrée sur le sujet, 1080x1080 au centre, fond flou du même plan (règle archives du dossier 40).
Sources verticales : plein cadre. Pexels seulement là où aucune image réelle n'existe (braquage, billets).
Aucun bandeau ni encart ; logo HPB validé ; sous-titres bas fixes.
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from narrateur.assemble import write_subtitles  # noqa: E402
from monter_lot_21_23 import caption_words  # noqa: E402
from securiser_habillage_tiktok import wrap_caption  # noqa: E402

W = Path(__file__).resolve().parent
M = W / '_montage'
R = ROOT / 'out/revisions-15nov-2026'
S31 = R / 'sources-31'
SV = R / 'sources'
PX = ROOT / 'assets/31-pogba'
SRC = ROOT / 'out/31-pogba-braque-pour-13-millions'
FPS = 30


def ff(*a, cwd=None):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str, a)], cwd=cwd, check=True)


def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', str(p)]))


J, LP, LPV, AD, EL, KI, AFP, AFP2, FIG, MON = (S31 / 'x8jKwFtoV7c.mp4', S31 / '8hD6fgR93jM.mp4',
                                             S31 / 'WpP9VkoO7-g.mp4', S31 / 'S_sMDNY-9PA.mp4',
                                             S31 / '17f320DMdLY.mp4', S31 / '-VCsVIWLDCE.mp4',
                                             SV / 'KCLUsiKZP1s.mp4', S31 / 'eLUsfD5ZbH4.mp4',
                                             S31 / '7yP3HAcCDQc.mp4', S31 / 'qhbAqh96OoA.mp4')
CARRE = SV / 'VFuZMU9rGA8.mp4'
PHOTO = SV / 'freres-pogba.jpg'
P = lambda i: PX / f'pexels-{i}.mp4'  # noqa: E731

# (mot repère qui ouvre le plan suivant, source, entrée, type, centre x, centre y, côté, note)
# type : sq = fenêtre carrée sur flou ; v = vertical plein cadre ; photo.
ROWS = [
    ('pour', J, 1.0, 'sq', 1100, 540, 1080, 'Juventus (chaîne officielle) : Pogba en pleine reprise de volée'),
    ('et', J, 130.0, 'sq', 1250, 540, 900, 'Juventus : gros plan de Pogba, maillot n° 6'),
    ('son', KI, 36.0, 'sq', 960, 540, 1000, 'AP, 19 déc. 2024, jour du verdict : policiers au tribunal de Paris'),
    ('mars', KI, 10.0, 'sq', 1250, 540, 900, 'AP, 19 déc. 2024 : Mathias Pogba (doudoune beige) arrive au verdict'),
    ('paul', AD, 62.6, 'sq', 1100, 540, 1000, 'Pub adidas « Le créateur » : Pogba sous le maillot de Manchester United'),
    ('retrouve', EL, 180.0, 'sq', 750, 450, 900, "L'Équipe, 16 juil. 2018 : Pogba champion du monde, micro à l'Élysée"),
    ('et', EL, 185.0, 'sq', 620, 450, 900, "L'Équipe, 16 juil. 2018 : Pogba au micro, fête à l'Élysée"),
    ('deux', P(4547598), 1.0, 'v', 0, 0, 0, 'PEXELS (aucune image du braquage) : porte sur une pièce sombre'),
    ('armes', P(6670907), 18.0, 'v', 0, 0, 0, 'PEXELS (aucune image du braquage) : cagoule'),
    ('le', P(6091316), 8.0, 'v', 0, 0, 0, 'PEXELS (aucune image du braquage) : arme braquée'),
    ('pogba', P(29992749), 1.0, 'v', 0, 0, 0, 'PEXELS (pas de vraie image) : billets en euros'),
    ('quand', CARRE, 414.0, 'sq', 1250, 540, 900, 'CARRÉ, 27 oct. 2024 : Paul Pogba raconte'),
    ('les', CARRE, 435.3, 'sq', 1250, 540, 900, 'CARRÉ, 27 oct. 2024 : Paul Pogba raconte'),
    ('mais', LP, 14.0, 'sq', 1350, 650, 760, 'Le Parisien, 23 sept. 2022 : Paul Pogba'),
    ('ses', AFP2, 18.0, 'sq', 1000, 540, 1000, 'AFP, 3 déc. 2024 : couloir du tribunal de Paris, procès Pogba'),
    ('le', P(31402662), 2.0, 'v', 0, 0, 0, 'PEXELS (pas de vraie image) : liasse d’euros'),
    ('une', AFP, 1.0, 'sq', 900, 540, 1000, 'AFP, 26 nov. 2024 : ouverture du procès, entrée dans la salle'),
    ('six', AD, 64.37, 'sq', 1400, 540, 1000, 'Pub adidas « Le créateur » : Pogba en action'),
    ('plus', AD, 68.95, 'sq', 1150, 540, 1000, 'Pub adidas « Le créateur » : Pogba en action'),
    ('pogba', AD, 71.75, 'sq', 1000, 540, 1000, 'Pub adidas « Le créateur » : Pogba en action'),
    ('et', AD, 62.52, 'sq', 1100, 540, 1000, 'Pub adidas « Le créateur » : visage de Pogba'),
    ('en', LP, 1.0, 'sq', 960, 540, 1000, 'Le Parisien, 23 sept. 2022 : Mathias Pogba lit sa déclaration'),
    ('il', LP, 29.0, 'sq', 960, 540, 1080, 'Le Parisien, 23 sept. 2022 : la vidéo publiée par Mathias sur les réseaux'),
    ('marabouter', LP, 64.3, 'sq', 950, 540, 1000, 'Le Parisien, 23 sept. 2022 : Paul Pogba en équipe de France'),
    ('paul', LP, 122.7, 'sq', 820, 540, 1000, 'Le Parisien : Mbappé, PSG - Manchester United 2019'),
    ('décembre', J, 258.9, 'sq', 1000, 540, 1000, 'Juventus : Pogba'),
    ('le', KI, 50.0, 'sq', 960, 540, 1000, 'AP, 19 déc. 2024 : police au tribunal, jour du verdict'),
    ('les', KI, 71.0, 'sq', 900, 540, 1000, 'AP, 19 déc. 2024 : cordon de police au tribunal'),
    ('mathias', KI, 80.3, 'sq', 960, 540, 1000, 'AP, 19 déc. 2024 : POLICE, brigade d’appui'),
    ('prend', KI, 3.0, 'sq', 1250, 540, 1000, 'AP, 19 déc. 2024 : Mathias Pogba arrive au verdict'),
    ('il', KI, 13.0, 'sq', 1100, 540, 900, 'AP, 19 déc. 2024 : Mathias Pogba face aux policiers'),
    ('et', FIG, 7.2, 'sq', 1000, 300, 560, 'Le Figaro / AFP, 19 déc. 2024 : son avocat annonce un appel'),
    ('mais', AFP, 38.5, 'sq', 960, 540, 1000, 'AFP, 26 nov. 2024 : la salle des pas perdus, sans Paul'),
    ('longue', PHOTO, 0, 'photo', 0, 0, 0, 'Photo publiée par Paul Pogba le 19 août 2025'),
    ('alors', MON, 7.0, 'sq', 960, 540, 760, 'AS TV, 28 juin 2025 : Pogba en larmes à la signature à Monaco'),
    ('réponds', MON, 23.0, 'sq', 960, 540, 760, 'AS TV, 28 juin 2025 : Pogba en larmes'),
    (None, EL, 192.5, 'sq', 750, 450, 900, "L'Équipe, 16 juil. 2018 : Pogba au micro à l'Élysée"),
]


def tok(w):
    return re.sub(r"[.,:;!?…]+$", '', w.lower().replace('’', "'"))


def plans():
    t = json.loads((M / 'timings-oraux.json').read_text(encoding='utf-8'))
    words, toks = t['words'], [tok(x['w']) for x in t['words']]
    out, cursor, start = [], -1, 0
    for anchor, src, ss, kind, cx, cy, side, note in ROWS:
        if anchor:
            cursor = next(i for i in range(cursor + 1, len(toks)) if toks[i] == anchor)
            end = round(words[cursor]['start'] * FPS)
        else:
            end = round(t['duration'] * FPS)
        assert end - start >= 15, (anchor, note)
        out.append(dict(debut=start / FPS, fin=end / FPS, frames=end - start, source=str(src), entree=ss,
                        type=kind, cx=cx, cy=cy, cote=side, note=note))
        start = end
    return out, t


def clip(i, p):
    f = M / f'plan-{i:02}.mp4'
    src, n = p['source'], p['frames']
    if p['type'] == 'v':
        inp = ['-ss', p['entree'], '-i', src]
        g = '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p[v]'
    elif p['type'] == 'photo':
        inp = ['-loop', '1', '-i', src]
        g = ('[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30,'
             'eq=brightness=-0.1[bg];[b]scale=-2:1100[fg];[bg][fg]overlay=(W-w)/2:480,'
             "zoompan=z='1+0.0004*on':x=iw/2-iw/zoom/2:y=ih/2-ih/zoom/2:d=1:s=1080x1920:fps=30,format=yuv420p[v]")
    else:
        s, x, y = p['cote'], p['cx'] - p['cote'] // 2, p['cy'] - p['cote'] // 2
        inp = ['-ss', p['entree'], '-i', src]
        g = ('[0:v]fps=30,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
             f'gblur=sigma=40,eq=brightness=-0.15[bg];[b]scale=1920:1080,crop={s}:{s}:{x}:{y},scale=1080:1080:flags=lanczos[fg];'
             '[bg][fg]overlay=0:400,setsar=1,format=yuv420p[v]')
    ff(*inp, '-filter_complex_threads', '1', '-filter_complex', g, '-map', '[v]', '-an', '-frames:v', n,
       '-r', FPS, '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-threads', '3', f)
    got = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                                       '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(f)]))
    assert got == n, (i, p['note'], got, n)


def subtitles(t):
    cfg = yaml.safe_load((ROOT / 'config.yaml').read_text(encoding='utf-8'))
    story = json.loads((SRC / 'histoire.json').read_text(encoding='utf-8'))
    aff = dict(story['affichage'])
    words = caption_words(t['words'], aff)
    words[0]['start'] = 0
    write_subtitles(cfg, words, M / 'sous-titres.ass')
    lines = []
    for l in (M / 'sous-titres.ass').read_text(encoding='utf-8').splitlines():
        if l.startswith('Dialogue:'):
            a = l.split(',', 9)
            size = 90
            txt = wrap_caption(a[9], size)
            if txt.count(r'\N') > 2:
                size = 80
                txt = wrap_caption(a[9], size)
            a[9] = r'{\an2\pos(540,1370)\fs' + str(size) + r'\fsp0}' + txt
            l = ','.join(a)
        lines.append(l)
    (M / 'sous-titres.ass').write_text('\n'.join(lines), encoding='utf-8')


def main(only=None):
    ps, t = plans()
    (M / 'plans.json').write_text(json.dumps(ps, ensure_ascii=False, indent=2), encoding='utf-8')
    todo = [i for i in range(len(ps)) if only is None or i in only]
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda i: clip(i, ps[i]), todo))
    (M / 'concat.txt').write_text(''.join(f"file 'plan-{i:02}.mp4'\n" for i in range(len(ps))), encoding='ascii')
    ff('-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'base.mp4', cwd=M)
    subtitles(t)
    for f in ['logo.png', 'police.ttf']:
        (M / f).write_bytes((R / '31' / f).read_bytes())
    ff('-i', 'base.mp4', '-i', 'mix.wav', '-loop', '1', '-i', 'logo.png', '-filter_complex_threads', '1',
       '-filter_complex', '[0:v]ass=sous-titres.ass:fontsdir=.[s];[s][2:v]overlay=0:0:shortest=1[v]',
       '-map', '[v]', '-map', '1:a', '-t', t['duration'], '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
       '-threads', '3', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
       '../final.mp4', cwd=M)
    ref = SRC / 'version-validee/final.mp4'
    total = max(dur(ref), dur(W / 'final.mp4'))
    g = (f'[0:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[l];'
         f'[1:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[r];'
         f'[l][r]hstack[v];[0:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a0];'
         f'[1:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a1]')
    ff('-i', ref, '-i', W / 'final.mp4', '-filter_complex_threads', '1', '-filter_complex', g, '-map', '[v]',
       '-map', '[a1]', '-map', '[a0]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-threads', '3',
       '-c:a', 'aac', '-b:a', '128k', '-metadata:s:a:0', 'title=HPB revision v2',
       '-metadata:s:a:1', 'title=Reference version validee', '-disposition:a:0', 'default',
       '-disposition:a:1', '0', '-movflags', '+faststart', W / 'comparaison.mp4')
    print('final', round(dur(W / 'final.mp4'), 2), 's ; comparaison', round(dur(W / 'comparaison.mp4'), 2), 's')


if __name__ == '__main__':
    main(None if len(sys.argv) < 2 else {int(x) for x in sys.argv[1].split(',')})
