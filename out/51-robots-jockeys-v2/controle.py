import cv2
from PIL import Image, ImageDraw, ImageFont

from montage import PLANS, ROOT, WORK


def font(size):
    return ImageFont.truetype('C:/Windows/Fonts/arial.ttf', size)


def frame(video, time):
    video.set(cv2.CAP_PROP_POS_FRAMES, round(time * 25))
    ok, pixels = video.read()
    if not ok:
        raise RuntimeError(f'Image illisible à {time:.2f} s')
    return Image.fromarray(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB))


def phone(video, times):
    sheet = Image.new('RGB', (1080, 665), '#181a1e')
    for i, time in enumerate(times):
        image = frame(video, time).convert('RGBA')
        ui = Image.new('RGBA', image.size)
        draw = ImageDraw.Draw(ui)
        draw.rounded_rectangle((65, 55, 1010, 160), 24, fill=(20, 20, 20, 175))
        draw.text((105, 82), 'Rechercher', font=font(46), fill='white')
        draw.rectangle((0, 1410, 1080, 1920), fill=(0, 0, 0, 165))
        draw.text((55, 1440), '@histoirespasbanales', font=font(46), fill='white')
        draw.text((55, 1510), 'En 2005, sept dromadaires prennent le départ…', font=font(35), fill='white')
        draw.text((55, 1705), 'Son original', font=font(35), fill='white')
        for y, label in [(850, 'Profil'), (1020, 'J’aime'), (1190, 'Com.'), (1360, 'Partager')]:
            draw.ellipse((963, y, 1035, y + 72), fill=(255, 255, 255, 215))
            draw.text((945, y + 75), label, font=font(28), fill='white')
        sheet.paste(Image.alpha_composite(image, ui).convert('RGB').resize((360, 640)), (i*360, 25))
        ImageDraw.Draw(sheet).text((i*360+10, 5), f'{time:.2f} s - simulation TikTok', font=font(14), fill='white')
    sheet.save(WORK/'apercu-tiktok.jpg', quality=94)


def main():
    directory = WORK / 'controle'
    directory.mkdir(exist_ok=True)
    video = cv2.VideoCapture(str(WORK / 'final.mp4'))
    for batch in range(4):
        sheet = Image.new('RGB', (1296, 550), '#181a1e')
        draw = ImageDraw.Draw(sheet)
        for k, (end, *_) in enumerate(PLANS[batch*6:batch*6+6]):
            i = batch*6 + k
            start = PLANS[i-1][0] if i else 0
            for j, time in enumerate([start, (start+end)/2, end-.08]):
                x, y = (k%3*3+j)*144, (k//3)*275
                sheet.paste(frame(video, time).resize((144, 256)), (x, y))
                draw.text((x+4, y+256), f'{i+1:02} / {time:.2f} s', fill='white', font=font(14))
        sheet.save(directory/f'plans-{batch+1}.jpg', quality=92)
    phone(video, [0, 36.28, 61.9])
    hook = Image.new('RGB', (1080, 665), '#181a1e')
    for i, time in enumerate([0, .4, .8, 1.24, 1.68, 2.1, 2.52, 2.96, 3.68, 4.08, 4.52, 4.92]):
        x, y = (i%6)*180, (i//6)*332
        hook.paste(frame(video, time).resize((180, 320)), (x, y))
        ImageDraw.Draw(hook).text((x+4, y+320), f'{time:.2f}', font=font(12), fill='white')
    hook.save(directory/'accroche-0-5.jpg', quality=94)
    video.release()
    reference = ROOT / 'identite/histoires-pas-banales/modeles-miniatures/09-pogba-magazine.png'
    items = [('Source', WORK/'miniature-brut.png'), ('Réglages photo', WORK/'miniature-reglee.jpg'),
             ('Miniature V2', WORK/'miniature.jpg'), ('Modèle magazine', reference)]
    proof = Image.new('RGB', (1440, 665), '#181a1e')
    for i, (label, path) in enumerate(items):
        photo = Image.open(path).convert('RGB')
        photo.thumbnail((360, 640))
        proof.paste(photo, (i*360+(360-photo.width)//2, 25))
        ImageDraw.Draw(proof).text((i*360+10, 5), label, font=font(14), fill='white')
    proof.save(directory/'miniature-avant-apres.jpg', quality=94)


if __name__ == '__main__':
    main()
