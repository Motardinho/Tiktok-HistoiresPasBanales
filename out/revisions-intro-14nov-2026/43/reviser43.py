# Révision du 14 novembre 2026 du dossier 43 (top 3 des motos de série), règles de Marc du 14 novembre :
# ouverture directe sans lecture du titre, aucun bandeau ni encart (rangs, fun fact, bandeau de série), logo HPB validé.
# Même méthode que reviser.py (42), avec en plus les volets jaunes du top, redessinés par monter_lot_21_23
# (leurs whooshes sont dans la piste son du final.mp4 d'origine). La voix n'est pas régénérée.
# On coupe « Top trois des motos de série les plus rapides. » (lecture du titre) et on garde l'enjeu
# « La numéro un est interdite sur la route. », qui commence sur une frontière de plan (2,667 s).
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

DST = Path(__file__).resolve().parent
ROOT = DST.parents[2]
sys.path.insert(0, str(ROOT))
from monter_lot_21_23 import wipe_panel, wipe_x  # noqa: E402

SRC = ROOT / 'out/43-top-3-motos-plus-rapides'
MT = SRC / '_montage'
REF = ROOT / 'out/20-telephone-2899-dollars/version-validee/final.mp4'
LOGO = ROOT / 'out/revisions-fluidite-14nov-2026/28/logo.png'
PHRASE = 'La numéro un est interdite sur la route.'


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


plans = json.loads((MT / 'montage.json').read_text(encoding='utf-8'))
mots = json.loads((MT / 'timings-oraux.json').read_text(encoding='utf-8'))['words']
la = next(w['start'] for w in mots if w['start'] > 2 and w['w'] == 'La')  # « La numéro un est interdite… »
cut = min((p['debut'] for p in plans), key=lambda x: abs(x - la))
assert abs(cut - la) < 0.06, (cut, la)
# son coupé dans le silence avant « La » (la coupe image tombe sur la frontière de plan, au plus 1 image d'écart)
fin_avant = max(w['end'] for w in mots if w['start'] < la)
cut_son = round(min(max(cut, fin_avant), la - 0.005), 3)  # au plus près de la coupe image, dans le silence
assert fin_avant <= cut_son <= la and abs(cut_son - cut) < 0.034, (fin_avant, cut_son, la, cut)

lignes, retires = [], []
for l in (MT / 'sous-titres.ass').read_text(encoding='utf-8-sig').splitlines():
    if l.startswith('Dialogue:'):
        a = l.split(',', 9)
        if a[3] != 'Default':
            retires.append(a[9])
            continue
        t0, t1 = tm(a[1]), tm(a[2])
        if t0 < cut - 0.02:
            continue
        a[1], a[2] = ass(t0 - cut), ass(t1 - cut)
        l = ','.join(a)
    lignes.append(l)
(DST / 'sous-titres.ass').write_text('\n'.join(lignes), encoding='utf-8')

histoire = json.loads((SRC / 'histoire.json').read_text(encoding='utf-8'))
volets = [round(t - cut, 3) for t in histoire['volets_jaunes']]
assert all(t > 0.4 for t in volets), volets
wipe_panel(DST / 'volet-jaune.png')
shutil.copy2(MT / 'police.ttf', DST / 'police.ttf')
shutil.copy2(LOGO, DST / 'logo.png')
shutil.copy2(MT / 'base.mp4', DST / 'base.mp4')
src_son = SRC / 'final.mp4'
total_src = dur(src_son)
graph = (f'[0:v]trim=start={cut},setpts=PTS-STARTPTS,ass=sous-titres.ass:fontsdir=.[sub];'
         f"[sub][3:v]overlay=x='{wipe_x(volets)}':y=0:shortest=1[w];"
         f'[w][2:v]overlay=0:0:shortest=1[v];[1:a]atrim=start={cut_son},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.01[a]')
ff(['-i', 'base.mp4', '-i', src_son, '-loop', '1', '-i', 'logo.png', '-loop', '1', '-framerate', '30', '-i', 'volet-jaune.png',
    '-filter_complex_threads', '1', '-filter_complex', graph, '-map', '[v]', '-map', '[a]', '-t', round(total_src - cut, 3),
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-threads', '3', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
    'final.mp4'], DST)
(DST / 'base.mp4').unlink()
d = dur(DST / 'final.mp4')
assert d > 60, d
total = max(d, dur(REF))
graph = (f'[0:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[l];'
         f'[1:v]scale=360:640,setsar=1,tpad=stop_mode=clone:stop_duration={total},trim=duration={total},setpts=PTS-STARTPTS[r];'
         f'[l][r]hstack=inputs=2[v];[0:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a0];'
         f'[1:a]apad,atrim=duration={total},asetpts=PTS-STARTPTS[a1]')
ff(['-i', REF, '-i', DST / 'final.mp4', '-filter_complex_threads', '1', '-filter_complex', graph, '-map', '[v]', '-map', '[a1]',
    '-map', '[a0]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-threads', '3', '-c:a', 'aac', '-b:a', '128k',
    '-metadata:s:a:0', 'title=HPB ouverture directe', '-metadata:s:a:1', 'title=Reference telephones',
    '-disposition:a:0', 'default', '-disposition:a:1', '0', '-movflags', '+faststart', DST / 'comparaison.mp4'])
for t in [0, 0.5, 2, 2.7, 5, 10, d / 2, d - 1]:
    ff(['-ss', round(t, 2), '-i', DST / 'final.mp4', '-frames:v', '1', '-vf', 'scale=270:480', DST / f'controle-{t:05.1f}.jpg'])
for f in ['legende.txt', 'publication.txt', 'CREDITS.md']:
    shutil.copy2(SRC / f, DST / f)
res = dict(numero=43, dossier=SRC.name, source_video=str(MT / 'base.mp4'), source_son=str(src_son), coupe_secondes=cut, coupe_son_secondes=cut_son,
           premiere_phrase=PHRASE, duree=round(d, 3), calques_retires=retires, volets_jaunes=volets,
           sha256=hashlib.sha256((DST / 'final.mp4').read_bytes()).hexdigest(),
           regle='ouverture directe, aucune lecture du titre, aucun carton ni bandeau (Marc, 14 novembre 2026)',
           voix_regeneree=False, statut='a_valider_par_Marc')
(DST / 'controle-livraison.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
man = DST.parent / 'manifest.json'
old = json.loads(man.read_text(encoding='utf-8'))
old['43'] = res
man.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(res, ensure_ascii=False))
