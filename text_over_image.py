import os
from requests import exceptions
from PIL import Image, ImageFont, ImageDraw
import pyimgur

CLIENT_ID = "91c4f749dfc0d86"

def find_size(text, isize):

	fs = 1 #starting size
	font = ImageFont.truetype('droid.ttf', fs)
	img_fraction = 0.98
	while font.getsize(text)[0] < img_fraction*isize:
		fs += 1
		font = ImageFont.truetype('droid.ttf', fs)
	
	fs -= 1
	font = ImageFont.truetype('droid.ttf', fs)
	return font

def text_to_image(imagefile, tquote, bquote):

	image = Image.open(imagefile)
	draw = ImageDraw.Draw(image)
	
	tfont = find_size(tquote, image.size[0])
	draw.text((10-2,0), tquote, fill='black', font=tfont, anchor=image.size[0]/2)
	draw.text((10+2,0), tquote, fill='black', font=tfont, anchor=image.size[0]/2)
	draw.text((10,0), tquote, fill='white', font=tfont, anchor=image.size[0]/2)
	
	bfont = find_size(bquote, image.size[0])
	draw.text((-2, image.size[1]*0.8), bquote, fill='black', font=bfont, anchor=image.size[0]/2)
	draw.text((2, image.size[1]*0.8), bquote, fill='black', font=bfont, anchor=image.size[0]/2)
	draw.text((0,image.size[1]*0.8), bquote, fill='white', font=bfont, anchor=image.size[0]/2)
	
	image.save('result.png', 'PNG')

def upload(path, title, search):
	im = pyimgur.Imgur(CLIENT_ID)
	
	image_to_upload = im.upload_image(path=path,title=title)

	return image_to_upload.link

