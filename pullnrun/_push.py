from requests import request
from shutil import make_archive

from _utils import timestamp

def push(filename, url, method='PUT', headers=None):
	ok = True
	status = None

	start = timestamp()
	try:
		with open(filename, 'rb') as f:
			r = request(method, url, data=f, headers=headers)
			r.raise_for_status()
			status = r.status_code
	except:
		ok = False
	end = timestamp()

	return {
		'type': 'push',
		'ok': ok,
		'data': {
			'url': url,
			'status': status,
			'extracted': extract,
		},
		'meta': {
			'start': start,
			'end': end,
		}
	}
