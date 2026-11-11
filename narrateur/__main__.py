import argparse
import json
import re
import unicodedata
from pathlib import Path

import yaml
from dotenv import load_dotenv

from . import assemble, images, story, video, voice

ROOT = Path(__file__).resolve().parent.parent


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "histoire"


def main():
    ap = argparse.ArgumentParser(description="Génère une vidéo TikTok narrée par une voix IA.")
    ap.add_argument("--sujet", help="Sujet de l'histoire (sinon choisi par l'IA)")
    ap.add_argument("--format", choices=["histoire", "top", "fait"], default="histoire",
                    help="Type de vidéo : histoire narrée, top (classement) ou fait court")
    ap.add_argument("--brouillon", action="store_true",
                    help="Sans clé API : voix Edge TTS, fonds dégradés, pas d'animation")
    ap.add_argument("--fonds-degrades", action="store_true",
                    help="Vraie voix, mais fonds dégradés au lieu d'images générées (sans clé OpenAI)")
    ap.add_argument("--dossier", help="Reprendre un dossier existant dans out/")
    ap.add_argument("--script-seulement", action="store_true", help="S'arrêter après le script")
    ap.add_argument("--sans-video", action="store_true", help="Images animées par ffmpeg uniquement")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    out_root = ROOT / "out"
    out_root.mkdir(exist_ok=True)

    if args.dossier:
        work = out_root / args.dossier
        data = json.loads((work / "histoire.json").read_text(encoding="utf-8"))
    else:
        done = [p.name for p in out_root.iterdir() if p.is_dir()]
        print("1/5 Écriture du script...")
        data = story.write_story(cfg, args.sujet, done, args.format)
        numbers = []
        for folder in out_root.iterdir():
            if not folder.is_dir():
                continue
            prefix = re.match(r"^(\d+)-", folder.name)
            if prefix:
                numbers.append(int(prefix.group(1)))
            existing_script = folder / "histoire.json"
            if existing_script.exists():
                existing = json.loads(existing_script.read_text(encoding="utf-8"))
                if isinstance(existing.get("numero"), int):
                    numbers.append(existing["numero"])
        data["numero"] = max(numbers, default=0) + 1
        work = out_root / f"{data['numero']:02d}-{slugify(data['titre'])}"
        work.mkdir(exist_ok=True)
        (work / "histoire.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(f"   « {data['titre']} » -> {work}")
    print(f"   Hook : {data['hook']}")
    if args.script_seulement:
        return

    scenes = data["scenes"]
    print("2/5 Voix " + ("Edge TTS (brouillon)" if args.brouillon else "ElevenLabs") + "...")
    audio = work / "voix.mp3"
    timing_file = work / "timings.json"
    if audio.exists() and timing_file.exists():
        timing = json.loads(timing_file.read_text(encoding="utf-8"))
    else:
        synth = voice.synthesize_edge if args.brouillon else voice.synthesize
        timing = synth(cfg, scenes, audio)
        timing_file.write_text(json.dumps(timing, ensure_ascii=False), encoding="utf-8")

    print("3/5 Images...")
    cartes = args.brouillon or args.fonds_degrades
    if cartes:
        imgs =[images.card(cfg, i, work / f"img{i:02d}.png") for i in range(len(scenes))]
    else:
        imgs = [images.generate_image(cfg, s["image_prompt"], work / f"img{i:02d}.png")
                for i, s in enumerate(scenes)]

    print("4/5 Animations...")
    clips = []
    for i, s in enumerate(scenes):
        clip = None
        manual = work / f"clip{i:02d}.mp4"
        if manual.exists():  # séquence vidéo fournie (Kling, Veo, banque libre de droits)
            clips.append(manual)
            continue
        if s.get("animate") and not (args.sans_video or cartes):
            clip = video.animate(cfg, imgs[i], s.get("motion_prompt", ""), work / f"clip{i:02d}.mp4")
        clips.append(clip)

    print("5/5 Montage...")
    subs = work / "sous-titres.ass"
    durations = timing["scene_durations"]
    overlays = [(0.0, min(2.5, durations[0]), f"DOSSIER N°{data.get('numero', 1)}")]
    cursor = 0.0
    for s, dur in zip(scenes, durations):
        if s.get("bandeau"):  # bandeau rouge : critère ou précision de la scène
            overlays.append((cursor, cursor + dur, s["bandeau"].upper(), "Bandeau"))
        if s.get("rang") is not None:
            overlays.append((cursor, cursor + dur, f"N°{s['rang']}"))
        elif s.get("texte_ecran") and cursor > 2.5:
            overlays.append((cursor, cursor + dur, s["texte_ecran"]))
        cursor += dur
    if data.get("titre_fixe"):
        overlays.append((0.0, sum(durations), data["titre_fixe"].upper(), "Titre"))
    stamp_at = assemble.stamp_time(timing["words"])  # tampon « DOSSIER CLOS » au mot « clos »
    assemble.write_subtitles(cfg, timing["words"], subs, overlays)
    scene_files = []
    for i, dur in enumerate(timing["scene_durations"]):
        f = work / f"scene{i:02d}.mp4"
        assemble.render_scene(cfg, work, imgs[i], clips[i], dur, f)
        scene_files.append(f)
    final = work / "final.mp4"
    assemble.assemble(cfg, work, scene_files, audio, subs, final, stamp_at)

    (work / "publication.txt").write_text(
        f"{data['legende']}\n\n{' '.join(data['hashtags'])}\n\n"
        "À vérifier avant publication :\n- " + "\n- ".join(data.get("sources_a_verifier", [])),
        encoding="utf-8",
    )
    from comparer_lot_16_18 import compare
    compare(work)
    print(f"Terminé : {final}\nComparaison : {work / 'comparaison.mp4'}")


if __name__ == "__main__":
    main()
