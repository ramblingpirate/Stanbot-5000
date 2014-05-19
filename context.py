import simplejson, os, time
import requests

from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError

def get_image(search):

	search = search.replace(' ', '%20')
	baseURL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
				'v=1.0&q={}&start=0&imgSize=large'.format(search)

	r = requests.get(baseURL)
	results = simplejson.loads(r.text)

	url = results['responseData']['results'][0]['unescapedUrl']
	try:

		image_request = requests.get(url)

	except ConnectionError as e:

		print('\n> Uh-oh! We couldn\'t download {}'.format(url))

	title = 'result_no_text.jpg'
	try:

		image = Image.open(StringIO(image_request.content)).save(title, 'JPEG')

	except IOError as e:

		print('\n> Uh-oh! We couldn\'t save {}'.format(search))