from PIL import Image, ImageFont, ImageDraw
import pyimgur

CLIENT_ID = "91c4f749dfc0d86"


def find_size(text, isize):

    fs = 1  # starting size
    font = ImageFont.truetype('droid.ttf', fs)
    img_fraction = 0.80
    while font.getsize(text)[0] < img_fraction*isize:
        fs += 1
        font = ImageFont.truetype('droid.ttf', fs)

    return font


def text_to_image(imagefile, tquote, bquote):

    image = Image.open(imagefile)
    draw = ImageDraw.Draw(image)

    tfont = find_size(tquote, image.size[0])
    draw.text((image.size[0]*.10-2, 0), tquote, fill='black',
              font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10+2, 0), tquote, fill='black',
              font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10, 2), tquote, fill='black',
              font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10, -2), tquote, fill='black',
              font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10, 0), tquote, fill='white',
              font=tfont, anchor=image.size[0]/2)

    draw.text((image.size[0]*.10+2, image.size[1]*.90),
              bquote, fill='black', font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10-2, image.size[1]*.90),
              bquote, fill='black', font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10, image.size[1]*.90-2),
              bquote, fill='black', font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10, image.size[1]*.90+2),
              bquote, fill='black', font=tfont, anchor=image.size[0]/2)
    draw.text((image.size[0]*.10, image.size[1]*.90),
              bquote, fill='white', font=tfont, anchor=image.size[0]/2)

    image.save('result.png', 'PNG')


def upload(path, title, search):

    im = pyimgur.Imgur(CLIENT_ID)

    image_to_upload = im.upload_image(path=path, title=title)

    return image_to_upload.link
