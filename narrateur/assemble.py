import shutil
import subprocess
import re
from pathlib import Path

from .tampon import make_stamp

ROOT = Path(__file__).resolve().parent.parent
YELLOW, RED = "&H00E6FF&", "&H3C3CFF&"


def _run(cmd: list[str], cwd: Path):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)


def _ass_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _bind_punctuation(words: list[dict]) -> list[dict]:
    """Attacher la ponctuation fermante avant blocs/lignes, sans modifier la source."""
    result = []
    for word in words:
        item = dict(word)
        token = item['w'].strip()
        if token and all(ch in '.,!?;:…)]}»”’' for ch in token) and result:
            previous = result[-1]
            previous['w'] = previous['w'].rstrip() + ('\u00a0' if token[0] in '!?;:»' else '') + token
            previous['end'] = max(previous['end'], item['end'])
        else:
            item['w'] = re.sub(r'\s+([!?;:»])', '\u00a0\\1', item['w'])
            item['w'] = re.sub(r'\s+([.,…\)\]\}])', r'\1', item['w'])
            result.append(item)
    return result


# Compatibilité avec les scripts de révision existants.
_bind_colons = _bind_punctuation


def _chunks(words: list[dict], max_words: int) -> list[list[dict]]:
    """Phrases de max_words mots au plus, coupées de préférence aux points et aux virgules."""
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        tok = w["w"].rstrip()
        if tok[-1:] in ".!?…" or (tok[-1:] == "," and len(cur) >= 4) or len(cur) >= max_words:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def _wrap(tokens: list[str], width: int) -> list[list[int]]:
    """Indices des mots par ligne, lignes d'au plus `width` caractères."""
    lines, cur, n = [], [], 0
    for i, t in enumerate(tokens):
        if cur and n + 1 + len(t) > width and not t.lstrip().startswith(tuple('.,!?;:…)]}»”’')):
            lines.append(cur)
            cur, n = [], 0
        n += len(t) + (1 if cur else 0)
        cur.append(i)
    if cur:
        lines.append(cur)
    return lines


def _reveal(chunk: list[dict], k: int, width: int, last: bool) -> str:
    """Phrase entière en place (mise en page stable), mots 0..k visibles, mot dit en jaune."""
    tokens = [w["w"] for w in chunk]
    out = []
    for line in _wrap(tokens, width):
        parts = []
        for i in line:
            t = tokens[i].replace('\u00a0', r'\h')
            if any(ch.isdigit() for ch in t):
                parts.append("{\\c" + RED + "}" + t + "{\\c}")
            elif i == k:
                parts.append("{\\c" + YELLOW + "}" + t + "{\\c}")
            else:
                parts.append(t)
        out.append(" ".join(parts))
    return ("{\\fad(0,90)}" if last else "") + "\\N".join(out)


def stamp_time(words: list[dict]) -> float | None:
    """Instant où « clos » est prononcé (fin du dossier), pour le tampon."""
    for w in reversed(words):
        if w["w"].lower().strip(".,!?…").startswith("clos"):
            return w["start"]
    return None


def stamp_filter(index: int, at: float, width: int = 940, center_y: int = 830) -> str:
    """Tampon encreur posé sur le visuel : part grossi (x2,6), s'écrase en 0,12 s avec un petit rebond.

    `index` est le numéro de l'entrée ffmpeg qui porte tampon.png (en boucle, 30 i/s).
    """
    grow = "1+1.6*max(0,1-t/0.12)+0.05*max(0,min(1,(t-0.12)/0.06))*max(0,1-(t-0.12)/0.2)"
    return (f"[{index}:v]format=rgba,scale=w='trunc({width}*({grow})/2)*2':h=-1:eval=frame,"
            f"fade=in:st=0:d=0.05:alpha=1,setpts=PTS+{at:.3f}/TB[st];"
            f"[sub][st]overlay=x='(W-w)/2':y='{center_y}-h/2':enable='gte(t,{at:.3f})':eof_action=pass[v]")


def thud_filter(at: float) -> str:
    """Bruit sourd de l'impact du tampon, synthétisé par ffmpeg (aucun fichier externe)."""
    return ("aevalsrc='0.9*sin(2*PI*55*t)*exp(-t*14)+0.3*(random(0)-0.5)*exp(-t*70)':d=0.6:s=44100,"
            f"adelay={int((at + 0.12) * 1000)}|{int((at + 0.12) * 1000)}")


