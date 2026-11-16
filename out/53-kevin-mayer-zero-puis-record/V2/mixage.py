"""Mixage sur une grille d'échantillons fixe, indépendante des horodatages des archives."""
import subprocess
import wave
from pathlib import Path

import numpy as np

from calage import FIN, REELS, REELS_T, VOIX
from plans import ECLAIRS, ENTREE, FINAL

TAUX = 48000


def ajouter(total, source, debut, duree, position, gain, entree, sortie, filtres=()):
    commande = ['ffmpeg', '-v', 'error', '-ss', str(debut), '-i', source, '-t', str(duree), '-vn']
    if filtres:
        commande += ['-af', ','.join(filtres)]
    commande += ['-ac', '2', '-ar', str(TAUX), '-f', 'f32le', '-']
    piste = np.frombuffer(subprocess.check_output(commande), dtype='<f4').reshape(-1, 2)
    depart = round(position * TAUX)
    piste = piste[:min(round(duree * TAUX), len(total) - depart)]
    temps = np.arange(len(piste)) / TAUX
    fondu = np.minimum(1, temps / entree) * np.minimum(1, (len(piste) / TAUX - temps) / sortie)
    niveau = gain(temps) if callable(gain) else gain
    total[depart:depart + len(piste)] += piste * (fondu * niveau)[:, None]


def rampe(temps, debut, duree):
    return np.clip((temps - debut) / duree, 0, 1)


def render_mix(chemin='_montage/mixage.wav'):
    total = np.zeros((round(FIN * TAUX), 2), dtype=np.float32)
    for position, debut, duree in VOIX:
        ajouter(total, 'voix.mp3', debut, duree, position, 3.1, .02, .04)
    for position, source, debut, duree, gain in REELS:
        ajouter(total, f'sources/{source}.mp4', debut, duree, position, gain, .09, .25)

    entree_piano = 1.40
    drapeau = ECLAIRS[0] - entree_piano
    ajouter(total, 'audio-v2/a-kind-of-hope-extrait.wav', 0, ENTREE - entree_piano, entree_piano,
            lambda t: .56 - .24 * rampe(t, drapeau - .12, .24), .65, .24)

    vestiaire = REELS_T['r3'] - ENTREE
    reprise = VOIX[2][0] - ENTREE
    sprint = FINAL - ENTREE
    coda = sprint + REELS[-1][3]
    def gain_talence(t):
        return (.58 - .435 * rampe(t, vestiaire - .33, .33) + .27 * rampe(t, reprise, .8)
                - .18 * rampe(t, sprint - 1.8, .30) + .01 * rampe(t, sprint, .25) - .17 * rampe(t, sprint + 6.55, .37)
                + .235 * rampe(t, coda, .42))

    ajouter(total, 'audio-v2/hunted-extrait.wav', 0, FIN - ENTREE, ENTREE,
            gain_talence, .055, .88, ('highpass=f=42',))
    plafond = .89
    crete = np.max(np.abs(total))
    if crete > plafond:
        total *= plafond / crete
    with wave.open(str(chemin), 'wb') as fichier:
        fichier.setparams((2, 2, TAUX, 0, 'NONE', 'not compressed'))
        fichier.writeframes((total * 32767).astype('<i2').tobytes())
    return str(chemin)


if __name__ == '__main__':
    print(render_mix())
