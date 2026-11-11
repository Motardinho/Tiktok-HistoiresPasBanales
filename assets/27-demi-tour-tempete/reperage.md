# Dossier 27 - repérage des plans (11 novembre 2026)

- Pexels : recherches dans le navigateur (données de page), filtre 4K ou vertical natif >= 1080x1920 ; planches `planche-pexels*.jpg`, `cat-1..3.jpg`. HDR écartés : 28915818, 34180226, 38672746.
- YouTube CC : vidéos de voile en tempête toutes en 720p ou 1080p, donc écartées (règle qualité).
- Archive INA k791y4C_aGs (licence YouTube standard, choix de Marc) : coupes à 96,44 / 99,84 / 104,24 / 109,92 s. Zone utile 1520x860+200+110, filigrane ina.fr à partir de x = 1488.
- `arch-cadre-95.mp4` : extrait 95-111 s, image entière 1280x860 sur fond flou, posée à y = 330 :
  ffmpeg -ss 95 -i arch-k791y4C_aGs.mkv -t 16 -filter_complex "[0:v]crop=1280:860:200:110,split[a][b];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2,eq=brightness=-0.12[bg];[a]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:330,setsar=1,format=yuv420p" -an -c:v libx264 -crf 16 arch-cadre-95.mp4
- Non téléchargés (YouTube « Sign in to confirm you're not a bot ») : UmjAM3qvUew (France TV, documentaire 1996-97), ReWqMQtzW_k (« Closer To The Wind », Vendee Globe 1996 Rescue).