def write_subtitles(cfg: dict, words: list[dict], path: Path, overlays: list[tuple] = ()):
    """Phrases mot à mot calées sur la voix (le mot prononcé s'affiche en jaune), plus des bandeaux."""
    r = cfg["render"]
    font, size = r["subtitle_font"], r["subtitle_size"]
    header = (
        "[Script Info]\nScriptType: v4.00+\n"
        f"PlayResX: {r['width']}\nPlayResY: {r['height']}\n\n"
        "[V4+ Styles]\n"
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,"
        "Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,"
        "Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
        f"Style: Default,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,"
        "0,0,0,0,100,100,1,0,1,8,4,8,50,50,1090,1\n"
        f"Style: Overlay,{font},{int(size * 1.3)},&H0000D7FF,&H0000D7FF,&H00000000,&H90000000,"
        "0,0,0,0,100,100,0,0,1,9,4,8,60,60,560,1\n"
        f"Style: Titre,{font},{int(size * 0.9)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,"
        "0,0,0,0,100,100,0,0,1,8,3,8,70,70,150,1\n"
        f"Style: Bandeau,{font},{int(size * 0.8)},&H00FFFFFF,&H00FFFFFF,&H000000D8,&H00000000,"
        "0,0,0,0,100,100,0,0,3,16,0,8,80,80,360,1\n"
        f"Style: Tampon,{font},120,&H002020D8,&H002020D8,&H002020D8,&H00000000,"
        "0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1\n\n"
        "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
    )
    lines = []
    chunks = _chunks(_bind_punctuation(words), r["words_per_caption"])
    for ci, chunk in enumerate(chunks):
        nxt = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else chunk[-1]["end"] + 0.4
        for k, w in enumerate(chunk):
            if k + 1 < len(chunk):
                end = chunk[k + 1]["start"]
            else:
                end = max(min(nxt, chunk[-1]["end"] + 0.6), w["end"])
            text = _reveal(chunk, k, r["subtitle_wrap"], k == len(chunk) - 1)
            lines.append(f"Dialogue: 0,{_ass_time(w['start'])},{_ass_time(end)},Default,,0,0,0,,{text}")
    for ov in overlays:
        start, end, text = ov[:3]
        style = ov[3] if len(ov) > 3 else "Overlay"
        lines.append(f"Dialogue: 1,{_ass_time(start)},{_ass_time(end)},{style},,0,0,0,,{text}")
    path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def render_scene(cfg: dict, work: Path, image: Path, clip: Path | None, dur: float, out: Path):
    r = cfg["render"]
    w, h, fps = r["width"], r["height"], r["fps"]
    if clip:
        # Zoom de 10 % rogné par le haut : retire le filigrane des clips téléchargés (coin bas droit).
        vf = (f"scale={int(w * 1.1)}:{int(h * 1.1)}:force_original_aspect_ratio=increase,"
              f"crop={w}:{h}:(iw-{w})/2:0,fps={fps},setsar=1")
        cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", clip.name, "-t", f"{dur:.3f}",
               "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", out.name]
    else:
        frames = max(int(dur * fps), 1)
        vf = (
            f"scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
            f"zoompan=z='min(zoom+0.0007,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={frames}:s={w}x{h}:fps={fps},setsar=1"
        )
        cmd = ["ffmpeg", "-y", "-i", image.name, "-vf", vf, "-frames:v", str(frames),
               "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", out.name]
    _run(cmd, work)


def assemble(cfg: dict, work: Path, scene_files: list[Path], audio: Path, subs: Path, out: Path,
             stamp_at: float | None = None):
    r = cfg["render"]
    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p.name}'\n" for p in scene_files), encoding="utf-8")
    _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt",
          "-c", "copy", "silent.mp4"], work)

    shutil.copy(ROOT / r["subtitle_fontfile"], work / "police.ttf")
    inputs = ["-i", "silent.mp4", "-i", audio.name]
    audio_map = "[1:a]anull[a]"
    if r.get("music_file"):
        music = Path(r["music_file"]).resolve()
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        audio_map = (f"[2:a]volume={r['music_volume']}[m];"
                     "[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]")
    elif stamp_at is not None:
        # aevalsrc est un filtre source : pas d'entrée -i, il se place dans le graphe
        audio_map = (f"{thud_filter(stamp_at)}[t];"
                     "[1:a][t]amix=inputs=2:duration=first:normalize=0[a]")
    video_map = f"[0:v]ass={subs.name}:fontsdir=.[v]"
    if stamp_at is not None:
        shutil.copy(make_stamp(ROOT / "assets" / "tampon.png"), work / "tampon.png")
        index = inputs.count("-i")
        inputs += ["-loop", "1", "-framerate", str(r["fps"]), "-t", "6", "-i", "tampon.png"]
        video_map = f"[0:v]ass={subs.name}:fontsdir=.[sub];" + stamp_filter(index, stamp_at)
    _run(["ffmpeg", "-y", *inputs,
          "-filter_complex", f"{video_map};{audio_map}",
          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
          "-movflags", "+faststart", out.name], work)
    from .validation import validate_duration
    validate_duration(out, max(60.0, float(r.get('minimum_duration_seconds', 60))))
