from requests import request
from shutil import make_archive

from ._utils import timestamp, create_meta

def _push_http(filename, url, method='PUT', headers=None):
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
        },
        'meta': create_meta(start, end)
    }

def push(**kwargs):
    to = kwargs.get('to')
    if to == 'url':
        keys = ('filename', 'url', 'method', 'headers', )
        return _push_http(**{k: v for k, v in kwargs.items() if k in keys})
    elif to == 's3':
        raise NotImplementedError('TODO')
