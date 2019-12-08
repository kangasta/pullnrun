from requests import get
from shutil import unpack_archive

try:
    import boto3
except ImportError:
    pass

from ._utils import timestamp, create_meta, filter_dict

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
        'type': 'pull_http',
        'ok': ok,
        'data': {
            'url': url,
            'file': filename,
            'status': status,
            'extracted': extract,
        },
        'meta': create_meta(start, end)
    }

def _pull_s3(bucket, object_name, filename=None):
    if not filename:
        filename = object_name

    ok = None

    try:
        s3 = boto3.client('s3')
    except NameError:
        pass

    start = timestamp()
    try:
        s3.download_file(bucket, object_name, filename)
        ok=True
    except:
        ok=False
    end = timestamp()

    return {
        'type': 'pull_s3',
        'ok': ok,
        'data': {
            'bucket': bucket,
            'object_name': object_name,
            'filename': filename,
        },
        'meta': create_meta(start, end)
    }

def pull(**kwargs):
    from_ = kwargs.get('from')

    if from_ == 'url':
        keys = ('url', 'headers', 'filename', 'extract')
        return _pull_http(**filter_dict(kwargs, keys))
    elif from_ == 's3':
        keys = ('bucket', 'object_name', 'filename')
        return _pull_s3(**filter_dict(kwargs, keys))
