import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'out/48-faid-evasion-helicoptere'
textes = [
    "Un hélicoptère vient chercher un détenu dans sa prison. Et un autre détenu filme son évasion.",
    "Premier juillet deux mille dix-huit. Prison de Réau, près de Paris. Le braqueur Rédoine Faïd est au parloir avec son frère.",
    "Pendant ce temps, ses complices arrivent par les airs. Le pilote a été pris en otage. Il est forcé de poser son appareil dans la cour.",
    "Un commando armé descend. Des fumigènes envahissent les lieux. À la disqueuse, les hommes ouvrent les portes pour atteindre le parloir.",
    "Et regarde ces images. Les caméras de surveillance enregistrent leur progression à l'intérieur de la prison.",
    "Le détail fou ? Faïd avait fait avancer sa visite au matin. Son prétexte ? Pouvoir regarder les matchs de la Coupe du monde.",
    "Quelques minutes plus tard, il repart en hélicoptère. Depuis sa cellule, un détenu filme l'appareil qui s'éloigne derrière les barreaux.",
    "L'hélicoptère est ensuite abandonné à Gonesse. Les enquêteurs le récupèrent. Mais Faïd, lui, reste en fuite jusqu'à son arrestation, en octobre.",
    "Trois mois de cavale. Quatorze ans de prison pour cette évasion. Tout ça pour trois mois dehors. Ça valait quoi, sa liberté ? Pas banal, hein ?"
]
affichage = {'Premier juillet deux mille dix-huit': '1er juillet 2018', 'Quatorze': '14', 'Trois': '3', 'trois': '3'}
sources = [
    ('Date, parloir, pilote pris en otage, fumigènes, disqueuse et prétexte du football', 'https://www.tf1info.fr/justice-faits-divers/video-proces-de-redoine-faid-braqueur-multi-recidiviste-les-images-inedites-d-une-evasion-hors-norme-2268658.html'),
    ('Prétexte du match pour avancer le parloir', 'https://www.rtl.fr/actu/justice-faits-divers/evasion-de-redoine-faid-il-a-decale-la-visite-de-son-frere-pour-soi-disant-voir-le-match-7793984041'),
    ('Vidéo filmée par un détenu', 'https://www.rtl.fr/actu/justice-faits-divers/video-redoine-faid-son-evasion-filmee-par-un-detenu-de-la-prison-7793955357'),
    ('Trois mois de cavale et condamnation à 14 ans en octobre 2023', 'https://www.tf1info.fr/justice-faits-divers/video-evasion-de-prison-en-2018-le-braqueur-redoine-faid-condamne-a-14-ans-de-prison-2274222.html')
]
scenes = []
for texte in textes:
    affichage_texte = texte
    for avant, apres in affichage.items():
        affichage_texte = affichage_texte.replace(avant, apres)
    scenes.append({'narration': affichage_texte, 'narration_voix': texte})
data = dict(numero=48, titre_fixe='IL S’ÉVADE EN HÉLICOPTÈRE', format='histoire', type_post='videos', scenes=scenes, affichage=affichage,
    chute_validee=textes[-1], autorisation='Sujet, chute et vraies images autorisés par Marc dans ce chat le 14 novembre 2026.',
    sources_a_verifier=[dict(fait=f, url=u, verification='Recherche web du 14 novembre 2026') for f,u in sources],
    fun_fact='Prétexte des matchs du Mondial pour avancer la visite au matin.',
    hooks_etudies=[textes[0], 'Il quitte sa prison en hélicoptère, sous les caméras.', 'Les barreaux ne suffisent pas quand les complices arrivent du ciel.', 'Un détenu filme. Devant lui, un autre s’évade en hélicoptère.', 'Cet hélicoptère vient chercher un prisonnier.'],
    tiktokabilite=dict(verdict='adapté sous réserve', preuves=['Planches LEnDeZyQV-I, vidéosurveillance du parloir, fumigènes et départ hélicoptère', 'Planches 5GKtCzNLoVo, vidéo filmée derrière les barreaux', 'Planches S6uGa2p7PfU, récupération du vrai appareil'], limites='Archives 720p, vidéosurveillance et téléphone de qualité limitée. Recadrages et plans finaux à contrôler.'), statut='préparation')
OUT.mkdir(exist_ok=True)
(OUT/'histoire.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
(OUT/'script.txt').write_text('\n\n'.join(s['narration'] for s in scenes), encoding='utf8')
print('Mots',len(' '.join(textes).split()))
if '--voix' in sys.argv:
    from produire_lot_16_18 import speech
    speech(OUT)
