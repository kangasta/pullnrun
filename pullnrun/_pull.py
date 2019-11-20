from requests import get
from shutil import unpack_archive

from _utils import timestamp

def pull(url, headers=None, filename=None, extract=True):
	if not filename:
		filename = url.split('/')[-1]

	ok = True
	status = None

	start = timestamp()
	try:
		with get(url, headers=headers, stream=True) as r:
			r.raise_for_status()
			status = r.status_code

			with open(filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1<<20): # 1 MB
					if chunk: f.write(chunk)

		if extract:
			unpack_archive(filename)
	except:
		ok = False

	end = timestamp()

	return {
		'type': 'pull',
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
