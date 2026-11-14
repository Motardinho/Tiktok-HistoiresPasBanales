"""Affiche les mots et leurs débuts (timings-oraux.json du dossier 33)."""
import json

w = json.load(open('out/33-149-buts-contre-leur-camp/_montage/timings-oraux.json', encoding='utf8'))['words']
print(' '.join(f"{x['w']}@{x['start']:.2f}" for x in w))
