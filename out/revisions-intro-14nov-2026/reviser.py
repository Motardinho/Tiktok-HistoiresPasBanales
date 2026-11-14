# Révision du 14 novembre 2026 (règle de Marc : ouverture directe, aucune lecture du titre, aucun carton ni bandeau).
# Pour 31, 33, 35, 36, 39, 42 : on repart de _montage/base.mp4 (plans sans habillage), on coupe le bloc d'accroche qui
# lisait le titre jusqu'à la phrase de contexte, on garde seulement les sous-titres (style Default, plus les bandeaux Tag),
# on pose le logo HPB validé, et on reprend la piste son de version-validee/final.mp4 coupée au même instant.
# Même méthode que out/revisions-sans-bandeaux-14nov-2026 (27 et 28). La voix n'est pas régénérée.
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
REF = ROOT / 'out/20-telephone-2899-dollars/version-validee/final.mp4'
LOGO = ROOT / 'out/revisions-fluidite-14nov-2026/28/logo.png'   # logo HPB validé, même pose que la 27 et la 28
# numéro -> (dossier, début de la phrase gardée en secondes, phrase gardée)
JOBS = {
    31: ('31-pogba-braque-pour-13-millions', 5.36, 'Mars deux mille vingt-deux.'),
    33: ('33-149-buts-contre-leur-camp', 6.24, 'Madagascar, octobre deux mille deux.'),
    35: ('35-renault-a-fait-crasher-son-pilote', 4.56, 'Singapour, septembre deux mille huit.'),
    36: ('36-mclaren-trahie-par-une-photocopie', 5.40, 'Formule Un, saison deux mille sept.'),
    39: ('39-l-entraineur-boycotte-dans-tout-le-pays', 5.68, 'Mondial deux mille vingt-six.'),
    42: ('42-top-10-plus-beaux-ballons-de-foot', 7.04, 'Numéro dix.'),
}
MARGE = 0.12  # on coupe un peu avant le premier mot gardé


def ff(args, cwd=None):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)], cwd=cwd, check=True)


def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)]))


def tm(s):
    h, m, v = s.split(':')
    return int(h) * 3600 + int(m) * 60 + float(v)


def ass(t):
    c = round(max(0, t) * 100)
    return f'{c // 360000}:{c // 6000 % 60:02}:{c // 100 % 60:02}.{c % 100:02}'


def render(n):
    name, debut, phrase = JOBS[n]
    src = ROOT / 'out' / name
    mt = src / '_montage'
    valide = src / 'version-validee/final.mp4'
    dst = OUT / str(n)
    dst.mkdir(parents=True, exist_ok=True)
    cut = round(max(0, debut - MARGE), 3)
    lignes = []
    for l in (mt / 'sous-titres.ass').read_text(encoding='utf-8-sig').splitlines():
        if l.startswith('Dialogue:'):
            a = l.split(',', 9)
            if a[3] != 'Default':  # bandeaux de contexte et fun facts : interdits
                continue
            t0, t1 = tm(a[1]), tm(a[2])
            if t1 <= cut + 0.05:
                continue
            a[1], a[2] = ass(t0 - cut), ass(t1 - cut)
            l = ','.join(a)
        lignes.append(l)
    (dst / 'sous-titres.ass').write_text('\n'.join(lignes), encoding='utf-8')
    shutil.copy2(mt / 'police.ttf', dst / 'police.ttf')
    shutil.copy2(LOGO, dst / 'logo.png')
    shutil.copy2(mt / 'base.mp4', dst / 'base.mp4')
    graph = (f'[0:v]trim=start={cut},setpts=PTS-STARTPTS,ass=sous-titres.ass:fontsdir=.[sub];'
             f'[sub][2:v]overlay=0:0:shortest=1[v];[1:a]atrim=start={cut},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.25[a]')
    ff(['-i', 'base.mp4', '-i', valide, '-loop', '1', '-i', 'logo.png', '-filter_complex_threads', '1', '-filter_complex', graph,
        '-map', '[v]', '-map', '[a]', '-t', round(dur(valide) - cut, 3), '-c:v', 'libx264', '-preset', 'fast', '-crf', '19',
        '-threads', '3', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'final.mp4'], dst)
    (dst / 'base.mp4').unlink()
    d = dur(dst / 'final.mp4')
    assert d > 60, (n, d)
    total = max(d, dur(REF))
    graph = (f'[0:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[l];'
             f'[1:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[r];'
             f'[l][r]hstack=inputs=2[v];[0:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a0];'
             f'[1:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a1]')
    ff(['-i', REF, '-i', dst / 'final.mp4', '-filter_complex_threads', '1', '-filter_complex', graph, '-map', '[v]', '-map', '[a1]',
        '-map', '[a0]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-threads', '3', '-c:a', 'aac', '-b:a', '128k',
        '-metadata:s:a:0', 'title=HPB ouverture directe', '-metadata:s:a:1', 'title=Reference telephones',
        '-disposition:a:0', 'default', '-disposition:a:1', '0', '-movflags', '+faststart', dst / 'comparaison.mp4'])
    for t in [0, 0.5, 2, 5, 10, d / 2, d - 1]:
        ff(['-ss', round(t, 2), '-i', dst / 'final.mp4', '-frames:v', '1', '-vf', 'scale=270:480', dst / f'controle-{t:05.1f}.jpg'])
    for f in ['legende.txt', 'publication.txt', 'CREDITS.md']:
        p = src / 'version-validee' / f
        if not p.exists():
            p = src / f
        if p.exists():
            shutil.copy2(p, dst / f)
    res = dict(numero=n, dossier=name, source_video=str(mt / 'base.mp4'), source_son=str(valide), coupe_secondes=cut,
               premiere_phrase=phrase, duree=round(d, 3), sha256=hashlib.sha256((dst / 'final.mp4').read_bytes()).hexdigest(),
               regle='ouverture directe, aucune lecture du titre, aucun carton ni bandeau (Marc, 14 novembre 2026)',
               voix_regeneree=False, statut='a_valider_par_Marc')
    (dst / 'controle-livraison.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(res, ensure_ascii=False), flush=True)
    return res


if __name__ == '__main__':
    nums = [int(a) for a in sys.argv[1:]] or sorted(JOBS)
    out = [render(n) for n in nums]
    man = OUT / 'manifest.json'
    old = json.loads(man.read_text(encoding='utf-8')) if man.exists() else {}
    old.update({str(r['numero']): r for r in out})
    man.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding='utf-8')
