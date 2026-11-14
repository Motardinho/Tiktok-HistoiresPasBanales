import json
from pathlib import Path
p=Path('out/45-origine-black-friday');p.mkdir(exist_ok=True)
texts=[
"Le Black Friday, c'était le cauchemar des flics !",
"Pour comprendre le nom de ta journée de promos, retour à Philadelphie, aux États-Unis, au début des années soixante. Le lendemain de Thanksgiving, les clients débarquent pour leurs achats de Noël.",
"Et ils ne sont pas seuls. Le grand match de football américain entre l'armée de terre et la marine attire aussi des visiteurs.",
"Résultat : des rues bondées, des bouchons, et des policiers qui enchaînent les heures. Pour eux, c'est un vendredi noir. Black Friday.",
"Sauf que ce surnom fait mauvais genre pour vendre des cadeaux. Alors les commerçants veulent changer son image.",
"Le détail savoureux ? En mille neuf cent soixante et un, une tentative de promouvoir le nom Big Friday est documentée. Le grand vendredi. Ça sonne tout de suite plus vendeur !",
"Mais c'est Black Friday qui finit par s'imposer. Et l'explication que tu as peut-être entendue arrive après.",
"Les magasins passeraient du rouge des pertes au noir des bénéfices. Une jolie histoire comptable pour rendre le nom positif.",
"Le cauchemar des policiers est devenu un argument de vente. Toi, Black Friday : bonnes affaires ou piège à achats ?",
"Abonne-toi pour la prochaine histoire. Pas banal, hein ?"
]
sources=[
dict(fait='Usage policier à Philadelphie, encombrement post-Thanksgiving',url='https://www.inquirer.com/philly/hp/news_update/Black_Friday_started_in_Philly.html'),
dict(fait='Rôle du match Army-Navy, longues journées des policiers',url='https://www.history.com/articles/black-friday-thanksgiving-origins-history'),
dict(fait='Public Relations News du 18 décembre 1961, promotion de Big Friday ; le nom Big Friday existait déjà avant 1961',url='https://barrypopik.com/blog/black_friday_big_friday'),
dict(fait='Explication comptable postérieure à l’usage policier ; ne pas dater arbitrairement son invention des années 1980',url='https://www.wgbh.org/news/local/2015-11-25/how-black-friday-got-its-name-its-not-what-you-think'),
dict(fait='Ne pas confondre avec le krach de 1869 ni nier l’usage de 1951 sur l’absentéisme ; récit centré sur la popularisation du nom commercial',url='https://barrypopik.com/blog/black_friday_big_friday')]
d=dict(numero=45,titre_fixe='BLACK FRIDAY : LE CAUCHEMAR DES FLICS',format='histoire',type_post='videos',variantes_demandees=['videos','photos'],scenes=[dict(narration=t,narration_voix=t.replace('Black Friday','Black Fraïdé').replace('Big Friday','Big Fraïdé').replace('Thanksgiving','Sanks guiving')) for t in texts],affichage={'black fraïdé':'Black Friday','big fraïdé':'Big Friday','sanks guiving':'Thanksgiving','mille neuf cent soixante et un':'1961'},sources_a_verifier=sources,fun_fact=dict(scene=5,fait='Promotion de Big Friday attestée en 1961',source=sources[2]['url']),reference='out/20-telephone-2899-dollars/version-validee/final.mp4',reference_fichier='out/20-telephone-2899-dollars/version-validee/final.mp4',reference_auteur='HPB téléphones, étalon visuel',statut='préparation : archives en contrôle',date_preparation='2026-11-14',tiktokabilite=dict(verdict='adapté sous réserve',limites='Archives historiques peu définies ; vérifier avant voix et montage. Film touristique Hagley repéré mais accès numérique bloqué par vérification humaine. Aucune archive prétendue du premier Black Friday.'))
(p/'histoire.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
(p/'script.txt').write_text('\n\n'.join(texts),encoding='utf8')
(p/'hooks.json').write_text(json.dumps([texts[0],'Ta journée de promos porte un surnom de policiers débordés.','Ils ont essayé de changer le nom du Black Friday.','Le vendredi noir devait devenir le grand vendredi.','Le Black Friday cachait une sacrée galère de circulation.'],ensure_ascii=False,indent=2),encoding='utf8')
print('mots',len(' '.join(texts).split()))
