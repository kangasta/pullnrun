from requests import get
from shutil import unpack_archive

from ._utils import timestamp, create_meta

def _write_to_file(response, filename):
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1<<20): # 1 MB
            if chunk: f.write(chunk)

def _pull_http(url, headers=None, filename=None, extract=False):
    if not filename:
        filename = url.split('/')[-1]

    ok = None
    status = None

    start = timestamp()
    try:
        with get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            status = r.status_code
            ok = r.ok
            _write_to_file(r, filename)

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
        'meta': create_meta(start, end)
    }

def pull(**kwargs):
    from_ = kwargs.get('from')
    if from_ == 'url':
        keys = ('url', 'headers', 'filename', 'extract')
        return _pull_http(**{k: v for k, v in kwargs.items() if k in keys})
    elif from_ == 's3':
        raise NotImplementedError('TODO')
