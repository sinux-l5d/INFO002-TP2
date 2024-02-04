from PIL import Image, ImageDraw, ImageFont


def generate_diploma(diplome="master en alchimie", name="John Doe", date="01/01/1970", moyenne=10):
    img = Image.open("diplome-BG.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')

    W, H = img.size

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("sans.ttf", 32)
    title = "Diplôme master en alchimie"
    to = "Décerné à " + name
    date = "Le " + date
    moyenne = "Moyenne générale: " + str(moyenne) + "/20"

    # title
    _, _, w, h = draw.textbbox((0, 0), title, font=font, stroke_width=1)
    draw.text(((W - w) / 2, (H - h) / 4), title, font=font,
              fill=(0, 0, 0, 128), stroke_width=1)

    # name
    _, _, w, h = draw.textbbox((0, 0), to, font=font, stroke_width=0)
    draw.text(((W - w) / 2, (H - h) / 2.5), to, font=font,
              fill=(0, 0, 0, 128), stroke_width=0)

    # moyenne
    _, _, w, h = draw.textbbox((0, 0), moyenne, font=font, stroke_width=0)
    draw.text(((W - w) / 2, (H - h) / 1.9), moyenne, font=font,
              fill=(0, 0, 0, 128), stroke_width=0)

    # date
    _, _, w, h = draw.textbbox((0, 0), date, font=font, stroke_width=0)
    draw.text(((W - w) / 2, (H - h) / 1.5), date, font=font,
              fill=(0, 0, 0, 128), stroke_width=0)

    return img
