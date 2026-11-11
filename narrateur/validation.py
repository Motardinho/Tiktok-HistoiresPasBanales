"""Contrôle de la durée réelle avant livraison d'une vidéo du compte."""
import json
import subprocess
from pathlib import Path


def validate_duration(path: Path, minimum: float = 60.0) -> float:
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,duration',
         '-of', 'json', str(path.resolve())],
        check=True, capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    duration = float(data['format']['duration'])
    video = next((x for x in data.get('streams',[]) if x['codec_type']=='video'),None)
    if video is None:
        raise ValueError(f'Livraison refusée : {path.name} ne contient pas de vidéo.')
    video_duration = float(video.get('duration', duration))
    if video_duration < duration - .25:
        raise ValueError(f'Livraison refusée : les images de {path.name} finissent à '
                         f'{video_duration:.3f} s, avant la fin du fichier à {duration:.3f} s.')
    if not duration > minimum:
        raise ValueError(
            f'Livraison refusée : {path.name} dure {duration:.3f} s. '
            f'La vidéo doit dépasser strictement {minimum:g} s. '
            'Allonger la narration et le montage avec du contenu utile.'
        )
    return duration
